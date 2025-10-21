"""Simple integration tests for Cart Service."""

import pytest
import pytest_asyncio
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

# Add the cart_service to the path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from cart_service.domain.entities.product import Product, ProductStatus
from cart_service.domain.entities.cart import Cart, CartStatus
from cart_service.infrastructure.repositories.product_repository_impl import SQLAlchemyProductRepository
from cart_service.infrastructure.repositories.cart_repository_impl import SQLAlchemyCartRepository


@pytest.mark.asyncio
class TestCartServiceSimple:
    """Simple integration tests for Cart Service with database."""
    
    async def test_create_product(self, cart_db_session: AsyncSession):
        """Test creating a product in the database."""
        # Arrange
        product_repo = SQLAlchemyProductRepository(cart_db_session)
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
    
    async def test_create_cart(self, cart_db_session: AsyncSession):
        """Test creating a cart in the database."""
        # Arrange
        cart_repo = SQLAlchemyCartRepository(cart_db_session)
        user_id = uuid4()
        cart = Cart(
            user_id=user_id,
            status=CartStatus.ACTIVE
        )
        
        # Act
        created_cart = await cart_repo.create(cart)
        
        # Assert
        assert created_cart.id is not None
        assert created_cart.user_id == user_id
        assert created_cart.status == CartStatus.ACTIVE
        assert created_cart.created_at is not None
        assert created_cart.updated_at is not None
    
    async def test_get_product_by_id(self, cart_db_session: AsyncSession):
        """Test retrieving a product by ID."""
        # Arrange
        product_repo = SQLAlchemyProductRepository(cart_db_session)
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
    
    async def test_get_cart_by_user_id(self, cart_db_session: AsyncSession):
        """Test retrieving a cart by user ID."""
        # Arrange
        cart_repo = SQLAlchemyCartRepository(cart_db_session)
        user_id = uuid4()
        cart = Cart(
            user_id=user_id,
            status=CartStatus.ACTIVE
        )
        created_cart = await cart_repo.create(cart)
        
        # Act
        retrieved_cart = await cart_repo.get_by_user_id(user_id)
        
        # Assert
        assert retrieved_cart is not None
        assert retrieved_cart.id == created_cart.id
        assert retrieved_cart.user_id == user_id
