from fastapi import FastAPI
from pydantic import BaseModel
import model
import history


app=FastAPI()

class payload(BaseModel):
    prompt: str


@app.get("/")
def life():
    return {"message": "Hello World"}
@app.post("/chatbot")
def chatbot_node(data:payload):
    new_message={"role" : "user","content":data.prompt}
    history.save_history(new_message)
    savemodel_response=model.chatbot(history.get_history())
    clean_model_response=savemodel_response["message"].model_dump()

    history.save_history(clean_model_response)
    if clean_model_response.get("tool_calls"):
        print("🤖 Intercepting tool request...")
        
        for tool_call in clean_model_response["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            
            # Catch the pre-formatted dictionary directly from model.py!
            tool_payload = model.get_toolcalls_result(tool_name)
            
            if tool_payload:
                # Save the complete tool payload checkpoint directly to history
                history.save_history(tool_payload)
        
        # 4. RESYNTHESIS: Call the model again with the fresh tool history loaded
        print("🧠 Re-invoking model with tool data...")
        second_model_response = model.chatbot(history.get_history())
        clean_second_response = second_model_response["message"].model_dump()
        
        history.save_history(clean_second_response)
        return {"response": clean_second_response["content"]}
        
    # If no tools were required, return text directly
    return {"response": clean_model_response["content"]}