from fastapi import FastAPI
import os
import dotenv

app=FastAPI()
def load_dotenv():
    dotenv.load_dotenv()
    api_key = os.getenv("API_KEY")
    return api_key
def user_input():pass
def send_input():pass
def response():pass