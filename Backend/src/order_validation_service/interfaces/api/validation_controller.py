"""Validation API controller."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from order_validation_service.application.dtos.validation_dto import (
    ValidationRequestDTO,
    ValidationResultDTO,
    OrderValidationResponseDTO
)
from order_validation_service.application.use_cases.validate_order import ValidateOrderUseCase
from order_validation_service.infrastructure.repositories.memory_validation_repository import MemoryValidationRepository

router = APIRouter()

# For simplicity, using in-memory repository
# In production, you would use a proper database
validation_repository = MemoryValidationRepository()


@router.post("/validate", response_model=ValidationResultDTO)
async def validate_order(validation_request: ValidationRequestDTO):
    """Validate an order."""
    try:
        use_case = ValidateOrderUseCase(validation_repository)
        return await use_case.execute(validation_request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error validating order: {str(e)}"
        )


@router.get("/{validation_id}", response_model=OrderValidationResponseDTO)
async def get_validation(validation_id: UUID):
    """Get validation by ID."""
    validation = await validation_repository.get_by_id(validation_id)
    
    if not validation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Validation not found"
        )
    
    return OrderValidationResponseDTO(
        id_validation=validation.id_validation,
        id_order=validation.id_order,
        status=validation.status,
        validated_rules=validation.validated_rules,
        errors=[
            {
                "rule": error.rule,
                "message": error.message,
                "field": error.field,
                "value": error.value
            }
            for error in validation.errors
        ],
        created_at=validation.created_at,
        updated_at=validation.updated_at,
        validated_by=validation.validated_by
    )


@router.get("/order/{order_id}", response_model=OrderValidationResponseDTO)
async def get_validation_by_order(order_id: UUID):
    """Get validation by order ID."""
    validation = await validation_repository.get_by_order_id(order_id)
    
    if not validation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Validation not found for this order"
        )
    
    return OrderValidationResponseDTO(
        id_validation=validation.id_validation,
        id_order=validation.id_order,
        status=validation.status,
        validated_rules=validation.validated_rules,
        errors=[
            {
                "rule": error.rule,
                "message": error.message,
                "field": error.field,
                "value": error.value
            }
            for error in validation.errors
        ],
        created_at=validation.created_at,
        updated_at=validation.updated_at,
        validated_by=validation.validated_by
    )


@router.get("/", response_model=List[OrderValidationResponseDTO])
async def get_all_validations(skip: int = 0, limit: int = 100):
    """Get all validations with pagination."""
    validations = await validation_repository.get_all(skip=skip, limit=limit)
    
    return [
        OrderValidationResponseDTO(
            id_validation=validation.id_validation,
            id_order=validation.id_order,
            status=validation.status,
            validated_rules=validation.validated_rules,
            errors=[
                {
                    "rule": error.rule,
                    "message": error.message,
                    "field": error.field,
                    "value": error.value
                }
                for error in validation.errors
            ],
            created_at=validation.created_at,
            updated_at=validation.updated_at,
            validated_by=validation.validated_by
        )
        for validation in validations
    ]
