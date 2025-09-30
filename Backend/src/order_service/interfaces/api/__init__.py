"""API interfaces module."""

from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from order_service.infrastructure.config.settings import get_settings
from order_service.interfaces.api.order_controller import router as order_router

settings = get_settings()

# Create main API router
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(order_router, prefix="/orders", tags=["orders"])


def setup_cors(app):
    """Setup CORS middleware."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
