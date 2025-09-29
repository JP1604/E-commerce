"""Product repository interface (port)."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities import Product


class ProductRepository(ABC):
    """Simple repository interface for Product entity."""
    
    @abstractmethod
    async def save(self, product: Product) -> Product:
        """Save a product to the repository."""
        pass
    
    @abstractmethod
    async def find_by_id(self, product_id: UUID) -> Optional[Product]:
        """Find a product by its ID."""
        pass
    
    @abstractmethod
    async def find_all(self) -> List[Product]:
        """Find all products."""
        pass
    
    @abstractmethod
    async def update(self, product: Product) -> Product:
        """Update an existing product."""
        pass
    
    @abstractmethod
    async def delete(self, product_id: UUID) -> bool:
        """Delete a product by ID."""
        pass