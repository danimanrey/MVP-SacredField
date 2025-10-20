"""
💭 Estado Emocional - Capa 5 (Emocional/Psicológica)

Captura y modela el estado emocional del usuario:
- Estado actual (calma, ansioso, entusiasmado, apagado, neutro)
- Intensidad (1-5)
- Tendencia (mejorando, empeorando, estable)
- Tracking histórico para detectar patrones

Principio: Las emociones son información, no ruido.
La Capa 5 escucha sin juzgar.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import json


class EstadoEmocionalTipo(str, Enum):
    """Estados emocionales básicos"""
    CALMA = "calma"
    ANSIOSO = "ansioso"
    ENTUSIASMADO = "entusiasmado"
    APAGADO = "apagado"
    NEUTRO = "neutro"
    TRISTE = "triste"
    IRRITADO = "irritado"
    ALEGRE = "alegre"
    ABRUMADO = "abrumado"
    CONECTADO = "conectado"


class TendenciaEmocional(str, Enum):
    """Dirección del estado emocional"""
    MEJORANDO = "mejorando"
    EMPEORANDO = "empeorando"
    ESTABLE = "estable"
    OSCILANTE = "oscilante"


class EstadoEmocional(BaseModel):
    """
    Estado emocional capturado en un momento específico.
    """

    # === CORE ===
    estado: EstadoEmocionalTipo = Field(
        ...,
        description="Estado emocional actual"
    )

    intensidad: int = Field(
        ...,
        ge=1,
        le=5,
        description="Intensidad del estado (1=leve, 5=muy intenso)"
    )

    # === TENDENCIA ===
    tendencia: TendenciaEmocional = Field(
        default=TendenciaEmocional.ESTABLE,
        description="Dirección del estado emocional"
    )

    # === CONTEXTO ===
    desencadenante: Optional[str] = Field(
        None,
        max_length=200,
        description="Qué desencadenó este estado (opcional)"
    )

    necesidad_subyacente: Optional[str] = Field(
        None,
        max_length=200,
        description="Necesidad que la emoción está señalando (opcional)"
    )

    # === METADATA ===
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Momento de captura"
    )

    momento_liturgico: Optional[str] = Field(
        None,
        description="Momento litúrgico asociado (fajr, dhuhr, etc.)"
    )

    # === MÉTODOS ===

    def esta_activo(self) -> bool:
        """
        Determina si el estado emocional debe marcar la capa como 'activa'.

        Returns:
            True si intensidad >= 4 o estado es polarizado
        """
        estados_polarizados = [
            EstadoEmocionalTipo.ANSIOSO,
            EstadoEmocionalTipo.ENTUSIASMADO,
            EstadoEmocionalTipo.ABRUMADO,
            EstadoEmocionalTipo.IRRITADO
        ]

        return self.intensidad >= 4 or self.estado in estados_polarizados

    def generar_sintesis(self) -> str:
        """
        Genera descripción textual del estado emocional.

        Returns:
            Frase descriptiva
        """
        tendencia_texto = {
            TendenciaEmocional.MEJORANDO: "mejorando",
            TendenciaEmocional.EMPEORANDO: "empeorando",
            TendenciaEmocional.ESTABLE: "estable",
            TendenciaEmocional.OSCILANTE: "oscilante"
        }

        return f"{self.estado.value} (intensidad {self.intensidad}/5, {tendencia_texto[self.tendencia]})"

    def necesita_atencion(self) -> bool:
        """
        Determina si el estado requiere atención inmediata.

        Returns:
            True si estado es crítico (abrumado/ansioso intenso)
        """
        estados_criticos = [
            EstadoEmocionalTipo.ABRUMADO,
            EstadoEmocionalTipo.ANSIOSO
        ]

        return self.estado in estados_criticos and self.intensidad >= 4


class TrackerEmocional:
    """
    Rastrea estados emocionales a lo largo del tiempo.

    Permite detectar patrones, tendencias, y ciclos emocionales.
    """

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Args:
            storage_path: Directorio donde guardar histórico emocional
        """
        self.storage_path = storage_path or Path(__file__).parent.parent / "storage" / "emocional"
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def guardar_estado(self, estado: EstadoEmocional, usuario_id: str = "default"):
        """
        Guarda estado emocional en histórico.

        Args:
            estado: EstadoEmocional a guardar
            usuario_id: ID del usuario
        """
        archivo = self.storage_path / f"{usuario_id}_emocional.json"

        # Cargar histórico existente
        historico = []
        if archivo.exists():
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    historico = json.load(f)
            except:
                historico = []

        # Agregar nuevo estado
        historico.append({
            "timestamp": estado.timestamp.isoformat(),
            "estado": estado.estado.value,
            "intensidad": estado.intensidad,
            "tendencia": estado.tendencia.value,
            "momento_liturgico": estado.momento_liturgico,
            "desencadenante": estado.desencadenante
        })

        # Guardar (mantener últimos 30 días)
        fecha_limite = datetime.now() - timedelta(days=30)
        historico = [
            h for h in historico
            if datetime.fromisoformat(h["timestamp"]) >= fecha_limite
        ]

        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(historico, f, indent=2, ensure_ascii=False)

    def obtener_historico(
        self,
        usuario_id: str = "default",
        dias: int = 7
    ) -> List[Dict]:
        """
        Obtiene histórico emocional reciente.

        Args:
            usuario_id: ID del usuario
            dias: Días a recuperar

        Returns:
            Lista de estados emocionales
        """
        archivo = self.storage_path / f"{usuario_id}_emocional.json"

        if not archivo.exists():
            return []

        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                historico = json.load(f)

            fecha_limite = datetime.now() - timedelta(days=dias)
            return [
                h for h in historico
                if datetime.fromisoformat(h["timestamp"]) >= fecha_limite
            ]
        except:
            return []

    def detectar_tendencia(self, usuario_id: str = "default") -> TendenciaEmocional:
        """
        Detecta tendencia emocional basada en últimos 3 estados.

        Args:
            usuario_id: ID del usuario

        Returns:
            TendenciaEmocional detectada
        """
        historico = self.obtener_historico(usuario_id, dias=2)

        if len(historico) < 3:
            return TendenciaEmocional.ESTABLE

        # Analizar últimos 3 estados
        ultimos_3 = historico[-3:]
        intensidades = [h["intensidad"] for h in ultimos_3]

        # Detectar tendencia
        if intensidades[-1] > intensidades[0] + 1:
            return TendenciaEmocional.MEJORANDO
        elif intensidades[-1] < intensidades[0] - 1:
            return TendenciaEmocional.EMPEORANDO
        elif max(intensidades) - min(intensidades) >= 2:
            return TendenciaEmocional.OSCILANTE
        else:
            return TendenciaEmocional.ESTABLE

    def detectar_patron_diario(
        self,
        usuario_id: str = "default"
    ) -> Optional[str]:
        """
        Detecta si hay un patrón emocional por momento del día.

        Args:
            usuario_id: ID del usuario

        Returns:
            Descripción del patrón o None
        """
        historico = self.obtener_historico(usuario_id, dias=7)

        if len(historico) < 10:
            return None

        # Agrupar por momento litúrgico
        por_momento = {}
        for h in historico:
            momento = h.get("momento_liturgico")
            if momento:
                if momento not in por_momento:
                    por_momento[momento] = []
                por_momento[momento].append(h["estado"])

        # Detectar si un momento tiene patrón consistente
        for momento, estados in por_momento.items():
            if len(estados) >= 3:
                # Si 70%+ son el mismo estado
                from collections import Counter
                conteo = Counter(estados)
                estado_comun, frecuencia = conteo.most_common(1)[0]

                if frecuencia / len(estados) >= 0.7:
                    return f"{estado_comun} recurrente en {momento}"

        return None


# === FUNCIONES PÚBLICAS ===

def capturar_estado_emocional(
    estado: str,
    intensidad: int,
    momento_liturgico: Optional[str] = None,
    desencadenante: Optional[str] = None,
    usuario_id: str = "default"
) -> EstadoEmocional:
    """
    Captura y guarda un estado emocional.

    Args:
        estado: Estado emocional (calma, ansioso, etc.)
        intensidad: 1-5
        momento_liturgico: Momento litúrgico asociado
        desencadenante: Qué lo desencadenó (opcional)
        usuario_id: ID del usuario

    Returns:
        EstadoEmocional creado
    """
    tracker = TrackerEmocional()

    # Detectar tendencia desde histórico
    tendencia = tracker.detectar_tendencia(usuario_id)

    # Crear estado
    estado_obj = EstadoEmocional(
        estado=EstadoEmocionalTipo(estado),
        intensidad=intensidad,
        tendencia=tendencia,
        momento_liturgico=momento_liturgico,
        desencadenante=desencadenante
    )

    # Guardar
    tracker.guardar_estado(estado_obj, usuario_id)

    return estado_obj


if __name__ == "__main__":
    # Test
    print("💭 ESTADO EMOCIONAL - Test\n")
    print("=" * 70)

    # Test 1: Crear estado
    estado1 = EstadoEmocional(
        estado=EstadoEmocionalTipo.ENTUSIASMADO,
        intensidad=4,
        tendencia=TendenciaEmocional.MEJORANDO,
        momento_liturgico="dhuhr"
    )

    print(f"\n📊 ESTADO EMOCIONAL:")
    print(f"   {estado1.generar_sintesis()}")
    print(f"   ¿Activo?: {estado1.esta_activo()}")
    print(f"   ¿Necesita atención?: {estado1.necesita_atencion()}")

    # Test 2: Tracker
    print(f"\n\n📈 TRACKER EMOCIONAL:")

    tracker = TrackerEmocional()

    # Simular 5 estados
    estados_simulados = [
        ("calma", 2, "fajr"),
        ("entusiasmado", 4, "dhuhr"),
        ("entusiasmado", 5, "asr"),
        ("abrumado", 4, "maghrib"),
        ("calma", 3, "isha")
    ]

    for estado, intensidad, momento in estados_simulados:
        capturar_estado_emocional(
            estado=estado,
            intensidad=intensidad,
            momento_liturgico=momento,
            usuario_id="test"
        )

    # Detectar tendencia
    tendencia = tracker.detectar_tendencia("test")
    print(f"   Tendencia detectada: {tendencia.value}")

    # Detectar patrón
    patron = tracker.detectar_patron_diario("test")
    if patron:
        print(f"   Patrón detectado: {patron}")

    # Obtener histórico
    historico = tracker.obtener_historico("test", dias=1)
    print(f"   Estados registrados: {len(historico)}")

    print("\n" + "=" * 70)
    print("✅ Capa 5 (Emocional) implementada correctamente")
