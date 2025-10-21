"""Integration tests for Product Service (Cart Service)."""

import pytest
import pytest_asyncio
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

# Add the cart_service to the path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from cart_service.domain.entities.product import Product, ProductStatus
from cart_service.infrastructure.repositories.product_repository_impl import SQLAlchemyProductRepository


@pytest.mark.asyncio
class TestProductServiceIntegration:
    """Integration tests for Product Service with database."""
    
    async def test_create_product(self, product_db_session: AsyncSession):
        """Test creating a product in the database."""
        # Arrange
        product_repo = SQLAlchemyProductRepository(product_db_session)
        product = Product(
            name="Test Product",
            description="A test product for integration testing",
            price=29.99,
            status=ProductStatus.ACTIVE
        )
        
        # Act
        created_product = await product_repo.create(product)
        
        # Assert
        assert created_product.id is not None
        assert created_product.name == "Test Product"
        assert created_product.description == "A test product for integration testing"
        assert created_product.price == 29.99
        assert created_product.status == ProductStatus.ACTIVE
        assert created_product.created_at is not None
        assert created_product.updated_at is not None
    
    async def test_get_product_by_id(self, product_db_session: AsyncSession):
        """Test retrieving a product by ID."""
        # Arrange
        product_repo = SQLAlchemyProductRepository(product_db_session)
        product = Product(
            name="Retrieval Test Product",
            description="Product for retrieval testing",
            price=19.99,
            status=ProductStatus.ACTIVE
        )
        created_product = await product_repo.create(product)
        
        # Act
        retrieved_product = await product_repo.get_by_id(created_product.id)
        
        # Assert
        assert retrieved_product is not None
        assert retrieved_product.id == created_product.id
        assert retrieved_product.name == "Retrieval Test Product"
        assert retrieved_product.price == 19.99
    
    async def test_get_nonexistent_product(self, product_db_session: AsyncSession):
        """Test retrieving a non-existent product returns None."""
        # Arrange
        product_repo = SQLAlchemyProductRepository(product_db_session)
        nonexistent_id = uuid4()
        
        # Act
        retrieved_product = await product_repo.get_by_id(nonexistent_id)
        
        # Assert
        assert retrieved_product is None
    
    async def test_list_products(self, product_db_session: AsyncSession):
        """Test listing all products."""
        # Arrange
        product_repo = SQLAlchemyProductRepository(product_db_session)
        
        # Create multiple products
        products = [
            Product(name=f"Product {i}", description=f"Description {i}", price=10.0 + i, status=ProductStatus.ACTIVE)
            for i in range(3)
        ]
        
        for product in products:
            await product_repo.create(product)
        
        # Act
        all_products = await product_repo.list_all()
        
        # Assert
        assert len(all_products) >= 3
        product_names = [p.name for p in all_products]
        assert "Product 0" in product_names
        assert "Product 1" in product_names
        assert "Product 2" in product_names
    
    async def test_update_product(self, product_db_session: AsyncSession):
        """Test updating a product."""
        # Arrange
        product_repo = SQLAlchemyProductRepository(product_db_session)
        product = Product(
            name="Original Product",
            description="Original description",
            price=25.00,
            status=ProductStatus.ACTIVE
        )
        created_product = await product_repo.create(product)
        
        # Act
        created_product.name = "Updated Product"
        created_product.description = "Updated description"
        created_product.price = 35.00
        updated_product = await product_repo.update(created_product)
        
        # Assert
        assert updated_product.name == "Updated Product"
        assert updated_product.description == "Updated description"
        assert updated_product.price == 35.00
        assert updated_product.updated_at > created_product.created_at
    
    async def test_delete_product(self, product_db_session: AsyncSession):
        """Test deleting a product."""
        # Arrange
        product_repo = SQLAlchemyProductRepository(product_db_session)
        product = Product(
            name="Product to Delete",
            description="This product will be deleted",
            price=15.00,
            status=ProductStatus.ACTIVE
        )
        created_product = await product_repo.create(product)
        
        # Act
        await product_repo.delete(created_product.id)
        
        # Assert
        deleted_product = await product_repo.get_by_id(created_product.id)
        assert deleted_product is None
    
    async def test_product_status_enum(self, product_db_session: AsyncSession):
        """Test product status enum values."""
        # Arrange
        product_repo = SQLAlchemyProductRepository(product_db_session)
        
        # Test ACTIVE status
        active_product = Product(
            name="Active Product",
            description="Active product",
            price=20.00,
            status=ProductStatus.ACTIVE
        )
        created_active = await product_repo.create(active_product)
        assert created_active.status == ProductStatus.ACTIVE
        
        # Test INACTIVE status
        inactive_product = Product(
            name="Inactive Product", 
            description="Inactive product",
            price=20.00,
            status=ProductStatus.INACTIVE
        )
        created_inactive = await product_repo.create(inactive_product)
        assert created_inactive.status == ProductStatus.INACTIVE
    
    async def test_product_price_precision(self, product_db_session: AsyncSession):
        """Test product price precision handling."""
        # Arrange
        product_repo = SQLAlchemyProductRepository(product_db_session)
        product = Product(
            name="Precision Test Product",
            description="Testing price precision",
            price=19.999,  # 3 decimal places
            status=ProductStatus.ACTIVE
        )
        
        # Act
        created_product = await product_repo.create(product)
        
        # Assert
        # Should handle precision correctly (typically rounded to 2 decimal places)
        assert abs(created_product.price - 19.999) < 0.01
