"""Update delivery use case."""

from uuid import UUID
from delivery_service.application.dtos.delivery_dto import DeliveryUpdateDTO
from delivery_service.domain.repositories.delivery_repository import DeliveryRepository


class UpdateDeliveryUseCase:
    def __init__(self, repository: DeliveryRepository) -> None:
        self._repository = repository

    async def execute(self, delivery_id: UUID, data: DeliveryUpdateDTO):
        delivery = await self._repository.find_by_id(delivery_id)
        if not delivery:
            raise ValueError("Delivery not found")

        if data.delivery_booked_schedule is not None:
            delivery.delivery_booked_schedule = data.delivery_booked_schedule
        if data.booking_start is not None:
            delivery.booking_start = data.booking_start
        if data.booking_end is not None:
            delivery.booking_end = data.booking_end
        if data.state is not None:
            delivery.state = data.state

        # validate time range
        if delivery.booking_end <= delivery.booking_start:
            raise ValueError("booking_end must be after booking_start")

        return await self._repository.update(delivery)


