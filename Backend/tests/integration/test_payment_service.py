"""Integration tests for Payment Service."""

import pytest
import pytest_asyncio
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

# Add the payment_service to the path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from payment_service.domain.entities.payment import Payment, PaymentStatus, PaymentMethod
from payment_service.infrastructure.repositories.payment_repository_impl import SQLAlchemyPaymentRepository


@pytest.mark.asyncio
class TestPaymentServiceIntegration:
    """Integration tests for Payment Service with database."""
    
    async def test_create_payment(self, payment_db_session: AsyncSession):
        """Test creating a payment in the database."""
        # Arrange
        payment_repo = SQLAlchemyPaymentRepository(payment_db_session)
        user_id = uuid4()
        order_id = uuid4()
        payment = Payment(
            user_id=user_id,
            order_id=order_id,
            amount=99.99,
            currency="USD",
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.PENDING,
            gateway_transaction_id="txn_test_123"
        )
        
        # Act
        created_payment = await payment_repo.create(payment)
        
        # Assert
        assert created_payment.id is not None
        assert created_payment.user_id == user_id
        assert created_payment.order_id == order_id
        assert created_payment.amount == 99.99
        assert created_payment.currency == "USD"
        assert created_payment.payment_method == PaymentMethod.CREDIT_CARD
        assert created_payment.status == PaymentStatus.PENDING
        assert created_payment.gateway_transaction_id == "txn_test_123"
        assert created_payment.created_at is not None
        assert created_payment.updated_at is not None
    
    async def test_get_payment_by_id(self, payment_db_session: AsyncSession):
        """Test retrieving a payment by ID."""
        # Arrange
        payment_repo = SQLAlchemyPaymentRepository(payment_db_session)
        user_id = uuid4()
        order_id = uuid4()
        payment = Payment(
            user_id=user_id,
            order_id=order_id,
            amount=149.99,
            currency="USD",
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.PENDING,
            gateway_transaction_id="txn_retrieval_456"
        )
        created_payment = await payment_repo.create(payment)
        
        # Act
        retrieved_payment = await payment_repo.get_by_id(created_payment.id)
        
        # Assert
        assert retrieved_payment is not None
        assert retrieved_payment.id == created_payment.id
        assert retrieved_payment.user_id == user_id
        assert retrieved_payment.order_id == order_id
        assert retrieved_payment.amount == 149.99
        assert retrieved_payment.gateway_transaction_id == "txn_retrieval_456"
    
    async def test_get_payments_by_user_id(self, payment_db_session: AsyncSession):
        """Test retrieving payments by user ID."""
        # Arrange
        payment_repo = SQLAlchemyPaymentRepository(payment_db_session)
        user_id = uuid4()
        
        # Create multiple payments for the same user
        payments = [
            Payment(
                user_id=user_id,
                order_id=uuid4(),
                amount=50.00 + i * 10,
                currency="USD",
                payment_method=PaymentMethod.CREDIT_CARD,
                status=PaymentStatus.PENDING,
                gateway_transaction_id=f"txn_user_{i}"
            )
            for i in range(3)
        ]
        
        created_payments = []
        for payment in payments:
            created_payments.append(await payment_repo.create(payment))
        
        # Act
        user_payments = await payment_repo.get_by_user_id(user_id)
        
        # Assert
        assert len(user_payments) == 3
        assert all(payment.user_id == user_id for payment in user_payments)
        payment_amounts = [payment.amount for payment in user_payments]
        assert 50.00 in payment_amounts
        assert 60.00 in payment_amounts
        assert 70.00 in payment_amounts
    
    async def test_get_payments_by_order_id(self, payment_db_session: AsyncSession):
        """Test retrieving payments by order ID."""
        # Arrange
        payment_repo = SQLAlchemyPaymentRepository(payment_db_session)
        user_id = uuid4()
        order_id = uuid4()
        
        # Create multiple payments for the same order
        payments = [
            Payment(
                user_id=user_id,
                order_id=order_id,
                amount=25.00 + i * 5,
                currency="USD",
                payment_method=PaymentMethod.CREDIT_CARD,
                status=PaymentStatus.PENDING,
                gateway_transaction_id=f"txn_order_{i}"
            )
            for i in range(2)
        ]
        
        for payment in payments:
            await payment_repo.create(payment)
        
        # Act
        order_payments = await payment_repo.get_by_order_id(order_id)
        
        # Assert
        assert len(order_payments) == 2
        assert all(payment.order_id == order_id for payment in order_payments)
        payment_amounts = [payment.amount for payment in order_payments]
        assert 25.00 in payment_amounts
        assert 30.00 in payment_amounts
    
    async def test_list_all_payments(self, payment_db_session: AsyncSession):
        """Test listing all payments."""
        # Arrange
        payment_repo = SQLAlchemyPaymentRepository(payment_db_session)
        
        # Create payments for different users and orders
        payments = [
            Payment(
                user_id=uuid4(),
                order_id=uuid4(),
                amount=100.00 + i * 10,
                currency="USD",
                payment_method=PaymentMethod.CREDIT_CARD,
                status=PaymentStatus.PENDING,
                gateway_transaction_id=f"txn_list_{i}"
            )
            for i in range(3)
        ]
        
        for payment in payments:
            await payment_repo.create(payment)
        
        # Act
        all_payments = await payment_repo.list_all()
        
        # Assert
        assert len(all_payments) >= 3
        payment_amounts = [payment.amount for payment in all_payments]
        assert 100.00 in payment_amounts
        assert 110.00 in payment_amounts
        assert 120.00 in payment_amounts
    
    async def test_update_payment(self, payment_db_session: AsyncSession):
        """Test updating a payment."""
        # Arrange
        payment_repo = SQLAlchemyPaymentRepository(payment_db_session)
        user_id = uuid4()
        order_id = uuid4()
        payment = Payment(
            user_id=user_id,
            order_id=order_id,
            amount=75.00,
            currency="USD",
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.PENDING,
            gateway_transaction_id="txn_update_789"
        )
        created_payment = await payment_repo.create(payment)
        
        # Act
        created_payment.status = PaymentStatus.COMPLETED
        created_payment.amount = 80.00
        updated_payment = await payment_repo.update(created_payment)
        
        # Assert
        assert updated_payment.status == PaymentStatus.COMPLETED
        assert updated_payment.amount == 80.00
        assert updated_payment.updated_at > created_payment.created_at
    
    async def test_delete_payment(self, payment_db_session: AsyncSession):
        """Test deleting a payment."""
        # Arrange
        payment_repo = SQLAlchemyPaymentRepository(payment_db_session)
        user_id = uuid4()
        order_id = uuid4()
        payment = Payment(
            user_id=user_id,
            order_id=order_id,
            amount=200.00,
            currency="USD",
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.PENDING,
            gateway_transaction_id="txn_delete_999"
        )
        created_payment = await payment_repo.create(payment)
        
        # Act
        await payment_repo.delete(created_payment.id)
        
        # Assert
        deleted_payment = await payment_repo.get_by_id(created_payment.id)
        assert deleted_payment is None
    
    async def test_payment_status_enum(self, payment_db_session: AsyncSession):
        """Test payment status enum values."""
        # Arrange
        payment_repo = SQLAlchemyPaymentRepository(payment_db_session)
        
        # Test PENDING status
        pending_payment = Payment(
            user_id=uuid4(),
            order_id=uuid4(),
            amount=50.00,
            currency="USD",
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.PENDING,
            gateway_transaction_id="txn_pending"
        )
        created_pending = await payment_repo.create(pending_payment)
        assert created_pending.status == PaymentStatus.PENDING
        
        # Test COMPLETED status
        completed_payment = Payment(
            user_id=uuid4(),
            order_id=uuid4(),
            amount=60.00,
            currency="USD",
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.COMPLETED,
            gateway_transaction_id="txn_completed"
        )
        created_completed = await payment_repo.create(completed_payment)
        assert created_completed.status == PaymentStatus.COMPLETED
        
        # Test FAILED status
        failed_payment = Payment(
            user_id=uuid4(),
            order_id=uuid4(),
            amount=70.00,
            currency="USD",
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.FAILED,
            gateway_transaction_id="txn_failed"
        )
        created_failed = await payment_repo.create(failed_payment)
        assert created_failed.status == PaymentStatus.FAILED
        
        # Test REFUNDED status
        refunded_payment = Payment(
            user_id=uuid4(),
            order_id=uuid4(),
            amount=80.00,
            currency="USD",
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.REFUNDED,
            gateway_transaction_id="txn_refunded"
        )
        created_refunded = await payment_repo.create(refunded_payment)
        assert created_refunded.status == PaymentStatus.REFUNDED
    
    async def test_payment_method_enum(self, payment_db_session: AsyncSession):
        """Test payment method enum values."""
        # Arrange
        payment_repo = SQLAlchemyPaymentRepository(payment_db_session)
        
        # Test CREDIT_CARD method
        cc_payment = Payment(
            user_id=uuid4(),
            order_id=uuid4(),
            amount=50.00,
            currency="USD",
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.PENDING,
            gateway_transaction_id="txn_cc"
        )
        created_cc = await payment_repo.create(cc_payment)
        assert created_cc.payment_method == PaymentMethod.CREDIT_CARD
        
        # Test DEBIT_CARD method
        dc_payment = Payment(
            user_id=uuid4(),
            order_id=uuid4(),
            amount=60.00,
            currency="USD",
            payment_method=PaymentMethod.DEBIT_CARD,
            status=PaymentStatus.PENDING,
            gateway_transaction_id="txn_dc"
        )
        created_dc = await payment_repo.create(dc_payment)
        assert created_dc.payment_method == PaymentMethod.DEBIT_CARD
        
        # Test PAYPAL method
        pp_payment = Payment(
            user_id=uuid4(),
            order_id=uuid4(),
            amount=70.00,
            currency="USD",
            payment_method=PaymentMethod.PAYPAL,
            status=PaymentStatus.PENDING,
            gateway_transaction_id="txn_pp"
        )
        created_pp = await payment_repo.create(pp_payment)
        assert created_pp.payment_method == PaymentMethod.PAYPAL
        
        # Test BANK_TRANSFER method
        bt_payment = Payment(
            user_id=uuid4(),
            order_id=uuid4(),
            amount=80.00,
            currency="USD",
            payment_method=PaymentMethod.BANK_TRANSFER,
            status=PaymentStatus.PENDING,
            gateway_transaction_id="txn_bt"
        )
        created_bt = await payment_repo.create(bt_payment)
        assert created_bt.payment_method == PaymentMethod.BANK_TRANSFER
    
    async def test_payment_currency_handling(self, payment_db_session: AsyncSession):
        """Test payment currency handling."""
        # Arrange
        payment_repo = SQLAlchemyPaymentRepository(payment_db_session)
        
        # Test different currencies
        currencies = ["USD", "EUR", "GBP", "CAD"]
        for currency in currencies:
            payment = Payment(
                user_id=uuid4(),
                order_id=uuid4(),
                amount=100.00,
                currency=currency,
                payment_method=PaymentMethod.CREDIT_CARD,
                status=PaymentStatus.PENDING,
                gateway_transaction_id=f"txn_{currency.lower()}"
            )
            created_payment = await payment_repo.create(payment)
            assert created_payment.currency == currency
    
    async def test_payment_amount_precision(self, payment_db_session: AsyncSession):
        """Test payment amount precision handling."""
        # Arrange
        payment_repo = SQLAlchemyPaymentRepository(payment_db_session)
        user_id = uuid4()
        order_id = uuid4()
        payment = Payment(
            user_id=user_id,
            order_id=order_id,
            amount=123.456,  # 3 decimal places
            currency="USD",
            payment_method=PaymentMethod.CREDIT_CARD,
            status=PaymentStatus.PENDING,
            gateway_transaction_id="txn_precision"
        )
        
        # Act
        created_payment = await payment_repo.create(payment)
        
        # Assert
        # Should handle precision correctly (typically rounded to 2 decimal places)
        assert abs(created_payment.amount - 123.456) < 0.01
    
    async def test_get_nonexistent_payment(self, payment_db_session: AsyncSession):
        """Test retrieving a non-existent payment returns None."""
        # Arrange
        payment_repo = SQLAlchemyPaymentRepository(payment_db_session)
        nonexistent_id = uuid4()
        
        # Act
        retrieved_payment = await payment_repo.get_by_id(nonexistent_id)
        
        # Assert
        assert retrieved_payment is None
