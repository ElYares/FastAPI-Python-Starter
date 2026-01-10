"""
Custom HTTP exceptions used across the application.

These exceptions allow the service layer to raise domain-specific errors while
keeping HTTP concerns explicit (status codes, client-facing messages).
"""

from __future__ import annotations

from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    """Exception for resource not found (HTTP 404)."""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestException(HTTPException):
    """Exception for bad request (HTTP 400)."""

    def __init__(self, detail: str = "Bad Request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedException(HTTPException):
    """Exception for unauthorized access (HTTP 401)."""

    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
