from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from aleaf.core.security import verify_token
from aleaf.core.config import settings

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Try to get the JWT token from the "Authorization" header
        token = request.headers.get("Authorization")

        if not token:
            raise HTTPException(status_code=401, detail="Token missing")

        # Extract the token from "Bearer <token>"
        token = token.split(" ")[1] if token.startswith("Bearer ") else token

        try:
            # Decode the JWT token and verify it
            payload = verify_token(token)
            request.state.user = payload # Store the decoded user in request.state
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # Pass the request to the next middleware or route handler
        response = await call_next(request)
        return response        