"""
Test del Ministerio del Cuerpo con decreto mock
"""

from ministerios.cuerpo import MinisterioCuerpo
from datetime import datetime, date

# Mock de DecretoSacral
class DecretoMock:
    def __init__(self, accion):
        self.id = 1
        self.fecha = date.today()
        self.accion_tangible = accion
        self.validado_contra_pilares = True

# Instanciar ministerio
ministerio = MinisterioCuerpo()

print("🏃 TESTING: MINISTERIO DEL CUERPO\n")
print("="*70)

# Test 1: Decreto con alta energía requerida
print("\n📜 DECRETO 1: 'Implementar sistema completo de autenticación'")
print("-"*70)

decreto1 = DecretoMock("Implementar sistema completo de autenticación y permisos")
respuesta1 = ministerio.responder_a_decreto(decreto1)

print(f"Evaluación: {respuesta1['evaluacion']}")
print(f"Coherencia circadiana: {respuesta1['coherencia_circadiana']:.1f}%")
print(f"Momento actual: {respuesta1['momento_actual']}")
print(f"Energía disponible: {respuesta1['energia_disponible']:.1f}")

if respuesta1['propuestas']:
    print(f"\nPropuestas del Ministerio:")
    for prop in respuesta1['propuestas']:
        print(f"  {prop}")

if respuesta1['alertas']:
    print(f"\nAlertas:")
    for alerta in respuesta1['alertas']:
        print(f"  {alerta}")

# Test 2: Decreto con calma requerida
print("\n"+ "="*70)
print("\n📜 DECRETO 2: 'Meditar y reflexionar sobre el día'")
print("-"*70)

decreto2 = DecretoMock("Meditar y reflexionar sobre los aprendizajes del día")
respuesta2 = ministerio.responder_a_decreto(decreto2)

print(f"Evaluación: {respuesta2['evaluacion']}")
print(f"Coherencia circadiana: {respuesta2['coherencia_circadiana']:.1f}%")
print(f"Momento actual: {respuesta2['momento_actual']}")
print(f"Energía disponible: {respuesta2['energia_disponible']:.1f}")

if respuesta2['propuestas']:
    print(f"\nPropuestas del Ministerio:")
    for prop in respuesta2['propuestas']:
        print(f"  {prop}")

if respuesta2['alertas']:
    print(f"\nAlertas:")
    for alerta in respuesta2['alertas']:
        print(f"  {alerta}")

# Test 3: Estado actual completo
print("\n"+ "="*70)
print("\n🔍 ESTADO COMPLETO DEL MINISTERIO")
print("-"*70)

estado = ministerio.estado_actual()
print("\nEstado Circadiano:")
for k, v in estado.items():
    print(f"  {k}: {v}")

print("\nMétricas de Salud:")
metricas = ministerio.metricas_salud()
for k, v in metricas.items():
    print(f"  {k}: {v:.1f}")

print("\n"+ "="*70)
print("\n✅ Test completado\n")

