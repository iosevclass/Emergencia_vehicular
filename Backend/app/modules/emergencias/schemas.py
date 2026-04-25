from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EmergenciaCreate(BaseModel):
    id_vehiculo: int
    ubicacion_real: str
    descripcion: str
    prioridad: str = "alta" # Opcional
    fotos: Optional[List[str]] = None

class EmergenciaResponse(BaseModel):
    nro: int
    ubicacion_real: str
    descripcion: str
    prioridad: str
    estado: str
    fotos: Optional[List[str]] = None
    fecha_creacion: datetime
    id_vehiculo: int
    id_taller: Optional[int] = None
    id_personal: Optional[int] = None

    class Config:
        from_attributes = True

class AceptarEmergenciaRequest(BaseModel):
    id_personal: int

class EstadoUpdateRequest(BaseModel):
    estado: str