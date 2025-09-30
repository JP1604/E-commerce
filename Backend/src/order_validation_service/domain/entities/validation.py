"""Validation domain entities."""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ValidationStatus(str, Enum):
    """Validation status enumeration."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ValidationRule(str, Enum):
    """Validation rule types."""
    STOCK_AVAILABILITY = "stock_availability"
    USER_VERIFICATION = "user_verification"
    PRODUCT_AVAILABILITY = "product_availability"
    PRICE_VALIDATION = "price_validation"
    QUANTITY_LIMITS = "quantity_limits"


class ValidationError(BaseModel):
    """Validation error entity."""
    rule: ValidationRule
    message: str
    field: Optional[str] = None
    value: Optional[str] = None


class OrderValidation(BaseModel):
    """Order validation entity."""
    id_validation: UUID = Field(default_factory=uuid4)
    id_order: UUID
    status: ValidationStatus = ValidationStatus.PENDING
    validated_rules: List[ValidationRule] = Field(default_factory=list)
    errors: List[ValidationError] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    validated_by: Optional[str] = None

    def add_error(self, rule: ValidationRule, message: str, field: Optional[str] = None, value: Optional[str] = None):
        """Add validation error."""
        error = ValidationError(rule=rule, message=message, field=field, value=value)
        self.errors.append(error)
        self.status = ValidationStatus.REJECTED
        self.updated_at = datetime.utcnow()

    def mark_rule_validated(self, rule: ValidationRule):
        """Mark a validation rule as completed."""
        if rule not in self.validated_rules:
            self.validated_rules.append(rule)
        self.updated_at = datetime.utcnow()

    def approve(self, validated_by: str):
        """Approve the validation."""
        if not self.errors:
            self.status = ValidationStatus.APPROVED
            self.validated_by = validated_by
            self.updated_at = datetime.utcnow()

    def reject(self, validated_by: str):
        """Reject the validation."""
        self.status = ValidationStatus.REJECTED
        self.validated_by = validated_by
        self.updated_at = datetime.utcnow()

    def is_complete(self) -> bool:
        """Check if all validation rules have been processed."""
        required_rules = [
            ValidationRule.STOCK_AVAILABILITY,
            ValidationRule.USER_VERIFICATION,
            ValidationRule.PRODUCT_AVAILABILITY,
            ValidationRule.PRICE_VALIDATION
        ]
        return all(rule in self.validated_rules for rule in required_rules)

    class Config:
        """Pydantic config."""
        from_attributes = True
