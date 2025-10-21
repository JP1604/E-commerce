"""Add item to cart use case."""

from uuid import UUID

from ...domain.entities.cart_item import CartItem
from ...domain.repositories.cart_repository import CartRepository
from ...domain.repositories.cart_item_repository import CartItemRepository
from ...infrastructure.config.settings import settings
import httpx


class AddItemToCartUseCase:
    """Use case for adding an item to cart."""

    def __init__(
        self,
        cart_repository: CartRepository,
        cart_item_repository: CartItemRepository,
    ) -> None:
        self._cart_repository = cart_repository
        self._cart_item_repository = cart_item_repository

    async def execute(
        self, cart_id: UUID, product_id: UUID, quantity: int
    ) -> CartItem:
        """Add an item to cart."""
        # Verify cart exists
        cart = await self._cart_repository.get_by_id(cart_id)
        if not cart:
            raise ValueError("Cart not found")

        # Verify product exists in Product Service and get current price
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{settings.product_service_url}/api/v1/products/{product_id}")
            if resp.status_code == 404:
                raise ValueError("Product not found")
            resp.raise_for_status()
            pdata = resp.json()
            current_price = pdata.get("price", 0.0)

        # Check if item already exists in cart
        existing_item = await self._cart_item_repository.get_by_cart_and_product(
            cart_id, product_id
        )

        if existing_item:
            # Update quantity
            existing_item.quantity += quantity
            existing_item.update_timestamp()
            return await self._cart_item_repository.update(existing_item)
        else:
            # Create new cart item
            cart_item = CartItem(
                cart_id=cart_id,
                product_id=product_id,
                quantity=quantity,
                unit_price=current_price,
            )
            return await self._cart_item_repository.create(cart_item)
