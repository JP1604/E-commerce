"""Main API router for cart service."""

from fastapi import APIRouter

from ..controllers.cart_controller import router as cart_router
from ..controllers.product_controller import router as product_router

api_router = APIRouter()

# Include all routers
api_router.include_router(cart_router)
api_router.include_router(product_router)
