"""
Global exception handlers.

Standardizes error responses across the API so clients receive a consistent shape.
"""

from __future__ import annotations

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Standard handler for HTTPException.

    Response shape:
        { "error": "<Reason>", "message": "<detail>" }
    """
    reason = getattr(exc, "detail", "HTTP Error")
    # If detail is not a string, keep it serialized
    message = reason if isinstance(reason, str) else "HTTP Error"
    request_id = _get_request_id(request)
    headers = dict(getattr(exc, "headers", {}) or {})
    headers.setdefault("X-Request-ID", request_id)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": _status_label(exc.status_code),
            "message": message,
            "request_id": request_id,
        },
        headers=headers,
    )


def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Standard handler for request validation errors (422).
    """
    request_id = _get_request_id(request)
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "La petición contiene datos inválidos",
            "details": exc.errors(),
            "request_id": request_id,
        },
        headers={"X-Request-ID": request_id},
    )


def unhandled_exception_handler(request: Request, __: Exception) -> JSONResponse:
    """
    Catch-all handler for unexpected errors (500).
    """
    request_id = _get_request_id(request)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Ocurrió un error inesperado",
            "request_id": request_id,
        },
        headers={"X-Request-ID": request_id},
    )


def _status_label(status_code: int) -> str:
    """
    Map status code to a short error label.
    """
    mapping: dict[int, str] = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        409: "Conflict",
        422: "Validation Error",
        500: "Internal Server Error",
    }
    return mapping.get(status_code, "HTTP Error")


def _get_request_id(request: Request) -> str:
    """Return the current request ID for error-correlation purposes."""
    return getattr(request.state, "request_id", "-")
