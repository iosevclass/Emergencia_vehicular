# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from passlib.context import CryptContext
# Cambia esta línea:
from app.modules.usuarios.models import Taller, UserRole
# Asegúrate de que el esquema también apunte al lugar correcto:
from app.modules.usuarios.schemas import TallerCreate

router = APIRouter(prefix="/auth", tags=["auth"])

# Configuramos el hasheador de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register-taller")
def register_taller(obj_in: TallerCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el usuario ya existe por email
    user_exists = db.query(Taller).filter(Taller.email == obj_in.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El email ya está registrado"
        )

    # 2. Instanciar el modelo Taller con los datos del Front
    # Nota: password_hash se guarda encriptado
    nuevo_taller = Taller(
        email=obj_in.email,
        password_hash=pwd_context.hash(obj_in.password),
        rol=UserRole.ADMIN_TALLER, # Asignamos el rol del Enum
        nombre_comercial=obj_in.nombre_taller,
        nit=obj_in.nit,
        ciudad=obj_in.ciudad,
        direccion=obj_in.direccion,
        # telefono=obj_in.telefono  <- Asegúrate de tener este campo en tu modelo Cliente o Usuario
    )

    try:
        db.add(nuevo_taller)
        db.commit() # Guarda en ambas tablas (usuarios y perfil_talleres)
        db.refresh(nuevo_taller)
        return {"status": "success", "message": "Taller creado", "id": nuevo_taller.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar: {str(e)}")