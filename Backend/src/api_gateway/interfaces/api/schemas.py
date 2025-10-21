"""Pydantic schemas used by API Gateway to document request/response bodies.

These mirror the common payload shapes used when proxying to downstream
microservices. Models allow the gateway to expose a richer OpenAPI contract
even when downstream services don't share models.
"""
from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    # downstream services sometimes use `id_product` and sometimes `product_id`;
    # accept both when serializing by allowing either field name.
    id_product: Optional[str] = Field(None, alias="id_product")
    product_id: Optional[str] = Field(None, alias="product_id")
    quantity: int
    unit_price: Optional[float] = None

    class Config:
        extra = "allow"
        allow_population_by_field_name = True


class CartCreate(BaseModel):
    user_id: Optional[str] = None

    class Config:
        extra = "allow"


class AddItemRequest(BaseModel):
    product_id: str
    quantity: int = 1
    unit_price: Optional[float] = None

    class Config:
        extra = "allow"


class PaymentInfo(BaseModel):
    method: str
    currency: Optional[str] = "USD"
    description: Optional[str] = None
    card_number: Optional[str] = None
    card_holder_name: Optional[str] = None
    card_expiry_month: Optional[int] = None
    card_expiry_year: Optional[int] = None
    card_cvv: Optional[str] = None
    billing_address: Optional[str] = None

    class Config:
        extra = "allow"


class CheckoutRequest(BaseModel):
    id_user: str
    items: List[OrderItem]
    payment: Optional[PaymentInfo] = None

    class Config:
        extra = "allow"


class OrderItemCreate(BaseModel):
    id_product: str
    quantity: int
    unit_price: Optional[float] = None

    class Config:
        extra = "allow"


class OrderCreate(BaseModel):
    id_user: str
    items: List[OrderItemCreate]

    class Config:
        extra = "allow"


class DeliveryBooking(BaseModel):
    delivery_booked_schedule: str
    booking_start: str
    booking_end: str

    class Config:
        extra = "allow"


class DeliveryStateChange(BaseModel):
    new_state: str

    class Config:
        extra = "allow"


class RefundRequest(BaseModel):
    # Keep flexible - payment service may expect different fields
    amount: Optional[float] = None
    reason: Optional[str] = None

    class Config:
        extra = "allow"


class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    password: Optional[str] = None

    class Config:
        extra = "allow"
