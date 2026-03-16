"""
Configure global middleware for the FastAPI application.
"""

from __future__ import annotations

from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.config import settings
from app.logger import logger, reset_request_id, set_request_id
from app.metrics import observe_request


def setup_middlewares(app: FastAPI) -> None:
    """Attach CORS and security-response middleware."""
    origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
    allow_methods = [m.strip().upper() for m in settings.CORS_ALLOW_METHODS.split(",") if m.strip()]
    allow_headers = [h.strip() for h in settings.CORS_ALLOW_HEADERS.split(",") if h.strip()]

    # Apply a safe fallback during local development.
    if not origins:
        origins = ["http://localhost", "http://127.0.0.1"]
    if not allow_methods:
        allow_methods = ["GET", "POST", "OPTIONS"]
    if not allow_headers:
        allow_headers = ["Authorization", "Content-Type"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
    )

    @app.middleware("http")
    async def add_request_context(request: Request, call_next) -> Response:
        """Assign a request ID, expose it in headers, and log the request outcome."""
        request_id = request.headers.get("X-Request-ID", uuid4().hex)
        request.state.request_id = request_id
        ctx_token = set_request_id(request_id)
        started_at = perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (perf_counter() - started_at) * 1000
            route = request.scope.get("route")
            route_path = getattr(route, "path", request.url.path)
            observe_request(
                method=request.method,
                path=route_path,
                status_code=500,
                duration_seconds=duration_ms / 1000,
            )
            logger.exception(
                "Request failed: method=%s path=%s duration_ms=%.2f",
                request.method,
                request.url.path,
                duration_ms,
            )
            reset_request_id(ctx_token)
            raise

        duration_ms = (perf_counter() - started_at) * 1000
        route = request.scope.get("route")
        route_path = getattr(route, "path", request.url.path)
        observe_request(
            method=request.method,
            path=route_path,
            status_code=response.status_code,
            duration_seconds=duration_ms / 1000,
        )
        response.headers.setdefault("X-Request-ID", request_id)
        logger.info(
            "Request completed: method=%s path=%s status_code=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        reset_request_id(ctx_token)
        return response

    @app.middleware("http")
    async def add_security_headers(request: Request, call_next) -> Response:
        """Attach secure-by-default HTTP headers to every response."""
        response = await call_next(request)
        if not settings.SECURITY_HEADERS_ENABLED:
            return response

        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault(
            "Permissions-Policy",
            "camera=(), microphone=(), geolocation=()",
        )
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'",
        )
        response.headers.setdefault("Cross-Origin-Resource-Policy", "same-origin")

        if settings.APP_ENV.lower() == "production":
            response.headers.setdefault(
                "Strict-Transport-Security",
                f"max-age={settings.HSTS_MAX_AGE_SECONDS}; includeSubDomains; preload",
            )

        return response
