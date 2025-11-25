"""Cart Service HTTP client."""

import os
from typing import Dict, List, Optional
from uuid import UUID
import httpx


class CartServiceClient:
    """Client to communicate with Cart Service."""

    def __init__(self):
        self.base_url = os.getenv("CART_SERVICE_URL", "http://cart-service:8003")
        self.timeout = 10.0

    async def get_cart(self, cart_id: UUID) -> Optional[Dict]:
        """Get cart by ID."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/api/v1/carts/{cart_id}")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error fetching cart {cart_id}: {e}")
                return None

    async def get_cart_items(self, cart_id: UUID) -> List[Dict]:
        """Get all items in a cart."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/api/v1/carts/{cart_id}/items")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error fetching cart items for {cart_id}: {e}")
                raise ValueError(f"Could not fetch cart items: {str(e)}")

    async def clear_cart(self, cart_id: UUID) -> bool:
        """Clear all items from cart after order creation."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Get all items first
                items = await self.get_cart_items(cart_id)
                
                # Delete each item
                for item in items:
                    item_id = item.get("id_cart_item")
                    if item_id:
                        await client.delete(f"{self.base_url}/api/v1/carts/{cart_id}/items/{item_id}")
                
                return True
            except Exception as e:
                print(f"Error clearing cart {cart_id}: {e}")
                return False
