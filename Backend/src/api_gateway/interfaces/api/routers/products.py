"""Gateway product proxy routes."""

from fastapi import APIRouter, Depends, HTTPException
import httpx

from api_gateway.infrastructure.config.settings import get_settings
from api_gateway.infrastructure.http.client import get_http_client


router = APIRouter()


@router.get("/")
async def list_products(client: httpx.AsyncClient = Depends(get_http_client)):
    settings = get_settings()
    url = f"{settings.product_service_url}/api/v1/products/"
    try:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Product service error: {exc}")


@router.get("/{product_id}")
async def get_product(product_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
    settings = get_settings()
    url = f"{settings.product_service_url}/api/v1/products/{product_id}"
    try:
        resp = await client.get(url)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Product not found")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Product service error: {exc}")


