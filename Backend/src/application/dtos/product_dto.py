"""Simple Product DTOs."""

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class ProductCreateDTO(BaseModel):
    """DTO for creating a new product."""
    name: str
    description: str
    price: float
    stock_quantity: int = 0


class ProductUpdateDTO(BaseModel):
    """DTO for updating an existing product."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None


class ProductResponseDTO(BaseModel):
    """DTO for product response."""
    id: UUID
    name: str
    description: str
    price: float
    stock_quantity: int
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_entity(cls, product):
        """Create DTO from domain entity."""
        return cls(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock_quantity=product.stock_quantity,
            created_at=product.created_at,
            updated_at=product.updated_at
        )