from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class CollectibleModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    owner_id: str
    metadata_url: str
    token_id: str
    price: float
    created_at: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
