from fastapi import FastAPI, HTTPException
import requests

from app.prompts import SYSTEM_PROMPT
from app.models.schemas import AskRequest
from app.services.data_service import load_jobs
from app.services.data_service import load_jobs, search_jobs

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"


@app.get("/")
def home():
    return {
        "message": "AI Job Assistant Running!"
    }


@app.post("/ask")
def ask(request: AskRequest):

    query = request.query.lower()
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

    print("Your Query:::::", request.query)

    try:
      # print("Query sent:::::")
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi",
                "prompt": full_prompt,
                "stream": False
            }
            
        )
       

        data = response.json()
        print("Response received:::::", data["response"])

        return {
            "response": data["response"]
        }

    except Exception as e:
        print("Exception occurred:::::", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/jobs")
def get_jobs():

    jobs = load_jobs()

    return jobs



@app.get("/search")
def search(skill: str):

    results = search_jobs(skill)

    return {
        "results": results
    }