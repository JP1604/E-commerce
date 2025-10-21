"""API Gateway settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration for API Gateway."""

    # Service
    service_name: str = "api-gateway"
    service_version: str = "0.1.0"
    debug: bool = True
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    api_prefix: str = "/api"

    # Downstream services - can be overridden by environment variables
    product_service_url: str = "http://product-service:8000"
    user_service_url: str = "http://user-service:8001"
    delivery_service_url: str = "http://delivery-service:8002"
    cart_service_url: str = "http://cart-service:8003"
    order_service_url: str = "http://order-service:8005"
    order_validation_service_url: str = "http://order-validation-service:8006"
    payment_service_url: str = "http://payment-service:8007"

    # CORS
    cors_origins: list[str] = ["*"]
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


