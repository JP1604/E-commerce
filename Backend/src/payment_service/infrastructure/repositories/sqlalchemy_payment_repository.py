"""SQLAlchemy implementation of payment repository."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from payment_service.domain.entities.payment import Payment, PaymentStatus
from payment_service.domain.repositories.payment_repository import PaymentRepository
from payment_service.infrastructure.database.models.payment_models import PaymentModel


class SQLAlchemyPaymentRepository(PaymentRepository):
    """SQLAlchemy implementation of payment repository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payment: Payment) -> Payment:
        """Create a new payment."""
        # Convert domain entity to database model
        payment_model = PaymentModel(
            id_payment=payment.id_payment,
            id_order=payment.id_order,
            id_user=payment.id_user,
            amount=payment.amount,
            method=payment.method,
            status=payment.status,
            reference_number=payment.reference_number,
            gateway_transaction_id=payment.gateway_transaction_id,
            created_at=payment.created_at,
            updated_at=payment.updated_at,
            processed_at=payment.processed_at,
            currency=payment.currency,
            description=payment.description,
            gateway_response=payment.gateway_response,
            failure_reason=payment.failure_reason
        )
        
        self.session.add(payment_model)
        await self.session.commit()
        await self.session.refresh(payment_model)
        
        return self._to_domain_entity(payment_model)

    async def get_by_id(self, payment_id: UUID) -> Optional[Payment]:
        """Get payment by ID."""
        stmt = select(PaymentModel).where(PaymentModel.id_payment == payment_id)
        result = await self.session.execute(stmt)
        payment_model = result.scalar_one_or_none()
        
        if not payment_model:
            return None
        
        return self._to_domain_entity(payment_model)

    async def get_by_order_id(self, order_id: UUID) -> List[Payment]:
        """Get payments by order ID."""
        stmt = select(PaymentModel).where(PaymentModel.id_order == order_id)
        result = await self.session.execute(stmt)
        payment_models = result.scalars().all()
        
        return [self._to_domain_entity(payment_model) for payment_model in payment_models]

    async def get_by_user_id(self, user_id: UUID) -> List[Payment]:
        """Get payments by user ID."""
        stmt = select(PaymentModel).where(PaymentModel.id_user == user_id)
        result = await self.session.execute(stmt)
        payment_models = result.scalars().all()
        
        return [self._to_domain_entity(payment_model) for payment_model in payment_models]

    async def update(self, payment: Payment) -> Payment:
        """Update an existing payment."""
        stmt = select(PaymentModel).where(PaymentModel.id_payment == payment.id_payment)
        result = await self.session.execute(stmt)
        payment_model = result.scalar_one_or_none()
        
        if not payment_model:
            raise ValueError(f"Payment with ID {payment.id_payment} not found")
        
        # Update payment fields
        payment_model.amount = payment.amount
        payment_model.method = payment.method
        payment_model.status = payment.status
        payment_model.reference_number = payment.reference_number
        payment_model.gateway_transaction_id = payment.gateway_transaction_id
        payment_model.updated_at = payment.updated_at
        payment_model.processed_at = payment.processed_at
        payment_model.currency = payment.currency
        payment_model.description = payment.description
        payment_model.gateway_response = payment.gateway_response
        payment_model.failure_reason = payment.failure_reason
        
        await self.session.commit()
        await self.session.refresh(payment_model)
        
        return self._to_domain_entity(payment_model)

    async def get_by_status(self, status: PaymentStatus) -> List[Payment]:
        """Get payments by status."""
        stmt = select(PaymentModel).where(PaymentModel.status == status)
        result = await self.session.execute(stmt)
        payment_models = result.scalars().all()
        
        return [self._to_domain_entity(payment_model) for payment_model in payment_models]

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Payment]:
        """Get all payments with pagination."""
        stmt = select(PaymentModel).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        payment_models = result.scalars().all()
        
        return [self._to_domain_entity(payment_model) for payment_model in payment_models]

    def _to_domain_entity(self, payment_model: PaymentModel) -> Payment:
        """Convert database model to domain entity."""
        return Payment(
            id_payment=payment_model.id_payment,
            id_order=payment_model.id_order,
            id_user=payment_model.id_user,
            amount=payment_model.amount,
            method=payment_model.method,
            status=payment_model.status,
            reference_number=payment_model.reference_number,
            gateway_transaction_id=payment_model.gateway_transaction_id,
            created_at=payment_model.created_at,
            updated_at=payment_model.updated_at,
            processed_at=payment_model.processed_at,
            currency=payment_model.currency,
            description=payment_model.description,
            gateway_response=payment_model.gateway_response,
            failure_reason=payment_model.failure_reason
        )
