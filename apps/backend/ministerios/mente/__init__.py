"""
🧠 MINISTERIO DE LA MENTE (Aql)

Nombre Divino: Al-'Alīm (El Conocedor)
Pregunta Existencial: ¿Cómo sirvo al conocimiento que busca manifestarse?

RESPONSABILIDADES:
- Gestión de carga cognitiva (proyectos, tareas)
- Modos de trabajo (deep work, shallow work, multitasking)
- Coherencia con ritmos circadianos cognitivos
- Performance múltiple consciente (no sobrecarga)
- Meta-aprendizaje (aprender a aprender)

PRINCIPIOS DE GESTIÓN COGNITIVA:

1. CARGA COGNITIVA LIMITADA:
   - Máximo 3 proyectos activos simultáneamente
   - 1 proyecto principal + 2 secundarios
   - Más allá de 3 → fragmentación y parálisis

2. MODOS DE TRABAJO:
   - Deep Work (90-120min): 1 proyecto, 0 distracciones
   - Shallow Work (25-45min): Tareas administrativas, emails
   - Multitasking Consciente: Solo para tareas mecánicas

3. RITMOS COGNITIVOS (alineados con Ministerio Cuerpo):
   - 05:00-09:00 (Fajr): Claridad mental → Planificación estratégica
   - 09:00-12:00 (Mañana): PICO COGNITIVO → Deep Work en proyecto principal
   - 12:00-14:00 (Dhuhr): Digestión → Shallow work, no decisiones importantes
   - 14:00-16:00 (Post-almuerzo): Valle → Tareas mecánicas, no creatividad
   - 16:00-18:00 (Asr): Segundo pico → Creatividad, ideación, conexiones
   - 18:00-20:00 (Maghrib): Integración → Revisión, cierre mental
   - 20:00-22:00 (Isha): Desconexión → Aprendizaje ligero, lectura
   - 22:00-05:00 (Noche): Consolidación → Sueño (procesamiento neuronal)

4. GESTIÓN DE PROYECTOS CONSCIENTE:
   - Cada proyecto tiene energía cognitiva asignada
   - Proyectos en "backlog" no consumen energía mental
   - Revisión semanal de prioridades
   - Cierre explícito o parking de proyectos

5. APRENDER A APRENDER:
   - Espaciado: Revisión en intervalos crecientes
   - Recuperación activa: Testing > re-lectura
   - Interleaving: Alternar temas para conexiones
   - Elaboración: Conectar nuevo conocimiento con existente
   - Generación: Crear antes de consumir

MÉTRICAS DE SALUD:
1. Carga cognitiva (0-100) - Proyectos activos vs capacidad
2. Claridad mental (0-100) - Dispersión vs enfoque
3. Momentum (0-100) - Progreso en proyecto principal
4. Aprendizaje (0-100) - Nuevas conexiones vs estancamiento

Referencia: core/arquitectura/MAPEO_7_MINISTERIOS.md
"""

from datetime import datetime, time, date, timedelta
from typing import Dict, Any, List, Optional
from enum import Enum
from ministerios import MinisterioBase


class ModoTrabajo(Enum):
    """Modos de trabajo mental"""
    DEEP_WORK = "deep_work"          # Trabajo profundo, sin distracciones
    SHALLOW_WORK = "shallow_work"    # Trabajo superficial, admin
    MULTITASKING = "multitasking"    # Multi-tarea consciente
    DESCANSO = "descanso"            # Descanso mental
    APRENDIZAJE = "aprendizaje"      # Modo aprendizaje


class EstadoProyecto(Enum):
    """Estados posibles de un proyecto"""
    ACTIVO_PRINCIPAL = "activo_principal"      # Proyecto principal (1 max)
    ACTIVO_SECUNDARIO = "activo_secundario"    # Proyecto secundario (2 max)
    BACKLOG = "backlog"                        # En backlog (no consume energía)
    COMPLETADO = "completado"                  # Completado
    PAUSADO = "pausado"                        # Pausado explícitamente


class MinisterioMente(MinisterioBase):
    """
    🧠 Ministerio de la Mente - Al-'Alīm (El Conocedor)
    
    Gobierna el espacio cognitivo: proyectos, tareas, enfoque, aprendizaje.
    Alinea trabajo mental con capacidad cognitiva y ritmos circadianos.
    """
    
    @property
    def nombre_divino(self) -> str:
        return "Al-'Alīm (El Conocedor)"
    
    @property
    def pregunta_existencial(self) -> str:
        return "¿Cómo sirvo al conocimiento que busca manifestarse?"
    
    def estado_actual(self) -> Dict[str, Any]:
        """
        Reporta estado actual de la mente.
        
        Considera:
        - Hora del día (ritmo cognitivo)
        - Carga cognitiva actual (proyectos activos)
        - Modo de trabajo recomendado
        """
        hora_actual = datetime.now().time()
        momento_cognitivo = self._identificar_momento_cognitivo(hora_actual)
        
        # TODO: Obtener proyectos activos desde DB
        # Por ahora, simulamos
        proyectos_activos = self._obtener_proyectos_activos_mock()
        carga_cognitiva = self._calcular_carga_cognitiva(proyectos_activos)
        
        return {
            "hora_actual": hora_actual.strftime("%H:%M"),
            "momento_cognitivo": momento_cognitivo["nombre"],
            "capacidad_cognitiva": momento_cognitivo["capacidad"],
            "modo_trabajo_recomendado": momento_cognitivo["modo_recomendado"],
            "proyectos_activos": len([p for p in proyectos_activos if p["estado"] != "backlog"]),
            "carga_cognitiva": carga_cognitiva,
            "recomendacion": momento_cognitivo["recomendacion"]
        }
    
    def responder_a_decreto(self, decreto: Any) -> Dict[str, Any]:
        """
        Responde al decreto del Sultán con perspectiva cognitiva.
        
        Evalúa:
        - ¿La acción requiere deep work o shallow work?
        - ¿Es el momento cognitivo correcto?
        - ¿Hay capacidad mental disponible?
        - ¿Se debe crear nuevo proyecto o es parte de existente?
        """
        hora_actual = datetime.now().time()
        momento = self._identificar_momento_cognitivo(hora_actual)
        
        # Analizar acción del decreto
        accion = decreto.accion_tangible.lower()
        
        # Evaluar tipo de trabajo requerido
        requiere_deep_work = any(palabra in accion for palabra in [
            "implementar", "diseñar", "crear", "construir", "desarrollar",
            "escribir", "programar", "arquitectura", "sistema", "complejo"
        ])
        
        requiere_aprendizaje = any(palabra in accion for palabra in [
            "aprender", "estudiar", "investigar", "explorar", "comprender",
            "analizar", "profundizar", "curso", "libro", "documentación"
        ])
        
        es_tarea_simple = any(palabra in accion for palabra in [
            "revisar", "responder", "organizar", "listar", "actualizar",
            "email", "mensaje", "llamada", "admin"
        ])
        
        # Evaluar coherencia con momento cognitivo
        coherencia = self._evaluar_coherencia_cognitiva(
            requiere_deep_work,
            requiere_aprendizaje,
            es_tarea_simple,
            momento
        )
        
        # Evaluar carga cognitiva
        proyectos_activos = self._obtener_proyectos_activos_mock()
        carga_actual = self._calcular_carga_cognitiva(proyectos_activos)
        
        # Proponer estrategia de ejecución
        estrategia = self._generar_estrategia_cognitiva(
            accion,
            momento,
            coherencia,
            carga_actual,
            requiere_deep_work,
            requiere_aprendizaje
        )
        
        return {
            "evaluacion": "favorable" if coherencia >= 70 and carga_actual < 80 else "requiere_ajustes",
            "coherencia_cognitiva": coherencia,
            "carga_cognitiva_actual": carga_actual,
            "momento_cognitivo": momento["nombre"],
            "capacidad_disponible": momento["capacidad"],
            "modo_trabajo_requerido": self._identificar_modo_trabajo(
                requiere_deep_work, requiere_aprendizaje, es_tarea_simple
            ),
            "estrategia": estrategia,
            "alertas": self._generar_alertas_cognitivas(coherencia, carga_actual, momento)
        }
    
    def metricas_salud(self) -> Dict[str, float]:
        """
        Métricas de salud mental/cognitiva.
        
        Por ahora son heurísticas basadas en hora + carga.
        TODO: Integrar con datos reales de proyectos y tareas.
        """
        hora_actual = datetime.now().time()
        momento = self._identificar_momento_cognitivo(hora_actual)
        
        # Heurísticas
        proyectos_activos = self._obtener_proyectos_activos_mock()
        carga_cognitiva = self._calcular_carga_cognitiva(proyectos_activos)
        claridad_mental = self._estimar_claridad_mental(hora_actual, carga_cognitiva)
        momentum = self._estimar_momentum(proyectos_activos)
        aprendizaje = 70.0  # TODO: Integrar con tracking real
        
        return {
            "carga_cognitiva": carga_cognitiva,
            "claridad_mental": claridad_mental,
            "momentum": momentum,
            "aprendizaje": aprendizaje
        }
    
    # =====================================================================
    # MÉTODOS INTERNOS: Ritmos Cognitivos
    # =====================================================================
    
    def _identificar_momento_cognitivo(self, hora: time) -> Dict[str, Any]:
        """
        Identifica momento cognitivo basándose en la hora.
        
        Alineado con ritmos circadianos + función cognitiva.
        """
        hora_num = hora.hour + hora.minute / 60
        
        if 5 <= hora_num < 9:
            return {
                "nombre": "Fajr - Claridad Mental",
                "capacidad": 80.0,
                "modo_recomendado": ModoTrabajo.DEEP_WORK.value,
                "recomendacion": "Planificación estratégica, decisiones importantes, arquitectura",
                "tipo_trabajo": "estratégico"
            }
        elif 9 <= hora_num < 12:
            return {
                "nombre": "Mañana - PICO COGNITIVO",
                "capacidad": 100.0,
                "modo_recomendado": ModoTrabajo.DEEP_WORK.value,
                "recomendacion": "Deep Work en proyecto principal, máxima complejidad",
                "tipo_trabajo": "profundo"
            }
        elif 12 <= hora_num < 14:
            return {
                "nombre": "Dhuhr - Digestión Mental",
                "capacidad": 70.0,
                "modo_recomendado": ModoTrabajo.SHALLOW_WORK.value,
                "recomendacion": "Tareas administrativas, no decisiones críticas",
                "tipo_trabajo": "superficial"
            }
        elif 14 <= hora_num < 16:
            return {
                "nombre": "Post-Almuerzo - Valle Cognitivo",
                "capacidad": 50.0,
                "modo_recomendado": ModoTrabajo.SHALLOW_WORK.value,
                "recomendacion": "Tareas mecánicas, reorganización, no creatividad",
                "tipo_trabajo": "mecánico"
            }
        elif 16 <= hora_num < 18:
            return {
                "nombre": "Asr - Creatividad",
                "capacidad": 85.0,
                "modo_recomendado": ModoTrabajo.DEEP_WORK.value,
                "recomendacion": "Creatividad, ideación, conexiones, brainstorming",
                "tipo_trabajo": "creativo"
            }
        elif 18 <= hora_num < 20:
            return {
                "nombre": "Maghrib - Integración",
                "capacidad": 60.0,
                "modo_recomendado": ModoTrabajo.SHALLOW_WORK.value,
                "recomendacion": "Revisión del día, cierre mental, integración",
                "tipo_trabajo": "integrativo"
            }
        elif 20 <= hora_num < 22:
            return {
                "nombre": "Isha - Aprendizaje Ligero",
                "capacidad": 45.0,
                "modo_recomendado": ModoTrabajo.APRENDIZAJE.value,
                "recomendacion": "Lectura, aprendizaje pasivo, consolidación",
                "tipo_trabajo": "receptivo"
            }
        else:  # 22:00 - 05:00
            return {
                "nombre": "Noche - Consolidación Neuronal",
                "capacidad": 10.0,
                "modo_recomendado": ModoTrabajo.DESCANSO.value,
                "recomendacion": "Dormir (procesamiento neuronal durante sueño)",
                "tipo_trabajo": "recuperación"
            }
    
    def _evaluar_coherencia_cognitiva(
        self,
        requiere_deep_work: bool,
        requiere_aprendizaje: bool,
        es_tarea_simple: bool,
        momento: Dict[str, Any]
    ) -> float:
        """
        Evalúa coherencia entre la acción y el momento cognitivo.
        
        Returns:
            Score 0-100
        """
        capacidad = momento["capacidad"]
        modo_recomendado = momento["modo_recomendado"]
        
        # Deep work en momentos de alta capacidad = coherente
        if requiere_deep_work:
            if modo_recomendado == ModoTrabajo.DEEP_WORK.value:
                return 95.0
            elif capacidad >= 70:
                return 75.0
            else:
                return 35.0  # Valle cognitivo → alto riesgo
        
        # Aprendizaje mejor en momentos específicos
        if requiere_aprendizaje:
            if modo_recomendado == ModoTrabajo.APRENDIZAJE.value:
                return 90.0
            elif momento["tipo_trabajo"] == "estratégico":
                return 85.0  # Fajr también bueno para aprender
            elif capacidad >= 80:
                return 70.0
            else:
                return 50.0
        
        # Tareas simples siempre aceptables (mejor en valles)
        if es_tarea_simple:
            if modo_recomendado == ModoTrabajo.SHALLOW_WORK.value:
                return 95.0
            else:
                return 70.0  # Desperdicia pico cognitivo, pero OK
        
        # Neutro
        return 65.0
    
    def _calcular_carga_cognitiva(self, proyectos: List[Dict]) -> float:
        """
        Calcula carga cognitiva basándose en proyectos activos.
        
        Regla: 3 proyectos = 100% de carga
        """
        activos = [p for p in proyectos if p["estado"] != "backlog"]
        
        if len(activos) == 0:
            return 0.0
        elif len(activos) == 1:
            return 33.0
        elif len(activos) == 2:
            return 66.0
        elif len(activos) == 3:
            return 90.0  # Límite saludable
        else:
            return 100.0  # Sobrecarga
    
    def _identificar_modo_trabajo(
        self,
        requiere_deep: bool,
        requiere_aprendizaje: bool,
        es_simple: bool
    ) -> str:
        """Identifica modo de trabajo requerido"""
        if requiere_deep:
            return ModoTrabajo.DEEP_WORK.value
        elif requiere_aprendizaje:
            return ModoTrabajo.APRENDIZAJE.value
        elif es_simple:
            return ModoTrabajo.SHALLOW_WORK.value
        else:
            return ModoTrabajo.DEEP_WORK.value  # Default a profundo
    
    def _generar_estrategia_cognitiva(
        self,
        accion: str,
        momento: Dict[str, Any],
        coherencia: float,
        carga: float,
        requiere_deep: bool,
        requiere_aprendizaje: bool
    ) -> Dict[str, Any]:
        """
        Genera estrategia de ejecución cognitiva.
        """
        estrategia = {
            "timeboxing": None,
            "tecnica": None,
            "preparacion": [],
            "cierre": []
        }
        
        # Timeboxing según tipo de trabajo
        if requiere_deep:
            if momento["capacidad"] >= 80:
                estrategia["timeboxing"] = "90-120min (deep work completo)"
                estrategia["tecnica"] = "Pomodoro Extendido: 90min trabajo + 20min descanso"
            else:
                estrategia["timeboxing"] = "45-60min (deep work adaptado)"
                estrategia["tecnica"] = "Pomodoro Estándar: 45min trabajo + 15min descanso"
        
        elif requiere_aprendizaje:
            estrategia["timeboxing"] = "25-45min (sesiones espaciadas)"
            estrategia["tecnica"] = "Recuperación Activa: Leer → Testar → Enseñar"
        
        else:  # Shallow work
            estrategia["timeboxing"] = "15-25min (timeboxing estricto)"
            estrategia["tecnica"] = "Batch Processing: Agrupar tareas similares"
        
        # Preparación según momento
        if momento["tipo_trabajo"] == "profundo":
            estrategia["preparacion"].extend([
                "🔕 Desactivar todas las notificaciones",
                "📝 Definir objetivo claro de la sesión",
                "🎯 Preparar entorno (cerrar tabs innecesarias)"
            ])
        
        if momento["tipo_trabajo"] == "valle" and coherencia < 60:
            estrategia["preparacion"].append(
                "☕ Considerar cafeína estratégica (si aplica)"
            )
        
        # Cierre
        estrategia["cierre"].extend([
            "📊 Documentar progreso",
            "🧠 Capturar ideas emergentes",
            "✅ Marcar completado o parking"
        ])
        
        return estrategia
    
    def _generar_alertas_cognitivas(
        self,
        coherencia: float,
        carga: float,
        momento: Dict[str, Any]
    ) -> List[str]:
        """
        Genera alertas cognitivas.
        """
        alertas = []
        
        if coherencia < 50:
            alertas.append("⚠️ ALERTA: Coherencia cognitiva muy baja. Riesgo de trabajo ineficiente.")
        
        if carga >= 90:
            alertas.append("🧠 ALERTA: Sobrecarga cognitiva. Considera pausar proyecto secundario.")
        
        if momento["capacidad"] < 60 and coherencia < 70:
            alertas.append("😴 ALERTA: Valle cognitivo + tarea compleja = alto riesgo de error.")
        
        if momento["tipo_trabajo"] == "recuperación":
            alertas.append("🌙 ALERTA: Momento de consolidación neuronal. Trabajar ahora compromete aprendizaje.")
        
        return alertas
    
    def _estimar_claridad_mental(self, hora: time, carga: float) -> float:
        """
        Estima claridad mental basándose en hora y carga.
        """
        hora_num = hora.hour + hora.minute / 60
        
        # Claridad base por hora
        if 5 <= hora_num < 12:
            claridad_base = 90.0
        elif 12 <= hora_num < 16:
            claridad_base = 65.0
        elif 16 <= hora_num < 20:
            claridad_base = 75.0
        else:
            claridad_base = 40.0
        
        # Penalización por sobrecarga
        if carga >= 90:
            claridad_base *= 0.6  # -40% por sobrecarga
        elif carga >= 70:
            claridad_base *= 0.8  # -20% por carga alta
        
        return min(claridad_base, 100.0)
    
    def _estimar_momentum(self, proyectos: List[Dict]) -> float:
        """
        Estima momentum (progreso) en proyecto principal.
        
        TODO: Integrar con tracking real de completitud.
        """
        principal = [p for p in proyectos if p["estado"] == "activo_principal"]
        
        if not principal:
            return 50.0  # Sin proyecto principal = momentum neutro
        
        # Heurística: asumimos momentum moderado
        return 70.0
    
    def _obtener_proyectos_activos_mock(self) -> List[Dict]:
        """
        Mock de proyectos activos.
        
        TODO: Obtener desde DB real.
        """
        return [
            {
                "id": 1,
                "nombre": "Dashboard Sagrado",
                "estado": "activo_principal",
                "progreso": 70
            },
            {
                "id": 2,
                "nombre": "Ministerios 7",
                "estado": "activo_secundario",
                "progreso": 30
            }
        ]
