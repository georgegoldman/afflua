from aleaf.schemas.transaction import TransactionCreate, TransactionResponse
from aleaf.db.connection import get_collection
from bson import ObjectId
from aleaf.services.wallet_service import add_funds_to_wallet
from typing import Optional

collection = get_collection("transactions")

async def create_transaction(transaction_data: TransactionCreate) -> TransactionResponse:
    # Handle the business logic for a transaction (buy, sell, transfer)
    
    # Example: Add funds to the seller's wallet if it's a sale
    if transaction_data.transaction_type == "pending":
        await add_funds_to_wallet(transaction_data.user_id, transaction_data.amount)
    
    # Insert the transaction into the database
    transaction_dict = transaction_data.model_dump()
    result = await collection.insert_one(transaction_dict)
    return TransactionResponse(
        transaction_id=str(result.inserted_id),
        **transaction_data.model_dump(),
        status="completed",  # Set transaction status
        timestamp=str(result.inserted_id)  # Using transaction ID as timestamp for illustration
    )

async def get_transaction_by_id(transaction_id: str) -> Optional[TransactionResponse]:
    transaction = await collection.find_one({"_id": transaction_id})
    if transaction:
        return TransactionResponse(
            transaction_id=str(transaction["_id"]),
            **transaction
        )
    return None

async def update_transaction(transaction_id: str, transaction_status: str) -> Optional[TransactionResponse]:
    transaction = await collection.find_one({"_id": transaction_id})
    if transaction:
        transaction["status"] = transaction_status
        result = await collection.update_one({"_id": ObjectId(transaction_id)})
        if result.modified_count == 1:
            updated_transaction = await collection.find_one({"_id": ObjectId(transaction_id)})
            return TransactionResponse(transaction_id=transaction_id, **updated_transaction) if updated_transaction else None
        return None
    else:
        return None
