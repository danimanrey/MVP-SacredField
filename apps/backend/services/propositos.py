"""
🕌 Servicio de Propósitos
=========================

Define el propósito de cada ciclo temporal:
- Estado Cero (5 momentos)
- Día de semana (7 días)
- Mes Hijri (13 meses)
"""

from typing import List
from models.schemas import PropositoEstadoCero, PropositoDiaSemana, PropositoMesHijri, MomentoLiturgico, TiemposRezoDia


# ============================================================================
# PROPÓSITOS DE ESTADOS CERO
# ============================================================================

PROPOSITOS_ESTADO_CERO = {
    MomentoLiturgico.FAJR: PropositoEstadoCero(
        momento=MomentoLiturgico.FAJR,
        proposito="INICIO - Establecer intención del día",
        enfoque="¿Qué quiere emerger hoy? ¿Cuál es la dirección?",
        resultado_esperado="Dirección clara y sensación de inicio",
        actualiza_espejo="Refina PLAN COMPLETO del día con intención"
    ),
    
    MomentoLiturgico.DHUHR: PropositoEstadoCero(
        momento=MomentoLiturgico.DHUHR,
        proposito="REVISIÓN - Refinar rumbo",
        enfoque="¿Cómo va la mañana? ¿Qué ajustar en la tarde?",
        resultado_esperado="Ajuste de rumbo si es necesario",
        actualiza_espejo="Ajusta BLOQUES DE TARDE según progreso mañana"
    ),
    
    MomentoLiturgico.ASR: PropositoEstadoCero(
        momento=MomentoLiturgico.ASR,
        proposito="COMPLETAR - Cerrar ciclos abiertos",
        enfoque="¿Qué necesita cerrarse? ¿Qué ciclos quedan abiertos?",
        resultado_esperado="Claridad sobre cierre del día",
        actualiza_espejo="Marca COMPLETADOS, identifica PENDIENTES para mañana"
    ),
    
    MomentoLiturgico.MAGHRIB: PropositoEstadoCero(
        momento=MomentoLiturgico.MAGHRIB,
        proposito="INTEGRACIÓN - Reflexionar y preparar",
        enfoque="¿Qué integrar del día? ¿Qué soltar? ¿Qué sembrar mañana?",
        resultado_esperado="Reflexión + Intención para mañana",
        actualiza_espejo="CIERRA día actual, CREA día siguiente en Calendar"
    ),
    
    MomentoLiturgico.ISHA: PropositoEstadoCero(
        momento=MomentoLiturgico.ISHA,
        proposito="SOLTAR - Paz y descanso",
        enfoque="¿Hay paz con lo vivido? ¿Qué suelta el cuerpo?",
        resultado_esperado="Paz, cierre, listo para descanso",
        actualiza_espejo="Marca día como CERRADO, prepara descanso"
    )
}


# ============================================================================
# PROPÓSITOS DE DÍAS DE LA SEMANA
# ============================================================================

PROPOSITOS_DIAS_SEMANA = {
    "Lunes": PropositoDiaSemana(
        dia="Lunes",
        proposito="Iniciar",
        energia="Expansión",
        enfoque="Nuevos comienzos, establecer momentum"
    ),
    
    "Martes": PropositoDiaSemana(
        dia="Martes",
        proposito="Construir",
        energia="Acción",
        enfoque="Momentum sostenido, construcción activa"
    ),
    
    "Miércoles": PropositoDiaSemana(
        dia="Miércoles",
        proposito="Expresar",
        energia="Comunicación",
        enfoque="Compartir, comunicar, conectar"
    ),
    
    "Jueves": PropositoDiaSemana(
        dia="Jueves",
        proposito="Expandir",
        energia="Abundancia",
        enfoque="Crecimiento, abundancia, apertura"
    ),
    
    "Viernes": PropositoDiaSemana(
        dia="Viernes",
        proposito="Agradecer",
        energia="Gratitud",
        enfoque="Celebración, gratitud, reconocimiento"
    ),
    
    "Sábado": PropositoDiaSemana(
        dia="Sábado",
        proposito="Reflexionar",
        energia="Introspección",
        enfoque="Aprender, reflexionar, integrar"
    ),
    
    "Domingo": PropositoDiaSemana(
        dia="Domingo",
        proposito="Descansar",
        energia="Restauración",
        enfoque="Renovar, restaurar, preparar"
    )
}


# ============================================================================
# PROPÓSITOS DE MESES HIJRI (13 meses)
# ============================================================================

PROPOSITOS_MESES_HIJRI = {
    "Muharram": PropositoMesHijri(
        mes="Muharram",
        proposito="Reflexionar",
        cualidad="Iniciar ciclo anual - Año Nuevo Hijri"
    ),
    
    "Safar": PropositoMesHijri(
        mes="Safar",
        proposito="Purificar",
        cualidad="Limpiar, soltar lo viejo"
    ),
    
    "Rabi al-Awwal": PropositoMesHijri(
        mes="Rabi al-Awwal",
        proposito="Celebrar",
        cualidad="Luz, nacimiento del Profeta"
    ),
    
    "Rabi al-Thani": PropositoMesHijri(
        mes="Rabi al-Thani",
        proposito="Construir",
        cualidad="Estabilidad, fundamentos"
    ),
    
    "Jumada al-Ula": PropositoMesHijri(
        mes="Jumada al-Ula",
        proposito="Consolidar",
        cualidad="Estructura, forma"
    ),
    
    "Jumada al-Akhirah": PropositoMesHijri(
        mes="Jumada al-Akhirah",
        proposito="Madurar",
        cualidad="Profundidad, madurez"
    ),
    
    "Rajab": PropositoMesHijri(
        mes="Rajab",
        proposito="Preparar",
        cualidad="Anticipación, preparación"
    ),
    
    "Shaban": PropositoMesHijri(
        mes="Shaban",
        proposito="Intensificar",
        cualidad="Enfoque, intensidad"
    ),
    
    "Ramadan": PropositoMesHijri(
        mes="Ramadan",
        proposito="Purificar",
        cualidad="Transformación profunda"
    ),
    
    "Shawwal": PropositoMesHijri(
        mes="Shawwal",
        proposito="Celebrar",
        cualidad="Gratitud, celebración"
    ),
    
    "Dhul-Qadah": PropositoMesHijri(
        mes="Dhul-Qadah",
        proposito="Preparar",
        cualidad="Tregua, preparación para Hajj"
    ),
    
    "Dhul-Hijjah": PropositoMesHijri(
        mes="Dhul-Hijjah",
        proposito="Culminar",
        cualidad="Sacrificio, culminación"
    ),
    
    "Muharram 13": PropositoMesHijri(
        mes="Muharram 13",
        proposito="Transición",
        cualidad="Puente al nuevo año"
    )
}


# ============================================================================
# FUNCIONES HELPER
# ============================================================================

def obtener_proposito_estado_cero(momento: MomentoLiturgico) -> PropositoEstadoCero:
    """Obtiene el propósito de un Estado Cero específico"""
    return PROPOSITOS_ESTADO_CERO[momento]


def obtener_proposito_dia_semana(dia: str) -> PropositoDiaSemana:
    """Obtiene el propósito de un día de la semana"""
    return PROPOSITOS_DIAS_SEMANA.get(dia, PROPOSITOS_DIAS_SEMANA["Lunes"])


def obtener_proposito_mes_hijri(mes: str) -> PropositoMesHijri:
    """Obtiene el propósito de un mes Hijri"""
    return PROPOSITOS_MESES_HIJRI.get(mes, PROPOSITOS_MESES_HIJRI["Muharram"])


def generar_anclas_dia(tiempos: TiemposRezoDia) -> List[dict]:
    """
    Genera las anclas del día (rezo + Estado Cero) con tiempos precisos.
    
    Cada momento tiene:
    - 15 min de rezo
    - 15 min de Estado Cero (después del rezo)
    - Total: 30 min por momento
    """
    from datetime import timedelta
    
    anclas = []
    
    # Fajr
    anclas.append({"tipo": "rezo", "momento": "fajr", "inicio": tiempos.fajr.inicio, "duracion": 15, "proposito": "Purificación alba"})
    anclas.append({"tipo": "estado_cero", "momento": "fajr", "inicio": tiempos.fajr.inicio + timedelta(minutes=15), "duracion": 15, "proposito": PROPOSITOS_ESTADO_CERO[MomentoLiturgico.FAJR].proposito})
    
    # Dhuhr
    anclas.append({"tipo": "rezo", "momento": "dhuhr", "inicio": tiempos.dhuhr.inicio, "duracion": 15, "proposito": "Purificación mediodía"})
    anclas.append({"tipo": "estado_cero", "momento": "dhuhr", "inicio": tiempos.dhuhr.inicio + timedelta(minutes=15), "duracion": 15, "proposito": PROPOSITOS_ESTADO_CERO[MomentoLiturgico.DHUHR].proposito})
    
    # Asr
    anclas.append({"tipo": "rezo", "momento": "asr", "inicio": tiempos.asr.inicio, "duracion": 15, "proposito": "Purificación tarde"})
    anclas.append({"tipo": "estado_cero", "momento": "asr", "inicio": tiempos.asr.inicio + timedelta(minutes=15), "duracion": 15, "proposito": PROPOSITOS_ESTADO_CERO[MomentoLiturgico.ASR].proposito})
    
    # Maghrib (30 min en vez de 15 para ritual completo)
    anclas.append({"tipo": "rezo", "momento": "maghrib", "inicio": tiempos.maghrib.inicio, "duracion": 15, "proposito": "Purificación ocaso"})
    anclas.append({"tipo": "ritual_maghrib", "momento": "maghrib", "inicio": tiempos.maghrib.inicio + timedelta(minutes=15), "duracion": 30, "proposito": PROPOSITOS_ESTADO_CERO[MomentoLiturgico.MAGHRIB].proposito})
    
    # Isha
    anclas.append({"tipo": "rezo", "momento": "isha", "inicio": tiempos.isha.inicio, "duracion": 15, "proposito": "Purificación noche"})
    anclas.append({"tipo": "estado_cero", "momento": "isha", "inicio": tiempos.isha.inicio + timedelta(minutes=15), "duracion": 15, "proposito": PROPOSITOS_ESTADO_CERO[MomentoLiturgico.ISHA].proposito})
    
    return anclas


def calcular_espacio_libre(
    tiempos: TiemposRezoDia,
    no_negociables: List[dict],
    rutinas: List[dict]
) -> tuple[int, float]:
    """
    Calcula el espacio libre del día.
    
    Returns:
        (minutos_libres, porcentaje_libre)
    """
    # Total del día
    total_minutos = 24 * 60  # 1440 minutos
    
    # Anclas (5 momentos × 30 min = 150 min)
    tiempo_anclas = 5 * 30 + 15  # +15 extra para Maghrib (45 min vs 30)
    
    # No-negociables
    tiempo_no_neg = sum([nn.get("duracion", 0) for nn in no_negociables])
    
    # Rutinas
    tiempo_rutinas = sum([r.get("duracion_minutos", 0) for r in rutinas])
    
    # Sueño (8 horas recomendadas)
    tiempo_sueno = 8 * 60
    
    # Asignado
    tiempo_asignado = tiempo_anclas + tiempo_no_neg + tiempo_rutinas + tiempo_sueno
    
    # Libre
    tiempo_libre = total_minutos - tiempo_asignado
    porcentaje_libre = (tiempo_libre / total_minutos) * 100
    
    return tiempo_libre, porcentaje_libre

