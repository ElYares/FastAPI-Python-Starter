"""
Integration tests for auth flow.

Covers the full flow:
- register a user
- login with credentials (OAuth2PasswordRequestForm)
- access a protected endpoint using Bearer token

Notes:
- Uses the `client` fixture (tests/conftest.py) which injects an isolated test DB.
- Uses unique emails to avoid collisions between tests.
"""

from __future__ import annotations

import uuid


def test_register_login_secure_flow(client):
    """
    Full end-to-end flow test:
    1) Register user
    2) Login and get JWT
    3) Access /secure and validate identity payload
    """
    email = f"flow-{uuid.uuid4().hex[:8]}@test.com"
    password = "12345678"  # must satisfy minimum length validation

    # --- Register ---
    register_payload = {
        "email": email,
        "password": password,
        "full_name": "Flow Test",
    }
    r = client.post("/api/v1/register", json=register_payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["email"] == email

    # --- Login (OAuth2 form) ---
    login_form = {"username": email, "password": password}
    r = client.post("/api/v1/login", data=login_form)
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    assert token

    # --- Secure endpoint ---
    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/api/v1/secure", headers=headers)
    assert r.status_code == 200, r.text
    secure_data = r.json()

    # Validate that the protected endpoint returns the authenticated user.
    assert secure_data["email"] == email
    assert secure_data["is_active"] is True


def test_login_rejects_invalid_password(client):
    """
    Logging in with an invalid password should be rejected (400/401).

    Flow:
    1) Register user
    2) Attempt login with wrong password
    3) Assert the API rejects it
    """
    email = f"badpass-{uuid.uuid4().hex[:8]}@test.com"
    password = "12345678"

    # Ensure user exists.
    client.post(
        "/api/v1/register",
        json={"email": email, "password": password, "full_name": "Bad Pass"},
    )

    # Wrong password should not authenticate.
    r = client.post("/api/v1/login", data={"username": email, "password": "wrong"})
    assert r.status_code in (400, 401), r.text


def test_secure_requires_token(client):
    """
    /secure must reject requests without a Bearer token.
    """
    r = client.get("/api/v1/secure")
    assert r.status_code == 401, r.text
