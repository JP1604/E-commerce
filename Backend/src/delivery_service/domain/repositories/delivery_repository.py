"""Delivery repository port."""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from uuid import UUID

from delivery_service.domain.entities.delivery import Delivery


class DeliveryRepository(ABC):
    @abstractmethod
    async def save(self, delivery: Delivery) -> Delivery:
        pass

    @abstractmethod
    async def find_by_id(self, delivery_id: UUID) -> Optional[Delivery]:
        pass

    @abstractmethod
    async def find_all(self) -> List[Delivery]:
        pass

    @abstractmethod
    async def find_filtered(
        self,
        *,
        order_id: Optional[UUID] = None,
        state: Optional["DeliveryState"] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Delivery]:
        pass

    @abstractmethod
    async def update(self, delivery: Delivery) -> Delivery:
        pass

    @abstractmethod
    async def delete(self, delivery_id: UUID) -> bool:
        pass


