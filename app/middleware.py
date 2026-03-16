"""
Configure global middleware for the FastAPI application.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


def setup_middlewares(app: FastAPI) -> None:
    """Attach CORS middleware using environment-driven allowed origins."""
    origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]

    # Apply a safe fallback during local development.
    if not origins:
        origins = ["http://localhost", "http://127.0.0.1"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
