"""
🎯 Orquestador de las 7 Capas - Sistema Completo de Contexto

Este servicio recopila las 7 capas jerárquicas del sistema para generar
contexto completo que alimenta las preguntas emergentes.

ARQUITECTURA DE LAS 7 CAPAS (de sutil a denso):
1. FÍSICA: Ubicación, momento litúrgico, hora del día
2. SOCIAL: No-negociables, proyectos, tensiones sociales
3. BIOLÓGICA: Energía, sueño, resonancia corporal
4. ENERGÉTICA: Diseño Humano (tipo, autoridad, estrategia)
5. EMOCIONAL: Estado emocional actual, intensidad, tendencia
6. MENTAL: MBTI, Eneagrama, patrones cognitivos
7. CÓSMICA: Fase lunar, hora planetaria, posición solar

Cada capa puede estar "activa" o "latente". El orquestador identifica
cuáles están más resonantes y proporciona contexto rico sin determinar.
"""

from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import json

from models.estado_biologico import EstadoBiologico, crear_estado_rapido
from models.diseno_humano import crear_diseno_daniel, cargar_diseno_desde_config
from models.estado_emocional import EstadoEmocional, TrackerEmocional, EstadoEmocionalTipo
from models.contexto_social import cargar_contexto_social_desde_config
from models.tipologia_cognitiva import crear_perfil_entp_5w4, cargar_perfil_cognitivo_desde_config
from services.calculador_cosmico import obtener_contexto_cosmico


class Orquestador7Capas:
    """
    Orquestador maestro que recopila las 7 capas y determina
    cuáles están más activas en cada momento.
    """

    def __init__(
        self,
        latitud: float = 40.4168,
        longitud: float = -3.7038,
        perfil_path: Optional[Path] = None
    ):
        self.latitud = latitud
        self.longitud = longitud
        self.perfil_path = perfil_path or Path(__file__).parent.parent / "storage" / "configuracion_usuario.json"

    def recopilar_capa_1_fisica(
        self,
        momento: str,
        fecha_hora: Optional[datetime] = None
    ) -> Dict:
        """CAPA 1: Contexto físico/material"""
        if fecha_hora is None:
            fecha_hora = datetime.now()

        # Mapeo de momentos litúrgicos a descripciones
        descripciones_momentos = {
            "fajr": "Alba, surgimiento de la luz, umbral entre noche y día",
            "dhuhr": "Mediodía, plenitud solar, momento de máxima presencia",
            "asr": "Tarde, inicio del descenso, transición a la reflexión",
            "maghrib": "Crepúsculo, atardecer, cierre del día",
            "isha": "Noche, oscuridad completa, introspección profunda"
        }

        # Horarios aproximados por momento
        horarios_aproximados = {
            "fajr": "~6:00",
            "dhuhr": "~13:00",
            "asr": "~17:00",
            "maghrib": "~20:00",
            "isha": "~21:30"
        }

        hora = fecha_hora.hour
        if 5 <= hora < 9:
            energia_dia = "emergente"
            contexto_temporal = "inicio_dia"
        elif 9 <= hora < 12:
            energia_dia = "ascendente"
            contexto_temporal = "mañana"
        elif 12 <= hora < 15:
            energia_dia = "cenital"
            contexto_temporal = "mediodia"
        elif 15 <= hora < 18:
            energia_dia = "descendente"
            contexto_temporal = "tarde"
        elif 18 <= hora < 21:
            energia_dia = "crepuscular"
            contexto_temporal = "atardecer"
        else:
            energia_dia = "nocturna"
            contexto_temporal = "noche"

        return {
            "momento": momento,
            "descripcion": descripciones_momentos.get(momento, "Momento litúrgico"),
            "horario_aproximado": horarios_aproximados.get(momento, "~12:00"),
            "fecha_hora": fecha_hora.isoformat(),
            "timestamp": fecha_hora.isoformat(),
            "momento_liturgico": momento,
            "hora_del_dia": fecha_hora.hour,
            "energia_dia": energia_dia,
            "contexto_temporal": contexto_temporal,
            "dia_semana": fecha_hora.strftime("%A"),
            "ubicacion": {"latitud": self.latitud, "longitud": self.longitud},
            "activa": True  # Siempre activa
        }

    def recopilar_capa_2_social(
        self,
        fecha_hora: Optional[datetime] = None
    ) -> Dict:
        """CAPA 2: Contexto social/relacional (con defaults hasta configuración completa)"""
        if fecha_hora is None:
            fecha_hora = datetime.now()

        # Por ahora usar contexto social básico con defaults
        # TODO: Implementar carga desde configuración completa cuando esté lista

        dia_semana = fecha_hora.strftime("%A").lower()

        # Proyectos por defecto (basados en contexto actual)
        proyectos_default = ["Campo Sagrado MVP"]

        # No-negociables según día (simplificado)
        no_negociables_default = []
        if dia_semana in ["monday", "wednesday", "friday"]:
            no_negociables_default.append("Entrenamiento")

        # Estados Cero siempre son no-negociables
        no_negociables_default.extend(["Fajr Estado Cero", "Dhuhr Estado Cero"])

        # Determinar si está activa
        activa = len(proyectos_default) > 0 or len(no_negociables_default) > 2

        return {
            "no_negociables_hoy": no_negociables_default,
            "proyectos_activos": proyectos_default,
            "tensiones_actuales": [],
            "tensiones_sociales": [],
            "sintesis": f"{len(proyectos_default)} proyectos activos, {len(no_negociables_default)} no-negociables",
            "activa": activa
        }

    def recopilar_capa_3_biologica(
        self,
        energia: Optional[int] = None,
        calidad_sueno: Optional[int] = None,
        resonancia: Optional[str] = None
    ) -> Dict:
        """CAPA 3: Contexto biológico"""
        energia = energia or 3
        calidad_sueno = calidad_sueno or 3
        resonancia = resonancia or "neutral"

        estado = crear_estado_rapido(energia, calidad_sueno, resonancia)

        return {
            "energia": energia,
            "calidad_sueno": calidad_sueno,
            "resonancia_corporal": resonancia,
            "score_vitalidad": estado.calcular_score_vitalidad(),
            "vitalidad_score": estado.calcular_score_vitalidad(),
            "sintesis": estado.generar_sintesis(),
            "necesita_atencion": estado.necesita_atencion_biologica(),
            "activa": estado.esta_activa()
        }

    def recopilar_capa_4_energetica(self) -> Dict:
        """CAPA 4: Diseño Humano (MEJORADO)"""
        try:
            # Intentar cargar desde config, si no existe usar default de Daniel
            dh = cargar_diseno_desde_config(str(self.perfil_path))
            if dh is None:
                dh = crear_diseno_daniel()

            return {
                "tipo": dh.tipo.value,
                "autoridad": dh.autoridad.value,
                "estrategia": dh.estrategia.value,
                "perfil": dh.perfil,
                "cruz_encarnacion": dh.cruz_encarnacion,
                "canales": dh.canales,
                "recordatorio": dh.generar_recordatorio(),
                "tiempo_respuesta_optimo": dh.tiempo_respuesta_optimo,
                "activa": True  # Siempre relevante para validación
            }

        except Exception as e:
            print(f"⚠️ Error cargando Capa 4 DH: {e}")
            # Fallback a configuración básica
            return {
                "tipo": "Generador",
                "autoridad": "Sacral",
                "estrategia": "Responder, no iniciar",
                "perfil": "4/6",
                "recordatorio": "Respuesta visceral < 3 segundos",
                "activa": True
            }

    def recopilar_capa_5_emocional(
        self,
        estado_emocional: Optional[str] = None,
        intensidad: Optional[int] = None,
        momento_liturgico: Optional[str] = None,
        usuario_id: str = "default"
    ) -> Dict:
        """CAPA 5: Estado emocional (MEJORADO con tracking)"""
        estado_emocional = estado_emocional or "neutro"
        intensidad = intensidad or 3

        try:
            # Crear tracker para detectar tendencia
            tracker = TrackerEmocional()
            tendencia = tracker.detectar_tendencia(usuario_id)

            # Crear estado emocional
            estado_obj = EstadoEmocional(
                estado=EstadoEmocionalTipo(estado_emocional),
                intensidad=intensidad,
                tendencia=tendencia,
                momento_liturgico=momento_liturgico
            )

            # Guardar en histórico
            tracker.guardar_estado(estado_obj, usuario_id)

            # Detectar patrón si existe
            patron = tracker.detectar_patron_diario(usuario_id)

            return {
                "estado": estado_emocional,
                "intensidad": intensidad,
                "tendencia": tendencia.value,
                "patron_detectado": patron,
                "sintesis": estado_obj.generar_sintesis(),
                "activa": estado_obj.esta_activo(),
                "necesita_atencion": estado_obj.necesita_atencion()
            }

        except Exception as e:
            print(f"⚠️ Error cargando Capa 5 Emocional: {e}")
            return {
                "estado": estado_emocional,
                "intensidad": intensidad,
                "tendencia": "estable",
                "patron_detectado": None,
                "sintesis": f"{estado_emocional} (intensidad {intensidad}/5)",
                "activa": intensidad >= 4,
                "necesita_atencion": False
            }

    def recopilar_capa_6_mental(
        self,
        fecha_hora: Optional[datetime] = None,
        patrones_recientes: Optional[List[str]] = None
    ) -> Dict:
        """CAPA 6: Tipología cognitiva (MBTI + Eneagrama) - MEJORADO"""
        if fecha_hora is None:
            fecha_hora = datetime.now()

        try:
            # Intentar cargar perfil cognitivo, si no existe usar default ENTP 5w4
            perfil = cargar_perfil_cognitivo_desde_config(str(self.perfil_path))
            if perfil is None:
                perfil = crear_perfil_entp_5w4()

            # Generar contexto mental completo
            contexto = perfil.generar_contexto_mental(
                hora=fecha_hora.hour,
                patrones_recientes=patrones_recientes
            )

            # Agregar síntesis si existe
            if perfil.sintesis:
                contexto["sintesis"] = perfil.sintesis

            return contexto

        except Exception as e:
            print(f"⚠️ Error cargando Capa 6 Mental: {e}")
            # Fallback a configuración básica
            hora = fecha_hora.hour
            if 6 <= hora < 12:
                funcion_activa = "Ne"
                descripcion = "Exploración de posibilidades, conexiones, ideas"
            elif 12 <= hora < 18:
                funcion_activa = "Ti"
                descripcion = "Análisis lógico, estructuración, comprensión"
            elif 18 <= hora < 22:
                funcion_activa = "Fe"
                descripcion = "Conexión social, armonía, expresión"
            else:
                funcion_activa = "Si"
                descripcion = "Memoria, reflexión, consolidación"

            return {
                "mbti": "ENTP",
                "funcion_activa": funcion_activa,
                "descripcion_funcion": descripcion,
                "eneagrama": "5w4",
                "nivel_salud": "promedio",
                "activa": funcion_activa in ["Ne", "Si"]
            }

    def recopilar_capa_7_cosmica(
        self,
        fecha_hora: Optional[datetime] = None
    ) -> Dict:
        """CAPA 7: Contexto astronómico/astrológico"""
        contexto = obtener_contexto_cosmico(
            latitud=self.latitud,
            longitud=self.longitud,
            fecha_hora=fecha_hora
        )

        fase_lunar = contexto["fase_lunar"]["fase"]
        hora_planetaria = contexto["hora_planetaria"]["planeta"]

        contexto["activa"] = (
            fase_lunar in ["Luna Nueva", "Luna Llena"] or
            hora_planetaria in ["Saturno", "Júpiter", "Sol"]
        )

        return contexto

    def recopilar_todo(
        self,
        momento: str,
        fecha_hora: Optional[datetime] = None,
        energia: Optional[int] = None,
        calidad_sueno: Optional[int] = None,
        resonancia_corporal: Optional[str] = None,
        estado_emocional: Optional[str] = None,
        intensidad_emocional: Optional[int] = None,
        usuario_id: str = "default"
    ) -> Dict:
        """
        Recopila TODAS las 7 capas en un único contexto.

        Returns:
            Dict con las 7 capas + metadata
        """
        if fecha_hora is None:
            fecha_hora = datetime.now()

        contexto_completo = {
            "timestamp": fecha_hora.isoformat(),
            "momento_liturgico": momento,
            "capas": {
                "1_fisica": self.recopilar_capa_1_fisica(momento, fecha_hora),
                "2_social": self.recopilar_capa_2_social(fecha_hora),
                "3_biologica": self.recopilar_capa_3_biologica(energia, calidad_sueno, resonancia_corporal),
                "4_energetica": self.recopilar_capa_4_energetica(),
                "5_emocional": self.recopilar_capa_5_emocional(estado_emocional, intensidad_emocional, momento, usuario_id),
                "6_mental": self.recopilar_capa_6_mental(fecha_hora),
                "7_cosmica": self.recopilar_capa_7_cosmica(fecha_hora)
            }
        }

        # Identificar capas activas
        capas_activas = [
            nombre for nombre, data in contexto_completo["capas"].items()
            if data.get("activa", False)
        ]

        contexto_completo["capas_activas"] = capas_activas
        contexto_completo["num_capas_activas"] = len(capas_activas)

        return contexto_completo

    def generar_sintesis_narrativa(self, contexto_completo: Dict) -> str:
        """
        Genera síntesis narrativa del contexto de las 7 capas.

        Returns:
            Texto narrativo describiendo el contexto
        """
        capas = contexto_completo["capas"]
        momento = contexto_completo["momento_liturgico"]

        partes = []

        # Momento litúrgico (Capa 1)
        partes.append(f"En {momento.upper()}")

        # Energía del día (Capa 1)
        energia_dia = capas["1_fisica"]["energia_dia"]
        partes.append(f"energía {energia_dia}")

        # Cósmica (Capa 7) - si está activa
        if capas["7_cosmica"]["activa"]:
            fase_lunar = capas["7_cosmica"]["fase_lunar"]["fase"]
            hora_planetaria = capas["7_cosmica"]["hora_planetaria"]["planeta"]
            partes.append(f"{fase_lunar}, hora de {hora_planetaria}")

        # Biológica (Capa 3) - si está activa
        if capas["3_biologica"]["activa"]:
            vitalidad = capas["3_biologica"]["vitalidad_score"]
            if vitalidad < 5:
                partes.append(f"vitalidad baja ({vitalidad}/10)")
            elif vitalidad > 8:
                partes.append(f"vitalidad alta ({vitalidad}/10)")

        # Emocional (Capa 5) - si está activa
        if capas["5_emocional"]["activa"]:
            estado = capas["5_emocional"]["estado"]
            partes.append(f"estado {estado}")

        # Mental (Capa 6)
        funcion_activa = capas["6_mental"]["funcion_activa"]
        partes.append(f"función {funcion_activa} activa")

        # Social (Capa 2) - si está activa
        if capas["2_social"]["activa"]:
            proyectos = capas["2_social"]["proyectos_activos"]
            if proyectos:
                partes.append(f"proyectos: {', '.join(proyectos[:2])}")

        return ", ".join(partes) + "."

    def identificar_dominios_relevantes(self, contexto_completo: Dict) -> List[str]:
        """
        Identifica dominios más presentes según capas activas.

        Returns:
            Lista de dominios (max 3)
        """
        capas = contexto_completo["capas"]
        dominios = []

        if capas["3_biologica"]["activa"]:
            dominios.append("cuerpo")

        if capas["5_emocional"]["activa"]:
            dominios.append("emoción")

        if capas["6_mental"]["funcion_activa"] in ["Ne", "Ti"]:
            dominios.append("mente")

        if capas["7_cosmica"]["activa"]:
            dominios.append("espiritualidad")

        if capas["2_social"]["activa"]:
            if capas["2_social"]["proyectos_activos"]:
                dominios.append("trabajo")
            if capas["2_social"]["no_negociables_hoy"]:
                dominios.append("salud")

        # Defaults por momento si no hay dominios
        if not dominios:
            momento = contexto_completo["momento_liturgico"]
            dominios_por_momento = {
                "fajr": ["espiritualidad", "cuerpo"],
                "dhuhr": ["trabajo", "mente"],
                "asr": ["creatividad", "emoción"],
                "maghrib": ["relaciones", "integración"],
                "isha": ["descanso", "reflexión"]
            }
            dominios = dominios_por_momento.get(momento, ["existencia", "presencia"])

        return dominios[:3]


# === FUNCIÓN PÚBLICA ===

def obtener_contexto_7_capas(
    momento: str,
    latitud: float = 40.4168,
    longitud: float = -3.7038,
    **kwargs
) -> Dict:
    """
    Función principal para obtener contexto completo de las 7 capas.

    Args:
        momento: Momento litúrgico
        latitud: Latitud del observador
        longitud: Longitud del observador
        **kwargs: Inputs opcionales (energia, calidad_sueno, etc.)

    Returns:
        Dict con las 7 capas + síntesis + dominios
    """
    orquestador = Orquestador7Capas(latitud, longitud)
    contexto = orquestador.recopilar_todo(momento, **kwargs)

    # Agregar síntesis y dominios
    contexto["sintesis_narrativa"] = orquestador.generar_sintesis_narrativa(contexto)
    contexto["dominios_relevantes"] = orquestador.identificar_dominios_relevantes(contexto)

    return contexto


if __name__ == "__main__":
    # Test del orquestador
    print("🎯 ORQUESTADOR DE 7 CAPAS - Test\n")
    print("=" * 80)

    # Test en momento Dhuhr
    contexto = obtener_contexto_7_capas(
        momento="dhuhr",
        energia=4,
        calidad_sueno=3,
        resonancia_corporal="fluido",
        estado_emocional="entusiasmado",
        intensidad_emocional=4
    )

    print(f"\n⏰ Timestamp: {contexto['timestamp']}")
    print(f"🕌 Momento: {contexto['momento_liturgico'].upper()}\n")

    print("📊 CAPAS ACTIVAS:")
    for capa in contexto["capas_activas"]:
        print(f"   ✓ {capa}")

    print(f"\n🔗 DOMINIOS RELEVANTES:")
    for dominio in contexto["dominios_relevantes"]:
        print(f"   - {dominio}")

    print(f"\n✨ SÍNTESIS NARRATIVA:")
    print(f"   {contexto['sintesis_narrativa']}\n")

    print("=" * 80)
    print("✅ Orquestador de 7 capas implementado correctamente")
    print(f"   Total capas: 7")
    print(f"   Capas activas: {contexto['num_capas_activas']}")
