"""
Migration script to add image_bin column to products table.
Run this once to update your existing database.
"""
import asyncio
from sqlalchemy import text
from infrastructure.database.connection import async_engine


async def add_image_column():
    """Add image_bin column to products table."""
    async with async_engine.begin() as conn:
        # Check if column already exists
        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='products' AND column_name='image_bin';
        """)
        
        result = await conn.execute(check_query)
        exists = result.fetchone()
        
        if not exists:
            print("Adding image_bin column to products table...")
            # Add the column
            alter_query = text("""
                ALTER TABLE products 
                ADD COLUMN image_bin BYTEA NULL;
            """)
            await conn.execute(alter_query)
            print("✅ Column added successfully!")
        else:
            print("ℹ️  Column already exists, no changes needed.")


if __name__ == "__main__":
    print("Running migration: Add image_bin column")
    asyncio.run(add_image_column())
    print("Migration completed!")

