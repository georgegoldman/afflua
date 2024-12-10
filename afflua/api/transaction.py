from fastapi import APIRouter, Depends, HTTPException
from aleaf.schemas.transaction import TransactionCreate, TransactionResponse
from aleaf.services.transaction_service import create_transaction, get_transaction_by_id

router = APIRouter()

# Create a transaction (e.g., buy/sell)
@router.post("/transaction/", response_model=TransactionResponse)
async def create_new_transaction(transaction_data: TransactionCreate):
    transaction = await create_transaction(transaction_data)
    if transaction is None:
        raise HTTPException(status_code=400, detail="Transaction failed")
    return transaction

# Get transaction details by ID
@router.get("/transaction/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: str):
    transaction = await get_transaction_by_id(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
