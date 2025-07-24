from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.config import settings

# Define el esquema oauth2 para obtener el token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Valida y decodifica el token JWT para obtener el usuario actual

    Args:
        token: Token JWT extraido de la cabecera

    Returns:
        str: NOmbre del usuario contenido en el token

    Raises:
        HTTPException: si el token no es valido o esta mal formado
    """

    try:
        payload = jwt.decode(token, "secret", algorithms=settings.JWT_ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalido")
        return username

    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido")
