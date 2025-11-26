"""Simple Product DTOs."""

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
import base64


class ProductCreateDTO(BaseModel):
    """DTO for creating a new product."""
    name: str
    description: str
    price: float
    category: str
    stock_quantity: int = 0
    image: Optional[str] = None  # Base64 encoded image


class ProductUpdateDTO(BaseModel):
    """DTO for updating an existing product."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock_quantity: Optional[int] = None
    image: Optional[str] = None  # Base64 encoded image


class ProductResponseDTO(BaseModel):
    """DTO for product response."""
    id: UUID
    name: str
    description: str
    price: float
    category: str
    stock_quantity: int
    image_url: Optional[str] = None  # Base64 encoded image data URL
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_entity(cls, product):
        """Create DTO from domain entity."""
        # Convert binary image to base64 data URL
        image_url = None
        if product.image_bin:
            # Encode to base64 and create data URL
            image_b64 = base64.b64encode(product.image_bin).decode('utf-8')
            # Assuming JPEG format, adjust if needed
            image_url = f"data:image/jpeg;base64,{image_b64}"
        
        return cls(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            stock_quantity=product.stock_quantity,
            image_url=image_url,
            created_at=product.created_at,
            updated_at=product.updated_at
        )