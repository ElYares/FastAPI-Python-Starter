"""
Auth endpoint tests.

These tests validate the minimal contract for:
- POST /api/v1/login (returns JWT token)
- GET /api/v1/secure (requires a valid Bearer token)
- expired / invalid token behavior

Notes:
- The project uses DB-backed authentication, so each test must ensure a user
  exists before attempting login.
- The `client` fixture comes from tests/conftest.py and uses an isolated test DB.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from jose import jwt

from app.config import settings


def _unique_email(prefix: str = "t") -> str:
    """
    Build a unique email for each test case to avoid collisions.

    Args:
        prefix: A short prefix used to identify the test scenario.

    Returns:
        A unique email address like "login-1a2b3c4d@test.com".
    """
    return f"{prefix}-{uuid.uuid4().hex[:8]}@test.com"


def test_login_returns_token(client):
    """
    A successful login should return a Bearer access token.

    Flow:
    1) Register a new user in the test database.
    2) Login using OAuth2PasswordRequestForm payload (username/password).
    3) Assert token shape matches API contract.
    """
    email = _unique_email("login")
    password = "12345678"  # must satisfy minimum length validation

    # Ensure user exists (DB-backed auth requires stored credentials).
    r = client.post(
        "/api/v1/register",
        json={"email": email, "password": password, "full_name": "Auth Test"},
    )
    assert r.status_code == 200, r.text

    # OAuth2 form fields: username/password
    r = client.post("/api/v1/login", data={"username": email, "password": password})
    assert r.status_code == 200, r.text

    body = r.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_secure_requires_token(client):
    """
    Protected resources should require a Bearer token.

    Expected:
        GET /api/v1/secure without Authorization header returns 401.
    """
    r = client.get("/api/v1/secure")
    assert r.status_code == 401


def test_secure_with_valid_token(client):
    """
    Protected resource should be accessible with a valid JWT.

    Flow:
    1) Register user
    2) Login to obtain token
    3) Call /secure with Authorization: Bearer <token>
    4) Validate the response includes the authenticated user's email.
    """
    email = _unique_email("secure")
    password = "12345678"

    client.post(
        "/api/v1/register",
        json={"email": email, "password": password, "full_name": "Secure User"},
    )

    login = client.post("/api/v1/login", data={"username": email, "password": password})
    assert login.status_code == 200, login.text

    token = login.json()["access_token"]
    r = client.get("/api/v1/secure", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text

    payload = r.json()
    assert payload["email"] == email
    assert payload["is_active"] is True


def test_secure_with_invalid_token(client):
    """
    An invalid token must be rejected.

    Expected:
        401 Unauthorized for malformed/invalid JWT.
    """
    r = client.get("/api/v1/secure", headers={"Authorization": "Bearer invalid-token"})
    assert r.status_code == 401


def test_secure_with_expired_token(client):
    """
    An expired JWT must be rejected.

    We generate a token with an expiration time in the past and verify
    the endpoint responds with 401.
    """
    expired = datetime.now(timezone.utc) - timedelta(minutes=2)

    token = jwt.encode(
        {"sub": "does-not-matter", "exp": expired},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    r = client.get("/api/v1/secure", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401
