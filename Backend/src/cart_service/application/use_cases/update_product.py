"""Update product use case."""

from ...domain.entities.product import Product
from ...domain.repositories.product_repository import ProductRepository


class UpdateProductUseCase:
    """Use case for updating a product."""

    def __init__(self, product_repository: ProductRepository) -> None:
        self._product_repository = product_repository

    async def execute(self, product: Product) -> Product:
        """Update an existing product."""
        return await self._product_repository.update(product)
