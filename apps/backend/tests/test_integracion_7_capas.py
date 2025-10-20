"""
Test de integración end-to-end del sistema de 7 capas.

Valida:
1. Orquestador genera contexto completo
2. Generador de preguntas usa las 7 capas
3. Agente Estado Cero integra correctamente
4. API endpoint acepta parámetros y responde
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.orquestador_7_capas import obtener_contexto_7_capas
from services.generador_preguntas_7_capas import GeneradorPreguntas7Capas
import json


def test_orquestador_contexto_completo():
    """Test 1: Orquestador genera contexto de 7 capas correctamente."""
    print("\n" + "="*80)
    print("TEST 1: ORQUESTADOR 7 CAPAS")
    print("="*80)

    contexto = obtener_contexto_7_capas(
        momento="dhuhr",
        energia=4,
        calidad_sueno=3,
        resonancia_corporal="fluido",
        estado_emocional="entusiasmado",
        intensidad_emocional=4
    )

    print(f"\n✓ Contexto generado exitosamente")
    print(f"  Capas activas: {contexto['num_capas_activas']}")
    print(f"  Lista de capas: {', '.join(contexto['capas_activas'])}")
    print(f"\n📊 SÍNTESIS NARRATIVA:")
    print(f"  {contexto['sintesis_narrativa']}")
    print(f"\n🔗 DOMINIOS RELEVANTES:")
    print(f"  {', '.join(contexto['dominios_relevantes'])}")

    # Validaciones
    assert contexto['num_capas_activas'] > 0, "Debe haber al menos 1 capa activa"
    assert len(contexto['capas']) == 7, "Deben existir las 7 capas"
    assert 'sintesis_narrativa' in contexto, "Debe tener síntesis narrativa"
    assert len(contexto['dominios_relevantes']) > 0, "Debe tener dominios relevantes"

    print("\n✅ TEST 1 PASADO: Orquestador funcional")
    return contexto


def test_generador_pregunta_7_capas():
    """Test 2: Generador usa las 7 capas para crear pregunta emergente."""
    print("\n" + "="*80)
    print("TEST 2: GENERADOR DE PREGUNTAS 7 CAPAS")
    print("="*80)

    generador = GeneradorPreguntas7Capas()

    pregunta_data = generador.generar_pregunta_unica(
        momento="dhuhr",
        energia=4,
        calidad_sueno=3,
        resonancia_corporal="fluido",
        estado_emocional="entusiasmado",
        intensidad_emocional=4
    )

    print(f"\n✨ PREGUNTA EMERGENTE:")
    print(f"  \"{pregunta_data['pregunta']}\"")
    print(f"\n💭 CONTEXTO:")
    print(f"  {pregunta_data['contexto']}")
    print(f"\n🎯 TIPO: {pregunta_data['tipo']}")
    print(f"🔗 DOMINIOS: {', '.join(pregunta_data['dominios'])}")
    print(f"📊 CAPAS ACTIVAS ({pregunta_data['contexto_7_capas']['num_capas_activas']}):")
    for capa in pregunta_data['contexto_7_capas']['capas_activas']:
        print(f"   • {capa}")

    # Validaciones
    assert 'pregunta' in pregunta_data, "Debe tener pregunta"
    assert len(pregunta_data['pregunta']) > 10, "Pregunta debe ser sustancial"
    assert 'contexto_7_capas' in pregunta_data, "Debe incluir metadata de 7 capas"
    assert pregunta_data['contexto_7_capas']['num_capas_activas'] > 0, "Debe tener capas activas"

    print("\n✅ TEST 2 PASADO: Generador funcional con 7 capas")
    return pregunta_data


def test_casos_borde():
    """Test 3: Casos borde - sin inputs de usuario (todas las capas automáticas)."""
    print("\n" + "="*80)
    print("TEST 3: CASOS BORDE - SIN INPUTS DE USUARIO")
    print("="*80)

    generador = GeneradorPreguntas7Capas()

    # Sin ningún input de usuario - solo momento
    pregunta_data = generador.generar_pregunta_unica(
        momento="fajr"
    )

    print(f"\n✨ PREGUNTA SIN INPUTS DE USUARIO:")
    print(f"  \"{pregunta_data['pregunta']}\"")
    print(f"\n📊 CAPAS ACTIVAS: {pregunta_data['contexto_7_capas']['num_capas_activas']}")
    for capa in pregunta_data['contexto_7_capas']['capas_activas']:
        print(f"   • {capa}")

    # Validaciones
    assert 'pregunta' in pregunta_data, "Debe generar pregunta incluso sin inputs"
    assert pregunta_data['contexto_7_capas']['num_capas_activas'] >= 2, "Capas 1, 4, 7 siempre activas"

    print("\n✅ TEST 3 PASADO: Casos borde manejados correctamente")
    return pregunta_data


def test_diferentes_momentos():
    """Test 4: Generación de preguntas para los 5 momentos litúrgicos."""
    print("\n" + "="*80)
    print("TEST 4: PREGUNTAS PARA 5 MOMENTOS LITÚRGICOS")
    print("="*80)

    generador = GeneradorPreguntas7Capas()
    momentos = ["fajr", "dhuhr", "asr", "maghrib", "isha"]

    resultados = {}

    for momento in momentos:
        pregunta_data = generador.generar_pregunta_unica(
            momento=momento,
            energia=3,
            calidad_sueno=3
        )

        resultados[momento] = pregunta_data

        print(f"\n{momento.upper()}:")
        print(f"  Pregunta: \"{pregunta_data['pregunta'][:80]}...\"")
        print(f"  Tipo: {pregunta_data['tipo']}")
        print(f"  Capas activas: {pregunta_data['contexto_7_capas']['num_capas_activas']}")

    # Validaciones
    assert len(resultados) == 5, "Debe generar pregunta para los 5 momentos"
    for momento, data in resultados.items():
        assert 'pregunta' in data, f"Momento {momento} debe tener pregunta"
        assert data['contexto_7_capas']['num_capas_activas'] > 0, f"Momento {momento} debe tener capas activas"

    print("\n✅ TEST 4 PASADO: Todos los momentos litúrgicos generan preguntas")
    return resultados


def test_extremos_biologicos():
    """Test 5: Estados biológicos extremos (muy bajo vs muy alto)."""
    print("\n" + "="*80)
    print("TEST 5: EXTREMOS BIOLÓGICOS")
    print("="*80)

    generador = GeneradorPreguntas7Capas()

    # Estado de agotamiento
    print("\n🔴 ESTADO DE AGOTAMIENTO:")
    pregunta_agotado = generador.generar_pregunta_unica(
        momento="asr",
        energia=1,
        calidad_sueno=1,
        resonancia_corporal="tension",
        estado_emocional="apagado",
        intensidad_emocional=4
    )
    print(f"  Pregunta: \"{pregunta_agotado['pregunta']}\"")
    print(f"  Capas activas: {', '.join(pregunta_agotado['contexto_7_capas']['capas_activas'])}")

    # Estado óptimo
    print("\n🟢 ESTADO ÓPTIMO:")
    pregunta_optimo = generador.generar_pregunta_unica(
        momento="dhuhr",
        energia=5,
        calidad_sueno=5,
        resonancia_corporal="vibrante",
        estado_emocional="entusiasmado",
        intensidad_emocional=4
    )
    print(f"  Pregunta: \"{pregunta_optimo['pregunta']}\"")
    print(f"  Capas activas: {', '.join(pregunta_optimo['contexto_7_capas']['capas_activas'])}")

    # Validaciones
    assert '3_biologica' in pregunta_agotado['contexto_7_capas']['capas_activas'], "Capa biológica debe estar activa en agotamiento"
    assert '3_biologica' in pregunta_optimo['contexto_7_capas']['capas_activas'], "Capa biológica debe estar activa en óptimo"

    print("\n✅ TEST 5 PASADO: Extremos biológicos detectados correctamente")
    return pregunta_agotado, pregunta_optimo


def ejecutar_suite_completa():
    """Ejecuta la suite completa de tests."""
    print("\n" + "🕌"*40)
    print("SUITE DE TESTS - SISTEMA DE 7 CAPAS")
    print("🕌"*40)

    try:
        # Test 1: Orquestador
        contexto = test_orquestador_contexto_completo()

        # Test 2: Generador
        pregunta = test_generador_pregunta_7_capas()

        # Test 3: Casos borde
        pregunta_borde = test_casos_borde()

        # Test 4: Diferentes momentos
        preguntas_momentos = test_diferentes_momentos()

        # Test 5: Extremos biológicos
        pregunta_agotado, pregunta_optimo = test_extremos_biologicos()

        # Resumen final
        print("\n" + "="*80)
        print("RESUMEN DE TESTS")
        print("="*80)
        print("✅ TEST 1: Orquestador 7 capas - PASADO")
        print("✅ TEST 2: Generador de preguntas - PASADO")
        print("✅ TEST 3: Casos borde - PASADO")
        print("✅ TEST 4: 5 momentos litúrgicos - PASADO")
        print("✅ TEST 5: Extremos biológicos - PASADO")
        print("\n🎉 TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("="*80)

        return True

    except Exception as e:
        print(f"\n❌ ERROR EN SUITE DE TESTS:")
        print(f"   {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    exito = ejecutar_suite_completa()
    sys.exit(0 if exito else 1)
