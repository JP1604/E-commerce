"""Delete cart use case."""

from uuid import UUID

from ...domain.repositories.cart_repository import CartRepository


class DeleteCartUseCase:
    """Use case for deleting a cart."""

    def __init__(self, cart_repository: CartRepository) -> None:
        self._cart_repository = cart_repository

    async def execute(self, cart_id: UUID) -> bool:
        """Delete a cart."""
        return await self._cart_repository.delete(cart_id)
