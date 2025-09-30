"""Update cart use case."""

from uuid import UUID

from ...domain.entities.cart import Cart
from ...domain.repositories.cart_repository import CartRepository


class UpdateCartUseCase:
    """Use case for updating a cart."""

    def __init__(self, cart_repository: CartRepository) -> None:
        self._cart_repository = cart_repository

    async def execute(self, cart: Cart) -> Cart:
        """Update an existing cart."""
        return await self._cart_repository.update(cart)
