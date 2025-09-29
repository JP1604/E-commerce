"""User service DI container."""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from user_service.domain.repositories import UserRepository
from user_service.infrastructure.repositories import SQLAlchemyUserRepository
from user_service.infrastructure.database.connection import get_db_session


class SimpleContainer:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.user_repository: UserRepository = SQLAlchemyUserRepository(session)


def get_container(session: AsyncSession = Depends(get_db_session)) -> SimpleContainer:
    return SimpleContainer(session)

