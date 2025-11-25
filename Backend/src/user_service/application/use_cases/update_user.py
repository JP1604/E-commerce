"""Use-case to update an existing user."""

from uuid import UUID
from user_service.application.dtos import UserUpdateDTO
from user_service.domain.repositories import UserRepository
from user_service.application.security import hash_password, verify_password


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
            if not data.current_password:
                raise ValueError("Current password is required to change password")
            if not verify_password(data.current_password, user.hash_password):
                raise ValueError("Current password is incorrect")
            user.hash_password = hash_password(data.password)
        if data.phone is not None:
            user.phone = data.phone
        if data.address is not None:
            user.address = data.address

        return await self._repository.update(user)

    

