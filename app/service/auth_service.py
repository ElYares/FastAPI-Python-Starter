"""
Authentication service (business layer).

Provides:
- JWT token generation
- Password hashing and verification

This module does not perform database access directly; it is used by services
that orchestrate repository calls.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Service responsible for authentication-related utilities.

    Responsibilities:
        - Create JWT access tokens
        - Hash and verify passwords using bcrypt
    """

    def hash_password(self, password: str) -> str:
        """
        Hash a plaintext password using bcrypt.

        Args:
            password: Plaintext password provided by the user.

        Returns:
            str: Secure bcrypt hash to be stored in the database.
        """

        if not password:
            raise ValueError("Password is required")

        # bcrypt only considers the first 72 bytes; longer inputs must be rejected to avoid ambiguity.
        if len(password.encode("utf-8")) > 72:
            raise ValueError("Password is too long")
        return _pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a plaintext password against a stored bcrypt hash.

        Args:
            password: Plaintext password.
            hashed_password: Stored bcrypt hash.

        Returns:
            bool: True if password matches the hash; otherwise False.
        """
        return _pwd_context.verify(password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        """
        Create a JWT access token.

        Args:
            data: Payload data to encode in the token (e.g., {"sub": "<user_id>"}).

        Returns:
            str: Encoded JWT token.
        """
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        return jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
