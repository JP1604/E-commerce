"""Payment database models."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, Enum, Float, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from payment_service.infrastructure.database.connection import Base
from payment_service.domain.entities.payment import PaymentStatus, PaymentMethod


class PaymentModel(Base):
    """Payment database model."""
    
    __tablename__ = "payments"
    
    id_payment = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    id_order = Column(PostgresUUID(as_uuid=True), nullable=False)
    id_user = Column(PostgresUUID(as_uuid=True), nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    reference_number = Column(String(50), nullable=True)
    gateway_transaction_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    processed_at = Column(DateTime, nullable=True)
    
    # Payment details
    currency = Column(String(3), nullable=False, default="USD")
    description = Column(Text, nullable=True)
    
    # Gateway response
    gateway_response = Column(JSON, nullable=True)
    failure_reason = Column(Text, nullable=True)
