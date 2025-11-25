"""Delivery service DI container."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from delivery_service.domain.repositories.delivery_repository import DeliveryRepository
from delivery_service.infrastructure.repositories.delivery_repository_impl import SQLAlchemyDeliveryRepository
from delivery_service.infrastructure.database.connection import get_db_session


class SimpleContainer:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.delivery_repository: DeliveryRepository = SQLAlchemyDeliveryRepository(session)


def get_container(session: AsyncSession = Depends(get_db_session)) -> SimpleContainer:
    return SimpleContainer(session)


