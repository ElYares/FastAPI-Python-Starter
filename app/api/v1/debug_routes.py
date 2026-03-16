"""
Debug routes (v1).

This router contains endpoints intended ONLY for development/testing.
They are not included in production environments.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.exceptions import BadRequestException, NotFoundException

router = APIRouter(tags=["Debug"])


@router.get(
    "/not-found",
    summary="Debug: Not Found",
    description="Endpoint de prueba que lanza NotFoundException (solo dev).",
)
def debug_not_found() -> None:
    """
    Raise a controlled 404 error for testing exception handlers.

    Raises:
        NotFoundException: Always raised to validate 404 response formatting.
    """
    raise NotFoundException("El recurso no existe")


@router.get(
    "/bad-request",
    summary="Debug: Bad Request",
    description="Endpoint de prueba que lanza BadRequestException (solo dev).",
)
def debug_bad_request() -> None:
    """
    Raise a controlled 400 error for testing exception handlers.

    Raises:
        BadRequestException: Always raised to validate 400 response formatting.
    """
    raise BadRequestException("Peticion Incorrecta")


@router.get(
    "/exception",
    summary="Debug: Unhandled Exception",
    description="Endpoint de prueba que lanza Exception genérica (solo dev).",
)
def debug_exception() -> None:
    """
    Raise an unhandled exception to validate 500-error behavior in tests.

    Raises:
        Exception: Always raised to trigger the global 500 handler.
    """
    raise Exception("boom")
