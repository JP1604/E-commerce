"""Add item to cart use case."""

from uuid import UUID

from ...domain.entities.cart_item import CartItem
from ...domain.repositories.cart_repository import CartRepository
from ...domain.repositories.cart_item_repository import CartItemRepository
from ...infrastructure.clients.product_client import ProductServiceClient


class AddItemToCartUseCase:
    """Use case for adding an item to cart."""

    def __init__(
        self,
        cart_repository: CartRepository,
        cart_item_repository: CartItemRepository,
        product_client: ProductServiceClient,
    ) -> None:
        self._cart_repository = cart_repository
        self._cart_item_repository = cart_item_repository
        self._product_client = product_client

    async def execute(
        self, cart_id: UUID, product_id: UUID, quantity: int
    ) -> CartItem:
        """Add an item to cart."""
        # Verify cart exists
        cart = await self._cart_repository.get_by_id(cart_id)
        if not cart:
            raise ValueError("Cart not found")

        # Verify product exists and get its information
        product = await self._product_client.get_product(product_id)
        if not product:
            raise ValueError("Product not found in Product Service")
        
        # Check stock availability
        if not await self._product_client.check_product_availability(product_id, quantity):
            raise ValueError("Product out of stock or insufficient quantity")

        # Check if item already exists in cart
        existing_item = await self._cart_item_repository.get_by_cart_and_product(
            cart_id, product_id
        )

        if existing_item:
            # Update quantity
            new_quantity = existing_item.quantity + quantity
            
            # Verify total quantity doesn't exceed stock
            if not await self._product_client.check_product_availability(product_id, new_quantity):
                raise ValueError("Adding this quantity would exceed available stock")
                
            existing_item.quantity = new_quantity
            existing_item.update_timestamp()
            return await self._cart_item_repository.update(existing_item)
        else:
            # Create new cart item with current price
            cart_item = CartItem(
                cart_id=cart_id,
                product_id=product_id,
                quantity=quantity,
                unit_price=float(product["price"]),
            )
            return await self._cart_item_repository.create(cart_item)
