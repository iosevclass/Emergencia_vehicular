from datetime import datetime, timedelta, timezone # timezone es clave
from typing import Optional
import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Configuramos el contexto de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    # Usamos timezone.utc para evitar líos con la hora del servidor
    now = datetime.now(timezone.utc)
    
    if expires_delta:
        expire = now + expires_delta
    else:
        # Usamos el valor que definiste en tus settings
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Firmamos el token con la llave secreta y el algoritmo (HS256)
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    """Compara contraseña plana vs hash de la DB"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Crea el hash para guardar en la DB"""
    return pwd_context.hash(password)