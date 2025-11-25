"""Simple E-commerce backend application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from src.product_service.infrastructure.config import get_settings
from src.product_service.infrastructure.database import init_database, close_database
from src.product_service.interfaces.api import api_router, setup_cors

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get application settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup
    logger.info("Starting up Simple E-commerce backend...")
    await init_database()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    await close_database()
    logger.info("Database closed")


# Create FastAPI application
app = FastAPI(
    title="Simple E-commerce API",
    description="Simple e-commerce backend with hexagonal architecture",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Setup CORS
setup_cors(app)

# Include API router
app.include_router(api_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Simple E-commerce API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint for Kubernetes."""
    return {
        "status": "healthy",
        "service": "product-service"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )