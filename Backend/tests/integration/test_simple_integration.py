"""Simple integration tests without testcontainers."""

import pytest
import pytest_asyncio
from uuid import uuid4
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Add the cart_service to the path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from cart_service.domain.entities.product import Product, ProductStatus
from cart_service.domain.entities.cart import Cart, CartStatus


@pytest_asyncio.fixture
async def test_db_session():
    """Create a test database session."""
    # Use a simple in-memory SQLite database for testing
    database_url = "sqlite+aiosqlite:///:memory:"
    
    engine = create_async_engine(database_url, echo=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()


@pytest.mark.asyncio
class TestSimpleIntegration:
    """Simple integration tests."""
    
    async def test_create_product_entity(self):
        """Test creating a product entity (no database)."""
        # Arrange & Act
        product = Product(
            name="Test Product",
            description="A test product",
            price=29.99,
            status=ProductStatus.ACTIVE
        )
        
        # Assert
        assert product.name == "Test Product"
        assert product.description == "A test product"
        assert product.price == 29.99
        assert product.status == ProductStatus.ACTIVE
        assert product.id is not None
        assert product.created_at is not None
        assert product.updated_at is not None
    
    async def test_create_cart_entity(self):
        """Test creating a cart entity (no database)."""
        # Arrange
        user_id = uuid4()
        
        # Act
        cart = Cart(
            user_id=user_id,
            status=CartStatus.ACTIVE
        )
        
        # Assert
        assert cart.user_id == user_id
        assert cart.status == CartStatus.ACTIVE
        assert cart.id is not None
        assert cart.created_at is not None
        assert cart.updated_at is not None
    
    async def test_product_status_enum(self):
        """Test product status enum values."""
        # Test ACTIVE status
        assert ProductStatus.ACTIVE == "activo"
        assert ProductStatus.INACTIVE == "inactivo"
        
        # Test creating products with different statuses
        active_product = Product(
            name="Active Product",
            description="Active product",
            price=20.00,
            status=ProductStatus.ACTIVE
        )
        assert active_product.status == ProductStatus.ACTIVE
        
        inactive_product = Product(
            name="Inactive Product", 
            description="Inactive product",
            price=20.00,
            status=ProductStatus.INACTIVE
        )
        assert inactive_product.status == ProductStatus.INACTIVE
    
    async def test_cart_status_enum(self):
        """Test cart status enum values."""
        # Test status values
        assert CartStatus.ACTIVE == "activo"
        assert CartStatus.EMPTY == "vacio"
        
        # Test creating carts with different statuses
        active_cart = Cart(
            user_id=uuid4(),
            status=CartStatus.ACTIVE
        )
        assert active_cart.status == CartStatus.ACTIVE
        
        empty_cart = Cart(
            user_id=uuid4(),
            status=CartStatus.EMPTY
        )
        assert empty_cart.status == CartStatus.EMPTY
    
    async def test_product_validation(self):
        """Test product validation."""
        # Test valid product
        valid_product = Product(
            name="Valid Product",
            description="Valid description",
            price=10.00,
            status=ProductStatus.ACTIVE
        )
        assert valid_product.name == "Valid Product"
        
        # Test invalid product (empty name)
        with pytest.raises(ValueError, match="Product name is required"):
            Product(
                name="",
                description="Valid description",
                price=10.00,
                status=ProductStatus.ACTIVE
            )
        
        # Test invalid product (negative price)
        with pytest.raises(ValueError, match="Product price must be non-negative"):
            Product(
                name="Valid Product",
                description="Valid description",
                price=-10.00,
                status=ProductStatus.ACTIVE
            )
    
    async def test_cart_validation(self):
        """Test cart validation."""
        # Test valid cart
        valid_cart = Cart(
            user_id=uuid4(),
            status=CartStatus.ACTIVE
        )
        assert valid_cart.user_id is not None
        
        # Test invalid cart (no user_id)
        with pytest.raises(ValueError, match="User ID is required"):
            Cart(
                user_id=None,
                status=CartStatus.ACTIVE
            )
    
    async def test_product_to_dict(self):
        """Test product to_dict method."""
        # Arrange
        product = Product(
            name="Dict Test Product",
            description="Product for dict testing",
            price=15.50,
            status=ProductStatus.ACTIVE
        )
        
        # Act
        product_dict = product.to_dict()
        
        # Assert
        assert product_dict["name"] == "Dict Test Product"
        assert product_dict["description"] == "Product for dict testing"
        assert product_dict["price"] == 15.50
        assert product_dict["status"] == "activo"
        assert "id_product" in product_dict
        assert "created_at" in product_dict
        assert "updated_at" in product_dict
    
    async def test_cart_to_dict(self):
        """Test cart to_dict method."""
        # Arrange
        user_id = uuid4()
        cart = Cart(
            user_id=user_id,
            status=CartStatus.ACTIVE
        )
        
        # Act
        cart_dict = cart.to_dict()
        
        # Assert
        assert cart_dict["user_id"] == user_id  # UUID objects are compared directly
        assert cart_dict["status"] == "activo"
        assert "id_cart" in cart_dict
        assert "created_at" in cart_dict
        assert "updated_at" in cart_dict
