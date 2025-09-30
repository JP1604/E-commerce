"""List products use case."""

from typing import List, Optional
from uuid import UUID

from ...domain.entities.product import Product, ProductStatus
from ...domain.repositories.product_repository import ProductRepository


class ListProductsUseCase:
    """Use case for listing products."""

    def __init__(self, product_repository: ProductRepository) -> None:
        self._product_repository = product_repository

    async def execute(self, status: Optional[ProductStatus] = None) -> List[Product]:
        """List products, optionally filtered by status."""
        if status:
            return await self._product_repository.list_by_status(status)
        return await self._product_repository.list_all()
