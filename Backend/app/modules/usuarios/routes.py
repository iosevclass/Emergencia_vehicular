from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.core.database import get_db
from .models import Taller, UserRole
from .schemas import TallerCreate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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