"""Cart controller."""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from ....application.dtos.cart_dto import CartDTO, CartCreateDTO, CartUpdateDTO
from ....application.dtos.cart_item_dto import CartItemDTO, CartItemCreateDTO
from ....application.use_cases import (
    CreateCartUseCase,
    GetCartUseCase,
    UpdateCartUseCase,
    DeleteCartUseCase,
    AddItemToCartUseCase,
    GetCartItemsUseCase,
)
from ....container import SimpleContainer, get_container

router = APIRouter(prefix="/carts", tags=["carts"])


@router.post("/", response_model=CartDTO, status_code=status.HTTP_201_CREATED)
async def create_cart(
    cart_data: CartCreateDTO,
    container: SimpleContainer = Depends(get_container),
):
    """Create a new cart."""
    try:
        use_case = CreateCartUseCase(container.cart_repository)
        cart = await use_case.execute(
            user_id=cart_data.user_id,
            status=cart_data.status,
        )
        return CartDTO(**cart.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{cart_id}", response_model=CartDTO)
async def get_cart(
    cart_id: UUID,
    container: SimpleContainer = Depends(get_container),
):
    """Get cart by ID."""
    use_case = GetCartUseCase(container.cart_repository)
    cart = await use_case.execute(cart_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    return CartDTO(**cart.to_dict())


@router.get("/user/{user_id}", response_model=CartDTO)
async def get_cart_by_user(
    user_id: UUID,
    container: SimpleContainer = Depends(get_container),
):
    """Get active cart by user ID."""
    use_case = GetCartUseCase(container.cart_repository)
    cart = await use_case.execute_by_user_id(user_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    return CartDTO(**cart.to_dict())


@router.put("/{cart_id}", response_model=CartDTO)
async def update_cart(
    cart_id: UUID,
    cart_data: CartUpdateDTO,
    container: SimpleContainer = Depends(get_container),
):
    """Update cart."""
    use_case = GetCartUseCase(container.cart_repository)
    cart = await use_case.execute(cart_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    
    if cart_data.status is not None:
        cart.status = cart_data.status
    
    update_use_case = UpdateCartUseCase(container.cart_repository)
    updated_cart = await update_use_case.execute(cart)
    return CartDTO(**updated_cart.to_dict())


@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(
    cart_id: UUID,
    container: SimpleContainer = Depends(get_container),
):
    """Delete cart."""
    use_case = DeleteCartUseCase(container.cart_repository)
    success = await use_case.execute(cart_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")


@router.post("/{cart_id}/items", response_model=CartItemDTO, status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(
    cart_id: UUID,
    item_data: CartItemCreateDTO,
    container: SimpleContainer = Depends(get_container),
):
    """Add item to cart."""
    try:
        use_case = AddItemToCartUseCase(
            container.cart_repository,
            container.cart_item_repository,
        )
        cart_item = await use_case.execute(
            cart_id=cart_id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
        )
        return CartItemDTO(**cart_item.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{cart_id}/items", response_model=List[CartItemDTO])
async def get_cart_items(
    cart_id: UUID,
    container: SimpleContainer = Depends(get_container),
):
    """Get cart items."""
    use_case = GetCartItemsUseCase(container.cart_item_repository)
    cart_items = await use_case.execute(cart_id)
    return [CartItemDTO(**item.to_dict()) for item in cart_items]
