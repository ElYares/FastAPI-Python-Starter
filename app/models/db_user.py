"""
Database models for the application.

This module contains SQLAlchemy ORM models that map directly to database tables.
These models represent the persistence layer (DB schema) and are separate from
Pydantic schemas (transport layer) and domain models (business layer).
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.dependencies.db import Base


class DBUser(Base):
    """
    SQLAlchemy ORM model for the `users` table.

    This model stores authentication-related user data such as:
    - Unique email identifier
    - Hashed password (never store raw passwords)
    - Basic profile info
    - Activity flags and timestamps

    Notes:
        - `created_at` is generated at the database level using `func.now()`.
        - `last_login_at` is updated after successful authentication.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
