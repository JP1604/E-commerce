"""Use-case to update an existing user."""

from uuid import UUID
from user_service.application.dtos import UserUpdateDTO
from user_service.domain.repositories import UserRepository


class UpdateUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, user_id: UUID, data: UserUpdateDTO):
        user = await self._repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if data.name is not None:
            user.name = data.name
        if data.email is not None:
            user.email = data.email
        if data.password is not None:
            user.hash_password = self._hash_password(data.password)
        if data.phone is not None:
            user.phone = data.phone
        if data.address is not None:
            user.address = data.address

        return await self._repository.update(user)

    def _hash_password(self, password: str) -> str:
        return f"sha256:{password}"

