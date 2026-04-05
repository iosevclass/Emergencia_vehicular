from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.core.database import get_db
from .models import Taller, UserRole
from .schemas import TallerCreate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #como que este no es necesario
#Lo importare desde security.py para evitar duplicación de código
from app.core.security import pwd_context



#IMPORTS NUEVOS JOSE
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.core.security import create_access_token, verify_password

from .models import Usuario
from .schemas import LoginRequest, TokenResponse, UsuarioResponse
from .services import authenticate_user
from fastapi.security import OAuth2PasswordBearer


#es un descriptor que le dice a FastAPI donde pedir el token en este caso el endpoint /login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

@router.post("/register-taller", status_code=status.HTTP_201_CREATED)
def register_taller(obj_in: TallerCreate, db: Session = Depends(get_db)):
    # ... validación de existencia ...

    nuevo_taller = Taller(
        email=obj_in.email,
        password_hash=pwd_context.hash(obj_in.password),
        rol=UserRole.ADMIN_TALLER,
        tipo_perfil="taller", # Mantén esta línea para la herencia polimórfica
        nombre_taller=obj_in.nombre_taller, # Ahora coinciden ambos lados
        nit=obj_in.nit,
        ciudad=obj_in.ciudad,
        direccion=obj_in.direccion
    )
    
    try:
        db.add(nuevo_taller)
        db.commit()
        db.refresh(nuevo_taller)
        
        # Opcional: Registrar actividad en la bitácora usando tu service
        # registrar_actividad(db, nuevo_taller.id, "Registro de taller nuevo")
        
        return {"message": "Taller registrado", "id": nuevo_taller.id}
    except Exception as e:
        db.rollback() # Siempre haz rollback si falla el commit
        print(f"ERROR REAL: {e}") # Mira esto en la terminal de VS Code
        raise HTTPException(status_code=500, detail=str(e))
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Valida el token JWT y devuelve el usuario.
    Se ejecuta automáticamente cuando un endpoint la usa como Depends.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado - token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica el token JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        user_id: str = payload.get("sub")  # Extrae el user_id del token
        if user_id is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    # Busca el usuario en la BD
    user = db.query(Usuario).filter(Usuario.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica usuario (email + contraseña) y genera token JWT.
    """
    # Llama a authenticate_user de services.py
    user = authenticate_user(db, request.email, request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crea el token con datos del usuario
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "rol": user.rol.value}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UsuarioResponse)
def read_users_me(current_user: Usuario = Depends(get_current_user)):
    """
    Devuelve datos del usuario autenticado.
    Requiere token JWT válido en header Authorization.
    """
    return current_user



'''┌─ IMPORTS (todo arriba)
├─ router = APIRouter(...)
├─ oauth2_scheme = OAuth2PasswordBearer(...)
│
├─ @router.post("/register-taller")   ← YA EXISTE
│  def register_taller():
│      ...
│
├─ def get_current_user():  ← NUEVO - función auxiliar
│      ...
│
├─ @router.post("/login")   ← NUEVO
│  def login():
│      ...
│
└─ @router.get("/me")       ← NUEVO
   def read_users_me():
       ...
'''