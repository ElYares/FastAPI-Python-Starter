"""
Define los esquemas de entrada y salida para los endpoints.

Usamos Pydantic para validar, serializar y documentar automáticamente
los datos expuestos por la API.
"""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


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

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """
    Esquema de salida para el endpoint de autenticación.
    """

    access_token: str = Field(..., description="JWT de acceso")
    token_type: str = Field("bearer", description="Tipo de token (Bearer)")
