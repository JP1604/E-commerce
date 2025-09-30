"""CartItem repository interface."""

from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.cart_item import CartItem


class CartItemRepository(ABC):
    """Abstract cart item repository interface."""

    @abstractmethod
    async def create(self, cart_item: CartItem) -> CartItem:
        """Create a new cart item."""
        pass

    @abstractmethod
    async def get_by_id(self, cart_item_id: UUID) -> Optional[CartItem]:
        """Get cart item by ID."""
        pass

    @abstractmethod
    async def get_by_cart_id(self, cart_id: UUID) -> List[CartItem]:
        """Get all items in a cart."""
        pass

    @abstractmethod
    async def get_by_cart_and_product(self, cart_id: UUID, product_id: UUID) -> Optional[CartItem]:
        """Get cart item by cart ID and product ID."""
        pass

    @abstractmethod
    async def update(self, cart_item: CartItem) -> CartItem:
        """Update an existing cart item."""
        pass

    @abstractmethod
    async def delete(self, cart_item_id: UUID) -> bool:
        """Delete a cart item."""
        pass

    @abstractmethod
    async def delete_by_cart_id(self, cart_id: UUID) -> bool:
        """Delete all items in a cart."""
        pass
