"""Delivery Service HTTP client."""

import os
from typing import Dict, Optional
from uuid import UUID
from datetime import date, time
import httpx


class DeliveryServiceClient:
    """Client to communicate with Delivery Service."""

    def __init__(self):
        self.base_url = os.getenv("DELIVERY_SERVICE_URL", "http://delivery-service:8002")
        self.timeout = 10.0

    async def create_delivery(
        self,
        order_id: UUID,
        delivery_booked_schedule: date,
        booking_start: time,
        booking_end: time
    ) -> Optional[Dict]:
        """Create a new delivery booking for an order."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                payload = {
                    "order_id": str(order_id),
                    "delivery_booked_schedule": delivery_booked_schedule.isoformat(),
                    "booking_start": booking_start.isoformat(),
                    "booking_end": booking_end.isoformat()
                }
                response = await client.post(
                    f"{self.base_url}/api/v1/deliveries/",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error creating delivery for order {order_id}: {e}")
                return None

    async def get_delivery_by_order(self, order_id: UUID) -> Optional[Dict]:
        """Get delivery by order ID."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/api/v1/deliveries/order/{order_id}")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error fetching delivery for order {order_id}: {e}")
                return None
