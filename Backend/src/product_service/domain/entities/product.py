"""Product domain entity."""

from decimal import Decimal
from typing import Dict, Any, Optional
from uuid import UUID

from .base import BaseEntity


class Product(BaseEntity):
    """Simple product entity for e-commerce catalog."""
    
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        category: str,
        stock_quantity: int = 0,
        id: Optional[UUID] = None,
    ) -> None:
        super().__init__(id)
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.stock_quantity = stock_quantity
        
        self._validate()
    
    def update_stock(self, quantity: int) -> None:
        """Update stock quantity."""
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        self.stock_quantity = quantity
        self.update_timestamp()
    
    def _validate(self) -> None:
        """Basic validation."""
        if not self.name or not self.name.strip():
            raise ValueError("Product name is required")
        if not self.category or not self.category.strip():
            raise ValueError("Product category is required")
        if self.price <= 0:
            raise ValueError("Product price must be positive")
        if self.stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert product to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category": self.category,
            "stock_quantity": self.stock_quantity,
        })
        return base_dict