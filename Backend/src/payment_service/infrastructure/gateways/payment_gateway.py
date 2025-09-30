"""Payment gateway interface and mock implementation."""

from abc import ABC, abstractmethod
from typing import Dict, Any
import asyncio
import random
import uuid


class PaymentGateway(ABC):
    """Abstract payment gateway interface."""

    @abstractmethod
    async def process_card_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process card payment."""
        pass

    @abstractmethod
    async def process_paypal_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process PayPal payment."""
        pass

    @abstractmethod
    async def process_bank_transfer(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process bank transfer."""
        pass

    @abstractmethod
    async def process_refund(self, refund_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process refund."""
        pass


class MockPaymentGateway(PaymentGateway):
    """Mock payment gateway for testing and development."""

    async def process_card_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process card payment (mock)."""
        # Simulate processing delay
        await asyncio.sleep(1)
        
        # Mock validation
        card_number = payment_data.get("card_number", "")
        amount = payment_data.get("amount", 0)
        
        # Simulate different scenarios based on card number
        if card_number.endswith("0000"):
            # Declined card
            return {
                "success": False,
                "error_code": "CARD_DECLINED",
                "error_message": "Card was declined by the issuing bank"
            }
        elif card_number.endswith("1111"):
            # Insufficient funds
            return {
                "success": False,
                "error_code": "INSUFFICIENT_FUNDS",
                "error_message": "Insufficient funds on the card"
            }
        elif amount > 10000:
            # Amount too high
            return {
                "success": False,
                "error_code": "AMOUNT_TOO_HIGH",
                "error_message": "Transaction amount exceeds limit"
            }
        else:
            # Successful payment
            return {
                "success": True,
                "transaction_id": f"TXN_{uuid.uuid4().hex[:12].upper()}",
                "authorization_code": f"AUTH_{random.randint(100000, 999999)}",
                "gateway_response_code": "00",
                "message": "Payment processed successfully"
            }

    async def process_paypal_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process PayPal payment (mock)."""
        await asyncio.sleep(2)  # PayPal typically takes longer
        
        # Mock PayPal processing
        amount = payment_data.get("amount", 0)
        
        if amount > 5000:
            return {
                "success": False,
                "error_code": "PAYPAL_LIMIT_EXCEEDED",
                "error_message": "PayPal transaction limit exceeded"
            }
        else:
            return {
                "success": True,
                "transaction_id": f"PP_{uuid.uuid4().hex[:10].upper()}",
                "paypal_transaction_id": f"PAYID-{uuid.uuid4().hex[:16].upper()}",
                "message": "PayPal payment processed successfully"
            }

    async def process_bank_transfer(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process bank transfer (mock)."""
        await asyncio.sleep(3)  # Bank transfers take longer
        
        # Mock bank transfer - usually requires manual verification
        return {
            "success": True,
            "transaction_id": f"BT_{uuid.uuid4().hex[:10].upper()}",
            "status": "PENDING_VERIFICATION",
            "message": "Bank transfer initiated, pending verification"
        }

    async def process_refund(self, refund_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process refund (mock)."""
        await asyncio.sleep(1)
        
        original_transaction_id = refund_data.get("original_transaction_id")
        amount = refund_data.get("amount", 0)
        
        if not original_transaction_id:
            return {
                "success": False,
                "error_code": "INVALID_TRANSACTION",
                "error_message": "Original transaction ID is required for refund"
            }
        
        # Mock refund processing
        if random.random() > 0.1:  # 90% success rate
            return {
                "success": True,
                "refund_transaction_id": f"REF_{uuid.uuid4().hex[:10].upper()}",
                "refund_amount": amount,
                "message": "Refund processed successfully"
            }
        else:
            return {
                "success": False,
                "error_code": "REFUND_FAILED",
                "error_message": "Refund could not be processed at this time"
            }
