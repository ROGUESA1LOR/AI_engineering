import json
import os
import subprocess
import dotenv

model = "llama3.1:8b"
username = "ROGUESA1LOR"
repo = "AI_engineering"

dotenv.load_dotenv() 
token = os.environ.get("GITHUB_TOKEN") 


print("Polling GitHub Actions API...")
url = f"https://api.github.com/repos/{username}/{repo}/actions/runs"
proc = subprocess.run(
    ["curl", "-s", "-H", f"Authorization: Bearer {token}", "-H", "User-Agent: python", url], 
    capture_output=True, text=True, check=True
)

try:
    data = json.loads(proc.stdout)
except json.JSONDecodeError:
    print("API error block: received bad text instead of json")
    exit(1)

run_node = data["workflow_runs"][0]
run_id = run_node["id"]
status = run_node["conclusion"]

print(f"Downloading authenticated logs for run {run_id}...")
log_url = f"https://api.github.com/repos/{username}/{repo}/actions/runs/{run_id}/logs"

# Added the Authorization header to bypass the 403 block perfectly
subprocess.run(
    ["curl", "-L", "-s", "-H", f"Authorization: Bearer {token}", "-H", "User-Agent: python", log_url, "--output", "logs.zip"], 
    check=True
)
subprocess.run(["unzip", "-o", "logs.zip", "-d", "extracted_logs"], capture_output=True)

# Bruting text extraction
err_text = ""
if os.path.exists("extracted_logs"):
    for f_name in os.listdir("extracted_logs"):
        if f_name.endswith(".txt"):
            with open(os.path.join("extracted_logs", f_name), "r", errors="ignore") as log_f:
                content = log_f.read()
                if "broken_script" in content or "Traceback" in content or "exit status" in content:
                    err_text += f"--- FILE: {f_name} ---\n" + content + "\n"

if not err_text:
    err_text = "No explicit errors found."

if os.path.exists("state.json"):
    with open("state.json", "r") as f:
        db = json.load(f)
else:
    db = {"history": []}

prompt = f"""
[IDENTITY: Classifier]
[RULE: Classify this real GitHub Action failure log. Output ONLY a valid raw JSON dictionary with keys 'is_flake' (true/false), 'category', and 'reason'. No backticks or talk.]
[LOG]
{err_text[:4000]}
[/LOG]
"""

print("Streaming to ollama core...")
ai_proc = subprocess.run(["ollama", "run", model, prompt], capture_output=True, text=True)
ai_out = ai_proc.stdout.strip()

try:
    verdict = json.loads(ai_out)
except json.JSONDecodeError:
    verdict = {"error": "bad syntax", "raw": ai_out}

node = {
    "run_id": run_id,
    "status": status,
    "log": "Real cloud traceback extracted successfully",
    "verdict": verdict
}
db["history"].append(node)

with open("state.json", "w") as f:
    json.dump(db, f, indent=2)

print("\n--- DONE ---")
subprocess.run(["cat", "state.json"])
