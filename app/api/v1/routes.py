"""
Users API routes (v1).

Defines user-related endpoints and delegates business logic to the Service layer.
Uses dependency injection to obtain a request-scoped SQLAlchemy session.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.service.user_service import UserService
from app.shemas.user_shema import UserResponse

router = APIRouter(tags=["Users"])


@router.get(
    "/users",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Retorna una lista de usuarios desde la base de datos.",
)
def get_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    """
    List users from the database.

    Args:
        db: Request-scoped SQLAlchemy session.

    Returns:
        list[UserResponse]: Users serialized using the response schema.
    """
    return UserService(db).list_users()
