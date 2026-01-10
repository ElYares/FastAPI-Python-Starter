from fastapi import APIRouter
from app.config import settings

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Health check",
    description="Verifica la disponibilidad del servicio y retorna metadata del entorno.",
)
def health_check() -> dict:
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
    }
