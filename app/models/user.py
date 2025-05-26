"""
Modelo de dominio que representa a un usuario
Este modelo esta desacoplado de Pydantic y de la capa de transporte 
"""

class User:
    """
    Clase que representa un usuario dentro de la logica de negocio
    """
    def __init__(self, id: int, name: str):
        self.id = id
        self.name =  name
