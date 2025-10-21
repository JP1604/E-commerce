"""Shared async HTTP client for the API Gateway."""

from typing import AsyncGenerator
import httpx


_client: httpx.AsyncClient | None = None


async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Provide a shared httpx.AsyncClient instance with sensible defaults."""
    global _client
    if _client is None:
        _client = httpx.AsyncClient(timeout=httpx.Timeout(10.0, read=30.0), follow_redirects=True)
    try:
        yield _client
    finally:
        # Keep client alive for reuse across requests; do not close here
        pass


