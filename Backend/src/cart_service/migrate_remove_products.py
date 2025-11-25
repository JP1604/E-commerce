"""
Migration script to remove products table from cart service.

Run this after deploying the new version to clean up the database.
"""

from sqlalchemy import text
from cart_service.infrastructure.database.connection import engine
import asyncio


async def migrate():
    """Remove products table and update cart_items FK."""
    
    async with engine.begin() as conn:
        print("Starting migration...")
        
        # Drop the foreign key constraint from cart_items to products
        print("1. Dropping foreign key constraint...")
        await conn.execute(text("""
            ALTER TABLE cart_items 
            DROP CONSTRAINT IF EXISTS cart_items_product_id_fkey;
        """))
        
        # Drop the products table
        print("2. Dropping products table...")
        await conn.execute(text("""
            DROP TABLE IF EXISTS products CASCADE;
        """))
        
        # Drop the product_status enum if it exists
        print("3. Dropping product_status enum...")
        await conn.execute(text("""
            DROP TYPE IF EXISTS product_status CASCADE;
        """))
        
        print("Migration completed successfully!")
        print("Note: Existing cart_items will keep their product_id references.")
        print("Make sure those product IDs exist in the Product Service.")


if __name__ == "__main__":
    asyncio.run(migrate())
