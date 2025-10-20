"""
🗓️ Campo Sagrado - API Calendario Bidireccional
===============================================

Endpoints para gestión completa del calendario:
- Programar Estados Cero semanales
- Crear No Negociables
- Sincronizar Espejo Diario
- Obtener eventos próximos
- Configuración de calendario

Configuración 0.01%: Precisión astronómica + automatización completa
"""

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Any
import os
import asyncio

from services.google_calendar import GoogleCalendarIntegration
from services.audit_trail import AuditTrail
from services.obsidian_structure import ObsidianStructureManager

router = APIRouter()

# Configuración
VAULT_PATH = os.path.expanduser(os.getenv("OBSIDIAN_VAULT_PATH", "~/Documents/CampoSagrado"))

# Inicializar servicios
calendar = GoogleCalendarIntegration(VAULT_PATH)
audit = AuditTrail(VAULT_PATH)
vault_manager = ObsidianStructureManager(VAULT_PATH)


@router.get("/test")
async def test_calendario():
    """Test de conectividad con Google Calendar"""
    try:
        eventos = await calendar.obtener_eventos_proximos(1)
        return {
            "status": "ok",
            "calendario": "conectado",
            "eventos_proximos": len(eventos),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "calendario": "no_conectado",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@router.post("/programar-semana")
async def programar_semana_estados_cero(
    fecha_inicio: str = None,
    semanas: int = 1
):
    """
    Programa Estados Cero para una o más semanas
    Crea eventos automáticos en Google Calendar
    """
    try:
        if fecha_inicio:
            fecha_start = date.fromisoformat(fecha_inicio)
        else:
            fecha_start = date.today()
        
        eventos_creados = []
        
        for semana in range(semanas):
            fecha_semana = fecha_start + timedelta(weeks=semana)
            eventos = await calendar.programar_semana_estados_cero(fecha_semana)
            eventos_creados.extend(eventos)
        
        # Audit trail
        audit.log_event(
            event_type="calendario_semana_programada",
            origen="api_request",
            estado="success",
            metadata={
                "fecha_inicio": fecha_start.isoformat(),
                "semanas": semanas,
                "eventos_creados": len(eventos_creados)
            }
        )
        
        return {
            "status": "success",
            "fecha_inicio": fecha_start.isoformat(),
            "semanas_programadas": semanas,
            "eventos_creados": len(eventos_creados),
            "event_ids": eventos_creados,
            "mensaje": f"Programados {len(eventos_creados)} Estados Cero para {semanas} semana(s)"
        }
        
    except Exception as e:
        audit.log_event(
            event_type="calendario_semana_programada",
            origen="api_request",
            estado="error",
            metadata={
                "fecha_inicio": fecha_inicio,
                "semanas": semanas,
                "error": str(e)
            }
        )
        raise HTTPException(status_code=500, detail=f"Error programando semana: {str(e)}")


@router.post("/crear-no-negociable")
async def crear_no_negociable(
    titulo: str,
    descripcion: str,
    fecha_inicio: str,
    hora_inicio: str,
    duracion_minutos: int = 60,
    tipo: str = "no_negociable"
):
    """
    Crea bloqueo de No Negociable en el calendario
    """
    try:
        # Parsear fecha y hora
        fecha = date.fromisoformat(fecha_inicio)
        hora_parts = hora_inicio.split(":")
        inicio = datetime.combine(fecha, datetime.min.time().replace(
            hour=int(hora_parts[0]),
            minute=int(hora_parts[1])
        ))
        fin = inicio + timedelta(minutes=duracion_minutos)
        
        event_id = await calendar.crear_bloqueo_no_negociable(
            titulo=titulo,
            descripcion=descripcion,
            inicio=inicio,
            fin=fin,
            tipo=tipo
        )
        
        audit.log_event(
            event_type="calendario_no_negociable_creado",
            origen="api_request",
            estado="success",
            metadata={
                "event_id": event_id,
                "titulo": titulo,
                "tipo": tipo
            }
        )
        
        return {
            "status": "success",
            "event_id": event_id,
            "titulo": titulo,
            "inicio": inicio.isoformat(),
            "fin": fin.isoformat(),
            "mensaje": f"No Negociable '{titulo}' creado en calendario"
        }
        
    except Exception as e:
        audit.log_event(
            event_type="calendario_no_negociable_creado",
            origen="api_request",
            estado="error",
            metadata={
                "titulo": titulo,
                "error": str(e)
            }
        )
        raise HTTPException(status_code=500, detail=f"Error creando No Negociable: {str(e)}")


@router.post("/crear-espejo-diario")
async def crear_evento_espejo_diario(
    fecha: str = None,
    estados_cero_count: int = 5
):
    """
    Crea evento de Espejo Diario en el calendario
    """
    try:
        if fecha:
            target_date = date.fromisoformat(fecha)
        else:
            target_date = date.today()
        
        event_id = await calendar.crear_evento_espejo_diario(
            fecha=target_date,
            estados_cero_count=estados_cero_count
        )
        
        audit.log_event(
            event_type="calendario_espejo_creado",
            origen="api_request",
            estado="success",
            metadata={
                "event_id": event_id,
                "fecha": target_date.isoformat()
            }
        )
        
        return {
            "status": "success",
            "event_id": event_id,
            "fecha": target_date.isoformat(),
            "mensaje": f"Espejo Diario programado para {target_date}"
        }
        
    except Exception as e:
        audit.log_event(
            event_type="calendario_espejo_creado",
            origen="api_request",
            estado="error",
            metadata={
                "fecha": fecha,
                "error": str(e)
            }
        )
        raise HTTPException(status_code=500, detail=f"Error creando Espejo Diario: {str(e)}")


@router.get("/eventos-proximos")
async def obtener_eventos_proximos(
    horas: int = 24
):
    """
    Obtiene eventos próximos del calendario
    """
    try:
        eventos = await calendar.obtener_eventos_proximos(horas)
        
        # Formatear eventos para respuesta
        eventos_formateados = []
        for evento in eventos:
            eventos_formateados.append({
                "id": evento.get("id"),
                "titulo": evento.get("summary"),
                "descripcion": evento.get("description", "")[:200] + "...",
                "inicio": evento.get("start", {}).get("dateTime"),
                "fin": evento.get("end", {}).get("dateTime"),
                "color": evento.get("colorId"),
                "ubicacion": evento.get("location", ""),
                "tipo": "campo_sagrado" if any(emoji in evento.get("summary", "") 
                                             for emoji in ["🕌", "🪞", "🔒"]) else "otro"
            })
        
        return {
            "status": "success",
            "horas": horas,
            "total_eventos": len(eventos),
            "eventos_campo_sagrado": len([e for e in eventos_formateados if e["tipo"] == "campo_sagrado"]),
            "eventos": eventos_formateados
        }
        
    except Exception as e:
        audit.log_event(
            event_type="calendario_obtener_eventos",
            origen="api_request",
            estado="error",
            metadata={
                "horas": horas,
                "error": str(e)
            }
        )
        raise HTTPException(status_code=500, detail=f"Error obteniendo eventos: {str(e)}")


@router.get("/estado-sincronizacion")
async def estado_sincronizacion():
    """
    Verifica estado de sincronización con Google Calendar
    """
    try:
        # Verificar conectividad
        eventos = await calendar.obtener_eventos_proximos(24)
        
        # Contar eventos del Campo Sagrado
        eventos_campo = [
            e for e in eventos 
            if any(emoji in e.get("summary", "") for emoji in ["🕌", "🪞", "🔒"])
        ]
        
        # Verificar configuración
        config_ok = all([
            os.getenv("GOOGLE_CALENDAR_API_KEY"),
            os.getenv("GOOGLE_CALENDAR_ID", "primary"),
            os.getenv("LATITUD"),
            os.getenv("LONGITUD"),
            os.getenv("TIMEZONE")
        ])
        
        return {
            "status": "success",
            "sincronizacion": {
                "conectado": True,
                "configuracion_completa": config_ok,
                "eventos_proximos_24h": len(eventos),
                "eventos_campo_sagrado": len(eventos_campo),
                "cache_eventos": len(calendar.eventos_cache)
            },
            "configuracion": {
                "api_key_configurada": bool(os.getenv("GOOGLE_CALENDAR_API_KEY")),
                "calendar_id": os.getenv("GOOGLE_CALENDAR_ID", "primary"),
                "latitud": os.getenv("LATITUD"),
                "longitud": os.getenv("LONGITUD"),
                "timezone": os.getenv("TIMEZONE")
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "sincronizacion": {
                "conectado": False,
                "error": str(e)
            },
            "timestamp": datetime.now().isoformat()
        }


@router.post("/limpiar-cache")
async def limpiar_cache_calendario():
    """
    Limpia cache de eventos del calendario
    """
    try:
        calendar.limpiar_cache()
        
        audit.log_event(
            event_type="calendario_cache_limpiado",
            origen="api_request",
            estado="success",
            metadata={}
        )
        
        return {
            "status": "success",
            "mensaje": "Cache de calendario limpiado",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        audit.log_event(
            event_type="calendario_cache_limpiado",
            origen="api_request",
            estado="error",
            metadata={"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=f"Error limpiando cache: {str(e)}")


@router.get("/tiempos-liturgicos")
async def obtener_tiempos_liturgicos(
    fecha: str = None
):
    """
    Obtiene tiempos litúrgicos calculados para una fecha
    """
    try:
        if fecha:
            target_date = date.fromisoformat(fecha)
        else:
            target_date = date.today()
        
        tiempos = calendar.calculador.calcular_tiempos_hoy(target_date)
        
        # Formatear tiempos
        tiempos_formateados = {
            "fajr": {
                "hora": tiempos.fajr.inicio.strftime("%H:%M"),
                "datetime": tiempos.fajr.inicio.isoformat(),
                "momento_español": "Alba"
            },
            "dhuhr": {
                "hora": tiempos.dhuhr.inicio.strftime("%H:%M"),
                "datetime": tiempos.dhuhr.inicio.isoformat(),
                "momento_español": "Mediodía"
            },
            "asr": {
                "hora": tiempos.asr.inicio.strftime("%H:%M"),
                "datetime": tiempos.asr.inicio.isoformat(),
                "momento_español": "Tarde"
            },
            "maghrib": {
                "hora": tiempos.maghrib.inicio.strftime("%H:%M"),
                "datetime": tiempos.maghrib.inicio.isoformat(),
                "momento_español": "Atardecer"
            },
            "isha": {
                "hora": tiempos.isha.inicio.strftime("%H:%M"),
                "datetime": tiempos.isha.inicio.isoformat(),
                "momento_español": "Noche"
            }
        }
        
        return {
            "status": "success",
            "fecha": target_date.isoformat(),
            "coordenadas": {
                "latitud": calendar.lat,
                "longitud": calendar.lon,
                "timezone": calendar.tz
            },
            "tiempos": tiempos_formateados
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculando tiempos: {str(e)}")


@router.post("/programar-mes")
async def programar_mes_completo(
    año: int = None,
    mes: int = None
):
    """
    Programa Estados Cero para todo un mes
    """
    try:
        if not año or not mes:
            hoy = date.today()
            año = año or hoy.year
            mes = mes or hoy.month
        
        # Primera fecha del mes
        fecha_inicio = date(año, mes, 1)
        
        # Última fecha del mes
        if mes == 12:
            fecha_fin = date(año + 1, 1, 1) - timedelta(days=1)
        else:
            fecha_fin = date(año, mes + 1, 1) - timedelta(days=1)
        
        # Calcular semanas necesarias
        dias_mes = (fecha_fin - fecha_inicio).days + 1
        semanas = (dias_mes + 6) // 7  # Redondear hacia arriba
        
        eventos_creados = []
        
        for semana in range(semanas):
            fecha_semana = fecha_inicio + timedelta(weeks=semana)
            eventos = await calendar.programar_semana_estados_cero(fecha_semana)
            eventos_creados.extend(eventos)
        
        audit.log_event(
            event_type="calendario_mes_programado",
            origen="api_request",
            estado="success",
            metadata={
                "año": año,
                "mes": mes,
                "eventos_creados": len(eventos_creados)
            }
        )
        
        return {
            "status": "success",
            "año": año,
            "mes": mes,
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin.isoformat(),
            "semanas_programadas": semanas,
            "eventos_creados": len(eventos_creados),
            "mensaje": f"Programados {len(eventos_creados)} Estados Cero para {mes}/{año}"
        }
        
    except Exception as e:
        audit.log_event(
            event_type="calendario_mes_programado",
            origen="api_request",
            estado="error",
            metadata={
                "año": año,
                "mes": mes,
                "error": str(e)
            }
        )
        raise HTTPException(status_code=500, detail=f"Error programando mes: {str(e)}")
