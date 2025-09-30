"""Order validation service settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    validation_database_url: str = "postgresql+asyncpg://validation_svc:validation_pass@validation_db:5432/validationdb"
    validation_database_echo: bool = False
    database_url: str = "postgresql+asyncpg://ecommerce_user:ecommerce_pass@localhost:5432/ecommerce_db"
    database_echo: bool = False
    
    # Service
    service_name: str = "order-validation-service"
    service_version: str = "0.1.0"
    debug: bool = True
    project_name: str = "Simple E-commerce Backend"
    
    # External services
    user_service_url: str = "http://user_service:8001"
    product_service_url: str = "http://product_service:8000"
    order_service_url: str = "http://order_service:8005"
    
    # CORS
    cors_origins: list[str] = ["*"]
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]
    backend_cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8080"]

    class Config:
        """Pydantic config."""
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
