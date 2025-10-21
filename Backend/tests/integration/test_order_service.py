"""Integration tests for Order Service."""

import pytest
import pytest_asyncio
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

# Add the order_service to the path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from order_service.domain.entities.order import Order, OrderStatus
from order_service.infrastructure.repositories.sqlalchemy_order_repository import SQLAlchemyOrderRepository


@pytest.mark.asyncio
class TestOrderServiceIntegration:
    """Integration tests for Order Service with database."""
    
    async def test_create_order(self, order_db_session: AsyncSession):
        """Test creating an order in the database."""
        # Arrange
        order_repo = SQLAlchemyOrderRepository(order_db_session)
        user_id = uuid4()
        order = Order(
            user_id=user_id,
            status=OrderStatus.PENDING,
            total_amount=99.99,
            shipping_address="123 Test Street, Test City, TC 12345"
        )
        
        # Act
        created_order = await order_repo.create(order)
        
        # Assert
        assert created_order.id is not None
        assert created_order.user_id == user_id
        assert created_order.status == OrderStatus.PENDING
        assert created_order.total_amount == 99.99
        assert created_order.shipping_address == "123 Test Street, Test City, TC 12345"
        assert created_order.created_at is not None
        assert created_order.updated_at is not None
    
    async def test_get_order_by_id(self, order_db_session: AsyncSession):
        """Test retrieving an order by ID."""
        # Arrange
        order_repo = SQLAlchemyOrderRepository(order_db_session)
        user_id = uuid4()
        order = Order(
            user_id=user_id,
            status=OrderStatus.PENDING,
            total_amount=149.99,
            shipping_address="456 Retrieval Ave, Test City, TC 12345"
        )
        created_order = await order_repo.create(order)
        
        # Act
        retrieved_order = await order_repo.get_by_id(created_order.id)
        
        # Assert
        assert retrieved_order is not None
        assert retrieved_order.id == created_order.id
        assert retrieved_order.user_id == user_id
        assert retrieved_order.total_amount == 149.99
        assert retrieved_order.status == OrderStatus.PENDING
    
    async def test_get_orders_by_user_id(self, order_db_session: AsyncSession):
        """Test retrieving orders by user ID."""
        # Arrange
        order_repo = SQLAlchemyOrderRepository(order_db_session)
        user_id = uuid4()
        
        # Create multiple orders for the same user
        orders = [
            Order(
                user_id=user_id,
                status=OrderStatus.PENDING,
                total_amount=50.00 + i * 10,
                shipping_address=f"{i} User Street, Test City, TC 12345"
            )
            for i in range(3)
        ]
        
        created_orders = []
        for order in orders:
            created_orders.append(await order_repo.create(order))
        
        # Act
        user_orders = await order_repo.get_by_user_id(user_id)
        
        # Assert
        assert len(user_orders) == 3
        assert all(order.user_id == user_id for order in user_orders)
        order_amounts = [order.total_amount for order in user_orders]
        assert 50.00 in order_amounts
        assert 60.00 in order_amounts
        assert 70.00 in order_amounts
    
    async def test_list_all_orders(self, order_db_session: AsyncSession):
        """Test listing all orders."""
        # Arrange
        order_repo = SQLAlchemyOrderRepository(order_db_session)
        
        # Create orders for different users
        orders = [
            Order(
                user_id=uuid4(),
                status=OrderStatus.PENDING,
                total_amount=25.00 + i * 5,
                shipping_address=f"{i} List Street, Test City, TC 12345"
            )
            for i in range(3)
        ]
        
        for order in orders:
            await order_repo.create(order)
        
        # Act
        all_orders = await order_repo.list_all()
        
        # Assert
        assert len(all_orders) >= 3
        order_amounts = [order.total_amount for order in all_orders]
        assert 25.00 in order_amounts
        assert 30.00 in order_amounts
        assert 35.00 in order_amounts
    
    async def test_update_order(self, order_db_session: AsyncSession):
        """Test updating an order."""
        # Arrange
        order_repo = SQLAlchemyOrderRepository(order_db_session)
        user_id = uuid4()
        order = Order(
            user_id=user_id,
            status=OrderStatus.PENDING,
            total_amount=75.00,
            shipping_address="789 Update Street, Test City, TC 12345"
        )
        created_order = await order_repo.create(order)
        
        # Act
        created_order.status = OrderStatus.CONFIRMED
        created_order.total_amount = 80.00
        updated_order = await order_repo.update(created_order)
        
        # Assert
        assert updated_order.status == OrderStatus.CONFIRMED
        assert updated_order.total_amount == 80.00
        assert updated_order.updated_at > created_order.created_at
    
    async def test_delete_order(self, order_db_session: AsyncSession):
        """Test deleting an order."""
        # Arrange
        order_repo = SQLAlchemyOrderRepository(order_db_session)
        user_id = uuid4()
        order = Order(
            user_id=user_id,
            status=OrderStatus.PENDING,
            total_amount=100.00,
            shipping_address="999 Delete Street, Test City, TC 12345"
        )
        created_order = await order_repo.create(order)
        
        # Act
        await order_repo.delete(created_order.id)
        
        # Assert
        deleted_order = await order_repo.get_by_id(created_order.id)
        assert deleted_order is None
    
    async def test_order_status_enum(self, order_db_session: AsyncSession):
        """Test order status enum values."""
        # Arrange
        order_repo = SQLAlchemyOrderRepository(order_db_session)
        
        # Test PENDING status
        pending_order = Order(
            user_id=uuid4(),
            status=OrderStatus.PENDING,
            total_amount=50.00,
            shipping_address="Pending Street, Test City, TC 12345"
        )
        created_pending = await order_repo.create(pending_order)
        assert created_pending.status == OrderStatus.PENDING
        
        # Test CONFIRMED status
        confirmed_order = Order(
            user_id=uuid4(),
            status=OrderStatus.CONFIRMED,
            total_amount=60.00,
            shipping_address="Confirmed Street, Test City, TC 12345"
        )
        created_confirmed = await order_repo.create(confirmed_order)
        assert created_confirmed.status == OrderStatus.CONFIRMED
        
        # Test SHIPPED status
        shipped_order = Order(
            user_id=uuid4(),
            status=OrderStatus.SHIPPED,
            total_amount=70.00,
            shipping_address="Shipped Street, Test City, TC 12345"
        )
        created_shipped = await order_repo.create(shipped_order)
        assert created_shipped.status == OrderStatus.SHIPPED
        
        # Test DELIVERED status
        delivered_order = Order(
            user_id=uuid4(),
            status=OrderStatus.DELIVERED,
            total_amount=80.00,
            shipping_address="Delivered Street, Test City, TC 12345"
        )
        created_delivered = await order_repo.create(delivered_order)
        assert created_delivered.status == OrderStatus.DELIVERED
        
        # Test CANCELLED status
        cancelled_order = Order(
            user_id=uuid4(),
            status=OrderStatus.CANCELLED,
            total_amount=90.00,
            shipping_address="Cancelled Street, Test City, TC 12345"
        )
        created_cancelled = await order_repo.create(cancelled_order)
        assert created_cancelled.status == OrderStatus.CANCELLED
    
    async def test_order_total_amount_precision(self, order_db_session: AsyncSession):
        """Test order total amount precision handling."""
        # Arrange
        order_repo = SQLAlchemyOrderRepository(order_db_session)
        user_id = uuid4()
        order = Order(
            user_id=user_id,
            status=OrderStatus.PENDING,
            total_amount=123.456,  # 3 decimal places
            shipping_address="Precision Street, Test City, TC 12345"
        )
        
        # Act
        created_order = await order_repo.create(order)
        
        # Assert
        # Should handle precision correctly (typically rounded to 2 decimal places)
        assert abs(created_order.total_amount - 123.456) < 0.01
    
    async def test_order_with_different_users(self, order_db_session: AsyncSession):
        """Test orders from different users are properly separated."""
        # Arrange
        order_repo = SQLAlchemyOrderRepository(order_db_session)
        user1_id = uuid4()
        user2_id = uuid4()
        
        # Create orders for different users
        order1 = Order(
            user_id=user1_id,
            status=OrderStatus.PENDING,
            total_amount=100.00,
            shipping_address="User1 Street, Test City, TC 12345"
        )
        order2 = Order(
            user_id=user2_id,
            status=OrderStatus.CONFIRMED,
            total_amount=200.00,
            shipping_address="User2 Street, Test City, TC 12345"
        )
        
        created_order1 = await order_repo.create(order1)
        created_order2 = await order_repo.create(order2)
        
        # Act
        user1_orders = await order_repo.get_by_user_id(user1_id)
        user2_orders = await order_repo.get_by_user_id(user2_id)
        
        # Assert
        assert len(user1_orders) == 1
        assert len(user2_orders) == 1
        assert user1_orders[0].id == created_order1.id
        assert user2_orders[0].id == created_order2.id
        assert user1_orders[0].user_id == user1_id
        assert user2_orders[0].user_id == user2_id
    
    async def test_get_nonexistent_order(self, order_db_session: AsyncSession):
        """Test retrieving a non-existent order returns None."""
        # Arrange
        order_repo = SQLAlchemyOrderRepository(order_db_session)
        nonexistent_id = uuid4()
        
        # Act
        retrieved_order = await order_repo.get_by_id(nonexistent_id)
        
        # Assert
        assert retrieved_order is None
