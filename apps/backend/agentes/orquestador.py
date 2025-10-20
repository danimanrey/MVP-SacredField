from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Any
import json
import uuid
from sqlalchemy.orm import Session

from models.schemas import (
    AccionConcreta, ContextoCompleto, JornadaAlBordeCaos,
    BloqueTiempo, PuntoDecision, NoNegociable, TipoNoNegociable,
    EstructuraDia, AnclaDia
)
from models.decreto_sacral import DecretoSacral  # 🏛️ Arquitectura Sagrada
from services.claude_client import ClaudeClient
from services.tiempos_liturgicos import CalculadorTiemposLiturgicos

# 🏛️ Arquitectura Sagrada: Gabinete Ministerial
from ministerios import obtener_gabinete


class AgenteOrquestador:
    """
    🎼 AGENTE ORQUESTADOR - El Primer Ministro (Aql)
    
    PODER EJECUTIVO del gobierno del reino humano.
    
    Responsabilidades:
    - RECIBE decreto del Sultán (Estado Cero)
    - CONSULTA con los 7 Ministerios
    - ORGANIZA la jornada al borde del caos
    - COORDINA recursos y tiempos
    - EJECUTA con Ihsān (excelencia)
    
    Arquitectura Sagrada:
    - Parte de los 3 Poderes de Gobierno
    - Opera EN los 7 Ministerios
    - Sirve al decreto del Sultán sin cuestionarlo
    
    Referencia: core/arquitectura/TRES_PODERES_GOBIERNO_DIVINO.md
    """
    
    def __init__(
        self,
        db: Session,
        claude: ClaudeClient,
        calculador_tiempos: CalculadorTiemposLiturgicos
    ):
        self.db = db
        self.claude = claude
        self.calculador_tiempos = calculador_tiempos
        self.plan_actual: Optional[JornadaAlBordeCaos] = None
        
        # 🏛️ Gabinete Ministerial (arquitectura sagrada)
        self.gabinete = obtener_gabinete()
        self._registrar_ministerios()
    
    def _registrar_ministerios(self):
        """
        Registra los 7 ministerios en el gabinete.
        
        NOTA: Registro lazy para evitar dependencias circulares.
        Solo registramos ministerios al momento de usarlos.
        """
        try:
            from ministerios.mente import MinisterioMente
            from ministerios.cuerpo import MinisterioCuerpo
            from ministerios.capital import MinisterioCapital
            from ministerios.conexion import MinisterioConexion
            from ministerios.creacion import MinisterioCreacion
            from ministerios.significado import MinisterioSignificado
            from ministerios.soberania import MinisterioSoberania
            
            self.gabinete.registrar_ministerio("mente", MinisterioMente())
            self.gabinete.registrar_ministerio("cuerpo", MinisterioCuerpo())
            self.gabinete.registrar_ministerio("capital", MinisterioCapital())
            self.gabinete.registrar_ministerio("conexion", MinisterioConexion())
            self.gabinete.registrar_ministerio("creacion", MinisterioCreacion())
            self.gabinete.registrar_ministerio("significado", MinisterioSignificado())
            self.gabinete.registrar_ministerio("soberania", MinisterioSoberania())
        except Exception as e:
            # Si falla, continuar sin ministerios (backwards compatibility)
            print(f"⚠️ No se pudieron registrar ministerios: {e}")
    
    def obtener_decreto_activo(self) -> Optional[DecretoSacral]:
        """
        🏛️ PODER EJECUTIVO: Verifica decreto del Sultán
        
        El Primer Ministro NO puede actuar sin decreto.
        Esta es la base de los 3 Poderes de Gobierno.
        
        Returns:
            DecretoSacral activo para hoy, o None si no existe
        """
        decreto = self.db.query(DecretoSacral).filter(
            DecretoSacral.fecha == date.today(),
            DecretoSacral.esta_activo
        ).first()
        
        if not decreto:
            print("⚠️ NO HAY DECRETO SACRAL - Primer Ministro no puede actuar")
            return None
        
        if decreto.estado != "pendiente":
            print(f"ℹ️ Decreto ya {decreto.estado}: {decreto.id}")
        
        return decreto
    
    async def consultar_gabinete_ministerial(self, decreto: DecretoSacral) -> Dict[str, Any]:
        """
        🏛️ CONSULTA CON LOS 7 MINISTERIOS
        
        El Primer Ministro consulta con su gabinete para ejecutar
        el decreto del Sultán.
        
        Args:
            decreto: DecretoSacral a ejecutar
            
        Returns:
            Dict con reportes de cada ministerio consultado
        """
        print(f"\n🏛️ GABINETE MINISTERIAL - Consulta para decreto {decreto.id}")
        print(f"   Acción: {decreto.accion_tangible}")
        
        # Consultar cada ministerio
        reportes = {}
        
        ministerios_a_consultar = [
            "mente",      # Estado mental, tareas cognitivas
            "cuerpo",     # Energía, deporte, sueño
            "capital",    # Recursos financieros
            "conexion",   # Relaciones, comunicación
            "creacion",   # Proyectos creativos
            "significado",# Propósito, trascendencia
            "soberania"   # Autonomía, decisiones
        ]
        
        for ministerio_id in ministerios_a_consultar:
            try:
                # Contexto para el ministerio
                contexto = {
                    "decreto_id": decreto.id,
                    "accion": decreto.accion_tangible,
                    "direccion": decreto.direccion_emergente,
                    "momento": decreto.momento_liturgico
                }
                
                # Consultar ministerio
                reporte = self.gabinete.consultar_ministerio(ministerio_id, contexto)
                reportes[ministerio_id] = reporte
                
                print(f"   ✅ {ministerio_id.upper()}: {reporte.get('estado', 'OK')}")
                
            except Exception as e:
                print(f"   ⚠️ {ministerio_id.upper()}: Error - {e}")
                reportes[ministerio_id] = {"error": str(e)}
        
        return reportes
    
    async def ejecutar_decreto(self, decreto_id: str) -> JornadaAlBordeCaos:
        """
        🏛️ PODER EJECUTIVO: Ejecuta Decreto del Sultán
        
        Flujo completo:
        1. Verificar que existe decreto
        2. Consultar Gabinete Ministerial
        3. Organizar jornada al borde del caos
        4. Marcar decreto como "en_ejecucion"
        
        Args:
            decreto_id: ID del DecretoSacral a ejecutar
            
        Returns:
            JornadaAlBordeCaos planificada
        """
        # 1. Obtener decreto
        decreto = self.db.query(DecretoSacral).filter(
            DecretoSacral.id == decreto_id
        ).first()
        
        if not decreto:
            raise ValueError(f"Decreto {decreto_id} no encontrado")
        
        if not decreto.validado_contra_pilares:
            print("⚠️ Decreto NO validado contra 8 Pilares (ejecutando de todos modos)")
        
        # 2. Consultar Gabinete Ministerial
        reportes_ministeriales = await self.consultar_gabinete_ministerial(decreto)
        
        # 3. Generar plan basándose en decreto + reportes
        plan = await self._generar_plan_desde_decreto(decreto, reportes_ministeriales)
        
        # 4. Marcar decreto como en ejecución
        decreto.estado = "en_ejecucion"
        self.db.commit()
        
        print(f"\n🎼 ORQUESTADOR: Plan generado para decreto {decreto.id}")
        print(f"   {len(plan.bloques_sugeridos)} bloques organizados")
        print(f"   {plan.espacio_emergencia}% espacio emergente")
        
        return plan
    
    async def _generar_plan_desde_decreto(
        self,
        decreto: DecretoSacral,
        reportes: Dict[str, Any]
    ) -> JornadaAlBordeCaos:
        """
        Genera JornadaAlBordeCaos basándose en:
        - DecretoSacral (dirección + acción)
        - Reportes de los 7 Ministerios
        
        Por ahora genera plan básico.
        TODO: Usar reportes ministeriales para ajustar bloques.
        """
        # Calcular tiempos litúrgicos
        tiempos = self.calculador_tiempos.calcular_tiempos_dia()
        
        # Bloques básicos del día
        bloques = [
            BloqueTiempo(
                id=str(uuid.uuid4()),
                inicio_aprox=tiempos["fajr"].strftime("%H:%M"),
                duracion="15min",
                actividad="🕌 FAJR - Rezo + Estado Cero",
                rol="Ancla sagrada",
                energia_optima=2,
                flexible=False,
                opciones_alternativas=[]
            ),
            BloqueTiempo(
                id=str(uuid.uuid4()),
                inicio_aprox="09:00",
                duracion="120min",
                actividad=f"⚡ ACCIÓN PRINCIPAL: {decreto.accion_tangible}",
                rol="Ejecución del decreto",
                energia_optima=4,
                flexible=True,
                opciones_alternativas=["Mover a 10:00", "Mover a 11:00"]
            ),
            BloqueTiempo(
                id=str(uuid.uuid4()),
                inicio_aprox=tiempos["dhuhr"].strftime("%H:%M"),
                duracion="15min",
                actividad="🕌 DHUHR - Rezo + Revisión",
                rol="Ancla sagrada",
                energia_optima=3,
                flexible=False,
                opciones_alternativas=[]
            ),
            BloqueTiempo(
                id=str(uuid.uuid4()),
                inicio_aprox=tiempos["maghrib"].strftime("%H:%M"),
                duracion="30min",
                actividad="🕌 MAGHRIB - Integración diaria",
                rol="Ancla sagrada",
                energia_optima=2,
                flexible=False,
                opciones_alternativas=[]
            )
        ]
        
        # TODO: Usar reportes ministeriales para añadir bloques específicos
        # Por ejemplo:
        # - Si Ministerio Cuerpo reporta baja energía → añadir siesta
        # - Si Ministerio Capital necesita acción → añadir revisión financiera
        # - etc.
        
        return JornadaAlBordeCaos(
            fecha=date.today(),
            accion_principal=decreto.accion_tangible,
            bloques_sugeridos=bloques,
            puntos_decision=[],
            espacio_emergencia=40.0,  # Borde del caos
            no_negociables=[],
            flexible=True,
            ultima_actualizacion=datetime.now()
        )
    
    async def actualizar_espejo_con_estado_cero(
        self,
        plan_actual: JornadaAlBordeCaos,
        direccion_emergente: str,
        momento: str,
        respuestas_sacra: List[Any]
    ) -> JornadaAlBordeCaos:
        """
        ACTUALIZACIÓN INCREMENTAL DEL ESPEJO
        
        El Espejo se refina con cada Estado Cero según el propósito del momento:
        
        FAJR (INICIO):
            → Refina PLAN COMPLETO del día con dirección
            → Ajusta bloques de todo el día
        
        DHUHR (REVISIÓN):
            → Ajusta BLOQUES DE TARDE según progreso mañana
            → Mantiene mañana intacta
        
        ASR (COMPLETAR):
            → Marca COMPLETADOS
            → Identifica PENDIENTES para mañana
        
        MAGHRIB (INTEGRACIÓN):
            → CIERRA día actual
            → CREA día siguiente
        
        ISHA (SOLTAR):
            → Marca día como CERRADO
        """
        
        from services.propositos import obtener_proposito_estado_cero
        from models.schemas import MomentoLiturgico
        
        momento_enum = MomentoLiturgico(momento)
        proposito = obtener_proposito_estado_cero(momento_enum)
        
        print(f"🔄 Actualizando Espejo ({momento.upper()}): {proposito.proposito}")
        
        bloques_actualizados = plan_actual.bloques_sugeridos.copy()
        
        # Actualizar según momento
        if momento == "fajr":
            # FAJR: Refinar plan completo
            bloques_actualizados = await self._refinar_plan_completo(
                bloques_actualizados,
                direccion_emergente,
                respuestas_sacra
            )
        
        elif momento == "dhuhr":
            # DHUHR: Ajustar solo tarde (después de 14:00)
            bloques_actualizados = await self._ajustar_bloques_tarde(
                bloques_actualizados,
                direccion_emergente
            )
        
        elif momento == "asr":
            # ASR: Marcar completados y pendientes
            bloques_actualizados = self._marcar_completados_pendientes(
                bloques_actualizados
            )
        
        elif momento == "maghrib":
            # MAGHRIB: Cerrar día, preparar mañana (se hace en ritual_maghrib)
            pass
        
        elif momento == "isha":
            # ISHA: Marcar día cerrado
            pass
        
        # Actualizar plan
        plan_actualizado = JornadaAlBordeCaos(
            fecha=plan_actual.fecha,
            accion_principal=plan_actual.accion_principal,
            bloques_sugeridos=bloques_actualizados,
            puntos_decision=plan_actual.puntos_decision,
            espacio_emergencia=plan_actual.espacio_emergencia,
            no_negociables=plan_actual.no_negociables,
            flexible=plan_actual.flexible,
            ultima_actualizacion=datetime.now()
        )
        
        self.plan_actual = plan_actualizado
        
        return plan_actualizado
    
    async def _refinar_plan_completo(
        self,
        bloques: List[BloqueTiempo],
        direccion: str,
        respuestas: List[Any]
    ) -> List[BloqueTiempo]:
        """FAJR: Refina todo el día basándose en dirección emergente"""
        
        # Separar anclas (intocables) de bloques flexibles
        anclas = [b for b in bloques if not b.flexible]
        flexibles = [b for b in bloques if b.flexible]
        
        # Ajustar bloques flexibles según dirección
        # Por ahora mantiene los existentes
        # TODO: Usar Claude para refinar según dirección
        
        return anclas + flexibles
    
    async def _ajustar_bloques_tarde(
        self,
        bloques: List[BloqueTiempo],
        direccion: str
    ) -> List[BloqueTiempo]:
        """DHUHR: Ajusta solo bloques de tarde (>= 14:00)"""
        
        bloques_mañana = [b for b in bloques if b.inicio_aprox < "14:00"]
        bloques_tarde = [b for b in bloques if b.inicio_aprox >= "14:00"]
        
        # Ajustar tarde según dirección
        # Por ahora mantiene existentes
        
        return bloques_mañana + bloques_tarde
    
    def _marcar_completados_pendientes(
        self,
        bloques: List[BloqueTiempo]
    ) -> List[BloqueTiempo]:
        """ASR: Marca qué se completó y qué queda pendiente"""
        
        # Por ahora retorna sin cambios
        # TODO: Marcar estado de cada bloque
        
        return bloques
    
    async def generar_plan_dia_coordinado(
        self,
        intencion_usuario: str,
        estructura_dia: EstructuraDia,
        contexto: ContextoCompleto
    ) -> JornadaAlBordeCaos:
        """
        CORRESPONDENCIA ENTRELAZADOR ↔ ORQUESTADOR
        
        Genera plan pragmático combinando:
        1. Estructura base del Entrelazador (anclas, no-negociables, rutinas)
        2. Intención del usuario (autoridad sacral)
        3. Tiempos litúrgicos precisos
        4. Contexto actual
        
        Output: Guion completo y flexible del día
        """
        
        bloques_finales = []
        
        # 1. ANCLAS (rezo + Estado Cero) - INTOCABLES
        for ancla in estructura_dia.anclas:
            bloques_finales.append(BloqueTiempo(
                id=str(uuid.uuid4()),
                inicio_aprox=ancla.inicio.strftime("%H:%M"),
                duracion=f"{ancla.duracion}min",
                actividad=f"{'🕌' if ancla.tipo == 'rezo' else '🔮' if ancla.tipo == 'estado_cero' else '🌆'} {ancla.momento.upper()} - {ancla.tipo.replace('_', ' ').title()}",
                rol=ancla.proposito or "Ritual sagrado",
                energia_optima=3,
                flexible=False,  # ⚓ ANCLADO - No se mueve
                opciones_alternativas=[]
            ))
        
        # 2. RUTINAS del día (del Entrelazador)
        for rutina in estructura_dia.rutinas_dia:
            bloques_finales.append(BloqueTiempo(
                id=str(uuid.uuid4()),
                inicio_aprox=rutina["hora_preferida"],
                duracion=f"{rutina['duracion_minutos']}min",
                actividad=f"🏃 {rutina['nombre']}",
                rol="Rutina deportiva",
                energia_optima=rutina["intensidad"],
                flexible=True,  # 🌊 Puede moverse ±30min
                opciones_alternativas=[
                    f"Mover a {self._calcular_hora_alternativa(rutina['hora_preferida'], -30)}",
                    f"Mover a {self._calcular_hora_alternativa(rutina['hora_preferida'], 30)}",
                    "Reducir a 30min si falta tiempo"
                ]
            ))
        
        # 3. NO-NEGOCIABLES (calcular mejor hora dentro de ventana)
        for nn in estructura_dia.no_negociables_dia:
            mejor_hora = self._calcular_mejor_hora_no_negociable(
                nn,
                bloques_finales
            )
            
            bloques_finales.append(BloqueTiempo(
                id=str(uuid.uuid4()),
                inicio_aprox=mejor_hora,
                duracion=f"{nn.duracion_min}min",
                actividad=f"⚓ {nn.nombre}",
                rol="No-negociable",
                energia_optima=2,
                flexible=False,  # ⚓ ANCLADO
                opciones_alternativas=[]
            ))
        
        # 4. BLOQUES EMERGENTES (basados en intención + contexto)
        bloques_emergentes = await self._generar_bloques_emergentes_coordinados(
            intencion=intencion_usuario,
            estructura=estructura_dia,
            contexto=contexto,
            bloques_ya_asignados=bloques_finales
        )
        
        bloques_finales.extend(bloques_emergentes)
        
        # 5. Ordenar por hora
        bloques_ordenados = sorted(bloques_finales, key=lambda b: b.inicio_aprox)
        
        # 6. Validar que mantenemos >= 40% libre
        tiempo_total_asignado = sum([self._parsear_duracion(b.duracion) for b in bloques_ordenados])
        porcentaje_asignado = (tiempo_total_asignado / (24 * 60)) * 100
        porcentaje_libre = 100 - porcentaje_asignado
        
        if porcentaje_libre < 40:
            print(f"⚠️ Espacio libre bajo ({porcentaje_libre:.1f}%), ajustando...")
            bloques_ordenados = self._reducir_bloques_emergentes(bloques_ordenados, objetivo_libre=40)
        
        # 7. Generar puntos de decisión
        puntos_decision = self._generar_puntos_decision_coordinados(
            bloques_ordenados,
            estructura_dia.tiempos_liturgicos
        )
        
        # 8. Crear Jornada
        return JornadaAlBordeCaos(
            fecha=estructura_dia.fecha,
            accion_principal=AccionConcreta(
                descripcion=intencion_usuario,
                resultado_observable="Día vivido según intención y estructura",
                duracion_estimada="jornada completa",
                energia_requerida=3
            ),
            bloques_sugeridos=bloques_ordenados,
            puntos_decision=puntos_decision,
            espacio_emergencia=int(estructura_dia.espacio_libre_minutos),
            no_negociables=[],  # Ya están en bloques
            flexible=True,
            ultima_actualizacion=datetime.now()
        )
    
    def _calcular_hora_alternativa(self, hora_str: str, delta_min: int) -> str:
        """Calcula hora alternativa ±delta minutos"""
        from datetime import datetime, timedelta
        hora = datetime.strptime(hora_str, "%H:%M")
        nueva_hora = hora + timedelta(minutes=delta_min)
        return nueva_hora.strftime("%H:%M")
    
    def _calcular_mejor_hora_no_negociable(
        self,
        no_negociable: NoNegociable,
        bloques_existentes: List[BloqueTiempo]
    ) -> str:
        """
        Calcula la mejor hora para un no-negociable
        considerando bloques ya asignados
        """
        # Por ahora retorna hora por defecto
        # TODO: Implementar lógica de detección de ventanas libres
        defaults = {
            "Movimiento": "07:00",
            "Comida nutritiva": "13:00",
            "Lectura profunda": "21:30"
        }
        return defaults.get(no_negociable.nombre, "12:00")
    
    async def _generar_bloques_emergentes_coordinados(
        self,
        intencion: str,
        estructura: EstructuraDia,
        contexto: ContextoCompleto,
        bloques_ya_asignados: List[BloqueTiempo]
    ) -> List[BloqueTiempo]:
        """
        Genera bloques emergentes basados en:
        - Intención del usuario
        - Proyectos sugeridos del Entrelazador
        - Aprendizaje sugerido del Entrelazador
        - Espacio libre disponible
        """
        
        bloques_emergentes = []
        
        # Calcular espacio disponible
        tiempo_ya_asignado = sum([self._parsear_duracion(b.duracion) for b in bloques_ya_asignados])
        espacio_disponible = estructura.espacio_libre_minutos
        
        # Máximo 60% del día asignado = 40% libre
        max_tiempo_emergente = max(0, int((24 * 60 * 0.6) - tiempo_ya_asignado))
        
        # Generar bloques con Claude (optimizado)
        prompt = f"""Intención: {intencion}
Espacio: {max_tiempo_emergente}min
Proyectos: {[p.get('nombre', '') for p in estructura.proyectos_sugeridos[:3]]}
Aprendizaje: {[a.get('nombre', '') for a in estructura.aprendizaje_sugerido[:2]]}

Genera 2-3 bloques pragmáticos (total <= {max_tiempo_emergente}min).
JSON: [{{"inicio":"10:00","duracion":"2h","actividad":"..."}}]"""
        
        messages = [{"role": "user", "content": prompt}]
        
        try:
            # Usar Haiku (más barato para esta tarea)
            resultado = await self.claude.generate_json_haiku("Generas bloques de trabajo.", messages)
            
            if isinstance(resultado, list):
                for i, bloque_data in enumerate(resultado[:3]):  # Máximo 3
                    bloques_emergentes.append(BloqueTiempo(
                        id=str(uuid.uuid4()),
                        inicio_aprox=bloque_data.get("inicio", "10:00"),
                        duracion=bloque_data.get("duracion", "1h"),
                        actividad=f"🌊 {bloque_data.get('actividad', 'Trabajo emergente')}",
                        rol="Emergente",
                        energia_optima=bloque_data.get("energia", 3),
                        flexible=True,
                        opciones_alternativas=[
                            "Mover si es necesario",
                            "Acortar si baja energía",
                            "Expandir si hay momentum"
                        ]
                    ))
        except Exception as e:
            print(f"⚠️ Error generando bloques emergentes: {e}")
        
        return bloques_emergentes
    
    def _generar_puntos_decision_coordinados(
        self,
        bloques: List[BloqueTiempo],
        tiempos: Any
    ) -> List[PuntoDecision]:
        """Genera puntos de decisión considerando estructura"""
        
        # Puntos de decisión estratégicos
        return [
            PuntoDecision(
                momento="Después de trabajo profundo",
                pregunta="¿Cómo está tu energía?",
                criterio="Si energía > 3, continuar; si < 3, descansar",
                opciones=["Continuar", "Break 15min", "Cambiar de actividad"]
            ),
            PuntoDecision(
                momento="Antes de tarde",
                pregunta="¿Qué pide tu cuerpo?",
                criterio="Consulta sensación visceral",
                opciones=["Trabajo profundo", "Aprendizaje", "Movimiento", "Emergente"]
            )
        ]
    
    def _reducir_bloques_emergentes(
        self,
        bloques: List[BloqueTiempo],
        objetivo_libre: int = 40
    ) -> List[BloqueTiempo]:
        """
        Reduce bloques emergentes si sobrepasamos 60% asignado.
        Mantiene anclas y no-negociables intactos.
        """
        
        # Separar bloques
        anclados = [b for b in bloques if not b.flexible]
        emergentes = [b for b in bloques if b.flexible]
        
        # Calcular cuánto reducir
        tiempo_anclado = sum([self._parsear_duracion(b.duracion) for b in anclados])
        max_tiempo_emergente = int((24 * 60 * 0.6) - tiempo_anclado)
        
        tiempo_emergente_actual = sum([self._parsear_duracion(b.duracion) for b in emergentes])
        
        if tiempo_emergente_actual <= max_tiempo_emergente:
            return bloques
        
        # Reducir bloques emergentes proporcionalmente
        factor = max_tiempo_emergente / tiempo_emergente_actual
        
        emergentes_reducidos = []
        for bloque in emergentes:
            duracion_min = self._parsear_duracion(bloque.duracion)
            nueva_duracion = int(duracion_min * factor)
            
            bloque.duracion = f"{nueva_duracion}min"
            emergentes_reducidos.append(bloque)
        
        return anclados + emergentes_reducidos
    
    def _parsear_duracion(self, duracion_str: str) -> int:
        """Parsea '2h', '90min', '1.5h' a minutos"""
        duracion_str = duracion_str.lower().strip()
        
        if 'h' in duracion_str:
            horas = float(duracion_str.replace('h', '').replace('min', '').strip())
            return int(horas * 60)
        elif 'min' in duracion_str:
            return int(duracion_str.replace('min', '').strip())
        else:
            return 60  # Default
        
    async def recibir_orientacion(
        self,
        accion: AccionConcreta,
        contexto: ContextoCompleto
    ) -> JornadaAlBordeCaos:
        """
        Recibe orientación del Estado Cero y genera plan emergente
        """
        
        # Generar plan
        plan = await self.generar_plan_emergente(accion, contexto)
        
        # Establecer no-negociables
        no_negociables = await self.establecer_no_negociables(contexto)
        plan.no_negociables = no_negociables
        
        # Guardar plan actual
        self.plan_actual = plan
        
        return plan
    
    async def generar_plan_emergente(
        self,
        accion: AccionConcreta,
        contexto: ContextoCompleto
    ) -> JornadaAlBordeCaos:
        """
        Genera plan flexible que honra la acción del Estado Cero
        40% de espacio sin asignar para lo emergente
        """
        
        proximo = self.calculador_tiempos.proximo_estado_cero()
        
        # PROMPT OPTIMIZADO: 300 tokens → 150 tokens
        prompt = f"""Acción: {accion.descripcion}
E:{accion.energia_requerida}/5, {accion.duracion_estimada}

Contexto: {contexto.temporal.momento_liturgico.value}, E actual:{contexto.biologico.energia_actual}/5
Próximo: {proximo.momento.value} en {proximo.countdown}

Plan emergente (40% libre, flexible):
JSON con bloques_sugeridos y puntos_decision

Ejemplo: [{{"id":"b1","inicio_aprox":"10:00","duracion":"2h","actividad":"...","energia_optima":4,"flexible":true}}]"""
        
        messages = [{"role": "user", "content": prompt}]
        resultado = await self.claude.generate_json(
            system="Orquestas jornadas al borde del caos.",
            messages=messages
        )
        
        # Construir bloques - manejar estructura de respuesta
        bloques = []
        puntos = []
        
        if isinstance(resultado, list):
            # Si resultado es una lista, crear bloques básicos
            for i, item in enumerate(resultado):
                if isinstance(item, dict) and "actividad" in item:
                    bloques.append(BloqueTiempo(
                        id=f"bloque_{i}",
                        inicio_aprox=item.get("inicio_aprox", "09:00"),
                        duracion=item.get("duracion", "90 min"),
                        actividad=item["actividad"],
                        rol=item.get("rol", "usuario")
                    ))
        elif isinstance(resultado, dict):
            # Si es diccionario, extraer bloques y puntos
            bloques_data = resultado.get("bloques_sugeridos", [])
            puntos_data = resultado.get("puntos_decision", [])
            
            for i, b in enumerate(bloques_data):
                if isinstance(b, dict):
                    bloques.append(BloqueTiempo(
                        id=b.get("id", f"bloque_{i}"),
                        inicio_aprox=b.get("inicio_aprox", "09:00"),
                        duracion=b.get("duracion", "90 min"),
                        actividad=b.get("actividad", "Actividad"),
                        rol=b.get("rol", "usuario")
                    ))
            
            for i, p in enumerate(puntos_data):
                if isinstance(p, dict):
                    puntos.append(PuntoDecision(
                        momento=p.get("momento", "12:00"),
                        pregunta=p.get("pregunta", "¿Qué hacer?"),
                        criterio=p.get("criterio", "Intuición"),
                        opciones=p.get("opciones", ["Opción A", "Opción B"])
                    ))
        
        return JornadaAlBordeCaos(
            fecha=date.today(),
            accion_principal=accion,
            bloques_sugeridos=bloques,
            puntos_decision=puntos,
            espacio_emergencia=40,
            no_negociables=[],  # Se llenan después
            flexible=True,
            ultima_actualizacion=datetime.now()
        )
    
    async def establecer_no_negociables(
        self,
        contexto: ContextoCompleto
    ) -> List[NoNegociable]:
        """
        Establece los no-negociables del día según contexto
        """
        
        no_negociables = []
        
        # BIOLÓGICOS
        no_negociables.extend([
            NoNegociable(
                tipo=TipoNoNegociable.BIOLOGICO,
                nombre="Luz solar matutina",
                ventana="despertar + 60min",
                duracion_min="15min",
                prioridad="CRÍTICA",
                razon="Sincronización circadiana fundamental"
            ),
            NoNegociable(
                tipo=TipoNoNegociable.BIOLOGICO,
                nombre="Primera comida",
                ventana="despertar + 120min",
                duracion_min="20min",
                prioridad="ALTA",
                razon="Iniciar metabolismo, 30-40g proteína"
            ),
            NoNegociable(
                tipo=TipoNoNegociable.BIOLOGICO,
                nombre="Movimiento diario",
                ventana="flexible",
                duracion_min="20min",
                prioridad="ALTA",
                razon="Mantener salud metabólica y mental"
            )
        ])
        
        # ESPIRITUALES
        proximo = self.calculador_tiempos.proximo_estado_cero()
        no_negociables.append(
            NoNegociable(
                tipo=TipoNoNegociable.ESPIRITUAL,
                nombre=f"Próximo Estado Cero ({proximo.momento.value})",
                ventana=proximo.hora.strftime("%H:%M"),
                duracion_min="15-30min",
                prioridad="CRÍTICA",
                razon="Estructura sagrada del día"
            )
        )
        
        # FINANCIEROS (si runway crítico)
        if contexto.financiero.runway_meses < 3:
            no_negociables.append(
                NoNegociable(
                    tipo=TipoNoNegociable.FINANCIERO,
                    nombre="Avance en generación de ingresos",
                    ventana="bloque_principal",
                    duracion_min="120min",
                    prioridad="CRÍTICA",
                    razon=f"Runway crítico: {contexto.financiero.runway_meses} meses"
                )
            )
        
        return no_negociables
    
    async def chat_interactivo(
        self,
        mensaje: str,
        contexto_actual: Dict
    ) -> str:
        """
        Chat con el Orquestador para ajustes manuales
        """
        
        # Serializar contexto de forma segura
        contexto_serializable = {}
        for key, value in contexto_actual.items():
            if hasattr(value, 'isoformat'):  # datetime objects
                contexto_serializable[key] = value.isoformat()
            elif hasattr(value, '__dict__'):  # custom objects
                contexto_serializable[key] = str(value)
            else:
                contexto_serializable[key] = value

        prompt = f"""Usuario dice: "{mensaje}"

ESTADO ACTUAL:
{json.dumps(contexto_serializable, indent=2)}

Responde como Orquestador:
1. Entiende la necesidad del usuario
2. Sugiere ajustes al plan
3. Mantiene la flexibilidad del sistema
4. Honra la autoridad sacral

Respuesta:"""

        messages = [{"role": "user", "content": prompt}]
        return await self.claude.generate("", messages)
    
    def obtener_plan_actual(self) -> Optional[JornadaAlBordeCaos]:
        """Obtiene el plan actual de la jornada"""
        return self.plan_actual
    
    async def actualizar_plan(
        self,
        ajustes: Dict,
        contexto_actual: Dict
    ) -> JornadaAlBordeCaos:
        """
        Actualiza el plan basado en ajustes del usuario
        """
        
        if not self.plan_actual:
            raise ValueError("No hay plan actual para actualizar")
        
        # Aplicar ajustes
        if "bloque_modificado" in ajustes:
            # Modificar bloque específico
            bloque_id = ajustes["bloque_modificado"]["id"]
            for bloque in self.plan_actual.bloques_sugeridos:
                if bloque.id == bloque_id:
                    bloque.actividad = ajustes["bloque_modificado"]["nueva_actividad"]
                    bloque.duracion = ajustes["bloque_modificado"].get("duracion", bloque.duracion)
                    break
        
        if "nuevo_bloque" in ajustes:
            # Agregar nuevo bloque
            nuevo_bloque = BloqueTiempo(**ajustes["nuevo_bloque"])
            self.plan_actual.bloques_sugeridos.append(nuevo_bloque)
        
        # Actualizar timestamp
        self.plan_actual.ultima_actualizacion = datetime.now()
        
        return self.plan_actual
