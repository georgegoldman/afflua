from pydantic import BaseModel
from typing import Optional

class WalletBase(BaseModel):
    user_id: str
    balance: float

# Response model for wallet balance
class WalletResponse(BaseModel):
    user_id: str
    balance: float  # The current balance in the wallet


# Request for adding funds
class AddFundsRequest(BaseModel):
    amount: float  # The amount of funds to add

# Request model for creating a wallet
class WalletCreate(WalletBase):
    balance: float = 0.0  # Default balance is 0 for a newly created wallet
