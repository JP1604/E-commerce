"""Change delivery state use case with transition guards."""

from uuid import UUID
from delivery_service.domain.entities.delivery import DeliveryState
from delivery_service.domain.repositories.delivery_repository import DeliveryRepository


class ChangeDeliveryStateUseCase:
    def __init__(self, repository: DeliveryRepository) -> None:
        self._repository = repository

    async def execute(self, delivery_id: UUID, new_state: DeliveryState):
        delivery = await self._repository.find_by_id(delivery_id)
        if not delivery:
            raise ValueError("Delivery not found")

        current = delivery.state
        # Prevent CONFIRMED -> BOOKED and CANCELLED -> BOOKED
        if current == DeliveryState.CONFIRMED and new_state == DeliveryState.BOOKED:
            raise ValueError("Cannot transition from CONFIRMED to BOOKED")
        if current == DeliveryState.CANCELLED and new_state == DeliveryState.BOOKED:
            raise ValueError("Cannot transition from CANCELLED to BOOKED")

        delivery.state = new_state
        return await self._repository.update(delivery)


