from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import subprocess
#import webbrowser
import requests

app = FastAPI()
history = []  
system_instruction = """
    You are an AI system with access to a terminal command tool.
    If the user asks for the time, you MUST execute the clock tool by replying with EXACTLY this JSON block:
    {"action": "get_time"}
    
    If the user is just saying hi or talking about something else, respond with normal text. Do not use JSON unless needed.
    """

# webbrowser.open("http://127.0.0.1:8000")
class ChatPayload(BaseModel):
    prompt: str

# @app.get("/", response_class=HTMLResponse)
# def home():
#     with open("templates/index.html", "r") as file:
#         return file.read()
@app.get("/health")
def health_check():
    return {"status": "ok"}
@app.post("/chat")
def chat(data: ChatPayload): # FastAPI automatically grabs this from the JS fetch URL!
    history.append({"role":"system", "content": system_instruction})
    history.append({"role": "user", "content": data.prompt})  
    payload = {
        "model": "llama3.1:8b", 
        "messages": history, 
        "stream": False,
        "format": "json" }
    output = requests.post("http://127.0.0.1:11434/api/chat", json=payload).json()
    history.append(output["message"])
    # Send a clean data dictionary straight back to JavaScript
    return {"message": output["message"]["content"]}
