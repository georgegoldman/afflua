from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt #type: ignore
from aleaf.core.config import settings


# JWT Settings
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Create a JWT access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verify a JWT token and retrieve the payload
def verify_access_token(x_token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(x_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    
# Optional: Revoke an access token (useful if you implement token blacklisting)
def revoke_access_token(token: str) -> bool:
    # This is a placeholder; revocation would require additional logic
    # such as a blacklist in your datab ase or an in-memory store.
    return True  # Always returns True for now; replace with actual revocation logic if needed