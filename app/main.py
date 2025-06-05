from fastapi import FastAPI, Request
from app.api.v1.routes import router
from fastapi.responses import JSONResponse
from app.middleware import LoggingMiddleware
from app.exceptions import NotFoundException, BadRequestException
from app.logger import get_logger

"""
Punto de entrada de la aplicacion FastAPI
Se inicializa la app, se configura los metadatos
Incluyen las rutas de la version 1 de la API
"""

# Crear instancia de la aplicacion FASTAPI
app = FastAPI(
    title="FastAPI Starter",
    version="1.0.0",
    description="Starter API con patron Repository + Service"
)

# Incluir rutas definidas en los modulos de rutas (v1)
# Todas las rutas estaran bajo el prefijo /api/v1
app.include_router(router, prefix="/api/v1")

# Agregamos middleware
app.add_middleware(LoggingMiddleware)

# logger
logger = get_logger()

# Manejo de errores personalizados
@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    """
    Maneja excepciones de tipo NotFoundException (HTTP 404).
    """
    logger.warning(f"NotFound: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    """
    Maneja excepciones de tipo BadRequestException (HTTP 400).
    """
    logger.warning(f"BadRequest: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Maneja cualquier otra excepción no capturada (HTTP 500).
    """
    logger.exception("Unhandled exception occurred")
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
