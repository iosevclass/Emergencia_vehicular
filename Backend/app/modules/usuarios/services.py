# app/modules/usuarios/services.py
from sqlalchemy.orm import Session
from .models import Usuario
from app.core.security import verify_password
'''def registrar_actividad(db: Session, usuario_id: int, accion: str):
    """Función global para alimentar la bitácora de actividad"""
    nueva_actividad = Bitacora(usuario_id=usuario_id, accion=accion)
    db.add(nueva_actividad)
    db.commit()
'''
def crear_usuario_taller(db: Session, datos_taller: dict):
    # Lógica para crear el usuario y su perfil de taller
    # Luego llamar a registrar_actividad...
    pass

from .models import Usuario, PersonalTaller, UserRole
from app.core.security import verify_password, get_password_hash
from .schemas import PersonalTallerCreate, PersonalTallerUpdate

def authenticate_user(db: Session, email: str, password: str):
    # ... código existente ...
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

# --- CRUD PERSONAL TALLER ---

def get_personal_by_id(db: Session, personal_id: int):
    return db.query(PersonalTaller).filter(PersonalTaller.id == personal_id).first()

def get_personal_by_taller(db: Session, taller_id: int):
    """Obtiene todo el personal vinculado a un taller específico"""
    return db.query(PersonalTaller).filter(PersonalTaller.taller_id == taller_id).all()

def create_personal_taller(db: Session, obj_in: PersonalTallerCreate, taller_id: int):
    """
    Crea un nuevo personal de taller. 
    Se le asigna automáticamente el taller_id del administrador que lo crea.
    """
    nuevo_personal = PersonalTaller(
        email=obj_in.email,
        password_hash=get_password_hash(obj_in.password),
        rol=UserRole.PERSONAL_TALLER,
        tipo_perfil="personal_taller",
        nombre_completo=obj_in.nombre_completo,
        cargo=obj_in.cargo,
        especialidad=obj_in.especialidad,
        foto_perfil=obj_in.foto_perfil,
        taller_id=taller_id
    )
    
    db.add(nuevo_personal)
    db.commit()
    db.refresh(nuevo_personal)
    return nuevo_personal

def update_personal_taller(db: Session, db_obj: PersonalTaller, obj_in: PersonalTallerUpdate):
    """Actualización parcial de los datos del personal"""
    update_data = obj_in.model_dump(exclude_unset=True)
    
    if update_data.get("password"):
        db_obj.password_hash = get_password_hash(update_data["password"])
        del update_data["password"]
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_personal_taller(db: Session, personal_id: int):
    """Borrado suave (opcional) o físico. Aquí haremos borrado físico."""
    db_obj = db.query(PersonalTaller).filter(PersonalTaller.id == personal_id).first()
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj

