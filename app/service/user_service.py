from app.repositories.user_repository import UserRepository
from app.logger import logger

"""
Servicio que encapsula la logica de negocio relacionada con usuarios.
Este modulo actua como intermediario entre la API (rutas) y el repositorio (datos).
"""

class UserService:
    """
    Servicio de usuarios: gestiona  operaciones relaciondas a usuario.
    """
    def __init__(self):
        self.repo = UserRepository()
        logger.info("UserService inicializado correctamente")

    def list_users(self):
        """
        Retorna la lista de usuarios disponibles usuando el repositorio.
        """
        logger.info("list_users() ejecutado - Consultando usuarios desde UserRepository")
        return self.repo.get_all_users()

