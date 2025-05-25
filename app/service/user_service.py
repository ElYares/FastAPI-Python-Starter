from app.repositories.user_repository import UserRepository

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

    def list_users(self):
        """
        Retorna la lista de usuarios disponibles usuando el repositorio.
        """
        return self.repo.get_all_users()

