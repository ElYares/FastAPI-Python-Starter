from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.error_handlers import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)

from app.api.v1.routes import router
from app.api.v1.health_routes import router as health_router
from app.api.v1.healthz_routes import router as healthz_router
from app.api.v1.auth_routes import router as auth_router
from app.api.v1.secure_routes import router as secure_router
from app.exceptions import NotFoundException, BadRequestException
from app.middleware import setup_middlewares

from app.config import settings
from app.api.v1.debug_routes import router as debug_router




"""
Punto de entrada de la aplicacion FastAPI
Se inicializa la app, se configura los metadatos
Incluyen las rutas de la version 1 de la API
"""

# Metadata para organizar la documentación Swagger por secciones (tags)
tags_metadata = [
    {
        "name": "Debug",
        "description": "Endpoints de prueba (solo disponibles en development).",
    },
    {
        "name": "Health",
        "description": "Endpoints de salud y verificación de disponibilidad del servicio.",
    },
    {
        "name": "Auth",
        "description": "Autenticación y generación de tokens JWT (Bearer).",
    },
    {
        "name": "Secure",
        "description": "Endpoints protegidos que requieren JWT válido.",
    },
    {
        "name": "Core",
        "description": "Rutas base y recursos principales de la API.",
    },
]

# Crear instancia de la aplicacion FASTAPI
app = FastAPI(
    title="FastAPI Starter",
    version="1.0.0",
    description="Starter API con patron Repository + Service",
    openapi_tags=tags_metadata,
    contact={
        "name": "Elyares",
        "url": "https://elyares.org",
    },
    license_info={"name": "MIT"},
    swagger_ui_parameters={
        "persistAuthorization": True,
    }
)

# -----------------------------
# Exception handlers (formato consistente)
# -----------------------------
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)




# Middleware global
setup_middlewares(app)

# Routers v1
app.include_router(router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
app.include_router(healthz_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(secure_router, prefix="/api/v1")

# Rutas debug solo en development / debug
if settings.DEBUG or settings.APP_ENV != "production":
    app.include_router(debug_router, prefix="/api/v1")
