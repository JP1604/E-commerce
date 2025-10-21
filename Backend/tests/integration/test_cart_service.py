"""Integration tests for Cart Service."""

import pytest
import pytest_asyncio
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

# Add the cart_service to the path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from cart_service.domain.entities.cart import Cart, CartStatus
from cart_service.domain.entities.cart_item import CartItem
from cart_service.domain.entities.product import Product, ProductStatus
from cart_service.infrastructure.repositories.cart_repository_impl import SQLAlchemyCartRepository
from cart_service.infrastructure.repositories.cart_item_repository_impl import SQLAlchemyCartItemRepository
from cart_service.infrastructure.repositories.product_repository_impl import SQLAlchemyProductRepository


@pytest.mark.asyncio
class TestCartServiceIntegration:
    """Integration tests for Cart Service with database."""
    
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
    
    async def test_get_cart_by_id(self, cart_db_session: AsyncSession):
        """Test retrieving a cart by ID."""
        # Arrange
        cart_repo = SQLAlchemyCartRepository(cart_db_session)
        user_id = uuid4()
        cart = Cart(
            user_id=user_id,
            status=CartStatus.ACTIVE
        )
        created_cart = await cart_repo.create(cart)
        
        # Act
        retrieved_cart = await cart_repo.get_by_id(created_cart.id)
        
        # Assert
        assert retrieved_cart is not None
        assert retrieved_cart.id == created_cart.id
        assert retrieved_cart.user_id == user_id
        assert retrieved_cart.status == CartStatus.ACTIVE
    
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
    
    async def test_create_cart_item(self, cart_db_session: AsyncSession):
        """Test creating a cart item in the database."""
        # Arrange
        cart_repo = SQLAlchemyCartRepository(cart_db_session)
        product_repo = SQLAlchemyProductRepository(cart_db_session)
        cart_item_repo = SQLAlchemyCartItemRepository(cart_db_session)
        
        # Create a cart and product first
        user_id = uuid4()
        cart = Cart(user_id=user_id, status=CartStatus.ACTIVE)
        created_cart = await cart_repo.create(cart)
        
        product = Product(
            name="Test Product",
            description="A test product",
            price=29.99,
            status=ProductStatus.ACTIVE
        )
        created_product = await product_repo.create(product)
        
        cart_item = CartItem(
            cart_id=created_cart.id,
            product_id=created_product.id,
            quantity=2,
            unit_price=created_product.price
        )
        
        # Act
        created_item = await cart_item_repo.create(cart_item)
        
        # Assert
        assert created_item.id is not None
        assert created_item.cart_id == created_cart.id
        assert created_item.product_id == created_product.id
        assert created_item.quantity == 2
        assert created_item.unit_price == 29.99
        assert created_item.subtotal == 59.98  # 2 * 29.99
        assert created_item.created_at is not None
        assert created_item.updated_at is not None
    
    async def test_get_cart_items_by_cart_id(self, cart_db_session: AsyncSession):
        """Test retrieving cart items by cart ID."""
        # Arrange
        cart_repo = SQLAlchemyCartRepository(cart_db_session)
        product_repo = SQLAlchemyProductRepository(cart_db_session)
        cart_item_repo = SQLAlchemyCartItemRepository(cart_db_session)
        
        # Create cart and products
        user_id = uuid4()
        cart = Cart(user_id=user_id, status=CartStatus.ACTIVE)
        created_cart = await cart_repo.create(cart)
        
        products = [
            Product(name=f"Product {i}", description=f"Description {i}", price=10.0 + i, status=ProductStatus.ACTIVE)
            for i in range(2)
        ]
        created_products = []
        for product in products:
            created_products.append(await product_repo.create(product))
        
        # Create cart items
        cart_items = [
            CartItem(
                cart_id=created_cart.id,
                product_id=created_products[i].id,
                quantity=i + 1,
                unit_price=created_products[i].price
            )
            for i in range(2)
        ]
        
        for item in cart_items:
            await cart_item_repo.create(item)
        
        # Act
        retrieved_items = await cart_item_repo.get_by_cart_id(created_cart.id)
        
        # Assert
        assert len(retrieved_items) == 2
        assert all(item.cart_id == created_cart.id for item in retrieved_items)
    
    async def test_update_cart_item(self, cart_db_session: AsyncSession):
        """Test updating a cart item."""
        # Arrange
        cart_repo = SQLAlchemyCartRepository(cart_db_session)
        product_repo = SQLAlchemyProductRepository(cart_db_session)
        cart_item_repo = SQLAlchemyCartItemRepository(cart_db_session)
        
        # Create cart, product, and cart item
        user_id = uuid4()
        cart = Cart(user_id=user_id, status=CartStatus.ACTIVE)
        created_cart = await cart_repo.create(cart)
        
        product = Product(
            name="Update Test Product",
            description="Product for update testing",
            price=15.00,
            status=ProductStatus.ACTIVE
        )
        created_product = await product_repo.create(product)
        
        cart_item = CartItem(
            cart_id=created_cart.id,
            product_id=created_product.id,
            quantity=1,
            unit_price=created_product.price
        )
        created_item = await cart_item_repo.create(cart_item)
        
        # Act
        created_item.quantity = 3
        updated_item = await cart_item_repo.update(created_item)
        
        # Assert
        assert updated_item.quantity == 3
        assert updated_item.subtotal == 45.00  # 3 * 15.00
        assert updated_item.updated_at > created_item.created_at
    
    async def test_delete_cart_item(self, cart_db_session: AsyncSession):
        """Test deleting a cart item."""
        # Arrange
        cart_repo = SQLAlchemyCartRepository(cart_db_session)
        product_repo = SQLAlchemyProductRepository(cart_db_session)
        cart_item_repo = SQLAlchemyCartItemRepository(cart_db_session)
        
        # Create cart, product, and cart item
        user_id = uuid4()
        cart = Cart(user_id=user_id, status=CartStatus.ACTIVE)
        created_cart = await cart_repo.create(cart)
        
        product = Product(
            name="Delete Test Product",
            description="Product for delete testing",
            price=20.00,
            status=ProductStatus.ACTIVE
        )
        created_product = await product_repo.create(product)
        
        cart_item = CartItem(
            cart_id=created_cart.id,
            product_id=created_product.id,
            quantity=1,
            unit_price=created_product.price
        )
        created_item = await cart_item_repo.create(cart_item)
        
        # Act
        await cart_item_repo.delete(created_item.id)
        
        # Assert
        deleted_item = await cart_item_repo.get_by_id(created_item.id)
        assert deleted_item is None
    
    async def test_cart_status_enum(self, cart_db_session: AsyncSession):
        """Test cart status enum values."""
        # Arrange
        cart_repo = SQLAlchemyCartRepository(cart_db_session)
        
        # Test ACTIVE status
        active_cart = Cart(
            user_id=uuid4(),
            status=CartStatus.ACTIVE
        )
        created_active = await cart_repo.create(active_cart)
        assert created_active.status == CartStatus.ACTIVE
        
        # Test ABANDONED status
        abandoned_cart = Cart(
            user_id=uuid4(),
            status=CartStatus.ABANDONED
        )
        created_abandoned = await cart_repo.create(abandoned_cart)
        assert created_abandoned.status == CartStatus.ABANDONED
        
        # Test COMPLETED status
        completed_cart = Cart(
            user_id=uuid4(),
            status=CartStatus.COMPLETED
        )
        created_completed = await cart_repo.create(completed_cart)
        assert created_completed.status == CartStatus.COMPLETED
    
    async def test_cart_item_subtotal_calculation(self, cart_db_session: AsyncSession):
        """Test that cart item subtotal is calculated correctly."""
        # Arrange
        cart_repo = SQLAlchemyCartRepository(cart_db_session)
        product_repo = SQLAlchemyProductRepository(cart_db_session)
        cart_item_repo = SQLAlchemyCartItemRepository(cart_db_session)
        
        # Create cart and product
        user_id = uuid4()
        cart = Cart(user_id=user_id, status=CartStatus.ACTIVE)
        created_cart = await cart_repo.create(cart)
        
        product = Product(
            name="Subtotal Test Product",
            description="Product for subtotal testing",
            price=12.50,
            status=ProductStatus.ACTIVE
        )
        created_product = await product_repo.create(product)
        
        cart_item = CartItem(
            cart_id=created_cart.id,
            product_id=created_product.id,
            quantity=4,
            unit_price=created_product.price
        )
        
        # Act
        created_item = await cart_item_repo.create(cart_item)
        
        # Assert
        expected_subtotal = 4 * 12.50  # 50.00
        assert created_item.subtotal == expected_subtotal
    
    async def test_cart_with_multiple_items(self, cart_db_session: AsyncSession):
        """Test a cart with multiple different items."""
        # Arrange
        cart_repo = SQLAlchemyCartRepository(cart_db_session)
        product_repo = SQLAlchemyProductRepository(cart_db_session)
        cart_item_repo = SQLAlchemyCartItemRepository(cart_db_session)
        
        # Create cart
        user_id = uuid4()
        cart = Cart(user_id=user_id, status=CartStatus.ACTIVE)
        created_cart = await cart_repo.create(cart)
        
        # Create multiple products
        products = [
            Product(name="Product A", description="Product A", price=10.00, status=ProductStatus.ACTIVE),
            Product(name="Product B", description="Product B", price=20.00, status=ProductStatus.ACTIVE),
            Product(name="Product C", description="Product C", price=30.00, status=ProductStatus.ACTIVE),
        ]
        created_products = []
        for product in products:
            created_products.append(await product_repo.create(product))
        
        # Create cart items with different quantities
        cart_items = [
            CartItem(cart_id=created_cart.id, product_id=created_products[0].id, quantity=2, unit_price=10.00),
            CartItem(cart_id=created_cart.id, product_id=created_products[1].id, quantity=1, unit_price=20.00),
            CartItem(cart_id=created_cart.id, product_id=created_products[2].id, quantity=3, unit_price=30.00),
        ]
        
        for item in cart_items:
            await cart_item_repo.create(item)
        
        # Act
        all_items = await cart_item_repo.get_by_cart_id(created_cart.id)
        
        # Assert
        assert len(all_items) == 3
        total_value = sum(item.subtotal for item in all_items)
        expected_total = (2 * 10.00) + (1 * 20.00) + (3 * 30.00)  # 20 + 20 + 90 = 130
        assert total_value == expected_total
