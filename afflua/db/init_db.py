from aleaf.db.connection import get_collection
from aleaf.db.models.user import User, UserCreate
from aleaf.db.models.collectible import Collectible
from aleaf.db.models.transaction import Transaction

async def init_db():
    """Initialize the database with default data."""
    # Example: Insert default users or setup collections here

    # Create default admin user
    admin_user  = UserCreate(
        name ="admin",
        age=None,
        role = "admin",
        wallet_address= "0xAdminWalletAddress",
        username="admin",
        email="admin@aleaf.com",
        password="hashedpassword"
    )

    # Insert admin user if not exists
    user_collection = get_collection("users")
    existing_admin = await user_collection.find_one({"email": admin_user.email})
    if not existing_admin:
        await user_collection.insert_one(admin_user.model_dump())
        print(f"Admin user created: {admin_user.email}")


    # Optionally, add other default data like default collectibles or setup

