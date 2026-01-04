"""
User repository implementation (persistence layer).

This module encapsulates database access for user entities using SQLAlchemy.
The repository is responsible only for persistence concerns:
- querying
- inserting
- returning ORM objects

Business rules (e.g., validation, password rules) must remain in the Service layer.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.db_user import DBUser


class UserRepository:
    """
    Repository for user persistence operations.

    Args:
        db: SQLAlchemy session used for all repository operations.

    Notes:
        - The session lifecycle is managed by FastAPI dependency `get_db()`.
        - This repository returns ORM instances (`DBUser`) and does not perform
          any serialization. Pydantic schemas handle response serialization.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(self, email: str, hashed_password: str, full_name: str | None = None) -> DBUser:
        """
        Persist a new user in the database.

        Args:
            email: Unique email.
            hashed_password: bcrypt hashed password.
            full_name: Optional full name.

        Returns:
            DBUser: Created ORM user.
        """
        user = DBUser(email=email, hashed_password=hashed_password, full_name=full_name)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def list_users(self) -> list[DBUser]:
        """
        Fetch all users ordered by ascending ID.

        Returns:
            list[DBUser]: List of users from the database.
        """
        stmt = select(DBUser).order_by(DBUser.id.asc())
        return list(self.db.execute(stmt).scalars().all())

    def get_by_email(self, email: str) -> DBUser | None:
        """
        Fetch a user by email.

        Args:
            email: User email.

        Returns:
            DBUser | None: User if found; otherwise None.
        """
        stmt = select(DBUser).where(DBUser.email == email)
        return self.db.execute(stmt).scalars().first()

    def get_by_id(self, user_id: int) -> DBUser | None:
        """
        Fetch a user by primary key ID.

        Args:
            user_id: User ID.

        Returns:
            DBUser | None: User if found; otherwise None.
        """
        return self.db.get(DBUser, user_id)
