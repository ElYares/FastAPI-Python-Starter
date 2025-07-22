"""
Configuracion de middlewares globales para la aplicacion FastApi
Incluyendo el soporte para CORS
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings


def setup_middlewares(app: FastAPI) -> None:

    """
    Configura middlewares globales como CORS según el entorno de ejecución.
    """
    # Definición de orígenes permitidos según entorno
    origins = ["http://localhost","http://127.0.0.1"]

    if settings.APP_ENV=="production":
        # Puedes definir esto como variable o lista configurable
        origins = ["https://tudominio.com"]

    app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
    )
