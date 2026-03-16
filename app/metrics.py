"""Prometheus metrics helpers for HTTP observability."""

from __future__ import annotations

from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

REQUEST_COUNT = Counter(
    "fastapi_requests_total",
    "Total HTTP requests processed by the API.",
    ["method", "path", "status_code"],
)

REQUEST_LATENCY_SECONDS = Histogram(
    "fastapi_request_duration_seconds",
    "HTTP request latency in seconds.",
    ["method", "path"],
)


def observe_request(method: str, path: str, status_code: int, duration_seconds: float) -> None:
    """Record Prometheus metrics for a completed HTTP request."""
    REQUEST_COUNT.labels(method=method, path=path, status_code=str(status_code)).inc()
    REQUEST_LATENCY_SECONDS.labels(method=method, path=path).observe(duration_seconds)


def render_metrics() -> tuple[bytes, str]:
    """Return the current Prometheus exposition payload and content type."""
    return generate_latest(), CONTENT_TYPE_LATEST
