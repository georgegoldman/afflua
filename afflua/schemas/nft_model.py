
from pydantic import BaseModel, HttpUrl
from typing import Optional

# Base model for shared attributes
class NFTBase(BaseModel):
    token_id: Optional[int] = None
    owner: Optional[str] = None  # Address of the current owner
    metadata_uri: Optional[HttpUrl] = None  # Metadata URL (e.g., IPFS link)

# Model for creating a new NFT
class NFTCreate(BaseModel):
    recipient_address: str  # Address to mint the NFT to
    metadata_uri: HttpUrl  # URL for the NFT's metadata (e.g., IPFS JSON file)

# Model for viewing NFT details
class NFTResponse(NFTBase):
    token_id: int  # The unique identifier of the NFT
    owner: str  # Address of the current owner
    metadata_uri: HttpUrl  # URL for the metadata file

# Model for deleting an NFT
class NFTDelete(BaseModel):
    token_id: int  # The ID of the NFT to delete
