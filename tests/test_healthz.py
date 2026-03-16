"""Tests for `/api/v1/healthz` liveness endpoint."""

from __future__ import annotations

import time

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz_returns_ok() -> None:
    """Assert that healthz returns HTTP 200 and status=ok."""
    r = client.get("/api/v1/healthz")
    assert r.status_code == 200
    body = r.json()
    assert "status" in body
    assert body["status"] == "ok"


def test_healthz_is_lightweight() -> None:
    """Healthz should be fast and without dependencies."""

    start = time.time()
    r = client.get("/api/v1/healthz")
    duration = time.time() - start
    assert r.status_code == 200
    assert duration < 0.1  # Should be very fast
