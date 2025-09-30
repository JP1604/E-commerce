"""Validation DTOs."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from order_validation_service.domain.entities.validation import ValidationStatus, ValidationRule


class ValidationErrorDTO(BaseModel):
    """DTO for validation errors."""
    rule: ValidationRule
    message: str
    field: Optional[str] = None
    value: Optional[str] = None


class OrderValidationCreateDTO(BaseModel):
    """DTO for creating order validations."""
    id_order: UUID


class OrderValidationUpdateDTO(BaseModel):
    """DTO for updating order validations."""
    status: Optional[ValidationStatus] = None
    validated_by: Optional[str] = None


class OrderValidationResponseDTO(BaseModel):
    """DTO for order validation response."""
    id_validation: UUID
    id_order: UUID
    status: ValidationStatus
    validated_rules: List[ValidationRule]
    errors: List[ValidationErrorDTO]
    created_at: datetime
    updated_at: Optional[datetime]
    validated_by: Optional[str]


class ValidationRequestDTO(BaseModel):
    """DTO for validation requests."""
    id_order: UUID
    id_user: UUID
    items: List[dict]  # Order items for validation
    total: float


class ValidationResultDTO(BaseModel):
    """DTO for validation results."""
    id_validation: UUID
    id_order: UUID
    is_valid: bool
    errors: List[ValidationErrorDTO]
    message: str
