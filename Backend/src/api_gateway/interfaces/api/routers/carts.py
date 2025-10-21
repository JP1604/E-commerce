"""Gateway cart proxy routes."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
import httpx

from api_gateway.infrastructure.config.settings import get_settings
from api_gateway.infrastructure.http.client import get_http_client
from api_gateway.interfaces.api.schemas import CartCreate, AddItemRequest


router = APIRouter()


@router.post("/", status_code=201)
async def create_cart(payload: CartCreate, client: httpx.AsyncClient = Depends(get_http_client)):
    settings = get_settings()
    url = f"{settings.cart_service_url}/api/v1/carts/"
    try:
        resp = await client.post(url, json=payload.dict(by_alias=True, exclude_none=True))
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Cart service error: {exc}")


# Accept no-trailing-slash as well for POST
@router.post("", status_code=201)
async def create_cart_no_slash(payload: CartCreate, client: httpx.AsyncClient = Depends(get_http_client)):
    return await create_cart(payload, client)


@router.get("/user/{user_id}")
async def get_user_cart(user_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
    settings = get_settings()
    url = f"{settings.cart_service_url}/api/v1/carts/user/{user_id}"
    try:
        resp = await client.get(url)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Cart not found")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Cart service error: {exc}")


@router.post("/{cart_id}/items", status_code=201)
async def add_item(cart_id: str, payload: AddItemRequest, client: httpx.AsyncClient = Depends(get_http_client)):
    settings = get_settings()
    url = f"{settings.cart_service_url}/api/v1/carts/{cart_id}/items"
    try:
        product_id = payload.product_id
        quantity = payload.quantity
        unit_price = payload.unit_price

        # Always use Product Service as source of truth
        if unit_price is None:
            p = await client.get(f"{settings.product_service_url}/api/v1/products/{product_id}")
            if p.status_code != 200:
                content = None
                try:
                    content = p.json()
                except Exception:
                    content = {"detail": p.text}
                return JSONResponse(status_code=p.status_code, content=content)
            unit_price = p.json().get("price", 0.0)

        body = {
            "cart_id": cart_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price,
        }

        resp = await client.post(url, json=body)
        if resp.status_code >= 400:
            content = None
            try:
                content = resp.json()
            except Exception:
                content = {"detail": resp.text}
            return JSONResponse(status_code=resp.status_code, content=content)
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Cart service error: {exc}")


@router.get("/{cart_id}/items")
async def list_items(cart_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
    settings = get_settings()
    url = f"{settings.cart_service_url}/api/v1/carts/{cart_id}/items"
    try:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Cart service error: {exc}")


