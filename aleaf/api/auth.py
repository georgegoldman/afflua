from fastapi import APIRouter, HTTPException
from aleaf.schemas.user import UserLogin
from aleaf.services.user_service import authenticate_user
from aleaf.core.jwt import create_access_token

router = APIRouter()

# Login route
@router.post("/login/")
async def login(user_login: UserLogin):
    user = await authenticate_user(user_login.email, user_login.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token upon successful login
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
