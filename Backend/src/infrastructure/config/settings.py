"""Simple application configuration."""

import os
from functools import lru_cache
from typing import List


class SimpleSettings:
    """Simple application settings."""
    
    def __init__(self):
        # Database settings (using PostgreSQL)
        self.database_url: str = os.getenv(
            "DATABASE_URL", 
            "postgresql+asyncpg://ecommerce_user:ecommerce_pass@localhost:5432/ecommerce_db"
        )
        self.database_echo: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"
        
        # Application settings
        self.debug: bool = True
        self.project_name: str = "Simple E-commerce Backend"
        
        # CORS settings
        self.backend_cors_origins: List[str] = [
            "http://localhost:3000",
            "http://localhost:8080"
        ]


@lru_cache()
def get_settings() -> SimpleSettings:
    """Get cached application settings."""
    return SimpleSettings()