"""Main API router for cart service."""

from fastapi import APIRouter

from ..controllers.cart_controller import router as cart_router

api_router = APIRouter()

# Include cart router only (products are managed by Product Service)
api_router.include_router(cart_router)
