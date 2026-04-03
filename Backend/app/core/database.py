import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Esto busca el archivo .env y carga las variables
load_dotenv()

DATABASE_URL = "postgresql://postgres:gabo2004@localhost:5432/emergencia_db"

# El motor de conexión
engine = create_engine(DATABASE_URL)

# La sesión para hacer consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# La clase base de la que heredarán todos tus modelos
Base = declarative_base()

# Dependencia para obtener la DB en las rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()