"""Get product use case."""

from typing import Optional
from uuid import UUID

from ...domain.entities.product import Product
from ...domain.repositories.product_repository import ProductRepository


class GetProductUseCase:
    """Use case for getting a product."""

    def __init__(self, product_repository: ProductRepository) -> None:
        self._product_repository = product_repository

    async def execute(self, product_id: UUID) -> Optional[Product]:
        """Get product by ID."""
        return await self._product_repository.get_by_id(product_id)
