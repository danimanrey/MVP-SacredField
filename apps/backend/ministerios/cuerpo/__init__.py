"""
🏃 MINISTERIO DEL CUERPO (Jasad)

Nombre Divino: Al-Qayyūm (El Sustentador)
Pregunta Existencial: ¿Cómo habita el espíritu en este templo?

RESPONSABILIDADES:
- Ritmos circadianos alineados con tiempos litúrgicos
- Energía disponible según momento del día
- Sueño sagrado (recuperación nocturna)
- Movimiento consciente (ejercicio según contexto)
- Alimentación litúrgica (timing según Fajr/Maghrib)

MÉTRICAS DE SALUD:
1. Calidad del sueño (0-100)
2. Nivel energético actual (0-100)
3. Coherencia circadiana (0-100)
4. Movimiento diario (0-100)

PROPUESTAS SEGÚN RITMO CIRCADIANO:
- 05:00-09:00 (Fajr): Energía ascendente → Ejercicio intenso, tareas difíciles
- 09:00-12:00 (Mañana): Pico cognitivo → Trabajo profundo
- 12:00-14:00 (Dhuhr): Digestión → Comida principal, descanso ligero
- 14:00-16:00 (Post-almuerzo): Valle energético → Siesta, tareas mecánicas
- 16:00-18:00 (Asr): Segundo pico → Creatividad, socialización
- 18:00-20:00 (Maghrib): Integración → Reflexión, cierre del día
- 20:00-22:00 (Isha): Preparación nocturna → Desconexión, ritual
- 22:00-05:00 (Noche): Sueño sagrado → Recuperación profunda

Referencia: core/arquitectura/MAPEO_7_MINISTERIOS.md
"""

from datetime import datetime, time
from typing import Dict, Any, List
from ministerios import MinisterioBase

class MinisterioCuerpo(MinisterioBase):
    """
    🏃 Ministerio del Cuerpo - Al-Qayyūm (El Sustentador)
    
    Gobierna el templo físico donde habita el espíritu.
    Alinea ritmos circadianos con tiempos litúrgicos.
    """
    
    @property
    def nombre_divino(self) -> str:
        return "Al-Qayyūm (El Sustentador)"
    
    @property
    def pregunta_existencial(self) -> str:
        return "¿Cómo habita el espíritu en este templo?"
    
    def estado_actual(self) -> Dict[str, Any]:
        """
        Reporta estado actual del cuerpo.
        
        Considera:
        - Hora del día (ritmo circadiano)
        - Momento litúrgico
        - Datos de biometría (si existen)
        """
        hora_actual = datetime.now().time()
        momento_dia = self._identificar_momento_circadiano(hora_actual)
        
        return {
            "hora_actual": hora_actual.strftime("%H:%M"),
            "momento_circadiano": momento_dia["nombre"],
            "fase_energetica": momento_dia["fase"],
            "nivel_energia_esperado": momento_dia["energia_base"],
            "recomendacion_base": momento_dia["recomendacion"]
        }
    
    def responder_a_decreto(self, decreto: Any) -> Dict[str, Any]:
        """
        Responde al decreto del Sultán con perspectiva corporal.
        
        Evalúa:
        - ¿La acción requiere alta energía?
        - ¿Es el momento circadiano correcto?
        - ¿Necesita preparación física?
        """
        hora_actual = datetime.now().time()
        momento = self._identificar_momento_circadiano(hora_actual)
        
        # Analizar acción del decreto
        accion = decreto.accion_tangible.lower()
        
        # Evaluar carga energética de la acción
        requiere_alta_energia = any(palabra in accion for palabra in [
            "ejercicio", "deporte", "correr", "entrenar", "físico",
            "trabajo intenso", "crear", "construir", "implementar"
        ])
        
        requiere_calma = any(palabra in accion for palabra in [
            "meditar", "reflexionar", "leer", "escribir", "contemplar",
            "integrar", "procesar", "descansar"
        ])
        
        # Evaluar coherencia con momento circadiano
        coherencia = self._evaluar_coherencia_circadiana(
            requiere_alta_energia,
            requiere_calma,
            momento
        )
        
        # Proponer ajustes si es necesario
        propuestas = self._generar_propuestas_corporales(
            accion,
            momento,
            coherencia
        )
        
        return {
            "evaluacion": "favorable" if coherencia >= 70 else "requiere_ajustes",
            "coherencia_circadiana": coherencia,
            "momento_actual": momento["nombre"],
            "energia_disponible": momento["energia_base"],
            "propuestas": propuestas,
            "alertas": self._generar_alertas(coherencia, momento)
        }
    
    def metricas_salud(self) -> Dict[str, float]:
        """
        Métricas de salud del cuerpo.
        
        Por ahora son heurísticas basadas en hora del día.
        TODO: Integrar con datos reales de biometría.
        """
        hora_actual = datetime.now().time()
        momento = self._identificar_momento_circadiano(hora_actual)
        
        # Heurísticas basadas en ritmo circadiano
        calidad_sueno = self._estimar_calidad_sueno(hora_actual)
        energia_actual = momento["energia_base"]
        coherencia_circadiana = self._calcular_coherencia_ritmo()
        movimiento_diario = 50.0  # TODO: Integrar con datos reales
        
        return {
            "calidad_sueno": calidad_sueno,
            "energia_actual": energia_actual,
            "coherencia_circadiana": coherencia_circadiana,
            "movimiento_diario": movimiento_diario
        }
    
    # =====================================================================
    # MÉTODOS INTERNOS: Ritmos Circadianos
    # =====================================================================
    
    def _identificar_momento_circadiano(self, hora: time) -> Dict[str, Any]:
        """
        Identifica momento circadiano basándose en la hora.
        
        Ritmo circadiano alineado con tiempos litúrgicos:
        - Fajr (05:00-09:00): Energía ascendente
        - Mañana (09:00-12:00): Pico cognitivo
        - Dhuhr (12:00-14:00): Digestión
        - Post-almuerzo (14:00-16:00): Valle energético
        - Asr (16:00-18:00): Segundo pico
        - Maghrib (18:00-20:00): Integración
        - Isha (20:00-22:00): Preparación nocturna
        - Noche (22:00-05:00): Sueño sagrado
        """
        hora_num = hora.hour + hora.minute / 60
        
        if 5 <= hora_num < 9:
            return {
                "nombre": "Fajr - Energía Ascendente",
                "fase": "ascendente",
                "energia_base": 85.0,
                "recomendacion": "Ejercicio intenso, Estado Cero, tareas difíciles",
                "momento_liturgico": "fajr"
            }
        elif 9 <= hora_num < 12:
            return {
                "nombre": "Mañana - Pico Cognitivo",
                "fase": "pico",
                "energia_base": 95.0,
                "recomendacion": "Trabajo profundo, decisiones importantes",
                "momento_liturgico": "mañana"
            }
        elif 12 <= hora_num < 14:
            return {
                "nombre": "Dhuhr - Digestión",
                "fase": "neutro",
                "energia_base": 75.0,
                "recomendacion": "Comida principal, descanso ligero",
                "momento_liturgico": "dhuhr"
            }
        elif 14 <= hora_num < 16:
            return {
                "nombre": "Post-Almuerzo - Valle Energético",
                "fase": "valle",
                "energia_base": 55.0,
                "recomendacion": "Siesta 20min, tareas mecánicas, no decisiones",
                "momento_liturgico": "post_dhuhr"
            }
        elif 16 <= hora_num < 18:
            return {
                "nombre": "Asr - Segundo Pico",
                "fase": "pico_secundario",
                "energia_base": 80.0,
                "recomendacion": "Creatividad, socialización, reuniones",
                "momento_liturgico": "asr"
            }
        elif 18 <= hora_num < 20:
            return {
                "nombre": "Maghrib - Integración",
                "fase": "integracion",
                "energia_base": 65.0,
                "recomendacion": "Espejo Nocturno, cierre del día, reflexión",
                "momento_liturgico": "maghrib"
            }
        elif 20 <= hora_num < 22:
            return {
                "nombre": "Isha - Preparación Nocturna",
                "fase": "descendente",
                "energia_base": 45.0,
                "recomendacion": "Desconexión, ritual de sueño, soltar",
                "momento_liturgico": "isha"
            }
        else:  # 22:00 - 05:00
            return {
                "nombre": "Noche - Sueño Sagrado",
                "fase": "recuperacion",
                "energia_base": 20.0,
                "recomendacion": "Dormir, recuperación profunda",
                "momento_liturgico": "noche"
            }
    
    def _evaluar_coherencia_circadiana(
        self,
        requiere_alta_energia: bool,
        requiere_calma: bool,
        momento: Dict[str, Any]
    ) -> float:
        """
        Evalúa coherencia entre la acción y el momento circadiano.
        
        Returns:
            Score 0-100
        """
        fase = momento["fase"]
        energia = momento["energia_base"]
        
        # Alta energía en momentos de pico = coherente
        if requiere_alta_energia:
            if fase in ["ascendente", "pico", "pico_secundario"]:
                return 90.0
            elif fase == "neutro":
                return 70.0
            else:
                return 40.0  # Valle o recuperación → no ideal
        
        # Calma en momentos de integración/descanso = coherente
        if requiere_calma:
            if fase in ["integracion", "descendente", "recuperacion"]:
                return 95.0
            elif fase == "neutro":
                return 75.0
            else:
                return 50.0  # Pico → posible, pero no ideal
        
        # Neutro → siempre aceptable
        return 70.0
    
    def _generar_propuestas_corporales(
        self,
        accion: str,
        momento: Dict[str, Any],
        coherencia: float
    ) -> List[str]:
        """
        Genera propuestas específicas desde perspectiva corporal.
        """
        propuestas = []
        
        # Si coherencia baja, proponer ajustes
        if coherencia < 70:
            if momento["fase"] == "valle":
                propuestas.append("⚠️ Momento de valle energético. Considera posponer 1-2h o hacer siesta de 20min primero.")
            elif momento["fase"] == "recuperacion":
                propuestas.append("🌙 Momento de recuperación nocturna. Mejor ejecutar en Fajr (mañana).")
            elif momento["fase"] == "pico" and "descansar" in accion:
                propuestas.append("☀️ Momento de pico energético. Aprovecha para acción antes de descansar.")
        
        # Propuestas según momento actual
        if momento["fase"] == "ascendente":
            propuestas.append("🌅 Momento ideal para ejercicio intenso antes de la acción.")
        
        if momento["fase"] == "valle":
            propuestas.append("😴 Siesta de 20min aumentaría energía en 30%.")
        
        if momento["fase"] == "pico":
            propuestas.append("⚡ Energía óptima. Ejecuta sin preparación adicional.")
        
        if momento["fase"] == "integracion":
            propuestas.append("🌆 Momento de integración. Considera reflexión post-acción.")
        
        return propuestas
    
    def _generar_alertas(self, coherencia: float, momento: Dict[str, Any]) -> List[str]:
        """
        Genera alertas si hay riesgos corporales.
        """
        alertas = []
        
        if coherencia < 50:
            alertas.append("⚠️ ALERTA: Coherencia circadiana muy baja. Riesgo de agotamiento.")
        
        if momento["fase"] == "recuperacion":
            alertas.append("🌙 ALERTA: Momento de sueño. Ejecutar ahora compromete recuperación.")
        
        if momento["fase"] == "valle" and coherencia < 60:
            alertas.append("😴 ALERTA: Valle energético + acción intensa = alto riesgo de fracaso.")
        
        return alertas
    
    def _estimar_calidad_sueno(self, hora: time) -> float:
        """
        Estima calidad del sueño basándose en hora del día.
        
        Heurística: si es temprano (05:00-09:00), asumimos buen sueño.
        Si es tarde (22:00+), asumimos cansancio.
        """
        hora_num = hora.hour + hora.minute / 60
        
        if 5 <= hora_num < 9:
            return 85.0  # Recién despierto, asumimos buen sueño
        elif 9 <= hora_num < 14:
            return 80.0  # Aún fresco
        elif 14 <= hora_num < 18:
            return 70.0  # Tarde, algo cansado
        elif 18 <= hora_num < 22:
            return 60.0  # Noche, cansancio normal
        else:
            return 40.0  # Debería estar durmiendo
    
    def _calcular_coherencia_ritmo(self) -> float:
        """
        Calcula coherencia con ritmo circadiano natural.
        
        Por ahora, heurística simple basada en si la hora es razonable.
        TODO: Integrar con datos reales de sueño y despertar.
        """
        hora = datetime.now().time()
        hora_num = hora.hour + hora.minute / 60
        
        # Coherencia alta si está despierto en horas normales
        if 5 <= hora_num < 23:
            return 85.0
        else:
            return 30.0  # Despierto en horas de sueño = incoherente
