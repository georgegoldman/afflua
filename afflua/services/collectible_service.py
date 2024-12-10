from aleaf.schemas.collectible import CollectibleCreate, CollectibleResponse
from aleaf.db.connection import get_collection
from bson import ObjectId
from aleaf.core.security import settings
from typing import List

db = get_collection(settings.DB_NAME)

# Create a collectible
async def create_collectible(collectible_data: CollectibleCreate) -> CollectibleResponse:
    collectible_dict = collectible_data.dict()
    result = await db["collectibles"].insert_one(collectible_dict)
    return CollectibleResponse(id=str(result.inserted_id), **collectible_data.dict())

# Retrieve a collectible by its ID
async def get_collectible_by_id(collectible_id: str) -> CollectibleResponse:
    collectible = await db["collectibles"].find_one({"_id": ObjectId(collectible_id)})
    if collectible:
        return CollectibleResponse(id=collectible_id, **collectible)
    return None  # Return None if collectible not found

# Retrieve collectibles by a user's ID
async def get_collectibles_by_user(user_id: str) -> List[CollectibleResponse]:
    collectibles = await db["collectibles"].find({"user_id": user_id}).to_list(None)
    return [CollectibleResponse(id=str(collectible["_id"]), **collectible) for collectible in collectibles]

# Transfer a collectible to another user
async def transfer_collectible(collectible_id: str, current_owner_id: str, new_owner_id: str) -> bool:
    collectible = await db["collectibles"].find_one({"_id": ObjectId(collectible_id)})

    # Verify ownership before transfer
    if collectible and collectible["user_id"] == current_owner_id:
        result = await db["collectibles"].update_one(
            {"_id": ObjectId(collectible_id)},
            {"$set": {"user_id": new_owner_id}}
        )
        return result.modified_count == 1  # Return True if transfer successful
    return False  # Return False if collectible not found or transfer unauthorized

# Mint a collectible as an NFT
async def mint_collectible(collectible_id: str) -> bool:
    result = await db["collectibles"].update_one(
        {"_id": ObjectId(collectible_id)}, {"$set": {"is_minted": True}}
    )
    return result.modified_count == 1
