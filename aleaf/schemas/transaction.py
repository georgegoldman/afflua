from pydantic import BaseModel
from typing import Optional

class TransactionBase(BaseModel):
    collectible_id: str
    buyer_id: str
    amount: float

class TransactionCreate(TransactionBase):
    user_id: str  # The ID of the user making the transaction
    collectible_id: str  # The ID of the collectible being bought/sold
    amount: float  # The amount involved in the transaction
    transaction_type: str  # For example: "buy", "sell", "transfer"


class TransactionResponse(TransactionBase):
    transaction_id: str
    user_id: str
    collectible_id: str
    amount: float
    transaction_type: str
    status: str  # For example: "completed", "pending", "failed"
    timestamp: str