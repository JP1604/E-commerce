"""Simple SQLAlchemy implementation of ProductRepository."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...domain.entities import Product
from ...domain.repositories import ProductRepository
from ..database.models import ProductModel


class SQLAlchemyProductRepository(ProductRepository):
    """Simple SQLAlchemy implementation of the ProductRepository interface."""
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def save(self, product: Product) -> Product:
        """Save a product to the database."""
        model = ProductModel(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock_quantity=product.stock_quantity,
        )
        
        self._session.add(model)
        await self._session.flush()
        
        return self._model_to_entity(model)
    
    async def find_by_id(self, product_id: UUID) -> Optional[Product]:
        """Find a product by its ID."""
        query = select(ProductModel).where(ProductModel.id == product_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        return self._model_to_entity(model) if model else None
    
    async def find_all(self) -> List[Product]:
        """Find all products."""
        query = select(ProductModel)
        result = await self._session.execute(query)
        models = result.scalars().all()
        
        return [self._model_to_entity(model) for model in models]
    
    async def update(self, product: Product) -> Product:
        """Update an existing product."""
        query = select(ProductModel).where(ProductModel.id == product.id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"Product with id {product.id} not found")
        
        # Update model fields
        model.name = product.name
        model.description = product.description
        model.price = product.price
        model.stock_quantity = product.stock_quantity
        
        await self._session.flush()
        
        return self._model_to_entity(model)
    
    async def delete(self, product_id: UUID) -> bool:
        """Delete a product by ID."""
        query = select(ProductModel).where(ProductModel.id == product_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        await self._session.delete(model)
        await self._session.flush()
        
        return True
    
    def _model_to_entity(self, model: ProductModel) -> Product:
        """Convert database model to domain entity."""
        return Product(
            name=model.name,
            description=model.description,
            price=model.price,
            stock_quantity=model.stock_quantity,
            id=model.id,
        )