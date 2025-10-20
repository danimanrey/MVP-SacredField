from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import Dict

from models.database import get_db
from models.schemas import ReporteDiario
from agentes.guardian import AgenteGuardian
from services.claude_client import ClaudeClient

router = APIRouter()

# Servicios
claude_client = ClaudeClient()


@router.post("/reporte-diario")
async def generar_reporte_diario(
    fecha: date = None,
    db: Session = Depends(get_db)
):
    """
    Genera reporte diario para la fecha especificada
    Si no se especifica fecha, usa hoy
    """
    
    if fecha is None:
        fecha = date.today()
    
    agente = AgenteGuardian(db, claude_client)
    reporte = await agente.generar_reporte_diario(fecha)
    
    return reporte


@router.get("/salud-sistema")
async def monitorear_salud_sistema(
    db: Session = Depends(get_db)
):
    """
    Monitorea la salud general del sistema
    """
    
    agente = AgenteGuardian(db, claude_client)
    salud = await agente.monitorear_salud_sistema()
    
    return salud


@router.get("/patrones")
async def detectar_patrones(
    dias_atras: int = 7,
    db: Session = Depends(get_db)
):
    """
    Detecta patrones en los últimos N días
    """
    
    agente = AgenteGuardian(db, claude_client)
    patrones = await agente.detectar_patrones(dias_atras)
    
    return patrones


@router.get("/metricas-hoy")
async def metricas_del_dia(
    db: Session = Depends(get_db)
):
    """
    Obtiene métricas del día actual
    """
    
    hoy = date.today()
    agente = AgenteGuardian(db, claude_client)
    
    # Obtener salud del sistema
    salud = await agente.monitorear_salud_sistema()
    
    return {
        "fecha": hoy.isoformat(),
        "salud": salud,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/metricas-semana")
async def metricas_semana_actual(
    db: Session = Depends(get_db)
):
    """
    Obtiene métricas de la semana actual
    """
    
    agente = AgenteGuardian(db, claude_client)
    
    # Obtener patrones de la semana
    patrones = await agente.detectar_patrones(7)
    
    # Obtener salud actual
    salud = await agente.monitorear_salud_sistema()
    
    return {
        "semana": patrones,
        "salud_actual": salud,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/estado-general")
async def estado_general_sistema(
    db: Session = Depends(get_db)
):
    """
    Estado general del sistema Campo Sagrado
    """
    
    agente = AgenteGuardian(db, claude_client)
    
    # Recopilar información completa
    salud = await agente.monitorear_salud_sistema()
    patrones = await agente.detectar_patrones(7)
    
    # Determinar estado general
    if salud["salud_general"] == "buena":
        estado = "optimo"
        mensaje = "Sistema funcionando correctamente"
    else:
        estado = "atencion_requerida"
        mensaje = "Se requiere atención en algunos aspectos"
    
    return {
        "estado": estado,
        "mensaje": mensaje,
        "salud": salud,
        "patrones": patrones,
        "timestamp": datetime.now().isoformat(),
        "version": "0.1.0-mvp"
    }


@router.post("/reporte-automatico")
async def generar_reporte_automatico(
    db: Session = Depends(get_db)
):
    """
    Genera reporte automático (llamado por cron/timer)
    """
    
    hoy = date.today()
    agente = AgenteGuardian(db, claude_client)
    
    try:
        # Generar reporte diario
        reporte = await agente.generar_reporte_diario(hoy)
        
        return {
            "status": "success",
            "reporte_generado": True,
            "fecha": hoy.isoformat(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "reporte_generado": False,
            "error": str(e),
            "fecha": hoy.isoformat(),
            "timestamp": datetime.now().isoformat()
        }


@router.get("/alertas")
async def verificar_alertas(
    db: Session = Depends(get_db)
):
    """
    Verifica si hay alertas que requieren atención
    """
    
    agente = AgenteGuardian(db, claude_client)
    salud = await agente.monitorear_salud_sistema()
    
    alertas = []
    
    # Verificar alertas
    if salud["estados_cero"] == 0:
        alertas.append({
            "tipo": "estados_cero",
            "nivel": "warning",
            "mensaje": "No se han completado Estados Cero hoy"
        })
    
    if salud["no_negociables"]["porcentaje"] < 50:
        alertas.append({
            "tipo": "no_negociables",
            "nivel": "warning",
            "mensaje": f"Solo {salud['no_negociables']['porcentaje']:.1f}% de no-negociables completados"
        })
    
    if salud["salud_general"] == "requiere_atencion":
        alertas.append({
            "tipo": "salud_general",
            "nivel": "info",
            "mensaje": "Sistema requiere atención general"
        })
    
    return {
        "alertas": alertas,
        "total_alertas": len(alertas),
        "timestamp": datetime.now().isoformat()
    }


@router.get("/estado-sistema")
async def obtener_estado_sistema(db: Session = Depends(get_db)):
    """
    Obtiene el estado actual completo del sistema (para Dashboard).
    """
    
    # Mock de datos del sistema (en futuro, consultar BD real)
    return {
        "estado_general": "saludable",
        "agentes": {
            "estado_cero": {
                "activo": True,
                "ultima_ejecucion": datetime.now().isoformat(),
                "estados_hoy": 3,
                "estados_objetivo": 5
            },
            "orquestador": {
                "activo": True,
                "ultima_planificacion": datetime.now().isoformat(),
                "precision_estimaciones": 0.87
            },
            "documentador": {
                "activo": True,
                "documentos_creados_hoy": 3,
                "vault_conectado": True
            }
        },
        "metricas": {
            "coherencia_sistema": 0.92,
            "adherencia_plan": 0.85,
            "espacio_libre_respetado": 0.95
        },
        "alertas": []
    }


@router.get("/reportes/diario")
async def obtener_reporte_diario(db: Session = Depends(get_db)):
    """
    Genera un reporte diario del sistema.
    """
    
    return {
        "fecha": date.today().isoformat(),
        "resumen": "Día productivo con Estados Cero completados",
        "estados_cero_completados": 3,
        "adherencia_plan": 0.85,
        "espacio_libre_utilizado": 0.40,
        "logros_del_dia": [
            "Completaste Estados Cero matinales",
            "Respetaste las anclas litúrgicas",
            "Mantuviste espacio libre adecuado"
        ],
        "areas_mejora": [
            "Considera añadir más no-negociables"
        ],
        "recomendaciones": [
            "Mañana prioriza la dimensión del día"
        ]
    }
