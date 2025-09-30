"""Delivery API controller."""

from typing import List
from uuid import UUID
from fastapi import Depends, HTTPException, status

from delivery_service.application.dtos.delivery_dto import (
    DeliveryCreateDTO,
    DeliveryUpdateDTO,
    DeliveryResponseDTO,
)
from delivery_service.application.use_cases.create_delivery import CreateDeliveryUseCase
from delivery_service.application.use_cases.get_delivery import GetDeliveryUseCase
from delivery_service.application.use_cases.list_deliveries import ListDeliveriesUseCase
from delivery_service.application.use_cases.update_delivery import UpdateDeliveryUseCase
from delivery_service.application.use_cases.delete_delivery import DeleteDeliveryUseCase
from delivery_service.application.use_cases.change_delivery_state import ChangeDeliveryStateUseCase
from delivery_service.domain.entities.delivery import DeliveryState
from delivery_service.container import SimpleContainer, get_container


class DeliveryController:
    @staticmethod
    async def create_delivery(
        data: DeliveryCreateDTO, container: SimpleContainer = Depends(get_container)
    ) -> DeliveryResponseDTO:
        try:
            use_case = CreateDeliveryUseCase(container.delivery_repository)
            delivery = await use_case.execute(data)
            return DeliveryResponseDTO.from_entity(delivery)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @staticmethod
    async def get_delivery(
        delivery_id: UUID, container: SimpleContainer = Depends(get_container)
    ) -> DeliveryResponseDTO:
        use_case = GetDeliveryUseCase(container.delivery_repository)
        delivery = await use_case.by_id(delivery_id)
        if not delivery:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found")
        return DeliveryResponseDTO.from_entity(delivery)

    @staticmethod
    async def list_deliveries(container: SimpleContainer = Depends(get_container)) -> List[DeliveryResponseDTO]:
        use_case = ListDeliveriesUseCase(container.delivery_repository)
        deliveries = await use_case.execute()
        return [DeliveryResponseDTO.from_entity(d) for d in deliveries]

    @staticmethod
    async def update_delivery(
        delivery_id: UUID, data: DeliveryUpdateDTO, container: SimpleContainer = Depends(get_container)
    ) -> DeliveryResponseDTO:
        try:
            use_case = UpdateDeliveryUseCase(container.delivery_repository)
            delivery = await use_case.execute(delivery_id, data)
            return DeliveryResponseDTO.from_entity(delivery)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @staticmethod
    async def delete_delivery(
        delivery_id: UUID, container: SimpleContainer = Depends(get_container)
    ) -> dict:
        use_case = DeleteDeliveryUseCase(container.delivery_repository)
        deleted = await use_case.execute(delivery_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found")
        return {"message": "Delivery deleted successfully"}

    @staticmethod
    async def change_state(
        delivery_id: UUID,
        new_state: DeliveryState,
        container: SimpleContainer = Depends(get_container),
    ) -> DeliveryResponseDTO:
        try:
            use_case = ChangeDeliveryStateUseCase(container.delivery_repository)
            delivery = await use_case.execute(delivery_id, new_state)
            return DeliveryResponseDTO.from_entity(delivery)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


