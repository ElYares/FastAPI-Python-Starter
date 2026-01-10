"""
Repositorio que simula el acceso a datos persistentes.
En un entorno real, aqui se conetaria a una base de datos (SQL, NoSQL)
"""

from app.models.user import User

# Simulacion de una "Base de datos" en memoria
_fake_db = [
    User(1,"Ada Lovelace"),
    User(2,"Alan Turing"),
    User(3,"Gauss Jordan"),
]


class UserRepository:
    """
    Repositorio que proporciona acceso a datos de usuario
    """

    def get_all_users(self):
        """
        Retorna todos los usuarios simulados de la "base de datos".
        """
        return _fake_db
