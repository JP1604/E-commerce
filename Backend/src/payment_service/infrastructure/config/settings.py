"""Payment service settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    payment_database_url: str = "postgresql+asyncpg://payment_svc:payment_pass@payment_db:5432/paymentdb"
    payment_database_echo: bool = False
    
    # Service
    service_name: str = "payment-service"
    service_version: str = "0.1.0"
    
    # Payment gateways
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    paypal_client_id: str = ""
    paypal_client_secret: str = ""
    
    # External services
    order_service_url: str = "http://order_service:8005"
    user_service_url: str = "http://user_service:8001"
    
    # CORS
    cors_origins: list[str] = ["*"]
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]

    class Config:
        """Pydantic config."""
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
