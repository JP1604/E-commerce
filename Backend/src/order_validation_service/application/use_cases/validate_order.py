"""Validate order use case."""

import httpx
from uuid import UUID
from typing import Dict, Any

from order_validation_service.domain.entities.validation import OrderValidation, ValidationRule
from order_validation_service.domain.repositories.validation_repository import ValidationRepository
from order_validation_service.application.dtos.validation_dto import ValidationRequestDTO, ValidationResultDTO, ValidationErrorDTO


class ValidateOrderUseCase:
    """Use case for validating orders."""

    def __init__(self, validation_repository: ValidationRepository):
        self.validation_repository = validation_repository

    async def execute(self, validation_request: ValidationRequestDTO) -> ValidationResultDTO:
        """Execute order validation."""
        # Create validation record
        validation = OrderValidation(id_order=validation_request.id_order)
        
        # Perform validation rules
        await self._validate_user_verification(validation, validation_request.id_user)
        await self._validate_product_availability(validation, validation_request.items)
        await self._validate_stock_availability(validation, validation_request.items)
        await self._validate_price_accuracy(validation, validation_request.items, validation_request.total)
        
        # Determine final status
        if validation.is_complete() and not validation.errors:
            validation.approve("system")
        else:
            validation.reject("system")
        
        # Save validation
        saved_validation = await self.validation_repository.create(validation)
        
        # Convert errors to DTOs
        error_dtos = [
            ValidationErrorDTO(
                rule=error.rule,
                message=error.message,
                field=error.field,
                value=error.value
            )
            for error in saved_validation.errors
        ]
        
        return ValidationResultDTO(
            id_validation=saved_validation.id_validation,
            id_order=saved_validation.id_order,
            is_valid=saved_validation.status.value == "approved",
            errors=error_dtos,
            message="Order validation completed" if not error_dtos else "Order validation failed"
        )

    async def _validate_user_verification(self, validation: OrderValidation, user_id: UUID):
        """Validate user exists and is active."""
        try:
            # Call user service to verify user
            async with httpx.AsyncClient() as client:
                response = await client.get(f"http://user_service:8001/api/v1/users/{user_id}")
                
                if response.status_code == 404:
                    validation.add_error(
                        ValidationRule.USER_VERIFICATION,
                        "User not found",
                        "id_user",
                        str(user_id)
                    )
                elif response.status_code != 200:
                    validation.add_error(
                        ValidationRule.USER_VERIFICATION,
                        "Unable to verify user",
                        "id_user",
                        str(user_id)
                    )
                else:
                    user_data = response.json()
                    if not user_data.get("is_active", True):
                        validation.add_error(
                            ValidationRule.USER_VERIFICATION,
                            "User account is not active",
                            "id_user",
                            str(user_id)
                        )
                    else:
                        validation.mark_rule_validated(ValidationRule.USER_VERIFICATION)
        except Exception as e:
            validation.add_error(
                ValidationRule.USER_VERIFICATION,
                f"Error validating user: {str(e)}",
                "id_user",
                str(user_id)
            )

    async def _validate_product_availability(self, validation: OrderValidation, items: list):
        """Validate all products exist and are active."""
        try:
            for item in items:
                product_id = item.get("id_product")
                
                # Call product service to verify product
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"http://product_service:8000/api/v1/products/{product_id}")
                    
                    if response.status_code == 404:
                        validation.add_error(
                            ValidationRule.PRODUCT_AVAILABILITY,
                            f"Product not found: {product_id}",
                            "id_product",
                            str(product_id)
                        )
                    elif response.status_code != 200:
                        validation.add_error(
                            ValidationRule.PRODUCT_AVAILABILITY,
                            f"Unable to verify product: {product_id}",
                            "id_product",
                            str(product_id)
                        )
                    else:
                        product_data = response.json()
                        if not product_data.get("is_active", True):
                            validation.add_error(
                                ValidationRule.PRODUCT_AVAILABILITY,
                                f"Product is not available: {product_id}",
                                "id_product",
                                str(product_id)
                            )
            
            if not validation.errors:
                validation.mark_rule_validated(ValidationRule.PRODUCT_AVAILABILITY)
                
        except Exception as e:
            validation.add_error(
                ValidationRule.PRODUCT_AVAILABILITY,
                f"Error validating products: {str(e)}"
            )

    async def _validate_stock_availability(self, validation: OrderValidation, items: list):
        """Validate stock availability for all items."""
        try:
            for item in items:
                product_id = item.get("id_product")
                quantity = item.get("quantity", 0)
                
                # Call product service to check stock
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"http://product_service:8000/api/v1/products/{product_id}/stock")
                    
                    if response.status_code == 200:
                        stock_data = response.json()
                        available_stock = stock_data.get("available_stock", 0)
                        
                        if available_stock < quantity:
                            validation.add_error(
                                ValidationRule.STOCK_AVAILABILITY,
                                f"Insufficient stock for product {product_id}. Available: {available_stock}, Requested: {quantity}",
                                "quantity",
                                str(quantity)
                            )
                    else:
                        validation.add_error(
                            ValidationRule.STOCK_AVAILABILITY,
                            f"Unable to check stock for product: {product_id}",
                            "id_product",
                            str(product_id)
                        )
            
            if not any(error.rule == ValidationRule.STOCK_AVAILABILITY for error in validation.errors):
                validation.mark_rule_validated(ValidationRule.STOCK_AVAILABILITY)
                
        except Exception as e:
            validation.add_error(
                ValidationRule.STOCK_AVAILABILITY,
                f"Error validating stock: {str(e)}"
            )

    async def _validate_price_accuracy(self, validation: OrderValidation, items: list, total: float):
        """Validate price accuracy."""
        try:
            calculated_total = 0.0
            
            for item in items:
                product_id = item.get("id_product")
                quantity = item.get("quantity", 0)
                unit_price = item.get("unit_price", 0.0)
                
                # Call product service to get current price
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"http://product_service:8000/api/v1/products/{product_id}")
                    
                    if response.status_code == 200:
                        product_data = response.json()
                        current_price = product_data.get("price", 0.0)
                        
                        # Allow small price differences (e.g., due to rounding)
                        if abs(current_price - unit_price) > 0.01:
                            validation.add_error(
                                ValidationRule.PRICE_VALIDATION,
                                f"Price mismatch for product {product_id}. Current: {current_price}, Provided: {unit_price}",
                                "unit_price",
                                str(unit_price)
                            )
                        
                        calculated_total += current_price * quantity
                    else:
                        validation.add_error(
                            ValidationRule.PRICE_VALIDATION,
                            f"Unable to verify price for product: {product_id}",
                            "id_product",
                            str(product_id)
                        )
            
            # Validate total amount
            if abs(calculated_total - total) > 0.01:
                validation.add_error(
                    ValidationRule.PRICE_VALIDATION,
                    f"Total amount mismatch. Calculated: {calculated_total}, Provided: {total}",
                    "total",
                    str(total)
                )
            
            if not any(error.rule == ValidationRule.PRICE_VALIDATION for error in validation.errors):
                validation.mark_rule_validated(ValidationRule.PRICE_VALIDATION)
                
        except Exception as e:
            validation.add_error(
                ValidationRule.PRICE_VALIDATION,
                f"Error validating prices: {str(e)}"
            )
