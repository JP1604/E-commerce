"""Simple dependency injection configuration."""

from sqlalchemy.ext.asyncio import AsyncSession

from .domain.repositories import ProductRepository
from .infrastructure.repositories import SQLAlchemyProductRepository


class SimpleContainer:
    """Simple dependency container."""
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.product_repository: ProductRepository = SQLAlchemyProductRepository(session)


def get_container(session: AsyncSession) -> SimpleContainer:
    """Get dependency container instance."""
    return SimpleContainer(session)