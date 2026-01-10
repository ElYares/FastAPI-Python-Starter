from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healthz_returns_ok():
    r = client.get("/api/v1/healthz")
    assert r.status_code == 200
    body = r.json()
    assert "status" in body
    assert body["status"] == "ok"

def test_healthz_is_lightweight():
    """Healthz should be fast and without dependencies."""
    import time
    start = time.time()
    r = client.get("/api/v1/healthz")
    duration = time.time() - start
    assert r.status_code == 200
    assert duration < 0.1  # Should be very fast
