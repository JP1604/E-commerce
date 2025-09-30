"""Refund payment use case."""

from uuid import UUID

from payment_service.domain.repositories.payment_repository import PaymentRepository
from payment_service.application.dtos.payment_dto import RefundRequestDTO, RefundResponseDTO
from payment_service.infrastructure.gateways.payment_gateway import PaymentGateway


class RefundPaymentUseCase:
    """Use case for refunding payments."""

    def __init__(self, payment_repository: PaymentRepository, payment_gateway: PaymentGateway):
        self.payment_repository = payment_repository
        self.payment_gateway = payment_gateway

    async def execute(self, payment_id: UUID, refund_request: RefundRequestDTO) -> RefundResponseDTO:
        """Execute payment refund."""
        # Get payment
        payment = await self.payment_repository.get_by_id(payment_id)
        
        if not payment:
            return RefundResponseDTO(
                id_payment=payment_id,
                refund_amount=0.0,
                status=payment.status if payment else None,
                success=False,
                message="Payment not found"
            )
        
        if not payment.can_be_refunded():
            return RefundResponseDTO(
                id_payment=payment.id_payment,
                refund_amount=0.0,
                status=payment.status,
                success=False,
                message="Payment cannot be refunded"
            )
        
        # Determine refund amount
        refund_amount = refund_request.amount if refund_request.amount else payment.amount
        
        if refund_amount > payment.amount:
            return RefundResponseDTO(
                id_payment=payment.id_payment,
                refund_amount=0.0,
                status=payment.status,
                success=False,
                message="Refund amount cannot exceed payment amount"
            )
        
        try:
            # Process refund through gateway
            gateway_response = await self.payment_gateway.process_refund({
                "original_transaction_id": payment.gateway_transaction_id,
                "amount": refund_amount,
                "currency": payment.currency,
                "reason": refund_request.reason
            })
            
            if gateway_response.get("success", False):
                # Refund successful
                payment.refund(gateway_response.get("refund_transaction_id"))
                
                # Update payment record
                updated_payment = await self.payment_repository.update(payment)
                
                return RefundResponseDTO(
                    id_payment=updated_payment.id_payment,
                    refund_amount=refund_amount,
                    status=updated_payment.status,
                    success=True,
                    message="Refund processed successfully",
                    refund_transaction_id=gateway_response.get("refund_transaction_id")
                )
            else:
                # Refund failed
                return RefundResponseDTO(
                    id_payment=payment.id_payment,
                    refund_amount=0.0,
                    status=payment.status,
                    success=False,
                    message=gateway_response.get("error_message", "Refund processing failed")
                )
                
        except Exception as e:
            return RefundResponseDTO(
                id_payment=payment.id_payment,
                refund_amount=0.0,
                status=payment.status,
                success=False,
                message=f"Refund processing error: {str(e)}"
            )
