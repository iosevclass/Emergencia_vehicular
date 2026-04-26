import sys
import os
from sqlalchemy import text
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Configurar el path para importar app
sys.path.append(os.path.join(os.getcwd(), "Backend"))

from app.core.database import SessionLocal, engine
from app.modules.usuarios.models import Taller, Cliente, PersonalTaller, UserRole, Usuario, Administrador
from app.core.security import get_password_hash
from app.modules.vehiculos.models import Vehiculo
from app.modules.emergencias.models import Emergencia, DetalleEmergencia, Mensajeria
from app.modules.bitacora.models import Bitacora

def fix_enum():
    """Intenta añadir el valor 'ADMIN_SISTEMA' al ENUM de Postgres si no existe."""
    try:
        with engine.connect() as conn:
            # Primero intentamos añadirlo en mayúsculas que es como están los otros
            conn.execute(text("ALTER TYPE userrole ADD VALUE 'ADMIN_SISTEMA'"))
            conn.commit()
            print("✅ Valor 'ADMIN_SISTEMA' añadido al ENUM.")
    except Exception as e:
        if "already exists" in str(e):
            print("ℹ️ El valor 'ADMIN_SISTEMA' ya existe en el ENUM.")
        else:
            print(f"⚠️ Nota sobre ENUM: {e}")

def seed_database_2():
    db: Session = SessionLocal()
    try:
        # 1. Limpieza de correos específicos de este seed para poder re-ejecutarlo
        emails_test = [
            "admin@emergencia.com",
            "taller_norte@example.com",
            "taller_sur@example.com",
            "mecanico_norte1@example.com",
            "mecanico_norte2@example.com",
            "mecanico_sur1@example.com",
            "mecanico_sur2@example.com",
            "maria_cliente@example.com",
            "carlos_cliente@example.com"
        ]
        
        usuarios_viejos = db.query(Usuario).filter(Usuario.email.in_(emails_test)).all()
        ids_viejos = [u.id for u in usuarios_viejos]
        
        if ids_viejos:
            # Borrar bitacora primero por las FK
            db.query(Bitacora).filter(Bitacora.id_usuario.in_(ids_viejos)).delete(synchronize_session=False)
            db.query(Administrador).filter(Administrador.id.in_(ids_viejos)).delete(synchronize_session=False)
            db.query(PersonalTaller).filter(PersonalTaller.id.in_(ids_viejos)).delete(synchronize_session=False)
            db.query(Taller).filter(Taller.id.in_(ids_viejos)).delete(synchronize_session=False)
            db.query(Cliente).filter(Cliente.id.in_(ids_viejos)).delete(synchronize_session=False)
            db.query(Usuario).filter(Usuario.id.in_(ids_viejos)).delete(synchronize_session=False)
            db.commit()
            print("🧹 Limpieza de datos de seed 2 completada.")

        hashed_password = get_password_hash("password123")

        # 2. Crear Administrador (Usando MAYÚSCULAS para el rol)
        admin = Administrador(
            email="admin@emergencia.com",
            password_hash=get_password_hash("admin123"),
            rol="ADMIN_SISTEMA", 
            nombre_completo="Administrador General",
            tipo_perfil="admin"
        )
        db.add(admin)
        print("✅ Admin creado: admin@emergencia.com")

        # 3. Crear Taller 1 (Norte)
        taller1 = Taller(
            email="taller_norte@example.com",
            password_hash=hashed_password,
            rol="ADMIN_TALLER",
            nombre_taller="Taller Mecánico El Norte",
            telefono="70000001",
            nit="11111111",
            ciudad="Santa Cruz",
            direccion="Zona Norte, Av. Banzer",
            foto_perfil="https://res.cloudinary.com/dh8zaedgv/image/upload/v1777234606/83a5d61f-4f3d-4fde-94e9-b3a0ff222c45.png",
            latitud=-17.780987,
            longitud=-63.193755,
            tipo_perfil="taller"
        )
        db.add(taller1)
        db.flush()

        # 4. Crear Taller 2 (Sur)
        taller2 = Taller(
            email="taller_sur@example.com",
            password_hash=hashed_password,
            rol="ADMIN_TALLER",
            nombre_taller="Taller Mecánico El Sur",
            telefono="70000002",
            nit="22222222",
            ciudad="Santa Cruz",
            direccion="Zona Sur, Av. Santos Dumont",
            foto_perfil="https://res.cloudinary.com/dh8zaedgv/image/upload/v1777234795/1dbc6eda-58cd-4d02-9316-3545ee82fb44.png",
            latitud=-17.772393,
            longitud=-63.198007,
            tipo_perfil="taller"
        )
        db.add(taller2)
        db.flush()

        # 5. Crear Personal (4 en total)
        p1 = PersonalTaller(email="mecanico_norte1@example.com", password_hash=hashed_password, rol="PERSONAL_TALLER", nombre_completo="Juan Mecanico Norte", taller_id=taller1.id, cargo="Mecánico", tipo_perfil="personal_taller")
        p2 = PersonalTaller(email="mecanico_norte2@example.com", password_hash=hashed_password, rol="PERSONAL_TALLER", nombre_completo="Pedro Electricista Norte", taller_id=taller1.id, cargo="Electricista", tipo_perfil="personal_taller")
        p3 = PersonalTaller(email="mecanico_sur1@example.com", password_hash=hashed_password, rol="PERSONAL_TALLER", nombre_completo="Luis Mecanico Sur", taller_id=taller2.id, cargo="Mecánico", tipo_perfil="personal_taller")
        p4 = PersonalTaller(email="mecanico_sur2@example.com", password_hash=hashed_password, rol="PERSONAL_TALLER", nombre_completo="Jose Ayudante Sur", taller_id=taller2.id, cargo="Ayudante", tipo_perfil="personal_taller")
        db.add_all([p1, p2, p3, p4])

        # 6. Crear Clientes (2)
        c1 = Cliente(email="maria_cliente@example.com", password_hash=hashed_password, rol="CLIENTE", nombre="Maria Garcia", telefono="78888881", tipo_perfil="cliente")
        c2 = Cliente(email="carlos_cliente@example.com", password_hash=hashed_password, rol="CLIENTE", nombre="Carlos Rodriguez", telefono="78888882", tipo_perfil="cliente")
        db.add_all([c1, c2])

        db.commit()
        print("🚀 Seed 2 completado con éxito (Admin, 2 Talleres, 4 Personal, 2 Clientes).")

    except Exception as e:
        db.rollback()
        print(f"❌ Error durante el seeding 2: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_enum()
    seed_database_2()
