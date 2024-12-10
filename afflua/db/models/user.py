from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

class UserModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    username: str
    email: EmailStr
    role: str
    wallet_address: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

