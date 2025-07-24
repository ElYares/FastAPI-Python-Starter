from fastapi import APIRouter
from app.service.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

@router.post("/login")
def login():
    """
    Simula un inicio de sesion devolviendo un token JWT para pruebas

    Returns:
        dict: Diccionario con el token y su tipo
    """

    token = auth_service.create_access_token({"sub":"admin"})
    return {"access_token": token,"token_type":"bearer"}
