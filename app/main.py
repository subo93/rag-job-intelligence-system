from fastapi import FastAPI, HTTPException
import requests

from app.prompts import SYSTEM_PROMPT
from app.models.schemas import AskRequest
from app.services.data_service import (
    load_jobs,
    search_jobs,
    format_jobs_context
)

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

@app.post("/search-ai")
def search_ai(request: AskRequest):

    query = request.query

    matched_jobs = []

    if "python" in query.lower():

        matched_jobs = search_jobs("python")

    elif "react" in query.lower():

        matched_jobs = search_jobs("react")

    context = format_jobs_context(matched_jobs)

    full_prompt = f"""
    {SYSTEM_PROMPT}

    Context:
    {context}

    User Question:
    {query}
    """

    try:
        print("Full Prompt Sent to AI:::::::::", full_prompt)

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi",
                "prompt": full_prompt,
                "stream": False
            }
        )

        data = response.json()

        return {
            "matched_jobs": matched_jobs,
            "ai_response": data["response"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )