from pydantic import BaseModel
from typing import Optional

class ChatMessage(BaseModel):
    sender: str # "user" or "AI"
    message: str
    timestamp: str

class ChatRequest(BaseModel):
    user_id: str
    message: str
    
class ChatResponse(BaseModel):
    response: str
    timestamp: str
