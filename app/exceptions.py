"""
Manejador de Errores custom para HTTP Errores
"""

from fastapi import HTTPException, status

class NotFoundExeption(HTTPException):
    """
    Exception for resource not found (HTTP 400)
    """

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestException(HTTPException):
    """
    Exception for bad request (HTTP 400)
    """

    def __init__(self, detail: str="Bad Request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

