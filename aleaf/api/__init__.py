# Import routers or important components from submodules to expose them at the package level
from .wallet import router as wallet_router
from .transaction import router as transaction_router
from .user import router as user_router
from .collectibles import router as collectible_router


# set up a global API version if needed
API_VERSION = "/api/v1"