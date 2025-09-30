"""Database connection management."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from order_service.infrastructure.config.settings import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.order_database_url,
    echo=settings.order_database_echo,
    future=True,
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


async def init_database():
    """Initialize database tables."""
    async with engine.begin() as conn:
        # Import models to ensure they are registered
        from order_service.infrastructure.database.models import order_models
        await conn.run_sync(Base.metadata.create_all)


async def close_database():
    """Close database connections."""
    await engine.dispose()


async def get_db_session():
    """Get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
