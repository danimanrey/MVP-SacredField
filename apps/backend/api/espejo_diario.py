"""
🪞 API - Espejo Diario
======================

Endpoints para obtener y actualizar el Espejo Diario en tiempo real.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

from models.database import get_db, EstadoCeroDB
from models.schemas import JornadaAlBordeCaos, RespuestaSacral
from agentes.orquestador import AgenteOrquestador
from agentes.entrelazador import agente_entrelazador
from services.claude_client import ClaudeClient
from services.tiempos_liturgicos import CalculadorTiemposLiturgicos
from services.contexto import RecopiladorContexto
from services.calendario_hijri import CalendarioHijri
import os
import json


router = APIRouter()

# Servicios
LAT = float(os.getenv("LATITUD", "40.4168"))
LON = float(os.getenv("LONGITUD", "-3.7038"))
TZ = os.getenv("TIMEZONE", "Europe/Madrid")

calculador = CalculadorTiemposLiturgicos(LAT, LON, TZ)
calendario = CalendarioHijri()
claude_client = ClaudeClient()

# Plan del día actual (en memoria)
plan_dia_actual: Optional[JornadaAlBordeCaos] = None


class ActualizarEspejoRequest(BaseModel):
    """Request para actualizar espejo con Estado Cero"""
    estado_cero_id: str
    direccion_emergente: str
    momento: str


@router.get("/hoy", response_model=JornadaAlBordeCaos)
async def obtener_espejo_hoy(db: Session = Depends(get_db)):
    """
    Obtiene el Espejo Diario de hoy.
    
    Si no existe, lo crea basándose en:
    - Ritual Maghrib de ayer (si existe)
    - O estructura base del día
    """
    
    global plan_dia_actual
    
    # Si ya existe en memoria
    if plan_dia_actual and plan_dia_actual.fecha == date.today():
        return plan_dia_actual
    
    # Si no existe, generar estructura base
    tiempos_hoy = calculador.calcular_tiempos_hoy()
    
    if agente_entrelazador.perfil_usuario:
        estructura = agente_entrelazador.generar_estructura_dia(
            date.today(),
            tiempos_hoy
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Perfil no configurado. Configure su perfil primero."
        )
    
    # Generar plan base
    recopilador = RecopiladorContexto(db, calculador, calendario)
    orquestador = AgenteOrquestador(db, claude_client, calculador)
    
    momento_actual = calculador.momento_actual()
    contexto = await recopilador.recopilar_contexto_completo(momento_actual)
    
    plan = await orquestador.generar_plan_dia_coordinado(
        intencion_usuario="Vivir el día con presencia y claridad",
        estructura_dia=estructura,
        contexto=contexto
    )
    
    plan_dia_actual = plan
    
    return plan


@router.post("/actualizar", response_model=JornadaAlBordeCaos)
async def actualizar_espejo(
    request: ActualizarEspejoRequest,
    db: Session = Depends(get_db)
):
    """
    Actualiza el Espejo Diario con un Estado Cero completado.
    
    El Espejo se refina incrementalmente:
    - FAJR: Refina plan completo
    - DHUHR: Ajusta tarde
    - ASR: Marca completados
    - MAGHRIB: Cierra día
    - ISHA: Marca cerrado
    """
    
    global plan_dia_actual
    
    # Obtener plan actual
    if not plan_dia_actual:
        plan_dia_actual = await obtener_espejo_hoy(db)
    
    # Obtener Estado Cero completado
    estado_db = db.query(EstadoCeroDB).filter(EstadoCeroDB.id == request.estado_cero_id).first()
    
    if not estado_db:
        raise HTTPException(status_code=404, detail="Estado Cero no encontrado")
    
    # Parsear respuestas
    respuestas = json.loads(estado_db.respuestas) if estado_db.respuestas else []
    
    # Actualizar espejo
    orquestador = AgenteOrquestador(db, claude_client, calculador)
    
    plan_actualizado = await orquestador.actualizar_espejo_con_estado_cero(
        plan_actual=plan_dia_actual,
        direccion_emergente=request.direccion_emergente,
        momento=request.momento,
        respuestas_sacra=respuestas
    )
    
    plan_dia_actual = plan_actualizado
    
    return plan_actualizado


@router.get("/estados-cero-hoy")
async def obtener_estados_cero_hoy(db: Session = Depends(get_db)):
    """
    Obtiene todos los Estados Cero completados hoy.
    
    Para mostrar en el Espejo cómo se ha ido refinando.
    """
    
    hoy = date.today()
    
    estados = db.query(EstadoCeroDB).filter(
        EstadoCeroDB.fecha >= datetime.combine(hoy, datetime.min.time()),
        EstadoCeroDB.fecha < datetime.combine(hoy, datetime.max.time())
    ).all()
    
    return {
        "fecha": hoy,
        "total": len(estados),
        "estados": [{
            "id": e.id,
            "momento": e.momento,
            "hora": e.fecha,
            "direccion": e.direccion,
            "completado": bool(e.direccion)
        } for e in estados]
    }


@router.delete("/reiniciar")
async def reiniciar_espejo():
    """Reinicia el espejo (útil para testing)"""
    global plan_dia_actual
    plan_dia_actual = None
    return {"mensaje": "Espejo reiniciado"}

