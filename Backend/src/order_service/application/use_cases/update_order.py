"""Update order use case."""

from uuid import UUID
from typing import Optional

from order_service.domain.repositories.order_repository import OrderRepository
from order_service.application.dtos.order_dto import OrderUpdateDTO, OrderResponseDTO, OrderItemResponseDTO


class UpdateOrderUseCase:
    """Use case for updating an order."""

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def execute(self, order_id: UUID, update_data: OrderUpdateDTO) -> Optional[OrderResponseDTO]:
        """Execute update order use case."""
        # Get existing order
        order = await self.order_repository.get_by_id(order_id)
        
        if not order:
            return None
        
        # Update fields if provided
        if update_data.status is not None:
            order.update_status(update_data.status)
        
        # Save updated order
        updated_order = await self.order_repository.update(order)
        
        # Convert to response DTO
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
            total=updated_order.total,
            status=updated_order.status,
            created_at=updated_order.created_at,
            updated_at=updated_order.updated_at,
            items=items_dto
        )
