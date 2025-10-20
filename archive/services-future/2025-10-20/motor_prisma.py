"""
🔮 Motor del Prisma: Alimenta a los Agentes con tu Configuración
=================================================================

Este motor traduce tu prisma personal en instrucciones operativas
para cada agente, asegurando que:

1. Respeten tu autoridad interna
2. Eviten tus puntos ciegos
3. Aprovechen tus fortalezas
4. Operen según tu estrategia vital

Principios:
- waḥdat al-wujūd (unidad del ser): Todo emerge de tu centro
- al-khayāl al-faʿʿāl (imaginación creadora): Materialización consciente
"""

from typing import Dict, List, Optional
from models.prisma_personal import (
    PrismaPersonal, TipoHumanDesign, AutoridadInterna,
    TipoMBTI, TipoEneagrama, DimensionVida
)
import json
import os


class MotorPrisma:
    """
    Traduce el prisma personal en configuración operativa para los agentes.
    
    Cada agente recibe instrucciones adaptadas a tu esencia única.
    """
    
    def __init__(self, prisma: PrismaPersonal):
        self.prisma = prisma
    
    # ═══════════════════════════════════════════════════════════════
    # ESTADO CERO: Preguntas Adaptadas
    # ═══════════════════════════════════════════════════════════════
    
    def configurar_estado_cero(self) -> Dict:
        """
        Configura el agente Estado Cero según tu prisma.
        
        Adapta:
        - Tipo de preguntas (sacral vs emocional vs mental)
        - Número de preguntas (ENTP-5 prefiere 3, no 6)
        - Estilo de redacción (directa vs exploratoria)
        - Categorías priorizadas
        """
        
        config = {
            "tipo_preguntas": self._determinar_tipo_preguntas(),
            "numero_preguntas": self._determinar_numero_preguntas(),
            "estilo_redaccion": self._determinar_estilo_preguntas(),
            "categorias_priorizadas": self._priorizar_categorias(),
            "evitar_sesgos": self._identificar_sesgos(),
            "prompt_adicional": self._generar_prompt_estado_cero()
        }
        
        return config
    
    def _determinar_tipo_preguntas(self) -> str:
        """Determina el tipo de preguntas según autoridad"""
        
        autoridad = self.prisma.diseño_humano.autoridad
        
        if autoridad == AutoridadInterna.SACRAL:
            return "binarias_viscerales"  # Expansión/Contracción inmediata
        elif autoridad == AutoridadInterna.EMOCIONAL:
            return "con_tiempo"  # Necesita ola emocional completa
        elif autoridad == AutoridadInterna.ESPLENICA:
            return "intuitivas_momento"  # Intuición instantánea
        elif autoridad == AutoridadInterna.MENTAL:
            return "exploratorias_entorno"  # NO para decidir
        else:
            return "binarias_viscerales"  # Default
    
    def _determinar_numero_preguntas(self) -> int:
        """
        Determina número DINÁMICO de preguntas según coherencia alcanzada.
        
        NO es fijo. Es emergente.
        
        Lógica:
        - Inicio (días 1-7): Exploración amplia (10-20 preguntas)
        - Integración (días 8-30): Pattern recognition (5-10 preguntas)
        - Refinamiento (días 31-90): Ajuste sutil (3-5 preguntas)
        - Maestría (90+): Mínimas necesarias (1-3 preguntas)
        
        El número disminuye según claridad alcanzada.
        """
        
        # Obtener días de uso del sistema
        dias_uso = self.prisma.metadatos_operativos.dias_datos
        
        # Obtener ratio de coherencia (expansión vs contracción)
        ratio_coherencia = self.prisma.metadatos_operativos.ratio_expansion_contraccion
        
        # FASE 1: EXPLORACIÓN (días 1-7)
        # Auditoría profunda de todas las dimensiones
        if dias_uso < 7:
            base = 15  # Exploración amplia inicial
            
        # FASE 2: PATTERN RECOGNITION (días 8-30)
        # El organismo identifica patrones, reduce redundancia
        elif dias_uso < 30:
            base = 8  # Ya identificó algunos patrones
            
        # FASE 3: REFINAMIENTO (días 31-90)
        # Ajustes sutiles, energía dirigida
        elif dias_uso < 90:
            base = 5  # Claridad emergiendo
            
        # FASE 4: MAESTRÍA (90+ días)
        # Mínimas preguntas necesarias, máxima claridad
        else:
            base = 3  # Solo lo esencial
        
        # AJUSTE POR COHERENCIA ACTUAL
        # Si ratio es alto (>0.7), usuario está alineado → menos preguntas
        # Si ratio es bajo (<0.5), hay desalineación → más preguntas
        
        if ratio_coherencia > 0.7:
            ajuste = -2  # Alta coherencia → reducir
        elif ratio_coherencia < 0.5:
            ajuste = +3  # Baja coherencia → aumentar
        else:
            ajuste = 0
        
        numero_final = max(1, base + ajuste)  # Mínimo 1
        
        return numero_final
    
    def _determinar_estilo_preguntas(self) -> str:
        """Determina estilo de redacción según MBTI"""
        
        mbti = self.prisma.perfil_psicologico.mbti
        
        if mbti == TipoMBTI.ENTP:
            return "exploratoria_conceptual"  # Permite conexiones
        elif mbti in [TipoMBTI.INTJ, TipoMBTI.ENTJ]:
            return "directa_estrategica"  # Sin rodeos
        elif mbti in [TipoMBTI.INFJ, TipoMBTI.ENFJ]:
            return "profunda_significado"  # Con propósito
        else:
            return "clara_simple"  # Default
    
    def _priorizar_categorias(self) -> List[str]:
        """Prioriza categorías según manifestaciones activas"""
        
        dimensiones = [m.dimension for m in self.prisma.manifestaciones]
        
        # Contar frecuencia
        contador = {}
        for dim in dimensiones:
            contador[dim.value] = contador.get(dim.value, 0) + 1
        
        # Ordenar por frecuencia
        priorizadas = sorted(contador.items(), key=lambda x: x[1], reverse=True)
        
        return [dim for dim, _ in priorizadas]
    
    def _identificar_sesgos(self) -> List[str]:
        """Identifica sesgos a evitar según perfil"""
        
        sesgos = []
        
        # Según Eneagrama
        enea = self.prisma.perfil_psicologico.eneagrama_base
        
        if enea == TipoEneagrama.TIPO_5:
            sesgos.extend([
                "sobre_analisis_paralizante",
                "postergar_accion_por_mas_info",
                "desconexion_necesidades_corporales",
                "retiro_en_vez_de_accion"
            ])
        elif enea == TipoEneagrama.TIPO_1:
            sesgos.extend([
                "perfeccionismo_paralizante",
                "critica_excesiva",
                "rigidez"
            ])
        elif enea == TipoEneagrama.TIPO_7:
            sesgos.extend([
                "dispersion",
                "evitar_profundidad",
                "sobre_optimismo"
            ])
        
        # Según MBTI
        mbti = self.prisma.perfil_psicologico.mbti
        
        if "P" in mbti.value:  # Perceptivo
            sesgos.append("dificultad_cerrar_opciones")
        
        if "T" in mbti.value:  # Pensador
            sesgos.append("desconexion_emocional")
        
        return sesgos
    
    def _generar_prompt_estado_cero(self) -> str:
        """Genera prompt adicional específico para el agente Estado Cero"""
        
        autoridad = self.prisma.diseño_humano.autoridad.value
        estrategia = self.prisma.diseño_humano.estrategia.value
        enea = self.prisma.perfil_psicologico.eneagrama_base.value
        punto_ciego = self.prisma.perfil_psicologico.punto_ciego
        num_preguntas = self._determinar_numero_preguntas()
        dias_uso = self.prisma.metadatos_operativos.dias_datos
        
        # Determinar alcance temporal según fase
        if dias_uso < 7:
            alcance = "AUDITORÍA COMPLETA: Presente + visión medio/largo plazo"
        elif dias_uso < 30:
            alcance = "PATTERN RECOGNITION: Identificar patrones recurrentes"
        elif dias_uso < 90:
            alcance = "REFINAMIENTO: Ajustes sutiles y deseos profundos"
        else:
            alcance = "MAESTRÍA: Solo lo que no ves o no sabes gestionar"
        
        prompt = f"""
CONFIGURACIÓN DEL USUARIO:
- Autoridad: {autoridad.upper()} → Las preguntas deben evocar RESPUESTA VISCERAL, no análisis mental
- Estrategia: {estrategia.replace('_', ' ').title()} → Esperar que algo resuene, no forzar
- Eneagrama {enea} → Punto ciego: {punto_ciego}
- Días de uso: {dias_uso} → Fase: {alcance}

NÚMERO DINÁMICO DE PREGUNTAS: {num_preguntas}
Este número NO es fijo. Se ajusta según:
- Coherencia alcanzada (ratio expansión/contracción)
- Claridad interna observada
- Patrones ya identificados
- Desalineaciones detectadas

ALCANCE TEMPORAL:
Las preguntas NO tienen que ser solo sobre el momento presente.
Pueden ser:
- Momento presente: "¿Tu cuerpo se expande al dedicar hoy a...?"
- Medio plazo (1-3 meses): "¿Resuena materializar X en este trimestre?"
- Largo plazo (1+ años): "¿La visión de Y sigue viva en ti?"
- Pattern recognition: "¿Notas que siempre postpones Z?"
- Deseos profundos: "¿Qué anhela tu ser que no estás escuchando?"

FUNCIÓN DEL ESPEJO:
Reflejar lo que NO estás viendo en tu comportamiento, o
lo que SÍ ves pero no sabes cómo gestionar.

INSTRUCCIONES ESPECÍFICAS:
1. NO preguntar "¿Deberías...?" → Pregunta "¿Tu cuerpo se expande al...?"
2. NO redundancia (si ya se identificó un patrón, no preguntar de nuevo)
3. Priorizar AUDITORÍA de dimensiones: {', '.join(self._priorizar_categorias()[:3])}
4. EVITAR sesgos conocidos: {', '.join(self._identificar_sesgos()[:2])}
5. Sensibilidad a escucha interna sutil y energética
6. Expresión de deseos verdaderamente profundos

ESTILO: {self._determinar_estilo_preguntas()}

waḥdat al-wujūd: Las preguntas emergen de la unidad del ser del usuario.
al-khayāl al-faʿʿāl: Evocan imaginación creadora y guía de autoridad interna.

La dirección emerge con CLARIDAD tras la auditoría de prioridades en cada dimensión.
"""
        
        return prompt.strip()
    
    # ═══════════════════════════════════════════════════════════════
    # ENTRELAZADOR: Estructura Personalizada
    # ═══════════════════════════════════════════════════════════════
    
    def configurar_entrelazador(self) -> Dict:
        """
        Configura el Entrelazador según tu prisma.
        
        Adapta:
        - Duración de bloques profundos
        - Horarios óptimos
        - Frecuencia de cambios de contexto
        - Balance profundidad/amplitud
        - ESPACIO LIBRE DINÁMICO
        """
        
        config = {
            "duracion_bloque_profundo": self._determinar_duracion_flujo(),
            "horarios_optimos": self._determinar_horarios_optimos(),
            "estilo_trabajo": self._determinar_estilo_trabajo(),
            "balance_profundidad": self._determinar_balance(),
            "espacio_libre_dinamico": self._calcular_espacio_libre_dinamico(),
            "protecciones": self._generar_protecciones(),
            "prompt_adicional": self._generar_prompt_entrelazador()
        }
        
        return config
    
    def _determinar_duracion_flujo(self) -> int:
        """Determina duración óptima de bloques de flujo"""
        
        return self.prisma.metodo_aprendizaje.duracion_optima_sesion
    
    def _determinar_horarios_optimos(self) -> List[str]:
        """Determina horarios óptimos para trabajo profundo"""
        
        # Priorizar metadatos reales si existen
        if self.prisma.metadatos_operativos.pico_energia_real:
            return [self.prisma.metadatos_operativos.pico_energia_real]
        
        # Sino, usar declarado
        return [self.prisma.metodo_aprendizaje.mejor_momento_aprendizaje]
    
    def _determinar_estilo_trabajo(self) -> str:
        """Determina estilo de trabajo según personalidad"""
        
        mbti = self.prisma.perfil_psicologico.mbti
        enea = self.prisma.perfil_psicologico.eneagrama_base
        
        if mbti in [TipoMBTI.ENTP, TipoMBTI.ENFP]:
            if enea.value == "5":
                return "bloques_profundos_con_exploracion"  # Profundidad pero flexible
            return "exploracion_libre_con_estructura"
        elif mbti in [TipoMBTI.INTJ, TipoMBTI.ISTJ]:
            return "bloques_largos_lineales"  # Profundidad sostenida
        else:
            return "pomodoro_adaptativo"  # Default
    
    def _determinar_balance(self) -> float:
        """Balance profundidad vs amplitud (0-1, donde 1=máxima profundidad)"""
        
        return self.prisma.metodo_aprendizaje.profundidad_vs_amplitud / 10.0
    
    def _generar_protecciones(self) -> List[str]:
        """Protecciones necesarias según perfil"""
        
        protecciones = []
        
        if self.prisma.metodo_aprendizaje.requiere_silencio:
            protecciones.append("silencio_absoluto_bloques_profundos")
        
        # ENTP-5: Necesita protección contra sobre-exploración
        if self.prisma.perfil_psicologico.mbti == TipoMBTI.ENTP:
            if self.prisma.perfil_psicologico.eneagrama_base.value == "5":
                protecciones.extend([
                    "limite_exploracion_conceptual",  # Evitar rabbit holes infinitos
                    "checkpoint_implementacion"  # Forzar pasar a acción
                ])
        
        return protecciones
    
    def _calcular_espacio_libre_dinamico(self) -> float:
        """
        Calcula % de espacio libre DINÁMICO según inteligencia sintética.
        
        NO es fijo en 40%. Es adaptativo.
        
        Factores:
        - Tipo HD (Generador necesita más espacio)
        - Ratio expansión/contracción (baja coherencia → más espacio)
        - Fase de manifestaciones (cerca de completar → menos espacio)
        - Nivel de energía observado
        - Patrones de sobre-compromiso
        """
        
        # BASE según tipo HD
        tipo = self.prisma.diseño_humano.tipo
        
        if tipo == TipoHumanDesign.GENERADOR:
            base = 0.45  # Necesita RESPONDER, no forzar
        elif tipo == TipoHumanDesign.PROYECTOR:
            base = 0.50  # Necesita aún MÁS espacio
        elif tipo == TipoHumanDesign.MANIFESTOR:
            base = 0.35  # Puede sostener más estructura
        elif tipo == TipoHumanDesign.REFLECTOR:
            base = 0.55  # Máximo espacio (ciclo lunar)
        else:
            base = 0.40  # Default
        
        # AJUSTE por coherencia
        ratio = self.prisma.metadatos_operativos.ratio_expansion_contraccion
        
        if ratio < 0.5:
            ajuste_coherencia = +0.10  # Baja coherencia → MÁS espacio
        elif ratio > 0.7:
            ajuste_coherencia = -0.05  # Alta coherencia → puede usar más
        else:
            ajuste_coherencia = 0
        
        # AJUSTE por progreso manifestaciones
        if self.prisma.manifestaciones:
            progreso_promedio = sum(m.progreso_estimado for m in self.prisma.manifestaciones) / len(self.prisma.manifestaciones)
            
            if progreso_promedio > 70:
                ajuste_manifestacion = -0.05  # Cerca de completar → sprint final
            else:
                ajuste_manifestacion = 0
        else:
            ajuste_manifestacion = 0
        
        # AJUSTE por patrón de días de expansión
        if self.prisma.metadatos_operativos.dias_alta_expansion:
            # Si hay días específicos de alta expansión, ajustar según día
            # (esto se hace en tiempo de ejecución, aquí solo el promedio)
            ajuste_patron = 0
        else:
            ajuste_patron = 0
        
        espacio_final = base + ajuste_coherencia + ajuste_manifestacion + ajuste_patron
        
        # Límites: 25% mínimo, 60% máximo
        espacio_final = max(0.25, min(0.60, espacio_final))
        
        return espacio_final
    
    def _generar_prompt_entrelazador(self) -> str:
        """Genera prompt para el Entrelazador"""
        
        tipo_hd = self.prisma.diseño_humano.tipo.value
        estilo = self._determinar_estilo_trabajo()
        balance = self._determinar_balance()
        espacio_libre = self._calcular_espacio_libre_dinamico()
        
        prompt = f"""
CONFIGURACIÓN DEL USUARIO:
- Tipo: {tipo_hd.title()} → {self.prisma.diseño_humano.patron_energia}
- Estilo trabajo: {estilo}
- Balance profundidad/amplitud: {balance:.1f} (0=amplitud, 1=profundidad)
- Duración flujo óptimo: {self._determinar_duracion_flujo()} min
- Horarios pico: {', '.join(self._determinar_horarios_optimos())}

ESPACIO LIBRE DINÁMICO: {int(espacio_libre*100)}%
Este porcentaje NO es fijo. Se ajusta según:
- Tipo HD y patrón energético
- Coherencia alcanzada (ratio expansión/contracción)
- Progreso de manifestaciones
- Días de alta/baja expansión observados
- Patrones de sobre-compromiso detectados

El organismo usa inteligencia sintética para calcular el espacio óptimo.

INSTRUCCIONES ESPECÍFICAS:
1. Bloques profundos en horarios pico SIEMPRE
2. Respetar duración óptima de flujo ({self._determinar_duracion_flujo()}min)
3. Mantener {int(espacio_libre*100)}% espacio libre (calculado dinámicamente)
4. Protecciones activas: {', '.join(self._generar_protecciones()[:2])}
5. Trabajo de integración 5→8: PRIORIZAR ACCIÓN sobre más análisis

waḥdat al-wujūd: La estructura emerge del ritmo natural del usuario.
al-khayāl al-faʿʿāl: Materialización requiere ACCIÓN, no solo comprensión.

El borde del caos se ajusta según la inteligencia sintética del organismo.
"""
        
        return prompt.strip()
    
    # ═══════════════════════════════════════════════════════════════
    # ORQUESTADOR: Decisiones Pragmáticas
    # ═══════════════════════════════════════════════════════════════
    
    def configurar_orquestador(self) -> Dict:
        """
        Configura el Orquestador según tu prisma.
        
        Adapta:
        - Criterios de priorización
        - Nivel de detalle en planes
        - Flexibilidad vs estructura
        - Puntos de decisión
        """
        
        config = {
            "criterios_priorizacion": self._determinar_criterios(),
            "nivel_detalle": self._determinar_nivel_detalle(),
            "flexibilidad": self._determinar_flexibilidad(),
            "puntos_decision": self._generar_puntos_decision(),
            "prompt_adicional": self._generar_prompt_orquestador()
        }
        
        return config
    
    def _determinar_criterios(self) -> List[str]:
        """Criterios de priorización según manifestaciones"""
        
        criterios = []
        
        # Priorizar según manifestaciones activas
        for m in sorted(self.prisma.manifestaciones, key=lambda x: x.progreso_estimado, reverse=False):
            criterios.append(f"{m.dimension.value}_{m.nivel.value}")
        
        # Añadir según tipo HD
        if self.prisma.diseño_humano.tipo == TipoHumanDesign.GENERADOR:
            criterios.insert(0, "respuesta_sacral_positiva")
        elif self.prisma.diseño_humano.tipo == TipoHumanDesign.PROYECTOR:
            criterios.insert(0, "invitacion_recibida")
        
        return criterios[:5]  # Top 5
    
    def _determinar_nivel_detalle(self) -> str:
        """Nivel de detalle en planes según preferencias"""
        
        enea = self.prisma.perfil_psicologico.eneagrama_base
        
        if enea.value == "5":
            return "minimalista"  # Evitar sobre-planificación
        elif enea.value == "1":
            return "detallado"  # Perfeccionista lo necesita
        else:
            return "moderado"
    
    def _determinar_flexibilidad(self) -> float:
        """Nivel de flexibilidad en planes (0-1)"""
        
        mbti = self.prisma.perfil_psicologico.mbti
        
        if "P" in mbti.value:  # Perceptivo
            return 0.7  # Alta flexibilidad
        elif "J" in mbti.value:  # Juicio
            return 0.3  # Baja flexibilidad (más estructura)
        else:
            return 0.5
    
    def _generar_puntos_decision(self) -> List[str]:
        """Genera puntos de decisión personalizados"""
        
        autoridad = self.prisma.diseño_humano.autoridad
        
        if autoridad == AutoridadInterna.SACRAL:
            return [
                "antes_bloque_profundo",
                "antes_cambio_contexto",
                "cierre_jornada"
            ]
        elif autoridad == AutoridadInterna.EMOCIONAL:
            return [
                "inicio_dia",
                "media_jornada",
                "cierre_dia"
            ]
        else:
            return ["inicio_dia", "cierre_dia"]
    
    def _generar_prompt_orquestador(self) -> str:
        """Genera prompt para el Orquestador"""
        
        nivel_detalle = self._determinar_nivel_detalle()
        flexibilidad = self._determinar_flexibilidad()
        trabajo_integracion = self.prisma.perfil_psicologico.trabajo_integracion
        
        prompt = f"""
CONFIGURACIÓN DEL USUARIO:
- Criterios priorización: {', '.join(self._determinar_criterios()[:3])}
- Nivel detalle: {nivel_detalle.upper()}
- Flexibilidad: {flexibilidad:.1f} (0=rígido, 1=muy flexible)
- Trabajo integración: {trabajo_integracion}

INSTRUCCIONES ESPECÍFICAS:
1. Planes {nivel_detalle}s que eviten sobre-planificación
2. {int(flexibilidad*100)}% de bloques DEBEN ser ajustables
3. SIEMPRE incluir checkpoints de "pasar a acción" (5→8)
4. Priorizar manifestaciones con menor progreso
5. Respetar 40% espacio libre (no llenar todo el día)

TRAMPA MENTAL A EVITAR:
"{self.prisma.diseño_humano.trampa_mental}"
→ Contramedida: Forzar decisión sacral antes de planificar mentalmente

waḥdat al-wujūd: Los planes emergen de la claridad interna, no de análisis externo.
al-khayāl al-faʿʿāl: La imaginación creadora requiere ESPACIO para manifestarse.
"""
        
        return prompt.strip()
    
    # ═══════════════════════════════════════════════════════════════
    # DOCUMENTADOR: Captura Personalizada
    # ═══════════════════════════════════════════════════════════════
    
    def configurar_documentador(self) -> Dict:
        """
        Configura el Documentador según tu prisma.
        
        Adapta:
        - Sistema de captura (Obsidian/Anytype)
        - Estructura de notas
        - Frecuencia de síntesis
        - Profundidad de documentación
        """
        
        config = {
            "sistema_primario": self.prisma.estructura_conocimiento.captura_primaria.value,
            "estructura_notas": self._determinar_estructura_notas(),
            "frecuencia_sintesis": self.prisma.estructura_conocimiento.frecuencia_revision,
            "profundidad": self._determinar_profundidad_doc(),
            "conexiones_auto": self.prisma.estructura_conocimiento.conecta_insights_automatico,
            "prompt_adicional": self._generar_prompt_documentador()
        }
        
        return config
    
    def _determinar_estructura_notas(self) -> str:
        """Determina estructura de notas según preferencias"""
        
        if self.prisma.estructura_conocimiento.usa_zettelkasten:
            return "zettelkasten_atomico"
        else:
            return "jerarquico_folders"
    
    def _determinar_profundidad_doc(self) -> str:
        """Determina profundidad de documentación"""
        
        balance = self.prisma.metodo_aprendizaje.profundidad_vs_amplitud
        
        if balance >= 7:
            return "profunda"  # Notas detalladas
        elif balance <= 3:
            return "bullets"  # Capturas rápidas
        else:
            return "moderada"
    
    def _generar_prompt_documentador(self) -> str:
        """Genera prompt para el Documentador"""
        
        sistema = self.prisma.estructura_conocimiento.captura_primaria.value
        umbral = self.prisma.estructura_conocimiento.umbral_nota_permanente
        
        prompt = f"""
CONFIGURACIÓN DEL USUARIO:
- Sistema: {sistema.title()}
- Estructura: {self._determinar_estructura_notas()}
- Profundidad: {self._determinar_profundidad_doc()}
- Umbral nota permanente: {umbral}

INSTRUCCIONES ESPECÍFICAS:
1. Documentar en {sistema.title()} SIEMPRE
2. Formato {self._determinar_estructura_notas()}
3. Síntesis {self.prisma.estructura_conocimiento.frecuencia_revision}
4. Conectar insights automáticamente: {self.prisma.estructura_conocimiento.conecta_insights_automatico}
5. ENTP-5: Documentar para ENSEÑAR (método Feynman), no solo capturar

INDICADORES DE DOMINIO (cuándo nota es permanente):
{chr(10).join(['- ' + ind for ind in self.prisma.metodo_aprendizaje.indicadores_dominio[:3]])}

waḥdat al-wujūd: La documentación refleja la unidad de tu comprensión.
al-khayāl al-faʿʿāl: Escribir es acto creador que materializa conocimiento.
"""
        
        return prompt.strip()
    
    # ═══════════════════════════════════════════════════════════════
    # GUARDIÁN: Métricas Personalizadas
    # ═══════════════════════════════════════════════════════════════
    
    def configurar_guardian(self) -> Dict:
        """
        Configura el Guardián según tu prisma.
        
        Adapta:
        - Métricas a trackear
        - Frecuencia de reportes
        - Alertas personalizadas
        """
        
        config = {
            "metricas_clave": self._determinar_metricas(),
            "frecuencia_reporte": "semanal",
            "alertas": self._generar_alertas(),
            "prompt_adicional": self._generar_prompt_guardian()
        }
        
        return config
    
    def _determinar_metricas(self) -> List[str]:
        """Determina métricas clave a trackear"""
        
        metricas = [
            "ratio_expansion_contraccion",
            "estados_cero_completados",
            "manifestaciones_progreso"
        ]
        
        # Añadir según sesgos
        sesgos = self._identificar_sesgos()
        
        if "sobre_analisis_paralizante" in sesgos:
            metricas.append("ratio_planificacion_accion")
        
        if "desconexion_necesidades_corporales" in sesgos:
            metricas.append("practicas_biologicas_completadas")
        
        return metricas
    
    def _generar_alertas(self) -> List[Dict]:
        """Genera alertas personalizadas"""
        
        alertas = []
        
        # Alerta según sesgos
        sesgos = self._identificar_sesgos()
        
        if "sobre_analisis_paralizante" in sesgos:
            alertas.append({
                "condicion": "ratio_planificacion_accion > 0.7",
                "mensaje": "⚠️ Demasiado análisis. 5→8: ACTÚA sin más preparación."
            })
        
        if "postergar_accion_por_mas_info" in sesgos:
            alertas.append({
                "condicion": "mismo_bloque_3_dias",
                "mensaje": "⚠️ Llevamos 3 días en el mismo bloque. Ya sabes suficiente. EJECUTA."
            })
        
        return alertas
    
    def _generar_prompt_guardian(self) -> str:
        """Genera prompt para el Guardián"""
        
        sesgos = self._identificar_sesgos()[:2]
        
        prompt = f"""
CONFIGURACIÓN DEL USUARIO:
- Métricas clave: {', '.join(self._determinar_metricas()[:3])}
- Sesgos a vigilar: {', '.join(sesgos)}

INSTRUCCIONES ESPECÍFICAS:
1. Reportar semanalmente
2. Alertar si se activan sesgos
3. Celebrar progreso en manifestaciones
4. Sugerir ajustes basados en metadatos reales

waḥdat al-wujūd: El guardián protege la integridad del ser.
al-khayāl al-faʿʿāl: Las métricas sirven a la materialización, no al análisis vacío.
"""
        
        return prompt.strip()
    
    # ═══════════════════════════════════════════════════════════════
    # EXPORTAR CONFIGURACIÓN COMPLETA
    # ═══════════════════════════════════════════════════════════════
    
    def exportar_configuracion_completa(self) -> Dict:
        """Exporta configuración completa para todos los agentes"""
        
        return {
            "estado_cero": self.configurar_estado_cero(),
            "entrelazador": self.configurar_entrelazador(),
            "orquestador": self.configurar_orquestador(),
            "documentador": self.configurar_documentador(),
            "guardian": self.configurar_guardian(),
            "prisma_version": self.prisma.version,
            "ultima_actualizacion": self.prisma.actualizado.isoformat()
        }
    
    def guardar_configuracion(self, ruta: str = None):
        """Guarda configuración en archivo JSON"""
        
        if not ruta:
            ruta = os.path.join(
                os.path.dirname(__file__),
                "..", "..", "config",
                "configuracion_agentes.json"
            )
        
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(self.exportar_configuracion_completa(), f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuración de agentes guardada en: {ruta}")


# ═══════════════════════════════════════════════════════════════════
# CARGAR PRISMA Y GENERAR CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════

def cargar_prisma_y_configurar() -> Optional[MotorPrisma]:
    """
    Carga el prisma personal y genera configuración para agentes.
    """
    
    ruta_prisma = os.path.join(
        os.path.dirname(__file__),
        "..", "..", "config",
        "prisma_personal.json"
    )
    
    if not os.path.exists(ruta_prisma):
        print("⚠️ No se encontró prisma_personal.json")
        print("   Ejecuta: python backend/scripts/configurar_prisma.py")
        return None
    
    with open(ruta_prisma, 'r', encoding='utf-8') as f:
        prisma_data = json.load(f)
    
    prisma = PrismaPersonal(**prisma_data)
    motor = MotorPrisma(prisma)
    
    # Guardar configuración
    motor.guardar_configuracion()
    
    print(f"✅ Prisma de {prisma.nombre} cargado")
    print(f"   {prisma.diseño_humano.tipo.value.title()} | {prisma.diseño_humano.autoridad.value.title()}")
    print(f"   {prisma.perfil_psicologico.mbti.value} | Eneagrama {prisma.perfil_psicologico.eneagrama_base.value}")
    
    return motor


if __name__ == "__main__":
    motor = cargar_prisma_y_configurar()
    
    if motor:
        print("\n📋 Configuración generada para:")
        print("   • Estado Cero")
        print("   • Entrelazador")
        print("   • Orquestador")
        print("   • Documentador")
        print("   • Guardián")
        
        print("\n🕌 Los agentes ahora operan según tu esencia única.")

