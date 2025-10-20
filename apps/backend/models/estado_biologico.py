"""
🧬 Estado Biológico - Capa 3 del Sistema

Captura y modela el estado biológico del usuario en cada Estado Cero:
- Nivel de energía (bajo/medio/alto)
- Calidad de sueño (última noche)
- Resonancia corporal (tensión/fluido/fatiga)
- Integración futura: HRV, métricas biométricas

Principio: El cuerpo sabe antes que la mente.
La Capa 3 es escucha somática, no análisis mental.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime, time
from enum import Enum


class NivelEnergia(str, Enum):
    """Nivel de energía física actual."""
    MUY_BAJO = "muy_bajo"      # 1/5 - Agotamiento
    BAJO = "bajo"              # 2/5 - Baja energía
    MEDIO = "medio"            # 3/5 - Energía estable
    ALTO = "alto"              # 4/5 - Energía elevada
    MUY_ALTO = "muy_alto"      # 5/5 - Energía pico


class CalidadSueno(str, Enum):
    """Calidad del sueño de la última noche."""
    PESIMO = "pesimo"          # Insomnio severo
    MALO = "malo"              # Sueño interrumpido
    REGULAR = "regular"        # Sueño aceptable
    BUENO = "bueno"            # Sueño reparador
    EXCELENTE = "excelente"    # Sueño profundo y completo


class ResonanciaCorporal(str, Enum):
    """Sensación somática predominante."""
    TENSION = "tension"        # Cuerpo contraído, tenso
    FATIGA = "fatiga"          # Cuerpo cansado, pesado
    NEUTRAL = "neutral"        # Sin sensación particular
    FLUIDO = "fluido"          # Cuerpo relajado, en flujo
    VIBRANTE = "vibrante"      # Cuerpo energizado, vital


class ZonaTension(str, Enum):
    """Ubicación de tensión corporal (si existe)."""
    NINGUNA = "ninguna"
    CABEZA = "cabeza"
    CUELLO_HOMBROS = "cuello_hombros"
    PECHO_CORAZON = "pecho_corazon"
    ESTOMAGO = "estomago"
    ESPALDA_BAJA = "espalda_baja"
    PIERNAS = "piernas"
    TODO_CUERPO = "todo_cuerpo"


class EstadoBiologico(BaseModel):
    """
    Estado biológico completo capturado en un Estado Cero.

    Este modelo representa la Capa 3: escucha del cuerpo.
    """

    # === CAMPOS CORE ===
    energia: NivelEnergia = Field(
        ...,
        description="Nivel de energía física actual (1-5)"
    )

    calidad_sueno: CalidadSueno = Field(
        ...,
        description="Calidad del sueño de la última noche"
    )

    resonancia_corporal: ResonanciaCorporal = Field(
        ...,
        description="Sensación somática predominante en este momento"
    )

    # === CAMPOS OPCIONALES ===
    horas_sueno: Optional[float] = Field(
        None,
        ge=0,
        le=24,
        description="Horas de sueño de la última noche"
    )

    zona_tension: Optional[ZonaTension] = Field(
        None,
        description="Dónde se siente tensión en el cuerpo (si existe)"
    )

    intensidad_tension: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Intensidad de la tensión (1-5)"
    )

    # === MÉTRICAS BIOMÉTRICAS (FUTURO) ===
    hrv: Optional[float] = Field(
        None,
        description="Variabilidad de frecuencia cardíaca (ms) - integración futura"
    )

    frecuencia_cardiaca_reposo: Optional[int] = Field(
        None,
        description="Frecuencia cardíaca en reposo (bpm) - integración futura"
    )

    # === METADATA ===
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Momento de captura"
    )

    notas_adicionales: Optional[str] = Field(
        None,
        max_length=500,
        description="Observaciones somáticas adicionales"
    )

    # === MÉTODOS ===

    def calcular_score_vitalidad(self) -> float:
        """
        Calcula un score de vitalidad general (0-10).

        Combina energía + sueño + resonancia corporal.

        Returns:
            Score de 0 (muy bajo) a 10 (óptimo)
        """
        # Mapeo de energía a puntos (0-4)
        energia_puntos = {
            NivelEnergia.MUY_BAJO: 0,
            NivelEnergia.BAJO: 1,
            NivelEnergia.MEDIO: 2,
            NivelEnergia.ALTO: 3,
            NivelEnergia.MUY_ALTO: 4
        }

        # Mapeo de sueño a puntos (0-3)
        sueno_puntos = {
            CalidadSueno.PESIMO: 0,
            CalidadSueno.MALO: 0.5,
            CalidadSueno.REGULAR: 1.5,
            CalidadSueno.BUENO: 2.5,
            CalidadSueno.EXCELENTE: 3
        }

        # Mapeo de resonancia a puntos (0-3)
        resonancia_puntos = {
            ResonanciaCorporal.TENSION: 0,
            ResonanciaCorporal.FATIGA: 1,
            ResonanciaCorporal.NEUTRAL: 2,
            ResonanciaCorporal.FLUIDO: 2.5,
            ResonanciaCorporal.VIBRANTE: 3
        }

        score = (
            energia_puntos[self.energia] +
            sueno_puntos[self.calidad_sueno] +
            resonancia_puntos[self.resonancia_corporal]
        )

        return round(score, 1)

    def generar_sintesis(self) -> str:
        """
        Genera una descripción textual del estado biológico.

        Returns:
            Frase descriptiva del estado corporal
        """
        partes = []

        # Energía
        energia_desc = {
            NivelEnergia.MUY_BAJO: "energía muy baja",
            NivelEnergia.BAJO: "energía baja",
            NivelEnergia.MEDIO: "energía media",
            NivelEnergia.ALTO: "energía alta",
            NivelEnergia.MUY_ALTO: "energía muy alta"
        }
        partes.append(energia_desc[self.energia])

        # Sueño
        sueno_desc = {
            CalidadSueno.PESIMO: "sueño pésimo",
            CalidadSueno.MALO: "sueño malo",
            CalidadSueno.REGULAR: "sueño regular",
            CalidadSueno.BUENO: "sueño bueno",
            CalidadSueno.EXCELENTE: "sueño excelente"
        }
        partes.append(sueno_desc[self.calidad_sueno])

        # Resonancia
        resonancia_desc = {
            ResonanciaCorporal.TENSION: "cuerpo tenso",
            ResonanciaCorporal.FATIGA: "cuerpo fatigado",
            ResonanciaCorporal.NEUTRAL: "cuerpo neutral",
            ResonanciaCorporal.FLUIDO: "cuerpo fluido",
            ResonanciaCorporal.VIBRANTE: "cuerpo vibrante"
        }
        partes.append(resonancia_desc[self.resonancia_corporal])

        # Agregar zona de tensión si existe
        if self.zona_tension and self.zona_tension != ZonaTension.NINGUNA:
            partes.append(f"tensión en {self.zona_tension.value}")

        sintesis = ", ".join(partes)
        score = self.calcular_score_vitalidad()

        return f"{sintesis} (vitalidad: {score}/10)"

    def esta_en_estado_optimo(self) -> bool:
        """
        Determina si el estado biológico es óptimo para Estado Cero profundo.

        Returns:
            True si vitalidad >= 6.5
        """
        return self.calcular_score_vitalidad() >= 6.5

    def necesita_atencion_biologica(self) -> bool:
        """
        Determina si el estado requiere atención biológica urgente.

        Returns:
            True si vitalidad < 3.0 (señal de agotamiento)
        """
        return self.calcular_score_vitalidad() < 3.0

    def esta_activa(self) -> bool:
        """
        Determina si la capa biológica debe estar 'activa'.

        Returns:
            True si vitalidad es extrema (muy baja < 6.0 o muy alta > 8.0)
        """
        score = self.calcular_score_vitalidad()
        return score < 6.0 or score > 8.0

    def generar_sugerencias(self) -> list[str]:
        """
        Genera sugerencias basadas en el estado actual.

        Returns:
            Lista de sugerencias
        """
        sugerencias_obj = generar_sugerencias_biologicas(self)
        return sugerencias_obj.sugerencias


class SugerenciasBiologicas(BaseModel):
    """
    Sugerencias basadas en el estado biológico.

    Este modelo NO dicta qué hacer, solo informa opciones.
    """

    sugerencias: list[str] = Field(
        description="Lista de sugerencias basadas en biología"
    )

    nivel_urgencia: Literal["baja", "media", "alta"] = Field(
        description="Urgencia de atender el estado biológico"
    )


def generar_sugerencias_biologicas(estado: EstadoBiologico) -> SugerenciasBiologicas:
    """
    Genera sugerencias basadas en el estado biológico.

    Args:
        estado: Estado biológico actual

    Returns:
        Sugerencias y nivel de urgencia
    """
    sugerencias = []
    vitalidad = estado.calcular_score_vitalidad()

    # Análisis de energía
    if estado.energia in [NivelEnergia.MUY_BAJO, NivelEnergia.BAJO]:
        sugerencias.append("Considerar siesta o descanso activo")
        if estado.calidad_sueno in [CalidadSueno.PESIMO, CalidadSueno.MALO]:
            sugerencias.append("Priorizar recuperación de sueño esta noche")

    # Análisis de sueño
    if estado.horas_sueno and estado.horas_sueno < 6:
        sugerencias.append("Déficit de sueño detectado - ajustar horarios")

    # Análisis de resonancia corporal
    if estado.resonancia_corporal == ResonanciaCorporal.TENSION:
        sugerencias.append("Práctica somática: respiración, estiramiento, o movimiento consciente")

    if estado.zona_tension and estado.zona_tension != ZonaTension.NINGUNA:
        sugerencias.append(f"Atender tensión en {estado.zona_tension.value}")

    # Estado óptimo
    if estado.esta_en_estado_optimo():
        sugerencias.append("Estado biológico óptimo - aprovechar para tareas exigentes")

    # Determinar urgencia
    if vitalidad < 3.0:
        urgencia = "alta"
    elif vitalidad < 5.0:
        urgencia = "media"
    else:
        urgencia = "baja"

    return SugerenciasBiologicas(
        sugerencias=sugerencias if sugerencias else ["Estado biológico estable"],
        nivel_urgencia=urgencia
    )


# === UTILIDADES ===

def crear_estado_rapido(
    energia: int,
    calidad_sueno: int,
    resonancia: str = "neutral"
) -> EstadoBiologico:
    """
    Crea un EstadoBiologico usando valores simplificados.

    Args:
        energia: 1-5
        calidad_sueno: 1-5
        resonancia: "tension", "fatiga", "neutral", "fluido", "vibrante"

    Returns:
        EstadoBiologico
    """
    # Mapear integers a enums
    energia_map = {
        1: NivelEnergia.MUY_BAJO,
        2: NivelEnergia.BAJO,
        3: NivelEnergia.MEDIO,
        4: NivelEnergia.ALTO,
        5: NivelEnergia.MUY_ALTO
    }

    sueno_map = {
        1: CalidadSueno.PESIMO,
        2: CalidadSueno.MALO,
        3: CalidadSueno.REGULAR,
        4: CalidadSueno.BUENO,
        5: CalidadSueno.EXCELENTE
    }

    resonancia_map = {
        "tension": ResonanciaCorporal.TENSION,
        "fatiga": ResonanciaCorporal.FATIGA,
        "neutral": ResonanciaCorporal.NEUTRAL,
        "fluido": ResonanciaCorporal.FLUIDO,
        "vibrante": ResonanciaCorporal.VIBRANTE
    }

    return EstadoBiologico(
        energia=energia_map.get(energia, NivelEnergia.MEDIO),
        calidad_sueno=sueno_map.get(calidad_sueno, CalidadSueno.REGULAR),
        resonancia_corporal=resonancia_map.get(resonancia, ResonanciaCorporal.NEUTRAL)
    )


if __name__ == "__main__":
    # Test del modelo
    print("🧬 ESTADO BIOLÓGICO - Test\n")
    print("=" * 70)

    # Test 1: Estado óptimo
    estado_optimo = EstadoBiologico(
        energia=NivelEnergia.ALTO,
        calidad_sueno=CalidadSueno.EXCELENTE,
        resonancia_corporal=ResonanciaCorporal.FLUIDO,
        horas_sueno=8.0
    )

    print("\n✨ Estado Óptimo:")
    print(f"   {estado_optimo.generar_sintesis()}")
    print(f"   ¿Óptimo?: {estado_optimo.esta_en_estado_optimo()}")

    sugerencias = generar_sugerencias_biologicas(estado_optimo)
    print(f"   Urgencia: {sugerencias.nivel_urgencia}")
    for s in sugerencias.sugerencias:
        print(f"   - {s}")

    # Test 2: Estado de agotamiento
    estado_agotado = EstadoBiologico(
        energia=NivelEnergia.MUY_BAJO,
        calidad_sueno=CalidadSueno.PESIMO,
        resonancia_corporal=ResonanciaCorporal.TENSION,
        horas_sueno=4.0,
        zona_tension=ZonaTension.CUELLO_HOMBROS,
        intensidad_tension=4
    )

    print("\n\n⚠️ Estado de Agotamiento:")
    print(f"   {estado_agotado.generar_sintesis()}")
    print(f"   ¿Necesita atención?: {estado_agotado.necesita_atencion_biologica()}")

    sugerencias = generar_sugerencias_biologicas(estado_agotado)
    print(f"   Urgencia: {sugerencias.nivel_urgencia}")
    for s in sugerencias.sugerencias:
        print(f"   - {s}")

    # Test 3: Uso de crear_estado_rapido
    print("\n\n🚀 Estado Rápido (API):")
    estado_rapido = crear_estado_rapido(energia=3, calidad_sueno=4, resonancia="fluido")
    print(f"   {estado_rapido.generar_sintesis()}")

    print("\n" + "=" * 70)
    print("✅ Capa 3 (Biológica) implementada correctamente")
