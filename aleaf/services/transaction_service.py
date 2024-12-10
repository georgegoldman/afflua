from aleaf.schemas.transaction import TransactionCreate, TransactionResponse
from aleaf.db.connection import get_collection
from bson import ObjectId
from aleaf.core.security import settings
from aleaf.services.wallet_service import add_funds_to_wallet

db = get_collection(settings.DB_NAME)

async def create_transaction(transaction_data: TransactionCreate) -> TransactionResponse:
    # Handle the business logic for a transaction (buy, sell, transfer)
    
    # Example: Add funds to the seller's wallet if it's a sale
    if transaction_data.transaction_type == "sell":
        await add_funds_to_wallet(transaction_data.user_id, transaction_data.amount)
    
    # Insert the transaction into the database
    transaction_dict = transaction_data.model_dump()
    result = await db["transactions"].insert_one(transaction_dict)
    return TransactionResponse(
        transaction_id=str(result.inserted_id),
        **transaction_data.model_dump(),
        status="completed",  # Set transaction status
        timestamp=str(result.inserted_id)  # Using transaction ID as timestamp for illustration
    )

async def get_transaction_by_id(transaction_id: str) -> TransactionResponse:
    transaction = await db["transactions"].find_one({"_id": transaction_id})
    if transaction:
        return TransactionResponse(
            transaction_id=str(transaction["_id"]),
            **transaction
        )
    return None