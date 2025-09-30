"""Settings for delivery service."""

import os
from functools import lru_cache


class DeliverySettings:
    def __init__(self) -> None:
        self.database_url: str = os.getenv(
            "DELIVERY_DATABASE_URL",
            "postgresql+asyncpg://delivery_svc:delivery_pass@localhost:5434/deliverydb",
        )
        self.database_echo: bool = os.getenv("DELIVERY_DATABASE_ECHO", "false").lower() == "true"


@lru_cache()
def get_settings() -> DeliverySettings:
    return DeliverySettings()


