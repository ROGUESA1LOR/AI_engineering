import ollama

import tools
import history

chatlog=history.get_history()
def chatbot(chatlog):
    return ollama.chat(model="qwen2.5:14b-instruct-q4_K_M",messages=chatlog,tools=[tools.get_current_time])