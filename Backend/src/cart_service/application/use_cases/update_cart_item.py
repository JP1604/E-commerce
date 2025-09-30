"""Update cart item use case."""

from uuid import UUID

from ...domain.entities.cart_item import CartItem
from ...domain.repositories.cart_item_repository import CartItemRepository


class UpdateCartItemUseCase:
    """Use case for updating a cart item."""

    def __init__(self, cart_item_repository: CartItemRepository) -> None:
        self._cart_item_repository = cart_item_repository

    async def execute(self, cart_item: CartItem) -> CartItem:
        """Update an existing cart item."""
        return await self._cart_item_repository.update(cart_item)
