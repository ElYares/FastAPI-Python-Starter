"""
Logger configuration using loguru
"""

from loguru import logger
import sys
import os

# Remove default handler and add a custom stdout Logger
logger.remove()
# Solo loguear si no estamos en entorno de test
if os.getenv("TESTING") != "1":
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time}</green> | <level>{level}</level> | <cyan>{message}</cyan>"
    )



def get_logger():
    """
    Returns the configured logger.

    Returns:
        loguru.Logger: configured logger instance
    """

    return logger
