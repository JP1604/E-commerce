"""Use-case to get a user by id or email."""

from uuid import UUID
from typing import Optional
from user_service.domain.entities import User
from user_service.domain.repositories import UserRepository


class GetUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def by_id(self, user_id: UUID) -> Optional[User]:
        return await self._repository.find_by_id(user_id)

    async def by_email(self, email: str) -> Optional[User]:
        return await self._repository.find_by_email(email)

