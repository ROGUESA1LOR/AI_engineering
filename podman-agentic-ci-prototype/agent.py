import json
import os
import subprocess

model = "llama3.1:8b"
username = "ROGUESA1LOR"
repo = "AI_engineering"

# fetch raw api
print("Polling GitHub Actions API...")
url = f"https://github.com/{username}/{repo}/actions/runs"
proc = subprocess.run(["curl", "-s", "-H", "User-Agent: python", url], capture_output=True, text=True, check=True)

try:
    data = json.loads(proc.stdout)
except json.JSONDecodeError:
    print("API Error: Received invalid non-JSON string data from GitHub!")
    print(proc.stdout)
    exit(1)

# stop crash if empty
if "workflow_runs" not in data or not data["workflow_runs"]:
    print(f"Zero workflow runs found for {username}/{repo} yet!")
    print("Make sure you pushed your .github/workflows/ci.yml file to GitHub.")
    exit(0)

# target first array element
run_node = data["workflow_runs"][0]
run_id = run_node["id"]
status = run_node["conclusion"]

# grab zip archive
print(f"Downloading logs for run {run_id}...")
log_url = f"https://github.com/{username}/{repo}/actions/runs/{run_id}/logs"
subprocess.run(["curl", "-L", "-s", "-H", "User-Agent: python", log_url, "--output", "logs.zip"], check=True)
subprocess.run(["unzip", "-o", "logs.zip", "-d", "extracted_logs"], capture_output=True)

# isolate text walls
err_text = ""
if os.path.exists("extracted_logs"):
    for f_name in os.listdir("extracted_logs"):
        if f_name.endswith(".txt"):
            with open(os.path.join("extracted_logs", f_name), "r") as log_f:
                for line in log_f:
                    if any(x in line for x in ["##[error]", "FATAL", "Error:", "exit status"]):
                        err_text += line.strip() + "\n"

if not err_text:
    err_text = "No explicit errors found."

# read memory db
if os.path.exists("state.json"):
    with open("state.json", "r") as f:
        db = json.load(f)
else:
    db = {"history": []}

# build payload fence
prompt = f"""
[IDENTITY: Classifier]
[RULE: Classify this real GitHub Action failure log. Output ONLY a valid raw JSON dictionary with keys 'is_flake' (true/false), 'category', and 'reason'. No backticks or talk.]
[LOG]
{err_text}
[/LOG]
"""

print("Streaming to ollama core...")
ai_proc = subprocess.run(["ollama", "run", model, prompt], capture_output=True, text=True)
ai_out = ai_proc.stdout.strip()

try:
    verdict = json.loads(ai_out)
except json.JSONDecodeError:
    verdict = {"error": "bad syntax", "raw": ai_out}

# append node transaction
node = {
    "run_id": run_id,
    "status": status,
    "log": err_text,
    "verdict": verdict
}
db["history"].append(node)

with open("state.json", "w") as f:
    json.dump(db, f, indent=2)

print("\n--- DONE ---")
subprocess.run(["cat", "state.json"])
