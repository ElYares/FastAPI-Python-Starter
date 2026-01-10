"""
Authentication routes (v1).

This module provides authentication endpoints. Currently, `/login` is a demo
endpoint that issues a JWT token without validating credentials.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.service.auth_service import AuthService
from app.service.user_service import UserService
from app.shemas.user_shema import TokenResponse, UserCreate, UserResponse

router = APIRouter(tags=["Auth"])
auth_service = AuthService()


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
    description=(
        "Valida credenciales contra la base de datos usando bcrypt y retorna un JWT. "
        "Compatible con Swagger OAuth2 Password flow (Authorize)."
    ),
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Authenticate user credentials and return a JWT token.

    Notes:
        - Swagger UI uses OAuth2 Password flow: sends `username` and `password`.
        - We interpret `username` as the user's email.
    """
    user = UserService(db).authenticate_user(
        email=form_data.username,
        password=form_data.password,
    )

    token = auth_service.create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, token_type="bearer")


@router.post(
    "/register",
    response_model=UserResponse,
    summary="Registrar usuario",
    description="Crea un usuario en base de datos, hasheando la contraseña con bcrypt.",
)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """
    Register a new user in the database.

    Args:
        payload: User registration payload.
        db: Request-scoped SQLAlchemy session.

    Returns:
        UserResponse: Created user (public fields only).
    """
    return UserService(db).register_user(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
    )
