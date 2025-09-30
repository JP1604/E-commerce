"""Order Validation service FastAPI app."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from order_validation_service.infrastructure.config.settings import get_settings
from order_validation_service.interfaces.api import api_router, setup_cors


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Order Validation service...")
    yield
    logger.info("Shutting down Order Validation service...")


app = FastAPI(
    title="Order Validation Service API",
    description="Order validation microservice with hexagonal architecture",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

setup_cors(app)
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Order Validation Service", "version": "0.1.0", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("order_validation_service.main:app", host="0.0.0.0", port=8006, reload=True)
