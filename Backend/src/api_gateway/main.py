"""API Gateway FastAPI app."""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from api_gateway.infrastructure.config.settings import get_settings
from api_gateway.interfaces.api import api_router, setup_cors


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="API Gateway",
    description="Gateway for E-commerce microservices",
    version=settings.service_version,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    lifespan=lifespan,
)

setup_cors(app)
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "API Gateway", "version": settings.service_version, "docs": settings.docs_url}


