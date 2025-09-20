"""Simple API router configuration."""

from fastapi import APIRouter
from ..controllers.product_controller import ProductController
from src.application.dtos import ProductCreateDTO, ProductUpdateDTO
from uuid import UUID
from typing import List

api_router = APIRouter(prefix="/api/v1")

# Include product routes
@api_router.post("/products/")
async def create_product(data: ProductCreateDTO):
    """Create a new product."""
    return await ProductController.create_product(data)

@api_router.get("/products/")
async def get_products():
    """Get all products."""
    return await ProductController.get_products()

@api_router.get("/products/{product_id}")
async def get_product(product_id: UUID):
    """Get a product by ID."""
    return await ProductController.get_product(product_id)

@api_router.put("/products/{product_id}")
async def update_product(product_id: UUID, data: ProductUpdateDTO):
    """Update a product."""
    return await ProductController.update_product(product_id, data)

@api_router.delete("/products/{product_id}")
async def delete_product(product_id: UUID):
    """Delete a product."""
    return await ProductController.delete_product(product_id)

@api_router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Simple E-commerce API is running"}