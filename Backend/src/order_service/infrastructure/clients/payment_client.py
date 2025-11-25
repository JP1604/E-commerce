"""Payment Service HTTP client."""

import os
from typing import Dict, Optional
from uuid import UUID
import httpx


class PaymentServiceClient:
    """Client to communicate with Payment Service."""

    def __init__(self):
        self.base_url = os.getenv("PAYMENT_SERVICE_URL", "http://payment-service:8007")
        self.timeout = 15.0

    async def create_payment(
        self,
        order_id: UUID,
        user_id: UUID,
        amount: float,
        payment_method: str = "credit_card"
    ) -> Optional[Dict]:
        """Create a payment for an order."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                payload = {
                    "id_order": str(order_id),
                    "id_user": str(user_id),
                    "amount": amount,
                    "method": payment_method,
                    "currency": "USD"
                }
                
                response = await client.post(
                    f"{self.base_url}/api/v1/payments",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error creating payment for order {order_id}: {e}")
                raise ValueError(f"Payment creation failed: {str(e)}")

    async def get_payment(self, payment_id: UUID) -> Optional[Dict]:
        """Get payment by ID."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/api/v1/payments/{payment_id}")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error fetching payment {payment_id}: {e}")
                return None
