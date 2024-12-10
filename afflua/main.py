from fastapi import FastAPI
from aleaf.core.events import startup_event, shutdown_event
from aleaf.api import wallet_router, transaction_router, user_router, collectible_router
from aleaf.middleware.jwt_auth import JWTAuthMiddleware
from contextlib import asynccontextmanager
from aleaf.core.config import settings
from aleaf.core.cors_config import setup_cors

@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect db
    await startup_event()
    yield
    # disconnect db
    await shutdown_event()


app = FastAPI(lifespan=lifespan)

app.middleware(JWTAuthMiddleware) #type: ignore

setup_cors(app)

# app.add_event_handler("startup", startup_event)
# app.add_event_handler("shutdown", shutdown_event)

app.include_router(wallet_router, prefix=settings.API_VERSION, tags=["wallets"])
app.include_router(transaction_router, prefix= settings.API_VERSION, tags=["transactions"])
app.include_router(user_router, prefix=settings.API_VERSION, tags=["users"])
app.include_router(collectible_router, prefix=settings.API_VERSION, tags=["collectibles"])



