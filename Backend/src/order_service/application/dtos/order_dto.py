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
    """DTO for creating orders - accepts cart_id OR items directly."""
    id_user: UUID
    id_cart: UUID
    items: Optional[List[OrderItemCreateDTO]] = None  # Optional: if provided, uses these instead of fetching cart
    payment_method: str = Field(default="credit_card")
    delivery_date: Optional[str] = None  # Date in YYYY-MM-DD format
    delivery_time_start: Optional[str] = Field(default="09:00")  # Time in HH:MM format
    delivery_time_end: Optional[str] = Field(default="17:00")  # Time in HH:MM format


class OrderUpdateDTO(BaseModel):
    """DTO for updating orders."""
    status: Optional[OrderStatus] = None


class OrderResponseDTO(BaseModel):
    """DTO for order response."""
    id_order: UUID
    id_user: UUID
    id_cart: UUID
    total: float
    status: OrderStatus
    payment_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[OrderItemResponseDTO]


class OrderListResponseDTO(BaseModel):
    """DTO for order list response."""
    orders: List[OrderResponseDTO]
    total_count: int
    page: int
    page_size: int
