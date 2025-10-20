"""
Sistema de autenticación JWT para Campo Sagrado
Implementa tokens seguros con expiración
"""

from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

# Configuración
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CHANGE_THIS_IN_PRODUCTION_TO_RANDOM_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT token con los datos proporcionados.
    
    Args:
        data: Diccionario con los claims del token (user_id, email, etc.)
        expires_delta: Tiempo de expiración personalizado
    
    Returns:
        Token JWT como string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """
    Verifica y decodifica un JWT token.
    
    Args:
        credentials: Credenciales HTTP Bearer del header
    
    Returns:
        Payload del token decodificado
    
    Raises:
        HTTPException: Si el token es inválido o ha expirado
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Verificar que no haya expirado
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_token_optional(credentials: Optional[HTTPAuthorizationCredentials] = Security(security, auto_error=False)) -> Optional[dict]:
    """
    Verifica token pero no falla si no está presente (para endpoints opcionales).
    
    Returns:
        Payload del token o None si no hay token
    """
    if credentials is None:
        return None
    
    try:
        return verify_token(credentials)
    except HTTPException:
        return None


def generate_api_key() -> str:
    """
    Genera una API key aleatoria para integraciones.
    
    Returns:
        API key segura de 32 caracteres
    """
    import secrets
    return secrets.token_urlsafe(32)


# Función helper para crear usuario de prueba (solo desarrollo)
def create_dev_token() -> str:
    """
    Crea un token de desarrollo para testing.
    Solo usar en desarrollo, NUNCA en producción.
    """
    if os.getenv("ENV") == "production":
        raise ValueError("❌ No usar tokens de desarrollo en producción")
    
    return create_access_token({
        "user_id": "dev_user",
        "email": "dev@campo-sagrado.local",
        "type": "development"
    })


# Modo de desarrollo: permitir acceso sin auth
def is_dev_mode() -> bool:
    """Verifica si estamos en modo desarrollo."""
    return os.getenv("ENV", "development") == "development"


def require_auth_in_production(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Requiere autenticación solo en producción.
    En desarrollo, permite acceso libre.
    """
    if is_dev_mode():
        # En desarrollo, crear token virtual
        return {
            "user_id": "dev_user",
            "email": "dev@campo-sagrado.local",
            "type": "development"
        }
    else:
        # En producción, verificar token real
        return verify_token(credentials)

