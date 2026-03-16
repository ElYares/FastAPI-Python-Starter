"""Persistence helpers for refresh token lifecycle management."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.db_refresh_token import DBRefreshToken


class RefreshTokenRepository:
    """Repository for storing, revoking, and rotating refresh tokens."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_token(
        self,
        user_id: int,
        token_jti: str,
        token_hash: str,
        expires_at: datetime,
    ) -> DBRefreshToken:
        """Create and persist a refresh token record."""
        token = DBRefreshToken(
            user_id=user_id,
            token_jti=token_jti,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def get_by_jti(self, token_jti: str) -> DBRefreshToken | None:
        """Return a refresh token record by JTI."""
        stmt = select(DBRefreshToken).where(DBRefreshToken.token_jti == token_jti)
        return self.db.execute(stmt).scalars().first()

    def revoke_and_replace(self, token: DBRefreshToken, replaced_by_jti: str) -> DBRefreshToken:
        """Revoke a token and store the successor token JTI."""
        token.revoked_at = datetime.now(UTC)
        token.replaced_by_jti = replaced_by_jti
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token
