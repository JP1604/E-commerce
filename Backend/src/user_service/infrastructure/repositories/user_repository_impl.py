"""SQLAlchemy implementation of UserRepository."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...domain.entities import User
from ...domain.repositories import UserRepository
from ..database.models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, user: User) -> User:
        model = UserModel(
            id_user=user.id,
            name=user.name,
            email=user.email,
            hash_password=user.hash_password,
            phone=user.phone,
            address=user.address,
        )
        self._session.add(model)
        await self._session.flush()
        return self._model_to_entity(model)

    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self._session.execute(select(UserModel).where(UserModel.id_user == user_id))
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None

    async def find_by_email(self, email: str) -> Optional[User]:
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None

    async def find_all(self) -> List[User]:
        result = await self._session.execute(select(UserModel))
        models = result.scalars().all()
        return [self._model_to_entity(m) for m in models]

    async def update(self, user: User) -> User:
        result = await self._session.execute(select(UserModel).where(UserModel.id_user == user.id))
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"User with id {user.id} not found")
        model.name = user.name
        model.email = user.email
        model.hash_password = user.hash_password
        model.phone = user.phone
        model.address = user.address
        await self._session.flush()
        return self._model_to_entity(model)

    async def delete(self, user_id: UUID) -> bool:
        result = await self._session.execute(select(UserModel).where(UserModel.id_user == user_id))
        model = result.scalar_one_or_none()
        if not model:
            return False
        await self._session.delete(model)
        await self._session.flush()
        return True

    def _model_to_entity(self, model: UserModel) -> User:
        user = User(
            name=model.name,
            email=model.email,
            hash_password=model.hash_password,
            phone=model.phone,
            address=model.address,
            id_user=model.id_user,
        )
        user.created_at = model.created_at
        user.updated_at = model.last_updated
        return user

