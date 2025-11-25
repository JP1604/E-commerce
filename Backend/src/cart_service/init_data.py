"""Script to initialize cart service with sample data."""

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


async def init_sample_data():
    """Initialize the database with sample data."""
    # Database URL
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
            print("🚀 Initializing cart service with sample data...")
            
            # Create sample products
            products_data = [
                {
                    "name": "Laptop Gaming",
                    "description": "Laptop para gaming de alta gama",
                    "price": 1299.99,
                    "status": ProductStatus.ACTIVE
                },
                {
                    "name": "Mouse Inalámbrico",
                    "description": "Mouse inalámbrico ergonómico",
                    "price": 49.99,
                    "status": ProductStatus.ACTIVE
                },
                {
                    "name": "Teclado Mecánico",
                    "description": "Teclado mecánico RGB",
                    "price": 89.99,
                    "status": ProductStatus.ACTIVE
                },
                {
                    "name": "Monitor 4K",
                    "description": "Monitor 4K de 27 pulgadas",
                    "price": 399.99,
                    "status": ProductStatus.ACTIVE
                },
                {
                    "name": "Auriculares Bluetooth",
                    "description": "Auriculares inalámbricos con cancelación de ruido",
                    "price": 199.99,
                    "status": ProductStatus.ACTIVE
                }
            ]
            
            created_products = []
            for product_data in products_data:
                product = Product(**product_data)
                created_product = await product_repo.create(product)
                created_products.append(created_product)
                print(f"✅ Created product: {created_product.name} - ${created_product.price}")
            
            # Create sample users and carts
            users_data = [
                {"user_id": uuid4(), "name": "Juan Pérez"},
                {"user_id": uuid4(), "name": "María García"},
                {"user_id": uuid4(), "name": "Carlos López"}
            ]
            
            for user_data in users_data:
                # Create cart for user
                cart = Cart(user_id=user_data["user_id"], status=CartStatus.ACTIVE)
                created_cart = await cart_repo.create(cart)
                print(f"✅ Created cart for {user_data['name']}: {created_cart.id}")
                
                # Add random products to cart
                import random
                num_items = random.randint(1, 3)
                selected_products = random.sample(created_products, num_items)
                
                for product in selected_products:
                    quantity = random.randint(1, 3)
                    cart_item = CartItem(
                        cart_id=created_cart.id,
                        product_id=product.id,
                        quantity=quantity,
                        unit_price=product.price
                    )
                    created_item = await cart_item_repo.create(cart_item)
                    print(f"  📦 Added {quantity}x {product.name} = ${created_item.subtotal}")
            
            print("\n🎉 Sample data initialization completed!")
            print(f"📊 Created {len(created_products)} products")
            print(f"🛒 Created {len(users_data)} carts with items")
            
        except Exception as e:
            print(f"❌ Error initializing data: {e}")
            raise
        finally:
            await session.close()
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_sample_data())
