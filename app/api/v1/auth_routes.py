"""
Authentication routes (v1).

This module provides user registration and login endpoints backed by the
database and password hashing/verification.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.rate_limit import enforce_login_rate_limit
from app.service.token_service import TokenService
from app.service.user_service import UserService
from app.shemas.user_shema import (
    RefreshTokenRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)

router = APIRouter(tags=["Auth"])


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
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Authenticate user credentials and return an access token.

    This endpoint expects `application/x-www-form-urlencoded` payload via
    OAuth2 Password flow:
    - `username`: user email
    - `password`: plaintext password

    Args:
        request: Incoming HTTP request used for rate limiting metadata.
        form_data: OAuth2 form payload from the request body.
        db: Request-scoped SQLAlchemy session.

    Returns:
        TokenResponse: JWT access token and token type (`bearer`).

    Raises:
        BadRequestException: If credentials are invalid.
        HTTPException: If login rate limit is exceeded (429).
    """
    enforce_login_rate_limit(request=request, username=form_data.username)

    user = UserService(db).authenticate_user(
        email=form_data.username,
        password=form_data.password,
    )
    return TokenService(db).issue_token_pair(user.id)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refrescar tokens",
    description="Rota un refresh token válido y retorna un nuevo access/refresh token.",
)
def refresh_tokens(payload: RefreshTokenRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """
    Rotate a refresh token and issue a new token pair.

    Args:
        payload: Refresh token payload.
        db: Request-scoped SQLAlchemy session.

    Returns:
        TokenResponse: New access token and new refresh token.
    """
    return TokenService(db).rotate_refresh_token(payload.refresh_token)


@router.post(
    "/register",
    response_model=UserResponse,
    summary="Registrar usuario",
    description="Crea un usuario en base de datos, hasheando la contraseña con bcrypt.",
)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """
    Register a new user and persist it in the database.

    Args:
        payload: User registration payload.
        db: Request-scoped SQLAlchemy session.

    Returns:
        UserResponse: Created user (public fields only).

    Raises:
        BadRequestException: If the email is already registered.
    """
    return UserService(db).register_user(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
    )
