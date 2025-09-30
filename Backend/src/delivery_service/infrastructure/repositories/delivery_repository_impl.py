"""SQLAlchemy implementation for DeliveryRepository."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

from delivery_service.domain.entities.delivery import Delivery, DeliveryState
from delivery_service.domain.repositories.delivery_repository import DeliveryRepository
from delivery_service.infrastructure.database.models import DeliveryModel


class SQLAlchemyDeliveryRepository(DeliveryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, delivery: Delivery) -> Delivery:
        model = DeliveryModel(
            id=delivery.id,
            order_id=delivery.order_id,
            delivery_booked_schedule=delivery.delivery_booked_schedule,
            booking_start=delivery.booking_start,
            booking_end=delivery.booking_end,
            state=delivery.state,
        )
        self._session.add(model)
        await self._session.flush()
        return self._model_to_entity(model)

    async def find_by_id(self, delivery_id: UUID) -> Optional[Delivery]:
        result = await self._session.execute(select(DeliveryModel).where(DeliveryModel.id == delivery_id))
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None

    async def find_all(self) -> List[Delivery]:
        result = await self._session.execute(select(DeliveryModel))
        models = result.scalars().all()
        return [self._model_to_entity(m) for m in models]

    async def find_filtered(
        self,
        *,
        order_id: Optional[UUID] = None,
        state: Optional[DeliveryState] = None,
        date_from: Optional["date"] = None,
        date_to: Optional["date"] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Delivery]:
        conditions = []
        if order_id is not None:
            conditions.append(DeliveryModel.order_id == order_id)
        if state is not None:
            conditions.append(DeliveryModel.state == state)
        if date_from is not None:
            conditions.append(DeliveryModel.delivery_booked_schedule >= date_from)
        if date_to is not None:
            conditions.append(DeliveryModel.delivery_booked_schedule <= date_to)

        query = select(DeliveryModel)
        if conditions:
            query = query.where(and_(*conditions))
        query = query.offset(offset).limit(limit)

        result = await self._session.execute(query)
        models = result.scalars().all()
        return [self._model_to_entity(m) for m in models]

    async def update(self, delivery: Delivery) -> Delivery:
        result = await self._session.execute(select(DeliveryModel).where(DeliveryModel.id == delivery.id))
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Delivery with id {delivery.id} not found")
        model.order_id = delivery.order_id
        model.delivery_booked_schedule = delivery.delivery_booked_schedule
        model.booking_start = delivery.booking_start
        model.booking_end = delivery.booking_end
        model.state = delivery.state
        await self._session.flush()
        return self._model_to_entity(model)

    async def delete(self, delivery_id: UUID) -> bool:
        result = await self._session.execute(select(DeliveryModel).where(DeliveryModel.id == delivery_id))
        model = result.scalar_one_or_none()
        if not model:
            return False
        await self._session.delete(model)
        await self._session.flush()
        return True

    def _model_to_entity(self, model: DeliveryModel) -> Delivery:
        return Delivery(
            id=model.id,
            order_id=model.order_id,
            delivery_booked_schedule=model.delivery_booked_schedule,
            booking_start=model.booking_start,
            booking_end=model.booking_end,
            state=model.state,
        )


