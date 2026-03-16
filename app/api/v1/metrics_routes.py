"""Metrics routes (v1)."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import Response

from app.metrics import render_metrics

router = APIRouter(tags=["Observability"])


@router.get(
    "/metrics",
    summary="Prometheus metrics",
    description="Expone métricas HTTP básicas en formato Prometheus text exposition.",
)
def get_metrics() -> Response:
    """
    Return Prometheus metrics for scraping.

    Returns:
        Response: Prometheus text payload with the correct content type.
    """
    body, content_type = render_metrics()
    return Response(content=body, media_type=content_type)
