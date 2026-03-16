"""
Healthz routes (v1).
Alternative health endpoint for monitoring systems that expect /healthz.
Lightweight endpoint without external dependencies.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["Healthz"])


@router.get(
    "/healthz",
    summary="Health check (alternative)",
    description="Health endpoint compatible con k8s /healthz convention.",
)
def healthz_check() -> dict[str, str]:
    """
    Return minimal liveness payload for container orchestration probes.

    Returns:
        dict[str, str]: Minimal liveness payload.
    """
    return {"status": "ok"}
