"""Cart domain entity."""

from typing import Optional, Dict, Any, List
from uuid import UUID
from enum import Enum

from .base import BaseEntity


class CartStatus(str, Enum):
    """Cart status enumeration."""
    ACTIVE = "activo"
    EMPTY = "vacio"
    COMPLETED = "completado"


class Cart(BaseEntity):
    """Cart entity for the cart microservice."""

    def __init__(
        self,
        user_id: UUID,
        status: CartStatus = CartStatus.ACTIVE,
        id_cart: Optional[UUID] = None,
    ) -> None:
        super().__init__(id_cart)
        self.user_id = user_id
        self.status = status
        self._validate()

    def _validate(self) -> None:
        if not self.user_id:
            raise ValueError("User ID is required")

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "id_cart": self.id,
                "user_id": self.user_id,
                "status": self.status.value,
            }
        )
        return base
