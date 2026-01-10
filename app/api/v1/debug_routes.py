"""
Debug routes (v1).

This router contains endpoints intended ONLY for development/testing.
They are not included in production environments.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.exceptions import NotFoundException, BadRequestException

router = APIRouter(tags=["Debug"])


@router.get(
    "/not-found",
    summary="Debug: Not Found",
    description="Endpoint de prueba que lanza NotFoundException (solo dev).",
)
def debug_not_found():
    raise NotFoundException("El recurso no existe")


@router.get(
    "/bad-request",
    summary="Debug: Bad Request",
    description="Endpoint de prueba que lanza BadRequestException (solo dev).",
)
def debug_bad_request():
    raise BadRequestException("Peticion Incorrecta")


@router.get(
    "/exception",
    summary="Debug: Unhandled Exception",
    description="Endpoint de prueba que lanza Exception genérica (solo dev).",
)
def debug_exception():
    raise Exception("boom")
