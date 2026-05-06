from fastapi import FastAPI
import requests

app = FastAPI()

OLLAMA_URL ="http://localhost:11434/api/generate"


@app.get("/")
def home():
    return {"message": "AI Job Assistant Running!"}


@app.get("/ask")
def ask(query:str):

    response =requests.post(OLLAMA_URL,
                             json={"model": "phi", "prompt": query,"stream": False},)
    data =response.json()

    return{
        "query": query,
        "answer":data["response"]
    }