"""User service configuration."""

import os
from functools import lru_cache
from typing import List


class UserSettings:
    """Settings for the user microservice."""

    def __init__(self) -> None:
        self.database_url: str = os.getenv(
            "USER_DATABASE_URL",
            "postgresql+asyncpg://user_svc:user_pass@localhost:5433/userdb",
        )
        self.database_echo: bool = os.getenv("USER_DATABASE_ECHO", "false").lower() == "true"
        self.debug: bool = os.getenv("USER_DEBUG", "false").lower() == "true"
        self.project_name: str = "User Service"
        self.backend_cors_origins: List[str] = [
            "http://localhost:3000",
            "http://localhost:8080",
        ]


@lru_cache()
def get_settings() -> UserSettings:
    return UserSettings()

