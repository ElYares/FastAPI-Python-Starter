"""
Custom middleware for structured request logging
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
from .logger import get_logger

logger = get_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs each HTTP requests
    """

    async def dispatch(self, request: Request, call_next):
        """
        Process and log the HTTP request

        Args:
            request: Incomming Request
            call_next: Next Handler middleware chain.

        Returns:
            Response: Outgoing response
        """

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
                f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s"
        )

        return response

