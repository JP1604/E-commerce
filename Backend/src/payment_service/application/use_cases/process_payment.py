"""Process payment use case."""

import uuid
from typing import Dict, Any

from payment_service.domain.entities.payment import Payment, PaymentMethod
from payment_service.domain.repositories.payment_repository import PaymentRepository
from payment_service.application.dtos.payment_dto import PaymentProcessRequestDTO, PaymentProcessResponseDTO
from payment_service.infrastructure.gateways.payment_gateway import PaymentGateway


class ProcessPaymentUseCase:
    """Use case for processing payments."""

    def __init__(self, payment_repository: PaymentRepository, payment_gateway: PaymentGateway):
        self.payment_repository = payment_repository
        self.payment_gateway = payment_gateway

    async def execute(self, payment_request: PaymentProcessRequestDTO) -> PaymentProcessResponseDTO:
        """Execute payment processing."""
        # Create payment record
        payment = Payment(
            id_order=payment_request.id_order,
            id_user=payment_request.id_user,
            amount=payment_request.amount,
            method=payment_request.method,
            currency=payment_request.currency,
            description=payment_request.description,
            reference_number=self._generate_reference_number()
        )
        
        # Save initial payment record
        created_payment = await self.payment_repository.create(payment)
        
        try:
            # Process payment through gateway
            gateway_response = await self._process_through_gateway(payment_request, created_payment)
            
            if gateway_response.get("success", False):
                # Payment successful
                created_payment.approve(
                    gateway_transaction_id=gateway_response.get("transaction_id"),
                    gateway_response=gateway_response
                )
                
                # Update payment record
                updated_payment = await self.payment_repository.update(created_payment)
                
                return PaymentProcessResponseDTO(
                    id_payment=updated_payment.id_payment,
                    status=updated_payment.status,
                    gateway_transaction_id=updated_payment.gateway_transaction_id,
                    reference_number=updated_payment.reference_number,
                    message="Payment processed successfully",
                    success=True
                )
            else:
                # Payment failed
                failure_reason = gateway_response.get("error_message", "Payment processing failed")
                created_payment.reject(failure_reason, gateway_response)
                
                # Update payment record
                updated_payment = await self.payment_repository.update(created_payment)
                
                return PaymentProcessResponseDTO(
                    id_payment=updated_payment.id_payment,
                    status=updated_payment.status,
                    gateway_transaction_id=updated_payment.gateway_transaction_id,
                    reference_number=updated_payment.reference_number,
                    message="Payment processing failed",
                    success=False,
                    failure_reason=failure_reason
                )
                
        except Exception as e:
            # Handle processing error
            created_payment.reject(f"Processing error: {str(e)}")
            await self.payment_repository.update(created_payment)
            
            return PaymentProcessResponseDTO(
                id_payment=created_payment.id_payment,
                status=created_payment.status,
                gateway_transaction_id=None,
                reference_number=created_payment.reference_number,
                message="Payment processing error",
                success=False,
                failure_reason=str(e)
            )

    async def _process_through_gateway(self, payment_request: PaymentProcessRequestDTO, payment: Payment) -> Dict[str, Any]:
        """Process payment through appropriate gateway."""
        if payment_request.method in [PaymentMethod.CREDIT_CARD, PaymentMethod.DEBIT_CARD]:
            return await self.payment_gateway.process_card_payment({
                "amount": payment_request.amount,
                "currency": payment_request.currency,
                "card_number": payment_request.card_number,
                "card_holder_name": payment_request.card_holder_name,
                "card_expiry_month": payment_request.card_expiry_month,
                "card_expiry_year": payment_request.card_expiry_year,
                "card_cvv": payment_request.card_cvv,
                "billing_address": payment_request.billing_address,
                "reference": payment.reference_number
            })
        elif payment_request.method == PaymentMethod.PAYPAL:
            return await self.payment_gateway.process_paypal_payment({
                "amount": payment_request.amount,
                "currency": payment_request.currency,
                "description": payment_request.description,
                "reference": payment.reference_number
            })
        elif payment_request.method == PaymentMethod.BANK_TRANSFER:
            return await self.payment_gateway.process_bank_transfer({
                "amount": payment_request.amount,
                "currency": payment_request.currency,
                "reference": payment.reference_number
            })
        else:
            # For cash payments, auto-approve (would be handled differently in real scenario)
            return {
                "success": True,
                "transaction_id": f"CASH_{uuid.uuid4().hex[:8].upper()}",
                "message": "Cash payment recorded"
            }

    def _generate_reference_number(self) -> str:
        """Generate unique reference number."""
        return f"PAY_{uuid.uuid4().hex[:8].upper()}"
