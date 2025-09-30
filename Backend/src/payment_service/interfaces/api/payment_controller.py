"""Payment API controller."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from payment_service.application.dtos.payment_dto import (
    PaymentProcessRequestDTO,
    PaymentProcessResponseDTO,
    PaymentResponseDTO,
    RefundRequestDTO,
    RefundResponseDTO
)
from payment_service.application.use_cases.process_payment import ProcessPaymentUseCase
from payment_service.application.use_cases.refund_payment import RefundPaymentUseCase
from payment_service.infrastructure.database.connection import get_db_session
from payment_service.infrastructure.repositories.sqlalchemy_payment_repository import SQLAlchemyPaymentRepository
from payment_service.infrastructure.gateways.payment_gateway import MockPaymentGateway

router = APIRouter()


def get_payment_repository(session: AsyncSession = Depends(get_db_session)) -> SQLAlchemyPaymentRepository:
    """Get payment repository dependency."""
    return SQLAlchemyPaymentRepository(session)


def get_payment_gateway() -> MockPaymentGateway:
    """Get payment gateway dependency."""
    return MockPaymentGateway()


@router.post("/process", response_model=PaymentProcessResponseDTO, status_code=status.HTTP_201_CREATED)
async def process_payment(
    payment_request: PaymentProcessRequestDTO,
    repository: SQLAlchemyPaymentRepository = Depends(get_payment_repository),
    gateway: MockPaymentGateway = Depends(get_payment_gateway)
):
    """Process a payment."""
    try:
        use_case = ProcessPaymentUseCase(repository, gateway)
        return await use_case.execute(payment_request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing payment: {str(e)}"
        )


@router.get("/{payment_id}", response_model=PaymentResponseDTO)
async def get_payment(
    payment_id: UUID,
    repository: SQLAlchemyPaymentRepository = Depends(get_payment_repository)
):
    """Get payment by ID."""
    payment = await repository.get_by_id(payment_id)
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    return PaymentResponseDTO(
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
        failure_reason=payment.failure_reason
    )


@router.get("/order/{order_id}", response_model=List[PaymentResponseDTO])
async def get_payments_by_order(
    order_id: UUID,
    repository: SQLAlchemyPaymentRepository = Depends(get_payment_repository)
):
    """Get payments by order ID."""
    payments = await repository.get_by_order_id(order_id)
    
    return [
        PaymentResponseDTO(
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
            failure_reason=payment.failure_reason
        )
        for payment in payments
    ]


@router.get("/user/{user_id}", response_model=List[PaymentResponseDTO])
async def get_payments_by_user(
    user_id: UUID,
    repository: SQLAlchemyPaymentRepository = Depends(get_payment_repository)
):
    """Get payments by user ID."""
    payments = await repository.get_by_user_id(user_id)
    
    return [
        PaymentResponseDTO(
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
            failure_reason=payment.failure_reason
        )
        for payment in payments
    ]


@router.post("/{payment_id}/refund", response_model=RefundResponseDTO)
async def refund_payment(
    payment_id: UUID,
    refund_request: RefundRequestDTO,
    repository: SQLAlchemyPaymentRepository = Depends(get_payment_repository),
    gateway: MockPaymentGateway = Depends(get_payment_gateway)
):
    """Refund a payment."""
    try:
        use_case = RefundPaymentUseCase(repository, gateway)
        return await use_case.execute(payment_id, refund_request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing refund: {str(e)}"
        )


@router.get("/", response_model=List[PaymentResponseDTO])
async def get_all_payments(
    skip: int = 0,
    limit: int = 100,
    repository: SQLAlchemyPaymentRepository = Depends(get_payment_repository)
):
    """Get all payments with pagination."""
    payments = await repository.get_all(skip=skip, limit=limit)
    
    return [
        PaymentResponseDTO(
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
            failure_reason=payment.failure_reason
        )
        for payment in payments
    ]
