from fastapi import APIRouter
from app.service.user_service import UserService
from app.shemas.user_shema import UserResponse

# Crear un enrutador para agrupar endpoints relacionados
router = APIRouter()

# Instanciar el servicio de usuruarios
user_service = UserService()

@router.get("/users", response_model=list[UserResponse])
def get_users():
    """
    Endpoint HTTP GET que retorna una lista de usuarios.
    La respuesta sera validada y documentada usando el esquema UserResponse
    """
    return user_service.list_users()


