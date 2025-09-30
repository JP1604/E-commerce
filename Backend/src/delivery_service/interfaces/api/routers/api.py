"""Delivery API routes."""

from fastapi import APIRouter, Depends, Query
from uuid import UUID
from datetime import date

from delivery_service.interfaces.api.controllers.delivery_controller import DeliveryController
from delivery_service.application.dtos.delivery_dto import DeliveryCreateDTO, DeliveryUpdateDTO, DeliveryResponseDTO
from delivery_service.container import SimpleContainer, get_container
from delivery_service.domain.entities.delivery import DeliveryState
from delivery_service.application.use_cases.list_deliveries import ListDeliveriesUseCase


api_router = APIRouter(prefix="/api/v1/deliveries")


@api_router.post(
    "/",
    summary="Create delivery",
    description=(
        "Create a delivery booking window for an order. "
        "Initial state is BOOKED. Returns the created delivery."
    ),
    response_model=DeliveryResponseDTO,
)
async def create_delivery(
    data: DeliveryCreateDTO,
    container: SimpleContainer = Depends(get_container),
):
    return await DeliveryController.create_delivery(data, container)


@api_router.get(
    "/",
    summary="List deliveries (filterable)",
    description=(
        "Returns deliveries with optional filters via query parameters.\n\n"
        "Use query params: order_id, state, date_from, date_to, limit, offset.\n"
        "Filters are optional and combined (AND). Date range is inclusive."
    ),
    response_model=list[DeliveryResponseDTO],
)
async def list_deliveries(
    container: SimpleContainer = Depends(get_container),
    order_id: UUID | None = Query(None, description="Filter by order id"),
    state: DeliveryState | None = Query(None, description="Filter by delivery state"),
    date_from: date | None = Query(None, description="Filter start date (YYYY-MM-DD), inclusive"),
    date_to: date | None = Query(None, description="Filter end date (YYYY-MM-DD), inclusive"),
    limit: int = Query(20, ge=1, le=100, description="Max items to return"),
    offset: int = Query(0, ge=0, description="Items to skip for pagination"),
):
    use_case = ListDeliveriesUseCase(container.delivery_repository)
    deliveries = await use_case.execute(
        order_id=order_id,
        state=state,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )
    return [DeliveryResponseDTO.from_entity(d) for d in deliveries]


@api_router.get(
    "/{delivery_id}",
    summary="Get delivery by id",
    description="Fetch a single delivery by its identifier.",
    response_model=DeliveryResponseDTO,
)
async def get_delivery(
    delivery_id: UUID,
    container: SimpleContainer = Depends(get_container),
):
    return await DeliveryController.get_delivery(delivery_id, container)


@api_router.put(
    "/{delivery_id}",
    summary="Update delivery",
    description=(
        "Update delivery details (date, booking window, state). "
        "Enforces booking_end > booking_start. Returns the updated delivery."
    ),
    response_model=DeliveryResponseDTO,
)
async def update_delivery(
    delivery_id: UUID,
    data: DeliveryUpdateDTO,
    container: SimpleContainer = Depends(get_container),
):
    return await DeliveryController.update_delivery(delivery_id, data, container)


@api_router.delete(
    "/{delivery_id}",
    summary="Delete delivery",
    description="Delete a delivery by id. Returns a confirmation message.",
)
async def delete_delivery(
    delivery_id: UUID,
    container: SimpleContainer = Depends(get_container),
):
    return await DeliveryController.delete_delivery(delivery_id, container)


@api_router.post(
    "/{delivery_id}/state",
    summary="Change delivery state",
    description=(
        "Change the state of a delivery. Not allowed: CONFIRMED→BOOKED, CANCELLED→BOOKED."
    ),
)
async def change_state(
    delivery_id: UUID,
    new_state: DeliveryState,
    container: SimpleContainer = Depends(get_container),
):
    return await DeliveryController.change_state(delivery_id, new_state, container)


