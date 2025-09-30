"""Product controller."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query

from ....application.dtos.product_dto import ProductDTO, ProductCreateDTO, ProductUpdateDTO
from ....application.use_cases import (
    CreateProductUseCase,
    GetProductUseCase,
    ListProductsUseCase,
    UpdateProductUseCase,
    DeleteProductUseCase,
)
from ....container import SimpleContainer, get_container
from ....domain.entities.product import ProductStatus

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductDTO, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreateDTO,
    container: SimpleContainer = Depends(get_container),
):
    """Create a new product."""
    try:
        use_case = CreateProductUseCase(container.product_repository)
        product = await use_case.execute(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            status=product_data.status,
        )
        return ProductDTO(**product.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{product_id}", response_model=ProductDTO)
async def get_product(
    product_id: UUID,
    container: SimpleContainer = Depends(get_container),
):
    """Get product by ID."""
    use_case = GetProductUseCase(container.product_repository)
    product = await use_case.execute(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ProductDTO(**product.to_dict())


@router.get("/", response_model=List[ProductDTO])
async def list_products(
    status: Optional[ProductStatus] = Query(None, description="Filter by product status"),
    container: SimpleContainer = Depends(get_container),
):
    """List products."""
    use_case = ListProductsUseCase(container.product_repository)
    products = await use_case.execute(status)
    return [ProductDTO(**product.to_dict()) for product in products]


@router.put("/{product_id}", response_model=ProductDTO)
async def update_product(
    product_id: UUID,
    product_data: ProductUpdateDTO,
    container: SimpleContainer = Depends(get_container),
):
    """Update product."""
    use_case = GetProductUseCase(container.product_repository)
    product = await use_case.execute(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    if product_data.name is not None:
        product.name = product_data.name
    if product_data.description is not None:
        product.description = product_data.description
    if product_data.price is not None:
        product.price = product_data.price
    if product_data.status is not None:
        product.status = product_data.status
    
    update_use_case = UpdateProductUseCase(container.product_repository)
    updated_product = await update_use_case.execute(product)
    return ProductDTO(**updated_product.to_dict())


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    container: SimpleContainer = Depends(get_container),
):
    """Delete product."""
    use_case = DeleteProductUseCase(container.product_repository)
    success = await use_case.execute(product_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
