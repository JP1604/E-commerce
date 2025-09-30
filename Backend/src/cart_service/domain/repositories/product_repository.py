"""Product repository interface."""

from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.product import Product, ProductStatus


class ProductRepository(ABC):
    """Abstract product repository interface."""

    @abstractmethod
    async def create(self, product: Product) -> Product:
        """Create a new product."""
        pass

    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """Get product by ID."""
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Product]:
        """Get product by name."""
        pass

    @abstractmethod
    async def list_by_status(self, status: ProductStatus) -> List[Product]:
        """List products by status."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Product]:
        """List all products."""
        pass

    @abstractmethod
    async def update(self, product: Product) -> Product:
        """Update an existing product."""
        pass

    @abstractmethod
    async def delete(self, product_id: UUID) -> bool:
        """Delete a product."""
        pass
