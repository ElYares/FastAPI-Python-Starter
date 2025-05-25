"""
Define los esquemas de entrada y salida para los endpoints
Usamos Pydantic para validar y documentar automaticamente los datos
"""

from pydantic import BaseModel

class UserResponse(BaseModel):
    """
    Esquema de salida que representa a un usuario en las respuestas HTTP
    """
    id: int
    name: str
