from fastapi  import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError #type: ignore
from aleaf.schemas.user import UserCreate, UserResponse, UserUpdate
from aleaf.db.connection import get_collection
from bson import ObjectId
from aleaf.core.security import verify_password, hash_password, decode_access_token
from aleaf.core.jwt import create_access_token, revoke_access_token


collection  = get_collection("users")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# db = get_collection(settings.DB_NAME)

async def create_user(user_data: UserCreate) -> UserResponse:
    # Insert user into MongoDB and return UserResponse
    user_dict = user_data.model_dump()
    user_dict["password"] = hash_password(user_data.password) # hash the password


    # Insert the user data into MongoDB
    result = await collection.insert_one(user_dict)

    # Return a UserResponse with the inserted ID
    return UserResponse(id=str(result.inserted_id), **user_data.model_dump())

async def get_user_by_id(user_id: str) -> UserResponse:
    # Fetch a user by ID
    user = await collection.find_one({"_id": ObjectId(user_id) })
    return UserResponse(id=user_id, **user) if user else None # type: ignore

# Update a user by ID
async def update_user(user_id: str, user_data: UserUpdate) -> UserResponse | None:
    update_dict = user_data.model_dump(exclude_unset=True)
    if "password" in update_dict:
        update_dict["password"] = hash_password(update_dict["password"])  # Re-hash password if updating
    result = await collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_dict})
    if result.modified_count == 1:
        updated_user = await collection.find_one({"_id": ObjectId(user_id)})
        return UserResponse(id=user_id, **updated_user) if updated_user else None  # type: ignore
    return None

# Delete a user by ID
async def delete_user(user_id: str) -> bool:
    result = await collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count == 1

async def authenticate_user(email: str, password: str) -> UserResponse | None:
    # Authenticate a user (dummy authentication for illustration)
    user = await collection.find_one({"email": email})

    # If the user exists and the password matches the hashed password, return UserResponse
    if user and verify_password(password, user["password"]) : # Assuming "password" is the hashed password field
        return UserResponse(id=str(user["_id"]), **user)
    
    return None #type: ignore

# Login user (returning JWT token)
async def login_user(email: str, password: str) -> dict | None:
    user = await authenticate_user(email, password)
    if user:
        access_token = create_access_token({"sub": user.id})  # Assume user ID as subject
        return {"access_token": access_token, "token_type": "bearer"}
    return None

# Logout user (token revocation)
async def logout_user(token: str) -> bool:
    return revoke_access_token(token)  # Implement token revocation in JWT utility

async def get_current_user(token: str =Depends(oauth2_scheme)) -> UserResponse:
    try:
        # Decode the JWT token to extract the payload
        payload = decode_access_token(token)

        # Extract the user ID from the token payload
        user_id: str = payload.get("sub").__str__() # The "sub" claim is typically used for user IDs
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        # Fetch the user from the database
        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")