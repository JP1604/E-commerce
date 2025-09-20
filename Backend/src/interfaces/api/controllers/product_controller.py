"""Simple product controller."""

from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database import get_db_session
from src.container import get_container, SimpleContainer
from src.domain.entities import Product
from src.application.dtos import ProductCreateDTO, ProductResponseDTO, ProductUpdateDTO


class ProductController:
    """Simple product controller."""
    
    @staticmethod
    async def create_product(
        data: ProductCreateDTO,
        container: SimpleContainer = Depends(get_container)
    ) -> ProductResponseDTO:
        """Create a new product."""
        try:
            product = Product(
                name=data.name,
                description=data.description,
                price=data.price,
                stock_quantity=data.stock_quantity or 0
            )
            
            saved_product = await container.product_repository.save(product)
            return ProductResponseDTO.from_entity(saved_product)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
    @staticmethod
    async def get_product(
        product_id: UUID,
        container: SimpleContainer = Depends(get_container)
    ) -> ProductResponseDTO:
        """Get a product by ID."""
        product = await container.product_repository.find_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        return ProductResponseDTO.from_entity(product)
    
    @staticmethod
    async def get_products(
        container: SimpleContainer = Depends(get_container)
    ) -> List[ProductResponseDTO]:
        """Get all products."""
        products = await container.product_repository.find_all()
        return [ProductResponseDTO.from_entity(product) for product in products]
    
    @staticmethod
    async def update_product(
        product_id: UUID,
        data: ProductUpdateDTO,
        container: SimpleContainer = Depends(get_container)
    ) -> ProductResponseDTO:
        """Update a product."""
        try:
            product = await container.product_repository.find_by_id(product_id)
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
            
            # Update fields if provided
            if data.name is not None:
                product.name = data.name
            if data.description is not None:
                product.description = data.description
            if data.price is not None:
                product.price = data.price
            if data.stock_quantity is not None:
                product.stock_quantity = data.stock_quantity
            
            updated_product = await container.product_repository.update(product)
            return ProductResponseDTO.from_entity(updated_product)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
    @staticmethod
    async def delete_product(
        product_id: UUID,
        container: SimpleContainer = Depends(get_container)
    ) -> dict:
        """Delete a product."""
        product = await container.product_repository.find_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        await container.product_repository.delete(product_id)
        return {"message": "Product deleted successfully"}