"""Use-case to list users."""

from typing import List
from user_service.domain.entities import User
from user_service.domain.repositories import UserRepository


class ListUsersUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self) -> List[User]:
        return await self._repository.find_all()

