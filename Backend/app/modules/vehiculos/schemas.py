from pydantic import BaseModel
from typing import Optional

class VehiculoBase(BaseModel):
    placa: str
    marca: str
    modelo: str
    color: str
    anio: int

class VehiculoCreate(VehiculoBase):
    pass

class VehiculoResponse(VehiculoBase):
    id: int
    cliente_id: int

    class Config:
        from_attributes = True
