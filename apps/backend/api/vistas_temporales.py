"""
📅 API - Vistas Temporales
===========================

Endpoints para obtener vistas semanal, mensual y anual
con significado litúrgico profundo.
"""

from fastapi import APIRouter, Query
from datetime import date, datetime
from typing import Optional

from services.calendario_hijri import CalendarioHijri
from services.tiempos_liturgicos import CalculadorTiemposLiturgicos
import os


router = APIRouter()

# Servicios
LAT = float(os.getenv("LATITUD", "40.5472"))
LON = float(os.getenv("LONGITUD", "-3.6228"))
TZ = os.getenv("TIMEZONE", "Europe/Madrid")

calendario = CalendarioHijri()
calculador = CalculadorTiemposLiturgicos(LAT, LON, TZ)


@router.get("/contexto-temporal")
async def obtener_contexto_temporal(fecha: Optional[str] = None):
    """
    Obtiene el contexto temporal completo para una fecha.
    
    Incluye:
    - Mes Hijri con significado místico
    - Día de la semana con propósito arquetípico
    - Guía para el Entrelazador
    - Enseñanzas y prácticas recomendadas
    
    Query params:
    - fecha: YYYY-MM-DD (opcional, default: hoy)
    """
    if fecha:
        dia = datetime.strptime(fecha, "%Y-%m-%d").date()
    else:
        dia = date.today()
    
    contexto = calendario.obtener_contexto_temporal_completo(dia)
    return contexto


@router.get("/vista-semanal")
async def obtener_vista_semanal(fecha_inicio: Optional[str] = None):
    """
    Vista semanal con propósito profundo de cada día.
    
    Retorna:
    - 7 días con sus arquetipos planetarios
    - Propósito e intención de cada día
    - Energía y dimensión prioritaria
    - Práctica sugerida
    - Alertas de sesgo personalizadas
    - Contexto del mes Hijri actual
    
    Query params:
    - fecha_inicio: YYYY-MM-DD (opcional, ajusta a lunes de esa semana)
    """
    if fecha_inicio:
        dia = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    else:
        dia = date.today()
    
    vista = calendario.obtener_vista_semanal(dia)
    
    # Enriquecer con tiempos de rezo para cada día
    for dia_info in vista["dias"]:
        fecha_dia = datetime.strptime(dia_info["fecha"], "%Y-%m-%d").date()
        tiempos = calculador.calcular_tiempos_hoy(fecha_dia)
        
        dia_info["tiempos_rezo"] = {
            "fajr": tiempos.fajr.inicio.strftime("%H:%M"),
            "dhuhr": tiempos.dhuhr.inicio.strftime("%H:%M"),
            "asr": tiempos.asr.inicio.strftime("%H:%M"),
            "maghrib": tiempos.maghrib.inicio.strftime("%H:%M"),
            "isha": tiempos.isha.inicio.strftime("%H:%M")
        }
    
    return vista


@router.get("/vista-mensual")
async def obtener_vista_mensual(fecha: Optional[str] = None):
    """
    Vista mensual con significado litúrgico Hijri completo.
    
    Retorna:
    - Nombre árabe y español del mes
    - Significado profundo
    - Enseñanza mística sufí
    - Cualidad espiritual
    - Si es mes sagrado (حُرُم)
    - Ayat del Corán relacionada
    - Práctica recomendada
    - Dimensión prioritaria
    - Símbolo y color
    
    Query params:
    - fecha: YYYY-MM-DD (opcional, default: mes actual)
    """
    if fecha:
        dia = datetime.strptime(fecha, "%Y-%m-%d").date()
    else:
        dia = date.today()
    
    vista_mensual = calendario.obtener_vista_mensual(dia)
    
    return vista_mensual


@router.get("/vista-anual")
async def obtener_vista_anual(fecha: Optional[str] = None):
    """
    Vista anual completa con los 12 meses lunares.
    
    Retorna:
    - Año Hijri actual
    - 12 meses con sus cualidades
    - Meses sagrados identificados
    - Ciclo completo del viaje espiritual
    - Enseñanza anual integradora
    
    Query params:
    - fecha: YYYY-MM-DD (opcional, default: año actual)
    """
    if fecha:
        dia = datetime.strptime(fecha, "%Y-%m-%d").date()
    else:
        dia = date.today()
    
    vista_anual = calendario.obtener_vista_anual(dia)
    
    return vista_anual


@router.get("/dias-semana")
async def obtener_todos_dias_semana():
    """
    Retorna la información completa de todos los días de la semana.
    
    Útil para:
    - Mostrar en UI una tabla completa
    - Entender el propósito de cada día
    - Planificación semanal consciente
    """
    return {
        "dias": [
            {
                "nombre": dia_info.nombre,
                "arquetipo": dia_info.arquetipo.value,
                "proposito": dia_info.proposito_profundo,
                "energia": dia_info.energia,
                "dimension": dia_info.dimension_prioritaria,
                "intencion": dia_info.intencion,
                "practica": dia_info.practica_sugerida,
                "alerta_sesgo": dia_info.alerta_sesgo
            }
            for dia_info in calendario.dias_semana.values()
        ]
    }


@router.get("/meses-hijri")
async def obtener_todos_meses_hijri():
    """
    Retorna la información completa de los 12 meses Hijri.
    
    Útil para:
    - Mostrar calendario anual completo
    - Entender el ciclo espiritual completo
    - Planificación a largo plazo
    """
    return {
        "meses": [
            {
                "numero": mes.numero,
                "nombre_arabe": mes.nombre_arabe,
                "nombre_es": mes.nombre_es,
                "significado": mes.significado,
                "cualidad": mes.cualidad.value,
                "es_sagrado": mes.es_sagrado,
                "ensenanza": mes.ensenanza_mistica,
                "practica": mes.practica_recomendada,
                "dimension": mes.dimension_prioritaria,
                "simbolo": mes.simbolo,
                "color": mes.color,
                "ayat": mes.ayat_clave
            }
            for mes in calendario.meses_hijri
        ],
        "meses_sagrados": [1, 7, 11, 12],
        "total_meses": 12
    }
