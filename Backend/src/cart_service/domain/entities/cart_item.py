"""CartItem domain entity."""

from typing import Optional, Dict, Any
from uuid import UUID

from .base import BaseEntity


class CartItem(BaseEntity):
    """CartItem entity for the cart microservice."""

    def __init__(
        self,
        cart_id: UUID,
        product_id: UUID,
        quantity: int,
        unit_price: float,
        id_cart_item: Optional[UUID] = None,
    ) -> None:
        super().__init__(id_cart_item)
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self._validate()

    def _validate(self) -> None:
        if not self.cart_id:
            raise ValueError("Cart ID is required")
        if not self.product_id:
            raise ValueError("Product ID is required")
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.unit_price < 0:
            raise ValueError("Unit price must be non-negative")

    @property
    def subtotal(self) -> float:
        """Calculate the subtotal for this cart item."""
        return self.quantity * self.unit_price

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "id_cart_item": self.id,
                "cart_id": self.cart_id,
                "product_id": self.product_id,
                "quantity": self.quantity,
                "unit_price": self.unit_price,
                "subtotal": self.subtotal,
            }
        )
        return base
