"""
Define los esquemas de entrada y salida para los endpoints.

Usamos Pydantic para validar, serializar y documentar automáticamente
los datos expuestos por la API.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserResponse(BaseModel):
    """
    Esquema público de salida para representar un usuario.

    Nota:
        - No expone campos sensibles como `hashed_password`.
        - Se serializa desde objetos ORM usando `from_attributes=True`.
    """

    id: int = Field(..., description="ID del usuario")
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    full_name: str | None = Field(default=None, description="Nombre completo del usuario")
    is_active: bool = Field(default=True, description="Indica si el usuario está activo")

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """
    Esquema de salida para el endpoint de autenticación.
    """

    access_token: str = Field(..., description="JWT de acceso")
    refresh_token: str | None = Field(default=None, description="JWT de refresco con rotación")
    token_type: str = Field("bearer", description="Tipo de token (Bearer)")


class RefreshTokenRequest(BaseModel):
    """Schema used to exchange a valid refresh token for a new token pair."""

    refresh_token: str = Field(..., description="Refresh token JWT vigente")


class UserCreate(BaseModel):
    """
    Schema used to register a new user.
    """

    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(
        ...,
        min_length=6,
        max_length=72,
        description="Contraseña (máx 72 bytes para bcrypt)",
    )
    full_name: str | None = Field(default=None, description="Nombre completo del usuario")
