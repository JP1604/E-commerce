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

    class Config:
        from_attributes = True


class CartItemCreateDTO(BaseModel):
    """CartItem creation data transfer object."""
    
    cart_id: UUID = Field(..., description="Cart ID")
    product_id: UUID = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity must be positive")
    unit_price: float = Field(..., ge=0, description="Unit price must be non-negative")

    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v

    @validator('unit_price')
    def validate_unit_price(cls, v):
        if v < 0:
            raise ValueError('Unit price must be non-negative')
        return v


class CartItemUpdateDTO(BaseModel):
    """CartItem update data transfer object."""
    
    quantity: Optional[int] = Field(None, gt=0, description="Quantity must be positive")
    unit_price: Optional[float] = Field(None, ge=0, description="Unit price must be non-negative")

    @validator('quantity')
    def validate_quantity(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Quantity must be positive')
        return v

    @validator('unit_price')
    def validate_unit_price(cls, v):
        if v is not None and v < 0:
            raise ValueError('Unit price must be non-negative')
        return v
