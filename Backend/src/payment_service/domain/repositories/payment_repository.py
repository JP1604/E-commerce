"""Payment repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from payment_service.domain.entities.payment import Payment, PaymentStatus


class PaymentRepository(ABC):
    """Abstract payment repository."""

    @abstractmethod
    async def create(self, payment: Payment) -> Payment:
        """Create a new payment."""
        pass

    @abstractmethod
    async def get_by_id(self, payment_id: UUID) -> Optional[Payment]:
        """Get payment by ID."""
        pass

    @abstractmethod
    async def get_by_order_id(self, order_id: UUID) -> List[Payment]:
        """Get payments by order ID."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[Payment]:
        """Get payments by user ID."""
        pass

    @abstractmethod
    async def update(self, payment: Payment) -> Payment:
        """Update an existing payment."""
        pass

    @abstractmethod
    async def get_by_status(self, status: PaymentStatus) -> List[Payment]:
        """Get payments by status."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Payment]:
        """Get all payments with pagination."""
        pass
