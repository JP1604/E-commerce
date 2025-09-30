"""Dependency injection container for payment service."""

from functools import lru_cache

from payment_service.application.use_cases.process_payment import ProcessPaymentUseCase
from payment_service.application.use_cases.refund_payment import RefundPaymentUseCase
from payment_service.infrastructure.repositories.sqlalchemy_payment_repository import SQLAlchemyPaymentRepository
from payment_service.infrastructure.gateways.payment_gateway import MockPaymentGateway


class Container:
    """Dependency injection container."""
    
    def __init__(self):
        self._payment_repository = None
        self._payment_gateway = None
    
    def payment_repository(self, session) -> SQLAlchemyPaymentRepository:
        """Get payment repository."""
        return SQLAlchemyPaymentRepository(session)
    
    def payment_gateway(self) -> MockPaymentGateway:
        """Get payment gateway."""
        if self._payment_gateway is None:
            self._payment_gateway = MockPaymentGateway()
        return self._payment_gateway
    
    def process_payment_use_case(self, session) -> ProcessPaymentUseCase:
        """Get process payment use case."""
        return ProcessPaymentUseCase(
            self.payment_repository(session),
            self.payment_gateway()
        )
    
    def refund_payment_use_case(self, session) -> RefundPaymentUseCase:
        """Get refund payment use case."""
        return RefundPaymentUseCase(
            self.payment_repository(session),
            self.payment_gateway()
        )


@lru_cache()
def get_container() -> Container:
    """Get container instance."""
    return Container()
