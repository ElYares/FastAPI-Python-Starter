from fastapi import APIRouter
from app.service.auth_service import AuthService
from app.shemas.user_shema import TokenResponse

router = APIRouter(tags=["Auth"])
auth_service = AuthService()


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión (demo)",
    description=(
        "Genera un token JWT para pruebas. "
        "Actualmente no valida credenciales y siempre genera un token para el usuario `admin`."
    ),
    responses={
        200: {"description": "Token generado correctamente"},
    },
)
def login() -> TokenResponse:
    token = auth_service.create_access_token({"sub": "admin"})
    return TokenResponse(access_token=token, token_type="bearer")
