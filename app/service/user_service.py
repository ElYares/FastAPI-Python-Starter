"""
User service (business layer).

This module contains business logic related to users and orchestrates calls
between API routes and the repository layer.

Guidelines:
- The service enforces business rules and validations.
- Persistence details are delegated to the repository.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.logger import logger
from app.repositories.user_repository import UserRepository


class UserService:
    """
    Service responsible for user-related use cases.

    Args:
        db: SQLAlchemy session for the current request.

    Notes:
        - This service is designed to be instantiated per request to avoid
          sharing state across requests.
    """

    def __init__(self, db: Session) -> None:
        self.repo = UserRepository(db)
        logger.info("UserService initialized (db-backed)")

    def list_users(self):
        """
        List users.

        Returns:
            list[DBUser]: ORM user objects from the repository.
        """
        logger.info("UserService.list_users() called")
        return self.repo.list_users()
