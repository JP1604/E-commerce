"""Test script for cart service."""

import asyncio
import sys
from uuid import uuid4
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Add the cart_service to the path
sys.path.append('.')

from cart_service.domain.entities.cart import Cart, CartStatus
from cart_service.domain.entities.cart_item import CartItem
from cart_service.domain.entities.product import Product, ProductStatus
from cart_service.infrastructure.repositories import (
    SQLAlchemyCartRepository,
    SQLAlchemyCartItemRepository,
    SQLAlchemyProductRepository,
)


async def test_cart_service():
    """Test the cart service functionality."""
    # Database URL for testing
    database_url = "postgresql+asyncpg://cart_svc:cart_pass@localhost:5434/cartdb"
    
    # Create engine and session
    engine = create_async_engine(database_url, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Create repositories
        cart_repo = SQLAlchemyCartRepository(session)
        cart_item_repo = SQLAlchemyCartItemRepository(session)
        product_repo = SQLAlchemyProductRepository(session)
        
        try:
            # Test 1: Create a product
            print("Creating product...")
            product = Product(
                name="Test Product",
                description="A test product for the cart",
                price=29.99,
                status=ProductStatus.ACTIVE
            )
            created_product = await product_repo.create(product)
            print(f"Created product: {created_product.name} - ${created_product.price}")
            
            # Test 2: Create a cart
            print("\nCreating cart...")
            user_id = uuid4()
            cart = Cart(user_id=user_id, status=CartStatus.ACTIVE)
            created_cart = await cart_repo.create(cart)
            print(f"Created cart: {created_cart.id} for user: {created_cart.user_id}")
            
            # Test 3: Add item to cart
            print("\nAdding item to cart...")
            cart_item = CartItem(
                cart_id=created_cart.id,
                product_id=created_product.id,
                quantity=2,
                unit_price=created_product.price
            )
            created_item = await cart_item_repo.create(cart_item)
            print(f"Added item: {created_item.quantity}x {created_product.name} = ${created_item.subtotal}")
            
            # Test 4: Get cart items
            print("\nGetting cart items...")
            cart_items = await cart_item_repo.get_by_cart_id(created_cart.id)
            print(f"Cart has {len(cart_items)} items")
            for item in cart_items:
                print(f"  - {item.quantity}x Product (${item.unit_price}) = ${item.subtotal}")
            
            # Test 5: Get cart by user
            print("\nGetting cart by user...")
            user_cart = await cart_repo.get_by_user_id(user_id)
            if user_cart:
                print(f"Found cart for user: {user_cart.id}")
            else:
                print("No cart found for user")
                
            print("\n✅ All tests passed!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            raise
        finally:
            await session.close()
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_cart_service())
