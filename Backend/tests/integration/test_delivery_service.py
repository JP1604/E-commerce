"""Integration tests for Delivery Service."""

import pytest
import pytest_asyncio
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

# Add the delivery_service to the path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from delivery_service.domain.entities.delivery import Delivery, DeliveryStatus
from delivery_service.infrastructure.repositories.delivery_repository_impl import SQLAlchemyDeliveryRepository


@pytest.mark.asyncio
class TestDeliveryServiceIntegration:
    """Integration tests for Delivery Service with database."""
    
    async def test_create_delivery(self, delivery_db_session: AsyncSession):
        """Test creating a delivery in the database."""
        # Arrange
        delivery_repo = SQLAlchemyDeliveryRepository(delivery_db_session)
        order_id = uuid4()
        delivery = Delivery(
            order_id=order_id,
            status=DeliveryStatus.PENDING,
            shipping_address="123 Test Street, Test City, TC 12345",
            tracking_number="TRK123456789",
            estimated_delivery_date="2024-12-31",
            carrier="Test Carrier"
        )
        
        # Act
        created_delivery = await delivery_repo.create(delivery)
        
        # Assert
        assert created_delivery.id is not None
        assert created_delivery.order_id == order_id
        assert created_delivery.status == DeliveryStatus.PENDING
        assert created_delivery.shipping_address == "123 Test Street, Test City, TC 12345"
        assert created_delivery.tracking_number == "TRK123456789"
        assert created_delivery.estimated_delivery_date == "2024-12-31"
        assert created_delivery.carrier == "Test Carrier"
        assert created_delivery.created_at is not None
        assert created_delivery.updated_at is not None
    
    async def test_get_delivery_by_id(self, delivery_db_session: AsyncSession):
        """Test retrieving a delivery by ID."""
        # Arrange
        delivery_repo = SQLAlchemyDeliveryRepository(delivery_db_session)
        order_id = uuid4()
        delivery = Delivery(
            order_id=order_id,
            status=DeliveryStatus.PENDING,
            shipping_address="456 Retrieval Ave, Test City, TC 12345",
            tracking_number="TRK987654321",
            estimated_delivery_date="2024-12-25",
            carrier="Retrieval Carrier"
        )
        created_delivery = await delivery_repo.create(delivery)
        
        # Act
        retrieved_delivery = await delivery_repo.get_by_id(created_delivery.id)
        
        # Assert
        assert retrieved_delivery is not None
        assert retrieved_delivery.id == created_delivery.id
        assert retrieved_delivery.order_id == order_id
        assert retrieved_delivery.tracking_number == "TRK987654321"
        assert retrieved_delivery.carrier == "Retrieval Carrier"
    
    async def test_get_delivery_by_order_id(self, delivery_db_session: AsyncSession):
        """Test retrieving a delivery by order ID."""
        # Arrange
        delivery_repo = SQLAlchemyDeliveryRepository(delivery_db_session)
        order_id = uuid4()
        delivery = Delivery(
            order_id=order_id,
            status=DeliveryStatus.PENDING,
            shipping_address="789 Order Street, Test City, TC 12345",
            tracking_number="TRK555666777",
            estimated_delivery_date="2024-12-20",
            carrier="Order Carrier"
        )
        created_delivery = await delivery_repo.create(delivery)
        
        # Act
        retrieved_delivery = await delivery_repo.get_by_order_id(order_id)
        
        # Assert
        assert retrieved_delivery is not None
        assert retrieved_delivery.id == created_delivery.id
        assert retrieved_delivery.order_id == order_id
        assert retrieved_delivery.tracking_number == "TRK555666777"
    
    async def test_list_all_deliveries(self, delivery_db_session: AsyncSession):
        """Test listing all deliveries."""
        # Arrange
        delivery_repo = SQLAlchemyDeliveryRepository(delivery_db_session)
        
        # Create multiple deliveries
        deliveries = [
            Delivery(
                order_id=uuid4(),
                status=DeliveryStatus.PENDING,
                shipping_address=f"{i} List Street, Test City, TC 12345",
                tracking_number=f"TRK{i:09d}",
                estimated_delivery_date="2024-12-15",
                carrier=f"Carrier {i}"
            )
            for i in range(3)
        ]
        
        for delivery in deliveries:
            await delivery_repo.create(delivery)
        
        # Act
        all_deliveries = await delivery_repo.list_all()
        
        # Assert
        assert len(all_deliveries) >= 3
        tracking_numbers = [d.tracking_number for d in all_deliveries]
        assert "TRK000000000" in tracking_numbers
        assert "TRK000000001" in tracking_numbers
        assert "TRK000000002" in tracking_numbers
    
    async def test_update_delivery(self, delivery_db_session: AsyncSession):
        """Test updating a delivery."""
        # Arrange
        delivery_repo = SQLAlchemyDeliveryRepository(delivery_db_session)
        order_id = uuid4()
        delivery = Delivery(
            order_id=order_id,
            status=DeliveryStatus.PENDING,
            shipping_address="999 Update Street, Test City, TC 12345",
            tracking_number="TRK111222333",
            estimated_delivery_date="2024-12-10",
            carrier="Update Carrier"
        )
        created_delivery = await delivery_repo.create(delivery)
        
        # Act
        created_delivery.status = DeliveryStatus.IN_TRANSIT
        created_delivery.tracking_number = "TRK444555666"
        updated_delivery = await delivery_repo.update(created_delivery)
        
        # Assert
        assert updated_delivery.status == DeliveryStatus.IN_TRANSIT
        assert updated_delivery.tracking_number == "TRK444555666"
        assert updated_delivery.updated_at > created_delivery.created_at
    
    async def test_delete_delivery(self, delivery_db_session: AsyncSession):
        """Test deleting a delivery."""
        # Arrange
        delivery_repo = SQLAlchemyDeliveryRepository(delivery_db_session)
        order_id = uuid4()
        delivery = Delivery(
            order_id=order_id,
            status=DeliveryStatus.PENDING,
            shipping_address="777 Delete Street, Test City, TC 12345",
            tracking_number="TRK777888999",
            estimated_delivery_date="2024-12-05",
            carrier="Delete Carrier"
        )
        created_delivery = await delivery_repo.create(delivery)
        
        # Act
        await delivery_repo.delete(created_delivery.id)
        
        # Assert
        deleted_delivery = await delivery_repo.get_by_id(created_delivery.id)
        assert deleted_delivery is None
    
    async def test_delivery_status_enum(self, delivery_db_session: AsyncSession):
        """Test delivery status enum values."""
        # Arrange
        delivery_repo = SQLAlchemyDeliveryRepository(delivery_db_session)
        
        # Test PENDING status
        pending_delivery = Delivery(
            order_id=uuid4(),
            status=DeliveryStatus.PENDING,
            shipping_address="Pending Street, Test City, TC 12345",
            tracking_number="TRK_PENDING",
            estimated_delivery_date="2024-12-01",
            carrier="Pending Carrier"
        )
        created_pending = await delivery_repo.create(pending_delivery)
        assert created_pending.status == DeliveryStatus.PENDING
        
        # Test IN_TRANSIT status
        in_transit_delivery = Delivery(
            order_id=uuid4(),
            status=DeliveryStatus.IN_TRANSIT,
            shipping_address="Transit Street, Test City, TC 12345",
            tracking_number="TRK_TRANSIT",
            estimated_delivery_date="2024-12-02",
            carrier="Transit Carrier"
        )
        created_transit = await delivery_repo.create(in_transit_delivery)
        assert created_transit.status == DeliveryStatus.IN_TRANSIT
        
        # Test DELIVERED status
        delivered_delivery = Delivery(
            order_id=uuid4(),
            status=DeliveryStatus.DELIVERED,
            shipping_address="Delivered Street, Test City, TC 12345",
            tracking_number="TRK_DELIVERED",
            estimated_delivery_date="2024-12-03",
            carrier="Delivered Carrier"
        )
        created_delivered = await delivery_repo.create(delivered_delivery)
        assert created_delivered.status == DeliveryStatus.DELIVERED
        
        # Test FAILED status
        failed_delivery = Delivery(
            order_id=uuid4(),
            status=DeliveryStatus.FAILED,
            shipping_address="Failed Street, Test City, TC 12345",
            tracking_number="TRK_FAILED",
            estimated_delivery_date="2024-12-04",
            carrier="Failed Carrier"
        )
        created_failed = await delivery_repo.create(failed_delivery)
        assert created_failed.status == DeliveryStatus.FAILED
        
        # Test RETURNED status
        returned_delivery = Delivery(
            order_id=uuid4(),
            status=DeliveryStatus.RETURNED,
            shipping_address="Returned Street, Test City, TC 12345",
            tracking_number="TRK_RETURNED",
            estimated_delivery_date="2024-12-05",
            carrier="Returned Carrier"
        )
        created_returned = await delivery_repo.create(returned_delivery)
        assert created_returned.status == DeliveryStatus.RETURNED
    
    async def test_delivery_tracking_number_uniqueness(self, delivery_db_session: AsyncSession):
        """Test that tracking numbers should be unique."""
        # Arrange
        delivery_repo = SQLAlchemyDeliveryRepository(delivery_db_session)
        
        delivery1 = Delivery(
            order_id=uuid4(),
            status=DeliveryStatus.PENDING,
            shipping_address="Unique Street 1, Test City, TC 12345",
            tracking_number="TRK_UNIQUE_123",
            estimated_delivery_date="2024-12-01",
            carrier="Unique Carrier 1"
        )
        
        delivery2 = Delivery(
            order_id=uuid4(),
            status=DeliveryStatus.PENDING,
            shipping_address="Unique Street 2, Test City, TC 12345",
            tracking_number="TRK_UNIQUE_123",  # Same tracking number
            estimated_delivery_date="2024-12-02",
            carrier="Unique Carrier 2"
        )
        
        # Act & Assert
        await delivery_repo.create(delivery1)
        
        # This should raise an exception due to unique constraint
        with pytest.raises(Exception):  # Could be IntegrityError or similar
            await delivery_repo.create(delivery2)
    
    async def test_delivery_with_different_carriers(self, delivery_db_session: AsyncSession):
        """Test deliveries with different carriers."""
        # Arrange
        delivery_repo = SQLAlchemyDeliveryRepository(delivery_db_session)
        
        carriers = ["FedEx", "UPS", "DHL", "USPS"]
        for carrier in carriers:
            delivery = Delivery(
                order_id=uuid4(),
                status=DeliveryStatus.PENDING,
                shipping_address=f"{carrier} Street, Test City, TC 12345",
                tracking_number=f"TRK_{carrier}",
                estimated_delivery_date="2024-12-01",
                carrier=carrier
            )
            created_delivery = await delivery_repo.create(delivery)
            assert created_delivery.carrier == carrier
    
    async def test_delivery_estimated_date_format(self, delivery_db_session: AsyncSession):
        """Test delivery estimated date format handling."""
        # Arrange
        delivery_repo = SQLAlchemyDeliveryRepository(delivery_db_session)
        
        # Test different date formats
        date_formats = [
            "2024-12-31",
            "2024-01-01", 
            "2024-06-15"
        ]
        
        for date_str in date_formats:
            delivery = Delivery(
                order_id=uuid4(),
                status=DeliveryStatus.PENDING,
                shipping_address="Date Street, Test City, TC 12345",
                tracking_number=f"TRK_DATE_{date_str.replace('-', '')}",
                estimated_delivery_date=date_str,
                carrier="Date Carrier"
            )
            created_delivery = await delivery_repo.create(delivery)
            assert created_delivery.estimated_delivery_date == date_str
    
    async def test_delivery_shipping_address_length(self, delivery_db_session: AsyncSession):
        """Test delivery shipping address with different lengths."""
        # Arrange
        delivery_repo = SQLAlchemyDeliveryRepository(delivery_db_session)
        
        # Test short address
        short_address = "123 Main St"
        delivery1 = Delivery(
            order_id=uuid4(),
            status=DeliveryStatus.PENDING,
            shipping_address=short_address,
            tracking_number="TRK_SHORT",
            estimated_delivery_date="2024-12-01",
            carrier="Short Carrier"
        )
        created1 = await delivery_repo.create(delivery1)
        assert created1.shipping_address == short_address
        
        # Test long address
        long_address = "123 Very Long Street Name That Goes On And On, Apartment 456, Building B, Complex Name, City Name, State Name, Country Name, Postal Code 12345-6789"
        delivery2 = Delivery(
            order_id=uuid4(),
            status=DeliveryStatus.PENDING,
            shipping_address=long_address,
            tracking_number="TRK_LONG",
            estimated_delivery_date="2024-12-01",
            carrier="Long Carrier"
        )
        created2 = await delivery_repo.create(delivery2)
        assert created2.shipping_address == long_address
    
    async def test_get_nonexistent_delivery(self, delivery_db_session: AsyncSession):
        """Test retrieving a non-existent delivery returns None."""
        # Arrange
        delivery_repo = SQLAlchemyDeliveryRepository(delivery_db_session)
        nonexistent_id = uuid4()
        
        # Act
        retrieved_delivery = await delivery_repo.get_by_id(nonexistent_id)
        
        # Assert
        assert retrieved_delivery is None
    
    async def test_delivery_order_id_relationship(self, delivery_db_session: AsyncSession):
        """Test that deliveries are properly linked to order IDs."""
        # Arrange
        delivery_repo = SQLAlchemyDeliveryRepository(delivery_db_session)
        order1_id = uuid4()
        order2_id = uuid4()
        
        # Create deliveries for different orders
        delivery1 = Delivery(
            order_id=order1_id,
            status=DeliveryStatus.PENDING,
            shipping_address="Order1 Street, Test City, TC 12345",
            tracking_number="TRK_ORDER1",
            estimated_delivery_date="2024-12-01",
            carrier="Order1 Carrier"
        )
        
        delivery2 = Delivery(
            order_id=order2_id,
            status=DeliveryStatus.IN_TRANSIT,
            shipping_address="Order2 Street, Test City, TC 12345",
            tracking_number="TRK_ORDER2",
            estimated_delivery_date="2024-12-02",
            carrier="Order2 Carrier"
        )
        
        created1 = await delivery_repo.create(delivery1)
        created2 = await delivery_repo.create(delivery2)
        
        # Act
        retrieved1 = await delivery_repo.get_by_order_id(order1_id)
        retrieved2 = await delivery_repo.get_by_order_id(order2_id)
        
        # Assert
        assert retrieved1.id == created1.id
        assert retrieved1.order_id == order1_id
        assert retrieved2.id == created2.id
        assert retrieved2.order_id == order2_id
