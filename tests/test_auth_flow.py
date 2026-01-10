"""
Integration tests for auth flow.

Covers the full flow:
- register a user
- login with credentials (OAuth2PasswordRequestForm)
- access a protected endpoint using Bearer token
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_login_secure_flow():
    # Register
    register_payload = {
        "email": "flow@test.com",
        "password": "123456",
        "full_name": "Flow Test",
    }
    r = client.post("/api/v1/register", json=register_payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["email"] == "flow@test.com"

    # Login (OAuth2 form)
    login_form = {"username": "flow@test.com", "password": "123456"}
    r = client.post("/api/v1/login", data=login_form)
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    assert token

    # Secure
    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/api/v1/secure", headers=headers)
    assert r.status_code == 200, r.text
    secure_data = r.json()
    assert secure_data["email"] == "flow@test.com"
    assert secure_data["is_active"] is True


def test_login_rejects_invalid_password():
    # Ensure user exists
    client.post(
        "/api/v1/register",
        json={"email": "badpass@test.com", "password": "123456", "full_name": "Bad Pass"},
    )

    # Wrong password
    r = client.post("/api/v1/login", data={"username": "badpass@test.com", "password": "wrong"})
    assert r.status_code in (400, 401), r.text


def test_secure_requires_token():
    r = client.get("/api/v1/secure")
    assert r.status_code == 401, r.text
