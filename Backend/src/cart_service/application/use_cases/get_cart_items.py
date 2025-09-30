"""Get cart items use case."""

from typing import List
from uuid import UUID

from ...domain.entities.cart_item import CartItem
from ...domain.repositories.cart_item_repository import CartItemRepository


class GetCartItemsUseCase:
    """Use case for getting cart items."""

    def __init__(self, cart_item_repository: CartItemRepository) -> None:
        self._cart_item_repository = cart_item_repository

    async def execute(self, cart_id: UUID) -> List[CartItem]:
        """Get all items in a cart."""
        return await self._cart_item_repository.get_by_cart_id(cart_id)
