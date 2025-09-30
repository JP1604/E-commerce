"""Simple API router configuration."""

from fastapi import APIRouter, Depends
from src.product_service.interfaces.api.controllers.product_controller import ProductController
from src.product_service.application.dtos import ProductCreateDTO, ProductUpdateDTO
from uuid import UUID
from typing import List
from src.product_service.container import SimpleContainer, get_container

api_router = APIRouter(prefix="/api/v1")

# Include product routes
@api_router.post("/products/")
async def create_product(
    data: ProductCreateDTO,
    container: SimpleContainer = Depends(get_container),
):
    """Create a new product."""
    return await ProductController.create_product(data, container)

@api_router.get("/products/")
async def get_products(container: SimpleContainer = Depends(get_container)):
    """Get all products."""
    return await ProductController.get_products(container)

@api_router.get("/products/{product_id}")
async def get_product(
    product_id: UUID,
    container: SimpleContainer = Depends(get_container),
):
    """Get a product by ID."""
    return await ProductController.get_product(product_id, container)

@api_router.put("/products/{product_id}")
async def update_product(
    product_id: UUID,
    data: ProductUpdateDTO,
    container: SimpleContainer = Depends(get_container),
):
    """Update a product."""
    return await ProductController.update_product(product_id, data, container)

@api_router.delete("/products/{product_id}")
async def delete_product(
    product_id: UUID,
    container: SimpleContainer = Depends(get_container),
):
    """Delete a product."""
    return await ProductController.delete_product(product_id, container)

@api_router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Simple E-commerce API is running"}