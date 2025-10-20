"""
🎵 LEY DE LA OCTAVA - Modelo de Manifestaciones
═══════════════════════════════════════════════════════════════════

Sistema de objetivos basado en la Ley Universal del Siete.

"Toda evolución procede en octavas. Entre cada nota hay un intervalo.
En dos intervalos (MI-FA y SI-DO) la octava pierde momentum naturalmente.
Se requiere un shock consciente para continuar."

- G.I. Gurdjieff, "En Busca del Ser"

Correspondencias:
- 7 notas musicales
- 7 días de la semana
- 7 dimensiones del ser
- 7 colores del arcoíris
- 7 cielos (سبع سماوات)
"""

from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import date, datetime


class Nota(str, Enum):
    """Las 7 notas de la octava"""
    DO = "do"      # Fundamental, inicio, centro
    RE = "re"      # Segundo grado, receptivo
    MI = "mi"      # Tercer grado, activo
    FA = "fa"      # Cuarto grado, conocimiento
    SOL = "sol"    # Quinto grado, expansión
    LA = "la"      # Sexto grado, refinamiento
    SI = "si"      # Séptimo grado, cristalización


class DiaSemanaOctava(str, Enum):
    """Días de la semana como notas"""
    DOMINGO = "domingo"      # DO - Centro, inicio
    LUNES = "lunes"          # RE - Receptivo
    MARTES = "martes"        # MI - Activo
    MIERCOLES = "miercoles"  # FA - Conocimiento
    JUEVES = "jueves"        # SOL - Expansión
    VIERNES = "viernes"      # LA - Refinamiento
    SABADO = "sabado"        # SI - Cristalización


class DimensionOctava(str, Enum):
    """Las 7 dimensiones como notas"""
    ESPIRITUAL = "espiritual"    # DO - Centro sagrado
    BIOLOGICO = "biologico"      # RE - Vitalidad
    FINANCIERO = "financiero"    # MI - Abundancia material
    CONOCIMIENTO = "conocimiento"  # FA - Sabiduría
    RELACIONAL = "relacional"    # SOL - Conexión
    DESARROLLO = "desarrollo"    # LA - Maestría
    CREATIVO = "creativo"        # SI - Belleza


class ColorOctava(str, Enum):
    """Los 7 colores del arcoíris como frecuencias"""
    ROJO = "#DC2626"      # DO - Raíz, fundamento
    NARANJA = "#F97316"   # RE - Vitalidad
    AMARILLO = "#F59E0B"  # MI - Abundancia
    VERDE = "#10B981"     # FA - Crecimiento
    AZUL = "#3B82F6"      # SOL - Comunicación
    INDIGO = "#6366F1"    # LA - Visión
    VIOLETA = "#8B5CF6"   # SI - Trascendencia


class TipoShock(str, Enum):
    """Tipos de shock consciente en intervalos críticos"""
    REVISION_PROFUNDA = "revision_profunda"          # MI-FA (Miércoles)
    CELEBRACION_INTEGRACION = "celebracion_integracion"  # SI-DO (Domingo)


class FrecuenciaNota(BaseModel):
    """Frecuencia matemática de cada nota (ratio al fundamental)"""
    nota: Nota
    frecuencia: float  # Ratio al DO fundamental
    intervalo_siguiente: float  # Distancia a la siguiente nota
    es_intervalo_critico: bool  # True si es MI-FA o SI-DO


# Frecuencias musicales reales (escala justa)
FRECUENCIAS_OCTAVA: Dict[Nota, FrecuenciaNota] = {
    Nota.DO: FrecuenciaNota(
        nota=Nota.DO,
        frecuencia=1.0,
        intervalo_siguiente=9/8,  # 1.125
        es_intervalo_critico=False
    ),
    Nota.RE: FrecuenciaNota(
        nota=Nota.RE,
        frecuencia=9/8,  # 1.125
        intervalo_siguiente=10/9,  # 1.111
        es_intervalo_critico=False
    ),
    Nota.MI: FrecuenciaNota(
        nota=Nota.MI,
        frecuencia=5/4,  # 1.25
        intervalo_siguiente=16/15,  # 1.067 ⚡ INTERVALO CRÍTICO (más pequeño)
        es_intervalo_critico=True
    ),
    Nota.FA: FrecuenciaNota(
        nota=Nota.FA,
        frecuencia=4/3,  # 1.333
        intervalo_siguiente=9/8,  # 1.125
        es_intervalo_critico=False
    ),
    Nota.SOL: FrecuenciaNota(
        nota=Nota.SOL,
        frecuencia=3/2,  # 1.5
        intervalo_siguiente=10/9,  # 1.111
        es_intervalo_critico=False
    ),
    Nota.LA: FrecuenciaNota(
        nota=Nota.LA,
        frecuencia=5/3,  # 1.666
        intervalo_siguiente=9/8,  # 1.125
        es_intervalo_critico=False
    ),
    Nota.SI: FrecuenciaNota(
        nota=Nota.SI,
        frecuencia=15/8,  # 1.875
        intervalo_siguiente=16/15,  # 1.067 ⚡ INTERVALO CRÍTICO (más pequeño)
        es_intervalo_critico=True
    ),
}


# Correspondencia: Nota → Día → Dimensión → Color
CORRESPONDENCIAS_OCTAVA = {
    Nota.DO: {
        "dia": DiaSemanaOctava.DOMINGO,
        "dimension": DimensionOctava.ESPIRITUAL,
        "color": ColorOctava.ROJO,
        "arquetipo": "Sol ☀️",
        "energia": "Central, radiante, iniciadora",
        "fase": "NIYYAH - Intención pura",
        "pregunta": "¿Por QUÉ quiero manifestar esto?",
        "frecuencia_hz": 261.63  # DO central (C4)
    },
    Nota.RE: {
        "dia": DiaSemanaOctava.LUNES,
        "dimension": DimensionOctava.BIOLOGICO,
        "color": ColorOctava.NARANJA,
        "arquetipo": "Luna 🌙",
        "energia": "Receptiva, introspectiva, preparatoria",
        "fase": "RECEPTIVIDAD - Preparación",
        "pregunta": "¿CÓMO mi cuerpo/mente soporta esto?",
        "frecuencia_hz": 293.66  # RE (D4)
    },
    Nota.MI: {
        "dia": DiaSemanaOctava.MARTES,
        "dimension": DimensionOctava.FINANCIERO,
        "color": ColorOctava.AMARILLO,
        "arquetipo": "Marte ⚔️",
        "energia": "Activa, material, concreta",
        "fase": "ACCIÓN - Materialización",
        "pregunta": "¿QUÉ valor genero?",
        "frecuencia_hz": 329.63  # MI (E4)
    },
    Nota.FA: {
        "dia": DiaSemanaOctava.MIERCOLES,
        "dimension": DimensionOctava.CONOCIMIENTO,
        "color": ColorOctava.VERDE,
        "arquetipo": "Mercurio ☿",
        "energia": "Comunicativa, integradora, sintética",
        "fase": "APRENDIZAJE - Comprensión",
        "pregunta": "¿QUÉ estoy comprendiendo?",
        "frecuencia_hz": 349.23,  # FA (F4)
        "shock_requerido": TipoShock.REVISION_PROFUNDA  # ⚡
    },
    Nota.SOL: {
        "dia": DiaSemanaOctava.JUEVES,
        "dimension": DimensionOctava.RELACIONAL,
        "color": ColorOctava.AZUL,
        "arquetipo": "Júpiter ♃",
        "energia": "Expansiva, generosa, compartida",
        "fase": "EXPANSIÓN - Compartir",
        "pregunta": "¿A QUIÉN sirve esto?",
        "frecuencia_hz": 392.00  # SOL (G4)
    },
    Nota.LA: {
        "dia": DiaSemanaOctava.VIERNES,
        "dimension": DimensionOctava.DESARROLLO,
        "color": ColorOctava.INDIGO,
        "arquetipo": "Venus ♀",
        "energia": "Armónica, refinadora, bella",
        "fase": "REFINAMIENTO - Maestría",
        "pregunta": "¿CÓMO puedo dominarlo mejor?",
        "frecuencia_hz": 440.00  # LA (A4 - nota de referencia)
    },
    Nota.SI: {
        "dia": DiaSemanaOctava.SABADO,
        "dimension": DimensionOctava.CREATIVO,
        "color": ColorOctava.VIOLETA,
        "arquetipo": "Saturno ♄",
        "energia": "Cristalizadora, creativa, elevada",
        "fase": "CRISTALIZACIÓN - Belleza",
        "pregunta": "¿CÓMO expreso esto creativamente?",
        "frecuencia_hz": 493.88,  # SI (B4)
        "shock_requerido": TipoShock.CELEBRACION_INTEGRACION  # ⚡
    },
}


class Armonico(BaseModel):
    """
    Armónico de una dimensión en un objetivo.
    
    Cada objetivo contiene TODAS las dimensiones (como armónicos),
    no solo su nota fundamental.
    """
    dimension: DimensionOctava
    nota: Nota
    frecuencia: float  # Ratio al fundamental
    peso: float = Field(ge=0.0, le=1.0)  # 0-1, suma total = 1.0
    pregunta: str
    satisfecho: bool = False  # ¿Este armónico está satisfecho?
    notas: str = ""  # Observaciones específicas


class ShockConsciente(BaseModel):
    """
    Shock consciente requerido en intervalos críticos.
    
    Sin estos shocks, la octava pierde momentum y no completa.
    """
    tipo: TipoShock
    intervalo: str  # "MI-FA" o "SI-DO"
    dia: DiaSemanaOctava
    fecha_programada: Optional[date] = None
    realizado: bool = False
    notas: str = ""
    
    # Acciones específicas del shock
    accion_sugerida: str
    pregunta_clave: str
    duracion_minutos: int = 30  # Duración del shock


class FaseSemanal(BaseModel):
    """Fase de la semana en la evolución del objetivo"""
    dia: DiaSemanaOctava
    nota: Nota
    fase: str  # "NIYYAH", "RECEPTIVIDAD", "ACCIÓN", etc.
    actividad_sugerida: str
    es_intervalo_critico: bool
    shock_requerido: Optional[TipoShock] = None
    completada: bool = False


class ObjetivoOctava(BaseModel):
    """
    Objetivo que evoluciona según la Ley de la Octava.
    
    Estructura:
    - Nota fundamental (dimensión primaria)
    - 7 armónicos (todas las dimensiones)
    - Plan semanal (7 fases)
    - Shocks conscientes
    - Tracking de octavas
    """
    id: str
    nombre: str
    descripcion: str
    
    # Nota fundamental
    nota_fundamental: Nota
    dimension_primaria: DimensionOctava
    frecuencia_base: float
    
    # Armónicos (todas las dimensiones contenidas)
    armonicos: Dict[DimensionOctava, Armonico]
    
    # Temporalidad
    fecha_inicio: date
    fecha_objetivo: date
    octava_actual: int = 1  # 1, 2, 3... (cada semana es una octava)
    nivel_frecuencia: float = 1.0  # 1.0, 2.0, 4.0, 8.0... (dobla cada octava)
    
    # Plan semanal
    plan_octava: Dict[DiaSemanaOctava, FaseSemanal]
    
    # Shocks conscientes
    shocks: List[ShockConsciente]
    
    # Progreso
    completitud_octava: float = 0.0  # 0-100%
    progreso_general: float = 0.0  # 0-100%
    estado: str = "activa"  # activa, pausada, completada, abandonada
    
    # Práctica diaria
    practica_diaria: str
    resultado_observable: str
    
    # Metadata
    creado: datetime = Field(default_factory=datetime.now)
    ultima_actualizacion: datetime = Field(default_factory=datetime.now)


class AnalisisArmonicos(BaseModel):
    """
    Análisis de qué armónicos están satisfechos y cuáles no.
    
    Permite detectar desequilibrios:
    - Si solo la nota fundamental está satisfecha → fragmentación
    - Si todos los armónicos resuenan → coherencia holística
    """
    objetivo_id: str
    nota_fundamental: Nota
    armonicos_satisfechos: List[DimensionOctava]
    armonicos_insatisfechos: List[DimensionOctava]
    coherencia_armonica: float  # 0-100%
    recomendaciones: List[str]


class EstadoOctava(BaseModel):
    """
    Estado actual de la octava en progreso.
    
    Indica:
    - En qué nota/día estamos
    - Si se acerca un intervalo crítico
    - Si el shock fue aplicado
    """
    objetivo_id: str
    semana_actual: int
    dia_actual: DiaSemanaOctava
    nota_actual: Nota
    
    # Intervalos críticos
    proximo_intervalo_critico: Optional[str] = None  # "MI-FA" o "SI-DO"
    dias_hasta_shock: Optional[int] = None
    shock_pendiente: Optional[ShockConsciente] = None
    
    # Progreso de la semana
    dias_completados: int  # 0-7
    completitud_octava: float  # 0-100%
    
    # Alerta
    requiere_atencion: bool = False
    mensaje_alerta: Optional[str] = None


# ═══════════════════════════════════════════════════════════════
# FUNCIONES HELPER
# ═══════════════════════════════════════════════════════════════

def obtener_correspondencia(nota: Nota) -> Dict:
    """Obtiene todas las correspondencias de una nota"""
    return CORRESPONDENCIAS_OCTAVA[nota]


def calcular_frecuencia_octava(nota: Nota, octava: int) -> float:
    """
    Calcula la frecuencia de una nota en una octava específica.
    
    Octava 1: frecuencia base
    Octava 2: frecuencia × 2
    Octava 3: frecuencia × 4
    Octava N: frecuencia × 2^(N-1)
    """
    freq_base = FRECUENCIAS_OCTAVA[nota].frecuencia
    return freq_base * (2 ** (octava - 1))


def es_intervalo_critico(nota_actual: Nota) -> bool:
    """Verifica si la nota actual está antes de un intervalo crítico"""
    return nota_actual in [Nota.MI, Nota.SI]


def obtener_shock_requerido(nota_actual: Nota) -> Optional[TipoShock]:
    """Retorna el tipo de shock requerido si estamos en intervalo crítico"""
    if nota_actual == Nota.MI:
        return TipoShock.REVISION_PROFUNDA
    elif nota_actual == Nota.SI:
        return TipoShock.CELEBRACION_INTEGRACION
    return None


def generar_plan_semanal_octava(
    objetivo: str,
    nota_fundamental: Nota,
    fecha_inicio: date
) -> Dict[DiaSemanaOctava, FaseSemanal]:
    """
    Genera el plan semanal para un objetivo según la Ley de la Octava.
    
    Cada día trabaja una nota/dimensión específica.
    Incluye los 2 shocks conscientes.
    """
    from datetime import timedelta
    
    plan: Dict[DiaSemanaOctava, FaseSemanal] = {}
    
    notas_secuencia = [Nota.DO, Nota.RE, Nota.MI, Nota.FA, Nota.SOL, Nota.LA, Nota.SI]
    dias_secuencia = [
        DiaSemanaOctava.DOMINGO,
        DiaSemanaOctava.LUNES,
        DiaSemanaOctava.MARTES,
        DiaSemanaOctava.MIERCOLES,
        DiaSemanaOctava.JUEVES,
        DiaSemanaOctava.VIERNES,
        DiaSemanaOctava.SABADO
    ]
    
    for i, (dia, nota) in enumerate(zip(dias_secuencia, notas_secuencia)):
        corresp = CORRESPONDENCIAS_OCTAVA[nota]
        
        # Determinar si es intervalo crítico
        es_critico = nota in [Nota.MI, Nota.SI]
        shock = obtener_shock_requerido(nota) if es_critico else None
        
        # Generar actividad sugerida
        if nota == Nota.DO:
            actividad = f"Clarificar intención profunda de '{objetivo}'"
        elif nota == Nota.RE:
            actividad = f"Preparar cuerpo/mente para '{objetivo}'"
        elif nota == Nota.MI:
            actividad = f"Primera acción material de '{objetivo}'"
        elif nota == Nota.FA:
            actividad = f"⚡ SHOCK: Revisar '{objetivo}' profundamente"
        elif nota == Nota.SOL:
            actividad = f"Compartir/enseñar '{objetivo}'"
        elif nota == Nota.LA:
            actividad = f"Refinar maestría de '{objetivo}'"
        elif nota == Nota.SI:
            actividad = f"⚡ SHOCK: Crear belleza con '{objetivo}'"
        else:
            actividad = f"Trabajar en '{objetivo}'"
        
        plan[dia] = FaseSemanal(
            dia=dia,
            nota=nota,
            fase=corresp["fase"],
            actividad_sugerida=actividad,
            es_intervalo_critico=es_critico,
            shock_requerido=shock,
            completada=False
        )
    
    return plan


def generar_armonicos_iniciales(
    dimension_primaria: DimensionOctava,
    objetivo_nombre: str
) -> Dict[DimensionOctava, Armonico]:
    """
    Genera los 7 armónicos de un objetivo.
    
    La dimensión primaria tiene peso mayor (0.30).
    Las otras 6 dimensiones tienen pesos menores pero están presentes.
    """
    armonicos: Dict[DimensionOctava, Armonico] = {}
    
    # Pesos predeterminados
    peso_primaria = 0.30
    peso_secundarias = (1.0 - peso_primaria) / 6  # ~0.117 cada una
    
    for dimension in DimensionOctava:
        # Encontrar la nota correspondiente a esta dimensión
        nota_dim = None
        for nota, corresp in CORRESPONDENCIAS_OCTAVA.items():
            if corresp["dimension"] == dimension:
                nota_dim = nota
                break
        
        peso = peso_primaria if dimension == dimension_primaria else peso_secundarias
        
        armonicos[dimension] = Armonico(
            dimension=dimension,
            nota=nota_dim,
            frecuencia=FRECUENCIAS_OCTAVA[nota_dim].frecuencia,
            peso=peso,
            pregunta=CORRESPONDENCIAS_OCTAVA[nota_dim]["pregunta"],
            satisfecho=False
        )
    
    return armonicos


def calcular_coherencia_armonica(armonicos: Dict[DimensionOctava, Armonico]) -> float:
    """
    Calcula la coherencia armónica (% de armónicos satisfechos).
    
    100% = todas las dimensiones alineadas (resonancia perfecta)
    0% = solo la fundamental (fragmentación)
    """
    if not armonicos:
        return 0.0
    
    satisfechos = sum(1 for arm in armonicos.values() if arm.satisfecho)
    total = len(armonicos)
    
    return (satisfechos / total) * 100


def detectar_shock_pendiente(
    plan_octava: Dict[DiaSemanaOctava, FaseSemanal],
    dia_hoy: DiaSemanaOctava
) -> Optional[ShockConsciente]:
    """
    Detecta si hay un shock consciente pendiente para hoy o próximo.
    """
    fase_hoy = plan_octava.get(dia_hoy)
    
    if fase_hoy and fase_hoy.shock_requerido and not fase_hoy.completada:
        corresp = CORRESPONDENCIAS_OCTAVA[fase_hoy.nota]
        
        if fase_hoy.shock_requerido == TipoShock.REVISION_PROFUNDA:
            return ShockConsciente(
                tipo=TipoShock.REVISION_PROFUNDA,
                intervalo="MI-FA",
                dia=DiaSemanaOctava.MIERCOLES,
                accion_sugerida="Revisar intención profunda. ¿Sigue resonando? Ajustar si es necesario.",
                pregunta_clave="¿La intención original sigue viva en mí?",
                duracion_minutos=30
            )
        elif fase_hoy.shock_requerido == TipoShock.CELEBRACION_INTEGRACION:
            return ShockConsciente(
                tipo=TipoShock.CELEBRACION_INTEGRACION,
                intervalo="SI-DO",
                dia=DiaSemanaOctava.DOMINGO,
                accion_sugerida="Celebrar lo logrado (Shukr). Integrar aprendizaje. Visionar siguiente octava.",
                pregunta_clave="¿Qué he integrado esta semana? ¿Qué emerge para la siguiente?",
                duracion_minutos=45
            )
    
    return None

