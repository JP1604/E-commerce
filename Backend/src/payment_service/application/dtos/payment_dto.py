"""Payment DTOs."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from payment_service.domain.entities.payment import PaymentStatus, PaymentMethod


class PaymentCreateDTO(BaseModel):
    """DTO for creating payments."""
    id_order: UUID
    id_user: UUID
    amount: float = Field(gt=0)
    method: PaymentMethod
    currency: str = Field(default="USD")
    description: Optional[str] = None


class PaymentUpdateDTO(BaseModel):
    """DTO for updating payments."""
    status: Optional[PaymentStatus] = None
    gateway_transaction_id: Optional[str] = None
    failure_reason: Optional[str] = None


class PaymentResponseDTO(BaseModel):
    """DTO for payment response."""
    id_payment: UUID
    id_order: UUID
    id_user: UUID
    amount: float
    method: PaymentMethod
    status: PaymentStatus
    reference_number: Optional[str]
    gateway_transaction_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    processed_at: Optional[datetime]
    currency: str
    description: Optional[str]
    failure_reason: Optional[str]


class PaymentProcessRequestDTO(BaseModel):
    """DTO for payment processing requests."""
    id_order: UUID
    id_user: UUID
    amount: float = Field(gt=0)
    method: PaymentMethod
    currency: str = Field(default="USD")
    description: Optional[str] = None
    
    # Card details (for card payments)
    card_number: Optional[str] = None
    card_holder_name: Optional[str] = None
    card_expiry_month: Optional[int] = None
    card_expiry_year: Optional[int] = None
    card_cvv: Optional[str] = None
    
    # Additional payment details
    billing_address: Optional[dict] = None


class PaymentProcessResponseDTO(BaseModel):
    """DTO for payment processing response."""
    id_payment: UUID
    status: PaymentStatus
    gateway_transaction_id: Optional[str]
    reference_number: Optional[str]
    message: str
    success: bool
    failure_reason: Optional[str] = None


class RefundRequestDTO(BaseModel):
    """DTO for refund requests."""
    amount: Optional[float] = None  # If None, full refund
    reason: Optional[str] = None


class RefundResponseDTO(BaseModel):
    """DTO for refund response."""
    id_payment: UUID
    refund_amount: float
    status: PaymentStatus
    success: bool
    message: str
    refund_transaction_id: Optional[str] = None
