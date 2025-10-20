"""
🏗️ API - Estructura del Día
============================

Endpoints para obtener la estructura base de cada día.
"""

from fastapi import APIRouter, HTTPException
from datetime import date, timedelta
from typing import Optional

from models.schemas import EstructuraDia
from agentes.entrelazador import agente_entrelazador
from services.tiempos_liturgicos import CalculadorTiemposLiturgicos
from services.propositos import obtener_proposito_estado_cero, obtener_proposito_dia_semana, obtener_proposito_mes_hijri
from services.calendario_hijri import CalendarioHijri
import os


router = APIRouter()

# Servicios
LAT = float(os.getenv("LATITUD", "40.4168"))
LON = float(os.getenv("LONGITUD", "-3.7038"))
TZ = os.getenv("TIMEZONE", "Europe/Madrid")

calculador = CalculadorTiemposLiturgicos(LAT, LON, TZ)
calendario = CalendarioHijri()


@router.get("/dia", response_model=EstructuraDia)
async def obtener_estructura_dia(fecha: Optional[str] = None):
    """
    Obtiene la estructura base de un día específico.
    
    Query params:
    - fecha: YYYY-MM-DD (opcional, default: hoy)
    
    Retorna:
    - Anclas (rezo + Estado Cero) con tiempos precisos
    - No-negociables
    - Propósito del día
    - Espacio libre disponible
    - Rutinas del día
    """
    
    # Parsear fecha
    if fecha:
        from datetime import datetime
        dia = datetime.strptime(fecha, "%Y-%m-%d").date()
    else:
        dia = date.today()
    
    # Verificar que haya perfil cargado
    if not agente_entrelazador.perfil_usuario:
        raise HTTPException(
            status_code=400,
            detail="Perfil no configurado. Primero configura tu perfil en /configurar-perfil"
        )
    
    # Calcular tiempos litúrgicos precisos
    tiempos = calculador.calcular_tiempos_hoy(dia)
    
    # Generar estructura
    estructura = agente_entrelazador.generar_estructura_dia(dia, tiempos)
    
    return estructura


@router.get("/propositos")
async def obtener_propositos():
    """
    Obtiene todos los propósitos del sistema:
    - Estados Cero (5)
    - Días de semana (7)
    - Meses Hijri (13)
    """
    
    from models.schemas import MomentoLiturgico
    
    return {
        "estados_cero": {
            momento.value: obtener_proposito_estado_cero(momento).model_dump()
            for momento in MomentoLiturgico
        },
        "dias_semana": {
            dia: obtener_proposito_dia_semana(dia).model_dump()
            for dia in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        },
        "meses_hijri": {
            mes: obtener_proposito_mes_hijri(mes).model_dump()
            for mes in ["Muharram", "Safar", "Rabi al-Awwal", "Rabi al-Thani", 
                       "Jumada al-Ula", "Jumada al-Akhirah", "Rajab", "Shaban",
                       "Ramadan", "Shawwal", "Dhul-Qadah", "Dhul-Hijjah", "Muharram 13"]
        }
    }


@router.get("/anclas-dia")
async def obtener_anclas_dia(fecha: Optional[str] = None):
    """
    Obtiene las anclas del día (rezo + Estado Cero) con tiempos precisos.
    
    Cada ancla incluye:
    - Hora exacta (astronómica)
    - Duración (15 min rezo, 15 min Estado Cero)
    - Propósito
    """
    
    if fecha:
        from datetime import datetime
        dia = datetime.strptime(fecha, "%Y-%m-%d").date()
    else:
        dia = date.today()
    
    tiempos = calculador.calcular_tiempos_hoy(dia)
    
    from services.propositos import generar_anclas_dia
    anclas = generar_anclas_dia(tiempos)
    
    return {
        "fecha": dia,
        "anclas": anclas,
        "total_tiempo_anclas": sum([a["duracion"] for a in anclas]),
        "momentos": 5
    }


@router.get("/espacio-libre")
async def calcular_espacio_libre_dia(fecha: Optional[str] = None):
    """
    Calcula el espacio libre disponible en un día.
    
    Considera:
    - Anclas (rezo + Estado Cero): ~165 min
    - Sueño: 480 min (8h)
    - No-negociables: ~120 min
    - Rutinas: variable
    
    Objetivo: Mantener 40% libre (~576 min de 1440)
    """
    
    if fecha:
        from datetime import datetime
        dia = datetime.strptime(fecha, "%Y-%m-%d").date()
    else:
        dia = date.today()
    
    if not agente_entrelazador.perfil_usuario:
        raise HTTPException(
            status_code=400,
            detail="Perfil no configurado"
        )
    
    tiempos = calculador.calcular_tiempos_hoy(dia)
    estructura = agente_entrelazador.generar_estructura_dia(dia, tiempos)
    
    return {
        "fecha": dia,
        "espacio_libre_minutos": estructura.espacio_libre_minutos,
        "espacio_libre_porcentaje": round(estructura.espacio_libre_porcentaje, 1),
        "objetivo_porcentaje": 40,
        "esta_en_objetivo": estructura.espacio_libre_porcentaje >= 40,
        "desglose": {
            "total_dia": 1440,
            "anclas_rezo_estado_cero": 165,
            "sueno": 480,
            "no_negociables": 120,
            "rutinas": sum([r["duracion_minutos"] for r in estructura.rutinas_dia]),
            "libre": estructura.espacio_libre_minutos
        }
    }

