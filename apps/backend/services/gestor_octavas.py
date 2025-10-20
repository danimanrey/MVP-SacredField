"""
🎼 GESTOR DE OCTAVAS
═══════════════════════════════════════════════════════════════════

Gestiona la evolución de objetivos según la Ley de la Octava.

Responsabilidades:
1. Crear objetivos con estructura de octava
2. Avanzar por las 7 notas semanalmente
3. Detectar y aplicar shocks conscientes
4. Calcular coherencia armónica
5. Evolucionar a nuevas octavas (niveles superiores)
"""

from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple

from models.ley_octava import (
    ObjetivoOctava, Nota, DiaSemanaOctava, DimensionOctava,
    Armonico, ShockConsciente, FaseSemanal, EstadoOctava,
    TipoShock, AnalisisArmonicos,
    CORRESPONDENCIAS_OCTAVA, FRECUENCIAS_OCTAVA,
    generar_plan_semanal_octava, generar_armonicos_iniciales,
    calcular_coherencia_armonica, detectar_shock_pendiente,
    calcular_frecuencia_octava
)


class GestorOctavas:
    """
    Gestor central de la Ley de la Octava aplicada a manifestaciones.
    """
    
    def __init__(self):
        self.objetivos: Dict[str, ObjetivoOctava] = {}
    
    def crear_objetivo_octava(
        self,
        nombre: str,
        descripcion: str,
        dimension_primaria: DimensionOctava,
        fecha_inicio: date,
        fecha_objetivo: date,
        practica_diaria: str,
        resultado_observable: str
    ) -> ObjetivoOctava:
        """
        Crea un nuevo objetivo estructurado como octava.
        
        Genera automáticamente:
        - Nota fundamental según dimensión
        - 7 armónicos (todas las dimensiones)
        - Plan semanal de 7 fases
        - 2 shocks conscientes programados
        """
        
        # Determinar nota fundamental según dimensión
        nota_fundamental = None
        for nota, corresp in CORRESPONDENCIAS_OCTAVA.items():
            if corresp["dimension"] == dimension_primaria:
                nota_fundamental = nota
                break
        
        if not nota_fundamental:
            raise ValueError(f"Dimensión no válida: {dimension_primaria}")
        
        # Generar ID único
        objetivo_id = f"obj_{int(datetime.now().timestamp())}"
        
        # Generar armónicos
        armonicos = generar_armonicos_iniciales(dimension_primaria, nombre)
        
        # Generar plan semanal
        plan_octava = generar_plan_semanal_octava(nombre, nota_fundamental, fecha_inicio)
        
        # Generar shocks conscientes
        shocks = self._generar_shocks_conscientes(nombre, fecha_inicio)
        
        objetivo = ObjetivoOctava(
            id=objetivo_id,
            nombre=nombre,
            descripcion=descripcion,
            nota_fundamental=nota_fundamental,
            dimension_primaria=dimension_primaria,
            frecuencia_base=FRECUENCIAS_OCTAVA[nota_fundamental].frecuencia,
            armonicos=armonicos,
            fecha_inicio=fecha_inicio,
            fecha_objetivo=fecha_objetivo,
            plan_octava=plan_octava,
            shocks=shocks,
            practica_diaria=practica_diaria,
            resultado_observable=resultado_observable
        )
        
        self.objetivos[objetivo_id] = objetivo
        return objetivo
    
    def _generar_shocks_conscientes(
        self,
        objetivo_nombre: str,
        fecha_inicio: date
    ) -> List[ShockConsciente]:
        """Genera los 2 shocks conscientes de la semana"""
        
        # Encontrar el miércoles y domingo de la semana
        dias_hasta_lunes = fecha_inicio.weekday()
        lunes_semana = fecha_inicio - timedelta(days=dias_hasta_lunes)
        
        miercoles = lunes_semana + timedelta(days=2)  # Miércoles
        domingo_siguiente = lunes_semana + timedelta(days=6)  # Domingo
        
        return [
            ShockConsciente(
                tipo=TipoShock.REVISION_PROFUNDA,
                intervalo="MI-FA",
                dia=DiaSemanaOctava.MIERCOLES,
                fecha_programada=miercoles,
                realizado=False,
                accion_sugerida=f"Revisar profundamente '{objetivo_nombre}'. ¿Sigue resonando la intención?",
                pregunta_clave="¿La intención original sigue viva en mí? ¿Necesito ajustar el rumbo?",
                duracion_minutos=30
            ),
            ShockConsciente(
                tipo=TipoShock.CELEBRACION_INTEGRACION,
                intervalo="SI-DO",
                dia=DiaSemanaOctava.DOMINGO,
                fecha_programada=domingo_siguiente,
                realizado=False,
                accion_sugerida=f"Celebrar progreso en '{objetivo_nombre}'. Integrar aprendizaje. Visionar siguiente octava.",
                pregunta_clave="¿Qué he integrado esta semana? ¿Qué emerge para la siguiente octava?",
                duracion_minutos=45
            )
        ]
    
    def obtener_estado_octava_actual(
        self,
        objetivo_id: str,
        fecha_hoy: date
    ) -> EstadoOctava:
        """
        Calcula el estado actual de la octava para un objetivo.
        
        Indica:
        - En qué nota/día estamos
        - Si hay shock pendiente
        - Progreso de la semana
        """
        objetivo = self.objetivos.get(objetivo_id)
        if not objetivo:
            raise ValueError(f"Objetivo no encontrado: {objetivo_id}")
        
        # Determinar día actual
        dias_semana = ["domingo", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado"]
        dia_actual_nombre = dias_semana[fecha_hoy.weekday()]
        dia_actual = DiaSemanaOctava(dia_actual_nombre)
        
        # Obtener fase actual
        fase_actual = objetivo.plan_octava[dia_actual]
        nota_actual = fase_actual.nota
        
        # Detectar shock pendiente
        shock_pendiente = detectar_shock_pendiente(objetivo.plan_octava, dia_actual)
        
        # Calcular días hasta próximo shock
        dias_hasta_shock = None
        proximo_intervalo = None
        
        if nota_actual == Nota.MI:
            proximo_intervalo = "MI-FA"
            dias_hasta_shock = (2 - fecha_hoy.weekday()) % 7  # Hasta miércoles
        elif nota_actual == Nota.SI:
            proximo_intervalo = "SI-DO"
            dias_hasta_shock = (6 - fecha_hoy.weekday()) % 7  # Hasta domingo
        
        # Calcular progreso semanal
        dias_completados = sum(1 for fase in objetivo.plan_octava.values() if fase.completada)
        completitud = (dias_completados / 7) * 100
        
        # Determinar si requiere atención
        requiere_atencion = False
        mensaje_alerta = None
        
        if shock_pendiente and not shock_pendiente.realizado:
            requiere_atencion = True
            mensaje_alerta = f"⚡ Shock consciente requerido HOY ({shock_pendiente.intervalo})"
        
        return EstadoOctava(
            objetivo_id=objetivo_id,
            semana_actual=objetivo.octava_actual,
            dia_actual=dia_actual,
            nota_actual=nota_actual,
            proximo_intervalo_critico=proximo_intervalo,
            dias_hasta_shock=dias_hasta_shock,
            shock_pendiente=shock_pendiente,
            dias_completados=dias_completados,
            completitud_octava=completitud,
            requiere_atencion=requiere_atencion,
            mensaje_alerta=mensaje_alerta
        )
    
    def aplicar_shock_consciente(
        self,
        objetivo_id: str,
        tipo_shock: TipoShock,
        notas_usuario: str
    ) -> ShockConsciente:
        """
        Aplica un shock consciente a un objetivo.
        
        El shock inyecta energía adicional en el intervalo crítico,
        permitiendo que la octava continúe.
        """
        objetivo = self.objetivos.get(objetivo_id)
        if not objetivo:
            raise ValueError(f"Objetivo no encontrado: {objetivo_id}")
        
        # Encontrar el shock correspondiente
        shock = None
        for s in objetivo.shocks:
            if s.tipo == tipo_shock and not s.realizado:
                shock = s
                break
        
        if not shock:
            raise ValueError(f"No hay shock pendiente de tipo {tipo_shock}")
        
        # Marcar como realizado
        shock.realizado = True
        shock.notas = notas_usuario
        
        # Si es shock de integración (SI-DO), avanzar a siguiente octava
        if tipo_shock == TipoShock.CELEBRACION_INTEGRACION:
            objetivo.octava_actual += 1
            objetivo.nivel_frecuencia *= 2  # Doblar frecuencia
            objetivo.completitud_octava = 0.0  # Resetear completitud
            
            # Regenerar plan para nueva octava
            fecha_nueva_octava = shock.fecha_programada + timedelta(days=1)
            objetivo.plan_octava = generar_plan_semanal_octava(
                objetivo.nombre,
                objetivo.nota_fundamental,
                fecha_nueva_octava
            )
            
            # Regenerar shocks para nueva octava
            objetivo.shocks = self._generar_shocks_conscientes(
                objetivo.nombre,
                fecha_nueva_octava
            )
        
        objetivo.ultima_actualizacion = datetime.now()
        
        return shock
    
    def analizar_armonicos(
        self,
        objetivo_id: str
    ) -> AnalisisArmonicos:
        """
        Analiza la coherencia armónica de un objetivo.
        
        Identifica qué dimensiones están satisfechas y cuáles no.
        Genera recomendaciones para equilibrar.
        """
        objetivo = self.objetivos.get(objetivo_id)
        if not objetivo:
            raise ValueError(f"Objetivo no encontrado: {objetivo_id}")
        
        satisfechos = [
            dim for dim, arm in objetivo.armonicos.items()
            if arm.satisfecho
        ]
        
        insatisfechos = [
            dim for dim, arm in objetivo.armonicos.items()
            if not arm.satisfecho
        ]
        
        coherencia = calcular_coherencia_armonica(objetivo.armonicos)
        
        # Generar recomendaciones
        recomendaciones = []
        
        if coherencia < 50:
            recomendaciones.append(
                f"⚠️ Baja coherencia ({coherencia:.0f}%). El objetivo está fragmentado."
            )
            recomendaciones.append(
                f"Atiende las dimensiones insatisfechas: {', '.join([d.value for d in insatisfechos[:3]])}"
            )
        
        if objetivo.dimension_primaria in insatisfechos:
            recomendaciones.append(
                f"🎯 Incluso tu dimensión primaria ({objetivo.dimension_primaria.value}) está insatisfecha. Requiere atención urgente."
            )
        
        if coherencia > 80:
            recomendaciones.append(
                f"✨ Excelente coherencia ({coherencia:.0f}%). El objetivo resuena en todas las dimensiones."
            )
        
        return AnalisisArmonicos(
            objetivo_id=objetivo_id,
            nota_fundamental=objetivo.nota_fundamental,
            armonicos_satisfechos=satisfechos,
            armonicos_insatisfechos=insatisfechos,
            coherencia_armonica=coherencia,
            recomendaciones=recomendaciones
        )
    
    def avanzar_semana(
        self,
        objetivo_id: str
    ) -> ObjetivoOctava:
        """
        Avanza el objetivo a la siguiente semana (nueva octava).
        
        Solo si la octava actual está completa (7 días).
        """
        objetivo = self.objetivos.get(objetivo_id)
        if not objetivo:
            raise ValueError(f"Objetivo no encontrado: {objetivo_id}")
        
        # Verificar que la octava esté completa
        if objetivo.completitud_octava < 100:
            raise ValueError(
                f"La octava actual no está completa ({objetivo.completitud_octava:.0f}%). "
                f"Completa las 7 fases antes de avanzar."
            )
        
        # Avanzar a nueva octava
        objetivo.octava_actual += 1
        objetivo.nivel_frecuencia *= 2
        objetivo.completitud_octava = 0.0
        
        # Regenerar plan
        nueva_fecha = date.today()
        objetivo.plan_octava = generar_plan_semanal_octava(
            objetivo.nombre,
            objetivo.nota_fundamental,
            nueva_fecha
        )
        
        # Regenerar shocks
        objetivo.shocks = self._generar_shocks_conscientes(objetivo.nombre, nueva_fecha)
        
        objetivo.ultima_actualizacion = datetime.now()
        
        return objetivo
    
    def obtener_objetivos_por_dia(
        self,
        dia: DiaSemanaOctava
    ) -> List[Tuple[ObjetivoOctava, FaseSemanal]]:
        """
        Obtiene todos los objetivos que tienen actividad en un día específico.
        
        Útil para que el Entrelazador planifique el día.
        """
        objetivos_dia = []
        
        for objetivo in self.objetivos.values():
            if objetivo.estado != "activa":
                continue
            
            fase_dia = objetivo.plan_octava.get(dia)
            if fase_dia and not fase_dia.completada:
                objetivos_dia.append((objetivo, fase_dia))
        
        return objetivos_dia
    
    def obtener_shocks_pendientes_hoy(
        self,
        fecha_hoy: date
    ) -> List[Tuple[ObjetivoOctava, ShockConsciente]]:
        """
        Obtiene todos los shocks conscientes que deben aplicarse HOY.
        
        Crítico para que el Orquestador los priorice.
        """
        dias_semana = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        dia_hoy = DiaSemanaOctava(dias_semana[fecha_hoy.weekday()])
        
        shocks_hoy = []
        
        for objetivo in self.objetivos.values():
            if objetivo.estado != "activa":
                continue
            
            shock = detectar_shock_pendiente(objetivo.plan_octava, dia_hoy)
            if shock:
                shocks_hoy.append((objetivo, shock))
        
        return shocks_hoy
    
    def calcular_dimension_prioritaria_hoy(
        self,
        fecha_hoy: date
    ) -> DimensionOctava:
        """
        Calcula qué dimensión debe priorizarse HOY según el día de la semana.
        
        El Entrelazador usa esto para estructurar el día.
        """
        dias_semana = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        dia_hoy = DiaSemanaOctava(dias_semana[fecha_hoy.weekday()])
        
        # Encontrar la nota del día
        for nota, corresp in CORRESPONDENCIAS_OCTAVA.items():
            if corresp["dia"] == dia_hoy:
                return corresp["dimension"]
        
        return DimensionOctava.ESPIRITUAL  # Default
    
    def generar_resumen_octavas_activas(self) -> Dict:
        """
        Genera resumen de todas las octavas activas.
        
        Para dashboard y visualización.
        """
        objetivos_activos = [obj for obj in self.objetivos.values() if obj.estado == "activa"]
        
        if not objetivos_activos:
            return {
                "total_objetivos": 0,
                "octavas_en_progreso": 0,
                "shocks_pendientes": 0,
                "coherencia_promedio": 0.0,
                "mensaje": "No hay objetivos activos. Define tu primera manifestación."
            }
        
        # Calcular métricas
        total_octavas = sum(obj.octava_actual for obj in objetivos_activos)
        coherencias = [
            calcular_coherencia_armonica(obj.armonicos) 
            for obj in objetivos_activos
        ]
        coherencia_promedio = sum(coherencias) / len(coherencias)
        
        # Contar shocks pendientes
        shocks_pendientes = 0
        for obj in objetivos_activos:
            for shock in obj.shocks:
                if not shock.realizado:
                    shocks_pendientes += 1
        
        # Agrupar por dimensión
        por_dimension = {}
        for obj in objetivos_activos:
            dim = obj.dimension_primaria.value
            if dim not in por_dimension:
                por_dimension[dim] = []
            por_dimension[dim].append({
                "nombre": obj.nombre,
                "octava": obj.octava_actual,
                "frecuencia": obj.nivel_frecuencia,
                "coherencia": calcular_coherencia_armonica(obj.armonicos)
            })
        
        return {
            "total_objetivos": len(objetivos_activos),
            "octavas_en_progreso": total_octavas,
            "shocks_pendientes": shocks_pendientes,
            "coherencia_promedio": coherencia_promedio,
            "por_dimension": por_dimension,
            "nivel_frecuencia_promedio": sum(obj.nivel_frecuencia for obj in objetivos_activos) / len(objetivos_activos)
        }
    
    def visualizar_espiral_octavas(
        self,
        objetivo_id: str
    ) -> Dict:
        """
        Genera datos para visualizar la espiral de octavas.
        
        Retorna coordenadas para dibujar:
        - Espiral ascendente
        - Posición actual
        - Shocks aplicados
        - Próximo shock
        """
        objetivo = self.objetivos.get(objetivo_id)
        if not objetivo:
            raise ValueError(f"Objetivo no encontrado: {objetivo_id}")
        
        # Generar puntos de la espiral
        # Cada octava es un círculo, pero con radio creciente
        import math
        
        puntos = []
        notas_secuencia = [Nota.DO, Nota.RE, Nota.MI, Nota.FA, Nota.SOL, Nota.LA, Nota.SI]
        
        for octava in range(1, objetivo.octava_actual + 1):
            radio = octava * 50  # Radio crece con cada octava
            
            for i, nota in enumerate(notas_secuencia):
                angulo = (i / 7) * 2 * math.pi  # Dividir círculo en 7
                x = radio * math.cos(angulo)
                y = radio * math.sin(angulo)
                
                # Marcar si es intervalo crítico
                es_critico = nota in [Nota.MI, Nota.SI]
                
                puntos.append({
                    "octava": octava,
                    "nota": nota.value,
                    "x": x,
                    "y": y,
                    "radio": radio,
                    "angulo": angulo,
                    "es_critico": es_critico,
                    "completado": octava < objetivo.octava_actual  # Octavas anteriores están completas
                })
        
        return {
            "objetivo": objetivo.nombre,
            "octava_actual": objetivo.octava_actual,
            "frecuencia_actual": objetivo.nivel_frecuencia,
            "puntos_espiral": puntos,
            "nota_actual": objetivo.plan_octava[
                DiaSemanaOctava(["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"][date.today().weekday()])
            ].nota.value
        }

