from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import handle_user_message

app = FastAPI(
    title="AI Booking Assistant",
    description="Book meetings via natural language using Gemini + Google Calendar",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    user_input: str

@app.get("/")
def read_root():
    return {"message": "✅ Welcome to the AI Booking Agent!"}

@app.post("/chat")
def chat_with_agent(request: ChatRequest):
    try:
        response = handle_user_message(request.user_input)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
