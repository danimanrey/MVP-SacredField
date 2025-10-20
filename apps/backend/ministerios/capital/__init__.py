"""
💰 MINISTERIO DEL CAPITAL (Māl)

Nombre Divino: Ar-Razzāq (El Proveedor)
Pregunta Existencial: ¿Cómo fluye la abundancia a través de mí?

RESPONSABILIDADES:
- Gestión de recursos vitales (tiempo, dinero, energía)
- Inversiones conscientes vs gastos reactivos
- Gestión de riesgos en proyectos/decisiones
- Entrega energética (dar vs acumular)
- Abundancia sostenible (no agotamiento)

PRINCIPIOS DE CAPITAL SAGRADO:

1. CAPITAL NO ES SOLO DINERO:
   - Tiempo disponible (recurso más escaso)
   - Energía vital (física + mental + emocional)
   - Dinero (medio de intercambio)
   - Relaciones (red de apoyo)
   - Conocimiento (experiencia acumulada)
   - Atención (recurso cognitivo limitado)

2. INVERSIÓN VS GASTO:
   - Inversión: Retorna multiplicado (curso, herramienta, salud)
   - Gasto neutro: Mantiene status quo (comida, transporte)
   - Gasto entrópico: Disminuye capital (distracción, deuda)
   
3. RUNWAY (PISTA DE ATERRIZAJE):
   - Tiempo que puedes operar sin ingresos
   - Runway financiero: Meses de gastos cubiertos
   - Runway energético: Tiempo antes de burnout
   - Runway temporal: Margen antes de deadline
   
4. GESTIÓN DE RIESGO CONSCIENTE:
   - Riesgo asumible: Capital disponible ≥ 3x costo
   - Riesgo moderado: Capital disponible ≥ 2x costo
   - Riesgo alto: Capital disponible < 2x costo
   - Riesgo prohibido: Compromete runway mínimo
   
5. LEY DE ENTREGA ENERGÉTICA:
   - Dar < Recibir → Acumulación (estancamiento)
   - Dar = Recibir → Balance (sostenible)
   - Dar > Recibir → Entrega (generativo)
   
   Óptimo: Dar 10-20% más de lo que recibes
   (Como naturaleza: árbol da más frutos de los que necesita)

6. ABUNDANCIA SOSTENIBLE:
   - No sobre-invertir en un solo proyecto (max 40% de capital)
   - Mantener reserva de emergencia (20% intocable)
   - Diversificar inversiones (no todo en una apuesta)
   - Reinvertir ganancias (capitalización compuesta)

MÉTRICAS DE SALUD:
1. Salud financiera (0-100) - Runway + flujo de caja
2. Inversión consciente (0-100) - % de inversiones vs gastos entrópicos
3. Gestión de riesgo (0-100) - Capital disponible vs comprometido
4. Generosidad (0-100) - Ratio dar/recibir

ESTADOS DE CAPITAL:
- Abundancia (>6 meses runway): Verde 🟢
- Sostenible (3-6 meses runway): Amarillo 🟡
- Precario (<3 meses runway): Naranja 🟠
- Crítico (<1 mes runway): Rojo 🔴

Referencia: core/arquitectura/MAPEO_7_MINISTERIOS.md
"""

from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from enum import Enum
from ministerios import MinisterioBase


class TipoRecurso(Enum):
    """Tipos de capital/recursos"""
    TIEMPO = "tiempo"
    ENERGIA = "energia"
    DINERO = "dinero"
    ATENCION = "atencion"
    CONOCIMIENTO = "conocimiento"
    RELACIONES = "relaciones"


class TipoMovimiento(Enum):
    """Tipos de movimientos de capital"""
    INVERSION = "inversion"           # Retorna multiplicado
    GASTO_NEUTRO = "gasto_neutro"     # Mantiene status quo
    GASTO_ENTROPICO = "gasto_entropico"  # Disminuye capital
    ENTRADA = "entrada"               # Ingreso de capital


class EstadoCapital(Enum):
    """Estados de salud del capital"""
    ABUNDANCIA = "abundancia"      # >6 meses runway
    SOSTENIBLE = "sostenible"      # 3-6 meses runway
    PRECARIO = "precario"          # <3 meses runway
    CRITICO = "critico"            # <1 mes runway


class MinisterioCapital(MinisterioBase):
    """
    💰 Ministerio del Capital - Ar-Razzāq (El Proveedor)
    
    Gobierna el flujo de abundancia: recursos, inversiones, riesgo, entrega.
    Asegura sostenibilidad sin agotamiento.
    """
    
    @property
    def nombre_divino(self) -> str:
        return "Ar-Razzāq (El Proveedor)"
    
    @property
    def pregunta_existencial(self) -> str:
        return "¿Cómo fluye la abundancia a través de mí?"
    
    def estado_actual(self) -> Dict[str, Any]:
        """
        Reporta estado actual del capital.
        
        Considera:
        - Runway financiero (meses de gastos cubiertos)
        - Runway energético (tiempo antes de burnout)
        - Runway temporal (margen antes de deadline)
        - Balance dar/recibir
        """
        # TODO: Obtener datos reales desde DB
        # Por ahora, simulamos con heurísticas
        
        capital_financiero = self._estimar_capital_financiero_mock()
        capital_energetico = self._estimar_capital_energetico()
        capital_temporal = self._estimar_capital_temporal()
        
        return {
            "fecha": date.today().isoformat(),
            "capital_financiero": capital_financiero,
            "capital_energetico": capital_energetico,
            "capital_temporal": capital_temporal,
            "estado_general": self._determinar_estado_general([
                capital_financiero["estado"],
                capital_energetico["estado"],
                capital_temporal["estado"]
            ]),
            "recomendacion": self._generar_recomendacion_capital(capital_financiero, capital_energetico)
        }
    
    def responder_a_decreto(self, decreto: Any) -> Dict[str, Any]:
        """
        Responde al decreto del Sultán con perspectiva de capital.
        
        Evalúa:
        - ¿La acción es inversión o gasto?
        - ¿Hay capital disponible (tiempo, energía, dinero)?
        - ¿Cuál es el riesgo asumido?
        - ¿Compromete runway mínimo?
        - ¿Balance de entrega vs acumulación?
        """
        accion = decreto.accion_tangible.lower()
        
        # Estimar costo en diferentes capitales
        costo_estimado = self._estimar_costo_accion(accion)
        
        # Evaluar tipo de movimiento (inversión vs gasto)
        tipo_movimiento = self._clasificar_movimiento(accion)
        
        # Evaluar capital disponible
        capital_actual = {
            "financiero": self._estimar_capital_financiero_mock(),
            "energetico": self._estimar_capital_energetico(),
            "temporal": self._estimar_capital_temporal()
        }
        
        # Evaluar riesgo
        riesgo = self._evaluar_riesgo(costo_estimado, capital_actual)
        
        # Evaluar viabilidad
        viabilidad = self._evaluar_viabilidad_capital(costo_estimado, capital_actual, riesgo)
        
        # Propuestas de optimización
        propuestas = self._generar_propuestas_capital(
            accion, tipo_movimiento, riesgo, capital_actual, costo_estimado
        )
        
        return {
            "evaluacion": "favorable" if viabilidad >= 70 else "requiere_ajustes",
            "viabilidad_capital": viabilidad,
            "tipo_movimiento": tipo_movimiento.value,
            "costo_estimado": costo_estimado,
            "capital_disponible": {
                "tiempo": capital_actual["temporal"]["horas_disponibles_semana"],
                "energia": capital_actual["energetico"]["porcentaje"],
                "runway_financiero": capital_actual["financiero"]["runway_meses"]
            },
            "nivel_riesgo": riesgo["nivel"],
            "ratio_riesgo": riesgo["ratio"],
            "propuestas": propuestas,
            "alertas": self._generar_alertas_capital(riesgo, capital_actual)
        }
    
    def metricas_salud(self) -> Dict[str, float]:
        """
        Métricas de salud del capital.
        
        Por ahora son heurísticas.
        TODO: Integrar con datos reales de finanzas y tracking.
        """
        capital_financiero = self._estimar_capital_financiero_mock()
        
        # Heurísticas
        salud_financiera = self._calcular_salud_financiera(capital_financiero)
        inversion_consciente = 70.0  # TODO: Tracking real de inversiones vs gastos
        gestion_riesgo = self._calcular_gestion_riesgo(capital_financiero)
        generosidad = 60.0  # TODO: Tracking real de dar/recibir
        
        return {
            "salud_financiera": salud_financiera,
            "inversion_consciente": inversion_consciente,
            "gestion_riesgo": gestion_riesgo,
            "generosidad": generosidad
        }
    
    # =====================================================================
    # MÉTODOS INTERNOS: Gestión de Capital
    # =====================================================================
    
    def _estimar_capital_financiero_mock(self) -> Dict[str, Any]:
        """
        Estima capital financiero.
        
        TODO: Integrar con datos reales de finanzas.
        """
        # Mock: Asumimos runway de 4 meses (sostenible)
        runway_meses = 4.0
        gastos_mensuales = 2000.0  # EUR
        capital_disponible = runway_meses * gastos_mensuales
        
        if runway_meses > 6:
            estado = EstadoCapital.ABUNDANCIA
        elif runway_meses >= 3:
            estado = EstadoCapital.SOSTENIBLE
        elif runway_meses >= 1:
            estado = EstadoCapital.PRECARIO
        else:
            estado = EstadoCapital.CRITICO
        
        return {
            "runway_meses": runway_meses,
            "capital_disponible": capital_disponible,
            "gastos_mensuales": gastos_mensuales,
            "estado": estado.value,
            "emoji": self._emoji_estado(estado)
        }
    
    def _estimar_capital_energetico(self) -> Dict[str, Any]:
        """
        Estima capital energético (tiempo antes de burnout).
        
        Basado en carga actual vs capacidad.
        """
        # Obtener carga de Ministerios Cuerpo y Mente
        # Por ahora, heurística
        hora_actual = datetime.now().hour
        
        if 9 <= hora_actual < 18:
            energia_porcentaje = 70.0
            runway_dias = 30  # Un mes de energía sostenible
            estado = EstadoCapital.SOSTENIBLE
        elif 18 <= hora_actual < 22:
            energia_porcentaje = 50.0
            runway_dias = 20
            estado = EstadoCapital.SOSTENIBLE
        else:
            energia_porcentaje = 30.0
            runway_dias = 15
            estado = EstadoCapital.PRECARIO
        
        return {
            "porcentaje": energia_porcentaje,
            "runway_dias": runway_dias,
            "estado": estado.value,
            "emoji": self._emoji_estado(estado)
        }
    
    def _estimar_capital_temporal(self) -> Dict[str, Any]:
        """
        Estima capital temporal (tiempo disponible).
        
        Basado en compromisos actuales.
        """
        # Heurística: 40h semana disponibles
        # TODO: Integrar con calendario y compromisos reales
        
        horas_semana_totales = 168  # 7 días × 24h
        horas_dormir = 56  # 8h × 7
        horas_esenciales = 28  # Comida, higiene, etc.
        horas_compromisos = 40  # Trabajo, etc.
        
        horas_disponibles = horas_semana_totales - horas_dormir - horas_esenciales - horas_compromisos
        porcentaje_disponible = (horas_disponibles / horas_semana_totales) * 100
        
        if porcentaje_disponible > 30:
            estado = EstadoCapital.ABUNDANCIA
        elif porcentaje_disponible >= 20:
            estado = EstadoCapital.SOSTENIBLE
        elif porcentaje_disponible >= 10:
            estado = EstadoCapital.PRECARIO
        else:
            estado = EstadoCapital.CRITICO
        
        return {
            "horas_disponibles_semana": horas_disponibles,
            "porcentaje_disponible": porcentaje_disponible,
            "horas_comprometidas": horas_compromisos,
            "estado": estado.value,
            "emoji": self._emoji_estado(estado)
        }
    
    def _estimar_costo_accion(self, accion: str) -> Dict[str, Any]:
        """
        Estima costo de una acción en diferentes capitales.
        """
        # Heurísticas basadas en palabras clave
        
        # Tiempo estimado
        if any(palabra in accion for palabra in ["implementar", "construir", "desarrollar", "sistema"]):
            horas_tiempo = 20.0  # Proyecto grande
        elif any(palabra in accion for palabra in ["crear", "diseñar", "escribir"]):
            horas_tiempo = 5.0  # Proyecto mediano
        elif any(palabra in accion for palabra in ["revisar", "actualizar", "organizar"]):
            horas_tiempo = 2.0  # Tarea simple
        else:
            horas_tiempo = 3.0  # Default
        
        # Energía estimada (% de reservas)
        if "complejo" in accion or "sistema" in accion:
            energia_porcentaje = 40.0
        elif "simple" in accion or "ligero" in accion:
            energia_porcentaje = 10.0
        else:
            energia_porcentaje = 20.0
        
        # Dinero estimado (si aplica)
        costo_dinero = 0.0
        if "curso" in accion or "comprar" in accion:
            costo_dinero = 100.0  # EUR
        elif "herramienta" in accion or "software" in accion:
            costo_dinero = 50.0
        
        return {
            "tiempo_horas": horas_tiempo,
            "energia_porcentaje": energia_porcentaje,
            "dinero_euros": costo_dinero
        }
    
    def _clasificar_movimiento(self, accion: str) -> TipoMovimiento:
        """
        Clasifica si la acción es inversión, gasto neutro o entrópico.
        """
        # Inversiones: Retornan multiplicado
        if any(palabra in accion for palabra in [
            "aprender", "curso", "estudiar", "salud", "ejercicio",
            "herramienta", "sistema", "automatizar", "optimizar"
        ]):
            return TipoMovimiento.INVERSION
        
        # Gastos entrópicos: Disminuyen capital
        if any(palabra in accion for palabra in [
            "distracción", "procrastinar", "redes sociales", "scrolling"
        ]):
            return TipoMovimiento.GASTO_ENTROPICO
        
        # Default: Gasto neutro
        return TipoMovimiento.GASTO_NEUTRO
    
    def _evaluar_riesgo(
        self,
        costo: Dict[str, Any],
        capital: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evalúa riesgo de la acción según capital disponible.
        
        Riesgo = Costo / Capital disponible
        """
        # Riesgo temporal
        horas_disponibles = capital["temporal"]["horas_disponibles_semana"]
        costo_horas = costo["tiempo_horas"]
        ratio_temporal = (costo_horas / horas_disponibles) * 100 if horas_disponibles > 0 else 100
        
        # Riesgo energético
        energia_disponible = capital["energetico"]["porcentaje"]
        costo_energia = costo["energia_porcentaje"]
        ratio_energetico = (costo_energia / energia_disponible) * 100 if energia_disponible > 0 else 100
        
        # Riesgo financiero
        capital_financiero = capital["financiero"]["capital_disponible"]
        costo_dinero = costo["dinero_euros"]
        ratio_financiero = (costo_dinero / capital_financiero) * 100 if capital_financiero > 0 else 0
        
        # Ratio máximo determina nivel de riesgo
        ratio_max = max(ratio_temporal, ratio_energetico, ratio_financiero)
        
        if ratio_max < 33:
            nivel = "bajo"  # Costo < 33% del capital
        elif ratio_max < 50:
            nivel = "moderado"  # Costo 33-50% del capital
        elif ratio_max < 80:
            nivel = "alto"  # Costo 50-80% del capital
        else:
            nivel = "prohibido"  # Costo > 80% del capital
        
        return {
            "nivel": nivel,
            "ratio": ratio_max,
            "ratios": {
                "temporal": ratio_temporal,
                "energetico": ratio_energetico,
                "financiero": ratio_financiero
            }
        }
    
    def _evaluar_viabilidad_capital(
        self,
        costo: Dict[str, Any],
        capital: Dict[str, Any],
        riesgo: Dict[str, Any]
    ) -> float:
        """
        Evalúa viabilidad total basándose en capital y riesgo.
        
        Returns:
            Score 0-100
        """
        # Viabilidad base según riesgo
        if riesgo["nivel"] == "bajo":
            viabilidad_base = 90.0
        elif riesgo["nivel"] == "moderado":
            viabilidad_base = 70.0
        elif riesgo["nivel"] == "alto":
            viabilidad_base = 45.0
        else:  # prohibido
            viabilidad_base = 20.0
        
        # Ajustar según estado de cada capital
        estados = [
            capital["financiero"]["estado"],
            capital["energetico"]["estado"],
            capital["temporal"]["estado"]
        ]
        
        if all(e in ["abundancia", "sostenible"] for e in estados):
            ajuste = 1.1  # +10%
        elif any(e == "critico" for e in estados):
            ajuste = 0.7  # -30%
        else:
            ajuste = 1.0
        
        return min(viabilidad_base * ajuste, 100.0)
    
    def _generar_propuestas_capital(
        self,
        accion: str,
        tipo_movimiento: TipoMovimiento,
        riesgo: Dict[str, Any],
        capital: Dict[str, Any],
        costo: Dict[str, Any]
    ) -> List[str]:
        """
        Genera propuestas específicas desde perspectiva de capital.
        """
        propuestas = []
        
        # Propuestas según tipo de movimiento
        if tipo_movimiento == TipoMovimiento.INVERSION:
            propuestas.append("💎 INVERSIÓN DETECTADA: Esta acción retornará multiplicado")
            if riesgo["nivel"] in ["bajo", "moderado"]:
                propuestas.append("✅ Riesgo asumible para inversión. Adelante.")
        
        # Propuestas según nivel de riesgo
        if riesgo["nivel"] == "alto":
            propuestas.append("⚠️ Riesgo alto. Considera dividir en fases más pequeñas.")
            propuestas.append(f"📊 Costo = {riesgo['ratio']:.0f}% del capital disponible")
        
        if riesgo["nivel"] == "prohibido":
            propuestas.append("🛑 RIESGO PROHIBIDO: Compromete runway mínimo")
            propuestas.append("💡 Opción: Reducir scope o buscar recursos adicionales")
        
        # Propuestas según capital temporal
        if riesgo["ratios"]["temporal"] > 40:
            horas_necesarias = costo["tiempo_horas"]
            propuestas.append(f"⏰ Requiere {horas_necesarias:.0f}h. Considera extender plazo.")
        
        # Propuestas según capital energético
        if riesgo["ratios"]["energetico"] > 50:
            propuestas.append("🔋 Alto consumo energético. Programa descansos frecuentes.")
        
        # Propuestas de optimización
        if tipo_movimiento == TipoMovimiento.GASTO_NEUTRO:
            propuestas.append("🔄 Gasto neutro. Pregunta: ¿Se puede convertir en inversión?")
        
        return propuestas
    
    def _generar_alertas_capital(
        self,
        riesgo: Dict[str, Any],
        capital: Dict[str, Any]
    ) -> List[str]:
        """
        Genera alertas de capital.
        """
        alertas = []
        
        if riesgo["nivel"] == "prohibido":
            alertas.append("🛑 ALERTA CRÍTICA: Riesgo prohibido. Compromete runway mínimo.")
        
        if capital["financiero"]["estado"] == "critico":
            alertas.append("💰 ALERTA: Runway financiero < 1 mes. Priorizar ingresos.")
        
        if capital["energetico"]["estado"] == "critico":
            alertas.append("🔋 ALERTA: Capital energético bajo. Riesgo de burnout.")
        
        if capital["temporal"]["estado"] == "critico":
            alertas.append("⏰ ALERTA: Capital temporal agotado. Eliminar compromisos.")
        
        return alertas
    
    def _determinar_estado_general(self, estados: List[str]) -> str:
        """Determina estado general basándose en estados individuales"""
        if any(e == "critico" for e in estados):
            return "critico"
        elif any(e == "precario" for e in estados):
            return "precario"
        elif all(e == "abundancia" for e in estados):
            return "abundancia"
        else:
            return "sostenible"
    
    def _generar_recomendacion_capital(
        self,
        financiero: Dict[str, Any],
        energetico: Dict[str, Any]
    ) -> str:
        """Genera recomendación basándose en estado del capital"""
        if financiero["estado"] == "critico":
            return "PRIORIDAD: Generar ingresos. Posponer inversiones no-esenciales."
        elif energetico["estado"] == "critico":
            return "PRIORIDAD: Recuperación energética. Rechazar nuevos compromisos."
        elif financiero["estado"] == "abundancia":
            return "Momento de invertir. Considera proyectos de largo plazo."
        else:
            return "Mantener curso sostenible. Optimizar inversiones existentes."
    
    def _emoji_estado(self, estado: EstadoCapital) -> str:
        """Retorna emoji según estado"""
        return {
            EstadoCapital.ABUNDANCIA: "🟢",
            EstadoCapital.SOSTENIBLE: "🟡",
            EstadoCapital.PRECARIO: "🟠",
            EstadoCapital.CRITICO: "🔴"
        }.get(estado, "⚪")
    
    def _calcular_salud_financiera(self, capital: Dict[str, Any]) -> float:
        """Calcula salud financiera (0-100) basándose en runway"""
        runway = capital["runway_meses"]
        
        if runway > 12:
            return 100.0
        elif runway > 6:
            return 90.0
        elif runway >= 3:
            return 70.0
        elif runway >= 1:
            return 40.0
        else:
            return 20.0
    
    def _calcular_gestion_riesgo(self, capital: Dict[str, Any]) -> float:
        """Calcula gestión de riesgo (0-100)"""
        # Heurística: Si hay runway sostenible, gestión es buena
        if capital["estado"] == "abundancia":
            return 90.0
        elif capital["estado"] == "sostenible":
            return 75.0
        elif capital["estado"] == "precario":
            return 50.0
        else:
            return 25.0
