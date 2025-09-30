"""Settings for cart service."""

import os
from typing import Optional


class Settings:
    """Application settings."""

    def __init__(self) -> None:
        self.database_url: str = os.getenv(
            "DATABASE_URL", 
            "postgresql+asyncpg://postgres:password@localhost:5432/cart_db"
        )
        self.database_host: str = os.getenv("DATABASE_HOST", "localhost")
        self.database_port: int = int(os.getenv("DATABASE_PORT", "5432"))
        self.database_name: str = os.getenv("DATABASE_NAME", "cart_db")
        self.database_user: str = os.getenv("DATABASE_USER", "postgres")
        self.database_password: str = os.getenv("DATABASE_PASSWORD", "password")
        
        self.app_name: str = os.getenv("APP_NAME", "Cart Service")
        self.app_version: str = os.getenv("APP_VERSION", "1.0.0")
        self.debug: bool = os.getenv("DEBUG", "False").lower() == "true"
        
        self.api_prefix: str = os.getenv("API_PREFIX", "/api/v1")
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8002"))


settings = Settings()
