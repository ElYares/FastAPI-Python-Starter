from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter(tags=["Secure"])


@router.get(
    "/secure",
    summary="Endpoint protegido (demo)",
    description="Requiere un JWT válido en el header Authorization: Bearer <token>.",
    responses={
        200: {"description": "Acceso permitido"},
        401: {"description": "Token inválido o ausente"},
    },
)
def protected_route(user: str = Depends(get_current_user)) -> dict:
    return {"message": f"Bienvenido {user}, loggeado con exito al recurso protegido"}
