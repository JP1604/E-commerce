"""Payment domain entity."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class PaymentStatus(str, Enum):
    """Payment status enumeration."""
    PENDING = "pendiente"
    APPROVED = "aprobado"
    REJECTED = "rechazado"
    REFUNDED = "reembolsado"


class PaymentMethod(str, Enum):
    """Payment method enumeration."""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"


class Payment(BaseModel):
    """Payment domain entity."""
    id_payment: UUID = Field(default_factory=uuid4)
    id_order: UUID
    id_user: UUID
    amount: float = Field(gt=0)
    method: PaymentMethod
    status: PaymentStatus = PaymentStatus.PENDING
    reference_number: Optional[str] = None
    gateway_transaction_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    
    # Payment details
    currency: str = Field(default="USD")
    description: Optional[str] = None
    
    # Gateway response
    gateway_response: Optional[dict] = None
    failure_reason: Optional[str] = None

    def approve(self, gateway_transaction_id: str, gateway_response: Optional[dict] = None):
        """Approve the payment."""
        self.status = PaymentStatus.APPROVED
        self.gateway_transaction_id = gateway_transaction_id
        self.gateway_response = gateway_response
        self.processed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def reject(self, failure_reason: str, gateway_response: Optional[dict] = None):
        """Reject the payment."""
        self.status = PaymentStatus.REJECTED
        self.failure_reason = failure_reason
        self.gateway_response = gateway_response
        self.processed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def refund(self, gateway_transaction_id: Optional[str] = None):
        """Refund the payment."""
        if self.status != PaymentStatus.APPROVED:
            raise ValueError("Only approved payments can be refunded")
        
        self.status = PaymentStatus.REFUNDED
        if gateway_transaction_id:
            self.gateway_transaction_id = gateway_transaction_id
        self.updated_at = datetime.utcnow()

    def can_be_refunded(self) -> bool:
        """Check if payment can be refunded."""
        return self.status == PaymentStatus.APPROVED

    def is_successful(self) -> bool:
        """Check if payment is successful."""
        return self.status == PaymentStatus.APPROVED

    class Config:
        """Pydantic config."""
        from_attributes = True
