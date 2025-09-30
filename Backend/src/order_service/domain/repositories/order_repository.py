"""Order repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from order_service.domain.entities.order import Order


class OrderRepository(ABC):
    """Abstract order repository."""

    @abstractmethod
    async def create(self, order: Order) -> Order:
        """Create a new order."""
        pass

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        """Get order by ID."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[Order]:
        """Get orders by user ID."""
        pass

    @abstractmethod
    async def update(self, order: Order) -> Order:
        """Update an existing order."""
        pass

    @abstractmethod
    async def delete(self, order_id: UUID) -> bool:
        """Delete an order."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders with pagination."""
        pass
