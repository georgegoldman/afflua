from aleaf.schemas.wallet import WalletResponse
from aleaf.db.connection import get_collection
from aleaf.core.security import settings

db = get_collection(settings.DB_NAME)

async def get_wallet_balance(user_id: str) -> WalletResponse:
    wallet = await db["wallets"].find_one({"user_id": user_id})
    if wallet:
        return WalletResponse(user_id=user_id, balance=wallet["balance"])
    return None

async def update_wallet_balance(user_id: str, amount: float) -> bool:
    # Update wallet balance (add or subtract amount)
    result = await db["wallets"].update_one(
        {"user_id": user_id}, {"$inc": {"balance": amount}}
    )
    return result.modified_count == 1


async def add_funds_to_wallet(user_id: str, amount: float) -> WalletResponse:
    # Add funds to the user's wallet
    wallet = await db["wallets"].find_one_and_update(
        {"user_id": user_id},
        {"$inc": {"balance": amount}},
        return_document=True
    )
    return WalletResponse(user_id=user_id, balance=wallet["balance"])

# Function to create a new wallet for a user
async def create_wallet(user_id: str, initial_balance: float) -> WalletResponse:
    # Check if the wallet already exists
    existing_wallet = await db["wallets"].find_one({"user_id": user_id})
    if existing_wallet:
        raise ValueError("Wallet already exists for this user")

    # Create a new wallet entry
    wallet_data = {
        "user_id": user_id,
        "balance": initial_balance
    }
    result = await db["wallets"].insert_one(wallet_data)

    # Return the newly created wallet
    return WalletResponse(user_id=user_id, balance=initial_balance)

# Function to transfer money between two users
async def transfer_money(sender_id: str, receiver_id: str, amount: float) -> dict:
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")

    # Fetch wallets for sender and receiver
    sender_wallet = await db["wallets"].find_one({"user_id": sender_id})
    receiver_wallet = await db["wallets"].find_one({"user_id": receiver_id})

    # Check if both wallets exist
    if not sender_wallet:
        raise ValueError(f"Sender wallet not found for user {sender_id}")
    if not receiver_wallet:
        raise ValueError(f"Receiver wallet not found for user {receiver_id}")

    # Ensure sender has enough funds
    if sender_wallet["balance"] < amount:
        raise ValueError("Sender does not have enough funds")

    # Start a transaction for atomicity (ensure both updates succeed or fail together)
    async with db.client.start_session() as session:
        async with session.start_transaction():
            # Deduct the amount from sender's wallet
            await db["wallets"].update_one(
                {"user_id": sender_id},
                {"$inc": {"balance": -amount}},
                session=session
            )

            # Add the amount to receiver's wallet
            await db["wallets"].update_one(
                {"user_id": receiver_id},
                {"$inc": {"balance": amount}},
                session=session
            )

    # Return the updated balances
    updated_sender_wallet = await db["wallets"].find_one({"user_id": sender_id})
    updated_receiver_wallet = await db["wallets"].find_one({"user_id": receiver_id})

    return {
        "sender_balance": updated_sender_wallet["balance"],
        "receiver_balance": updated_receiver_wallet["balance"]
    }