"""Order DTOs."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from order_service.domain.entities.order import OrderStatus


class OrderItemCreateDTO(BaseModel):
    """DTO for creating order items."""
    id_product: UUID
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)


class OrderItemResponseDTO(BaseModel):
    """DTO for order item response."""
    id_order_item: UUID
    id_order: UUID
    id_product: UUID
    quantity: int
    unit_price: float
    subtotal: float
    created_at: datetime


class OrderCreateDTO(BaseModel):
    """DTO for creating orders."""
    id_user: UUID
    items: List[OrderItemCreateDTO] = Field(min_items=1)


class OrderUpdateDTO(BaseModel):
    """DTO for updating orders."""
    status: Optional[OrderStatus] = None


class OrderResponseDTO(BaseModel):
    """DTO for order response."""
    id_order: UUID
    id_user: UUID
    total: float
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[OrderItemResponseDTO]


class OrderListResponseDTO(BaseModel):
    """DTO for order list response."""
    orders: List[OrderResponseDTO]
    total_count: int
    page: int
    page_size: int
