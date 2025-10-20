"""
🌙 CALENDARIO HIJRI DE 12 MESES LUNARES
═══════════════════════════════════════════════════════════════════

Sistema litúrgico islámico basado en ciclos lunares puros.

El calendario Hijri es LUNAR (354-355 días/año), no solar.
Por eso las estaciones rotan a través de los meses cada ~33 años.

Cada mes tiene:
- Nombre árabe y significado profundo
- Cualidad energética espiritual
- Enseñanza mística (تصوف)
- Práctica recomendada
- Dimensión del ser priorizada

Cada día de la semana tiene:
- Propósito específico
- Energía arquetípica
- Dimensión prioritaria
- Intención profunda
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum


class CualidadEspiritual(str, Enum):
    """Cualidades espirituales de cada mes (no vinculadas a estaciones solares)"""
    SAGRADO = "sagrado"  # Meses sagrados (4 en total)
    PREPARACION = "preparación"  # Preparación para eventos litúrgicos
    PURIFICACION = "purificación"  # Purificación y ayuno
    CELEBRACION = "celebración"  # Celebración y gratitud
    INTROSPECCIÓN = "introspección"  # Vuelta al interior
    EXPANSION = "expansión"  # Crecimiento y desarrollo
    REVELACION = "revelación"  # Recepción de luz divina


class DiaSemanaArquetipo(str, Enum):
    """Arquetipos de cada día de la semana"""
    LUNES = "lunes"  # Luna - Receptividad, introspección
    MARTES = "martes"  # Marte - Acción, coraje, voluntad
    MIERCOLES = "miércoles"  # Mercurio - Comunicación, conexiones
    JUEVES = "jueves"  # Júpiter - Expansión, sabiduría, enseñanza
    VIERNES = "viernes"  # Venus - Belleza, relaciones, armonía
    SABADO = "sábado"  # Saturno - Estructura, límites, maestría
    DOMINGO = "domingo"  # Sol - Identidad, propósito, centro


class MesHijri(BaseModel):
    """Mes lunar islámico con simbología completa"""
    numero: int
    nombre_arabe: str
    nombre_es: str
    significado: str
    cualidad: CualidadEspiritual
    es_sagrado: bool  # Los 4 meses sagrados
    ensenanza_mistica: str  # تصوف
    practica_recomendada: str
    dimension_prioritaria: str  # De las 7 dimensiones
    simbolo: str
    color: str
    ayat_clave: str  # Ayat del Corán relacionada (opcional)


class DiaSemana(BaseModel):
    """Día de la semana con propósito profundo"""
    nombre: str
    arquetipo: DiaSemanaArquetipo
    proposito_profundo: str
    energia: str
    dimension_prioritaria: str
    intencion: str
    practica_sugerida: str
    alerta_sesgo: str  # Qué sesgo vigilar este día


class CalendarioHijri:
    """
    Calendario Hijri de 12 meses lunares islámico.
    
    Basado en ciclos lunares puros (29-30 días por mes, ~354 días/año).
    
    Los 4 meses sagrados (حُرُم):
    1. Muharram
    2. Rajab
    3. Dhu al-Qi'dah
    4. Dhu al-Hijjah
    
    Para MVP: Usamos hijri-converter para cálculo preciso.
    """

    def __init__(self):
        self.meses_hijri = self._inicializar_meses()
        self.dias_semana = self._inicializar_dias_semana()

    def _inicializar_meses(self) -> list[MesHijri]:
        """
        12 meses lunares islámicos con profundidad mística.
        
        Basado en el calendario Hijri real (comienza con la Hégira, 622 CE).
        Cada mes tiene enseñanzas sufíes profundas.
        """
        return [
            # ═══════════════════════════════════════════════════════════
            # INVIERNO: Introspección y Silencio Interior
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=1,
                nombre_arabe="Muharram",
                nombre_es="El Sagrado",
                significado="Mes de inicio, introspección profunda, muerte del ego",
                cualidad_energetica="Silencio sagrado, vuelta al centro",
                estacion=EstacionAlma.INVIERNO,
                ensenanza_espiritual="La verdadera renovación comienza en el silencio. Morir antes de morir.",
                practica_recomendada="Ayuno voluntario, meditación en oscuridad, dhikr silencioso",
                dimension_prioritaria="Espiritual",
                simbolo="🌑",
                color="Negro/Índigo",
                elemento="Agua quieta"
            ),
            
            MesHijri(
                numero=2,
                nombre_arabe="Safar",
                nombre_es="El Vacío",
                significado="Vaciamiento, soltar lo que no sirve, preparar el recipiente",
                cualidad_energetica="Purificación, liberación de apegos",
                estacion=EstacionAlma.INVIERNO,
                ensenanza_espiritual="Solo el recipiente vacío puede llenarse. El vacío no es ausencia, es potencial.",
                practica_recomendada="Tawba (arrepentimiento sincero), eliminar lo superfluo, minimalismo",
                dimension_prioritaria="Biológico/Físico",
                simbolo="🫗",
                color="Gris/Blanco",
                elemento="Viento invernal"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # PRIMAVERA: Renacimiento y Brotes de Luz
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=3,
                nombre_arabe="Rabi' al-Awwal",
                nombre_es="Primavera Primera",
                significado="Nacimiento del Profeta ﷺ, luz que emerge",
                cualidad_energetica="Amor, compasión, conexión con el maestro interior",
                estacion=EstacionAlma.PRIMAVERA,
                ensenanza_espiritual="La luz profética es tu propia luz interior. El maestro está dentro.",
                practica_recomendada="Salawat (bendiciones al Profeta), estudiar Sira, emular Akhlaq",
                dimension_prioritaria="Conocimiento",
                simbolo="🌱",
                color="Verde claro",
                elemento="Brisa primaveral"
            ),
            
            MesHijri(
                numero=4,
                nombre_arabe="Rabi' al-Thani",
                nombre_es="Primavera Segunda",
                significado="Florecimiento, expresión de la belleza interior",
                cualidad_energetica="Creatividad, expresión, belleza",
                estacion=EstacionAlma.PRIMAVERA,
                ensenanza_espiritual="Tu existencia es acto creativo. Expresa lo que tu alma anhela materializar.",
                practica_recomendada="Arte devocional, poesía, caligrafía, música sacra",
                dimension_prioritaria="Creativo",
                simbolo="🌸",
                color="Rosa/Coral",
                elemento="Lluvia de primavera"
            ),
            
            MesHijri(
                numero=5,
                nombre_arabe="Jumada al-Awwal",
                nombre_es="Primera Aridez",
                significado="Consolidar raíces, profundizar en tierra",
                cualidad_energetica="Estabilidad, disciplina, trabajo interno",
                estacion=EstacionAlma.PRIMAVERA,
                ensenanza_espiritual="La planta que crece rápido tiene raíces débiles. Profundiza antes de expandir.",
                practica_recomendada="Rutinas diarias, Tahajjud constante, estudio sistemático",
                dimension_prioritaria="Desarrollo",
                simbolo="🌿",
                color="Verde oscuro",
                elemento="Tierra fértil"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # VERANO: Manifestación y Plenitud
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=6,
                nombre_arabe="Jumada al-Thani",
                nombre_es="Segunda Aridez",
                significado="Resistencia en el calor, perseverancia",
                cualidad_energetica="Fuerza interior, paciencia (sabr), resiliencia",
                estacion=EstacionAlma.VERANO,
                ensenanza_espiritual="El desierto enseña resistencia. La sed enseña el valor del agua viva.",
                practica_recomendada="Sabr (paciencia activa), ayuno de Dawud, retiros solitarios",
                dimension_prioritaria="Biológico/Físico",
                simbolo="🏜️",
                color="Dorado/Ocre",
                elemento="Fuego del desierto"
            ),
            
            MesHijri(
                numero=7,
                nombre_arabe="Rajab",
                nombre_es="El Respetado",
                significado="Mes sagrado, preparación para Ramadán, Isra y Mi'raj",
                cualidad_energetica="Elevación, trascendencia, viaje interior",
                estacion=EstacionAlma.VERANO,
                ensenanza_espiritual="El viaje nocturno del alma. Trasciende los límites de tu ser pequeño.",
                practica_recomendada="Meditación profunda, contemplación de los cielos, qiyam al-layl",
                dimension_prioritaria="Espiritual",
                simbolo="🌌",
                color="Azul noche",
                elemento="Éter"
            ),
            
            MesHijri(
                numero=8,
                nombre_arabe="Sha'ban",
                nombre_es="El Distribuidor",
                significado="Preparación intensiva, distribución de destinos",
                cualidad_energetica="Anticipación, preparación, clarificación de intención",
                estacion=EstacionAlma.VERANO,
                ensenanza_espiritual="Prepara el corazón antes de que llegue el huésped. La intención precede a la acción.",
                practica_recomendada="Niyyah (clarificar intenciones), ayuno preparatorio, du'a intenso",
                dimension_prioritaria="Desarrollo",
                simbolo="🎯",
                color="Blanco brillante",
                elemento="Aire puro"
            ),
            
            MesHijri(
                numero=9,
                nombre_arabe="Ramadan",
                nombre_es="El Ardiente",
                significado="Mes del Corán, purificación total, Laylat al-Qadr",
                cualidad_energetica="Purificación máxima, revelación, intimidad divina",
                estacion=EstacionAlma.VERANO,
                ensenanza_espiritual="El ayuno es puerta. La purificación es velo que cae. Laylat al-Qadr: una noche vale 1000 meses.",
                practica_recomendada="Sawm (ayuno), Tarawih, recitación completa del Corán, I'tikaf",
                dimension_prioritaria="Espiritual",
                simbolo="🌙✨",
                color="Plateado/Dorado",
                elemento="Luz pura"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # OTOÑO: Cosecha y Gratitud
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=10,
                nombre_arabe="Shawwal",
                nombre_es="El Elevador",
                significado="Celebración de Eid, gratitud, elevación post-Ramadán",
                cualidad_energetica="Gozo, gratitud (shukr), celebración",
                estacion=EstacionAlma.OTONO,
                ensenanza_espiritual="La gratitud es puerta de más bendición. Celebra con conciencia.",
                practica_recomendada="Eid al-Fitr, 6 días de ayuno de Shawwal, sadaqah (caridad)",
                dimension_prioritaria="Relacional",
                simbolo="🎉",
                color="Verde esmeralda",
                elemento="Brisa fresca"
            ),
            
            MesHijri(
                numero=11,
                nombre_arabe="Dhu al-Qi'dah",
                nombre_es="El de la Tregua",
                significado="Mes sagrado, cese de conflictos, paz interior",
                cualidad_energetica="Paz, reconciliación, armonía",
                estacion=EstacionAlma.OTONO,
                ensenanza_espiritual="La tregua externa refleja la paz interna. Reconcíliate contigo mismo primero.",
                practica_recomendada="Perdón (af'w), reconciliación, diálogo interno",
                dimension_prioritaria="Relacional",
                simbolo="☮️",
                color="Azul claro",
                elemento="Agua tranquila"
            ),
            
            MesHijri(
                numero=12,
                nombre_arabe="Dhu al-Hijjah",
                nombre_es="El de la Peregrinación",
                significado="Hajj, sacrificio de Eid al-Adha, ofrenda total",
                cualidad_energetica="Entrega, sacrificio, devoción absoluta",
                estacion=EstacionAlma.OTONO,
                ensenanza_espiritual="El Hajj es símbolo del viaje interior. Sacrifica tu ego, no el animal.",
                practica_recomendada="10 primeros días sagrados, Arafah, Eid al-Adha, Qurbani (sacrificio)",
                dimension_prioritaria="Espiritual",
                simbolo="🕋",
                color="Negro/Blanco (Ihram)",
                elemento="Piedra/Montaña"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # INTERSTICIO: Tiempo Fuera del Tiempo
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=13,
                nombre_arabe="Al-Barzakh",
                nombre_es="El Intersticio",
                significado="Tiempo fuera del tiempo, puente entre ciclos, bardo",
                cualidad_energetica="Misterio, transición, integración total",
                estacion=EstacionAlma.INTERSTICIO,
                ensenanza_espiritual="El Barzakh es el espacio entre respiraciones. Ahí habita Dios. El ciclo se cierra y abre simultáneamente.",
                practica_recomendada="Retiro silencioso, khalwah, integración del año, muraqabah",
                dimension_prioritaria="Espiritual",
                simbolo="∞",
                color="Transparente/Iridiscente",
                elemento="Vacío luminoso"
            ),
        ]

    def _inicializar_dias_semana(self) -> dict[str, DiaSemana]:
        """
        7 días con propósito arquetípico profundo.
        
        Cada día tiene una energía específica que el Entrelazador usa
        para planificar actividades alineadas.
        """
        return {
            "lunes": DiaSemana(
                nombre="Lunes",
                arquetipo=DiaSemanaArquetipo.LUNES,
                proposito_profundo="Receptividad y escucha interior. Día de la Luna.",
                energia="Femenina, receptiva, introspectiva, emocional",
                dimension_prioritaria="Espiritual/Conocimiento",
                intencion="Escuchar lo que el alma necesita esta semana",
                practica_sugerida="Meditación matutina, journaling, recepción de insights",
                alerta_sesgo="Sobre-análisis sin acción (ENTP-5)"
            ),
            
            "martes": DiaSemana(
                nombre="Martes",
                arquetipo=DiaSemanaArquetipo.MARTES,
                proposito_profundo="Acción decidida y coraje. Día de Marte.",
                energia="Masculina, activa, guerrera, volitiva",
                dimension_prioritaria="Desarrollo/Financiero",
                intencion="Ejecutar lo prioritario con valentía",
                practica_sugerida="Bloques de acción profunda, confrontar lo difícil",
                alerta_sesgo="Impulsividad sin estrategia"
            ),
            
            "miércoles": DiaSemana(
                nombre="Miércoles",
                arquetipo=DiaSemanaArquetipo.MIERCOLES,
                proposito_profundo="Comunicación y conexión. Día de Mercurio.",
                energia="Neutra, comunicativa, conectiva, versátil",
                dimension_prioritaria="Conocimiento/Relacional",
                intencion="Conectar ideas, personas, conceptos",
                practica_sugerida="Networking, enseñar lo aprendido, escritura",
                alerta_sesgo="Dispersión en múltiples rabbit holes"
            ),
            
            "jueves": DiaSemana(
                nombre="Jueves",
                arquetipo=DiaSemanaArquetipo.JUEVES,
                proposito_profundo="Expansión y sabiduría. Día de Júpiter.",
                energia="Expansiva, generosa, filosófica, abundante",
                dimension_prioritaria="Conocimiento/Financiero",
                intencion="Expandir comprensión y generar abundancia",
                practica_sugerida="Estudio profundo, mentoría, generar valor",
                alerta_sesgo="Exceso de optimismo sin realismo"
            ),
            
            "viernes": DiaSemana(
                nombre="Viernes",
                arquetipo=DiaSemanaArquetipo.VIERNES,
                proposito_profundo="Belleza y relación. Día de Venus. Jumu'ah.",
                energia="Armoniosa, relacional, estética, amorosa",
                dimension_prioritaria="Relacional/Creativo",
                intencion="Nutrir relaciones y crear belleza",
                practica_sugerida="Jumu'ah, tiempo con seres queridos, arte",
                alerta_sesgo="Complacer a otros ignorando necesidad propia"
            ),
            
            "sábado": DiaSemana(
                nombre="Sábado",
                arquetipo=DiaSemanaArquetipo.SABADO,
                proposito_profundo="Estructura y maestría. Día de Saturno.",
                energia="Cristalizadora, disciplinada, maestra, limitante",
                dimension_prioritaria="Desarrollo/Biológico",
                intencion="Consolidar aprendizaje, dominio técnico",
                practica_sugerida="Práctica deliberada, refinamiento, sistemas",
                alerta_sesgo="Rigidez excesiva, perfeccionismo paralizante"
            ),
            
            "domingo": DiaSemana(
                nombre="Domingo",
                arquetipo=DiaSemanaArquetipo.DOMINGO,
                proposito_profundo="Identidad y propósito. Día del Sol. Centro.",
                energia="Central, radiante, identitaria, integradora",
                dimension_prioritaria="Espiritual/Todas",
                intencion="Integrar la semana, reconectar con propósito vital",
                practica_sugerida="Revisión semanal, gratitud, visión de futuro",
                alerta_sesgo="Egocentrismo, desconexión de lo trascendente"
            ),
        }

    def obtener_mes_actual(self, fecha: Optional[date] = None) -> MesHijri:
        """
        Obtiene el mes Hijri actual.
        
        Para MVP: Aproximación por mes gregoriano.
        Futura implementación: hijri-converter para cálculo lunar preciso.
        """
        fecha = fecha or date.today()
        
        # Aproximación: ciclo de 13 meses
        # Cada mes gregoriano se mapea a un mes Hijri
        indice = (fecha.month - 1) % 13
        
        return self.meses_hijri[indice]

    def obtener_dia_semana(self, fecha: Optional[date] = None) -> DiaSemana:
        """
        Obtiene el día de la semana con su propósito profundo.
        """
        fecha = fecha or date.today()
        
        dias_nombres = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        dia_idx = fecha.weekday()
        dia_nombre = dias_nombres[dia_idx]
        
        return self.dias_semana[dia_nombre]

    def obtener_contexto_temporal_completo(
        self, 
        fecha: Optional[date] = None
    ) -> dict:
        """
        Retorna contexto temporal completo para el Entrelazador/Orquestador.
        
        Incluye:
        - Mes Hijri actual con toda su simbología
        - Día de la semana con propósito
        - Estación del alma
        - Dimensión prioritaria
        - Prácticas recomendadas
        """
        fecha = fecha or date.today()
        
        mes = self.obtener_mes_actual(fecha)
        dia = self.obtener_dia_semana(fecha)
        
        return {
            "fecha": fecha.isoformat(),
            "mes_hijri": {
                "numero": mes.numero,
                "nombre": mes.nombre_arabe,
                "nombre_es": mes.nombre_es,
                "significado": mes.significado,
                "cualidad": mes.cualidad_energetica,
                "estacion": mes.estacion.value,
                "ensenanza": mes.ensenanza_espiritual,
                "practica": mes.practica_recomendada,
                "dimension": mes.dimension_prioritaria,
                "simbolo": mes.simbolo,
                "color": mes.color,
                "elemento": mes.elemento
            },
            "dia_semana": {
                "nombre": dia.nombre,
                "arquetipo": dia.arquetipo.value,
                "proposito": dia.proposito_profundo,
                "energia": dia.energia,
                "dimension": dia.dimension_prioritaria,
                "intencion": dia.intencion,
                "practica": dia.practica_sugerida,
                "alerta": dia.alerta_sesgo
            },
            "guia_entrelazador": self._generar_guia_entrelazador(mes, dia)
        }

    def _generar_guia_entrelazador(self, mes: MesHijri, dia: DiaSemana) -> dict:
        """
        Genera guía específica para que el Entrelazador planifique con excelencia.
        
        Combina:
        - Energía del mes
        - Propósito del día
        - Dimensiones prioritarias
        """
        return {
            "dimension_prioritaria_mes": mes.dimension_prioritaria,
            "dimension_prioritaria_dia": dia.dimension_prioritaria,
            "energia_dominante": dia.energia,
            "practica_integrada": f"{mes.practica_recomendada} + {dia.practica_sugerida}",
            "sesgo_vigilar": dia.alerta_sesgo,
            "mensaje_guia": f"Mes de {mes.cualidad_energetica}. Día para {dia.intencion}. {mes.ensenanza_espiritual}"
        }

    def obtener_vista_semanal(self, fecha_inicio: Optional[date] = None) -> dict:
        """
        Vista semanal con propósito de cada día.
        
        Para la interfaz de Vista Semanal.
        """
        from datetime import timedelta
        
        fecha_inicio = fecha_inicio or date.today()
        # Ajustar a lunes
        dias_hasta_lunes = fecha_inicio.weekday()
        lunes = fecha_inicio - timedelta(days=dias_hasta_lunes)
        
        semana = []
        for i in range(7):
            dia_fecha = lunes + timedelta(days=i)
            dia_info = self.obtener_dia_semana(dia_fecha)
            
            semana.append({
                "fecha": dia_fecha.isoformat(),
                "dia": dia_info.nombre,
                "arquetipo": dia_info.arquetipo.value,
                "proposito": dia_info.proposito_profundo,
                "energia": dia_info.energia,
                "dimension": dia_info.dimension_prioritaria,
                "intencion": dia_info.intencion,
                "practica": dia_info.practica_sugerida
            })
        
        mes_actual = self.obtener_mes_actual(lunes)
        
        return {
            "semana_inicio": lunes.isoformat(),
            "mes_hijri": mes_actual.nombre_arabe,
            "cualidad_mes": mes_actual.cualidad_energetica,
            "dias": semana
        }

    def obtener_vista_mensual(self, mes: Optional[int] = None, año: Optional[int] = None) -> dict:
        """
        Vista mensual con significado litúrgico completo.
        
        Para la interfaz de Vista Mensual.
        """
        fecha_ref = date(año or date.today().year, mes or date.today().month, 1)
        mes_hijri = self.obtener_mes_actual(fecha_ref)
        
        return {
            "mes_numero": mes_hijri.numero,
            "nombre": mes_hijri.nombre_arabe,
            "nombre_es": mes_hijri.nombre_es,
            "significado": mes_hijri.significado,
            "cualidad": mes_hijri.cualidad_energetica,
            "estacion": mes_hijri.estacion.value,
            "ensenanza": mes_hijri.ensenanza_espiritual,
            "practica": mes_hijri.practica_recomendada,
            "dimension": mes_hijri.dimension_prioritaria,
            "simbolo": mes_hijri.simbolo,
            "color": mes_hijri.color,
            "elemento": mes_hijri.elemento
        }

    def obtener_vista_anual(self, año: Optional[int] = None) -> dict:
        """
        Vista anual completa con los 13 meses y sus significados.
        
        Para la interfaz de Vista Anual.
        """
        return {
            "año": año or date.today().year,
            "meses": [
                {
                    "numero": m.numero,
                    "nombre": m.nombre_arabe,
                    "nombre_es": m.nombre_es,
                    "cualidad": m.cualidad_energetica,
                    "estacion": m.estacion.value,
                    "dimension": m.dimension_prioritaria,
                    "simbolo": m.simbolo,
                    "color": m.color
                }
                for m in self.meses_hijri
            ],
            "ciclo_completo": "13 meses lunares + intersticio",
            "ensenanza_anual": "El ciclo completo es un viaje del alma: desde el silencio de Muharram hasta el vacío luminoso de Al-Barzakh, para renacer de nuevo."
        }
