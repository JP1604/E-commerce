"""Get user orders use case."""

from uuid import UUID
from typing import List

from order_service.domain.repositories.order_repository import OrderRepository
from order_service.application.dtos.order_dto import OrderResponseDTO, OrderItemResponseDTO


class GetUserOrdersUseCase:
    """Use case for getting orders by user ID."""

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def execute(self, user_id: UUID) -> List[OrderResponseDTO]:
        """Execute get user orders use case."""
        orders = await self.order_repository.get_by_user_id(user_id)
        
        # Convert to response DTOs
        return [self._to_response_dto(order) for order in orders]

    def _to_response_dto(self, order) -> OrderResponseDTO:
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
