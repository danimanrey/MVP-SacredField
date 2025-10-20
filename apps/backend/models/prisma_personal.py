"""
🔮 Prisma Personal: La Lente Única del Usuario
================================================

Este módulo define la configuración PROFUNDA que el organismo necesita
para reflejar correctamente en el espejo diario.

NO es "preferencias". Es TU CÓDIGO GENÉTICO OPERATIVO.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date
from enum import Enum


# ═══════════════════════════════════════════════════════════════════
# DISEÑO HUMANO: Tu Autoridad Operativa
# ═══════════════════════════════════════════════════════════════════

class TipoHumanDesign(str, Enum):
    MANIFESTOR = "manifestor"
    GENERADOR = "generador"
    GENERADOR_MANIFESTANTE = "generador_manifestante"
    PROYECTOR = "proyector"
    REFLECTOR = "reflector"


class AutoridadInterna(str, Enum):
    SACRAL = "sacral"  # Respuesta visceral instantánea
    EMOCIONAL = "emocional"  # Requiere ola emocional completa
    ESPLENICA = "esplenica"  # Intuición en el momento
    EGO = "ego"  # Fuerza de voluntad
    SELF_PROYECTADO = "self_proyectado"  # Expresión verbal
    MENTAL = "mental"  # Entorno y consejo (no para decidir)
    LUNAR = "lunar"  # Ciclo de 28 días


class EstrategiaVital(str, Enum):
    INFORMAR = "informar"  # Manifestor
    RESPONDER = "responder"  # Generador
    ESPERAR_INVITACION = "esperar_invitacion"  # Proyector
    ESPERAR_CICLO_LUNAR = "esperar_ciclo_lunar"  # Reflector


class DiseñoHumano(BaseModel):
    """Tu blueprint energético"""
    tipo: TipoHumanDesign
    autoridad: AutoridadInterna
    estrategia: EstrategiaVital
    perfil: str = Field(default="", description="Ej: 5/1, 3/5, etc.")
    centros_definidos: List[str] = Field(default_factory=list, description="Centros con definición constante")
    canales_activos: List[str] = Field(default_factory=list)
    
    # Interpretación operativa
    patron_energia: str = Field(default="", description="Cómo fluye tu energía")
    forma_correcta_decidir: str = Field(default="", description="Cómo tomas decisiones correctas")
    trampa_mental: str = Field(default="", description="Qué evitar")


# ═══════════════════════════════════════════════════════════════════
# PERSONALIDAD: MBTI + Eneagrama
# ═══════════════════════════════════════════════════════════════════

class TipoMBTI(str, Enum):
    # 16 tipos
    INTJ = "INTJ"
    INTP = "INTP"
    ENTJ = "ENTJ"
    ENTP = "ENTP"
    INFJ = "INFJ"
    INFP = "INFP"
    ENFJ = "ENFJ"
    ENFP = "ENFP"
    ISTJ = "ISTJ"
    ISFJ = "ISFJ"
    ESTJ = "ESTJ"
    ESFJ = "ESFJ"
    ISTP = "ISTP"
    ISFP = "ISFP"
    ESTP = "ESTP"
    ESFP = "ESFP"


class TipoEneagrama(str, Enum):
    TIPO_1 = "1"  # Perfeccionista
    TIPO_2 = "2"  # Ayudador
    TIPO_3 = "3"  # Triunfador
    TIPO_4 = "4"  # Individualista
    TIPO_5 = "5"  # Investigador
    TIPO_6 = "6"  # Leal
    TIPO_7 = "7"  # Entusiasta
    TIPO_8 = "8"  # Desafiador
    TIPO_9 = "9"  # Pacificador


class PerfilPsicologico(BaseModel):
    """Tu estructura cognitiva y emocional"""
    mbti: TipoMBTI
    eneagrama_base: TipoEneagrama
    alas: List[TipoEneagrama] = Field(default_factory=list, description="Ej: 5 ala 4 y 6")
    
    # Interpretación operativa
    patron_aprendizaje: str = Field(
        default="",
        description="Cómo aprendes mejor (ENTP: exploración conceptual, conexiones, debate interno)"
    )
    motivacion_profunda: str = Field(
        default="",
        description="Qué te mueve realmente (5: comprensión, autonomía, dominio)"
    )
    punto_ciego: str = Field(
        default="",
        description="Qué tiendes a ignorar (5: necesidades corporales, conexión emocional)"
    )
    trabajo_integracion: str = Field(
        default="",
        description="Hacia dónde crecer (5→8: acción sin sobre-análisis)"
    )


# ═══════════════════════════════════════════════════════════════════
# MANIFESTACIONES: Metas y Visión
# ═══════════════════════════════════════════════════════════════════

class NivelManifestacion(str, Enum):
    DIARIO = "diario"  # Prácticas repetidas hoy
    SEMANAL = "semanal"  # Hábitos a consolidar esta semana
    MENSUAL = "mensual"  # Hitos a alcanzar este mes
    TRIMESTRAL = "trimestral"  # Proyectos en curso (3 meses)
    ANUAL = "anual"  # Objetivos del año
    QUINQUENAL = "quinquenal"  # Visión 5 años
    DECADAL = "decadal"  # Legado 10 años


class DimensionVida(str, Enum):
    BIOLOGICO = "biologico"  # Cuerpo, energía, salud
    FINANCIERO = "financiero"  # Abundancia, runway, generación
    DESARROLLO = "desarrollo"  # Habilidades técnicas, maestría
    CONOCIMIENTO = "conocimiento"  # Aprendizaje, síntesis, insights
    RELACIONES = "relaciones"  # Pareja, familia, comunidad
    ESPIRITUAL = "espiritual"  # Conexión, propósito, trascendencia
    CREATIVO = "creativo"  # Expresión, arte, creación


class Manifestacion(BaseModel):
    """Una manifestación específica en proceso"""
    id: str
    dimension: DimensionVida
    nivel: NivelManifestacion
    
    # La manifestación
    vision: str = Field(description="Qué estás manifestando (ej: 'Dominio de arquitecturas multi-agente')")
    resultado_observable: str = Field(description="Cómo sabes que se materializó")
    
    # Proceso de materialización
    practica_diaria: Optional[str] = None  # Repetición que lo materializa
    frecuencia_minima: str = Field(default="diaria", description="Ej: 'diaria', '3x/semana'")
    tiempo_estimado_materializacion: str = Field(default="", description="Ej: '3 meses', '1 año'")
    
    # Tracking
    fecha_inicio: date
    ultimo_avance: Optional[date] = None
    progreso_estimado: int = Field(default=0, ge=0, le=100, description="% completado")
    
    # Conexiones
    se_integra_con: List[str] = Field(default_factory=list, description="IDs de otras manifestaciones relacionadas")
    depende_de: List[str] = Field(default_factory=list, description="IDs de manifestaciones previas necesarias")


# ═══════════════════════════════════════════════════════════════════
# SISTEMA VIVO DE CONOCIMIENTO
# ═══════════════════════════════════════════════════════════════════

class MetodoCaptura(str, Enum):
    OBSIDIAN = "obsidian"
    ANYTYPE = "anytype"
    VOZ = "voz"  # Transcripción automática
    MANUAL = "manual"  # Durante Estado Cero


class TipoNota(str, Enum):
    FLEETING = "fleeting"  # Captura rápida, se procesa después
    LITERATURE = "literature"  # De fuentes externas (libros, artículos)
    PERMANENT = "permanent"  # Insight destilado en tus palabras
    MOC = "moc"  # Map of Content (índice de conceptos)
    PROJECT = "project"  # Nota de proyecto activo


class EstructuraConocimiento(BaseModel):
    """Cómo estructuras y metabolizas conocimiento"""
    
    # Métodos preferidos
    captura_primaria: MetodoCaptura
    captura_secundaria: Optional[MetodoCaptura] = None
    
    # Zettelkasten / Segundo Cerebro
    usa_zettelkasten: bool = Field(default=True)
    sistema_vinculacion: Literal["tags", "backlinks", "folders", "mixto"] = "backlinks"
    
    # Procesamiento
    frecuencia_revision: str = Field(default="semanal", description="Cuándo procesas notas fleeting")
    umbral_nota_permanente: str = Field(
        default="",
        description="Cuándo una nota fleeting se vuelve permanent (ej: 'al conectar con 3+ ideas')"
    )
    
    # Metabolización (aprender a aprender)
    practica_sintesis_semanal: bool = Field(default=True, description="Sintetizar aprendizajes cada domingo")
    genera_mocs_automaticos: bool = Field(default=True, description="El organismo sugiere MOCs")
    conecta_insights_automatico: bool = Field(default=True, description="Encuentra conexiones entre notas")


class MetodoAprendizaje(BaseModel):
    """Cómo aprendes mejor (aprender a aprender)"""
    
    # Modalidad
    modalidad_preferida: Literal["visual", "auditivo", "kinestesico", "lectura_escritura"] = "lectura_escritura"
    profundidad_vs_amplitud: int = Field(
        default=5,
        ge=1,
        le=10,
        description="1=máxima amplitud, 10=máxima profundidad. ENTP-5: ~7"
    )
    
    # Estrategias efectivas
    estrategias_efectivas: List[str] = Field(
        default_factory=list,
        description=[
            "Exploración conceptual libre",
            "Enseñar a otros (método Feynman)",
            "Construcción de frameworks",
            "Debate interno / externo",
            "Implementación práctica inmediata"
        ]
    )
    
    # Contextos óptimos
    mejor_momento_aprendizaje: str = Field(default="mañana temprano", description="Según ritmo circadiano")
    duracion_optima_sesion: int = Field(default=90, description="Minutos de concentración profunda")
    requiere_silencio: bool = Field(default=True)
    
    # Señales de comprensión real
    indicadores_dominio: List[str] = Field(
        default_factory=list,
        description=[
            "Puedo explicarlo a un niño de 10 años",
            "Puedo implementarlo sin mirar referencias",
            "Puedo conectarlo con 5+ conceptos previos",
            "Puedo prever implicaciones y limitaciones"
        ]
    )


# ═══════════════════════════════════════════════════════════════════
# METADATOS PARA EL ORGANISMO
# ═══════════════════════════════════════════════════════════════════

class MetadatosOperativos(BaseModel):
    """
    Metadatos que el organismo extrae y metaboliza automáticamente.
    NO los configuras manualmente. El organismo los aprende.
    """
    
    # Patrones biológicos observados
    pico_energia_real: str = Field(default="", description="Ej: '09:00-12:00' (aprendido de datos)")
    duracion_flujo_promedio: int = Field(default=0, description="Minutos de flujo profundo sostenido")
    dias_alta_expansion: List[str] = Field(default_factory=list, description="Qué días de la semana eres más expansivo")
    
    # Patrones de decisión observados
    ratio_expansion_contraccion: float = Field(default=0.0, description="Promedio histórico")
    categorias_maxima_expansion: List[str] = Field(default_factory=list, description="Qué categorías generan más expansión")
    decisiones_recurrentes: List[str] = Field(default_factory=list, description="Qué decides repetidamente (automatizar)")
    
    # Patrones de conocimiento observados
    temas_mas_explorados: List[str] = Field(default_factory=list)
    frecuencia_captura_notas: str = Field(default="", description="Cuántas notas/día en promedio")
    ratio_captura_vs_sintesis: float = Field(default=0.0, description="Capturas vs notas permanentes")
    
    # Patrones de manifestación observados
    tasa_completitud_manifestaciones: float = Field(default=0.0, description="% de manifestaciones materializadas")
    tiempo_promedio_materializacion: str = Field(default="", description="Cuánto tardas en materializar")
    
    # Última actualización
    ultima_actualizacion: date = Field(default_factory=date.today)
    dias_datos: int = Field(default=0, description="Días de datos recopilados")


# ═══════════════════════════════════════════════════════════════════
# PRISMA PERSONAL COMPLETO
# ═══════════════════════════════════════════════════════════════════

class PrismaPersonal(BaseModel):
    """
    El Prisma Personal es la lente única desde la cual el usuario
    refracta la realidad en el espejo diario.
    
    Todo el organismo se configura según este prisma.
    """
    
    # Identidad
    nombre: str
    fecha_nacimiento: date
    
    # Tu código genético operativo
    diseño_humano: DiseñoHumano
    perfil_psicologico: PerfilPsicologico
    
    # Tus manifestaciones en proceso
    manifestaciones: List[Manifestacion] = Field(default_factory=list)
    
    # Tu sistema de conocimiento
    estructura_conocimiento: EstructuraConocimiento
    metodo_aprendizaje: MetodoAprendizaje
    
    # Metadatos que el organismo aprende
    metadatos_operativos: MetadatosOperativos = Field(default_factory=MetadatosOperativos)
    
    # Meta
    creado: date = Field(default_factory=date.today)
    actualizado: date = Field(default_factory=date.today)
    version: str = Field(default="1.0.0")


# ═══════════════════════════════════════════════════════════════════
# FUNCIONES AUXILIARES
# ═══════════════════════════════════════════════════════════════════

def crear_prisma_ejemplo_entp_5() -> PrismaPersonal:
    """
    Crea un prisma personal de ejemplo para ENTP-A, Generador Sacral, 5 ala 4/6
    """
    
    return PrismaPersonal(
        nombre="Usuario Ejemplo",
        fecha_nacimiento=date(1990, 1, 1),
        
        diseño_humano=DiseñoHumano(
            tipo=TipoHumanDesign.GENERADOR,
            autoridad=AutoridadInterna.SACRAL,
            estrategia=EstrategiaVital.RESPONDER,
            perfil="5/1",
            centros_definidos=["Sacral", "Garganta", "Raíz"],
            canales_activos=["20-34"],
            patron_energia="Energía sostenida cuando responde correctamente. Motor constante.",
            forma_correcta_decidir="Esperar a que algo aparezca y sentir respuesta sacral (expansión/contracción).",
            trampa_mental="Iniciar mentalmente sin esperar respuesta sacral. Sobre-compromiso."
        ),
        
        perfil_psicologico=PerfilPsicologico(
            mbti=TipoMBTI.ENTP,
            eneagrama_base=TipoEneagrama.TIPO_5,
            alas=[TipoEneagrama.TIPO_4, TipoEneagrama.TIPO_6],
            patron_aprendizaje="Exploración conceptual multidimensional. Necesita ver el sistema completo. Aprende mejor conectando ideas aparentemente no relacionadas. Debate interno constante refina comprensión.",
            motivacion_profunda="Comprender sistemas complejos. Dominio técnico. Autonomía intelectual. Crear frameworks elegantes.",
            punto_ciego="Desconexión de necesidades corporales. Tendencia a sobre-analizar. Postergar acción por 'necesitar más información'.",
            trabajo_integracion="5→8: Pasar de análisis a acción. Confiar en conocimiento suficiente. Encarnar poder sin sobre-preparación."
        ),
        
        manifestaciones=[
            Manifestacion(
                id="m1",
                dimension=DimensionVida.DESARROLLO,
                nivel=NivelManifestacion.TRIMESTRAL,
                vision="Dominio de arquitecturas multi-agente con LangGraph",
                resultado_observable="3 sistemas multi-agente en producción funcionando sin intervención",
                practica_diaria="2h de desarrollo profundo + 30min documentación",
                frecuencia_minima="5 días/semana",
                tiempo_estimado_materializacion="3 meses",
                fecha_inicio=date.today(),
                progreso_estimado=30,
                se_integra_con=["m2", "m3"]
            ),
            Manifestacion(
                id="m2",
                dimension=DimensionVida.CONOCIMIENTO,
                nivel=NivelManifestacion.ANUAL,
                vision="Sistema vivo de conocimiento en Obsidian: 1000+ notas permanentes interconectadas",
                resultado_observable="Puedo encontrar cualquier concepto en <30s. 10+ MOCs robustos.",
                practica_diaria="Captura durante día + 20min síntesis nocturna",
                frecuencia_minima="diaria",
                tiempo_estimado_materializacion="12 meses",
                fecha_inicio=date.today(),
                progreso_estimado=15
            ),
            Manifestacion(
                id="m3",
                dimension=DimensionVida.FINANCIERO,
                nivel=NivelManifestacion.ANUAL,
                vision="Runway 24 meses + ingresos recurrentes >5k€/mes",
                resultado_observable="2 años de libertad financiera asegurada. Ingresos pasivos funcionando.",
                practica_diaria="1h trabajo generativo + 30min optimización sistemas",
                frecuencia_minima="5 días/semana",
                tiempo_estimado_materializacion="12 meses",
                fecha_inicio=date.today(),
                progreso_estimado=40,
                se_integra_con=["m1"]
            )
        ],
        
        estructura_conocimiento=EstructuraConocimiento(
            captura_primaria=MetodoCaptura.OBSIDIAN,
            captura_secundaria=MetodoCaptura.VOZ,
            usa_zettelkasten=True,
            sistema_vinculacion="backlinks",
            frecuencia_revision="semanal",
            umbral_nota_permanente="Cuando conecto con 3+ conceptos previos y puedo explicarlo en mis palabras",
            practica_sintesis_semanal=True,
            genera_mocs_automaticos=True,
            conecta_insights_automatico=True
        ),
        
        metodo_aprendizaje=MetodoAprendizaje(
            modalidad_preferida="lectura_escritura",
            profundidad_vs_amplitud=7,
            estrategias_efectivas=[
                "Exploración conceptual libre",
                "Construcción de frameworks mentales",
                "Implementación práctica inmediata",
                "Enseñar/documentar (método Feynman)",
                "Debate interno refinando argumentos"
            ],
            mejor_momento_aprendizaje="07:00-12:00",
            duracion_optima_sesion=90,
            requiere_silencio=True,
            indicadores_dominio=[
                "Puedo explicarlo sin mirar referencias",
                "Puedo implementarlo de memoria",
                "Puedo conectarlo con 5+ conceptos",
                "Puedo prever limitaciones y trade-offs",
                "Puedo enseñarlo y responder preguntas profundas"
            ]
        )
    )

