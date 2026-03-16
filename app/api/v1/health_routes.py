"""
Health check routes (v1).

Health endpoints are used for liveness checks and service monitoring.
They should be lightweight and avoid calling external dependencies whenever possible.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.config import settings

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Health check",
    description="Verifica la disponibilidad del servicio y retorna metadata del entorno.",
)
def health_check() -> dict[str, str]:
    """
    Return service health and basic runtime metadata.

    Returns:
        dict[str, str]: Liveness payload with app name and environment.

    Notes:
        Keep this endpoint lightweight to be used by probes/health checks.
    """
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
    }
