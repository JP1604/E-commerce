"""Delete product use case."""

from uuid import UUID

from ...domain.repositories.product_repository import ProductRepository


class DeleteProductUseCase:
    """Use case for deleting a product."""

    def __init__(self, product_repository: ProductRepository) -> None:
        self._product_repository = product_repository

    async def execute(self, product_id: UUID) -> bool:
        """Delete a product."""
        return await self._product_repository.delete(product_id)
