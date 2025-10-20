"""
🔍 AUDITORÍA FUNCIONAL - Sistema 7 Capas

Valida:
1. Integridad estructural de cada capa
2. Coherencia entre capas
3. Detección de capas activas
4. Pipeline completo de generación
5. Manejo de errores y fallbacks

Principio: "Confianza radical en el organismo"
"""

import sys
from pathlib import Path
from datetime import datetime, time
from typing import Dict, List, Tuple

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# === IMPORTS ===
from services.calculador_cosmico import CalculadorCosmico
from models.estado_biologico import EstadoBiologico, NivelEnergia, CalidadSueno, ResonanciaCorporal
from models.contexto_social import ContextoSocial, NoNegociable, Proyecto, TensionSocial, TipoNoNegociable, EstadoProyecto
from models.diseno_humano import crear_diseno_daniel
from models.estado_emocional import EstadoEmocional, EstadoEmocionalTipo, TendenciaEmocional
from models.tipologia_cognitiva import crear_perfil_entp_5w4
from services.orquestador_7_capas import Orquestador7Capas


class AuditoriaFuncional:
    """Auditor del sistema completo"""

    def __init__(self):
        self.orquestador = Orquestador7Capas()
        self.errores = []
        self.warnings = []
        self.exitos = []

    def log_exito(self, capa: str, test: str):
        """Registra test exitoso"""
        self.exitos.append(f"✅ {capa}: {test}")

    def log_warning(self, capa: str, test: str, detalle: str):
        """Registra warning"""
        self.warnings.append(f"⚠️ {capa}: {test} - {detalle}")

    def log_error(self, capa: str, test: str, detalle: str):
        """Registra error"""
        self.errores.append(f"❌ {capa}: {test} - {detalle}")

    # === AUDITORÍA CAPA 1: FÍSICA/LITÚRGICA ===

    def auditar_capa_1_fisica(self) -> Dict:
        """Audita Capa 1 (Física/Litúrgica)"""
        print("\n📍 CAPA 1: FÍSICA/LITÚRGICA")
        print("=" * 70)

        resultado = {"capa": "1_fisica", "tests": []}

        # Test 1: Validar momentos litúrgicos
        momentos_validos = ["fajr", "dhuhr", "asr", "maghrib", "isha"]
        for momento in momentos_validos:
            try:
                contexto = self.orquestador.recopilar_capa_1_fisica(
                    momento=momento,
                    fecha_hora=datetime.now()
                )

                if contexto["momento"] == momento:
                    self.log_exito("Capa 1", f"Momento {momento} procesado correctamente")
                else:
                    self.log_error("Capa 1", f"Momento {momento}", f"Expected {momento}, got {contexto['momento']}")

                resultado["tests"].append({"momento": momento, "status": "ok"})

            except Exception as e:
                self.log_error("Capa 1", f"Momento {momento}", str(e))
                resultado["tests"].append({"momento": momento, "status": "error", "detalle": str(e)})

        # Test 2: Validar estructura de datos
        contexto = self.orquestador.recopilar_capa_1_fisica("fajr", datetime.now())
        campos_esperados = ["momento", "descripcion", "horario_aproximado", "fecha_hora", "timestamp", "activa"]

        for campo in campos_esperados:
            if campo in contexto:
                self.log_exito("Capa 1", f"Campo '{campo}' presente")
            else:
                self.log_error("Capa 1", "Estructura", f"Falta campo '{campo}'")

        # Test 3: Validar que siempre está activa
        if contexto.get("activa") == True:
            self.log_exito("Capa 1", "Capa siempre activa (correcto)")
        else:
            self.log_error("Capa 1", "Activación", "Capa 1 debe estar siempre activa")

        return resultado

    # === AUDITORÍA CAPA 2: SOCIAL ===

    def auditar_capa_2_social(self) -> Dict:
        """Audita Capa 2 (Social/Relacional)"""
        print("\n🤝 CAPA 2: SOCIAL/RELACIONAL")
        print("=" * 70)

        resultado = {"capa": "2_social", "tests": []}

        # Test 1: Crear contexto vacío (debería funcionar)
        try:
            contexto_vacio = ContextoSocial()
            if not contexto_vacio.esta_activa():
                self.log_exito("Capa 2", "Contexto vacío correctamente inactivo")
            else:
                self.log_warning("Capa 2", "Contexto vacío", "Debería estar inactivo")

            resultado["tests"].append({"test": "contexto_vacio", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 2", "Contexto vacío", str(e))
            resultado["tests"].append({"test": "contexto_vacio", "status": "error"})

        # Test 2: Crear no-negociable válido
        try:
            nn = NoNegociable(
                nombre="Test",
                tipo=TipoNoNegociable.BIOLOGICO,
                dias_semana=["lunes"],
                duracion_minutos=30,
                prioridad=3
            )
            self.log_exito("Capa 2", "NoNegociable creado correctamente")
            resultado["tests"].append({"test": "no_negociable", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 2", "NoNegociable", str(e))
            resultado["tests"].append({"test": "no_negociable", "status": "error"})

        # Test 3: Crear proyecto válido
        try:
            proy = Proyecto(
                nombre="Test MVP",
                tipo="código",
                estado=EstadoProyecto.ACTIVO,
                prioridad=5
            )
            self.log_exito("Capa 2", "Proyecto creado correctamente")
            resultado["tests"].append({"test": "proyecto", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 2", "Proyecto", str(e))
            resultado["tests"].append({"test": "proyecto", "status": "error"})

        # Test 4: Crear tensión social válida
        try:
            tension = TensionSocial(
                descripcion="Test tensión",
                ambito="trabajo",
                intensidad=4
            )
            self.log_exito("Capa 2", "TensionSocial creada correctamente")
            resultado["tests"].append({"test": "tension", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 2", "TensionSocial", str(e))
            resultado["tests"].append({"test": "tension", "status": "error"})

        # Test 5: Contexto con datos (debe activarse)
        try:
            contexto_activo = ContextoSocial(
                no_negociables_hoy=[nn],
                proyectos_activos=[proy]
            )

            if contexto_activo.esta_activa():
                self.log_exito("Capa 2", "Contexto con datos correctamente activo")
            else:
                self.log_error("Capa 2", "Activación", "Contexto con proyectos debería estar activo")

            sintesis = contexto_activo.generar_sintesis()
            if len(sintesis) > 0:
                self.log_exito("Capa 2", f"Síntesis generada: '{sintesis}'")

            resultado["tests"].append({"test": "contexto_activo", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 2", "Contexto activo", str(e))
            resultado["tests"].append({"test": "contexto_activo", "status": "error"})

        # Test 6: Integración con orquestador
        try:
            contexto_orq = self.orquestador.recopilar_capa_2_social(datetime.now())
            campos_esperados = ["no_negociables_hoy", "proyectos_activos", "tensiones_actuales", "sintesis", "activa"]

            for campo in campos_esperados:
                if campo in contexto_orq:
                    self.log_exito("Capa 2", f"Orquestador: campo '{campo}' presente")
                else:
                    self.log_error("Capa 2", "Orquestador", f"Falta campo '{campo}'")

            resultado["tests"].append({"test": "orquestador", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 2", "Orquestador", str(e))
            resultado["tests"].append({"test": "orquestador", "status": "error"})

        return resultado

    # === AUDITORÍA CAPA 3: BIOLÓGICA ===

    def auditar_capa_3_biologica(self) -> Dict:
        """Audita Capa 3 (Biológica)"""
        print("\n🧬 CAPA 3: BIOLÓGICA")
        print("=" * 70)

        resultado = {"capa": "3_biologica", "tests": []}

        # Test 1: Crear estado con mínima energía
        try:
            estado_bajo = EstadoBiologico(
                energia=NivelEnergia.MUY_BAJO,
                calidad_sueno=CalidadSueno.MALO,
                resonancia_corporal=ResonanciaCorporal.TENSION
            )

            score = estado_bajo.calcular_score_vitalidad()
            if score <= 3.0:
                self.log_exito("Capa 3", f"Estado bajo: score={score} (correcto)")
            else:
                self.log_warning("Capa 3", "Score bajo", f"Esperado <=3.0, obtenido {score}")

            if estado_bajo.esta_activa():
                self.log_exito("Capa 3", "Estado bajo correctamente marca capa como activa")
            else:
                self.log_error("Capa 3", "Activación", "Estado bajo debería activar la capa")

            resultado["tests"].append({"test": "estado_bajo", "status": "ok", "score": score})
        except Exception as e:
            self.log_error("Capa 3", "Estado bajo", str(e))
            resultado["tests"].append({"test": "estado_bajo", "status": "error"})

        # Test 2: Crear estado con máxima energía
        try:
            estado_alto = EstadoBiologico(
                energia=NivelEnergia.MUY_ALTO,
                calidad_sueno=CalidadSueno.EXCELENTE,
                resonancia_corporal=ResonanciaCorporal.VIBRANTE
            )

            score = estado_alto.calcular_score_vitalidad()
            if score >= 8.0:
                self.log_exito("Capa 3", f"Estado alto: score={score} (correcto)")
            else:
                self.log_warning("Capa 3", "Score alto", f"Esperado >=8.0, obtenido {score}")

            if estado_alto.esta_activa():
                self.log_exito("Capa 3", "Estado alto correctamente marca capa como activa")
            else:
                self.log_error("Capa 3", "Activación", "Estado alto debería activar la capa")

            resultado["tests"].append({"test": "estado_alto", "status": "ok", "score": score})
        except Exception as e:
            self.log_error("Capa 3", "Estado alto", str(e))
            resultado["tests"].append({"test": "estado_alto", "status": "error"})

        # Test 3: Validar generación de sugerencias
        try:
            sugerencias = estado_bajo.generar_sugerencias()
            if len(sugerencias) > 0:
                self.log_exito("Capa 3", f"Sugerencias generadas: {len(sugerencias)}")
            else:
                self.log_warning("Capa 3", "Sugerencias", "No se generaron sugerencias para estado bajo")

            resultado["tests"].append({"test": "sugerencias", "status": "ok", "count": len(sugerencias)})
        except Exception as e:
            self.log_error("Capa 3", "Sugerencias", str(e))
            resultado["tests"].append({"test": "sugerencias", "status": "error"})

        # Test 4: Integración con orquestador
        try:
            contexto_orq = self.orquestador.recopilar_capa_3_biologica(
                energia=3,  # Medio
                calidad_sueno=4,  # Buena
                resonancia="neutral"  # El orquestador usa strings, no enums
            )

            campos_esperados = ["energia", "calidad_sueno", "resonancia_corporal", "score_vitalidad", "activa"]

            for campo in campos_esperados:
                if campo in contexto_orq:
                    self.log_exito("Capa 3", f"Orquestador: campo '{campo}' presente")
                else:
                    self.log_error("Capa 3", "Orquestador", f"Falta campo '{campo}'")

            resultado["tests"].append({"test": "orquestador", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 3", "Orquestador", str(e))
            resultado["tests"].append({"test": "orquestador", "status": "error"})

        return resultado

    # === AUDITORÍA CAPA 4: ENERGÉTICA (DISEÑO HUMANO) ===

    def auditar_capa_4_energetica(self) -> Dict:
        """Audita Capa 4 (Energética/Diseño Humano)"""
        print("\n🌟 CAPA 4: ENERGÉTICA (DISEÑO HUMANO)")
        print("=" * 70)

        resultado = {"capa": "4_energetica", "tests": []}

        # Test 1: Crear diseño humano de Daniel
        try:
            dh = crear_diseno_daniel()

            if dh.tipo.value == "Generador":
                self.log_exito("Capa 4", "Diseño Daniel creado: Generador")
            else:
                self.log_error("Capa 4", "Tipo", f"Esperado Generador, obtenido {dh.tipo.value}")

            if dh.autoridad.value == "Sacral":
                self.log_exito("Capa 4", "Autoridad Daniel: Sacral")
            else:
                self.log_error("Capa 4", "Autoridad", f"Esperado Sacral, obtenido {dh.autoridad.value}")

            resultado["tests"].append({"test": "crear_daniel", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 4", "Crear diseño Daniel", str(e))
            resultado["tests"].append({"test": "crear_daniel", "status": "error"})

        # Test 2: Validar tiempo de respuesta Sacral
        try:
            # Sacral: debe ser < 3 segundos
            if dh.validar_tiempo_respuesta(2.0):
                self.log_exito("Capa 4", "Tiempo respuesta 2s: válido para Sacral")
            else:
                self.log_error("Capa 4", "Validación tiempo", "2s debería ser válido para Sacral")

            if not dh.validar_tiempo_respuesta(5.0):
                self.log_exito("Capa 4", "Tiempo respuesta 5s: inválido para Sacral (correcto)")
            else:
                self.log_warning("Capa 4", "Validación tiempo", "5s debería ser inválido para Sacral")

            resultado["tests"].append({"test": "validar_tiempo_respuesta", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 4", "Validar tiempo respuesta", str(e))
            resultado["tests"].append({"test": "validar_tiempo_respuesta", "status": "error"})

        # Test 3: Validar estrategia
        try:
            # Generador debe responder, no iniciar
            if dh.esta_siguiendo_estrategia(respondio_a_algo=True):
                self.log_exito("Capa 4", "Estrategia: respondió a algo (correcto)")
            else:
                self.log_error("Capa 4", "Estrategia", "Generador respondiendo debería seguir estrategia")

            if not dh.esta_siguiendo_estrategia(respondio_a_algo=False):
                self.log_exito("Capa 4", "Estrategia: inició sin responder (incorrecto, detectado)")
            else:
                self.log_warning("Capa 4", "Estrategia", "Generador iniciando debería violar estrategia")

            resultado["tests"].append({"test": "validar_estrategia", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 4", "Validar estrategia", str(e))
            resultado["tests"].append({"test": "validar_estrategia", "status": "error"})

        # Test 4: Generar recordatorio
        try:
            recordatorio = dh.generar_recordatorio()
            if len(recordatorio) > 0:
                self.log_exito("Capa 4", f"Recordatorio generado: '{recordatorio[:50]}...'")
            else:
                self.log_error("Capa 4", "Recordatorio", "Recordatorio vacío")

            resultado["tests"].append({"test": "generar_recordatorio", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 4", "Generar recordatorio", str(e))
            resultado["tests"].append({"test": "generar_recordatorio", "status": "error"})

        # Test 5: Integración con orquestador
        try:
            contexto_orq = self.orquestador.recopilar_capa_4_energetica()

            campos_esperados = ["tipo", "autoridad", "estrategia", "recordatorio", "activa"]

            for campo in campos_esperados:
                if campo in contexto_orq:
                    self.log_exito("Capa 4", f"Orquestador: campo '{campo}' presente")
                else:
                    self.log_error("Capa 4", "Orquestador", f"Falta campo '{campo}'")

            # Capa 4 siempre activa
            if contexto_orq.get("activa") == True:
                self.log_exito("Capa 4", "Orquestador: capa siempre activa (correcto)")
            else:
                self.log_error("Capa 4", "Activación", "Capa 4 debería estar siempre activa")

            resultado["tests"].append({"test": "orquestador", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 4", "Orquestador", str(e))
            resultado["tests"].append({"test": "orquestador", "status": "error"})

        return resultado

    # === AUDITORÍA CAPA 5: EMOCIONAL ===

    def auditar_capa_5_emocional(self) -> Dict:
        """Audita Capa 5 (Emocional/Psicológica)"""
        print("\n💭 CAPA 5: EMOCIONAL/PSICOLÓGICA")
        print("=" * 70)

        resultado = {"capa": "5_emocional", "tests": []}

        # Test 1: Crear estado emocional neutro
        try:
            estado_neutro = EstadoEmocional(
                estado=EstadoEmocionalTipo.NEUTRO,
                intensidad=2,
                tendencia=TendenciaEmocional.ESTABLE
            )

            if not estado_neutro.esta_activo():
                self.log_exito("Capa 5", "Estado neutro bajo intensidad: inactivo (correcto)")
            else:
                self.log_warning("Capa 5", "Estado neutro", "Intensidad 2 neutro debería ser inactivo")

            if not estado_neutro.necesita_atencion():
                self.log_exito("Capa 5", "Estado neutro: no necesita atención")

            resultado["tests"].append({"test": "estado_neutro", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 5", "Estado neutro", str(e))
            resultado["tests"].append({"test": "estado_neutro", "status": "error"})

        # Test 2: Crear estado polarizado (debe activarse)
        try:
            estado_ansioso = EstadoEmocional(
                estado=EstadoEmocionalTipo.ANSIOSO,
                intensidad=4,
                tendencia=TendenciaEmocional.EMPEORANDO
            )

            if estado_ansioso.esta_activo():
                self.log_exito("Capa 5", "Estado ansioso intensidad 4: activo (correcto)")
            else:
                self.log_error("Capa 5", "Activación", "Ansioso intensidad 4 debería estar activo")

            if estado_ansioso.necesita_atencion():
                self.log_exito("Capa 5", "Estado ansioso: necesita atención (correcto)")
            else:
                self.log_error("Capa 5", "Atención", "Ansioso intensidad 4 debería necesitar atención")

            resultado["tests"].append({"test": "estado_polarizado", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 5", "Estado polarizado", str(e))
            resultado["tests"].append({"test": "estado_polarizado", "status": "error"})

        # Test 3: Generar síntesis
        try:
            sintesis = estado_ansioso.generar_sintesis()
            if "ansioso" in sintesis.lower():
                self.log_exito("Capa 5", f"Síntesis generada: '{sintesis}'")
            else:
                self.log_warning("Capa 5", "Síntesis", f"Debería incluir 'ansioso': '{sintesis}'")

            resultado["tests"].append({"test": "generar_sintesis", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 5", "Generar síntesis", str(e))
            resultado["tests"].append({"test": "generar_sintesis", "status": "error"})

        # Test 4: Integración con orquestador
        try:
            contexto_orq = self.orquestador.recopilar_capa_5_emocional(
                estado_emocional="entusiasmado",  # El orquestador usa strings
                intensidad=4,  # Parámetro correcto es 'intensidad', no 'intensidad_emocional'
                momento_liturgico="dhuhr",
                usuario_id="test_auditoria"
            )

            campos_esperados = ["estado", "intensidad", "tendencia", "sintesis", "activa", "necesita_atencion"]

            for campo in campos_esperados:
                if campo in contexto_orq:
                    self.log_exito("Capa 5", f"Orquestador: campo '{campo}' presente")
                else:
                    self.log_error("Capa 5", "Orquestador", f"Falta campo '{campo}'")

            resultado["tests"].append({"test": "orquestador", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 5", "Orquestador", str(e))
            resultado["tests"].append({"test": "orquestador", "status": "error"})

        return resultado

    # === AUDITORÍA CAPA 6: MENTAL/COGNITIVA ===

    def auditar_capa_6_mental(self) -> Dict:
        """Audita Capa 6 (Mental/Cognitiva)"""
        print("\n🧠 CAPA 6: MENTAL/COGNITIVA")
        print("=" * 70)

        resultado = {"capa": "6_mental", "tests": []}

        # Test 1: Crear perfil ENTP 5w4
        try:
            perfil = crear_perfil_entp_5w4()

            if perfil.mbti.tipo.value == "ENTP":
                self.log_exito("Capa 6", "Perfil creado: ENTP")
            else:
                self.log_error("Capa 6", "Tipo MBTI", f"Esperado ENTP, obtenido {perfil.mbti.tipo.value}")

            if perfil.eneagrama.tipo_base.value == 5:
                self.log_exito("Capa 6", "Eneagrama: Tipo 5")
            else:
                self.log_error("Capa 6", "Eneagrama", f"Esperado 5, obtenido {perfil.eneagrama.tipo_base.value}")

            resultado["tests"].append({"test": "crear_perfil", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 6", "Crear perfil", str(e))
            resultado["tests"].append({"test": "crear_perfil", "status": "error"})

        # Test 2: Validar stack de funciones ENTP
        try:
            if perfil.mbti.funcion_dominante.value == "Ne":
                self.log_exito("Capa 6", "Función dominante: Ne (correcto)")
            else:
                self.log_error("Capa 6", "Stack funciones", f"Esperado Ne, obtenido {perfil.mbti.funcion_dominante.value}")

            if perfil.mbti.funcion_auxiliar.value == "Ti":
                self.log_exito("Capa 6", "Función auxiliar: Ti (correcto)")
            else:
                self.log_error("Capa 6", "Stack funciones", f"Esperado Ti, obtenido {perfil.mbti.funcion_auxiliar.value}")

            if len(perfil.mbti.sombra) == 4:
                self.log_exito("Capa 6", f"Sombra: 4 funciones (correcto)")
            else:
                self.log_warning("Capa 6", "Sombra", f"Esperado 4 funciones, obtenido {len(perfil.mbti.sombra)}")

            resultado["tests"].append({"test": "stack_funciones", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 6", "Stack funciones", str(e))
            resultado["tests"].append({"test": "stack_funciones", "status": "error"})

        # Test 3: Mapear función activa por hora
        try:
            # Mañana (7:00): Ne dominante
            funcion_manana, _ = perfil.mbti.mapear_funcion_activa(7)
            if funcion_manana.value == "Ne":
                self.log_exito("Capa 6", "Mañana (7h): Ne activa (correcto)")
            else:
                self.log_warning("Capa 6", "Mapeo hora", f"Mañana esperado Ne, obtenido {funcion_manana.value}")

            # Tarde (14:00): Ti auxiliar
            funcion_tarde, _ = perfil.mbti.mapear_funcion_activa(14)
            if funcion_tarde.value == "Ti":
                self.log_exito("Capa 6", "Tarde (14h): Ti activa (correcto)")
            else:
                self.log_warning("Capa 6", "Mapeo hora", f"Tarde esperado Ti, obtenido {funcion_tarde.value}")

            resultado["tests"].append({"test": "mapear_funcion_hora", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 6", "Mapear función hora", str(e))
            resultado["tests"].append({"test": "mapear_funcion_hora", "status": "error"})

        # Test 4: Validar líneas de integración/desintegración
        try:
            if perfil.eneagrama.linea_integracion == 8:
                self.log_exito("Capa 6", "Eneagrama: línea integración 5→8 (correcto)")
            else:
                self.log_error("Capa 6", "Eneagrama", f"Línea integración esperado 8, obtenido {perfil.eneagrama.linea_integracion}")

            if perfil.eneagrama.linea_desintegracion == 7:
                self.log_exito("Capa 6", "Eneagrama: línea desintegración 5→7 (correcto)")
            else:
                self.log_error("Capa 6", "Eneagrama", f"Línea desintegración esperado 7, obtenido {perfil.eneagrama.linea_desintegracion}")

            resultado["tests"].append({"test": "lineas_eneagrama", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 6", "Líneas eneagrama", str(e))
            resultado["tests"].append({"test": "lineas_eneagrama", "status": "error"})

        # Test 5: Integración con orquestador
        try:
            contexto_orq = self.orquestador.recopilar_capa_6_mental(
                fecha_hora=datetime.now(),
                patrones_recientes=[]
            )

            # Fallback devuelve: mbti, funcion_activa, descripcion_funcion, eneagrama, nivel_salud, activa
            campos_esperados = ["funcion_activa", "nivel_salud", "activa"]

            for campo in campos_esperados:
                if campo in contexto_orq:
                    self.log_exito("Capa 6", f"Orquestador: campo '{campo}' presente")
                else:
                    self.log_error("Capa 6", "Orquestador", f"Falta campo '{campo}'")

            # Capa 6 siempre activa
            if contexto_orq.get("activa") == True:
                self.log_exito("Capa 6", "Orquestador: capa siempre activa (correcto)")
            else:
                self.log_error("Capa 6", "Activación", "Capa 6 debería estar siempre activa")

            resultado["tests"].append({"test": "orquestador", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 6", "Orquestador", str(e))
            resultado["tests"].append({"test": "orquestador", "status": "error"})

        return resultado

    # === AUDITORÍA CAPA 7: CÓSMICA ===

    def auditar_capa_7_cosmica(self) -> Dict:
        """Audita Capa 7 (Cósmica/Astronómica)"""
        print("\n🌙 CAPA 7: CÓSMICA/ASTRONÓMICA")
        print("=" * 70)

        resultado = {"capa": "7_cosmica", "tests": []}

        # Test 1: Crear calculador cósmico
        try:
            calculador = CalculadorCosmico()
            self.log_exito("Capa 7", "CalculadorCosmico instanciado")
            resultado["tests"].append({"test": "crear_calculador", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 7", "Crear calculador", str(e))
            resultado["tests"].append({"test": "crear_calculador", "status": "error"})
            return resultado

        # Test 2: Calcular fase lunar
        try:
            fase = calculador.calcular_fase_lunar()

            if "fase" in fase and "porcentaje_iluminacion" in fase:
                self.log_exito("Capa 7", f"Fase lunar: {fase['fase']} ({fase['porcentaje_iluminacion']:.1f}%)")
            else:
                self.log_error("Capa 7", "Fase lunar", "Faltan campos en resultado")

            if 0 <= fase["porcentaje_iluminacion"] <= 100:
                self.log_exito("Capa 7", "Iluminación lunar: rango válido 0-100%")
            else:
                self.log_error("Capa 7", "Iluminación", f"Valor fuera de rango: {fase['porcentaje_iluminacion']}")

            resultado["tests"].append({"test": "calcular_fase_lunar", "status": "ok", "fase": fase["fase"]})
        except Exception as e:
            self.log_error("Capa 7", "Calcular fase lunar", str(e))
            resultado["tests"].append({"test": "calcular_fase_lunar", "status": "error"})

        # Test 3: Calcular hora planetaria
        try:
            hora = calculador.calcular_hora_planetaria()

            planetas_validos = ["Sol", "Luna", "Marte", "Mercurio", "Júpiter", "Venus", "Saturno"]

            if hora["planeta"] in planetas_validos:
                self.log_exito("Capa 7", f"Hora planetaria: {hora['planeta']} (válido)")
            else:
                self.log_error("Capa 7", "Hora planetaria", f"Planeta inválido: {hora['planeta']}")

            if "cualidad" in hora:
                self.log_exito("Capa 7", f"Cualidad: {hora['cualidad']}")

            resultado["tests"].append({"test": "calcular_hora_planetaria", "status": "ok", "planeta": hora["planeta"]})
        except Exception as e:
            self.log_error("Capa 7", "Calcular hora planetaria", str(e))
            resultado["tests"].append({"test": "calcular_hora_planetaria", "status": "error"})

        # Test 4: Calcular posición solar
        try:
            sol = calculador.calcular_posicion_solar()

            signos_validos = [
                "Aries", "Tauro", "Géminis", "Cáncer", "Leo", "Virgo",
                "Libra", "Escorpio", "Sagitario", "Capricornio", "Acuario", "Piscis"
            ]

            if sol["signo"] in signos_validos:
                self.log_exito("Capa 7", f"Posición solar: {sol['signo']} (válido)")
            else:
                self.log_error("Capa 7", "Posición solar", f"Signo inválido: {sol['signo']}")

            if "elemento" in sol and "cualidad" in sol:
                self.log_exito("Capa 7", f"Elemento: {sol['elemento']}, Cualidad: {sol['cualidad']}")

            resultado["tests"].append({"test": "calcular_posicion_solar", "status": "ok", "signo": sol["signo"]})
        except Exception as e:
            self.log_error("Capa 7", "Calcular posición solar", str(e))
            resultado["tests"].append({"test": "calcular_posicion_solar", "status": "error"})

        # Test 5: Contexto completo
        try:
            contexto = calculador.calcular_contexto_completo()

            if "fase_lunar" in contexto and "hora_planetaria" in contexto and "posicion_solar" in contexto:
                self.log_exito("Capa 7", "Contexto completo: todos los componentes presentes")
            else:
                self.log_error("Capa 7", "Contexto completo", "Faltan componentes")

            resultado["tests"].append({"test": "contexto_completo", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 7", "Contexto completo", str(e))
            resultado["tests"].append({"test": "contexto_completo", "status": "error"})

        # Test 6: Integración con orquestador
        try:
            contexto_orq = self.orquestador.recopilar_capa_7_cosmica(datetime.now())

            campos_esperados = ["fase_lunar", "hora_planetaria", "posicion_solar", "activa"]

            for campo in campos_esperados:
                if campo in contexto_orq:
                    self.log_exito("Capa 7", f"Orquestador: campo '{campo}' presente")
                else:
                    self.log_error("Capa 7", "Orquestador", f"Falta campo '{campo}'")

            resultado["tests"].append({"test": "orquestador", "status": "ok"})
        except Exception as e:
            self.log_error("Capa 7", "Orquestador", str(e))
            resultado["tests"].append({"test": "orquestador", "status": "error"})

        return resultado

    # === AUDITORÍA DE COHERENCIA ENTRE CAPAS ===

    def auditar_coherencia_entre_capas(self) -> Dict:
        """Audita coherencia e interacciones entre capas"""
        print("\n🔗 COHERENCIA ENTRE CAPAS")
        print("=" * 70)

        resultado = {"tests": []}

        # Test 1: Recopilar todas las capas simultáneamente
        try:
            contexto_completo = self.orquestador.recopilar_todo(
                momento="dhuhr",
                usuario_id="test_coherencia",
                energia=4,  # Alto
                calidad_sueno=4,  # Buena
                resonancia_corporal="fluido",  # String, no Enum
                estado_emocional="entusiasmado",  # String, no Enum
                intensidad_emocional=4
            )

            if "capas" in contexto_completo:
                self.log_exito("Coherencia", "Contexto completo: campo 'capas' presente")
            else:
                self.log_error("Coherencia", "Estructura", "Falta campo 'capas'")

            if len(contexto_completo["capas"]) == 7:
                self.log_exito("Coherencia", "7 capas recopiladas simultáneamente")
            else:
                self.log_error("Coherencia", "Capas", f"Esperado 7, obtenido {len(contexto_completo['capas'])}")

            resultado["tests"].append({"test": "recopilar_todas", "status": "ok", "capas_count": len(contexto_completo["capas"])})
        except Exception as e:
            self.log_error("Coherencia", "Recopilar todas", str(e))
            resultado["tests"].append({"test": "recopilar_todas", "status": "error"})

        # Test 2: Identificar capas activas
        try:
            if "capas_activas" in contexto_completo:
                capas_activas = contexto_completo["capas_activas"]
                self.log_exito("Coherencia", f"Capas activas identificadas: {len(capas_activas)}")

                for capa in capas_activas:
                    self.log_exito("Coherencia", f"  → {capa}")

                # Validar que capas que deben estar activas lo estén
                if "1_fisica" in capas_activas:
                    self.log_exito("Coherencia", "Capa 1 (Física) siempre activa ✓")
                else:
                    self.log_error("Coherencia", "Activación", "Capa 1 debería estar siempre activa")

                if "4_energetica" in capas_activas:
                    self.log_exito("Coherencia", "Capa 4 (Energética) siempre activa ✓")
                else:
                    self.log_error("Coherencia", "Activación", "Capa 4 debería estar siempre activa")

                if "6_mental" in capas_activas:
                    self.log_exito("Coherencia", "Capa 6 (Mental) siempre activa ✓")
                else:
                    self.log_error("Coherencia", "Activación", "Capa 6 debería estar siempre activa")

            resultado["tests"].append({"test": "capas_activas", "status": "ok", "count": len(capas_activas)})
        except Exception as e:
            self.log_error("Coherencia", "Capas activas", str(e))
            resultado["tests"].append({"test": "capas_activas", "status": "error"})

        # Test 3: Generar narrativa de síntesis
        try:
            if "narrativa" in contexto_completo:
                narrativa = contexto_completo["narrativa"]
                self.log_exito("Coherencia", f"Narrativa generada: '{narrativa[:100]}...'")

                if len(narrativa) > 50:
                    self.log_exito("Coherencia", "Narrativa: longitud adecuada")
                else:
                    self.log_warning("Coherencia", "Narrativa", "Parece demasiado corta")

            resultado["tests"].append({"test": "narrativa", "status": "ok"})
        except Exception as e:
            self.log_error("Coherencia", "Narrativa", str(e))
            resultado["tests"].append({"test": "narrativa", "status": "error"})

        # Test 4: Validar que capas inactivas no interfieren
        try:
            # Crear contexto con biología baja (debería marcar capa 3 como inactiva)
            contexto_bajo = self.orquestador.recopilar_todo(
                momento="fajr",
                usuario_id="test_coherencia",
                energia=3,  # Medio
                calidad_sueno=3,  # Regular
                resonancia_corporal="neutral",  # String
                estado_emocional="neutro",  # String
                intensidad_emocional=2
            )

            capa_3 = contexto_bajo["capas"]["3_biologica"]

            # Biología media/regular no debería activar capa
            if not capa_3.get("activa", False):
                self.log_exito("Coherencia", "Capa 3 inactiva con valores medios (correcto)")
            else:
                self.log_warning("Coherencia", "Capa 3", "Valores medios deberían dejar capa inactiva")

            resultado["tests"].append({"test": "capas_inactivas", "status": "ok"})
        except Exception as e:
            self.log_error("Coherencia", "Capas inactivas", str(e))
            resultado["tests"].append({"test": "capas_inactivas", "status": "error"})

        return resultado

    # === AUDITORÍA DE MANEJO DE ERRORES ===

    def auditar_manejo_errores(self) -> Dict:
        """Audita robustez del sistema ante errores"""
        print("\n🛡️ MANEJO DE ERRORES Y FALLBACKS")
        print("=" * 70)

        resultado = {"tests": []}

        # Test 1: Orquestador con inputs inválidos
        try:
            contexto_invalido = self.orquestador.recopilar_todo(
                momento="momento_invalido",  # momento inválido
                usuario_id="test_errores"
            )

            # Sistema debería degradar gracefully
            if "capas" in contexto_invalido:
                self.log_exito("Errores", "Sistema degradó gracefully con momento inválido")
            else:
                self.log_error("Errores", "Degradación", "Sistema falló completamente")

            resultado["tests"].append({"test": "momento_invalido", "status": "ok"})
        except Exception as e:
            self.log_warning("Errores", "Momento inválido", f"Excepción lanzada: {str(e)[:50]}")
            resultado["tests"].append({"test": "momento_invalido", "status": "warning"})

        # Test 2: Capa biológica con valores None
        try:
            contexto_none = self.orquestador.recopilar_capa_3_biologica(
                energia=None,  # None
                calidad_sueno=None,
                resonancia_corporal=None
            )

            if "energia" in contexto_none:
                self.log_exito("Errores", "Capa 3 maneja None con fallback")
            else:
                self.log_warning("Errores", "Capa 3", "No maneja None correctamente")

            resultado["tests"].append({"test": "valores_none", "status": "ok"})
        except Exception as e:
            self.log_warning("Errores", "Valores None", f"Excepción: {str(e)[:50]}")
            resultado["tests"].append({"test": "valores_none", "status": "warning"})

        # Test 3: Usuario inexistente (tracker emocional)
        try:
            contexto_usuario_nuevo = self.orquestador.recopilar_capa_5_emocional(
                estado_emocional="calma",  # String, no Enum
                intensidad=3,  # Parámetro correcto
                momento_liturgico="fajr",
                usuario_id="usuario_que_no_existe_12345"
            )

            # Debería crear nuevo tracker sin errores
            if "estado" in contexto_usuario_nuevo:
                self.log_exito("Errores", "Tracker emocional crea nuevo usuario sin error")
            else:
                self.log_error("Errores", "Tracker", "Falla con usuario nuevo")

            resultado["tests"].append({"test": "usuario_inexistente", "status": "ok"})
        except Exception as e:
            self.log_warning("Errores", "Usuario inexistente", str(e))
            resultado["tests"].append({"test": "usuario_inexistente", "status": "warning"})

        return resultado

    # === EJECUCIÓN COMPLETA ===

    def ejecutar_auditoria_completa(self):
        """Ejecuta auditoría completa del sistema"""
        print("\n" + "="*70)
        print("🔍 AUDITORÍA FUNCIONAL - SISTEMA 7 CAPAS")
        print("="*70)
        print("\nValidando integridad, coherencia, y robustez...")
        print("\n")

        resultados = {}

        # Auditar cada capa
        resultados["capa_1"] = self.auditar_capa_1_fisica()
        resultados["capa_2"] = self.auditar_capa_2_social()
        resultados["capa_3"] = self.auditar_capa_3_biologica()
        resultados["capa_4"] = self.auditar_capa_4_energetica()
        resultados["capa_5"] = self.auditar_capa_5_emocional()
        resultados["capa_6"] = self.auditar_capa_6_mental()
        resultados["capa_7"] = self.auditar_capa_7_cosmica()

        # Auditar coherencia
        resultados["coherencia"] = self.auditar_coherencia_entre_capas()

        # Auditar manejo de errores
        resultados["errores"] = self.auditar_manejo_errores()

        # === REPORTE FINAL ===
        self.generar_reporte_final(resultados)

        return resultados

    def generar_reporte_final(self, resultados: Dict):
        """Genera reporte final de auditoría"""
        print("\n\n" + "="*70)
        print("📊 REPORTE FINAL DE AUDITORÍA")
        print("="*70)

        # Contadores
        total_exitos = len(self.exitos)
        total_warnings = len(self.warnings)
        total_errores = len(self.errores)
        total_tests = total_exitos + total_warnings + total_errores

        print(f"\n📈 ESTADÍSTICAS:")
        print(f"   Total tests ejecutados: {total_tests}")
        print(f"   ✅ Exitosos: {total_exitos} ({100*total_exitos/total_tests if total_tests > 0 else 0:.1f}%)")
        print(f"   ⚠️ Warnings: {total_warnings} ({100*total_warnings/total_tests if total_tests > 0 else 0:.1f}%)")
        print(f"   ❌ Errores: {total_errores} ({100*total_errores/total_tests if total_tests > 0 else 0:.1f}%)")

        # Errores críticos
        if total_errores > 0:
            print(f"\n\n❌ ERRORES CRÍTICOS ({total_errores}):")
            print("-" * 70)
            for error in self.errores:
                print(f"   {error}")

        # Warnings
        if total_warnings > 0:
            print(f"\n\n⚠️ WARNINGS ({total_warnings}):")
            print("-" * 70)
            for warning in self.warnings:
                print(f"   {warning}")

        # Diagnóstico final
        print("\n\n" + "="*70)

        if total_errores == 0 and total_warnings == 0:
            print("🎉 SISTEMA 100% FUNCIONAL")
            print("\nTodas las capas operan correctamente.")
            print("El organismo está coherente y robusto.")
            print("\n✅ LISTO PARA INTEGRACIÓN EN API (DÍA 6)")
        elif total_errores == 0:
            print("✅ SISTEMA FUNCIONAL CON OBSERVACIONES")
            print(f"\n{total_warnings} warnings detectados (no críticos).")
            print("El organismo es funcional pero requiere afinación.")
            print("\n⚠️ REVISAR WARNINGS ANTES DE CONTINUAR")
        else:
            print("⚠️ SISTEMA REQUIERE CORRECCIONES")
            print(f"\n{total_errores} errores críticos detectados.")
            print("El organismo requiere ajustes antes de continuar.")
            print("\n❌ CORREGIR ERRORES ANTES DE DÍA 6")

        print("="*70)


if __name__ == "__main__":
    auditoria = AuditoriaFuncional()
    resultados = auditoria.ejecutar_auditoria_completa()
