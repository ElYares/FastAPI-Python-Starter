"""
User service (business layer).

Contains business rules and user use-cases, orchestrating:
- persistence via UserRepository
- security utilities via AuthService (password hashing)

The service should not implement raw SQL or DB session lifecycle management.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.exceptions import BadRequestException
from app.logger import logger
from app.repositories.user_repository import UserRepository
from app.service.auth_service import AuthService
from app.exceptions import BadRequestException

class UserService:
    """
    Service responsible for user-related business operations.

    Args:
        db: SQLAlchemy session scoped to the current request.
    """

    def __init__(self, db: Session) -> None:
        self.repo = UserRepository(db)
        self.auth = AuthService()
        logger.info("UserService initialized (db-backed)")

    def list_users(self):
        """
        Return all users from the repository.

        Returns:
            list[DBUser]: ORM user objects.
        """
        logger.info("UserService.list_users() called")
        return self.repo.list_users()

    def register_user(self, email: str, password: str, full_name: str | None = None):
        """
        Register a new user in the database.

        Business rules:
            - Email must be unique.
            - Password is stored as a bcrypt hash (never store plaintext).

        Args:
            email: Unique email address.
            password: Plaintext password provided by the user.
            full_name: Optional full name.

        Raises:
            BadRequestException: If the email is already registered.

        Returns:
            DBUser: Newly created ORM user.
        """
        existing = self.repo.get_by_email(email)
        if existing is not None:
            raise BadRequestException("El email ya está registrado")

        hashed_password = self.auth.hash_password(password)

        user = self.repo.create_user(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
        )

        logger.info("User registered successfully: user_id=%s email=%s", user.id, user.email)
        return user

    def authenticate_user(self, email:str, password:str):
        """
        Authenticate a user by and password.

        Args:
            email: User email.
            password: User password.

        Raises:
            BadRequestException: If the email is not found or the password is invalid.

        Returns:
            DBUser | None: Authenticated user if found; otherwise None.
        """

        user = self.repo.get_by_email(email)
        if user is None:
            raise BadRequestException("Credenciales inválidas")
        
        if not self.auth.verify_password(password, user.hashed_password):
            raise BadRequestException("Credenciales inválidas")
        
        # Track last login
        self.repo.update_last_login(user)
        return user
