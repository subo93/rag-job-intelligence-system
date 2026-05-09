from fastapi import FastAPI, HTTPException
import requests

from app.prompts import SYSTEM_PROMPT
from app.models.schemas import AskRequest

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"


@app.get("/")
def home():
    return {
        "message": "AI Job Assistant Running!"
    }


@app.post("/ask")
def ask(request: AskRequest):
    print("before query:::::::::::::::::::::::::")

    query = request.query.lower()
    print("after query:::::::::::::::::::::::::")
    job_keywords = [
        "job",
        "salary",
        "skills",
        "developer",
        "python",
        "react",
        "backend",
        "frontend"
    ]
    print   ("after keywords:::::::::::::::::::::::::")

    if not any(word in query for word in job_keywords):

        raise HTTPException(
            status_code=400,
            detail="Only job-related queries are allowed."
        )
#    // print("system prompt" + SYSTEM_PROMPT)

    full_prompt = f"""
    {SYSTEM_PROMPT}


    User Question:
    {request.query}
    """

    try:
        print("seding response:::::::::::::::::::::::::")
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi",
                "prompt": full_prompt,
                "stream": False
            }
            
        )
        print  ("after response:::::::::::::::::::::::::")

        data = response.json()

        return {
            "response": data["response"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )