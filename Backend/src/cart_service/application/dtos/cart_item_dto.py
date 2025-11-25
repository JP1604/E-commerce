"""CartItem DTOs."""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, validator
from datetime import datetime


class CartItemDTO(BaseModel):
    """CartItem data transfer object."""
    
    id_cart_item: UUID
    cart_id: UUID
    product_id: UUID
    quantity: int
    unit_price: float
    subtotal: float
    created_at: datetime
    updated_at: datetime
    # Optional product info (enriched from Product Service)
    product_name: Optional[str] = None
    product_description: Optional[str] = None

    class Config:
        from_attributes = True


class CartItemCreateDTO(BaseModel):
    """CartItem creation data transfer object."""
    
    product_id: UUID = Field(..., description="Product ID from Product Service")
    quantity: int = Field(default=1, gt=0, description="Quantity must be positive")

    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v


class CartItemUpdateDTO(BaseModel):
    """CartItem update data transfer object."""
    
    quantity: int = Field(..., gt=0, description="Quantity must be positive")

    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v
