"""
Modulo de configuración principal de la aplicación.
Gestiona las variables de entorno mediante Pydantic Settings y dotenv.
"""
from jedi import settings
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Carga automáticamente las variables del archivo .env
load_dotenv()


class Settings(BaseSettings):
    """
    Clase Settings expone las variables de configuración globales
    de la aplicación, usando tipado fuerte con Pydantic.
    """
    APP_NAME: str = "FastAPI Starter"
    APP_ENV: str = "development"
    DEBUG: bool = True
    ALLOWED_ORIGINS: str = "http://localhost"
    LOG_LEVEL: str = "info"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30

    # Configuración de Pydantic Settings
    model_config = SettingsConfigDict(env_file=".env")


# Instancia global para uso desde cualquier módulo
settings = Settings()

