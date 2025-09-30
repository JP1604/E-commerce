"""Cart repository interface."""

from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.cart import Cart


class CartRepository(ABC):
    """Abstract cart repository interface."""

    @abstractmethod
    async def create(self, cart: Cart) -> Cart:
        """Create a new cart."""
        pass

    @abstractmethod
    async def get_by_id(self, cart_id: UUID) -> Optional[Cart]:
        """Get cart by ID."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Optional[Cart]:
        """Get active cart by user ID."""
        pass

    @abstractmethod
    async def update(self, cart: Cart) -> Cart:
        """Update an existing cart."""
        pass

    @abstractmethod
    async def delete(self, cart_id: UUID) -> bool:
        """Delete a cart."""
        pass

    @abstractmethod
    async def list_by_user_id(self, user_id: UUID) -> List[Cart]:
        """List all carts for a user."""
        pass
