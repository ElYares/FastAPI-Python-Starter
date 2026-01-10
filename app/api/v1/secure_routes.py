"""
Protected routes (v1).

Endpoints under this router require a valid JWT token.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.models.db_user import DBUser
from app.shemas.user_shema import UserResponse

router = APIRouter(tags=["Secure"])


@router.get(
    "/secure",
    response_model=UserResponse,
    summary="Recurso protegido",
    description="Retorna el usuario autenticado validando el JWT contra la base de datos.",
)
def protected_route(user: DBUser = Depends(get_current_user)) -> UserResponse:
    """
    Return the authenticated user.

    Args:
        user: Authenticated user loaded from the database.

    Returns:
        UserResponse: Public user data.
    """
    return user
