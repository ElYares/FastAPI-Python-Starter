"""
Authentication service (business layer).

Provides:
- JWT token generation
- Password hashing and verification

This module does not perform database access directly; it is used by services
that orchestrate repository calls.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from hashlib import sha256
from uuid import uuid4

import bcrypt
from jose import jwt

from app.config import settings


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

        # bcrypt only considers the first 72 bytes.
        # Reject longer inputs to avoid ambiguity.
        if len(password.encode("utf-8")) > 72:
            raise ValueError("Password is too long")
        password_bytes = password.encode("utf-8")
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed_bytes.decode("utf-8")

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a plaintext password against a stored bcrypt hash.

        Args:
            password: Plaintext password.
            hashed_password: Stored bcrypt hash.

        Returns:
            bool: True if password matches the hash; otherwise False.
        """
        password_bytes = password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")
        try:
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except ValueError:
            return False

    def create_access_token(self, data: dict) -> str:
        """
        Create a JWT access token.

        Args:
            data: Payload data to encode in the token (e.g., {"sub": "<user_id>"}).

        Returns:
            str: Encoded JWT token.
        """
        to_encode = data.copy()
        to_encode.update({"type": "access"})
        return self._encode_token(to_encode, settings.JWT_EXPIRE_MINUTES)

    def create_refresh_token(self, user_id: int, token_jti: str | None = None) -> str:
        """
        Create a refresh token with token type and JTI.

        Args:
            user_id: User ID owning the token.
            token_jti: Optional unique token identifier. Generated if omitted.

        Returns:
            str: Encoded refresh JWT token.
        """
        jti = token_jti or uuid4().hex
        payload = {
            "sub": str(user_id),
            "jti": jti,
            "type": "refresh",
        }
        return self._encode_token(payload, settings.JWT_REFRESH_EXPIRE_MINUTES)

    def decode_token(self, token: str) -> dict:
        """
        Decode and validate a JWT token.

        Args:
            token: Encoded JWT string.

        Raises:
            JWTError: If token is invalid or expired.

        Returns:
            dict: Decoded payload.
        """
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

    @staticmethod
    def hash_token(token: str) -> str:
        """Return a stable SHA-256 hex digest for secure token storage."""
        return sha256(token.encode("utf-8")).hexdigest()

    def _encode_token(self, payload: dict, expires_minutes: int) -> str:
        """Encode a JWT payload with UTC expiration and issued-at claims."""
        now = datetime.now(UTC)
        to_encode = payload.copy()
        to_encode.update(
            {
                "iat": now,
                "exp": now + timedelta(minutes=expires_minutes),
            }
        )
        return jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
