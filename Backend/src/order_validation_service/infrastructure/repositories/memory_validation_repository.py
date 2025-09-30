"""In-memory implementation of validation repository."""

from typing import Dict, List, Optional
from uuid import UUID

from order_validation_service.domain.entities.validation import OrderValidation, ValidationStatus
from order_validation_service.domain.repositories.validation_repository import ValidationRepository


class MemoryValidationRepository(ValidationRepository):
    """In-memory implementation of validation repository."""

    def __init__(self):
        self._validations: Dict[UUID, OrderValidation] = {}
        self._order_validations: Dict[UUID, UUID] = {}  # order_id -> validation_id

    async def create(self, validation: OrderValidation) -> OrderValidation:
        """Create a new validation."""
        self._validations[validation.id_validation] = validation
        self._order_validations[validation.id_order] = validation.id_validation
        return validation

    async def get_by_id(self, validation_id: UUID) -> Optional[OrderValidation]:
        """Get validation by ID."""
        return self._validations.get(validation_id)

    async def get_by_order_id(self, order_id: UUID) -> Optional[OrderValidation]:
        """Get validation by order ID."""
        validation_id = self._order_validations.get(order_id)
        if validation_id:
            return self._validations.get(validation_id)
        return None

    async def update(self, validation: OrderValidation) -> OrderValidation:
        """Update an existing validation."""
        if validation.id_validation not in self._validations:
            raise ValueError(f"Validation with ID {validation.id_validation} not found")
        
        self._validations[validation.id_validation] = validation
        return validation

    async def get_by_status(self, status: ValidationStatus) -> List[OrderValidation]:
        """Get validations by status."""
        return [
            validation for validation in self._validations.values()
            if validation.status == status
        ]

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[OrderValidation]:
        """Get all validations with pagination."""
        validations = list(self._validations.values())
        return validations[skip:skip + limit]
