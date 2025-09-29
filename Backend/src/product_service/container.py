"""Simple dependency injection configuration."""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from .domain.repositories import ProductRepository
from .infrastructure.repositories import SQLAlchemyProductRepository
from .infrastructure.database import get_db_session


class SimpleContainer:
    """Simple dependency container."""
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.product_repository: ProductRepository = SQLAlchemyProductRepository(session)


def get_container(session: AsyncSession = Depends(get_db_session)) -> SimpleContainer:
    """Get dependency container instance."""
    return SimpleContainer(session)