"""
Configuración del sistema de logging para la aplicación.
Inicializa un logger global con formato estructurado para producción o desarrollo.
"""

import logging
import sys
from app.config import settings


def setup_logger() -> None:
    """
    Inicializa el logger global con nivel y formato adecuado
    según el entorno configurado en las variables de entorno.
    """
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    logging.info("✅ Logger inicializado en nivel %s", logging.getLevelName(log_level))


# Llamada para inicializar el logger global
setup_logger()

# Instancia del logger para importar en cualquier parte del código
logger = logging.getLogger(settings.APP_NAME)

