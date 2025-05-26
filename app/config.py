from pydantic import BaseSettings
from dotenv import load_dotenv

"""
Modulo de configuracion de la aplicacion
Carga las variables de entorno necesarias desde un archivo '.env'
y las expone de forma de estructurada para la app
"""

# Carga automaticamente variables desde un archivo .env
load_dotenv()

class Settings(BaseSettings):
    """
    Clase de configuracion que define todas las variables que pueden
    ser utilizadas desde cualquier parte de la aplicacion.
    """

    APP_NAME: str = "FastAPI Starter"
    APP_ENV: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

# Instancia global accesible para cualquier Modulo
settings = Settings()
