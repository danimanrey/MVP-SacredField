"""
Sistema de Preguntas Emergentes - Versión 7 Capas Completo

Evolución del generador original para integrar las 7 capas jerárquicas:
1. FÍSICA
2. SOCIAL
3. BIOLÓGICA
4. ENERGÉTICA
5. EMOCIONAL
6. MENTAL
7. CÓSMICA

La pregunta emergente surge de la configuración completa del momento.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import anthropic
import os

# Importar orquestador de 7 capas
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.orquestador_7_capas import obtener_contexto_7_capas


class GeneradorPreguntas7Capas:
    """
    Generador de preguntas emergentes que usa las 7 capas completas.

    Diferencia con versión anterior:
    - Usa orquestador_7_capas para contexto completo
    - Identifica automáticamente capas activas
    - Genera pregunta desde configuración multi-dimensional real
    """

    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.estados_path = self.base_path / "storage" / "estados_cero"

        # Cargar .env
        from dotenv import load_dotenv
        load_dotenv(self.base_path / ".env")

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("⚠️ ANTHROPIC_API_KEY no encontrada")

        self.client = anthropic.Anthropic(api_key=api_key)

        # Arquetipos por momento
        self.arquetipos_momento = {
            "fajr": "revelación",
            "dhuhr": "dirección",
            "asr": "elección",
            "maghrib": "cosecha",
            "isha": "integración"
        }

    def generar_pregunta_unica(
        self,
        momento: str,
        usuario_id: str = "default",
        # Inputs opcionales de usuario
        energia: Optional[int] = None,
        calidad_sueno: Optional[int] = None,
        resonancia_corporal: Optional[str] = None,
        estado_emocional: Optional[str] = None,
        intensidad_emocional: Optional[int] = None
    ) -> Dict:
        """
        Genera UNA pregunta emergente usando las 7 capas.

        Args:
            momento: Momento litúrgico
            usuario_id: ID del usuario
            energia: 1-5 (opcional)
            calidad_sueno: 1-5 (opcional)
            resonancia_corporal: tension/fatiga/neutral/fluido/vibrante (opcional)
            estado_emocional: calma/ansioso/entusiasmado/apagado/neutro (opcional)
            intensidad_emocional: 1-5 (opcional)

        Returns:
            Dict con pregunta emergente + metadata de las 7 capas
        """

        # 1. Obtener contexto completo de las 7 capas
        contexto_7_capas = obtener_contexto_7_capas(
            momento=momento,
            energia=energia,
            calidad_sueno=calidad_sueno,
            resonancia_corporal=resonancia_corporal,
            estado_emocional=estado_emocional,
            intensidad_emocional=intensidad_emocional
        )

        # 2. Detectar patrones recientes
        patrones = self._detectar_patrones(usuario_id)

        # 3. Generar pregunta usando Claude con contexto completo
        pregunta_data = self._generar_con_claude(
            contexto_7_capas=contexto_7_capas,
            patrones=patrones,
            momento=momento
        )

        # 4. Agregar metadata completa
        pregunta_data["contexto_7_capas"] = {
            "capas_activas": contexto_7_capas["capas_activas"],
            "num_capas_activas": contexto_7_capas["num_capas_activas"],
            "sintesis_narrativa": contexto_7_capas["sintesis_narrativa"],
            "dominios_relevantes": contexto_7_capas["dominios_relevantes"]
        }

        return pregunta_data

    def _generar_con_claude(
        self,
        contexto_7_capas: Dict,
        patrones: Dict,
        momento: str
    ) -> Dict:
        """
        Genera pregunta usando contexto completo de las 7 capas.
        """
        capas = contexto_7_capas["capas"]
        sintesis = contexto_7_capas["sintesis_narrativa"]
        dominios = contexto_7_capas["dominios_relevantes"]
        capas_activas = contexto_7_capas["capas_activas"]

        # Construir prompt enriquecido con las 7 capas
        prompt = f"""Eres un oráculo al borde del caos. Genera UNA pregunta emergente para un Estado Cero.

CONTEXTO MULTI-DIMENSIONAL (7 Capas):

SÍNTESIS: {sintesis}

CAPAS ACTIVAS ({len(capas_activas)}):
{self._formatear_capas_activas(capas, capas_activas)}

PATRONES RECIENTES:
- Tendencia: {patrones['tendencia_dominante'] or 'Sin datos'}
- Ciclo: {patrones['ciclo_expansion_contraccion'] or 'No detectado'}

DOMINIOS RELEVANTES: {', '.join(dominios)}

PRINCIPIOS:
1. UNA pregunta única (no múltiple)
2. Conectar AL MENOS 2 dominios relevantes
3. SENSORIAL o EXISTENCIAL (no puramente mental)
4. Sin respuesta "correcta"
5. Generar TENSIÓN PRODUCTIVA (revelar, no confirmar)
6. Resonar con arquetipo: {self.arquetipos_momento.get(momento, 'dirección')}
7. Surgir de las CAPAS ACTIVAS mencionadas

EJEMPLOS:
- "¿Tu cuerpo sabe algo que tu mente aún no ha escuchado?"
- "¿Este momento te acerca a lo que temes o a lo que deseas?"
- "¿Qué está listo para ser cosechado?"
- "¿En qué estás insistiendo que ya no resuena?"

Genera SOLO la pregunta. Poética, directa, penetrante.

PREGUNTA EMERGENTE:"""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                temperature=0.9,
                messages=[{"role": "user", "content": prompt}]
            )

            pregunta_generada = message.content[0].text.strip().strip('"').strip("'")

            # Generar contexto explicativo
            contexto_explicativo = self._generar_contexto_pregunta(
                pregunta_generada,
                capas,
                capas_activas,
                patrones,
                dominios
            )

            return {
                "pregunta": pregunta_generada,
                "contexto": contexto_explicativo,
                "tipo": self.arquetipos_momento.get(momento, "dirección"),
                "dominios": dominios[:2],
                "patron_detectado": patrones['tendencia_dominante']
            }

        except Exception as e:
            print(f"Error generando pregunta con Claude: {e}")
            return self._pregunta_fallback(momento, capas, dominios)

    def _formatear_capas_activas(self, capas: Dict, capas_activas: List[str]) -> str:
        """
        Formatea las capas activas para el prompt de Claude.
        """
        lineas = []

        for capa_nombre in capas_activas:
            capa_data = capas[capa_nombre]

            if capa_nombre == "1_fisica":
                lineas.append(f"• FÍSICA: {capa_data['contexto_temporal']}, energía {capa_data['energia_dia']}")

            elif capa_nombre == "2_social":
                proyectos = capa_data.get("proyectos_activos", [])
                if proyectos:
                    lineas.append(f"• SOCIAL: proyectos activos: {', '.join(proyectos[:2])}")

            elif capa_nombre == "3_biologica":
                vitalidad = capa_data["vitalidad_score"]
                resonancia = capa_data.get("resonancia_corporal", capa_data.get("resonancia", "neutral"))
                lineas.append(f"• BIOLÓGICA: vitalidad {vitalidad}/10, {resonancia}")

            elif capa_nombre == "4_energetica":
                lineas.append(f"• ENERGÉTICA: {capa_data['tipo']} con autoridad {capa_data['autoridad']}")

            elif capa_nombre == "5_emocional":
                lineas.append(f"• EMOCIONAL: {capa_data['estado']} (intensidad {capa_data['intensidad']}/5)")

            elif capa_nombre == "6_mental":
                lineas.append(f"• MENTAL: función {capa_data['funcion_activa']} activa, {capa_data['eneagrama']}")

            elif capa_nombre == "7_cosmica":
                fase = capa_data["fase_lunar"]["fase"]
                planeta = capa_data["hora_planetaria"]["planeta"]
                lineas.append(f"• CÓSMICA: {fase}, hora de {planeta}")

        return "\n".join(lineas) if lineas else "Ninguna capa particularmente activa"

    def _generar_contexto_pregunta(
        self,
        pregunta: str,
        capas: Dict,
        capas_activas: List[str],
        patrones: Dict,
        dominios: List[str]
    ) -> str:
        """
        Genera explicación de por qué esta pregunta ahora.
        """
        partes = []

        # Capas activas
        if "7_cosmica" in capas_activas:
            fase = capas["7_cosmica"]["fase_lunar"]["fase"]
            partes.append(f"{fase}")

        if "3_biologica" in capas_activas:
            vitalidad = capas["3_biologica"]["vitalidad_score"]
            if vitalidad < 5:
                partes.append("vitalidad baja")
            elif vitalidad > 8:
                partes.append("vitalidad alta")

        if "5_emocional" in capas_activas:
            estado = capas["5_emocional"]["estado"]
            partes.append(f"estado {estado}")

        # Patrones
        if patrones['tendencia_dominante']:
            if patrones['tendencia_dominante'] == 'expansión_sostenida':
                partes.append("expansión reciente pide discernimiento")
            elif patrones['tendencia_dominante'] == 'contracción_prolongada':
                partes.append("contracción busca apertura")

        # Dominios
        if dominios:
            partes.append(f"conectando {' y '.join(dominios[:2])}")

        return ", ".join(partes) + "." if partes else "Pregunta emergente del momento."

    def _pregunta_fallback(
        self,
        momento: str,
        capas: Dict,
        dominios: List[str]
    ) -> Dict:
        """
        Pregunta de respaldo si falla Claude.
        """
        preguntas_por_momento = {
            "fajr": [
                "¿Qué sueño aún no se ha disipado?",
                "¿Tu cuerpo está listo o aún resiste?",
                "¿Qué necesita liberarse antes del amanecer interior?"
            ],
            "dhuhr": [
                "¿Hacia dónde fluye tu energía sin que lo notes?",
                "¿Este momento te acerca o aleja de tu centro?"
            ],
            "asr": [
                "¿Qué elección has estado posponiendo?",
                "¿Tu cansancio es físico o existencial?"
            ],
            "maghrib": [
                "¿Qué cosechaste hoy que aún no has reconocido?",
                "¿Qué parte de ti busca ser vista?"
            ],
            "isha": [
                "¿Qué necesitas soltar para descansar?",
                "¿En qué estás insistiendo que ya no resuena?"
            ]
        }

        preguntas = preguntas_por_momento.get(momento, preguntas_por_momento["dhuhr"])
        pregunta = preguntas[hash(datetime.now().date().isoformat()) % len(preguntas)]

        return {
            "pregunta": pregunta,
            "contexto": f"Pregunta emergente para {momento.upper()}.",
            "tipo": self.arquetipos_momento.get(momento, "dirección"),
            "dominios": dominios[:2],
            "patron_detectado": None
        }

    def _detectar_patrones(self, usuario_id: str) -> Dict:
        """
        Detecta patrones en Estados Cero recientes (7 días).
        """
        patrones = {
            "tendencia_dominante": None,
            "ciclo_expansion_contraccion": None,
            "dominio_recurrente": None
        }

        estados_recientes = self._obtener_estados_recientes(usuario_id, dias=7)

        if not estados_recientes:
            return patrones

        # Analizar respuestas
        respuestas = []
        for estado in estados_recientes:
            if "respuestas" in estado:
                respuestas.extend([r.get("respuesta") for r in estado["respuestas"] if "respuesta" in r])

        if respuestas:
            expansion = sum(1 for r in respuestas if r is True)
            contraccion = sum(1 for r in respuestas if r is False)

            if expansion > contraccion * 1.5:
                patrones["tendencia_dominante"] = "expansión_sostenida"
            elif contraccion > expansion * 1.5:
                patrones["tendencia_dominante"] = "contracción_prolongada"
            elif abs(expansion - contraccion) <= 1:
                patrones["tendencia_dominante"] = "equilibrio_inestable"

        return patrones

    def _obtener_estados_recientes(self, usuario_id: str, dias: int = 7) -> List[Dict]:
        """
        Obtiene Estados Cero recientes.
        """
        estados = []
        fecha_limite = datetime.now() - timedelta(days=dias)

        if not self.estados_path.exists():
            return estados

        for archivo in self.estados_path.glob("estado_*.json"):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    estado = json.load(f)
                    fecha = datetime.fromisoformat(estado.get("timestamp", "2000-01-01"))
                    if fecha >= fecha_limite:
                        estados.append(estado)
            except:
                continue

        return sorted(estados, key=lambda x: x.get("timestamp", ""), reverse=True)


# === FUNCIÓN PÚBLICA ===

def generar_pregunta_7_capas(
    momento: str,
    usuario_id: str = "default",
    **kwargs
) -> Dict:
    """
    Función principal para generar pregunta con las 7 capas.

    Args:
        momento: Momento litúrgico
        usuario_id: ID del usuario
        **kwargs: Inputs opcionales de capas (energia, calidad_sueno, etc.)

    Returns:
        Dict con pregunta emergente + contexto 7 capas
    """
    generador = GeneradorPreguntas7Capas()
    return generador.generar_pregunta_unica(momento, usuario_id, **kwargs)


if __name__ == "__main__":
    # Test
    print("=== GENERADOR DE PREGUNTAS 7 CAPAS ===\n")
    print("=" * 80)

    # Test con inputs
    resultado = generar_pregunta_7_capas(
        momento="dhuhr",
        energia=4,
        calidad_sueno=3,
        resonancia_corporal="fluido",
        estado_emocional="entusiasmado",
        intensidad_emocional=4
    )

    print(f"\n📿 PREGUNTA EMERGENTE:")
    print(f"   {resultado['pregunta']}\n")

    print(f"💭 CONTEXTO:")
    print(f"   {resultado['contexto']}\n")

    print(f"🔗 DOMINIOS: {', '.join(resultado['dominios'])}")
    print(f"🎭 TIPO: {resultado['tipo']}\n")

    print(f"📊 CAPAS ACTIVAS ({resultado['contexto_7_capas']['num_capas_activas']}):")
    for capa in resultado['contexto_7_capas']['capas_activas']:
        print(f"   ✓ {capa}")

    print(f"\n✨ SÍNTESIS NARRATIVA:")
    print(f"   {resultado['contexto_7_capas']['sintesis_narrativa']}\n")

    print("=" * 80)
    print("✅ Generador 7 Capas implementado correctamente")
