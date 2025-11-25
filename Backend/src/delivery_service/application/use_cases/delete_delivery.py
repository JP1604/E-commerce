"""Delete delivery use case."""

from uuid import UUID
from delivery_service.domain.repositories.delivery_repository import DeliveryRepository


class DeleteDeliveryUseCase:
    def __init__(self, repository: DeliveryRepository) -> None:
        self._repository = repository

    async def execute(self, delivery_id: UUID) -> bool:
        return await self._repository.delete(delivery_id)


