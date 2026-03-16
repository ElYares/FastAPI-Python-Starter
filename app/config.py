"""
Application configuration module.

This module defines strongly-typed settings using Pydantic Settings.
Configuration is loaded from environment variables and an optional `.env` file.

Notes:
    - `extra="allow"` allows docker-compose variables (e.g., UID/GID) to exist
      in the same `.env` without breaking Settings validation.
"""

from __future__ import annotations

from typing import Literal

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
        CORS_ALLOW_METHODS: CSV list of allowed CORS methods.
        CORS_ALLOW_HEADERS: CSV list of allowed CORS headers.
        CORS_ALLOW_CREDENTIALS: Whether CORS credentials are allowed.
        SECURITY_HEADERS_ENABLED: Enables secure HTTP response headers.
        HSTS_MAX_AGE_SECONDS: Strict-Transport-Security max-age.
        LOG_LEVEL: Logging verbosity ("debug", "info", "warning", etc.).
        LOG_FORMAT: Output format for logs ("text", "json", or "auto").
        DATABASE_URL: SQLAlchemy database URL (SQLite by default).
        DB_ECHO: If True, logs SQL statements (useful for debugging).
        JWT_SECRET_KEY: Secret key used to sign JWTs.
        JWT_ALGORITHM: JWT algorithm (default HS256).
        JWT_EXPIRE_MINUTES: Access token expiration in minutes.
        JWT_REFRESH_EXPIRE_MINUTES: Refresh token expiration in minutes.
        LOGIN_RATE_LIMIT_ATTEMPTS_PER_IP: Max login attempts per IP in window.
        LOGIN_RATE_LIMIT_ATTEMPTS_PER_USER: Max login attempts per user in window.
        LOGIN_RATE_LIMIT_WINDOW_SECONDS: Sliding window size in seconds.
    """

    # App
    APP_NAME: str = "FastAPI Starter"
    APP_ENV: str = "development"
    DEBUG: bool = True
    ALLOWED_ORIGINS: str = "http://localhost"
    CORS_ALLOW_METHODS: str = "GET,POST,PUT,PATCH,DELETE,OPTIONS"
    CORS_ALLOW_HEADERS: str = "Authorization,Content-Type,Accept,Origin"
    CORS_ALLOW_CREDENTIALS: bool = True
    SECURITY_HEADERS_ENABLED: bool = True
    HSTS_MAX_AGE_SECONDS: int = 31536000
    LOG_LEVEL: str = "info"
    LOG_FORMAT: Literal["auto", "text", "json"] = "auto"

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"
    DB_ECHO: bool = False

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_EXPIRE_MINUTES: int = 60 * 24 * 7

    # Rate limit (login endpoint)
    LOGIN_RATE_LIMIT_ATTEMPTS_PER_IP: int = 20
    LOGIN_RATE_LIMIT_ATTEMPTS_PER_USER: int = 5
    LOGIN_RATE_LIMIT_WINDOW_SECONDS: int = 60

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

        if is_production:
            if "*" in self.ALLOWED_ORIGINS:
                raise ValueError("Production CORS cannot use wildcard origins")
            if "*" in self.CORS_ALLOW_METHODS or "*" in self.CORS_ALLOW_HEADERS:
                raise ValueError("Production CORS methods/headers cannot use wildcards")

        return self

    def resolved_log_format(self) -> str:
        """Return the effective log format for the current environment."""
        if self.LOG_FORMAT != "auto":
            return self.LOG_FORMAT
        return "json" if self.APP_ENV.lower() == "production" else "text"


# Global settings instance for import across the project.
settings = Settings()
