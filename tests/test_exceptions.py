"""
Exception endpoint tests.

These tests validate:
- Standardized error response shape from handlers
- Debug-only endpoints when they are available (development mode)

Note:
- Debug endpoints are only mounted when settings.DEBUG is True or APP_ENV != "production".
"""

from __future__ import annotations


def test_not_found_exception(client):
    """
    A NotFound path should return HTTP 404 with a consistent error shape.
    """
    response = client.get("/api/v1/not-found")
    assert response.status_code == 404

    payload = response.json()
    assert payload["error"] == "Not Found"

    # Message can vary depending on which handler produced the response.
    # We only assert that the message exists and is non-empty.
    assert "message" in payload
    assert isinstance(payload["message"], str)
    assert payload["message"].strip() != ""


def test_bad_request_exception(client):
    """
    Debug-only endpoint: /api/v1/bad-request

    If debug routes are mounted, it should return 400 with consistent error shape.
    If not mounted, return 404 and fail with a clear hint.
    """
    response = client.get("/api/v1/bad-request")

    if response.status_code == 404:
        raise AssertionError(
            "Debug routes are not mounted in tests. "
            "Ensure tests run with DEBUG=true or APP_ENV!=production "
            "before importing app.main."
        )

    assert response.status_code == 400, response.text
    payload = response.json()
    assert payload["error"] == "Bad Request"
    assert "message" in payload


def test_unhandled_exception(client):
    """
    Debug-only endpoint: /api/v1/exception

    If debug routes are mounted, it should return 500 with consistent error shape.
    If not mounted, return 404 and fail with a clear hint.
    """
    response = client.get("/api/v1/exception")

    if response.status_code == 404:
        raise AssertionError(
            "Debug routes are not mounted in tests. "
            "Ensure tests run with DEBUG=true or APP_ENV!=production "
            "before importing app.main."
        )

    assert response.status_code == 500, response.text
    payload = response.json()
    assert payload["error"] == "Internal Server Error"
    assert "message" in payload
    assert isinstance(payload["message"], str)
    assert payload["message"].strip() != ""
