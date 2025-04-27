from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from retriever import retrieve_travel_info  # Import the retrieve function

app = FastAPI()

# Pydantic model to validate the input request data (query and city)
class TravelRequest(BaseModel):
    query: str
    city: str

# Simple session to hold conversation state (just a demo)
class ChatSession:
    def __init__(self):
        self.history = []

    def add_message(self, message: str):
        self.history.append(message)

    def get_history(self):
        return " ".join(self.history)

# Initialize chat session
chat_sessions = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Travel Planner!"}

@app.post("/retrieve_travel_info")
def get_travel_info(request: TravelRequest):
    """
    Accepts a query and city, returns top-k relevant travel info for that city.
    """
    try:
        results = retrieve_travel_info(request.query, city=request.city)
        if not results:
            raise HTTPException(status_code=404, detail="No results found.")
        return {"city": request.city, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_with_bot(request: TravelRequest):
    """
    This is the chatbot interaction API where users can ask questions about travel.
    """
    try:
        # Check if the user has a session, if not, create a new one
        if request.city not in chat_sessions:
            chat_sessions[request.city] = ChatSession()

        # Get the session for the city (context for chat)
        session = chat_sessions[request.city]
        
        # Retrieve travel information based on the user's query
        results = retrieve_travel_info(request.query, city=request.city)
        
        # Add user query and bot response to chat history
        session.add_message(f"User: {request.query}")
        session.add_message(f"Bot: {', '.join(results)}")

        # Limit to 3 questions for the demo
        if len(session.history) // 2 >= 3:  # Each interaction (user + bot) takes two entries in history
            return {"message": "Thanks for chatting! Your session has ended."}

        return {"session_history": session.get_history(), "results": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
