"""Validation repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from order_validation_service.domain.entities.validation import OrderValidation, ValidationStatus


class ValidationRepository(ABC):
    """Abstract validation repository."""

    @abstractmethod
    async def create(self, validation: OrderValidation) -> OrderValidation:
        """Create a new validation."""
        pass

    @abstractmethod
    async def get_by_id(self, validation_id: UUID) -> Optional[OrderValidation]:
        """Get validation by ID."""
        pass

    @abstractmethod
    async def get_by_order_id(self, order_id: UUID) -> Optional[OrderValidation]:
        """Get validation by order ID."""
        pass

    @abstractmethod
    async def update(self, validation: OrderValidation) -> OrderValidation:
        """Update an existing validation."""
        pass

    @abstractmethod
    async def get_by_status(self, status: ValidationStatus) -> List[OrderValidation]:
        """Get validations by status."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[OrderValidation]:
        """Get all validations with pagination."""
        pass
