"""SQLAlchemy implementation of cart item repository."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from ...domain.entities.cart_item import CartItem
from ...domain.repositories.cart_item_repository import CartItemRepository
from ..database.models import CartItemModel


class SQLAlchemyCartItemRepository(CartItemRepository):
    """SQLAlchemy implementation of cart item repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, cart_item: CartItem) -> CartItem:
        """Create a new cart item."""
        cart_item_model = CartItemModel(
            id_cart_item=cart_item.id,
            cart_id=cart_item.cart_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
        )
        self._session.add(cart_item_model)
        await self._session.commit()
        await self._session.refresh(cart_item_model)
        return self._to_entity(cart_item_model)

    async def get_by_id(self, cart_item_id: UUID) -> Optional[CartItem]:
        """Get cart item by ID."""
        result = await self._session.execute(
            select(CartItemModel).where(CartItemModel.id_cart_item == cart_item_id)
        )
        cart_item_model = result.scalar_one_or_none()
        return self._to_entity(cart_item_model) if cart_item_model else None

    async def get_by_cart_id(self, cart_id: UUID) -> List[CartItem]:
        """Get all items in a cart."""
        result = await self._session.execute(
            select(CartItemModel).where(CartItemModel.cart_id == cart_id)
        )
        cart_item_models = result.scalars().all()
        return [self._to_entity(cart_item_model) for cart_item_model in cart_item_models]

    async def get_by_cart_and_product(self, cart_id: UUID, product_id: UUID) -> Optional[CartItem]:
        """Get cart item by cart ID and product ID."""
        result = await self._session.execute(
            select(CartItemModel).where(
                CartItemModel.cart_id == cart_id,
                CartItemModel.product_id == product_id
            )
        )
        cart_item_model = result.scalar_one_or_none()
        return self._to_entity(cart_item_model) if cart_item_model else None

    async def update(self, cart_item: CartItem) -> CartItem:
        """Update an existing cart item."""
        cart_item.update_timestamp()
        await self._session.execute(
            update(CartItemModel)
            .where(CartItemModel.id_cart_item == cart_item.id)
            .values(
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                updated_at=cart_item.updated_at,
            )
        )
        await self._session.commit()
        return cart_item

    async def delete(self, cart_item_id: UUID) -> bool:
        """Delete a cart item."""
        result = await self._session.execute(
            delete(CartItemModel).where(CartItemModel.id_cart_item == cart_item_id)
        )
        await self._session.commit()
        return result.rowcount > 0

    async def delete_by_cart_id(self, cart_id: UUID) -> bool:
        """Delete all items in a cart."""
        result = await self._session.execute(
            delete(CartItemModel).where(CartItemModel.cart_id == cart_id)
        )
        await self._session.commit()
        return result.rowcount > 0

    def _to_entity(self, cart_item_model: CartItemModel) -> CartItem:
        """Convert model to entity."""
        return CartItem(
            id_cart_item=cart_item_model.id_cart_item,
            cart_id=cart_item_model.cart_id,
            product_id=cart_item_model.product_id,
            quantity=cart_item_model.quantity,
            unit_price=cart_item_model.unit_price,
        )
