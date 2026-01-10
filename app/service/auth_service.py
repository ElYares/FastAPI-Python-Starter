from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import settings


class AuthService:
    """
    Servicio encargado de generar JWTs.
    """

    def create_access_token(self, data: dict) -> str:
        """
        Genera un JWT usando los datos y tiempo de expiracion
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        return jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
