"""API Gateway routers and CORS setup."""

from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api_gateway.infrastructure.config.settings import get_settings
from api_gateway.interfaces.api.routers.products import router as products_router
from api_gateway.interfaces.api.routers.users import router as users_router
from api_gateway.interfaces.api.routers.orders import router as orders_router
from api_gateway.interfaces.api.routers.checkout import router as checkout_router
from api_gateway.interfaces.api.routers.carts import router as carts_router


settings = get_settings()

api_router = APIRouter(prefix=settings.api_prefix)
api_router.include_router(products_router, prefix="/products", tags=["products"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(orders_router, prefix="/orders", tags=["orders"])
api_router.include_router(checkout_router, prefix="/checkout", tags=["checkout"])
api_router.include_router(carts_router, prefix="/carts", tags=["carts"])


def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )


