"""Configuration for integration tests."""

import asyncio
import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from testcontainers.postgres import PostgresContainer
from testcontainers.compose import DockerCompose

# Test database configurations
TEST_DATABASES = {
    "product": {
        "user": "ecommerce_user",
        "password": "ecommerce_pass", 
        "database": "ecommerce_test",
        "port": 5432
    },
    "user": {
        "user": "user_svc",
        "password": "user_pass",
        "database": "userdb_test", 
        "port": 5433
    },
    "delivery": {
        "user": "delivery_svc",
        "password": "delivery_pass",
        "database": "deliverydb_test",
        "port": 5434
    },
    "cart": {
        "user": "cart_svc", 
        "password": "cart_pass",
        "database": "cartdb_test",
        "port": 5436
    },
    "order": {
        "user": "order_svc",
        "password": "order_pass", 
        "database": "orderdb_test",
        "port": 5437
    },
    "payment": {
        "user": "payment_svc",
        "password": "payment_pass",
        "database": "paymentdb_test", 
        "port": 5435
    }
}


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def postgres_containers() -> Generator[dict, None, None]:
    """Start PostgreSQL containers for each service."""
    containers = {}
    
    try:
        for service, config in TEST_DATABASES.items():
            container = PostgresContainer(
                image="postgres:16",
                username=config["user"],
                password=config["password"],
                dbname=config["database"]
            )
            container.start()
            containers[service] = container
            
        yield containers
        
    finally:
        for container in containers.values():
            container.stop()


@pytest_asyncio.fixture
async def product_db_session(postgres_containers) -> AsyncGenerator[AsyncSession, None]:
    """Create a database session for product service tests."""
    container = postgres_containers["product"]
    database_url = container.get_connection_url().replace("postgresql://", "postgresql+asyncpg://")
    
    engine = create_async_engine(database_url, echo=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()


@pytest_asyncio.fixture
async def user_db_session(postgres_containers) -> AsyncGenerator[AsyncSession, None]:
    """Create a database session for user service tests."""
    container = postgres_containers["user"]
    database_url = container.get_connection_url().replace("postgresql://", "postgresql+asyncpg://")
    
    engine = create_async_engine(database_url, echo=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()


@pytest_asyncio.fixture
async def cart_db_session(postgres_containers) -> AsyncGenerator[AsyncSession, None]:
    """Create a database session for cart service tests."""
    container = postgres_containers["cart"]
    database_url = container.get_connection_url().replace("postgresql://", "postgresql+asyncpg://")
    
    engine = create_async_engine(database_url, echo=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()


@pytest_asyncio.fixture
async def order_db_session(postgres_containers) -> AsyncGenerator[AsyncSession, None]:
    """Create a database session for order service tests."""
    container = postgres_containers["order"]
    database_url = container.get_connection_url().replace("postgresql://", "postgresql+asyncpg://")
    
    engine = create_async_engine(database_url, echo=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()


@pytest_asyncio.fixture
async def payment_db_session(postgres_containers) -> AsyncGenerator[AsyncSession, None]:
    """Create a database session for payment service tests."""
    container = postgres_containers["payment"]
    database_url = container.get_connection_url().replace("postgresql://", "postgresql+asyncpg://")
    
    engine = create_async_engine(database_url, echo=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()


@pytest_asyncio.fixture
async def delivery_db_session(postgres_containers) -> AsyncGenerator[AsyncSession, None]:
    """Create a database session for delivery service tests."""
    container = postgres_containers["delivery"]
    database_url = container.get_connection_url().replace("postgresql://", "postgresql+asyncpg://")
    
    engine = create_async_engine(database_url, echo=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()
