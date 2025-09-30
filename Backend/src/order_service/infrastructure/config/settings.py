"""Order service settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    order_database_url: str = "postgresql+asyncpg://order_svc:order_pass@order_db:5432/orderdb"
    order_database_echo: bool = False
    
    # Service
    service_name: str = "order-service"
    service_version: str = "0.1.0"
    
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
