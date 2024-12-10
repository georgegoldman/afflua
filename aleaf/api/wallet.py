from fastapi import APIRouter, Depends, HTTPException
from aleaf.schemas.wallet import WalletResponse, AddFundsRequest
from aleaf.services.wallet_service import get_wallet_balance, add_funds_to_wallet

router = APIRouter()

# Get wallet balance for a user
@router.get("/wallet/{user_id}", response_model=WalletResponse)
async def get_balance(user_id: str):
    wallet_balance = await get_wallet_balance(user_id)
    if wallet_balance is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet_balance

# Add funds to user's wallet
@router.post("/wallet/{user_id}/add_funds", response_model=WalletResponse)
async def add_funds(user_id: str, funds: AddFundsRequest):
    updated_wallet = await add_funds_to_wallet(user_id, funds.amount)
    return updated_wallet
