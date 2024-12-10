from pydantic import BaseModel
from typing import Optional

class TransactionBase(BaseModel):
    collectible_id: str
    amount: float
    timestamp: str

class TransactionCreate(TransactionBase):
    transaction_type: str  # For example: "buy", "sell", "transfer"
    recipient: str
    sender: str
    status: str
    metadata: Optional[str] = None


class TransactionResponse(TransactionBase):
    user_id: str
    collectible_id: str
    amount: float
    transaction_type: str
    status: str  # For example: "completed", "pending", "failed"