from aleaf.db.connection import get_collection
from aleaf.schemas.nft_model import NFTCreate, NFTResponse #type: ignore
from bson import ObjectId

collection = get_collection("nft")

async def create_nft(nft:NFTCreate ) -> NFTResponse:
    result = await collection.insert_one(nft)

    return NFTResponse(token_id=int(result.inserted_id), **nft.model_dump())

async def view_all_nft() -> list[NFTResponse]:
    ntfs_cursor =  collection.find() # Fetch all documents
    ntfs = await ntfs_cursor.to_list(length=None) # Convert cursor to a list
    return [NFTResponse(token_id=nft["tokenj_id"], **nft) for nft in ntfs]

async def get_nft(token_id: int) -> NFTResponse:
        nft = await collection.find_one({"token_id": token_id})
        return NFTResponse(**nft)
    