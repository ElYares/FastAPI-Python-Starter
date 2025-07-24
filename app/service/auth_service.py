from datetime import datetime, timedelta
from jose import jwt
from app.config import settings

class AuthService:
    """
    Servicio encargado de generar y verificar JWTs.
    """

    def create_access_token(self, data: dict) -> str:
        """
        Genera un JWT usando los datos y tiempo de expiracion
        """

        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, "secret", algorithm=settings.JWT_ALGORITHM)
        return  encoded_jwt

