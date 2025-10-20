from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Dict
import json

from models.database import get_db
from models.schemas import (
    JornadaAlBordeCaos, AccionConcreta, ContextoCompleto,
    ChatOrquestadorRequest, AjustePlanRequest
)
from agentes.orquestador import AgenteOrquestador
from services.claude_client import ClaudeClient
from services.contexto import RecopiladorContexto
from services.tiempos_liturgicos import CalculadorTiemposLiturgicos
from services.calendario_hijri import CalendarioHijri
import os

router = APIRouter()

# Servicios
LAT = float(os.getenv("LATITUD", "40.4168"))
LON = float(os.getenv("LONGITUD", "-3.7038"))
TZ = os.getenv("TIMEZONE", "Europe/Madrid")

calculador = CalculadorTiemposLiturgicos(LAT, LON, TZ)
calendario = CalendarioHijri()
claude_client = ClaudeClient()


@router.post("/generar-plan")
async def generar_plan_jornada(
    accion: AccionConcreta = Body(...),
    db: Session = Depends(get_db)
):
    """
    Genera plan emergente de jornada basado en acción del Estado Cero
    """
    
    # Crear agente y recopilador
    recopilador = RecopiladorContexto(db, calculador, calendario)
    agente = AgenteOrquestador(db, claude_client, calculador)
    
    # Recopilar contexto actual
    momento_actual = calculador.momento_actual()
    contexto = await recopilador.recopilar_contexto_completo(momento_actual)
    
    # Generar plan
    plan = await agente.recibir_orientacion(accion, contexto)
    
    return plan


@router.get("/plan-actual")
async def obtener_plan_actual(
    db: Session = Depends(get_db)
):
    """
    Obtiene el plan actual de la jornada
    """
    
    agente = AgenteOrquestador(db, claude_client, calculador)
    plan = agente.obtener_plan_actual()
    
    if not plan:
        raise HTTPException(status_code=404, detail="No hay plan activo")
    
    return plan


@router.post("/chat")
async def chat_orquestador(
    request: ChatOrquestadorRequest,
    db: Session = Depends(get_db)
):
    """
    Chat interactivo con el Orquestador para ajustes
    """
    
    agente = AgenteOrquestador(db, claude_client, calculador)
    
    # Obtener contexto actual
    plan_actual = agente.obtener_plan_actual()
    contexto_actual = {
        "plan": plan_actual.model_dump() if plan_actual else None,
        "momento": calculador.momento_actual().value,
        "proximo_estado_cero": calculador.proximo_estado_cero().model_dump()
    }
    
    # Generar respuesta
    respuesta = await agente.chat_interactivo(request.mensaje, contexto_actual)
    
    return {"respuesta": respuesta}


@router.post("/ajustar-plan")
async def ajustar_plan(
    request: AjustePlanRequest,
    db: Session = Depends(get_db)
):
    """
    Ajusta el plan actual según solicitud del usuario
    """
    
    agente = AgenteOrquestador(db, claude_client, calculador)
    
    # Obtener contexto actual
    plan_actual = agente.obtener_plan_actual()
    if not plan_actual:
        raise HTTPException(status_code=404, detail="No hay plan activo para ajustar")
    
    contexto_actual = {
        "plan": plan_actual.model_dump(),
        "momento": calculador.momento_actual().value
    }
    
    # Aplicar ajustes
    plan_actualizado = await agente.actualizar_plan(request.ajustes, contexto_actual)
    
    return plan_actualizado


@router.post("/establecer-no-negociables")
async def establecer_no_negociables(
    db: Session = Depends(get_db)
):
    """
    Establece los no-negociables del día según contexto actual
    """
    
    agente = AgenteOrquestador(db, claude_client, calculador)
    recopilador = RecopiladorContexto(db, calculador, calendario)
    
    # Recopilar contexto
    momento_actual = calculador.momento_actual()
    contexto = await recopilador.recopilar_contexto_completo(momento_actual)
    
    # Establecer no-negociables
    no_negociables = await agente.establecer_no_negociables(contexto)
    
    return {
        "no_negociables": no_negociables,
        "total": len(no_negociables),
        "por_tipo": {
            "biologico": len([nn for nn in no_negociables if nn.tipo.value == "biologico"]),
            "espiritual": len([nn for nn in no_negociables if nn.tipo.value == "espiritual"]),
            "financiero": len([nn for nn in no_negociables if nn.tipo.value == "financiero"])
        }
    }


@router.get("/estado-jornada")
async def estado_jornada_actual(
    db: Session = Depends(get_db)
):
    """
    Obtiene el estado actual de la jornada
    """
    
    agente = AgenteOrquestador(db, claude_client, calculador)
    plan = agente.obtener_plan_actual()
    
    momento_actual = calculador.momento_actual()
    proximo_estado_cero = calculador.proximo_estado_cero()
    
    return {
        "momento_actual": momento_actual.value,
        "proximo_estado_cero": proximo_estado_cero.model_dump(),
        "plan_activo": plan is not None,
        "plan": plan.model_dump() if plan else None,
        "estado": "activo" if plan else "sin_plan"
    }


@router.post("/reiniciar-jornada")
async def reiniciar_jornada(
    db: Session = Depends(get_db)
):
    """
    Reinicia la jornada (limpia plan actual)
    """
    
    agente = AgenteOrquestador(db, claude_client, calculador)
    agente.plan_actual = None
    
    return {"status": "jornada_reiniciada", "mensaje": "Plan actual eliminado. Listo para nueva orientación."}


@router.get("/espejo-diario/{fecha}")
async def obtener_espejo_diario(fecha: str, db: Session = Depends(get_db)):
    """
    Obtiene el Espejo Diario (plan del día) para una fecha específica.
    Si no existe, genera uno básico con anclas litúrgicas.
    """
    from datetime import datetime as dt, timedelta
    
    try:
        fecha_obj = dt.strptime(fecha, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usar YYYY-MM-DD")
    
    # Por ahora, generar espejo básico (en futuro, consultar BD)
    tiempos_rezo = calculador.calcular_tiempos_hoy()
    
    bloques = []
    
    # Convertir TiemposRezoDia a dict
    tiempos_dict = {
        "fajr": tiempos_rezo.fajr,
        "dhuhr": tiempos_rezo.dhuhr,
        "asr": tiempos_rezo.asr,
        "maghrib": tiempos_rezo.maghrib,
        "isha": tiempos_rezo.isha
    }
    
    # Añadir anclas litúrgicas y Estados Cero
    for nombre_rezo, hora in tiempos_dict.items():
        # Ancla litúrgica
        bloques.append({
            "id": f"ancla_{nombre_rezo}",
            "hora_inicio": hora,
            "hora_fin": hora,
            "tipo": "ancla_liturgica",
            "titulo": f"Salat {nombre_rezo.capitalize()}",
            "descripcion": f"Tiempo de rezo {nombre_rezo}",
            "es_flexible": False,
            "prioridad": "alta"
        })
        
        # Estado Cero (15 min después)
        try:
            hora_dt = dt.strptime(hora, "%H:%M")
            hora_fin = (hora_dt + timedelta(minutes=15)).strftime("%H:%M")
            
            bloques.append({
                "id": f"estado_cero_{nombre_rezo}",
                "hora_inicio": hora,
                "hora_fin": hora_fin,
                "tipo": "estado_cero",
                "titulo": f"Estado Cero ({nombre_rezo.capitalize()})",
                "descripcion": "Consulta sacral",
                "es_flexible": False,
                "prioridad": "alta"
            })
        except Exception as e:
            print(f"Error procesando hora {hora}: {e}")
    
    # Estadísticas básicas
    estadisticas = {
        "anclas_liturgicas": 5,
        "estados_cero": 5,
        "no_negociables": 0,
        "espacio_libre_porcentaje": 40.0,
        "horas_productivas": 0.0
    }
    
    return {
        "fecha": fecha,
        "bloques": bloques,
        "estadisticas": estadisticas,
        "insight": "Tu día está estructurado alrededor de los tiempos litúrgicos.",
        "generado_en": dt.now().isoformat()
    }
