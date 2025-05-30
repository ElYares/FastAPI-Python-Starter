from fastapi import FastAPI
from app.api.v1.routes import router

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
