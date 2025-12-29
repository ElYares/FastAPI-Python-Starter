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
    # CSV -> list, ejemplo:
    # ALLOWED_ORIGINS=http://localhost,http://127.0.0.1,http://localhost:5173
    # Definición de orígenes permitidos según entorno
    origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]

    # Fallback seguro si viene vacio
    if not origins:
        origins = ["http://localhost", "http://127.0.0.1"]

    app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
    )