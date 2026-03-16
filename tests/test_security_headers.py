"""Security middleware tests (headers + CORS behavior)."""

from __future__ import annotations


def test_security_headers_present(client) -> None:
    """Responses should include secure-by-default HTTP headers."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    assert response.headers.get("x-request-id")
    assert response.headers.get("x-content-type-options") == "nosniff"
    assert response.headers.get("x-frame-options") == "DENY"
    assert response.headers.get("referrer-policy") == "no-referrer"
    assert "content-security-policy" in response.headers
    assert "permissions-policy" in response.headers


def test_cors_preflight_allows_configured_origin(client) -> None:
    """Preflight should allow configured local frontend origins."""
    response = client.options(
        "/api/v1/secure",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Authorization,Content-Type",
        },
    )

    assert response.status_code in (200, 204)
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_request_id_header_is_preserved_when_provided(client) -> None:
    """A caller-supplied X-Request-ID should be echoed back in the response."""
    request_id = "req-test-12345"
    response = client.get("/api/v1/health", headers={"X-Request-ID": request_id})

    assert response.status_code == 200
    assert response.headers.get("x-request-id") == request_id
