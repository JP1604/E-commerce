"""Create order use case."""

from uuid import UUID
from typing import List

from order_service.domain.entities.order import Order, OrderItem
from order_service.domain.repositories.order_repository import OrderRepository
from order_service.application.dtos.order_dto import OrderCreateDTO, OrderResponseDTO, OrderItemResponseDTO


class CreateOrderUseCase:
    """Use case for creating orders."""

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def execute(self, order_data: OrderCreateDTO) -> OrderResponseDTO:
        """Execute create order use case."""
        # Create new order
        order = Order(id_user=order_data.id_user, total=0.0)
        
        # Add items to order
        for item_data in order_data.items:
            order.add_item(
                id_product=item_data.id_product,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price
            )
        
        # Save order
        created_order = await self.order_repository.create(order)
        
        # Convert to response DTO
        return self._to_response_dto(created_order)

    def _to_response_dto(self, order: Order) -> OrderResponseDTO:
        """Convert order entity to response DTO."""
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
            for item in order.items
        ]
        
        return OrderResponseDTO(
            id_order=order.id_order,
            id_user=order.id_user,
            total=order.total,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=items_dto
        )
