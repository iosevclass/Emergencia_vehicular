from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.auth import get_current_user
from app.modules.usuarios.models import Usuario, UserRole, PersonalTaller
from app.modules.emergencias import models, schemas
from app.modules.vehiculos.models import Vehiculo
from app.modules.emergencias.websockets import manager

router = APIRouter(prefix="/emergencias", tags=["emergencias"])

# ---- WEBSOCKETS ----
@router.websocket("/ws/taller")
async def websocket_taller(websocket: WebSocket):
    await manager.connect_taller(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_taller(websocket)

@router.websocket("/ws/cliente/{client_id}")
async def websocket_cliente(websocket: WebSocket, client_id: int):
    await manager.connect_client(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_client(client_id)

@router.get("/espera", response_model=List[schemas.EmergenciaResponse])
def get_emergencias_espera(db: Session = Depends(get_db)):
    # Los talleres consultan las emergencias que están esperando
    return db.query(models.Emergencia).filter(models.Emergencia.estado == models.EstadoEmergencia.espera).all()

@router.get("/taller", response_model=List[schemas.EmergenciaResponse])
def get_emergencias_taller(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.rol.value not in ["admin_taller", "personal_taller"]:
        raise HTTPException(status_code=403, detail="Solo taller puede ver su historial")
    
    taller_id = current_user.id
    if current_user.rol.value == "personal_taller":
        personal = db.query(PersonalTaller).filter(PersonalTaller.id == current_user.id).first()
        if personal:
            taller_id = personal.taller_id

    return db.query(models.Emergencia).filter(models.Emergencia.id_taller == taller_id).order_by(models.Emergencia.fecha_creacion.desc()).all()

@router.get("/cliente", response_model=List[schemas.EmergenciaResponse])
def get_emergencias_cliente(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.rol.value != "cliente":
        raise HTTPException(status_code=403, detail="Solo clientes pueden ver su historial")
    
    return db.query(models.Emergencia).join(Vehiculo).filter(Vehiculo.cliente_id == current_user.id).order_by(models.Emergencia.fecha_creacion.desc()).all()

# ---- ENDPOINTS ----
@router.post("/", response_model=schemas.EmergenciaResponse)
async def create_emergencia(emergencia: schemas.EmergenciaCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.rol.value != "cliente":
        raise HTTPException(status_code=403, detail="Solo clientes pueden solicitar emergencias")
        
    # Validar que el vehiculo le pertenece
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == emergencia.id_vehiculo, Vehiculo.cliente_id == current_user.id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado o no pertenece al cliente")

    db_emergencia = models.Emergencia(
        id_vehiculo=emergencia.id_vehiculo,
        ubicacion_real=emergencia.ubicacion_real,
        descripcion=emergencia.descripcion,
        prioridad=emergencia.prioridad,
        fotos=emergencia.fotos
    )
    db.add(db_emergencia)
    db.commit()
    db.refresh(db_emergencia)
    
    # Broadcast a todos los talleres
    await manager.broadcast_to_talleres({
        "type": "NEW_EMERGENCY",
        "data": {
            "nro": db_emergencia.nro,
            "ubicacion_real": db_emergencia.ubicacion_real,
            "descripcion": db_emergencia.descripcion,
            "fotos": db_emergencia.fotos,
            "vehiculo": f"{vehiculo.marca} {vehiculo.modelo} ({vehiculo.placa})"
        }
    })
    
    return db_emergencia

@router.get("/espera", response_model=List[schemas.EmergenciaResponse])
def get_emergencias_espera(db: Session = Depends(get_db)):
    # Los talleres consultan las emergencias que están esperando
    return db.query(models.Emergencia).filter(models.Emergencia.estado == models.EstadoEmergencia.espera).all()

@router.post("/{nro}/aceptar", response_model=schemas.EmergenciaResponse)
async def aceptar_emergencia(nro: int, req: schemas.AceptarEmergenciaRequest, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.rol.value not in ["admin_taller", "personal_taller"]:
        raise HTTPException(status_code=403, detail="Solo taller puede aceptar")

    emergencia = db.query(models.Emergencia).filter(models.Emergencia.nro == nro).first()
    if not emergencia:
        raise HTTPException(status_code=404, detail="Emergencia no encontrada")
    if emergencia.estado != models.EstadoEmergencia.espera:
        raise HTTPException(status_code=400, detail="Emergencia ya no está en espera")

    # --- NUEVO: Descubrir de qué taller es el usuario actual ---
    taller_id = current_user.id
    if current_user.rol.value == "personal_taller":
        personal = db.query(PersonalTaller).filter(PersonalTaller.id == current_user.id).first()
        if personal:
            taller_id = personal.taller_id
            
    # Asignamos la emergencia a este taller
    emergencia.id_taller = taller_id 
    # -----------------------------------------------------------

    emergencia.id_personal = req.id_personal
    emergencia.estado = models.EstadoEmergencia.atendiendo
    db.commit()
    db.refresh(emergencia)

    # Notificar al cliente
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == emergencia.id_vehiculo).first()
    if vehiculo:
        await manager.send_to_client(vehiculo.cliente_id, {
            "type": "STATUS_UPDATE",
            "data": {
                "nro": emergencia.nro,
                "estado": "atendiendo"
            }
        })

    return emergencia

@router.post("/{nro}/completar", response_model=schemas.EmergenciaResponse)
async def completar_emergencia(nro: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.rol.value not in ["admin_taller", "personal_taller"]:
        raise HTTPException(status_code=403, detail="Solo taller puede completar")

    emergencia = db.query(models.Emergencia).filter(models.Emergencia.nro == nro).first()
    if not emergencia:
        raise HTTPException(status_code=404, detail="Emergencia no encontrada")

    emergencia.estado = models.EstadoEmergencia.terminado
    db.commit()
    db.refresh(emergencia)

    # Notificar al cliente
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == emergencia.id_vehiculo).first()
    if vehiculo:
        await manager.send_to_client(vehiculo.cliente_id, {
            "type": "STATUS_UPDATE",
            "data": {
                "nro": emergencia.nro,
                "estado": "terminado"
            }
        })

    return emergencia

@router.patch("/{nro}/estado", response_model=schemas.EmergenciaResponse)
async def actualizar_estado_generico(nro: int, req: schemas.EstadoUpdateRequest, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.rol.value not in ["admin_taller", "personal_taller"]:
        raise HTTPException(status_code=403, detail="Solo el taller puede cambiar el estado")

    emergencia = db.query(models.Emergencia).filter(models.Emergencia.nro == nro).first()
    if not emergencia:
        raise HTTPException(status_code=404, detail="Emergencia no encontrada")

    emergencia.estado = req.estado
    
    # --- NUEVO: Si cambian el estado a atendiendo por aquí, aseguramos que tenga id_taller ---
    if req.estado == "atendiendo" and emergencia.id_taller is None:
        taller_id = current_user.id
        if current_user.rol.value == "personal_taller":
            personal = db.query(PersonalTaller).filter(PersonalTaller.id == current_user.id).first()
            if personal:
                taller_id = personal.taller_id
        
        emergencia.id_taller = taller_id
        if current_user.rol.value == "personal_taller":
            emergencia.id_personal = current_user.id
    # -----------------------------------------------------------------------------------------

    db.commit()
    db.refresh(emergencia)

    # Notificar al cliente vía WebSocket que su estado cambió
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == emergencia.id_vehiculo).first()
    if vehiculo:
        await manager.send_to_client(vehiculo.cliente_id, {
            "type": "STATUS_UPDATE",
            "data": {
                "nro": emergencia.nro,
                "estado": req.estado
            }
        })

    return emergencia