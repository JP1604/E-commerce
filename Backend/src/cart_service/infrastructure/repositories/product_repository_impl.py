"""SQLAlchemy implementation of product repository."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from ...domain.entities.product import Product, ProductStatus
from ...domain.repositories.product_repository import ProductRepository
from ..database.models import ProductModel


class SQLAlchemyProductRepository(ProductRepository):
    """SQLAlchemy implementation of product repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, product: Product) -> Product:
        """Create a new product."""
        product_model = ProductModel(
            id_product=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            status=product.status.value,
        )
        self._session.add(product_model)
        await self._session.commit()
        await self._session.refresh(product_model)
        return self._to_entity(product_model)

    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """Get product by ID."""
        result = await self._session.execute(
            select(ProductModel).where(ProductModel.id_product == product_id)
        )
        product_model = result.scalar_one_or_none()
        return self._to_entity(product_model) if product_model else None

    async def get_by_name(self, name: str) -> Optional[Product]:
        """Get product by name."""
        result = await self._session.execute(
            select(ProductModel).where(ProductModel.name == name)
        )
        product_model = result.scalar_one_or_none()
        return self._to_entity(product_model) if product_model else None

    async def list_by_status(self, status: ProductStatus) -> List[Product]:
        """List products by status."""
        result = await self._session.execute(
            select(ProductModel).where(ProductModel.status == status.value)
        )
        product_models = result.scalars().all()
        return [self._to_entity(product_model) for product_model in product_models]

    async def list_all(self) -> List[Product]:
        """List all products."""
        result = await self._session.execute(select(ProductModel))
        product_models = result.scalars().all()
        return [self._to_entity(product_model) for product_model in product_models]

    async def update(self, product: Product) -> Product:
        """Update an existing product."""
        product.update_timestamp()
        await self._session.execute(
            update(ProductModel)
            .where(ProductModel.id_product == product.id)
            .values(
                name=product.name,
                description=product.description,
                price=product.price,
                status=product.status.value,
                updated_at=product.updated_at,
            )
        )
        await self._session.commit()
        return product

    async def delete(self, product_id: UUID) -> bool:
        """Delete a product."""
        result = await self._session.execute(
            delete(ProductModel).where(ProductModel.id_product == product_id)
        )
        await self._session.commit()
        return result.rowcount > 0

    def _to_entity(self, product_model: ProductModel) -> Product:
        """Convert model to entity."""
        return Product(
            id_product=product_model.id_product,
            name=product_model.name,
            description=product_model.description,
            price=product_model.price,
            status=ProductStatus(product_model.status),
        )
