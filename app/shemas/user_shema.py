"""
Define los esquemas de entrada y salida para los endpoints
Usamos Pydantic para validar y documentar automaticamente los datos
"""

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    """
    Esquema de salida que representa a un usuario en las respuestas HTTP
    """
    id: int = Field(..., description="ID del usuario")
    name: str = Field(..., description="Nombre del usuario")


class TokenResponse(BaseModel):
    """
    Esquema de salida para el endpoint de autenticación.
    """
    access_token: str = Field(..., description="JWT de acceso")
    token_type: str = Field("bearer", description="Tipo de token (Bearer)")
