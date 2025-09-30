"""Delivery domain entity and state enum."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time, datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class DeliveryState(str, Enum):
    BOOKED = "BOOKED"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


@dataclass
class Delivery:
    order_id: UUID
    delivery_booked_schedule: date
    booking_start: time
    booking_end: time
    state: DeliveryState = DeliveryState.BOOKED
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.booking_end <= self.booking_start:
            raise ValueError("booking_end must be after booking_start")


