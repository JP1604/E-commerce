"""Use-case to delete a user."""

from uuid import UUID
from user_service.domain.repositories import UserRepository


class DeleteUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, user_id: UUID) -> bool:
        return await self._repository.delete(user_id)

