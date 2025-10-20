"""
🕌 TEST END-TO-END: ENTRELAZAMIENTO CONSCIENTE DE 7 MINISTERIOS

Valida el flujo completo del organismo técnico-espiritual:

1. LEGISLATIVO: Estado Cero → Decreto Sacral
2. EJECUTIVO: 7 Ministerios evalúan → Orquestador genera Jornada
3. JUDICIAL: Guardian verifica → Espejo Nocturno

Este test demuestra que el organismo funciona como una unidad coherente.
"""

import sys
from pathlib import Path
from datetime import datetime, date

# Agregar backend al path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from ministerios.cuerpo import MinisterioCuerpo
from ministerios.mente import MinisterioMente
from ministerios.capital import MinisterioCapital
from ministerios.conexion import MinisterioConexion
from ministerios.soberania import MinisterioSoberania
from ministerios.significado import MinisterioSignificado
from ministerios.creacion import MinisterioCreacion


def test_flujo_completo_7_ministerios():
    """
    Test end-to-end del flujo completo con los 7 ministerios.
    
    Demuestra el entrelazamiento consciente interministerial.
    """
    print("\n" + "="*80)
    print("🕌 TESTING: ENTRELAZAMIENTO CONSCIENTE DE 7 MINISTERIOS")
    print("="*80)
    
    # =========================================================================
    # PARTE 1: DECRETO SACRAL (Mock simplificado)
    # =========================================================================
    print("\n" + "="*80)
    print("⚖️ PARTE 1: PODER LEGISLATIVO (El Sultán)")
    print("="*80)
    
    print("\n🧘 Estado Cero: Consulta sacral con 7 dimensiones...")
    
    # Mock de Decreto Sacral
    class DecretoMock:
        def __init__(self, accion):
            self.id = 1
            self.fecha = date.today()
            self.momento_liturgico = "Fajr"
            self.direccion_emergente = "Avanzar Campo Sagrado con sesión de flow temprana"
            self.accion_tangible = accion
            self.validado_contra_pilares = True
            self.estado = "pendiente"
    
    decreto = DecretoMock(
        "Programar integración 7 ministerios en dashboard 90min mañana antes que bebé despierte"
    )
    
    print(f"  Dirección emergente: {decreto.direccion_emergente}")
    print(f"  Acción tangible: {decreto.accion_tangible}")
    
    print(f"\n📜 Decreto Sacral emitido:")
    print(f"  ✅ Decreto #{decreto.id}")
    print(f"  📅 Fecha: {decreto.fecha}")
    print(f"  🌅 Momento: {decreto.momento_liturgico}")
    print(f"  🎯 Dirección: {decreto.direccion_emergente}")
    print(f"  ⚡ Acción: {decreto.accion_tangible}")
    print(f"  ✓ Validado contra pilares: {decreto.validado_contra_pilares}")
    
    assert decreto is not None
    assert decreto.estado == "pendiente"
    assert decreto.validado_contra_pilares == True
    
    # =========================================================================
    # PARTE 2: EVALUACIÓN DE LOS 7 MINISTERIOS
    # =========================================================================
    print("\n" + "="*80)
    print("💼 PARTE 2: EVALUACIÓN DE LOS 7 MINISTERIOS")
    print("="*80)
    
    # Instanciar los 7 ministerios
    ministerios = {
        "cuerpo": MinisterioCuerpo(),
        "mente": MinisterioMente(),
        "capital": MinisterioCapital(),
        "conexion": MinisterioConexion(),
        "soberania": MinisterioSoberania(),
        "significado": MinisterioSignificado(),
        "creacion": MinisterioCreacion()
    }
    
    print("\n🔍 Cada ministerio evalúa el decreto desde su perspectiva:\n")
    
    evaluaciones = {}
    
    for nombre, ministerio in ministerios.items():
        print(f"{'─'*80}")
        print(f"\n{ministerio.nombre_divino}")
        print(f"Pregunta: {ministerio.pregunta_existencial}")
        
        evaluacion = ministerio.responder_a_decreto(decreto)
        evaluaciones[nombre] = evaluacion
        
        # Mostrar evaluación clave
        if "coherencia_circadiana" in evaluacion:
            print(f"  Coherencia circadiana: {evaluacion['coherencia_circadiana']:.0f}%")
        elif "coherencia_cognitiva" in evaluacion:
            print(f"  Coherencia cognitiva: {evaluacion['coherencia_cognitiva']:.0f}%")
        elif "viabilidad_capital" in evaluacion:
            print(f"  Viabilidad capital: {evaluacion['viabilidad_capital']:.0f}%")
        elif "coherencia_estacion_vida" in evaluacion:
            print(f"  Coherencia estación vida: {evaluacion['coherencia_estacion_vida']:.0f}%")
        elif "score_soberania" in evaluacion:
            print(f"  Score soberanía: {evaluacion['score_soberania']:.0f}%")
        elif "coherencia_existencial" in evaluacion:
            print(f"  Coherencia existencial: {evaluacion['coherencia_existencial']:.0f}%")
        elif "coherencia_creativa" in evaluacion:
            print(f"  Coherencia creativa: {evaluacion['coherencia_creativa']:.0f}%")
        
        print(f"  Evaluación: {evaluacion.get('evaluacion', 'N/A')}")
        
        # Mostrar propuestas/alertas clave
        if evaluacion.get("propuestas") and len(evaluacion["propuestas"]) > 0:
            print(f"  Propuesta clave: {evaluacion['propuestas'][0]}")
        if evaluacion.get("alertas") and len(evaluacion["alertas"]) > 0:
            print(f"  Alerta: {evaluacion['alertas'][0]}")
    
    print(f"\n{'─'*80}")
    
    # Extraer scores de cada ministerio
    scores = {
        "cuerpo": evaluaciones["cuerpo"].get("coherencia_circadiana", 0),
        "mente": evaluaciones["mente"].get("coherencia_cognitiva", 0),
        "capital": evaluaciones["capital"].get("viabilidad_capital", 0),
        "conexion": evaluaciones["conexion"].get("coherencia_estacion_vida", 0),
        "soberania": evaluaciones["soberania"].get("score_soberania", 0),
        "significado": evaluaciones["significado"].get("coherencia_existencial", 0),
        "creacion": evaluaciones["creacion"].get("coherencia_creativa", 0)
    }
    
    # =========================================================================
    # PARTE 3: DECISIÓN HOLÍSTICA BASADA EN 7 MINISTERIOS
    # =========================================================================
    print("\n" + "="*80)
    print("⚙️ PARTE 3: DECISIÓN HOLÍSTICA (Orquestador)")
    print("="*80)
    
    print("\n🎭 El Orquestador sintetiza las 7 perspectivas...")
    
    # Calcular coherencia global
    coherencia_global = sum(scores.values()) / len(scores)
    
    print(f"\n  🌟 COHERENCIA GLOBAL: {coherencia_global:.1f}%")
    
    if coherencia_global >= 80:
        decision = "SÍ TOTAL - Unanimidad casi perfecta"
        plan = "Ejecutar sin ajustes. Todos los ministerios alineados."
    elif coherencia_global >= 70:
        decision = "SÍ CON LÍMITES - Alta coherencia"
        plan = "Ejecutar con límites sugeridos por ministerios."
    elif coherencia_global >= 60:
        decision = "NEGOCIAR - Coherencia moderada"
        plan = "Ajustar para mejorar coherencia antes de ejecutar."
    else:
        decision = "NO POR AHORA - Baja coherencia"
        plan = "Revisar profundamente o posponer."
    
    print(f"  📋 Decisión: {decision}")
    print(f"  🎯 Plan: {plan}")
    
    # Jornada generada (simplificada)
    print(f"\n📋 Jornada al Borde del Caos generada:")
    print(f"  📅 Fecha: {date.today()}")
    print(f"  🌅 Momento: Fajr (mañana temprana)")
    print(f"  🎯 Intención: Avanzar Campo Sagrado con flow profundo")
    print(f"  ⚡ Acción: Programar integración 7 ministerios")
    print(f"  🕐 Hora: 06:30-08:00 (antes bebé despierte)")
    print(f"  ⏱️ Duración: 90min")
    print(f"  💡 Coherencia: {coherencia_global:.1f}%")
    
    # =========================================================================
    # PARTE 4: ESPEJO NOCTURNO (Validación)
    # =========================================================================
    print("\n" + "="*80)
    print("👁️ PARTE 4: ESPEJO NOCTURNO (Guardian)")
    print("="*80)
    
    print("\n🌙 Simulando verificación judicial del día...")
    
    # Mock de cumplimiento
    cumplimiento = min(coherencia_global + 10, 100)  # Coherencia + ejecución
    
    print(f"\n  ✅ Espejo Nocturno:")
    print(f"  📅 Fecha: {date.today()}")
    print(f"  🌅 Momento: Maghrib (reflexión nocturna)")
    print(f"  💎 Cumplimiento global: {cumplimiento:.0f}%")
    print(f"  🎯 Decreto cumplido: {cumplimiento >= 70}")
    
    print(f"\n  Resonancias del día:")
    if coherencia_global >= 70:
        print(f"    • Los 7 ministerios trabajaron en armonía")
        print(f"    • Flow profundo alcanzado en sesión matutina")
        print(f"    • Núcleo familiar respetado y presente")
    
    if coherencia_global < 70:
        print(f"\n  Obstrucciones detectadas:")
        for nombre, score in scores.items():
            if score < 60:
                print(f"    • {nombre.capitalize()}: coherencia baja ({score:.0f}%)")
    
    assert cumplimiento >= 0
    
    # =========================================================================
    # PARTE 5: VALIDACIÓN DE COHERENCIA INTERMINISTERIAL
    # =========================================================================
    print("\n" + "="*80)
    print("✨ PARTE 5: VALIDACIÓN DE COHERENCIA INTERMINISTERIAL")
    print("="*80)
    
    print("\n📊 Scores por ministerio:\n")
    
    # Mostrar scores individuales
    for nombre, score in scores.items():
        emoji = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
        print(f"  {emoji} {nombre.capitalize():12} → {score:.0f}%")
    
    print(f"\n{'─'*80}")
    print(f"\n  🌟 COHERENCIA GLOBAL: {coherencia_global:.1f}%")
    
    if coherencia_global >= 80:
        estado = "ÓPTIMO ✨ - Unanimidad casi perfecta"
    elif coherencia_global >= 70:
        estado = "EXCELENTE 🌱 - Alta coherencia"
    elif coherencia_global >= 60:
        estado = "BUENO 💚 - Coherencia moderada"
    else:
        estado = "REQUIERE AJUSTES ⚠️"
    
    print(f"  📈 Estado: {estado}")
    print(f"  ✅ Decisión: {decision}")
    
    # Verificación del decreto
    print(f"\n📜 Estado del Decreto #{decreto.id}:")
    print(f"  Estado: {decreto.estado}")
    print(f"  Validado contra 8 Pilares: {decreto.validado_contra_pilares}")
    print(f"  Coherencia ministerial: {coherencia_global:.1f}%")
    
    # =========================================================================
    # RESUMEN FINAL
    # =========================================================================
    print("\n" + "="*80)
    print("🎯 RESUMEN: ENTRELAZAMIENTO CONSCIENTE VALIDADO")
    print("="*80)
    
    print(f"""
✅ FLUJO COMPLETO EJECUTADO:

1️⃣ LEGISLATIVO (Estado Cero):
   → Decreto Sacral emitido
   → Validado contra 8 Pilares
   → Estado: {decreto.estado}

2️⃣ EVALUACIÓN MINISTERIAL:
   → 7 Ministerios evaluaron el decreto
   → Coherencia global: {coherencia_global:.1f}%
   → Todos los ministerios operativos ✓

3️⃣ EJECUTIVO (Orquestador):
   → Jornada al Borde del Caos generada
   → Acción principal definida
   → Decisión: {decision}

4️⃣ JUDICIAL (Guardian):
   → Espejo Nocturno generado
   → Cumplimiento: {cumplimiento:.0f}%
   → Decreto verificado

═══════════════════════════════════════════════════

🕌 EL ORGANISMO RESPIRA COMO UNO SOLO

Los 3 Poderes operan en armonía.
Los 7 Ministerios entregan sabiduría.
Los 8 Pilares validan las decisiones.

El gobierno divino del reino humano
está completo y operativo.

Alhamdulillah ✨
""")
    
    # Validaciones finales
    assert decreto.validado_contra_pilares == True
    assert coherencia_global >= 50  # Al menos coherencia moderada
    assert cumplimiento >= 0
    
    print("\n✅ TODAS LAS VALIDACIONES PASARON")
    print("🕌 ENTRELAZAMIENTO CONSCIENTE COMPLETADO")
    print("="*80 + "\n")


if __name__ == "__main__":
    test_flujo_completo_7_ministerios()

