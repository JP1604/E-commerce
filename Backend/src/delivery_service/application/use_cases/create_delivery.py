"""Create delivery use case."""

from delivery_service.application.dtos.delivery_dto import DeliveryCreateDTO
from delivery_service.domain.entities.delivery import Delivery
from delivery_service.domain.repositories.delivery_repository import DeliveryRepository


class CreateDeliveryUseCase:
    def __init__(self, repository: DeliveryRepository) -> None:
        self._repository = repository

    async def execute(self, data: DeliveryCreateDTO) -> Delivery:
        delivery = Delivery(
            order_id=data.order_id,
            delivery_booked_schedule=data.delivery_booked_schedule,
            booking_start=data.booking_start,
            booking_end=data.booking_end,
        )
        return await self._repository.save(delivery)


