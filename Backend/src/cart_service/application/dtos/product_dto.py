"""Product DTOs."""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, validator
from datetime import datetime

from ...domain.entities.product import ProductStatus


class ProductDTO(BaseModel):
    """Product data transfer object."""
    
    id_product: UUID
    name: str
    description: str
    price: float
    status: ProductStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductCreateDTO(BaseModel):
    """Product creation data transfer object."""
    
    name: str = Field(..., min_length=1, description="Product name")
    description: str = Field(..., min_length=1, description="Product description")
    price: float = Field(..., ge=0, description="Price must be non-negative")
    status: ProductStatus = Field(default=ProductStatus.ACTIVE, description="Product status")

    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Product name is required')
        return v.strip()

    @validator('description')
    def validate_description(cls, v):
        if not v or not v.strip():
            raise ValueError('Product description is required')
        return v.strip()

    @validator('price')
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price must be non-negative')
        return v


class ProductUpdateDTO(BaseModel):
    """Product update data transfer object."""
    
    name: Optional[str] = Field(None, min_length=1, description="Product name")
    description: Optional[str] = Field(None, min_length=1, description="Product description")
    price: Optional[float] = Field(None, ge=0, description="Price must be non-negative")
    status: Optional[ProductStatus] = Field(None, description="Product status")

    @validator('name')
    def validate_name(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Product name cannot be empty')
        return v.strip() if v else v

    @validator('description')
    def validate_description(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Product description cannot be empty')
        return v.strip() if v else v

    @validator('price')
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError('Price must be non-negative')
        return v
