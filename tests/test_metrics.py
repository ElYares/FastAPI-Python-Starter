"""Metrics endpoint tests."""

from __future__ import annotations


def test_metrics_endpoint_exposes_prometheus_payload(client) -> None:
    """The metrics endpoint should expose Prometheus text format."""
    client.get("/api/v1/health")

    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert "fastapi_requests_total" in response.text
    assert 'path="/api/v1/health"' in response.text


def test_metrics_count_health_requests(client) -> None:
    """Health requests should increment the labeled request counter."""
    client.get("/api/v1/health")
    client.get("/api/v1/health")

    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    metric_key = 'fastapi_requests_total{method="GET",path="/api/v1/health",status_code="200"}'
    assert metric_key in response.text
