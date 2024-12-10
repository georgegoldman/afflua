from fastapi import Depends
from aleaf.db.connection import get_collection
from aleaf.schemas.wallet import WalletBase
from aleaf.schemas.user import UserResponse
from aleaf.schemas.transaction import TransactionCreate, TransactionResponse
from aleaf.services.user_service import get_current_user
from aleaf.services.transaction_service import create_transaction
from bson import ObjectId
from typing import Optional
from datetime import datetime

collection = get_collection("wallet")


async def check_balance(wallet_id:str) -> float:
    wallet: Optional[WalletBase] = await get_wallet(wallet_id)
    if wallet:
        return wallet.balance
    return 0

async def transfer_fund(
        amount: float, 
        recipient: str, 
        wallet_id: str,
        current_user: UserResponse = Depends(get_current_user)
        ) -> TransactionResponse:
    bal = await check_balance(wallet_id)
    if bal <= 0:
        raise ValueError("Insufficient balance")
    elif amount > bal:
        raise ValueError("Insufficient balance")
    txn = TransactionCreate(
        collectible_id="collectible_id", 
        sender=current_user.id, 
        recipient=recipient, 
        amount=amount,
        transaction_type="crypto",
        timestamp=datetime.now().__str__(),
        status="Pending"
        )
    
    # Process the transaction (implementation omitted)
    txn_res = await create_transaction(txn)

    return txn_res



async def get_wallet(wallet_id:str) -> Optional[WalletBase]:
    wallet: WalletBase = await collection.find_one({"_id": ObjectId(wallet_id)})
    if wallet:
        return wallet
    return None


async def mint_nft(metadata_url: str, wallet_id: str, current_user: UserResponse = Depends(get_current_user)) -> TransactionResponse:
    #mint the nft

    # create and log the transaction
    txn = TransactionCreate(
        collectible_id="collectible_id", 
        sender=current_user.id, 
        recipient=current_user.id, 
        amount=0,
        transaction_type="mint",
        timestamp=datetime.now().__str__(),
        status="confirmed",
        metadata= metadata_url
    )

    txn_res = await create_transaction(txn)
    return txn_res

async def transfer_nft(token_id: str, recipient: str, current_user: UserResponse = Depends(get_current_user)) -> TransactionResponse:
    return TransactionResponse()