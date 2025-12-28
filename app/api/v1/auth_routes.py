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
    responses={
        200: {"description": "Token generado correctamente"},
    },
)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    token = auth_service.create_access_token({"sub": form_data.username})
    return TokenResponse(access_token=token, token_type="bearer")
    