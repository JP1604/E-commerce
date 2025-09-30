"""SQLAlchemy implementation of cart repository."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from ...domain.entities.cart import Cart, CartStatus
from ...domain.repositories.cart_repository import CartRepository
from ..database.models import CartModel


class SQLAlchemyCartRepository(CartRepository):
    """SQLAlchemy implementation of cart repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, cart: Cart) -> Cart:
        """Create a new cart."""
        cart_model = CartModel(
            id_cart=cart.id,
            user_id=cart.user_id,
            status=cart.status.value,
        )
        self._session.add(cart_model)
        await self._session.commit()
        await self._session.refresh(cart_model)
        return self._to_entity(cart_model)

    async def get_by_id(self, cart_id: UUID) -> Optional[Cart]:
        """Get cart by ID."""
        result = await self._session.execute(
            select(CartModel).where(CartModel.id_cart == cart_id)
        )
        cart_model = result.scalar_one_or_none()
        return self._to_entity(cart_model) if cart_model else None

    async def get_by_user_id(self, user_id: UUID) -> Optional[Cart]:
        """Get active cart by user ID."""
        result = await self._session.execute(
            select(CartModel).where(
                CartModel.user_id == user_id,
                CartModel.status == CartStatus.ACTIVE.value
            )
        )
        cart_model = result.scalar_one_or_none()
        return self._to_entity(cart_model) if cart_model else None

    async def update(self, cart: Cart) -> Cart:
        """Update an existing cart."""
        cart.update_timestamp()
        await self._session.execute(
            update(CartModel)
            .where(CartModel.id_cart == cart.id)
            .values(
                status=cart.status.value,
                updated_at=cart.updated_at,
            )
        )
        await self._session.commit()
        return cart

    async def delete(self, cart_id: UUID) -> bool:
        """Delete a cart."""
        result = await self._session.execute(
            delete(CartModel).where(CartModel.id_cart == cart_id)
        )
        await self._session.commit()
        return result.rowcount > 0

    async def list_by_user_id(self, user_id: UUID) -> List[Cart]:
        """List all carts for a user."""
        result = await self._session.execute(
            select(CartModel).where(CartModel.user_id == user_id)
        )
        cart_models = result.scalars().all()
        return [self._to_entity(cart_model) for cart_model in cart_models]

    def _to_entity(self, cart_model: CartModel) -> Cart:
        """Convert model to entity."""
        return Cart(
            id_cart=cart_model.id_cart,
            user_id=cart_model.user_id,
            status=CartStatus(cart_model.status),
        )
