from pydantic import EmailStr, BaseModel
from typing import Optional

class TallerCreate(BaseModel):
    # Datos de la tabla Usuario
    email: EmailStr
    password: Optional[str] = None
    telefono: str
    
    # Datos de la tabla Taller
    nombre_taller: str
    nit: str
    ciudad: str
    direccion: str
    
    class Config:
        from_attributes = True