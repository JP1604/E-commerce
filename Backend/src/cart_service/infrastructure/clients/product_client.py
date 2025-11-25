"""Product Service HTTP client."""

import httpx
from typing import Optional, Dict, Any
from uuid import UUID
import os


class ProductServiceClient:
    """Client to communicate with Product Service."""
    
    def __init__(self):
        self.base_url = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8000")
        self.timeout = 10.0
    
    async def get_product(self, product_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get product information from Product Service.
        
        Args:
            product_id: UUID of the product
            
        Returns:
            Product data dict or None if not found
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/products/{product_id}"
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return None
                else:
                    # Log error or handle other status codes
                    return None
                    
        except (httpx.RequestError, httpx.TimeoutException) as e:
            # Log the error
            print(f"Error fetching product {product_id}: {str(e)}")
            return None
    
    async def check_product_availability(self, product_id: UUID, quantity: int) -> bool:
        """
        Check if product has enough stock.
        
        Args:
            product_id: UUID of the product
            quantity: Requested quantity
            
        Returns:
            True if product exists and has enough stock, False otherwise
        """
        product = await self.get_product(product_id)
        
        if not product:
            return False
        
        # Check if product has enough stock
        stock_quantity = product.get("stock_quantity", 0)
        return stock_quantity >= quantity
