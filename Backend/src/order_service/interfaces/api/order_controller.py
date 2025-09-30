"""Order API controller."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from order_service.application.dtos.order_dto import (
    OrderCreateDTO,
    OrderResponseDTO,
    OrderUpdateDTO
)
from order_service.application.use_cases.create_order import CreateOrderUseCase
from order_service.application.use_cases.get_order import GetOrderUseCase
from order_service.application.use_cases.get_user_orders import GetUserOrdersUseCase
from order_service.application.use_cases.update_order import UpdateOrderUseCase
from order_service.infrastructure.database.connection import get_db_session
from order_service.infrastructure.repositories.sqlalchemy_order_repository import SQLAlchemyOrderRepository

router = APIRouter()


def get_order_repository(session: AsyncSession = Depends(get_db_session)) -> SQLAlchemyOrderRepository:
    """Get order repository dependency."""
    return SQLAlchemyOrderRepository(session)


@router.post("/", response_model=OrderResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreateDTO,
    repository: SQLAlchemyOrderRepository = Depends(get_order_repository)
):
    """Create a new order."""
    try:
        use_case = CreateOrderUseCase(repository)
        return await use_case.execute(order_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating order: {str(e)}"
        )


@router.get("/{order_id}", response_model=OrderResponseDTO)
async def get_order(
    order_id: UUID,
    repository: SQLAlchemyOrderRepository = Depends(get_order_repository)
):
    """Get order by ID."""
    use_case = GetOrderUseCase(repository)
    order = await use_case.execute(order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order


@router.get("/user/{user_id}", response_model=List[OrderResponseDTO])
async def get_user_orders(
    user_id: UUID,
    repository: SQLAlchemyOrderRepository = Depends(get_order_repository)
):
    """Get orders by user ID."""
    use_case = GetUserOrdersUseCase(repository)
    return await use_case.execute(user_id)


@router.patch("/{order_id}", response_model=OrderResponseDTO)
async def update_order(
    order_id: UUID,
    update_data: OrderUpdateDTO,
    repository: SQLAlchemyOrderRepository = Depends(get_order_repository)
):
    """Update order."""
    use_case = UpdateOrderUseCase(repository)
    order = await use_case.execute(order_id, update_data)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order


@router.get("/", response_model=List[OrderResponseDTO])
async def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    repository: SQLAlchemyOrderRepository = Depends(get_order_repository)
):
    """Get all orders with pagination."""
    orders = await repository.get_all(skip=skip, limit=limit)
    
    # Convert to response DTOs
    return [
        OrderResponseDTO(
            id_order=order.id_order,
            id_user=order.id_user,
            total=order.total,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=[
                {
                    "id_order_item": item.id_order_item,
                    "id_order": item.id_order,
                    "id_product": item.id_product,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "subtotal": item.subtotal,
                    "created_at": item.created_at
                }
                for item in order.items
            ]
        )
        for order in orders
    ]
