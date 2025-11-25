"""Cart service DI container."""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from cart_service.domain.repositories import CartRepository, CartItemRepository
from cart_service.infrastructure.repositories import (
    SQLAlchemyCartRepository,
    SQLAlchemyCartItemRepository,
)
from cart_service.infrastructure.database.connection import get_db_session


class SimpleContainer:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.cart_repository: CartRepository = SQLAlchemyCartRepository(session)
        self.cart_item_repository: CartItemRepository = SQLAlchemyCartItemRepository(session)


def get_container(session: AsyncSession = Depends(get_db_session)) -> SimpleContainer:
    return SimpleContainer(session)
