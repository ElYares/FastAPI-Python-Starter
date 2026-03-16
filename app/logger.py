"""
Configuración del sistema de logging para la aplicación.
Inicializa un logger global con formato estructurado para producción o desarrollo.
"""

from __future__ import annotations

import json
import logging
import sys
from contextvars import ContextVar
from datetime import UTC, datetime

from app.config import settings

_request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="-")


class JsonFormatter(logging.Formatter):
    """Render log records as compact JSON for production ingestion."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "request_id": getattr(record, "request_id", "-"),
            "message": record.getMessage(),
        }
        return json.dumps(payload, ensure_ascii=True)


class RequestIdFilter(logging.Filter):
    """Inject the current request ID into every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = _request_id_ctx_var.get()
        return True


def setup_logger() -> None:
    """
    Configure root logging for the application runtime.
    """
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    logging.basicConfig(
        level=log_level,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    root_logger = logging.getLogger()
    request_id_filter = RequestIdFilter()
    resolved_format = settings.resolved_log_format()

    for handler in root_logger.handlers:
        handler.addFilter(request_id_filter)
        if resolved_format == "json":
            handler.setFormatter(JsonFormatter())
        else:
            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s | %(levelname)s | request_id=%(request_id)s | %(message)s"
                )
            )

    logging.info("Logger inicializado en nivel %s", logging.getLevelName(log_level))


def set_request_id(request_id: str) -> object:
    """Store a request ID in the current execution context."""
    return _request_id_ctx_var.set(request_id)


def reset_request_id(token: object) -> None:
    """Restore the previous request ID context after a request finishes."""
    _request_id_ctx_var.reset(token)


# Llamada para inicializar el logger global
setup_logger()

# Instancia del logger para importar en cualquier parte del código
logger = logging.getLogger(settings.APP_NAME)
