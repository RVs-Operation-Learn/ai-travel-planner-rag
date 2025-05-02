import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
from retriever import retrieve_travel_info
from chat import generate_answer
import logging

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
openai_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow frontend to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware for question limit tracking
app.add_middleware(SessionMiddleware, secret_key=openai_key)

# --- Models ---

class PlanRequest(BaseModel):
    city: str
    budget: int

class ChatRequest(BaseModel):
    query: str
    city: str

# --- Endpoints ---

@app.post("/plan")
async def plan_trip(plan_request: PlanRequest):
    city = plan_request.city
    budget = plan_request.budget

    print(f"Received city: {city}, budget: {budget}")
    query = f"Things to do in {city}"

    info = retrieve_travel_info(query, city)
    return {
        "plan": f"Here's your travel plan for {city} with a budget of ₹{budget}:\n\n{info}"
    } if info else {"plan": "Sorry, we couldn't find information for that city."}

@app.post("/chat")
def chat(chat_request: ChatRequest, request: Request):
    session = request.session

    if "chat_count" not in session:
        session["chat_count"] = 0

    if session["chat_count"] >= 3:
        return {"message": "Limit reached. Only 3 questions allowed."}

    session["chat_count"] += 1
    answer = generate_answer(chat_request.query, chat_request.city)
    return {"results": answer}
