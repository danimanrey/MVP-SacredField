#!/usr/bin/env python3
"""
🧪 Test del Sistema de Preguntas Emergentes

Prueba el generador en diferentes momentos y contextos para ver
la variedad y calidad de las preguntas generadas.
"""

import sys
from pathlib import Path

# Añadir path del backend
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.generador_preguntas import generar_pregunta_emergente
from datetime import datetime


def print_separator(char="=", length=70):
    print(char * length)


def test_pregunta_por_momento(momento: str):
    """Prueba generación de pregunta para un momento específico"""
    print_separator()
    print(f"🕌 MOMENTO: {momento.upper()}")
    print_separator()

    try:
        resultado = generar_pregunta_emergente(momento, usuario_id="test_user")

        print(f"\n📿 Pregunta Emergente:")
        print(f"   {resultado['pregunta']}")

        print(f"\n💭 Contexto:")
        print(f"   {resultado['contexto']}")

        print(f"\n🔗 Dominios conectados:")
        for dominio in resultado['dominios']:
            print(f"   - {dominio}")

        print(f"\n🌙 Fase Lunar: {resultado['fase_lunar']}")
        print(f"🎭 Tipo: {resultado['tipo']}")

        if resultado['patron_detectado']:
            print(f"📊 Patrón detectado: {resultado['patron_detectado']}")

        return True

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiples_generaciones(momento: str, num_tests: int = 3):
    """Genera múltiples preguntas para ver variedad"""
    print_separator("~")
    print(f"🔄 Generando {num_tests} preguntas para {momento.upper()}")
    print_separator("~")

    preguntas_unicas = set()

    for i in range(num_tests):
        print(f"\n--- Iteración {i+1} ---")
        resultado = generar_pregunta_emergente(momento)
        pregunta = resultado['pregunta']
        preguntas_unicas.add(pregunta)
        print(f"• {pregunta}")

    print(f"\n📊 Variedad: {len(preguntas_unicas)}/{num_tests} preguntas únicas")


def test_flujo_completo():
    """Simula un día completo con Estados Cero"""
    print("\n")
    print_separator("#")
    print("# SIMULACIÓN DE DÍA COMPLETO")
    print_separator("#")

    momentos = ["fajr", "dhuhr", "asr", "maghrib", "isha"]
    resultados = []

    for momento in momentos:
        try:
            resultado = generar_pregunta_emergente(momento)
            resultados.append({
                "momento": momento,
                "pregunta": resultado['pregunta'],
                "tipo": resultado['tipo'],
                "dominios": resultado['dominios']
            })
        except Exception as e:
            print(f"❌ Error en {momento}: {e}")

    print("\n🌅 PREGUNTA S DEL DÍA:\n")
    for r in resultados:
        print(f"**{r['momento'].upper()}** ({r['tipo']})")
        print(f"  {r['pregunta']}")
        print(f"  Dominios: {', '.join(r['dominios'])}\n")


def main():
    print("\n")
    print("=" * 70)
    print("🧪 TEST - SISTEMA DE PREGUNTAS EMERGENTES")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # Test 1: Pregunta por cada momento
    print("\n📋 TEST 1: Pregunta por momento litúrgico")
    print("=" * 70)

    momentos = ["fajr", "dhuhr", "maghrib"]
    exitos = 0

    for momento in momentos:
        if test_pregunta_por_momento(momento):
            exitos += 1
        print()

    print(f"\n✅ Test completado: {exitos}/{len(momentos)} momentos exitosos\n")

    # Test 2: Variedad de preguntas
    print("\n📋 TEST 2: Variedad en generación")
    test_multiples_generaciones("dhuhr", num_tests=3)

    # Test 3: Flujo diario
    print("\n📋 TEST 3: Simulación de día completo")
    test_flujo_completo()

    print("\n")
    print_separator("=")
    print("🎉 TESTS COMPLETADOS")
    print_separator("=")


if __name__ == "__main__":
    main()
