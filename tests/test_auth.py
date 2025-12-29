from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from jose import jwt

from app.main import app
from app.config import settings

client = TestClient(app)


def test_login_returns_token():
    r = client.post(
        "/api/v1/login",
        data={"username": "admin", "password": "anything"},
    )
    assert r.status_code == 200
    body = r.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_secure_requires_token():
    r = client.get("/api/v1/secure")
    assert r.status_code == 401


def test_secure_with_valid_token():
    login = client.post("/api/v1/login", data={"username": "admin", "password": "x"})
    token = login.json()["access_token"]

    r = client.get("/api/v1/secure", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert "admin" in r.json()["message"]


def test_secure_with_invalid_token():
    r = client.get("/api/v1/secure", headers={"Authorization": "Bearer invalid-token"})
    assert r.status_code == 401


def test_secure_with_expired_token():
    expired = datetime.now(timezone.utc) - timedelta(minutes=2)
    token = jwt.encode(
        {"sub": "admin", "exp": expired},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    r = client.get("/api/v1/secure", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401
