"""
🤝 MINISTERIO DE LA CONEXIÓN (Ṣilah)

Nombre Divino: Al-Wadūd (El Amoroso)
Pregunta Existencial: ¿A quién sirvo con mi presencia?

RESPONSABILIDADES:
- Gestión consciente de círculos relacionales
- Priorización según estación de vida
- Balance presencia vs productividad
- Necesidades relacionales por círculo
- Entrelazamiento proyectos-relaciones

FILOSOFÍA DE LA CONEXIÓN SAGRADA:

"La conexión no es un recurso a gestionar.
 Es el tejido mismo de la existencia humana.
 Cada relación es un espejo del Amado."

PRINCIPIO CENTRAL:
   PRESENCIA > PRODUCTIVIDAD
   
   Estar presente con un bebé de 2 meses
   vale infinitamente más que cualquier proyecto.

CÍRCULOS DE RELACIÓN:

1. NÚCLEO FAMILIAR (Prioridad absoluta)
   └─ Bebé (2 meses) → Presencia constante, amor incondicional
   └─ Esposa/Pareja → Apoyo activo, tiempo de calidad, co-creación
   
   Necesidades específicas:
   • Bebé: Presencia física, cuidado, juego, vínculo
   • Esposa: Apoyo en proyectos, comida hecha, viajes, conversación profunda
   
   Tiempo requerido: 60-70% del tiempo disponible
   Este NO es un "gasto". Es la INVERSIÓN más alta.

2. FAMILIA EXTENDIDA (Prioridad alta)
   └─ Padres → Gratitud, visitas, apoyo
   └─ Hermano → Vínculo, complicidad
   
   Necesidades: Tiempo de calidad, presencia en momentos importantes
   Frecuencia: Semanal/quincenal según cercanía geográfica
   
3. AMIGOS CERCANOS (Círculo íntimo - 5 personas)
   └─ Relaciones profundas, vulnerabilidad, apoyo mutuo
   
   Necesidades: Conversaciones significativas, experiencias compartidas
   Frecuencia: Mensual/trimestral (calidad > cantidad)
   Potencial: Beta testers del Campo Sagrado

4. COLEGAS/PROFESIONAL (Círculo colaborativo - 15 personas)
   └─ Proyectos en común, co-creación, crecimiento mutuo
   
   Necesidades: Colaboración efectiva, comunicación clara
   Entrelazamiento: Proyectos sirven a relaciones, relaciones potencian proyectos
   Potencial: Adoptantes tempranos del sistema

ESTACIÓN DE VIDA ACTUAL: PADRE DE BEBÉ RECIÉN NACIDO

Esta estación es **sagrada y temporal**. Requiere:

✓ Aceptar reducción de productividad (es temporal)
✓ Priorizar presencia sobre proyectos
✓ Rechazar compromisos que comprometan núcleo familiar
✓ Pedir ayuda (familia, amigos)
✓ Celebrar cada momento (nunca volverán a tener 2 meses)

Duración: 0-12 meses (intensidad máxima)
          12-36 meses (intensidad alta)
          36+ meses (normalización gradual)

BALANCE RELACIONAL:

Para cada círculo, evaluar:
1. Tiempo invertido vs necesidad
2. Calidad de presencia (física, mental, emocional)
3. Balance dar/recibir
4. Necesidades insatisfechas
5. Ajustes necesarios

MÉTRICAS DE SALUD:
1. Presencia familiar (0-100) - Tiempo de calidad con núcleo
2. Vínculo extendido (0-100) - Conexión con familia/amigos
3. Colaboración (0-100) - Efectividad con colegas
4. Generosidad relacional (0-100) - Dar sin expectativas

ALERTAS RELACIONALES:
⚠️ Núcleo familiar desatendido → TODO LO DEMÁS ES SECUNDARIO
⚠️ Aislamiento social → Pedir apoyo a círculo íntimo
⚠️ Sobrecarga relacional → Decir no a círculos externos

Referencia: core/arquitectura/MAPEO_7_MINISTERIOS.md
"""

from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from enum import Enum
from ministerios import MinisterioBase


class CirculoRelacional(Enum):
    """Círculos de relación por prioridad"""
    NUCLEO_FAMILIAR = "nucleo_familiar"           # Prioridad absoluta
    FAMILIA_EXTENDIDA = "familia_extendida"       # Prioridad alta
    AMIGOS_CERCANOS = "amigos_cercanos"           # Prioridad moderada
    COLEGAS = "colegas"                           # Prioridad contextual


class EstacionVida(Enum):
    """Estaciones de vida que afectan prioridades"""
    PADRE_RECIEN_NACIDO = "padre_recien_nacido"   # 0-12 meses
    PADRE_INFANCIA = "padre_infancia"             # 1-5 años
    CRECIMIENTO_PERSONAL = "crecimiento_personal"
    CUIDADOR = "cuidador"                         # Cuidando padres/familia
    EXPANSION = "expansion"                       # Enfoque en crecimiento


class TipoPresencia(Enum):
    """Tipos de presencia en relaciones"""
    FISICA = "fisica"                 # Estar ahí físicamente
    MENTAL = "mental"                 # Atención plena
    EMOCIONAL = "emocional"          # Apertura emocional
    INSTRUMENTAL = "instrumental"     # Apoyo práctico (hacer comida, etc.)


class MinisterioConexion(MinisterioBase):
    """
    🤝 Ministerio de la Conexión - Al-Wadūd (El Amoroso)
    
    Gobierna las relaciones humanas: familia, amigos, colegas.
    Prioriza presencia sobre productividad en estación de vida actual.
    """
    
    @property
    def nombre_divino(self) -> str:
        return "Al-Wadūd (El Amoroso)"
    
    @property
    def pregunta_existencial(self) -> str:
        return "¿A quién sirvo con mi presencia?"
    
    def estado_actual(self) -> Dict[str, Any]:
        """
        Reporta estado actual de las conexiones.
        
        Considera:
        - Estación de vida (padre de bebé de 2 meses)
        - Necesidades de cada círculo
        - Balance tiempo invertido vs requerido
        """
        # Estación de vida actual
        estacion = EstacionVida.PADRE_RECIEN_NACIDO
        
        # Evaluar estado de cada círculo
        circulos = self._evaluar_circulos_relacionales()
        
        # Calcular salud relacional global
        salud_global = self._calcular_salud_relacional(circulos)
        
        return {
            "fecha": date.today().isoformat(),
            "estacion_vida": estacion.value,
            "prioridad_absoluta": "Núcleo familiar (bebé 2 meses + esposa)",
            "circulos": circulos,
            "salud_relacional": salud_global,
            "recomendacion": self._generar_recomendacion_relacional(estacion, circulos)
        }
    
    def responder_a_decreto(self, decreto: Any) -> Dict[str, Any]:
        """
        Responde al decreto desde perspectiva relacional.
        
        Evalúa:
        - ¿La acción compromete tiempo con núcleo familiar?
        - ¿La acción fortalece relaciones (proyecto con amigos/colegas)?
        - ¿Es momento de pedir ayuda al círculo íntimo?
        - ¿La acción está alineada con estación de vida?
        """
        accion = decreto.accion_tangible.lower()
        
        # Evaluar impacto relacional
        impacto = self._evaluar_impacto_relacional(accion)
        
        # Evaluar entrelazamiento con proyectos
        entrelazamiento = self._evaluar_entrelazamiento_proyectos(accion)
        
        # Evaluar coherencia con estación de vida
        coherencia_estacion = self._evaluar_coherencia_estacion_vida(
            accion,
            EstacionVida.PADRE_RECIEN_NACIDO
        )
        
        # Evaluar si puede involucrar a círculos (beta testing, colaboración)
        oportunidad_conexion = self._identificar_oportunidad_conexion(accion)
        
        # Propuestas relacionales
        propuestas = self._generar_propuestas_relacionales(
            accion,
            impacto,
            entrelazamiento,
            coherencia_estacion,
            oportunidad_conexion
        )
        
        return {
            "evaluacion": "favorable" if coherencia_estacion >= 70 else "requiere_ajustes",
            "coherencia_estacion_vida": coherencia_estacion,
            "impacto_relacional": impacto,
            "entrelazamiento_proyectos": entrelazamiento,
            "oportunidad_conexion": oportunidad_conexion,
            "propuestas": propuestas,
            "alertas": self._generar_alertas_relacionales(impacto, coherencia_estacion)
        }
    
    def metricas_salud(self) -> Dict[str, float]:
        """
        Métricas de salud relacional.
        
        Por ahora son heurísticas.
        TODO: Integrar con tracking real de tiempo con cada círculo.
        """
        # Heurísticas basadas en estación de vida
        presencia_familiar = self._estimar_presencia_familiar()
        vinculo_extendido = self._estimar_vinculo_extendido()
        colaboracion = self._estimar_colaboracion()
        generosidad = 75.0  # TODO: Tracking real de dar/recibir
        
        return {
            "presencia_familiar": presencia_familiar,
            "vinculo_extendido": vinculo_extendido,
            "colaboracion": colaboracion,
            "generosidad_relacional": generosidad
        }
    
    # =====================================================================
    # MÉTODOS INTERNOS: Gestión Relacional
    # =====================================================================
    
    def _evaluar_circulos_relacionales(self) -> Dict[str, Any]:
        """
        Evalúa estado de cada círculo relacional.
        """
        return {
            "nucleo_familiar": {
                "miembros": ["Bebé (2 meses)", "Esposa"],
                "necesidad_tiempo": "60-70% del tiempo disponible",
                "necesidad_presencia": ["física", "mental", "emocional", "instrumental"],
                "estado": "prioridad_maxima",
                "satisfaccion": 80.0,  # TODO: Tracking real
                "alertas": []
            },
            "familia_extendida": {
                "miembros": ["Padres", "Hermano"],
                "necesidad_frecuencia": "Semanal/quincenal",
                "estado": "sostenible",
                "satisfaccion": 70.0,
                "alertas": []
            },
            "amigos_cercanos": {
                "cantidad": 5,
                "tipo": "Círculo íntimo",
                "necesidad_frecuencia": "Mensual/trimestral",
                "potencial": "Beta testers Campo Sagrado",
                "estado": "sostenible",
                "satisfaccion": 65.0,
                "alertas": []
            },
            "colegas": {
                "cantidad": 15,
                "tipo": "Círculo colaborativo",
                "entrelazamiento": "Proyectos en común",
                "potencial": "Adoptantes tempranos",
                "estado": "activo",
                "satisfaccion": 70.0,
                "alertas": []
            }
        }
    
    def _evaluar_impacto_relacional(self, accion: str) -> Dict[str, Any]:
        """
        Evalúa impacto de la acción en relaciones.
        """
        # Tiempo requerido (de Ministerio Capital/Mente)
        horas_estimadas = self._estimar_horas_accion(accion)
        
        # Momento del día
        hora_actual = datetime.now().hour
        
        # ¿Compromete tiempo familiar crítico?
        if 18 <= hora_actual <= 22:  # Horario familia (tarde-noche)
            impacto_nucleo = "alto" if horas_estimadas > 2 else "moderado"
        elif 6 <= hora_actual <= 9:  # Horario mañana (bebé despierta)
            impacto_nucleo = "alto" if horas_estimadas > 1 else "moderado"
        else:
            impacto_nucleo = "bajo"
        
        return {
            "impacto_nucleo_familiar": impacto_nucleo,
            "horas_estimadas": horas_estimadas,
            "momento_dia": "familiar" if impacto_nucleo != "bajo" else "disponible",
            "requiere_coordinacion": impacto_nucleo != "bajo"
        }
    
    def _evaluar_entrelazamiento_proyectos(self, accion: str) -> Dict[str, Any]:
        """
        Evalúa si la acción entrelaza proyectos con relaciones.
        """
        # ¿Es proyecto colaborativo?
        es_colaborativo = any(palabra in accion for palabra in [
            "equipo", "colaborar", "juntos", "compartir", "enseñar",
            "documentar para", "beta", "feedback"
        ])
        
        # ¿Puede involucrar círculos?
        puede_involucrar = {
            "amigos": "beta testing" in accion or "probar" in accion,
            "colegas": "equipo" in accion or "colaborar" in accion,
            "esposa": "apoyo" in accion or "proyecto conjunto" in accion
        }
        
        nivel_entrelazamiento = "alto" if es_colaborativo else "bajo"
        
        return {
            "nivel": nivel_entrelazamiento,
            "es_colaborativo": es_colaborativo,
            "puede_involucrar": puede_involucrar,
            "potencial_conexion": any(puede_involucrar.values())
        }
    
    def _evaluar_coherencia_estacion_vida(
        self,
        accion: str,
        estacion: EstacionVida
    ) -> float:
        """
        Evalúa coherencia de la acción con estación de vida actual.
        
        Padre de recién nacido = prioridad absoluta a presencia familiar.
        """
        if estacion != EstacionVida.PADRE_RECIEN_NACIDO:
            return 70.0  # Otras estaciones tienen más flexibilidad
        
        # Para padre de bebé de 2 meses:
        horas = self._estimar_horas_accion(accion)
        
        # Acciones que fortalecen núcleo familiar
        fortalece_nucleo = any(palabra in accion for palabra in [
            "familia", "bebé", "esposa", "pareja", "descanso",
            "comida para", "apoyo", "cuidado"
        ])
        
        if fortalece_nucleo:
            return 100.0  # Perfectamente alineado
        
        # Acciones rápidas y flexibles
        if horas <= 2:
            return 80.0  # Aceptable
        
        # Inversiones en futuro (Campo Sagrado para organizar vida)
        es_inversion_organizativa = any(palabra in accion for palabra in [
            "organizar", "sistema", "automatizar", "optimizar tiempo"
        ])
        
        if es_inversion_organizativa:
            return 75.0  # Alineado a medio plazo
        
        # Proyectos grandes que requieren tiempo extenso
        if horas > 10:
            return 30.0  # Conflicto con estación de vida
        
        # Default
        return 50.0
    
    def _identificar_oportunidad_conexion(self, accion: str) -> Dict[str, Any]:
        """
        Identifica oportunidades de involucrar círculos relacionales.
        """
        oportunidades = []
        
        # ¿Puede ser beta tested por amigos?
        if any(palabra in accion for palabra in ["sistema", "app", "herramienta", "campo sagrado"]):
            oportunidades.append({
                "circulo": "amigos_cercanos",
                "accion": "Invitar a 1-2 amigos a beta testar",
                "beneficio": "Feedback + fortalecer vínculo + servicio"
            })
        
        # ¿Puede colaborar con colegas?
        if any(palabra in accion for palabra in ["proyecto", "desarrollo", "implementar"]):
            oportunidades.append({
                "circulo": "colegas",
                "accion": "Proponer como proyecto conjunto",
                "beneficio": "Co-creación + aprendizaje mutuo"
            })
        
        # ¿Puede apoyar proyecto de esposa?
        if any(palabra in accion for palabra in ["diseño", "web", "contenido", "marketing"]):
            oportunidades.append({
                "circulo": "esposa",
                "accion": "Ofrecer apoyo técnico en sus proyectos",
                "beneficio": "Apoyo activo + tiempo juntos + co-creación"
            })
        
        return {
            "hay_oportunidades": len(oportunidades) > 0,
            "cantidad": len(oportunidades),
            "oportunidades": oportunidades
        }
    
    def _generar_propuestas_relacionales(
        self,
        accion: str,
        impacto: Dict[str, Any],
        entrelazamiento: Dict[str, Any],
        coherencia: float,
        oportunidad: Dict[str, Any]
    ) -> List[str]:
        """
        Genera propuestas desde perspectiva relacional.
        """
        propuestas = []
        
        # Propuestas según impacto en núcleo
        if impacto["impacto_nucleo_familiar"] == "alto":
            propuestas.append("👨‍👩‍👦 ALTO IMPACTO FAMILIAR: Coordinar con esposa. ¿Puede ser en horario bebé duerme?")
            propuestas.append("💡 Considerar: ¿Es urgente o puede esperar a tener apoyo familiar?")
        
        # Propuestas según entrelazamiento
        if entrelazamiento["potencial_conexion"]:
            propuestas.append("🤝 OPORTUNIDAD: Este proyecto puede fortalecer relaciones.")
            for circulo, puede in entrelazamiento["puede_involucrar"].items():
                if puede:
                    propuestas.append(f"   → Involucrar {circulo}")
        
        # Propuestas según coherencia con estación
        if coherencia < 50:
            propuestas.append("⚠️ CONFLICTO CON ESTACIÓN DE VIDA: Padre de bebé de 2 meses.")
            propuestas.append("💡 Opciones: Posponer 6-12 meses o reducir scope drásticamente")
        
        # Propuestas de oportunidades específicas
        if oportunidad["hay_oportunidades"]:
            propuestas.append(f"✨ {oportunidad['cantidad']} OPORTUNIDAD(ES) DE CONEXIÓN:")
            for op in oportunidad["oportunidades"]:
                propuestas.append(f"   → {op['circulo']}: {op['accion']}")
        
        # Propuesta de ayuda familiar
        if impacto["horas_estimadas"] > 5:
            propuestas.append("🆘 CONSIDERA PEDIR AYUDA: Familia/amigos pueden apoyar con bebé.")
        
        return propuestas
    
    def _generar_alertas_relacionales(
        self,
        impacto: Dict[str, Any],
        coherencia: float
    ) -> List[str]:
        """
        Genera alertas relacionales.
        """
        alertas = []
        
        if impacto["impacto_nucleo_familiar"] == "alto":
            alertas.append("👨‍👩‍👦 ALERTA: Alto impacto en tiempo familiar. PRIORIDAD ABSOLUTA al núcleo.")
        
        if coherencia < 40:
            alertas.append("⚠️ ALERTA ESTACIÓN DE VIDA: Conflicto grave con paternidad reciente.")
            alertas.append("🍼 RECORDATORIO: Bebé de 2 meses nunca volverá. Esta ventana es sagrada.")
        
        return alertas
    
    def _calcular_salud_relacional(self, circulos: Dict[str, Any]) -> float:
        """
        Calcula salud relacional global.
        """
        # Ponderar por prioridad
        pesos = {
            "nucleo_familiar": 0.50,      # 50% del peso
            "familia_extendida": 0.20,    # 20%
            "amigos_cercanos": 0.15,      # 15%
            "colegas": 0.15               # 15%
        }
        
        salud = sum(
            circulos[circulo]["satisfaccion"] * peso
            for circulo, peso in pesos.items()
        )
        
        return salud
    
    def _generar_recomendacion_relacional(
        self,
        estacion: EstacionVida,
        circulos: Dict[str, Any]
    ) -> str:
        """
        Genera recomendación relacional.
        """
        if estacion == EstacionVida.PADRE_RECIEN_NACIDO:
            return (
                "PRIORIDAD ABSOLUTA: Núcleo familiar (bebé + esposa). "
                "Todo lo demás es secundario y puede esperar. "
                "Aceptar reducción temporal de productividad. "
                "Pedir ayuda a círculos cuando sea necesario."
            )
        
        return "Mantener balance entre círculos relacionales."
    
    def _estimar_presencia_familiar(self) -> float:
        """
        Estima presencia con núcleo familiar.
        
        En estación padre recién nacido, debería ser 60-70%.
        """
        # Heurística: si estación es padre recién nacido, asumimos presencia alta
        # TODO: Integrar con tracking real de tiempo
        return 75.0
    
    def _estimar_vinculo_extendido(self) -> float:
        """
        Estima vínculo con familia extendida y amigos.
        """
        # Heurística
        return 70.0
    
    def _estimar_colaboracion(self) -> float:
        """
        Estima efectividad de colaboración con colegas.
        """
        # Heurística
        return 75.0
    
    def _estimar_horas_accion(self, accion: str) -> float:
        """
        Estima horas requeridas para la acción.
        
        Reutiliza lógica de Ministerio Capital.
        """
        if any(palabra in accion for palabra in ["implementar", "construir", "desarrollar", "sistema"]):
            return 20.0
        elif any(palabra in accion for palabra in ["crear", "diseñar", "escribir"]):
            return 5.0
        elif any(palabra in accion for palabra in ["revisar", "actualizar", "organizar"]):
            return 2.0
        else:
            return 3.0
