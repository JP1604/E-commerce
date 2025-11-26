"""CORS middleware for user service."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from user_service.infrastructure.config.settings import get_settings


def setup_cors(app: FastAPI) -> None:
    settings = get_settings()
    
    # For development, allow all localhost origins
    allow_origin_regex = r"http://localhost:\d+"
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_origin_regex=allow_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

