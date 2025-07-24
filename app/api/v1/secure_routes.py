from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/secure")
def protected_route(user: str = Depends(get_current_user)):
    """
    Endpoint protegido que requiere autenticacion JWT para acceder

    Args:
        user: Usuario autenticado extraido del JWT

    Returns:
        dict: Mensaje de exito incluyendo el nombre del Usuario
    """

    return {"message": f"Bienvenido {user}, loggeado con exito al recurso protegido"}

