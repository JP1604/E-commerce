"""Create product use case."""

from ...domain.entities.product import Product, ProductStatus
from ...domain.repositories.product_repository import ProductRepository


class CreateProductUseCase:
    """Use case for creating a new product."""

    def __init__(self, product_repository: ProductRepository) -> None:
        self._product_repository = product_repository

    async def execute(
        self,
        name: str,
        description: str,
        price: float,
        status: ProductStatus = ProductStatus.ACTIVE,
    ) -> Product:
        """Create a new product."""
        product = Product(
            name=name,
            description=description,
            price=price,
            status=status,
        )
        return await self._product_repository.create(product)
