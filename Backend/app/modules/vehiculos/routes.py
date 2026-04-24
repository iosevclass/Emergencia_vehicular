from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.modules.vehiculos import schemas, models
from app.api.auth import get_current_user
from app.modules.usuarios.models import Usuario, Cliente

router = APIRouter(prefix="/vehiculos", tags=["vehiculos"])

@router.post("/", response_model=schemas.VehiculoResponse)
def create_vehiculo(vehiculo: schemas.VehiculoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    # Solo clientes pueden registrar vehículos
    if current_user.rol.value != "cliente":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo clientes pueden registrar vehículos")
    
    # Check if placa exists
    existing = db.query(models.Vehiculo).filter(models.Vehiculo.placa == vehiculo.placa).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un vehículo con esa placa")
        
    db_vehiculo = models.Vehiculo(
        placa=vehiculo.placa,
        marca=vehiculo.marca,
        modelo=vehiculo.modelo,
        color=vehiculo.color,
        anio=vehiculo.anio,
        cliente_id=current_user.id
    )
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

@router.get("/mis-vehiculos", response_model=List[schemas.VehiculoResponse])
def get_mis_vehiculos(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.rol.value != "cliente":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo clientes tienen vehículos")
        
    vehiculos = db.query(models.Vehiculo).filter(models.Vehiculo.cliente_id == current_user.id).all()
    return vehiculos
