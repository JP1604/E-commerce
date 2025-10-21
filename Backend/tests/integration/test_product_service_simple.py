"""Simplified integration tests for Product Service - no database required."""

import pytest
import pytest_asyncio
from uuid import uuid4
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from cart_service.domain.entities.product import Product, ProductStatus


@pytest.mark.asyncio
class TestProductServiceSimple:
    """Simplified integration tests for Product Service."""

    async def test_create_product_entity(self):
        """Test creating a product entity."""
        product = Product(
            name="Test Product",
            description="A test product for integration testing",
            price=29.99,
            status=ProductStatus.ACTIVE
        )
        
        assert product.name == "Test Product"
        assert product.description == "A test product for integration testing"
        assert product.price == 29.99
        assert product.status == ProductStatus.ACTIVE
        assert product.id is not None

    async def test_product_status_enum(self):
        """Test product status enumeration."""
        assert ProductStatus.ACTIVE.value == "activo"
        assert ProductStatus.INACTIVE.value == "inactivo"

    async def test_product_validation(self):
        """Test product validation."""
        # Test valid product
        product = Product(
            name="Valid Product",
            description="A valid product",
            price=19.99,
            status=ProductStatus.ACTIVE
        )
        assert product.name == "Valid Product"
        
        # Test invalid product name
        with pytest.raises(ValueError, match="Product name is required"):
            Product(
                name="",
                description="Invalid product",
                price=19.99,
                status=ProductStatus.ACTIVE
            )
        
        # Test invalid product price
        with pytest.raises(ValueError, match="Product price must be non-negative"):
            Product(
                name="Invalid Price Product",
                description="Product with negative price",
                price=-10.0,
                status=ProductStatus.ACTIVE
            )

    async def test_product_to_dict(self):
        """Test product serialization."""
        product = Product(
            name="Serialization Test Product",
            description="Product for serialization testing",
            price=15.99,
            status=ProductStatus.ACTIVE
        )
        
        product_dict = product.to_dict()
        
        assert product_dict["name"] == "Serialization Test Product"
        assert product_dict["description"] == "Product for serialization testing"
        assert product_dict["price"] == 15.99
        assert product_dict["status"] == "activo"
        assert "id_product" in product_dict
        assert "created_at" in product_dict
        assert "updated_at" in product_dict

    async def test_product_with_different_statuses(self):
        """Test products with different statuses."""
        # Active product
        active_product = Product(
            name="Active Product",
            description="An active product",
            price=25.0,
            status=ProductStatus.ACTIVE
        )
        assert active_product.status == ProductStatus.ACTIVE
        
        # Inactive product
        inactive_product = Product(
            name="Inactive Product",
            description="An inactive product",
            price=30.0,
            status=ProductStatus.INACTIVE
        )
        assert inactive_product.status == ProductStatus.INACTIVE

    async def test_product_price_precision(self):
        """Test product price precision."""
        product = Product(
            name="Precision Test Product",
            description="Product for price precision testing",
            price=19.999,
            status=ProductStatus.ACTIVE
        )
        
        # Price should be stored as provided
        assert product.price == 19.999

    async def test_product_with_zero_price(self):
        """Test product with zero price."""
        product = Product(
            name="Free Product",
            description="A free product",
            price=0.0,
            status=ProductStatus.ACTIVE
        )
        
        assert product.price == 0.0
        assert product.name == "Free Product"

    async def test_product_entity_immutability(self):
        """Test that product entity properties are properly set."""
        product = Product(
            name="Immutability Test",
            description="Testing entity immutability",
            price=12.50,
            status=ProductStatus.ACTIVE
        )
        
        # All properties should be set correctly
        assert product.name == "Immutability Test"
        assert product.description == "Testing entity immutability"
        assert product.price == 12.50
        assert product.status == ProductStatus.ACTIVE
        assert product.id is not None
        assert product.created_at is not None
        assert product.updated_at is not None
