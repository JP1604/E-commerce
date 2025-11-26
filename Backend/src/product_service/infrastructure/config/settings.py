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
            "postgresql+asyncpg://ecommerce_user:ecommerce_pass@localhost:5432/ecommerce"
        )
        self.database_echo: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"
        
        # Application settings
        self.debug: bool = True
        self.project_name: str = "Simple E-commerce Backend"
        
        # CORS settings
        # Allow all localhost ports for development
        import re
        self.backend_cors_origins: List[str] = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:5174",
            "http://localhost:5175",
            "http://localhost:5176",
            "http://localhost:5177",
            "http://localhost:5178",
            "http://localhost:8080"
        ]


@lru_cache()
def get_settings() -> SimpleSettings:
    """Get cached application settings."""
    return SimpleSettings()