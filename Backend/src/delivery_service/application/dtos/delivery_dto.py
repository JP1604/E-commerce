"""DTOs for Delivery service."""

from datetime import date, time, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from delivery_service.domain.entities.delivery import Delivery, DeliveryState


class DeliveryCreateDTO(BaseModel):
    order_id: UUID
    delivery_booked_schedule: date
    booking_start: time
    booking_end: time


class DeliveryUpdateDTO(BaseModel):
    delivery_booked_schedule: Optional[date] = None
    booking_start: Optional[time] = None
    booking_end: Optional[time] = None
    state: Optional[DeliveryState] = None


class DeliveryResponseDTO(BaseModel):
    id: UUID
    order_id: UUID
    delivery_booked_schedule: date
    booking_start: time
    booking_end: time
    state: DeliveryState
    created_at: datetime

    @classmethod
    def from_entity(cls, d: Delivery) -> "DeliveryResponseDTO":
        return cls(
            id=d.id,
            order_id=d.order_id,
            delivery_booked_schedule=d.delivery_booked_schedule,
            booking_start=d.booking_start,
            booking_end=d.booking_end,
            state=d.state,
            created_at=d.created_at,
        )


