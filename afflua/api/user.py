from fastapi import APIRouter, Depends, HTTPException, Request
from aleaf.schemas.user import UserCreate, UserResponse, UserUpdate
from aleaf.services.user_service import create_user, get_user_by_id, update_user
from aleaf.core.security import verify_password
from aleaf.core.jwt import create_access_token
from aleaf.core.dependencies import get_current_user

router = APIRouter()

# Create user (registration)
@router.post("/users/", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    user = await create_user(user_data)
    return user

# Get user by ID
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str = Depends(get_current_user)):
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user data
@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user_data(user_id: str, user_data: UserUpdate, request: Request):
    current_user = request.state.user  # Get the authenticated user from request.state
    
    # Check if the user is trying to update their own data
    if current_user["sub"] != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this user")

    user = await update_user(user_id, user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user