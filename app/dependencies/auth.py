"""
Authentication dependencies.

This module provides reusable dependencies for protected routes, including:
- extracting the bearer token (OAuth2)
- decoding JWT
- loading the current user from the database
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.config import settings
from app.dependencies.db import get_db
from app.models.db_user import DBUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> DBUser:
    """
    Decode the JWT token and load the current user from the database.

    Args:
        db: Request-scoped SQLAlchemy session.
        token: Bearer token extracted from the Authorization header.

    Raises:
        HTTPException: If token is invalid/expired, user not found, or inactive.

    Returns:
        DBUser: Authenticated user ORM instance.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        sub = payload.get("sub")
        if not sub:
            raise credentials_exception

        try:
            user_id = int(sub)
        except (TypeError, ValueError):
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.get(DBUser, user_id)
    if user is None or not user.is_active:
        raise credentials_exception

    return user