"""Order service FastAPI app."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from order_service.infrastructure.config.settings import get_settings
from order_service.infrastructure.database.connection import init_database, close_database
from order_service.interfaces.api import api_router, setup_cors


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Order service...")
    await init_database()
    logger.info("Order DB initialized")
    yield
    logger.info("Shutting down Order service...")
    await close_database()


app = FastAPI(
    title="Order Service API",
    description="Order microservice with hexagonal architecture",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

setup_cors(app)
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Order Service", "version": "0.1.0", "docs": "/docs"}


@app.get("/health")
async def health():
    """Health check endpoint for Kubernetes."""
    return {"status": "healthy", "service": "order-service"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("order_service.main:app", host="0.0.0.0", port=8005, reload=True)
