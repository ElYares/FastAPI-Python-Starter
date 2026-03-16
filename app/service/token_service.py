"""Token orchestration service (access + refresh with rotation/revocation)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from jose import JWTError
from sqlalchemy.orm import Session

from app.exceptions import UnauthorizedException
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.service.auth_service import AuthService
from app.shemas.user_shema import TokenResponse


class TokenService:
    """Issue and rotate token pairs backed by refresh-token persistence."""

    def __init__(self, db: Session) -> None:
        self.auth = AuthService()
        self.user_repo = UserRepository(db)
        self.refresh_repo = RefreshTokenRepository(db)

    def issue_token_pair(self, user_id: int) -> TokenResponse:
        """Create an access token and a persisted refresh token for a user."""
        access_token = self.auth.create_access_token({"sub": str(user_id)})

        refresh_jti = uuid4().hex
        refresh_token = self.auth.create_refresh_token(user_id=user_id, token_jti=refresh_jti)
        refresh_payload = self.auth.decode_token(refresh_token)

        exp_unix = refresh_payload.get("exp")
        if not isinstance(exp_unix, int):
            raise UnauthorizedException("Refresh token inválido")

        self.refresh_repo.create_token(
            user_id=user_id,
            token_jti=refresh_jti,
            token_hash=self.auth.hash_token(refresh_token),
            expires_at=datetime.fromtimestamp(exp_unix, tz=UTC),
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    def rotate_refresh_token(self, refresh_token: str) -> TokenResponse:
        """Validate and rotate a refresh token, returning a new token pair."""
        try:
            payload = self.auth.decode_token(refresh_token)
        except JWTError as err:
            raise UnauthorizedException("Refresh token inválido o expirado") from err

        if payload.get("type") != "refresh":
            raise UnauthorizedException("Token no es de tipo refresh")

        sub = payload.get("sub")
        jti = payload.get("jti")
        if not isinstance(sub, str) or not isinstance(jti, str):
            raise UnauthorizedException("Refresh token inválido")

        try:
            user_id = int(sub)
        except ValueError as err:
            raise UnauthorizedException("Refresh token inválido") from err

        stored = self.refresh_repo.get_by_jti(jti)
        if stored is None:
            raise UnauthorizedException("Refresh token revocado o no reconocido")

        if stored.revoked_at is not None:
            raise UnauthorizedException("Refresh token ya fue revocado")

        expires_at = stored.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)

        if expires_at <= datetime.now(UTC):
            raise UnauthorizedException("Refresh token expirado")

        if stored.token_hash != self.auth.hash_token(refresh_token):
            raise UnauthorizedException("Refresh token inválido")

        user = self.user_repo.get_by_id(user_id)
        if user is None or not user.is_active:
            raise UnauthorizedException("Usuario no autorizado")

        new_jti = uuid4().hex
        new_refresh_token = self.auth.create_refresh_token(user_id=user.id, token_jti=new_jti)
        new_payload = self.auth.decode_token(new_refresh_token)
        new_exp_unix = new_payload.get("exp")
        if not isinstance(new_exp_unix, int):
            raise UnauthorizedException("Refresh token inválido")

        self.refresh_repo.revoke_and_replace(stored, replaced_by_jti=new_jti)
        self.refresh_repo.create_token(
            user_id=user.id,
            token_jti=new_jti,
            token_hash=self.auth.hash_token(new_refresh_token),
            expires_at=datetime.fromtimestamp(new_exp_unix, tz=UTC),
        )

        new_access_token = self.auth.create_access_token({"sub": str(user.id)})
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )
