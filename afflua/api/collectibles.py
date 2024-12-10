from fastapi import APIRouter, HTTPException
from aleaf.schemas.collectible import CollectibleCreate, CollectibleResponse
from aleaf.services.collectible_service import create_collectible, get_collectible_by_id

router = APIRouter()

# Create collectible (art, music, experience, etc.)
@router.post("/collectibles/", response_model=CollectibleResponse)
async def create_new_collectible(collectible_data: CollectibleCreate):
    collectible = await create_collectible(collectible_data)
    return collectible

# Get collectible by ID
@router.get("/collectibles/{collectible_id}", response_model=CollectibleResponse)
async def get_collectible(collectible_id: str):
    collectible = await get_collectible_by_id(collectible_id)
    if collectible is None:
        raise HTTPException(status_code=404, detail="Collectible not found")
    return collectible
