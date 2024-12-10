from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class MessageModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    sender_id: str
    receiver_id: str
    content: str
    timestamp: Optional[str] = None
    is_ai_response: Optional[bool] = False

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}