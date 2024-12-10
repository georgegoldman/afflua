from pydantic import BaseModel
from typing import List, Optional

class CollectibleBase(BaseModel):
    title: str
    description: Optional[str]
    creator_id: str
    tags: Optional[List[str]] = []

class CollectibleCreate(CollectibleBase):
    media_url: str # URL to the stored media on IPFS or other storage

class CollectibleResponse(CollectibleBase):
    id:str
    is_minted: bool
    created_at: str