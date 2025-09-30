"""Get delivery use case."""

from uuid import UUID
from delivery_service.domain.repositories.delivery_repository import DeliveryRepository


class GetDeliveryUseCase:
    def __init__(self, repository: DeliveryRepository) -> None:
        self._repository = repository

    async def by_id(self, delivery_id: UUID):
        return await self._repository.find_by_id(delivery_id)


