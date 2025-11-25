"""CORS middleware configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ....infrastructure.config import get_settings


def setup_cors(app: FastAPI) -> None:
    """Configure CORS middleware for the FastAPI application."""
    settings = get_settings()
    
    # For development, allow all localhost origins
    import re
    allow_origins = settings.backend_cors_origins
    
    # Add regex pattern for all localhost ports
    allow_origin_regex = r"http://localhost:\d+"
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_origin_regex=allow_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )