"""Product domain entity."""

from typing import Optional, Dict, Any
from uuid import UUID
from enum import Enum

from .base import BaseEntity


class ProductStatus(str, Enum):
    """Product status enumeration."""
    ACTIVE = "activo"
    INACTIVE = "inactivo"


class Product(BaseEntity):
    """Product entity for the cart microservice."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        status: ProductStatus = ProductStatus.ACTIVE,
        id_product: Optional[UUID] = None,
    ) -> None:
        super().__init__(id_product)
        self.name = name
        self.description = description
        self.price = price
        self.status = status
        self._validate()

    def _validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Product name is required")
        if not self.description or not self.description.strip():
            raise ValueError("Product description is required")
        if self.price < 0:
            raise ValueError("Product price must be non-negative")

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "id_product": self.id,
                "name": self.name,
                "description": self.description,
                "price": self.price,
                "status": self.status.value,
            }
        )
        return base
