from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class TransactionModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    collectible_id: str
    amount: float
    status: str
    timestamp: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}