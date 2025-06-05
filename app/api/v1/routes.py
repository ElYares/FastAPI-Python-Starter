from fastapi import APIRouter
from app.service.user_service import UserService
from app.shemas.user_shema import UserResponse
from app.exceptions import NotFoundException, BadRequestException

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

@router.get("/not-found")
async def trigger_not_found():
    raise NotFoundException("El recurso no existe")

@router.get("/bad-request")
async def trigger_bad_request():
    raise BadRequestException("Peticion Incorrecta")

@router.get("/exception")
async def trigger_exception():
    raise Exception("Explosión")

