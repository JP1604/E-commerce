"""Delivery service FastAPI app."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from delivery_service.infrastructure.config.settings import get_settings
from delivery_service.infrastructure.database.connection import init_database, close_database
from delivery_service.interfaces.api import api_router
from delivery_service.interfaces.api.middlewares.cors import setup_cors


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Delivery service...")
    await init_database()
    logger.info("Delivery DB initialized")
    yield
    logger.info("Shutting down Delivery service...")
    await close_database()


app = FastAPI(
    title="Delivery Service API",
    description="Delivery microservice with hexagonal architecture",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

setup_cors(app)
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Delivery Service", "version": "0.1.0", "docs": "/docs"}


@app.get("/health")
async def health():
    """Health check endpoint for Kubernetes."""
    return {"status": "healthy", "service": "delivery-service"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("delivery_service.main:app", host="0.0.0.0", port=8002, reload=True)


