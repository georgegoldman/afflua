from fastapi import Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from aleaf.core.security import verify_token
from aleaf.db.connection import get_collection

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(x_token: str = Header(...)):
    payload = verify_token(x_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"X-Token": "Invalid or Missing"},
        )
    # Return user data or object based on payload
    return payload

def get_user_collection():
    return get_collection("users")