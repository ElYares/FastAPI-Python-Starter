"""
Application configuration module.

This module defines strongly-typed settings using Pydantic Settings.
Configuration is loaded from environment variables and an optional `.env` file.

Notes:
    - `extra="allow"` allows docker-compose variables (e.g., UID/GID) to exist
      in the same `.env` without breaking Settings validation.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load .env into process environment for local/dev execution.
# In Docker, variables can be provided via env_file or environment.
load_dotenv()


class Settings(BaseSettings):
    """
    Global application settings loaded from environment variables.

    Attributes:
        APP_NAME: Human-readable application name (used in logs, docs).
        APP_ENV: Environment name (development/production/etc.).
        DEBUG: Enables debug behaviors and more verbose logging.
        ALLOWED_ORIGINS: CSV list of CORS allowed origins.
        LOG_LEVEL: Logging verbosity ("debug", "info", "warning", etc.).
        DATABASE_URL: SQLAlchemy database URL (SQLite by default).
        DB_ECHO: If True, logs SQL statements (useful for debugging).
        JWT_SECRET_KEY: Secret key used to sign JWTs.
        JWT_ALGORITHM: JWT algorithm (default HS256).
        JWT_EXPIRE_MINUTES: Access token expiration in minutes.
    """

    # App
    APP_NAME: str = "FastAPI Starter"
    APP_ENV: str = "development"
    DEBUG: bool = True
    ALLOWED_ORIGINS: str = "http://localhost"
    LOG_LEVEL: str = "info"

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"
    DB_ECHO: bool = False

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
    )


# Global settings instance for import across the project.
settings = Settings()
