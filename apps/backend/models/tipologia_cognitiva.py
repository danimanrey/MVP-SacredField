"""
🧠 Tipología Cognitiva - Capa 6 (Mental/Cognitiva)

Modela el funcionamiento cognitivo del usuario mediante:
- MBTI: Stack de funciones cognitivas (Ne-Ti-Fe-Si para ENTP)
- Eneagrama: Tipo base, alas, líneas de integración/desintegración
- Detección de función activa según contexto y hora
- Mapeo de nivel de salud desde patrones observados

Principio: La mente tiene estructura, no es ruido aleatorio.
La Capa 6 mapea CÓMO procesa información el individuo.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Tuple
from datetime import datetime, time
from enum import Enum
from pathlib import Path
import json


# === MBTI ===

class FuncionCognitiva(str, Enum):
    """8 funciones cognitivas del modelo MBTI"""
    # Funciones primarias
    NE = "Ne"  # Intuición Extrovertida (exploración, posibilidades)
    NI = "Ni"  # Intuición Introvertida (visión, convergencia)
    SE = "Se"  # Sensación Extrovertida (experiencia, presente)
    SI = "Si"  # Sensación Introvertida (memoria, datos)
    TE = "Te"  # Pensamiento Extrovertido (organización, eficiencia)
    TI = "Ti"  # Pensamiento Introvertido (lógica, comprensión)
    FE = "Fe"  # Sentimiento Extrovertido (armonía, valores compartidos)
    FI = "Fi"  # Sentimiento Introvertido (autenticidad, valores internos)


class TipoMBTI(str, Enum):
    """16 tipos MBTI"""
    # Analistas (NT)
    INTJ = "INTJ"
    INTP = "INTP"
    ENTJ = "ENTJ"
    ENTP = "ENTP"

    # Diplomáticos (NF)
    INFJ = "INFJ"
    INFP = "INFP"
    ENFJ = "ENFJ"
    ENFP = "ENFP"

    # Centinelas (SJ)
    ISTJ = "ISTJ"
    ISFJ = "ISFJ"
    ESTJ = "ESTJ"
    ESFJ = "ESFJ"

    # Exploradores (SP)
    ISTP = "ISTP"
    ISFP = "ISFP"
    ESTP = "ESTP"
    ESFP = "ESFP"


class PerfilMBTI(BaseModel):
    """
    Perfil completo MBTI con stack de funciones cognitivas.
    """

    tipo: TipoMBTI = Field(
        ...,
        description="Tipo MBTI de 4 letras"
    )

    # Stack de funciones (orden de fortaleza)
    funcion_dominante: FuncionCognitiva = Field(
        ...,
        description="Función principal (más fuerte)"
    )

    funcion_auxiliar: FuncionCognitiva = Field(
        ...,
        description="Función de apoyo (segunda más fuerte)"
    )

    funcion_terciaria: FuncionCognitiva = Field(
        ...,
        description="Función terciaria (tercera)"
    )

    funcion_inferior: FuncionCognitiva = Field(
        ...,
        description="Función inferior (más débil, vulnerable)"
    )

    # Funciones de la sombra (4 adicionales, inconscientes)
    sombra: List[FuncionCognitiva] = Field(
        default_factory=list,
        description="4 funciones de la sombra (espejo oscuro del stack)"
    )

    # Metadata
    descripcion_corta: str = Field(
        ...,
        description="Descripción del tipo en 1 línea"
    )

    fortalezas: List[str] = Field(
        default_factory=list,
        description="Fortalezas naturales"
    )

    desafios: List[str] = Field(
        default_factory=list,
        description="Desafíos típicos"
    )

    # === MÉTODOS ===

    def mapear_funcion_activa(
        self,
        hora: int,
        contexto: Optional[str] = None
    ) -> Tuple[FuncionCognitiva, str]:
        """
        Mapea qué función cognitiva está más activa según hora y contexto.

        Args:
            hora: Hora del día (0-23)
            contexto: Contexto adicional (ej: "trabajo", "social", "reflexión")

        Returns:
            Tupla (función_activa, descripción)
        """
        # Mapeo temporal básico (puede refinarse con contexto)
        if 6 <= hora < 12:
            # Mañana: función dominante (energía fresca)
            return (
                self.funcion_dominante,
                self._descripcion_funcion(self.funcion_dominante)
            )
        elif 12 <= hora < 18:
            # Tarde: función auxiliar (estable, productivo)
            return (
                self.funcion_auxiliar,
                self._descripcion_funcion(self.funcion_auxiliar)
            )
        elif 18 <= hora < 22:
            # Noche temprana: función terciaria (relax, social)
            return (
                self.funcion_terciaria,
                self._descripcion_funcion(self.funcion_terciaria)
            )
        else:
            # Noche tardía: función inferior (vulnerable, cansancio)
            return (
                self.funcion_inferior,
                self._descripcion_funcion(self.funcion_inferior)
            )

    def _descripcion_funcion(self, funcion: FuncionCognitiva) -> str:
        """Descripción de cada función cognitiva."""
        descripciones = {
            FuncionCognitiva.NE: "Exploración de posibilidades, conexiones, ideas divergentes",
            FuncionCognitiva.NI: "Visión convergente, insight profundo, futuro",
            FuncionCognitiva.SE: "Experiencia sensorial presente, acción inmediata",
            FuncionCognitiva.SI: "Memoria detallada, datos pasados, tradición",
            FuncionCognitiva.TE: "Organización externa, eficiencia, logística",
            FuncionCognitiva.TI: "Análisis lógico interno, comprensión de sistemas",
            FuncionCognitiva.FE: "Armonía grupal, conexión social, valores compartidos",
            FuncionCognitiva.FI: "Autenticidad interna, valores personales, identidad"
        }
        return descripciones.get(funcion, "Función cognitiva")


# === ENEAGRAMA ===

class TipoEneagrama(int, Enum):
    """9 tipos del Eneagrama"""
    UNO = 1    # El Perfeccionista
    DOS = 2    # El Ayudador
    TRES = 3   # El Triunfador
    CUATRO = 4 # El Individualista
    CINCO = 5  # El Investigador
    SEIS = 6   # El Leal
    SIETE = 7  # El Entusiasta
    OCHO = 8   # El Desafiador
    NUEVE = 9  # El Pacificador


class NivelSalud(str, Enum):
    """Niveles de salud psicológica en Eneagrama"""
    SALUDABLE = "saludable"          # Niveles 1-3 (integrado, equilibrado)
    PROMEDIO = "promedio"            # Niveles 4-6 (funcionamiento normal)
    NO_SALUDABLE = "no_saludable"    # Niveles 7-9 (desintegrado, estresado)


class PerfilEneagrama(BaseModel):
    """
    Perfil completo del Eneagrama.
    """

    tipo_base: TipoEneagrama = Field(
        ...,
        description="Tipo principal del Eneagrama (1-9)"
    )

    ala_dominante: Optional[int] = Field(
        None,
        ge=1,
        le=9,
        description="Ala más fuerte (tipo adyacente)"
    )

    ala_secundaria: Optional[int] = Field(
        None,
        ge=1,
        le=9,
        description="Segunda ala (si es equilibrado)"
    )

    # Líneas de movimiento
    linea_integracion: int = Field(
        ...,
        ge=1,
        le=9,
        description="Tipo hacia el que se mueve cuando saludable"
    )

    linea_desintegracion: int = Field(
        ...,
        ge=1,
        le=9,
        description="Tipo hacia el que se mueve cuando estresado"
    )

    # Estado actual
    nivel_salud: NivelSalud = Field(
        default=NivelSalud.PROMEDIO,
        description="Nivel de salud psicológica actual"
    )

    # Metadata
    motivacion_basica: str = Field(
        ...,
        description="Motivación inconsciente del tipo"
    )

    miedo_basico: str = Field(
        ...,
        description="Miedo inconsciente del tipo"
    )

    pasion: str = Field(
        ...,
        description="Pasión emocional (aspecto no saludable)"
    )

    virtud: str = Field(
        ...,
        description="Virtud (aspecto saludable)"
    )

    # === MÉTODOS ===

    def detectar_nivel_desde_patrones(
        self,
        patrones_recientes: List[str]
    ) -> NivelSalud:
        """
        Detecta nivel de salud desde patrones observados.

        Args:
            patrones_recientes: Comportamientos/estados observados

        Returns:
            Nivel de salud estimado
        """
        # Indicadores de salud/no-salud por tipo
        # Esto se puede expandir con ML en el futuro

        if self.tipo_base == TipoEneagrama.CINCO:
            # Tipo 5: Investigador
            indicadores_saludables = ["curiosidad", "compartir conocimiento", "conexión social"]
            indicadores_no_saludables = ["aislamiento extremo", "acumulación sin acción", "desconexión total"]

            saludables = sum(1 for p in patrones_recientes if any(i in p.lower() for i in indicadores_saludables))
            no_saludables = sum(1 for p in patrones_recientes if any(i in p.lower() for i in indicadores_no_saludables))

            if saludables > no_saludables * 2:
                return NivelSalud.SALUDABLE
            elif no_saludables > saludables * 2:
                return NivelSalud.NO_SALUDABLE
            else:
                return NivelSalud.PROMEDIO

        # Default: promedio
        return NivelSalud.PROMEDIO

    def generar_recordatorio(self) -> str:
        """
        Genera recordatorio basado en nivel de salud actual.

        Returns:
            Texto de recordatorio
        """
        if self.nivel_salud == NivelSalud.SALUDABLE:
            return f"Tipo {self.tipo_base.value}: En tu mejor momento. Comparte tu {self.virtud}."
        elif self.nivel_salud == NivelSalud.NO_SALUDABLE:
            return f"Tipo {self.tipo_base.value}: Atención a {self.pasion}. Cultivar {self.virtud}."
        else:
            return f"Tipo {self.tipo_base.value}: Equilibrio. Recordar motivación: {self.motivacion_basica}."


# === PERFIL COGNITIVO COMPLETO ===

class PerfilCognitivo(BaseModel):
    """
    Perfil cognitivo completo: MBTI + Eneagrama integrados.

    Esta es la Capa 6 completa.
    """

    mbti: PerfilMBTI = Field(
        ...,
        description="Perfil MBTI completo"
    )

    eneagrama: PerfilEneagrama = Field(
        ...,
        description="Perfil Eneagrama completo"
    )

    # Integración
    sintesis: Optional[str] = Field(
        None,
        description="Síntesis de cómo MBTI + Eneagrama interactúan"
    )

    # === MÉTODOS ===

    def generar_contexto_mental(
        self,
        hora: int,
        patrones_recientes: Optional[List[str]] = None
    ) -> Dict:
        """
        Genera contexto mental completo para un momento.

        Args:
            hora: Hora del día
            patrones_recientes: Patrones observados recientemente

        Returns:
            Dict con contexto mental completo
        """
        # Función cognitiva activa
        funcion_activa, desc_funcion = self.mbti.mapear_funcion_activa(hora)

        # Nivel de salud Eneagrama
        if patrones_recientes:
            nivel_salud = self.eneagrama.detectar_nivel_desde_patrones(patrones_recientes)
        else:
            nivel_salud = self.eneagrama.nivel_salud

        return {
            "mbti": self.mbti.tipo.value,
            "funcion_activa": funcion_activa.value,
            "descripcion_funcion": desc_funcion,
            "eneagrama": f"{self.eneagrama.tipo_base.value}w{self.eneagrama.ala_dominante}",
            "nivel_salud": nivel_salud.value,
            "recordatorio_eneagrama": self.eneagrama.generar_recordatorio(),
            "activa": funcion_activa in [self.mbti.funcion_dominante, self.mbti.funcion_inferior]
            # Activa si es función extrema (dominante o inferior = vulnerable)
        }


# === FUNCIONES UTILIDAD ===

def crear_perfil_entp_5w4() -> PerfilCognitivo:
    """
    Crea perfil cognitivo de Daniel: ENTP-A + 5w4/5w6.

    Returns:
        PerfilCognitivo completo
    """
    # MBTI: ENTP
    mbti = PerfilMBTI(
        tipo=TipoMBTI.ENTP,
        funcion_dominante=FuncionCognitiva.NE,
        funcion_auxiliar=FuncionCognitiva.TI,
        funcion_terciaria=FuncionCognitiva.FE,
        funcion_inferior=FuncionCognitiva.SI,
        sombra=[FuncionCognitiva.NI, FuncionCognitiva.TE, FuncionCognitiva.FI, FuncionCognitiva.SE],
        descripcion_corta="El Innovador: Curioso, ingenioso, desafiante de lo establecido",
        fortalezas=["Pensamiento divergente", "Rápida conexión de ideas", "Versatilidad"],
        desafios=["Dispersión", "Seguimiento de proyectos", "Rutina"]
    )

    # Eneagrama: 5w4 (El Iconoclasta)
    eneagrama = PerfilEneagrama(
        tipo_base=TipoEneagrama.CINCO,
        ala_dominante=4,
        ala_secundaria=6,
        linea_integracion=8,  # Hacia acción decisiva cuando saludable
        linea_desintegracion=7,  # Hacia dispersión cuando estresado
        nivel_salud=NivelSalud.PROMEDIO,
        motivacion_basica="Comprender el mundo, ser competente",
        miedo_basico="Ser incompetente, inútil, vacío",
        pasion="Avaricia (acumular conocimiento sin acción)",
        virtud="Desapego (compartir conocimiento sin miedo)"
    )

    return PerfilCognitivo(
        mbti=mbti,
        eneagrama=eneagrama,
        sintesis="ENTP 5w4: Innovador intelectual con profundidad emocional. Explora posibilidades (Ne) mientras busca comprensión profunda (Ti + 5). El ala 4 añade individualismo y sensibilidad estética."
    )


def cargar_perfil_cognitivo_desde_config(config_path: str) -> Optional[PerfilCognitivo]:
    """
    Carga perfil cognitivo desde configuración.

    Args:
        config_path: Ruta al archivo de configuración

    Returns:
        PerfilCognitivo o None
    """
    path = Path(config_path)
    if not path.exists():
        return None

    try:
        with open(path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        if "perfil_cognitivo" not in config:
            return None

        pc_data = config["perfil_cognitivo"]

        # Construir MBTI
        mbti = PerfilMBTI(**pc_data["mbti"])

        # Construir Eneagrama
        eneagrama = PerfilEneagrama(**pc_data["eneagrama"])

        return PerfilCognitivo(
            mbti=mbti,
            eneagrama=eneagrama,
            sintesis=pc_data.get("sintesis")
        )

    except Exception as e:
        print(f"Error cargando perfil cognitivo: {e}")
        return None


if __name__ == "__main__":
    # Test
    print("🧠 TIPOLOGÍA COGNITIVA - Test\n")
    print("=" * 70)

    # Crear perfil ENTP 5w4
    perfil = crear_perfil_entp_5w4()

    print(f"\n📋 MBTI: {perfil.mbti.tipo.value}")
    print(f"   Stack: {perfil.mbti.funcion_dominante.value} → {perfil.mbti.funcion_auxiliar.value} → {perfil.mbti.funcion_terciaria.value} → {perfil.mbti.funcion_inferior.value}")
    print(f"   Descripción: {perfil.mbti.descripcion_corta}")

    print(f"\n📋 ENEAGRAMA: {perfil.eneagrama.tipo_base.value}w{perfil.eneagrama.ala_dominante}")
    print(f"   Motivación: {perfil.eneagrama.motivacion_basica}")
    print(f"   Nivel: {perfil.eneagrama.nivel_salud.value}")
    print(f"   Recordatorio: {perfil.eneagrama.generar_recordatorio()}")

    print(f"\n✨ SÍNTESIS:")
    print(f"   {perfil.sintesis}")

    # Test: Contexto mental por hora
    print(f"\n\n🕐 CONTEXTO MENTAL POR HORA:")

    for hora, momento in [(8, "mañana"), (14, "tarde"), (20, "noche"), (1, "madrugada")]:
        contexto = perfil.generar_contexto_mental(hora)
        print(f"\n   {hora}:00 ({momento}):")
        print(f"   Función activa: {contexto['funcion_activa']} - {contexto['descripcion_funcion']}")
        print(f"   ¿Capa activa?: {contexto['activa']}")

    print("\n" + "=" * 70)
    print("✅ Capa 6 (Mental/Cognitiva) implementada completamente")
