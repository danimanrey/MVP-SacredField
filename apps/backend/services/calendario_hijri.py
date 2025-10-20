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

from datetime import date, datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from enum import Enum
import hijri_converter


class CualidadEspiritual(str, Enum):
    """Cualidades espirituales de cada mes (no vinculadas a estaciones solares)"""
    SAGRADO = "sagrado"  # Meses sagrados (4 en total)
    PREPARACION = "preparación"  # Preparación para eventos litúrgicos
    PURIFICACION = "purificación"  # Purificación y ayuno
    CELEBRACION = "celebración"  # Celebración y gratitud
    INTROSPECCION = "introspección"  # Vuelta al interior
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
    ayat_clave: str  # Ayat del Corán relacionada


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
    1. Muharram (mes 1)
    2. Rajab (mes 7)
    3. Dhu al-Qi'dah (mes 11)
    4. Dhu al-Hijjah (mes 12)
    
    Usa hijri-converter para cálculo preciso.
    """

    def __init__(self):
        self.meses_hijri = self._inicializar_meses()
        self.dias_semana = self._inicializar_dias_semana()

    def _inicializar_meses(self) -> list[MesHijri]:
        """
        12 meses lunares islámicos REALES con profundidad mística.
        
        Basado en el calendario Hijri (comienza con la Hégira, 622 CE).
        Cada mes tiene enseñanzas sufíes profundas.
        """
        return [
            # ═══════════════════════════════════════════════════════════
            # MES 1: MUHARRAM - El Sagrado
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=1,
                nombre_arabe="Muharram",
                nombre_es="El Sagrado",
                significado="Primer mes del año Hijri. Mes sagrado de introspección profunda.",
                cualidad=CualidadEspiritual.SAGRADO,
                es_sagrado=True,
                ensenanza_mistica="La verdadera renovación comienza en el silencio interior. Morir antes de morir (موت قبل أن تموت). Ashura: el día que salvó a Moisés y los creyentes.",
                practica_recomendada="Ayuno voluntario (especialmente día 10, Ashura), dhikr silencioso, muraqabah (meditación contemplativa)",
                dimension_prioritaria="Espiritual",
                simbolo="🌑",
                color="Negro/Índigo profundo",
                ayat_clave="Corán 39:53 - 'Di: Oh siervos míos que os habéis excedido contra vosotros mismos, no desesperéis de la misericordia de Allah.'"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # MES 2: SAFAR - El Vacío
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=2,
                nombre_arabe="Safar",
                nombre_es="El Vacío",
                significado="Mes de vaciamiento y soltar lo que no sirve. Preparar el recipiente.",
                cualidad=CualidadEspiritual.INTROSPECCION,
                es_sagrado=False,
                ensenanza_mistica="Solo el recipiente vacío puede llenarse. El vacío (فراغ) no es ausencia, es potencial infinito. Tawba sincera.",
                practica_recomendada="Tawba (arrepentimiento consciente), eliminar lo superfluo, minimalismo intencional, purificación de apegos",
                dimension_prioritaria="Biológico/Físico",
                simbolo="🫗",
                color="Gris/Blanco puro",
                ayat_clave="Corán 2:286 - 'Allah no impone a ninguna alma una carga mayor de lo que puede soportar.'"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # MES 3: RABI' AL-AWWAL - Primera Primavera
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=3,
                nombre_arabe="Rabi' al-Awwal",
                nombre_es="Primera Primavera",
                significado="Nacimiento del Profeta Muhammad ﷺ (Mawlid). Luz profética que emerge.",
                cualidad=CualidadEspiritual.REVELACION,
                es_sagrado=False,
                ensenanza_mistica="La luz profética (نور محمدي) es tu propia luz interior. El maestro perfecto está dentro de ti. Akhlaq (carácter noble).",
                practica_recomendada="Salawat (bendiciones al Profeta), estudiar Sira (biografía profética), emular Akhlaq muhammadi",
                dimension_prioritaria="Conocimiento",
                simbolo="🌱✨",
                color="Verde esmeralda",
                ayat_clave="Corán 33:21 - 'Tenéis en el Mensajero de Allah un excelente ejemplo.'"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # MES 4: RABI' AL-THANI - Segunda Primavera
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=4,
                nombre_arabe="Rabi' al-Thani",
                nombre_es="Segunda Primavera",
                significado="Florecimiento y expresión de la belleza interior.",
                cualidad=CualidadEspiritual.EXPANSION,
                es_sagrado=False,
                ensenanza_mistica="Tu existencia es acto creativo divino. Expresa lo que tu alma (روح) anhela materializar. Al-Jamāl (la Belleza divina).",
                practica_recomendada="Arte devocional, poesía (como Rumi), caligrafía árabe, música sacra, expresión creativa consciente",
                dimension_prioritaria="Creativo",
                simbolo="🌸",
                color="Rosa/Coral",
                ayat_clave="Corán 55:1-4 - 'El Misericordioso enseñó el Corán. Creó al ser humano. Le enseñó la expresión clara.'"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # MES 5: JUMADA AL-AWWAL - Primera Aridez
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=5,
                nombre_arabe="Jumada al-Awwal",
                nombre_es="Primera Aridez",
                significado="Consolidar raíces profundas. Disciplina interior.",
                cualidad=CualidadEspiritual.INTROSPECCION,
                es_sagrado=False,
                ensenanza_mistica="La planta que crece rápido tiene raíces débiles. Profundiza (تعمق) antes de expandir. Sabr (paciencia activa).",
                practica_recomendada="Rutinas diarias consistentes, Tahajjud (oración nocturna) constante, estudio sistemático del Din",
                dimension_prioritaria="Desarrollo",
                simbolo="🌿",
                color="Verde oscuro/Tierra",
                ayat_clave="Corán 2:153 - 'Oh creyentes, buscad ayuda en la paciencia y la oración.'"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # MES 6: JUMADA AL-THANI - Segunda Aridez
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=6,
                nombre_arabe="Jumada al-Thani",
                nombre_es="Segunda Aridez",
                significado="Resistencia en el desierto. Perseverancia y fuerza interior.",
                cualidad=CualidadEspiritual.INTROSPECCION,
                es_sagrado=False,
                ensenanza_mistica="El desierto enseña resistencia (مقاومة). La sed enseña el valor del agua viva. Tawakkul (confianza absoluta).",
                practica_recomendada="Sabr (paciencia activa), ayuno de Dawud (un día sí, uno no), retiros en silencio",
                dimension_prioritaria="Biológico/Físico",
                simbolo="🏜️",
                color="Dorado/Ocre",
                ayat_clave="Corán 65:3 - 'Quien confía en Allah, Él le basta.'"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # MES 7: RAJAB - El Respetado
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=7,
                nombre_arabe="Rajab",
                nombre_es="El Respetado",
                significado="Mes sagrado. Isra y Mi'raj (viaje nocturno y ascensión del Profeta ﷺ).",
                cualidad=CualidadEspiritual.SAGRADO,
                es_sagrado=True,
                ensenanza_mistica="El viaje nocturno del alma (معراج الروح). Trasciende los límites de tu ser pequeño. La oración es Mi'raj del creyente.",
                practica_recomendada="Meditación profunda, contemplación de los cielos (تفكر), Qiyam al-Layl intenso, ayuno voluntario",
                dimension_prioritaria="Espiritual",
                simbolo="🌌",
                color="Azul noche/Índigo",
                ayat_clave="Corán 17:1 - 'Glorificado sea Quien hizo viajar de noche a Su siervo desde la Mezquita Sagrada.'"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # MES 8: SHA'BAN - El Distribuidor
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=8,
                nombre_arabe="Sha'ban",
                nombre_es="El Distribuidor",
                significado="Preparación intensiva para Ramadán. Distribución de destinos (Laylat al-Bara'ah).",
                cualidad=CualidadEspiritual.PREPARACION,
                es_sagrado=False,
                ensenanza_mistica="Prepara el corazón antes de que llegue el huésped. Niyyah (intención pura) precede a toda acción. Laylat al-Bara'ah (noche 15).",
                practica_recomendada="Clarificar intenciones (نية), ayuno preparatorio, du'a intenso, istighfar (pedir perdón)",
                dimension_prioritaria="Desarrollo",
                simbolo="🎯",
                color="Blanco brillante",
                ayat_clave="Corán 2:225 - 'Allah os pedirá cuentas por la intención de vuestros corazones.'"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # MES 9: RAMADAN - El Ardiente
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=9,
                nombre_arabe="Ramadan",
                nombre_es="El Ardiente",
                significado="Mes del Corán. Purificación total. Laylat al-Qadr (noche del decreto).",
                cualidad=CualidadEspiritual.PURIFICACION,
                es_sagrado=False,
                ensenanza_mistica="El ayuno (صوم) es puerta de purificación total. Laylat al-Qadr: una noche vale más que mil meses. La revelación del Corán.",
                practica_recomendada="Sawm (ayuno completo), Tarawih (oración nocturna), recitación completa del Corán, I'tikaf (retiro espiritual), Zakat",
                dimension_prioritaria="Espiritual",
                simbolo="🌙✨",
                color="Plateado/Dorado",
                ayat_clave="Corán 2:185 - 'El mes de Ramadán, en el que fue revelado el Corán como guía para la humanidad.'"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # MES 10: SHAWWAL - El Elevador
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=10,
                nombre_arabe="Shawwal",
                nombre_es="El Elevador",
                significado="Celebración de Eid al-Fitr. Gratitud y elevación post-Ramadán.",
                cualidad=CualidadEspiritual.CELEBRACION,
                es_sagrado=False,
                ensenanza_mistica="La gratitud (شكر) es puerta de más bendición. Celebra con conciencia. 6 días de ayuno de Shawwal = año completo.",
                practica_recomendada="Eid al-Fitr (celebración), 6 días de ayuno voluntario, Sadaqah (caridad), reuniones familiares conscientes",
                dimension_prioritaria="Relacional",
                simbolo="🎉",
                color="Verde esmeralda claro",
                ayat_clave="Corán 14:7 - 'Si sois agradecidos, os aumentaré. Pero si sois ingratos, Mi castigo es severo.'"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # MES 11: DHU AL-QI'DAH - El de la Tregua
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=11,
                nombre_arabe="Dhu al-Qi'dah",
                nombre_es="El de la Tregua",
                significado="Mes sagrado. Cese de conflictos. Paz interior y exterior.",
                cualidad=CualidadEspiritual.SAGRADO,
                es_sagrado=True,
                ensenanza_mistica="La tregua externa refleja la paz interna (سلام). Reconcíliate contigo mismo primero. Salām (paz) es nombre de Allah.",
                practica_recomendada="Perdón consciente (عفو), reconciliación con otros, diálogo interno, Salat al-Shukr (oración de gratitud)",
                dimension_prioritaria="Relacional",
                simbolo="☮️",
                color="Azul claro/Turquesa",
                ayat_clave="Corán 8:61 - 'Y si se inclinan por la paz, inclínate tú también y confía en Allah.'"
            ),
            
            # ═══════════════════════════════════════════════════════════
            # MES 12: DHU AL-HIJJAH - El de la Peregrinación
            # ═══════════════════════════════════════════════════════════
            
            MesHijri(
                numero=12,
                nombre_arabe="Dhu al-Hijjah",
                nombre_es="El de la Peregrinación",
                significado="Hajj (peregrinación). Eid al-Adha. Sacrificio de Ibrahim. Cierre del ciclo.",
                cualidad=CualidadEspiritual.SAGRADO,
                es_sagrado=True,
                ensenanza_mistica="El Hajj es símbolo del viaje interior hacia el centro (الكعبة). Sacrifica tu ego (nafs), no el animal. Entrega total (تسليم).",
                practica_recomendada="10 primeros días sagrados (أفضل من الجهاد), día de Arafah (ayuno), Eid al-Adha, Qurbani (sacrificio simbólico), Dhikr intenso",
                dimension_prioritaria="Espiritual",
                simbolo="🕋",
                color="Negro/Blanco (Ihram)",
                ayat_clave="Corán 22:27 - 'Y proclama entre los humanos la Peregrinación. Vendrán a ti a pie y en todo corcel.'"
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
                proposito_profundo="Receptividad y escucha interior. Día de la Luna (القمر). Introspección profunda.",
                energia="Femenina, receptiva, introspectiva, emocional, contemplativa",
                dimension_prioritaria="Espiritual/Conocimiento",
                intencion="Escuchar lo que el alma necesita esta semana. Recibir insights desde el silencio.",
                practica_sugerida="Meditación matutina (مراقبة), journaling contemplativo, recepción de revelaciones internas",
                alerta_sesgo="Sobre-análisis sin acción (parálisis ENTP-5). Desconexión del cuerpo."
            ),
            
            "martes": DiaSemana(
                nombre="Martes",
                arquetipo=DiaSemanaArquetipo.MARTES,
                proposito_profundo="Acción decidida y coraje. Día de Marte (المريخ). Jihad interior (esfuerzo noble).",
                energia="Masculina, activa, guerrera, volitiva, transformadora",
                dimension_prioritaria="Desarrollo/Financiero",
                intencion="Ejecutar lo prioritario con valentía (شجاعة). Confrontar lo difícil sin evasión.",
                practica_sugerida="Bloques de acción profunda (2-3h), confrontar resistencia, materializar intención",
                alerta_sesgo="Impulsividad sin estrategia. Acción sin respuesta sacral."
            ),
            
            "miércoles": DiaSemana(
                nombre="Miércoles",
                arquetipo=DiaSemanaArquetipo.MIERCOLES,
                proposito_profundo="Comunicación y conexión. Día de Mercurio (عطارد). Puente entre mundos.",
                energia="Neutra, comunicativa, conectiva, versátil, mediadora",
                dimension_prioritaria="Conocimiento/Relacional",
                intencion="Conectar ideas, personas, conceptos. Enseñar lo comprendido (التعليم).",
                practica_sugerida="Networking consciente, enseñar lo aprendido (método Feynman), escritura, síntesis",
                alerta_sesgo="Dispersión en múltiples rabbit holes. Superficialidad sin profundidad."
            ),
            
            "jueves": DiaSemana(
                nombre="Jueves",
                arquetipo=DiaSemanaArquetipo.JUEVES,
                proposito_profundo="Expansión y sabiduría. Día de Júpiter (المشتري). Generosidad y abundancia.",
                energia="Expansiva, generosa, filosófica, abundante, visionaria",
                dimension_prioritaria="Conocimiento/Financiero",
                intencion="Expandir comprensión profunda. Generar abundancia (بركة) desde el valor.",
                practica_sugerida="Estudio profundo del Din, mentoría (dar y recibir), generar valor económico consciente",
                alerta_sesgo="Exceso de optimismo sin realismo. Promesas sin ejecución."
            ),
            
            "viernes": DiaSemana(
                nombre="Viernes",
                arquetipo=DiaSemanaArquetipo.VIERNES,
                proposito_profundo="Belleza y relación. Día de Venus (الزهرة). Jumu'ah (يوم الجمعة) - El mejor día.",
                energia="Armoniosa, relacional, estética, amorosa, comunitaria",
                dimension_prioritaria="Relacional/Creativo",
                intencion="Nutrir relaciones sagradas. Crear belleza (جمال). Reunión comunitaria (Jumu'ah).",
                practica_sugerida="Salat al-Jumu'ah (obligatoria), tiempo cualitativo con seres queridos, expresión artística devocional",
                alerta_sesgo="Complacer a otros ignorando necesidad propia. Evasión del conflicto necesario."
            ),
            
            "sábado": DiaSemana(
                nombre="Sábado",
                arquetipo=DiaSemanaArquetipo.SABADO,
                proposito_profundo="Estructura y maestría. Día de Saturno (زحل). Disciplina que libera.",
                energia="Cristalizadora, disciplinada, maestra, limitante-liberadora, rigurosa",
                dimension_prioritaria="Desarrollo/Biológico",
                intencion="Consolidar aprendizaje. Dominio técnico (إتقان). Práctica deliberada.",
                practica_sugerida="Práctica deliberada intensiva, refinamiento técnico, construcción de sistemas robustos",
                alerta_sesgo="Rigidez excesiva. Perfeccionismo paralizante. Sobre-control."
            ),
            
            "domingo": DiaSemana(
                nombre="Domingo",
                arquetipo=DiaSemanaArquetipo.DOMINGO,
                proposito_profundo="Identidad y propósito. Día del Sol (الشمس). Centro del ser. Integración.",
                energia="Central, radiante, identitaria, integradora, totalizante",
                dimension_prioritaria="Espiritual/Todas",
                intencion="Integrar la semana vivida. Reconectar con propósito vital (رسالة). Visión de futuro.",
                practica_sugerida="Revisión semanal profunda, gratitud activa (شكر), planificación visionaria desde el centro",
                alerta_sesgo="Egocentrismo. Desconexión de lo trascendente. Identificación con el yo pequeño."
            ),
        }

    def obtener_mes_actual(self, fecha: Optional[date] = None) -> MesHijri:
        """
        Obtiene el mes Hijri actual usando cálculo lunar preciso.
        
        Usa hijri-converter para conversión gregoriana → hijri real.
        """
        fecha = fecha or date.today()
        
        # Convertir fecha gregoriana a Hijri
        hijri = hijri_converter.Gregorian(fecha.year, fecha.month, fecha.day).to_hijri()
        
        # hijri.month va de 1 a 12
        mes_numero = hijri.month
        
        return self.meses_hijri[mes_numero - 1]  # Lista indexada desde 0

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
        - Cualidad espiritual
        - Dimensión prioritaria
        - Prácticas recomendadas
        """
        fecha = fecha or date.today()
        
        mes = self.obtener_mes_actual(fecha)
        dia = self.obtener_dia_semana(fecha)
        
        # Obtener fecha Hijri completa
        hijri = hijri_converter.Gregorian(fecha.year, fecha.month, fecha.day).to_hijri()
        
        return {
            "fecha_gregoriana": fecha.isoformat(),
            "fecha_hijri": f"{hijri.day} {mes.nombre_arabe} {hijri.year}",
            "mes_hijri": {
                "numero": mes.numero,
                "nombre": mes.nombre_arabe,
                "nombre_es": mes.nombre_es,
                "significado": mes.significado,
                "cualidad": mes.cualidad.value,
                "es_sagrado": mes.es_sagrado,
                "ensenanza": mes.ensenanza_mistica,
                "practica": mes.practica_recomendada,
                "dimension": mes.dimension_prioritaria,
                "simbolo": mes.simbolo,
                "color": mes.color,
                "ayat": mes.ayat_clave
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
        # Combinar dimensiones (mes + día)
        dimensiones_prioritarias = [mes.dimension_prioritaria, dia.dimension_prioritaria]
        
        return {
            "dimension_prioritaria_mes": mes.dimension_prioritaria,
            "dimension_prioritaria_dia": dia.dimension_prioritaria,
            "energia_dominante": dia.energia,
            "practica_integrada": f"{mes.practica_recomendada} + {dia.practica_sugerida}",
            "sesgo_vigilar": dia.alerta_sesgo,
            "mensaje_guia": f"Mes de {mes.cualidad.value}. Día para {dia.intencion}. {mes.ensenanza_mistica}",
            "es_mes_sagrado": mes.es_sagrado
        }

    def obtener_vista_semanal(self, fecha_inicio: Optional[date] = None) -> dict:
        """
        Vista semanal con propósito profundo de cada día.
        
        Para la interfaz de Vista Semanal.
        """
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
                "practica": dia_info.practica_sugerida,
                "alerta_sesgo": dia_info.alerta_sesgo
            })
        
        mes_actual = self.obtener_mes_actual(lunes)
        
        return {
            "semana_inicio": lunes.isoformat(),
            "mes_hijri": mes_actual.nombre_arabe,
            "cualidad_mes": mes_actual.cualidad.value,
            "ensenanza_mes": mes_actual.ensenanza_mistica,
            "dias": semana
        }

    def obtener_vista_mensual(self, fecha: Optional[date] = None) -> dict:
        """
        Vista mensual con significado litúrgico completo.
        
        Para la interfaz de Vista Mensual.
        """
        fecha = fecha or date.today()
        mes_hijri = self.obtener_mes_actual(fecha)
        
        # Obtener fecha Hijri completa
        hijri = hijri_converter.Gregorian(fecha.year, fecha.month, fecha.day).to_hijri()
        
        return {
            "año_hijri": hijri.year,
            "mes_numero": mes_hijri.numero,
            "nombre": mes_hijri.nombre_arabe,
            "nombre_es": mes_hijri.nombre_es,
            "significado": mes_hijri.significado,
            "cualidad": mes_hijri.cualidad.value,
            "es_sagrado": mes_hijri.es_sagrado,
            "ensenanza": mes_hijri.ensenanza_mistica,
            "practica": mes_hijri.practica_recomendada,
            "dimension": mes_hijri.dimension_prioritaria,
            "simbolo": mes_hijri.simbolo,
            "color": mes_hijri.color,
            "ayat": mes_hijri.ayat_clave
        }

    def obtener_vista_anual(self, fecha: Optional[date] = None) -> dict:
        """
        Vista anual completa con los 12 meses y sus significados.
        
        Para la interfaz de Vista Anual.
        """
        fecha = fecha or date.today()
        hijri = hijri_converter.Gregorian(fecha.year, fecha.month, fecha.day).to_hijri()
        
        return {
            "año_hijri": hijri.year,
            "año_gregoriano": fecha.year,
            "meses": [
                {
                    "numero": m.numero,
                    "nombre": m.nombre_arabe,
                    "nombre_es": m.nombre_es,
                    "cualidad": m.cualidad.value,
                    "es_sagrado": m.es_sagrado,
                    "dimension": m.dimension_prioritaria,
                    "simbolo": m.simbolo,
                    "color": m.color,
                    "ensenanza_breve": m.ensenanza_mistica[:100] + "..."
                }
                for m in self.meses_hijri
            ],
            "meses_sagrados": [1, 7, 11, 12],
            "ciclo_completo": "12 meses lunares (~354 días)",
            "ensenanza_anual": "El ciclo completo es un viaje del alma: desde el silencio sagrado de Muharram hasta la entrega total en Dhu al-Hijjah, para renacer de nuevo en el siguiente Muharram. Un viaje hacia el centro (الكعبة) de tu ser."
        }
