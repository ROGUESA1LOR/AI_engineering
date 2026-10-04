import json
import os


system_message=[
    {
        "role": "system", 
        "content": (
            "You are a precise, lightweight system assistant. You have access to a suite of local tools.\n"
            "CRITICAL RULES:\n"
            "1. ONLY invoke a tool if the user's prompt explicitly requests data that requires it.\n"
            "2. For generic greetings, casual conversation, or open-ended questions, DO NOT trigger a tool call. Respond using normal conversational text.\n"
            "3. If a tool call is unnecessary, leave the 'tool_calls' configuration empty."
        )
    }
]
def get_history():
    if not os.path.exists("history.json"):
        with open("history.json","w") as f:
            json.dump(system_message,f,indent=4)
    with open("history.json","r") as f:
        data=json.load(f)
    return data 


def save_history(data):
    with open("history.json","r") as f:
        history=json.load(f)
        history.append(data)
    with open("history.json","w") as f:
        json.dump(history,f,indent=4)
