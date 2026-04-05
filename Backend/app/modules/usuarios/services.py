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

def authenticate_user(db: Session, email: str, password: str):
    # Lógica para autenticar al usuario y generar token
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

