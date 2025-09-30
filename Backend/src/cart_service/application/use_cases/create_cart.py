"""Create cart use case."""

from typing import Optional
from uuid import UUID

from ...domain.entities.cart import Cart, CartStatus
from ...domain.repositories.cart_repository import CartRepository


class CreateCartUseCase:
    """Use case for creating a new cart."""

    def __init__(self, cart_repository: CartRepository) -> None:
        self._cart_repository = cart_repository

    async def execute(self, user_id: UUID, status: CartStatus = CartStatus.ACTIVE) -> Cart:
        """Create a new cart for a user."""
        # Check if user already has an active cart
        existing_cart = await self._cart_repository.get_by_user_id(user_id)
        if existing_cart and existing_cart.status == CartStatus.ACTIVE:
            raise ValueError("User already has an active cart")

        cart = Cart(user_id=user_id, status=status)
        return await self._cart_repository.create(cart)
