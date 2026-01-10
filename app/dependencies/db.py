"""
Database dependency wiring for FastAPI.

This module centralizes SQLAlchemy configuration:
- Engine creation from settings
- Session factory (SessionLocal)
- `get_db()` dependency for request-scoped sessions
- Declarative Base for ORM models

Design:
    - `get_db()` yields a session per request and guarantees cleanup.
    - SQLite requires `check_same_thread=False` for typical FastAPI usage.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

#: Declarative base used by all ORM models (e.g., DBUser).
Base = declarative_base()

# SQLite thread-safety configuration:
# FastAPI typically uses concurrency patterns that require disabling SQLite's
# same-thread restriction for web apps.
connect_args: dict[str, object] = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DB_ECHO,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)


def get_db():
    """
    Provide a SQLAlchemy session for a single request.

    Yields:
        sqlalchemy.orm.Session: An active database session.

    Notes:
        - The session is always closed after the request completes.
        - This dependency is meant to be used with `Depends(get_db)`.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
