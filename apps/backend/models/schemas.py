from __future__ import annotations

from datetime import datetime, date
from enum import Enum
from typing import List, Optional, Any

from pydantic import BaseModel


class MomentoLiturgico(str, Enum):
    FAJR = "fajr"
    DHUHR = "dhuhr"
    ASR = "asr"
    MAGHRIB = "maghrib"
    ISHA = "isha"


class SensacionSacral(str, Enum):
    EXPANSION = "expansion"
    CONTRACCION = "contraccion"


class TipoNoNegociable(str, Enum):
    BIOLOGICO = "biologico"
    ESPIRITUAL = "espiritual"
    FINANCIERO = "financiero"


class PropositoEstadoCero(BaseModel):
    """Propósito específico de cada Estado Cero"""
    momento: MomentoLiturgico
    proposito: str
    enfoque: str
    resultado_esperado: str
    actualiza_espejo: str


class PropositoDiaSemana(BaseModel):
    """Propósito de cada día de la semana"""
    dia: str  # "Lunes", "Martes", etc.
    proposito: str  # "Iniciar", "Construir", etc.
    energia: str  # "Expansión", "Acción", etc.
    enfoque: str  # "Nuevos comienzos", "Momentum", etc.


class PropositoMesHijri(BaseModel):
    """Propósito de cada mes Hijri"""
    mes: str
    proposito: str
    cualidad: str


class TiempoRezo(BaseModel):
    inicio: datetime
    fin: datetime
    ventana_estado_cero: datetime


class TiemposRezoDia(BaseModel):
    fecha: date
    fajr: TiempoRezo
    dhuhr: TiempoRezo
    asr: TiempoRezo
    maghrib: TiempoRezo
    isha: TiempoRezo


class VerificacionMomento(BaseModel):
    es_momento: bool
    momento: Optional[MomentoLiturgico] = None
    ventana_inicio: Optional[datetime] = None
    ventana_fin: Optional[datetime] = None
    minutos_restantes: Optional[int] = None
    fuera_de_ventana: bool = False  # True si la ventana ya pasó pero se permite acceso


class ProximoEstadoCero(BaseModel):
    momento: MomentoLiturgico
    hora: datetime
    countdown: str


class DiaHijri(BaseModel):
    nombre: str = ""
    proposito: str = ""


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    proximo_estado_cero: ProximoEstadoCero
    dia_actual: Any


class PreguntaBinaria(BaseModel):
    id: str
    pregunta: str
    contexto: str
    categoria: str


class RespuestaSacral(BaseModel):
    pregunta_id: str
    sensacion: SensacionSacral
    intensidad: int
    nota: Optional[str] = ""
    timestamp: Optional[datetime] = None


class AccionConcreta(BaseModel):
    descripcion: str
    resultado_observable: str
    duracion_estimada: str
    energia_requerida: int
    rol: Optional[str] = None
    notas: Optional[str] = ""


class MensajeChat(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None


class ContextoTemporal(BaseModel):
    momento_liturgico: MomentoLiturgico
    dia_semana: str
    mes_hijri: str
    cualidad_momento: str = ""
    cualidad_mes: str = ""


class ContextoBiologico(BaseModel):
    energia_actual: int = 3
    hrv: Optional[float] = None
    luz_solar_hoy: bool = False
    ejercicio_hoy: bool = False


class ContextoFinanciero(BaseModel):
    runway_meses: float = 6.0
    urgencia_financiera: bool = False
    proyectos_activos: List[str] = []


class ContextoConocimiento(BaseModel):
    capturas_sin_procesar: int = 0
    insights_listos: int = 0


class ContextoCompleto(BaseModel):
    temporal: ContextoTemporal
    biologico: ContextoBiologico
    financiero: ContextoFinanciero
    conocimiento: ContextoConocimiento
    tiempo_disponible_hoy: int


class EstadoCeroCompleto(BaseModel):
    id: str
    fecha: datetime
    momento: MomentoLiturgico
    contexto: ContextoCompleto
    preguntas: List[PreguntaBinaria]
    respuestas: List[RespuestaSacral]
    direccion_emergente: str
    accion_tangible: AccionConcreta
    chat_clarificacion: List[MensajeChat]
    completado: bool


class IniciarEstadoCeroRequest(BaseModel):
    momento: MomentoLiturgico
    # Inputs opcionales para sistema de 7 capas
    energia: Optional[int] = None  # 1-5
    calidad_sueno: Optional[int] = None  # 1-5
    resonancia_corporal: Optional[str] = None  # tension/fatiga/neutral/fluido/vibrante
    estado_emocional: Optional[str] = None  # calma/ansioso/entusiasmado/apagado/neutro
    intensidad_emocional: Optional[int] = None  # 1-5


class ResponderPreguntaRequest(BaseModel):
    pregunta_id: str
    sensacion: SensacionSacral
    intensidad: int
    nota: Optional[str] = ""


class ChatClarificacionRequest(BaseModel):
    mensaje: str


class NoNegociable(BaseModel):
    tipo: str
    nombre: str
    ventana: str
    duracion_min: str
    prioridad: str
    razon: str
    completado: bool = False
    hora_completado: Optional[datetime] = None
    en_riesgo: bool = False


class BloqueTiempo(BaseModel):
    id: str
    inicio_aprox: str
    duracion: str
    actividad: str
    rol: Optional[str] = None
    energia_optima: int = 3
    flexible: bool = True
    opciones_alternativas: List[str] = []


class PuntoDecision(BaseModel):
    momento: str
    pregunta: str
    criterio: str
    opciones: List[str]


class AnclaDia(BaseModel):
    """Ancla fija del día (rezo + Estado Cero)"""
    tipo: str  # "rezo", "estado_cero", "ritual_maghrib"
    momento: str  # "fajr", "dhuhr", etc.
    inicio: datetime
    duracion: int  # minutos
    proposito: Optional[str] = None


class EstructuraDia(BaseModel):
    """
    Estructura base de un día específico.
    Define anclas, no-negociables y espacio disponible.
    """
    fecha: date
    dia_semana: str  # "Lunes", "Martes", etc.
    proposito_dia: str  # "Iniciar", "Construir", etc.
    energia_dia: str  # "Expansión", "Acción", etc.
    
    # Tiempos litúrgicos precisos
    tiempos_liturgicos: TiemposRezoDia
    
    # ANCLAS (intocables)
    anclas: List[AnclaDia]  # Rezo + Estados Cero
    
    # NO-NEGOCIABLES (pueden ajustar hora dentro de ventana)
    no_negociables_dia: List[NoNegociable]
    
    # Espacio disponible
    espacio_libre_minutos: int
    espacio_libre_porcentaje: float
    
    # Del perfil personal
    rutinas_dia: List[Any] = []  # RutinaDeportiva del día
    proyectos_sugeridos: List[Any] = []
    aprendizaje_sugerido: List[Any] = []
    
    # Detecciones
    conflictos: List[str] = []
    sinergias: List[str] = []


class JornadaAlBordeCaos(BaseModel):
    fecha: date
    accion_principal: AccionConcreta
    bloques_sugeridos: List[BloqueTiempo]
    puntos_decision: List[PuntoDecision]
    espacio_emergencia: int
    no_negociables: List[NoNegociable]
    flexible: bool
    ultima_actualizacion: datetime


class ReporteDiario(BaseModel):
    fecha: date
    estados_cero_completados: int
    sesiones: List[dict]
    no_negociables_cumplidos: int
    no_negociables_totales: int
    biologia: dict
    finanzas: dict
    conocimiento: dict
    resonancias: List[str]
    obstrucciones: List[str]
    semilla_mañana: str
    generado_timestamp: datetime


# Schemas para API de agentes
class ChatOrquestadorRequest(BaseModel):
    mensaje: str


class AjustePlanRequest(BaseModel):
    ajustes: dict


class ChatClarificacionRequest(BaseModel):
    mensaje: str


# ============================================
# PERFIL PERSONAL Y DASHBOARD DE ENTRELAZAMIENTO
# ============================================

class RutinaDeportiva(BaseModel):
    """Configuración de rutina deportiva semanal"""
    nombre: str
    dias_semana: List[str]  # ["lunes", "miércoles", "viernes"]
    hora_preferida: str
    duracion_minutos: int
    tipo: str  # "fuerza", "cardio", "movilidad", "yoga"
    intensidad: int  # 1-5
    notas: Optional[str] = ""


class ComidaConfiguracion(BaseModel):
    """Configuración de sistema de comidas"""
    tipo: str  # "desayuno", "almuerzo", "cena", "snack"
    hora_aproximada: str
    duracion_preparacion: int  # minutos
    recetas_preferidas: List[str]
    restricciones: List[str] = []
    batch_cooking: bool = False
    dias_batch: Optional[List[str]] = None


class PresupuestoCategoria(BaseModel):
    """Categoría de presupuesto mensual"""
    nombre: str
    asignado_mensual: float
    gastado_mes_actual: float = 0.0
    prioridad: int  # 1-5
    notas: Optional[str] = ""


class TemaAprendizaje(BaseModel):
    """Tema de aprendizaje activo"""
    nombre: str
    dominio: str  # "tecnología", "filosofía", "arte", etc.
    prioridad: int  # 1-5
    tiempo_semanal_deseado: int  # minutos
    recursos: List[str] = []
    progreso_porcentaje: float = 0.0
    fecha_inicio: Optional[date] = None
    fecha_objetivo: Optional[date] = None


class ProyectoDesarrollo(BaseModel):
    """Proyecto de desarrollo activo"""
    nombre: str
    tipo: str  # "código", "escritura", "diseño", "investigación"
    estado: str  # "activo", "pausado", "completado"
    prioridad: int  # 1-5
    horas_semanales_deseadas: int
    deadline: Optional[date] = None
    hitos: List[str] = []
    notas: Optional[str] = ""


class InversionAsunto(BaseModel):
    """Asunto de inversión o gestión financiera"""
    nombre: str
    tipo: str  # "investigación", "seguimiento", "decisión_pendiente"
    monto_involucrado: Optional[float] = None
    fecha_decision: Optional[date] = None
    prioridad: int  # 1-5
    notas: Optional[str] = ""


class PerfilPersonal(BaseModel):
    """Perfil completo del usuario con todas sus configuraciones"""
    # Información básica
    nombre: str
    timezone: str = "Europe/Madrid"
    
    # Rutinas deportivas
    rutinas_deportivas: List[RutinaDeportiva] = []
    
    # Sistema de comidas
    sistema_comidas: List[ComidaConfiguracion] = []
    
    # Gestión financiera
    presupuesto_mensual: List[PresupuestoCategoria] = []
    dia_compra_semanal: Optional[str] = None  # "sábado"
    
    # Aprendizaje
    temas_aprendizaje: List[TemaAprendizaje] = []
    
    # Desarrollo y proyectos
    proyectos_desarrollo: List[ProyectoDesarrollo] = []
    
    # Inversiones y asuntos financieros
    inversiones_asuntos: List[InversionAsunto] = []
    
    # Documentación
    sistemas_documentacion: List[str] = ["obsidian"]  # "obsidian", "anytype"
    
    # Preferencias
    energia_pico_manana: bool = True
    prefiere_batch_cooking: bool = False
    
    # Metadata
    creado: datetime
    actualizado: datetime


class EntrelazamientoDia(BaseModel):
    """Entrelazamiento diario de todos los aspectos"""
    fecha: date
    
    # Deportes del día
    deportes_hoy: List[dict]  # {nombre, hora_sugerida, completado}
    
    # Comidas del día
    comidas_hoy: List[dict]  # {tipo, hora, tiempo_cocinar, receta_sugerida}
    
    # Finanzas del día
    necesita_compra: bool = False
    presupuesto_disponible: float = 0.0
    categorias_alerta: List[str] = []
    
    # Aprendizaje del día
    temas_sugeridos: List[dict]  # {tema, tiempo_sugerido, razon}
    
    # Desarrollo del día
    proyectos_sugeridos: List[dict]  # {proyecto, tiempo_sugerido, hitos_hoy}
    
    # Inversiones del día
    asuntos_revisar: List[dict]  # {asunto, accion_sugerida}
    
    # Síntesis de entrelazamiento
    conflictos_detectados: List[str] = []
    sinergias_detectadas: List[str] = []
    recomendacion_principal: str = ""
    energia_requerida_total: int = 0


class DashboardEntrelazamiento(BaseModel):
    """Dashboard completo de entrelazamiento semanal"""
    semana_inicio: date
    semana_fin: date
    
    # Vista semanal
    dias_semana: List[EntrelazamientoDia]
    
    # Resumen deportivo
    sesiones_deportivas_semana: int
    objetivo_cumplido_deporte: bool
    
    # Resumen alimentación
    batch_cooking_planificado: List[dict]  # {dia, recetas, tiempo_total}
    compra_necesaria: List[dict]  # {ingrediente, cantidad, presupuesto}
    
    # Resumen financiero
    gasto_semana_proyectado: float
    presupuesto_disponible: float
    alertas_financieras: List[str] = []
    
    # Resumen aprendizaje
    horas_aprendizaje_semana: float
    temas_prioridad: List[str]
    
    # Resumen desarrollo
    horas_desarrollo_semana: float
    proyectos_avance: List[dict]
    
    # Resumen inversiones
    decisiones_pendientes: List[dict]
    
    # Entrelazamiento inteligente
    patron_energia_semanal: dict
    sugerencias_optimizacion: List[str]
    espacios_emergencia: List[dict]  # {dia, hora, duracion}


