"""
Healthz routes (v1).
Alternative health endpoint for monitoring systems that expect /healthz.
Lightweight endpoint without external dependencies.
"""
from __future__ import annotations
from fastapi import APIRouter
from app.config import settings

router = APIRouter(tags=["Healthz"])

@router.get(
    "/healthz",
    summary="Health check (alternative)",
    description="Health endpoint compatible con k8s /healthz convention.",
)
def healthz_check() -> dict[str, str]:
    """
    Check service status for k8s health check.

    Returns:
        dict[str, str]: Service status and version if available.
    """
    response = {"status": "ok"}
    
    # NO CONFIRMADO: No hay variable VERSION en config.py verificado
    # Para agregar versión, necesitaría confirmar si existe en settings
    # o proponer agregarla. Por ahora sin versión para evitar invenciones.
    
    return response
