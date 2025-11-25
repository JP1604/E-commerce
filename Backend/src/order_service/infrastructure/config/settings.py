"""Order service settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    order_database_url: str = "postgresql+asyncpg://order_svc:order_pass@order_db:5432/orderdb"
    order_database_echo: bool = False
    database_url: str = "postgresql+asyncpg://ecommerce_user:ecommerce_pass@localhost:5432/ecommerce_db"
    database_echo: bool = False
    
    # Service
    service_name: str = "order-service"
    service_version: str = "0.1.0"
    debug: bool = True
    project_name: str = "Simple E-commerce Backend"
    
    # CORS
    cors_origins: list[str] = ["*"]
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]
    backend_cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176", "http://localhost:5177", "http://localhost:8080"]

    class Config:
        """Pydantic config."""
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
