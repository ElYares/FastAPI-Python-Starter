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
    summary="Iniciar sesión (demo)",
    description=(
        "Genera un token JWT para pruebas usando el flujo OAuth2 Password. "
        "Actualmente NO valida credenciales: cualquier usuario/contraseña genera un token. "
        "El usuario del token se toma del campo `username`."
    ),
    responses={200: {"description": "Token generado correctamente"}},
)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    """
    Issue a demo JWT token using the OAuth2 Password flow.

    Warning:
        This endpoint does not validate the user's password (demo-only).
        It should be replaced by a database-backed authentication flow in ÉPICA 5.
    """
    token = auth_service.create_access_token({"sub": form_data.username})
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
