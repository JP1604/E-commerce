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
    session: AsyncSession = Depends(get_db_session)
):
    """Create a new order."""
    try:
        # Validate items
        if not order_data.items or len(order_data.items) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Items are required. Please provide order items."
            )
        
        # Import models
        from order_service.infrastructure.database.models.order_models import OrderModel, OrderItemModel
        from order_service.domain.entities.order import OrderStatus
        from uuid import uuid4
        from datetime import datetime
        
        # Calculate total
        total = sum(item.quantity * item.unit_price for item in order_data.items)
        
        # Create order model directly
        order_id = uuid4()
        order_model = OrderModel(
            id_order=order_id,
            id_user=order_data.id_user,
            id_cart=order_data.id_cart,
            total=total,
            status=OrderStatus.CREATED,
            created_at=datetime.utcnow()
        )
        
        # Create order items
        items_response = []
        for item_data in order_data.items:
            item_id = uuid4()
            subtotal = item_data.quantity * item_data.unit_price
            
            item_model = OrderItemModel(
                id_order_item=item_id,
                id_order=order_id,
                id_product=item_data.id_product,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                subtotal=subtotal,
                created_at=datetime.utcnow()
            )
            order_model.items.append(item_model)
            
            # Build response item
            from order_service.application.dtos.order_dto import OrderItemResponseDTO
            items_response.append(OrderItemResponseDTO(
                id_order_item=item_id,
                id_order=order_id,
                id_product=item_data.id_product,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                subtotal=subtotal,
                created_at=datetime.utcnow()
            ))
        
        # Save to database
        session.add(order_model)
        await session.commit()
        
        # Return response
        return OrderResponseDTO(
            id_order=order_id,
            id_user=order_data.id_user,
            id_cart=order_data.id_cart,
            total=total,
            status=OrderStatus.CREATED,
            payment_id=None,
            created_at=datetime.utcnow(),
            updated_at=None,
            items=items_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
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
    
    return [
        OrderResponseDTO(
            id_order=order.id_order,
            id_user=order.id_user,
            id_cart=order.id_cart,
            total=order.total,
            status=order.status,
            payment_id=order.payment_id,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=[
                OrderItemResponseDTO(
                    id_order_item=item.id_order_item,
                    id_order=item.id_order,
                    id_product=item.id_product,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    subtotal=item.subtotal,
                    created_at=item.created_at
                )
                for item in order.items
            ]
        )
        for order in orders
    ]


@router.post("/{order_id}/pay", response_model=OrderResponseDTO)
async def pay_order(
    order_id: UUID,
    payment_method: str = "credit_card"
):
    """Process payment for an order."""
    from order_service.infrastructure.clients.payment_client import PaymentServiceClient
    from order_service.infrastructure.database.connection import AsyncSessionLocal
    
    try:
        # 1. Get order from DB
        async with AsyncSessionLocal() as session:
            repository = SQLAlchemyOrderRepository(session)
            order = await repository.get_by_id(order_id)
            
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            
            if order.payment_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Order already has a payment"
                )
        
        # 2. Create payment (HTTP call after DB session closed)
        payment_client = PaymentServiceClient()
        payment_response = await payment_client.create_payment(
            order_id=order.id_order,
            user_id=order.id_user,
            amount=order.total,
            payment_method=payment_method
        )
        
        # 3. Update order with payment_id
        async with AsyncSessionLocal() as session:
            repository = SQLAlchemyOrderRepository(session)
            order.payment_id = UUID(payment_response["id_payment"])
            updated_order = await repository.update(order)
            
            # Build response
            from order_service.application.dtos.order_dto import OrderItemResponseDTO
            items_dto = [
                OrderItemResponseDTO(
                    id_order_item=item.id_order_item,
                    id_order=item.id_order,
                    id_product=item.id_product,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    subtotal=item.subtotal,
                    created_at=item.created_at
                )
                for item in updated_order.items
            ]
            
            return OrderResponseDTO(
                id_order=updated_order.id_order,
                id_user=updated_order.id_user,
                id_cart=updated_order.id_cart,
                total=updated_order.total,
                status=updated_order.status,
                payment_id=updated_order.payment_id,
                created_at=updated_order.created_at,
                updated_at=updated_order.updated_at,
                items=items_dto
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing payment: {str(e)}"
        )
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
