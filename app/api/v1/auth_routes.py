"""
Authentication routes (v1).

This module provides authentication endpoints. Currently, `/login` is a demo
endpoint that issues a JWT token without validating credentials.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.service.auth_service import AuthService
from app.shemas.user_shema import TokenResponse

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

    Args:
        form_data: OAuth2 form data provided by Swagger UI or clients.

    Returns:
        TokenResponse: JWT access token and token type.

    Warning:
        This endpoint does not validate the user's password (demo-only).
        It should be replaced by a database-backed authentication flow in ÉPICA 5.
    """
    token = auth_service.create_access_token({"sub": form_data.username})
    return TokenResponse(access_token=token, token_type="bearer")
