"""List deliveries use case."""

from datetime import date
from typing import Optional
from uuid import UUID

from delivery_service.domain.entities.delivery import DeliveryState
from delivery_service.domain.repositories.delivery_repository import DeliveryRepository


class ListDeliveriesUseCase:
    def __init__(self, repository: DeliveryRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        *,
        order_id: Optional[UUID] = None,
        state: Optional[DeliveryState] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 20,
        offset: int = 0,
    ):
        return await self._repository.find_filtered(
            order_id=order_id,
            state=state,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
        )


