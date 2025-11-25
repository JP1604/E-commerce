"""Main application for cart service."""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from cart_service.infrastructure.config.settings import settings
from cart_service.infrastructure.database.connection import engine, Base
from cart_service.interfaces.api.middlewares.cors import setup_cors
from cart_service.interfaces.api.routers.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )
    
    # Setup CORS
    setup_cors(app)
    
    # Include API router
    app.include_router(api_router, prefix=settings.api_prefix)
    
    return app


app = create_app()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"status": "healthy", "service": "cart-service"}


@app.get("/health")
async def health():
    """Health check endpoint for Kubernetes."""
    return {"status": "healthy", "service": "cart-service"}
