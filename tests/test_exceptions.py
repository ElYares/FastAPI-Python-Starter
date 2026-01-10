"""
Exception endpoint tests.

These tests validate that debug-only endpoints return the expected HTTP status
codes and the standardized error response shape.

Note:
- These endpoints should only be mounted in development environments.
- The test suite expects the global exception handlers to return:
    { "error": "<Label>", "message": "<detail>" }
"""

from __future__ import annotations


def test_not_found_exception(client):
    """
    A NotFoundException should return HTTP 404 with a consistent error shape.
    """
    response = client.get("/api/v1/not-found")
    assert response.status_code == 404

    payload = response.json()
    assert payload["error"] == "Not Found"
    assert payload["message"] == "El recurso no existe"


def test_bad_request_exception(client):
    """
    A BadRequestException should return HTTP 400 with a consistent error shape.
    """
    response = client.get("/api/v1/bad-request")
    assert response.status_code == 400

    payload = response.json()
    assert payload["error"] == "Bad Request"
    assert payload["message"] == "Peticion Incorrecta"


def test_unhandled_exception(client):
    """
    An unhandled exception should return HTTP 500 with a consistent error shape.
    """
    response = client.get("/api/v1/exception")
    assert response.status_code == 500

    payload = response.json()
    assert payload["error"] == "Internal Server Error"
    # Message can be environment-dependent; only assert it's present and non-empty.
    assert "message" in payload
    assert isinstance(payload["message"], str)
    assert payload["message"].strip() != ""
