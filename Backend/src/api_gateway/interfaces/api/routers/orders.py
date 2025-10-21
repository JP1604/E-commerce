"""Gateway order proxy routes."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
import httpx

from api_gateway.infrastructure.config.settings import get_settings
from api_gateway.infrastructure.http.client import get_http_client


router = APIRouter()


@router.get("/")
async def list_orders(skip: int = 0, limit: int = 100, client: httpx.AsyncClient = Depends(get_http_client)):
    settings = get_settings()
    url = f"{settings.order_service_url}/api/v1/orders/?skip={skip}&limit={limit}"
    try:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Order service error: {exc}")


@router.get("/{order_id}")
async def get_order(order_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
    settings = get_settings()
    url = f"{settings.order_service_url}/api/v1/orders/{order_id}"
    try:
        resp = await client.get(url)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Order not found")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Order service error: {exc}")


@router.post("/")
async def create_order(payload: dict, client: httpx.AsyncClient = Depends(get_http_client)):
    """Create an order via Order Service."""
    settings = get_settings()
    url = f"{settings.order_service_url}/api/v1/orders/"
    try:
        resp = await client.post(url, json=payload)
        if resp.status_code >= 400:
            # Forward downstream error body/status for easier debugging
            content = None
            try:
                content = resp.json()
            except Exception:
                content = {"detail": resp.text}
            return JSONResponse(status_code=resp.status_code, content=content)
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Order creation error: {exc}")


@router.patch("/{order_id}/status")
async def update_order_status(order_id: str, payload: dict, client: httpx.AsyncClient = Depends(get_http_client)):
    """Update order status (creada, pagada, enviada, entregada, cancelada)."""
    settings = get_settings()
    url = f"{settings.order_service_url}/api/v1/orders/{order_id}"
    try:
        resp = await client.patch(url, json=payload)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Order not found")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Order update error: {exc}")


# Convenience aliases to accept no-trailing-slash paths as well
@router.get("")
async def list_orders_no_slash(skip: int = 0, limit: int = 100, client: httpx.AsyncClient = Depends(get_http_client)):
    return await list_orders(skip, limit, client)


@router.post("")
async def create_order_no_slash(payload: dict, client: httpx.AsyncClient = Depends(get_http_client)):
    return await create_order(payload, client)


