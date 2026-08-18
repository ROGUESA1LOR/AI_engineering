import subprocess
import json
import os
# subprocess.run()
# model="llama3.1:8b"
# userinput=str(input("Enter your input for model: "))
# ai_process=subprocess.run(["ollama", "run",model,userinput] , capture_output=True , text=True)
# ai_response=ai_process.stdout.strip()
# if os.path.exists("state.json"):
#     with open ("state.json","r") as f:
#         mydict=json.load(f)
# else:
#     mydict={
#         "Model": model,
#         "history":[]
#     }
# history= {
#     "Userinput": userinput,
#     "AI Response": ai_response
#     }
# mydict["history"].append(history)

# with open("state.json", "w") as f:
#     json.dump(mydict,f,indent=2)
# subprocess.run(["cat","state.json"])
with open ("mock_failed_log.txt","r") as f:
    log_lines=f.readlines()
