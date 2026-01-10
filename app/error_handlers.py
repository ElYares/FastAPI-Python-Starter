"""
Global exception handlers.

Standardizes error responses across the API so clients receive a consistent shape.
"""

from __future__ import annotations

from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Standard handler for HTTPException.

    Response shape:
        { "error": "<Reason>", "message": "<detail>" }
    """
    reason = getattr(exc, "detail", "HTTP Error")
    # If detail is not a string, keep it serialized
    message = reason if isinstance(reason, str) else "HTTP Error"
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": _status_label(exc.status_code), "message": message},
        headers=getattr(exc, "headers", None),
    )


def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Standard handler for request validation errors (422).
    """
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "La petición contiene datos inválidos",
            "details": exc.errors(),
        },
    )


def unhandled_exception_handler(_: Request, __: Exception) -> JSONResponse:
    """
    Catch-all handler for unexpected errors (500).
    """
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "message": "Ocurrió un error inesperado"},
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
