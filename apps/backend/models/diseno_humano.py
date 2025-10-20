"""
🌟 Diseño Humano - Capa 4 (Energética)

Modela la configuración de Diseño Humano del usuario:
- Tipo (Generador, Manifestador, Proyector, Reflector)
- Autoridad (Sacral, Emocional, Esplénica, Ego, Self-Projected, etc.)
- Estrategia (Responder, Informar, Esperar invitación, Esperar ciclo lunar)
- Perfil, Cruz de Encarnación, Canales

Principio: El Diseño Humano define CÓMO opera la energía,
no QUÉ hacer. Es configuración, no determinación.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class TipoDH(str, Enum):
    """Tipos de Diseño Humano"""
    GENERADOR = "Generador"
    GENERADOR_MANIFESTADOR = "Generador Manifestador"
    MANIFESTADOR = "Manifestador"
    PROYECTOR = "Proyector"
    REFLECTOR = "Reflector"


class AutoridadDH(str, Enum):
    """Autoridad interna (centro de toma de decisiones)"""
    SACRAL = "Sacral"
    EMOCIONAL = "Emocional"
    ESPLENICA = "Esplénica"
    EGO_MANIFESTADO = "Ego Manifestado"
    EGO_PROYECTADO = "Ego Proyectado"
    SELF_PROJECTED = "Self-Projected"
    MENTAL = "Mental"
    LUNAR = "Lunar"


class EstrategiaDH(str, Enum):
    """Estrategia para tomar decisiones correctas"""
    RESPONDER = "Responder, no iniciar"
    INFORMAR = "Informar antes de actuar"
    ESPERAR_INVITACION = "Esperar invitación"
    ESPERAR_CICLO_LUNAR = "Esperar ciclo lunar (28 días)"


class DisenoHumano(BaseModel):
    """
    Configuración completa de Diseño Humano del usuario.

    Esta es la Capa 4: cómo opera la energía del individuo.
    """

    # === CORE ===
    tipo: TipoDH = Field(
        ...,
        description="Tipo de Diseño Humano"
    )

    autoridad: AutoridadDH = Field(
        ...,
        description="Autoridad interna para tomar decisiones"
    )

    estrategia: EstrategiaDH = Field(
        ...,
        description="Estrategia para alinearse con el diseño"
    )

    # === PERFIL ===
    perfil: Optional[str] = Field(
        None,
        description="Perfil (ej: '4/6', '1/3', '5/1')"
    )

    cruz_encarnacion: Optional[str] = Field(
        None,
        description="Cruz de Encarnación (ej: 'Cruz de Ángulo Derecho de la Penetración 2')"
    )

    # === CANALES Y CENTROS ===
    canales: List[str] = Field(
        default_factory=list,
        description="Canales definidos (ej: ['53/54', '51/57'])"
    )

    centros_definidos: List[str] = Field(
        default_factory=list,
        description="Centros definidos (ej: ['Sacral', 'Garganta', 'Raíz'])"
    )

    # === VALIDACIÓN ===
    tiempo_respuesta_optimo: Optional[str] = Field(
        None,
        description="Tiempo óptimo para responder desde autoridad (ej: '< 3 segundos para Sacral')"
    )

    not_self_theme: Optional[str] = Field(
        None,
        description="Tema del 'no-ser' cuando no se sigue la estrategia (ej: 'frustración' para Generadores)"
    )

    signature: Optional[str] = Field(
        None,
        description="Firma de alineación (ej: 'satisfacción' para Generadores)"
    )

    # === MÉTODOS ===

    def generar_recordatorio(self) -> str:
        """
        Genera recordatorio de estrategia para Estado Cero.

        Returns:
            Texto recordatorio de cómo usar la autoridad
        """
        recordatorios = {
            AutoridadDH.SACRAL: "Escucha tu respuesta visceral inmediata (< 3 seg). Un 'uh-huh' (sí) o 'uh-uh' (no) desde el sacro.",
            AutoridadDH.EMOCIONAL: "Espera la ola emocional. No hay verdad en el ahora, solo claridad a través del tiempo.",
            AutoridadDH.ESPLENICA: "Confía en el primer impulso. Tu intuición habla solo una vez, en el momento presente.",
            AutoridadDH.EGO_MANIFESTADO: "¿Qué quiere tu corazón? ¿Qué promesa puedes sostener?",
            AutoridadDH.EGO_PROYECTADO: "¿Qué hay en esto para ti? Tu ego debe estar involucrado.",
            AutoridadDH.SELF_PROJECTED: "Escucha lo que dices cuando hablas sobre esto. Tu verdad emerge al expresarte.",
            AutoridadDH.MENTAL: "No hay autoridad interna. Habla con otros y siente resonancia en conversación.",
            AutoridadDH.LUNAR: "Espera el ciclo completo de la luna (28 días) para decisiones importantes."
        }

        return recordatorios.get(
            self.autoridad,
            f"Sigue tu estrategia: {self.estrategia.value}"
        )

    def validar_tiempo_respuesta(self, segundos: float) -> bool:
        """
        Valida si el tiempo de respuesta es apropiado para la autoridad.

        Args:
            segundos: Tiempo que tomó responder

        Returns:
            True si el tiempo es apropiado
        """
        # Sacral: debe ser inmediato (< 3 segundos)
        if self.autoridad == AutoridadDH.SACRAL:
            return segundos < 3.0

        # Esplénica: debe ser inmediato (< 2 segundos)
        if self.autoridad == AutoridadDH.ESPLENICA:
            return segundos < 2.0

        # Emocional: NO debe ser inmediato
        if self.autoridad == AutoridadDH.EMOCIONAL:
            return False  # Necesita tiempo (horas/días)

        # Lunar: necesita 28 días
        if self.autoridad == AutoridadDH.LUNAR:
            return False

        # Otras autoridades: flexible
        return True

    def esta_siguiendo_estrategia(
        self,
        fue_invitado: bool = False,
        informo_antes: bool = False,
        respondio_a_algo: bool = False
    ) -> bool:
        """
        Verifica si se está siguiendo la estrategia correcta.

        Args:
            fue_invitado: Para Proyectores
            informo_antes: Para Manifestadores
            respondio_a_algo: Para Generadores

        Returns:
            True si está siguiendo la estrategia
        """
        if self.tipo in [TipoDH.GENERADOR, TipoDH.GENERADOR_MANIFESTADOR]:
            return respondio_a_algo

        if self.tipo == TipoDH.MANIFESTADOR:
            return informo_antes

        if self.tipo == TipoDH.PROYECTOR:
            return fue_invitado

        # Reflector: siempre en proceso
        return True


# === FUNCIONES UTILIDAD ===

def crear_diseno_daniel() -> DisenoHumano:
    """
    Crea el Diseño Humano de Daniel (hardcoded por ahora).

    TODO: Cargar desde configuración o archivo.

    Returns:
        DisenoHumano de Daniel
    """
    return DisenoHumano(
        tipo=TipoDH.GENERADOR,
        autoridad=AutoridadDH.SACRAL,
        estrategia=EstrategiaDH.RESPONDER,
        perfil="4/6",
        cruz_encarnacion="Cruz de Ángulo Derecho de la Penetración 2",
        canales=["53/54", "51/57"],
        centros_definidos=["Sacral", "Raíz", "Garganta"],
        tiempo_respuesta_optimo="< 3 segundos",
        not_self_theme="frustración",
        signature="satisfacción"
    )


def cargar_diseno_desde_config(config_path: str) -> Optional[DisenoHumano]:
    """
    Carga Diseño Humano desde archivo de configuración.

    Args:
        config_path: Ruta al archivo de configuración

    Returns:
        DisenoHumano o None si no existe
    """
    from pathlib import Path
    import json

    path = Path(config_path)
    if not path.exists():
        return None

    try:
        with open(path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        if "diseno_humano" not in config:
            return None

        dh_data = config["diseno_humano"]

        return DisenoHumano(
            tipo=TipoDH(dh_data["tipo"]),
            autoridad=AutoridadDH(dh_data["autoridad"]),
            estrategia=EstrategiaDH(dh_data["estrategia"]),
            perfil=dh_data.get("perfil"),
            cruz_encarnacion=dh_data.get("cruz_encarnacion"),
            canales=dh_data.get("canales", []),
            centros_definidos=dh_data.get("centros_definidos", []),
            tiempo_respuesta_optimo=dh_data.get("tiempo_respuesta_optimo"),
            not_self_theme=dh_data.get("not_self_theme"),
            signature=dh_data.get("signature")
        )

    except Exception as e:
        print(f"Error cargando Diseño Humano: {e}")
        return None


if __name__ == "__main__":
    # Test
    print("🌟 DISEÑO HUMANO - Test\n")
    print("=" * 70)

    # Test 1: Diseño de Daniel
    dh = crear_diseno_daniel()

    print(f"\n📋 CONFIGURACIÓN:")
    print(f"   Tipo: {dh.tipo.value}")
    print(f"   Autoridad: {dh.autoridad.value}")
    print(f"   Estrategia: {dh.estrategia.value}")
    print(f"   Perfil: {dh.perfil}")
    print(f"   Cruz: {dh.cruz_encarnacion}")

    print(f"\n💡 RECORDATORIO:")
    print(f"   {dh.generar_recordatorio()}")

    print(f"\n⏱️ VALIDACIÓN TIEMPO RESPUESTA:")
    print(f"   2 segundos: {'✅ Válido' if dh.validar_tiempo_respuesta(2.0) else '❌ Inválido'}")
    print(f"   5 segundos: {'✅ Válido' if dh.validar_tiempo_respuesta(5.0) else '❌ Inválido'}")

    print(f"\n✓ SIGUIENDO ESTRATEGIA:")
    print(f"   Respondió a algo: {'✅ Sí' if dh.esta_siguiendo_estrategia(respondio_a_algo=True) else '❌ No'}")
    print(f"   Inició sin responder: {'✅ Sí' if dh.esta_siguiendo_estrategia(respondio_a_algo=False) else '❌ No'}")

    # Test 2: Otros tipos
    print("\n\n📋 OTROS TIPOS:")

    proyector = DisenoHumano(
        tipo=TipoDH.PROYECTOR,
        autoridad=AutoridadDH.SELF_PROJECTED,
        estrategia=EstrategiaDH.ESPERAR_INVITACION
    )
    print(f"\n   Proyector: {proyector.generar_recordatorio()}")

    manifestador = DisenoHumano(
        tipo=TipoDH.MANIFESTADOR,
        autoridad=AutoridadDH.EMOCIONAL,
        estrategia=EstrategiaDH.INFORMAR
    )
    print(f"   Manifestador: {manifestador.generar_recordatorio()}")

    print("\n" + "=" * 70)
    print("✅ Capa 4 (Energética/DH) implementada correctamente")
