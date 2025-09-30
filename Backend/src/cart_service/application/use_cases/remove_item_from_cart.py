"""Remove item from cart use case."""

from uuid import UUID

from ...domain.repositories.cart_item_repository import CartItemRepository


class RemoveItemFromCartUseCase:
    """Use case for removing an item from cart."""

    def __init__(self, cart_item_repository: CartItemRepository) -> None:
        self._cart_item_repository = cart_item_repository

    async def execute(self, cart_item_id: UUID) -> bool:
        """Remove an item from cart."""
        return await self._cart_item_repository.delete(cart_item_id)
