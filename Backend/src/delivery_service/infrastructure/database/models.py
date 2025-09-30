"""SQLAlchemy models for delivery service."""

from sqlalchemy import Column, Date, Time, Enum as SAEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from delivery_service.infrastructure.database.connection import Base
from delivery_service.domain.entities.delivery import DeliveryState


class DeliveryModel(Base):
    __tablename__ = "deliveries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), nullable=False)
    delivery_booked_schedule = Column(Date, nullable=False)
    booking_start = Column(Time, nullable=False)
    booking_end = Column(Time, nullable=False)
    state = Column(SAEnum(DeliveryState, name="delivery_state"), nullable=False, default=DeliveryState.BOOKED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


