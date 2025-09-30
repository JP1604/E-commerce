"""Dependency injection container for order service."""

from functools import lru_cache

from order_service.application.use_cases.create_order import CreateOrderUseCase
from order_service.application.use_cases.get_order import GetOrderUseCase
from order_service.application.use_cases.get_user_orders import GetUserOrdersUseCase
from order_service.application.use_cases.update_order import UpdateOrderUseCase
from order_service.infrastructure.repositories.sqlalchemy_order_repository import SQLAlchemyOrderRepository


class Container:
    """Dependency injection container."""
    
    def __init__(self):
        self._order_repository = None
    
    def order_repository(self, session) -> SQLAlchemyOrderRepository:
        """Get order repository."""
        return SQLAlchemyOrderRepository(session)
    
    def create_order_use_case(self, session) -> CreateOrderUseCase:
        """Get create order use case."""
        return CreateOrderUseCase(self.order_repository(session))
    
    def get_order_use_case(self, session) -> GetOrderUseCase:
        """Get order use case."""
        return GetOrderUseCase(self.order_repository(session))
    
    def get_user_orders_use_case(self, session) -> GetUserOrdersUseCase:
        """Get user orders use case."""
        return GetUserOrdersUseCase(self.order_repository(session))
    
    def update_order_use_case(self, session) -> UpdateOrderUseCase:
        """Get update order use case."""
        return UpdateOrderUseCase(self.order_repository(session))


@lru_cache()
def get_container() -> Container:
    """Get container instance."""
    return Container()
