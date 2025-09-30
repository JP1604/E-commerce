"""Use-case to create a new user."""

from user_service.application.dtos import UserCreateDTO
from user_service.domain.entities import User
from user_service.domain.repositories import UserRepository
from user_service.application.security import hash_password


class CreateUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, data: UserCreateDTO) -> User:
        user = User(
            name=data.name,
            email=data.email,
            hash_password=hash_password(data.password),
            phone=data.phone,
            address=data.address,
        )
        return await self._repository.save(user)


