# app/modules/usuarios/services.py
from sqlalchemy.orm import Session
from .models import Usuario, Bitacora

def registrar_actividad(db: Session, usuario_id: int, accion: str):
    """Función global para alimentar la bitácora de actividad"""
    nueva_actividad = Bitacora(usuario_id=usuario_id, accion=accion)
    db.add(nueva_actividad)
    db.commit()

def crear_usuario_taller(db: Session, datos_taller: dict):
    # Lógica para crear el usuario y su perfil de taller
    # Luego llamar a registrar_actividad...
    pass