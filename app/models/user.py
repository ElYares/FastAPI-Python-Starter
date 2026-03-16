"""
Domain user model.

This model is intentionally decoupled from persistence (SQLAlchemy) and
transport (Pydantic schemas).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class User:
    """Represent a user in the business domain layer."""

    id: int
    name: str
