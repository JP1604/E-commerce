"""Use-case to create a new user."""

from user_service.application.dtos import UserCreateDTO
from user_service.domain.entities import User
from user_service.domain.repositories import UserRepository


class CreateUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, data: UserCreateDTO) -> User:
        user = User(
            name=data.name,
            email=data.email,
            hash_password=self._hash_password(data.password),
            phone=data.phone,
            address=data.address,
        )
        return await self._repository.save(user)

    def _hash_password(self, password: str) -> str:
        # Placeholder hashing; replace with proper hashing in production
        return f"sha256:{password}"

