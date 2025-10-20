"""
🌆 API - Ritual Maghrib
=======================

Endpoints para el ritual de cierre del día y preparación de mañana.
"""

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date, timedelta
from pydantic import BaseModel, EmailStr

from models.database import get_db
from models.schemas import MomentoLiturgico, JornadaAlBordeCaos, AccionConcreta
from agentes.orquestador import AgenteOrquestador
from agentes.entrelazador import agente_entrelazador
from services.claude_client import ClaudeClient
from services.contexto import RecopiladorContexto
from services.tiempos_liturgicos import CalculadorTiemposLiturgicos
from services.calendario_hijri import CalendarioHijri
from integraciones.google_calendar import google_calendar
import os


router = APIRouter()

# Servicios
LAT = float(os.getenv("LATITUD", "40.4168"))
LON = float(os.getenv("LONGITUD", "-3.7038"))
TZ = os.getenv("TIMEZONE", "Europe/Madrid")

calculador = CalculadorTiemposLiturgicos(LAT, LON, TZ)
calendario = CalendarioHijri()
claude_client = ClaudeClient()


# ============================================================================
# Schemas
# ============================================================================

class SugerirIntencionRequest(BaseModel):
    """Request para sugerir intención del día siguiente"""
    reflexion_dia: Optional[str] = ""
    estado_cero_direccion: Optional[str] = ""


class PrepararDiaSiguienteRequest(BaseModel):
    """Request para crear jornada en Google Calendar"""
    intencion: str
    asistentes: Optional[List[EmailStr]] = []
    fecha: Optional[date] = None  # Si no se provee, usa mañana


class PrepararDiaSiguienteResponse(BaseModel):
    """Response con plan y eventos creados"""
    plan: JornadaAlBordeCaos
    eventos_creados: int
    eventos: List[dict]
    fecha: date
    google_calendar_url: str


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/sugerir-intencion")
async def sugerir_intencion(
    request: SugerirIntencionRequest,
    db: Session = Depends(get_db)
):
    """
    Sugiere una intención para el día siguiente basándose en:
    - Reflexión del día actual
    - Dirección emergente del Estado Cero de Maghrib
    - Contexto del usuario
    """
    
    # Crear prompt para Claude
    prompt = f"""Eres el Agente Orquestador del Campo Sagrado.

Es el momento Maghrib (cierre del día). El usuario está preparando su intención para mañana.

CONTEXTO DEL DÍA DE HOY:
{f"Reflexión: {request.reflexion_dia}" if request.reflexion_dia else "Sin reflexión explícita"}
{f"Dirección del Estado Cero: {request.estado_cero_direccion}" if request.estado_cero_direccion else ""}

Tu tarea: Sugerir una intención clara y accionable para mañana.

La intención debe ser:
1. Concreta y específica (no abstracta)
2. Evocadora (que genere sensación corporal)
3. Alineada con lo emergente del día
4. En 1-2 líneas máximo

EJEMPLOS BUENOS:
- "Completar dashboard wellness con energía enfocada y momentum sostenido"
- "Profundizar en arquitectura backend permitiendo espacio para lo emergente"
- "Sesión de código creativo en la mañana, integración por la tarde"

EJEMPLOS MALOS (muy abstractos):
- "Ser productivo"
- "Trabajar en el proyecto"
- "Hacer cosas importantes"

Responde solo con la intención sugerida, sin explicaciones adicionales.

Intención para mañana:"""

    try:
        # Generar con Claude
        messages = [{"role": "user", "content": prompt}]
        intencion = await claude_client.generate("", messages)
        
        return {
            "intencion_sugerida": intencion.strip(),
            "puede_editar": True,
            "mensaje": "Sugerencia generada. Puedes modificarla según tu intuición."
        }
    
    except Exception as e:
        # Fallback si Claude falla
        return {
            "intencion_sugerida": "Dedicar energía enfocada a lo más importante del día",
            "puede_editar": True,
            "mensaje": "Sugerencia por defecto (Claude no disponible). Personalízala."
        }


@router.post("/preparar-dia-siguiente", response_model=PrepararDiaSiguienteResponse)
async def preparar_dia_siguiente(
    request: PrepararDiaSiguienteRequest,
    db: Session = Depends(get_db)
):
    """
    Prepara el día siguiente:
    1. Genera plan emergente basado en la intención
    2. Crea eventos en Google Calendar
    3. Invita a asistentes (opcional)
    4. Documenta en Obsidian
    """
    
    # Verificar que Google Calendar esté configurado
    if not google_calendar or not google_calendar.is_authenticated():
        raise HTTPException(
            status_code=503,
            detail="Google Calendar no configurado. Ejecuta: python scripts/setup_google_calendar.py"
        )
    
    # Fecha del día a preparar
    fecha_objetivo = request.fecha or (date.today() + timedelta(days=1))
    
    # Crear servicios
    recopilador = RecopiladorContexto(db, calculador, calendario)
    agente_orquestador = AgenteOrquestador(db, claude_client, calculador)
    
    # ═══════════════════════════════════════════════════════════════
    # CORRESPONDENCIA ENTRELAZADOR ↔ ORQUESTADOR
    # ═══════════════════════════════════════════════════════════════
    
    # 1. Obtener tiempos litúrgicos precisos de mañana
    tiempos_mañana = calculador.calcular_tiempos_hoy(fecha_objetivo)
    
    # 2. Generar estructura base del día (Entrelazador)
    if agente_entrelazador.perfil_usuario:
        estructura_dia = agente_entrelazador.generar_estructura_dia(
            fecha=fecha_objetivo,
            tiempos_liturgicos=tiempos_mañana
        )
    else:
        # Sin perfil, usar estructura mínima
        from services.propositos import generar_anclas_dia, obtener_proposito_dia_semana
        
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        dia_semana = dias_semana[fecha_objetivo.weekday()]
        proposito = obtener_proposito_dia_semana(dia_semana)
        
        estructura_dia = EstructuraDia(
            fecha=fecha_objetivo,
            dia_semana=dia_semana,
            proposito_dia=proposito.proposito,
            energia_dia=proposito.energia,
            tiempos_liturgicos=tiempos_mañana,
            anclas=[],
            no_negociables_dia=[],
            espacio_libre_minutos=675,
            espacio_libre_porcentaje=46.9,
            rutinas_dia=[],
            proyectos_sugeridos=[],
            aprendizaje_sugerido=[]
        )
    
    # 3. Recopilar contexto
    momento_actual = calculador.momento_actual()
    contexto = await recopilador.recopilar_contexto_completo(momento_actual)
    
    # 4. Orquestador genera plan coordinado
    plan = await agente_orquestador.generar_plan_dia_coordinado(
        intencion_usuario=request.intencion,
        estructura_dia=estructura_dia,
        contexto=contexto
    )
    
    # Crear eventos en Google Calendar
    try:
        eventos = google_calendar.crear_jornada_completa(
            fecha=fecha_objetivo,
            plan=plan,
            intencion=request.intencion,
            asistentes=request.asistentes or None
        )
        
        # URL a Google Calendar
        fecha_str = fecha_objetivo.strftime('%Y%m%d')
        calendar_url = f"https://calendar.google.com/calendar/u/0/r/day/{fecha_str}"
        
        return PrepararDiaSiguienteResponse(
            plan=plan,
            eventos_creados=len(eventos),
            eventos=[{
                "id": e.get("id"),
                "titulo": e.get("summary"),
                "inicio": e.get("start", {}).get("dateTime"),
                "url": e.get("htmlLink")
            } for e in eventos],
            fecha=fecha_objetivo,
            google_calendar_url=calendar_url
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creando eventos en Calendar: {str(e)}"
        )


@router.get("/verificar-google-calendar")
async def verificar_google_calendar():
    """Verifica el estado de la integración con Google Calendar"""
    
    if not google_calendar:
        return {
            "conectado": False,
            "mensaje": "Google Calendar no inicializado",
            "instrucciones": "Ejecuta: python scripts/setup_google_calendar.py"
        }
    
    if not google_calendar.is_authenticated():
        return {
            "conectado": False,
            "mensaje": "No autenticado con Google Calendar",
            "instrucciones": "Ejecuta: python scripts/setup_google_calendar.py"
        }
    
    try:
        # Intentar listar calendarios
        calendars = google_calendar.service.calendarList().list().execute()
        calendar_count = len(calendars.get('items', []))
        
        return {
            "conectado": True,
            "mensaje": "Google Calendar conectado correctamente",
            "calendarios_disponibles": calendar_count,
            "listo_para_usar": True
        }
    
    except Exception as e:
        return {
            "conectado": False,
            "mensaje": f"Error verificando conexión: {str(e)}",
            "instrucciones": "Re-ejecuta: python scripts/setup_google_calendar.py"
        }


@router.delete("/limpiar-eventos-dia")
async def limpiar_eventos_dia(fecha: date = None):
    """
    Elimina todos los eventos del Campo Sagrado de un día específico
    (útil para re-planificar)
    """
    if not google_calendar or not google_calendar.is_authenticated():
        raise HTTPException(
            status_code=503,
            detail="Google Calendar no configurado"
        )
    
    fecha_objetivo = fecha or (date.today() + timedelta(days=1))
    
    try:
        eliminados = google_calendar.eliminar_eventos_dia(fecha_objetivo)
        
        return {
            "fecha": fecha_objetivo,
            "eventos_eliminados": eliminados,
            "mensaje": f"Se eliminaron {eliminados} eventos del Campo Sagrado"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error eliminando eventos: {str(e)}"
        )


@router.get("/eventos-dia")
async def listar_eventos_dia(fecha: date = None):
    """Lista todos los eventos de un día"""
    if not google_calendar or not google_calendar.is_authenticated():
        raise HTTPException(
            status_code=503,
            detail="Google Calendar no configurado"
        )
    
    fecha_objetivo = fecha or date.today()
    
    try:
        eventos = google_calendar.listar_eventos_dia(fecha_objetivo)
        
        return {
            "fecha": fecha_objetivo,
            "total_eventos": len(eventos),
            "eventos": [{
                "titulo": e.get("summary"),
                "inicio": e.get("start", {}).get("dateTime"),
                "fin": e.get("end", {}).get("dateTime"),
                "url": e.get("htmlLink")
            } for e in eventos]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listando eventos: {str(e)}"
        )

