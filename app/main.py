from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.routes import router
from app.api.v1.health_routes import router as health_router
from app.api.v1.auth_routes import router as auth_router
from app.api.v1.secure_routes import router as secure_router
from app.exceptions import NotFoundException, BadRequestException
from app.middleware import setup_middlewares




"""
Punto de entrada de la aplicacion FastAPI
Se inicializa la app, se configura los metadatos
Incluyen las rutas de la version 1 de la API
"""

# Metadata para organizar la documentación Swagger por secciones (tags)
tags_metadata = [
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
@app.exception_handler(NotFoundException)
def not_found_handler(_: Request, exc: NotFoundException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(BadRequestException)
def bad_request_handler(_: Request, exc: BadRequestException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(Exception)
def unhandled_exception_handler(_: Request, __: Exception):
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})


# -----------------------------
# Endpoints de prueba para tests/test_exceptions.py
# -----------------------------
@app.get("/api/v1/not-found")
def _not_found():
    raise NotFoundException("El recurso no existe")


@app.get("/api/v1/bad-request")
def _bad_request():
    raise BadRequestException("Peticion Incorrecta")


@app.get("/api/v1/exception")
def _exception():
    raise Exception("boom")



# Middleware global
setup_middlewares(app)

# Incluir rutas definidas en los modulos de rutas (v1)
# Todas las rutas estaran bajo el prefijo /api/v1
app.include_router(router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(secure_router, prefix="/api/v1")
