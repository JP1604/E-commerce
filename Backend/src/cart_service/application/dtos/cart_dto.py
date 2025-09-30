"""Cart DTOs."""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

from ...domain.entities.cart import CartStatus


class CartDTO(BaseModel):
    """Cart data transfer object."""
    
    id_cart: UUID
    user_id: UUID
    status: CartStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CartCreateDTO(BaseModel):
    """Cart creation data transfer object."""
    
    user_id: UUID = Field(..., description="User ID who owns the cart")
    status: CartStatus = Field(default=CartStatus.ACTIVE, description="Cart status")


class CartUpdateDTO(BaseModel):
    """Cart update data transfer object."""
    
    status: Optional[CartStatus] = Field(None, description="Cart status")
