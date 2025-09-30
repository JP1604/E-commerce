"""User service API routes."""

from fastapi import APIRouter, Depends
from uuid import UUID

from user_service.interfaces.api.controllers.user_controller import UserController
from user_service.application.dtos import UserCreateDTO, UserUpdateDTO, LoginDTO
from user_service.container import SimpleContainer, get_container


api_router = APIRouter(prefix="/api/v1/users")


@api_router.post("/")
async def create_user(
    data: UserCreateDTO,
    container: SimpleContainer = Depends(get_container),
):
    return await UserController.create_user(data, container)


@api_router.get("/")
async def list_users(
    container: SimpleContainer = Depends(get_container),
):
    return await UserController.get_users(container)


@api_router.get("/{user_id}")
async def get_user(
    user_id: UUID,
    container: SimpleContainer = Depends(get_container),
):
    return await UserController.get_user(user_id, container)


@api_router.put("/{user_id}")
async def update_user(
    user_id: UUID,
    data: UserUpdateDTO,
    container: SimpleContainer = Depends(get_container),
):
    return await UserController.update_user(user_id, data, container)


@api_router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    container: SimpleContainer = Depends(get_container),
):
    return await UserController.delete_user(user_id, container)


@api_router.post("/login")
async def login(
    data: LoginDTO,
    container: SimpleContainer = Depends(get_container),
):
    return await UserController.login(data, container)
