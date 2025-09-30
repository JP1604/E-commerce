"""User API controller."""

from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException, status

from user_service.application.dtos import UserCreateDTO, UserUpdateDTO, UserResponseDTO, LoginDTO
from user_service.application.use_cases.create_user import CreateUserUseCase
from user_service.application.use_cases.get_user import GetUserUseCase
from user_service.application.use_cases.list_users import ListUsersUseCase
from user_service.application.use_cases.update_user import UpdateUserUseCase
from user_service.application.use_cases.delete_user import DeleteUserUseCase
from user_service.container import get_container, SimpleContainer
from user_service.application.security import verify_password
from user_service.domain.entities import User


class UserController:
    @staticmethod
    async def create_user(data: UserCreateDTO, container: SimpleContainer = Depends(get_container)) -> UserResponseDTO:
        try:
            use_case = CreateUserUseCase(container.user_repository)
            user = await use_case.execute(data)
            return UserResponseDTO.from_entity(user)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @staticmethod
    async def get_user(user_id: UUID, container: SimpleContainer = Depends(get_container)) -> UserResponseDTO:
        use_case = GetUserUseCase(container.user_repository)
        user = await use_case.by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponseDTO.from_entity(user)

    @staticmethod
    async def get_users(container: SimpleContainer = Depends(get_container)) -> List[UserResponseDTO]:
        use_case = ListUsersUseCase(container.user_repository)
        users = await use_case.execute()
        return [UserResponseDTO.from_entity(u) for u in users]

    @staticmethod
    async def update_user(user_id: UUID, data: UserUpdateDTO, container: SimpleContainer = Depends(get_container)) -> UserResponseDTO:
        try:
            use_case = UpdateUserUseCase(container.user_repository)
            user = await use_case.execute(user_id, data)
            return UserResponseDTO.from_entity(user)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @staticmethod
    async def delete_user(user_id: UUID, container: SimpleContainer = Depends(get_container)) -> dict:
        use_case = DeleteUserUseCase(container.user_repository)
        deleted = await use_case.execute(user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"message": "User deleted successfully"}

    @staticmethod
    async def login(data: LoginDTO, container: SimpleContainer = Depends(get_container)) -> dict:
        # Placeholder login: verify email+password only
        user = await container.user_repository.find_by_email(data.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not verify_password(data.password, user.hash_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        # No JWT issued here, just a confirmation for now 
        return {"status": "ok", "user_id": str(user.id)}

