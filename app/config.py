"""
Application configuration module.

This module defines strongly-typed settings using Pydantic Settings.
Configuration is loaded from environment variables and an optional `.env` file.

Notes:
    - `extra="allow"` allows docker-compose variables (e.g., UID/GID) to exist
      in the same `.env` without breaking Settings validation.
"""

from __future__ import annotations

from dotenv import load_dotenv
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

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

    @model_validator(mode="after")
    def validate_security_settings(self) -> Settings:
        """Apply minimum security rules for runtime configuration."""
        if len(self.JWT_SECRET_KEY.encode("utf-8")) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 bytes long")

        is_production = self.APP_ENV.lower() == "production"
        uses_example_secret = "CHANGE_ME" in self.JWT_SECRET_KEY
        if is_production and (self.DEBUG or uses_example_secret):
            raise ValueError("Production requires DEBUG=false and a non-default JWT secret")

        return self


# Global settings instance for import across the project.
settings = Settings()
