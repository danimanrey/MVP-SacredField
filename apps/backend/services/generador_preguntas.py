"""
Sistema de Preguntas Emergentes al Borde del Caos

Genera UNA pregunta única por Estado Cero que emerge del contexto
multi-dimensional del sistema: momento litúrgico, fase lunar, patrones
detectados, dominios necesitando atención.

Principio: La pregunta debe REVELAR, no CONFIRMAR.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import anthropic
import os

class GeneradorPreguntasEmergentes:
    """
    Genera preguntas únicas que operan al borde del caos.

    Características:
    - Una pregunta por Estado Cero
    - Emerge del contexto actual del sistema
    - Conecta al menos 2 dominios
    - Sensorial o existencial, no puramente mental
    - Genera tensión productiva
    """

    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.estados_path = self.base_path / "storage" / "estados_cero"
        self.config_path = self.base_path / "storage" / "configuracion_usuario.json"

        # Cargar .env explícitamente
        from dotenv import load_dotenv
        load_dotenv(self.base_path / ".env")

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("⚠️ ANTHROPIC_API_KEY no encontrada en .env")

        self.client = anthropic.Anthropic(api_key=api_key)

        # Arquetipos de preguntas por momento
        self.arquetipos_momento = {
            "fajr": "revelación",      # Lo que emerge del inconsciente
            "dhuhr": "dirección",      # Hacia dónde se mueve la energía
            "asr": "elección",         # Qué camino tomar
            "maghrib": "cosecha",      # Qué recoger del día
            "isha": "integración"      # Qué necesita ser digerido
        }

        # Dominios del sistema
        self.dominios = [
            "cuerpo",
            "mente",
            "emoción",
            "trabajo",
            "relaciones",
            "creatividad",
            "espiritualidad",
            "salud",
            "recursos"
        ]

    def generar_pregunta_unica(
        self,
        momento: str,
        usuario_id: str = "default"
    ) -> Dict:
        """
        Genera UNA pregunta emergente para este Estado Cero específico.

        Returns:
            {
                "pregunta": str,
                "contexto": str,  # Por qué esta pregunta ahora
                "tipo": str,      # revelación, dirección, elección, etc.
                "dominios": List[str],  # Dominios que conecta
                "fase_lunar": str,
                "patron_detectado": Optional[str]
            }
        """

        # 1. Analizar contexto multi-dimensional
        contexto = self._analizar_contexto(momento, usuario_id)

        # 2. Detectar patrones recientes
        patrones = self._detectar_patrones(usuario_id)

        # 3. Identificar dominios necesitando atención
        dominios_atencion = self._identificar_dominios_atencion(usuario_id)

        # 4. Generar pregunta usando Claude
        pregunta_data = self._generar_con_claude(
            contexto=contexto,
            patrones=patrones,
            dominios_atencion=dominios_atencion,
            momento=momento
        )

        return pregunta_data

    def _analizar_contexto(self, momento: str, usuario_id: str) -> Dict:
        """
        Analiza el contexto multi-dimensional actual.
        """
        # Momento litúrgico
        arquetipoMomento = self.arquetipos_momento.get(momento, "dirección")

        # Fase lunar
        fase_lunar = self._calcular_fase_lunar()

        # Hora del día
        hora_actual = datetime.now().hour
        energia_dia = self._mapear_energia_hora(hora_actual)

        # Día de la semana
        dia_semana = datetime.now().strftime("%A")

        return {
            "momento": momento,
            "arquetipo": arquetipoMomento,
            "fase_lunar": fase_lunar,
            "energia_dia": energia_dia,
            "dia_semana": dia_semana,
            "timestamp": datetime.now().isoformat()
        }

    def _detectar_patrones(self, usuario_id: str) -> Dict:
        """
        Detecta patrones en los últimos Estados Cero (7 días).
        """
        patrones = {
            "tendencia_dominante": None,
            "ciclo_expansion_contraccion": None,
            "dominio_recurrente": None,
            "conflicto_emergente": None
        }

        # Buscar últimos estados cero
        estados_recientes = self._obtener_estados_recientes(usuario_id, dias=7)

        if not estados_recientes:
            return patrones

        # Analizar tendencias
        respuestas = []
        for estado in estados_recientes:
            if "respuestas" in estado:
                respuestas.extend([r.get("respuesta") for r in estado["respuestas"] if "respuesta" in r])

        if respuestas:
            # Tendencia: más expansión o contracción
            expansion_count = sum(1 for r in respuestas if r is True)
            contraccion_count = sum(1 for r in respuestas if r is False)

            if expansion_count > contraccion_count * 1.5:
                patrones["tendencia_dominante"] = "expansión_sostenida"
            elif contraccion_count > expansion_count * 1.5:
                patrones["tendencia_dominante"] = "contracción_prolongada"
            elif abs(expansion_count - contraccion_count) <= 1:
                patrones["tendencia_dominante"] = "equilibrio_inestable"
            else:
                patrones["tendencia_dominante"] = "oscilación_natural"

        # Buscar ciclos (patrón repetitivo)
        if len(respuestas) >= 4:
            # Últimos 4: alternan o se repiten?
            ultimos_4 = respuestas[-4:]
            if ultimos_4 == [True, False, True, False] or ultimos_4 == [False, True, False, True]:
                patrones["ciclo_expansion_contraccion"] = "alternancia_rápida"
            elif all(r == ultimos_4[0] for r in ultimos_4):
                patrones["ciclo_expansion_contraccion"] = "estancamiento"

        return patrones

    def _identificar_dominios_atencion(self, usuario_id: str) -> List[str]:
        """
        Identifica dominios que necesitan atención basado en:
        - Dominios no mencionados recientemente
        - Dominios con conflictos detectados
        - Dominios desequilibrados
        """
        # Por ahora, selección semi-aleatoria basada en momento
        # En producción, esto analizaría reflexiones y patrones

        hora = datetime.now().hour

        # Mapeo temporal basado en energía del día
        if 5 <= hora < 9:  # Fajr-mañana
            return ["cuerpo", "espiritualidad"]
        elif 12 <= hora < 15:  # Dhuhr
            return ["trabajo", "mente"]
        elif 15 <= hora < 18:  # Asr
            return ["creatividad", "emoción"]
        elif 18 <= hora < 21:  # Maghrib
            return ["relaciones", "cosecha_día"]
        else:  # Isha-noche
            return ["integración", "descanso"]

    def _generar_con_claude(
        self,
        contexto: Dict,
        patrones: Dict,
        dominios_atencion: List[str],
        momento: str
    ) -> Dict:
        """
        Usa Claude para generar una pregunta emergente única.
        """

        prompt = f"""Eres un oráculo al borde del caos. Tu tarea es generar UNA pregunta emergente para un Estado Cero.

CONTEXTO ACTUAL:
- Momento litúrgico: {momento.upper()} (arquetipo: {contexto['arquetipo']})
- Fase lunar: {contexto['fase_lunar']}
- Energía del día: {contexto['energia_dia']}
- Día: {contexto['dia_semana']}

PATRONES DETECTADOS (últimos 7 días):
- Tendencia dominante: {patrones['tendencia_dominante'] or 'Sin datos suficientes'}
- Ciclo: {patrones['ciclo_expansion_contraccion'] or 'No detectado'}

DOMINIOS NECESITANDO ATENCIÓN:
{', '.join(dominios_atencion)}

PRINCIPIOS PARA LA PREGUNTA:
1. Debe ser UNA pregunta única (no múltiple)
2. Debe conectar AL MENOS 2 de los dominios mencionados
3. Debe ser SENSORIAL o EXISTENCIAL, no puramente mental
4. NO debe tener respuesta "correcta"
5. Debe generar TENSIÓN PRODUCTIVA (revelar, no confirmar)
6. Debe resonar con el arquetipo del momento ({contexto['arquetipo']})

EJEMPLOS DE PREGUNTAS AL BORDE DEL CAOS:
- "¿Tu cuerpo sabe algo que tu mente aún no ha escuchado?"
- "¿Este momento te acerca a lo que temes o a lo que deseas?"
- "Si este día tuviera una textura, ¿sería rugosa o lisa?"
- "¿Qué está listo para ser cosechado?"
- "¿En qué estás insistiendo que ya no resuena?"

Genera SOLO la pregunta (sin explicación adicional). La pregunta debe ser poética, directa, y capaz de penetrar las defensas mentales.

PREGUNTA EMERGENTE:"""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                temperature=0.9,  # Alta creatividad
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            pregunta_generada = message.content[0].text.strip()

            # Limpiar si viene con comillas
            pregunta_generada = pregunta_generada.strip('"').strip("'")

            # Generar explicación del contexto
            contexto_pregunta = self._generar_contexto_pregunta(
                pregunta_generada,
                contexto,
                patrones,
                dominios_atencion
            )

            return {
                "pregunta": pregunta_generada,
                "contexto": contexto_pregunta,
                "tipo": contexto['arquetipo'],
                "dominios": dominios_atencion[:2],  # Principales 2 dominios
                "fase_lunar": contexto['fase_lunar'],
                "patron_detectado": patrones['tendencia_dominante']
            }

        except Exception as e:
            print(f"Error generando pregunta con Claude: {e}")
            # Fallback: pregunta por defecto según momento
            return self._pregunta_fallback(momento, contexto, dominios_atencion)

    def _generar_contexto_pregunta(
        self,
        pregunta: str,
        contexto: Dict,
        patrones: Dict,
        dominios: List[str]
    ) -> str:
        """
        Genera explicación de por qué esta pregunta ahora.
        """
        partes = []

        # Momento
        if contexto['arquetipo'] == 'revelación':
            partes.append("En este momento de revelación matutina")
        elif contexto['arquetipo'] == 'dirección':
            partes.append("En el punto medio del día")
        elif contexto['arquetipo'] == 'elección':
            partes.append("En este momento de elección vespertina")
        elif contexto['arquetipo'] == 'cosecha':
            partes.append("En este momento de recolección")
        elif contexto['arquetipo'] == 'integración':
            partes.append("En este momento de integración nocturna")

        # Patrones
        if patrones['tendencia_dominante'] == 'expansión_sostenida':
            partes.append("tu expansión reciente pide discernimiento")
        elif patrones['tendencia_dominante'] == 'contracción_prolongada':
            partes.append("tu contracción reciente busca apertura")
        elif patrones['tendencia_dominante'] == 'equilibrio_inestable':
            partes.append("tu equilibrio busca dirección")

        # Dominios
        if dominios:
            partes.append(f"conectando {' y '.join(dominios[:2])}")

        return ", ".join(partes) + "."

    def _pregunta_fallback(
        self,
        momento: str,
        contexto: Dict,
        dominios: List[str]
    ) -> Dict:
        """
        Preguntas de respaldo por momento si falla Claude.
        """
        preguntas_por_momento = {
            "fajr": [
                "¿Qué sueño aún no se ha disipado completamente?",
                "¿Tu cuerpo está listo para este día o aún resiste?",
                "¿Qué necesita ser liberado antes del amanecer interior?"
            ],
            "dhuhr": [
                "¿Hacia dónde fluye tu energía sin que lo notes?",
                "¿Qué estás construyendo sin darte cuenta?",
                "¿Este momento te acerca o te aleja de tu centro?"
            ],
            "asr": [
                "¿Qué elección has estado posponiendo?",
                "¿Tu cansancio es físico o existencial?",
                "¿Qué necesita cambiar antes del ocaso?"
            ],
            "maghrib": [
                "¿Qué cosechaste hoy que aún no has reconocido?",
                "¿Qué conversación quedó inconclusa?",
                "¿Qué parte de ti busca ser vista?"
            ],
            "isha": [
                "¿Qué necesitas soltar para descansar?",
                "¿Qué verdad emergió hoy que aún no has nombrado?",
                "¿En qué estás insistiendo que ya no resuena?"
            ]
        }

        preguntas = preguntas_por_momento.get(momento, preguntas_por_momento["dhuhr"])
        pregunta = preguntas[hash(datetime.now().date().isoformat()) % len(preguntas)]

        return {
            "pregunta": pregunta,
            "contexto": f"Pregunta emergente para {momento.upper()}.",
            "tipo": contexto['arquetipo'],
            "dominios": dominios[:2],
            "fase_lunar": contexto['fase_lunar'],
            "patron_detectado": None
        }

    # === UTILIDADES ===

    def _calcular_fase_lunar(self) -> str:
        """
        Calcula fase lunar aproximada.
        """
        # Referencia: Luna nueva conocida (2024-01-11)
        luna_nueva_ref = datetime(2024, 1, 11)
        ciclo_lunar = 29.53  # días

        dias_desde_ref = (datetime.now() - luna_nueva_ref).days
        posicion_ciclo = (dias_desde_ref % ciclo_lunar) / ciclo_lunar

        if posicion_ciclo < 0.125:
            return "Luna Nueva"
        elif posicion_ciclo < 0.375:
            return "Cuarto Creciente"
        elif posicion_ciclo < 0.625:
            return "Luna Llena"
        elif posicion_ciclo < 0.875:
            return "Cuarto Menguante"
        else:
            return "Luna Nueva"

    def _mapear_energia_hora(self, hora: int) -> str:
        """
        Mapea hora del día a tipo de energía.
        """
        if 5 <= hora < 9:
            return "emergente"
        elif 9 <= hora < 12:
            return "ascendente"
        elif 12 <= hora < 15:
            return "cenital"
        elif 15 <= hora < 18:
            return "descendente"
        elif 18 <= hora < 21:
            return "crepuscular"
        else:
            return "nocturna"

    def _obtener_estados_recientes(
        self,
        usuario_id: str,
        dias: int = 7
    ) -> List[Dict]:
        """
        Obtiene Estados Cero de los últimos N días.
        """
        estados = []
        fecha_limite = datetime.now() - timedelta(days=dias)

        if not self.estados_path.exists():
            return estados

        # Buscar archivos de estados cero
        for archivo in self.estados_path.glob("estado_*.json"):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    estado = json.load(f)

                    # Verificar fecha
                    fecha_estado = datetime.fromisoformat(estado.get("timestamp", "2000-01-01"))
                    if fecha_estado >= fecha_limite:
                        estados.append(estado)
            except Exception as e:
                print(f"Error leyendo estado {archivo}: {e}")
                continue

        return sorted(estados, key=lambda x: x.get("timestamp", ""), reverse=True)


# === FUNCIONES PÚBLICAS ===

def generar_pregunta_emergente(momento: str, usuario_id: str = "default") -> Dict:
    """
    Función principal para generar una pregunta emergente.

    Args:
        momento: Momento litúrgico (fajr, dhuhr, asr, maghrib, isha)
        usuario_id: ID del usuario

    Returns:
        Dict con pregunta y metadata
    """
    generador = GeneradorPreguntasEmergentes()
    return generador.generar_pregunta_unica(momento, usuario_id)


if __name__ == "__main__":
    # Test
    print("=== GENERADOR DE PREGUNTAS EMERGENTES ===\n")

    for momento in ["fajr", "dhuhr", "maghrib"]:
        print(f"\n{'='*50}")
        print(f"MOMENTO: {momento.upper()}")
        print('='*50)

        resultado = generar_pregunta_emergente(momento)

        print(f"\n📿 Pregunta:")
        print(f"   {resultado['pregunta']}")
        print(f"\n💭 Contexto:")
        print(f"   {resultado['contexto']}")
        print(f"\n🔗 Dominios: {', '.join(resultado['dominios'])}")
        print(f"🌙 Fase Lunar: {resultado['fase_lunar']}")
        if resultado['patron_detectado']:
            print(f"📊 Patrón: {resultado['patron_detectado']}")
