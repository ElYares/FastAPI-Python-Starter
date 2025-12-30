"""
Users API routes (v1).

This module exposes user-related HTTP endpoints and delegates business logic to
the Service layer. Responses are validated/documented using Pydantic schemas.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.service.user_service import UserService
from app.shemas.user_shema import UserResponse

router = APIRouter(tags=["Users"])

# Service instance for user operations (demo / non-DB version).
user_service = UserService()


@router.get(
    "/users",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Retorna una lista de usuarios desde el repositorio (demo).",
)
def get_users() -> list[UserResponse]:
    """
    List users.

    Returns:
        list[UserResponse]: List of users returned by the service layer.
    """
    return user_service.list_users()
