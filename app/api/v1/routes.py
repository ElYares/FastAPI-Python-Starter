from fastapi import APIRouter
from app.service.user_service import UserService
from app.shemas.user_shema import UserResponse

router = APIRouter(tags=["Users"])
user_service = UserService()


@router.get(
    "/users",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Retorna una lista de usuarios desde el repositorio (demo).",
)
def get_users() -> list[UserResponse]:
    return user_service.list_users()
