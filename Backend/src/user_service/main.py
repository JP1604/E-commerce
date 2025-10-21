"""User service FastAPI app."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from user_service.infrastructure.config.settings import get_settings
from user_service.infrastructure.database.connection import init_database, close_database
from user_service.interfaces.api import api_router, setup_cors


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up User service...")
    await init_database()
    logger.info("User DB initialized")
    yield
    logger.info("Shutting down User service...")
    await close_database()


app = FastAPI(
    title="User Service API",
    description="User microservice with hexagonal architecture",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

setup_cors(app)
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "User Service", "version": "0.1.0", "docs": "/docs"}


@app.get("/health")
async def health():
    """Health check endpoint for Kubernetes."""
    return {"status": "healthy", "service": "user-service"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("user_service.main:app", host="0.0.0.0", port=8001, reload=True)

