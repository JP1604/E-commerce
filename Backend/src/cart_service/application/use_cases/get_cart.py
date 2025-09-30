"""Get cart use case."""

from typing import Optional
from uuid import UUID

from ...domain.entities.cart import Cart
from ...domain.repositories.cart_repository import CartRepository


class GetCartUseCase:
    """Use case for getting a cart."""

    def __init__(self, cart_repository: CartRepository) -> None:
        self._cart_repository = cart_repository

    async def execute(self, cart_id: UUID) -> Optional[Cart]:
        """Get cart by ID."""
        return await self._cart_repository.get_by_id(cart_id)

    async def execute_by_user_id(self, user_id: UUID) -> Optional[Cart]:
        """Get active cart by user ID."""
        return await self._cart_repository.get_by_user_id(user_id)
