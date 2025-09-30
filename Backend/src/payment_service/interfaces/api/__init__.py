"""API interfaces module."""

from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from payment_service.infrastructure.config.settings import get_settings
from payment_service.interfaces.api.payment_controller import router as payment_router

settings = get_settings()

# Create main API router
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(payment_router, prefix="/payments", tags=["payments"])


def setup_cors(app):
    """Setup CORS middleware."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
