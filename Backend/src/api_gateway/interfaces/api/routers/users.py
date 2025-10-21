"""Gateway user proxy routes."""

from fastapi import APIRouter, Depends, HTTPException
import httpx

from api_gateway.infrastructure.config.settings import get_settings
from api_gateway.infrastructure.http.client import get_http_client


router = APIRouter()


@router.get("/")
async def list_users(client: httpx.AsyncClient = Depends(get_http_client)):
    settings = get_settings()
    url = f"{settings.user_service_url}/api/v1/users/"
    try:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"User service error: {exc}")


@router.get("/{user_id}")
async def get_user(user_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
    settings = get_settings()
    url = f"{settings.user_service_url}/api/v1/users/{user_id}"
    try:
        resp = await client.get(url)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"User service error: {exc}")


