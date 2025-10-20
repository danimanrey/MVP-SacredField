#!/usr/bin/env python3
"""
⚙️ Generador de Configuración de Agentes
==========================================

Carga tu prisma personal y genera configuración operativa
para todos los agentes.

Ejecutar después de configurar_prisma.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.motor_prisma import cargar_prisma_y_configurar
import json


def main():
    print("\n" + "="*70)
    print("  ⚙️ GENERANDO CONFIGURACIÓN DE AGENTES")
    print("="*70)
    
    # Cargar prisma y generar configuración
    motor = cargar_prisma_y_configurar()
    
    if not motor:
        print("\n❌ No se pudo cargar el prisma personal")
        print("   Ejecuta primero: python scripts/configurar_prisma.py")
        return
    
    print("\n✅ Configuración generada exitosamente\n")
    
    # Mostrar resumen
    config = motor.exportar_configuracion_completa()
    
    print("📋 CONFIGURACIÓN POR AGENTE:")
    print("="*70)
    
    # Estado Cero
    ec = config["estado_cero"]
    print("\n🔮 ESTADO CERO:")
    print(f"   Tipo preguntas: {ec['tipo_preguntas']}")
    print(f"   Número: {ec['numero_preguntas']}")
    print(f"   Estilo: {ec['estilo_redaccion']}")
    print(f"   Categorías priorizadas: {', '.join(ec['categorias_priorizadas'][:3])}")
    print(f"   Sesgos a evitar: {', '.join(ec['evitar_sesgos'][:2])}")
    
    # Entrelazador
    ent = config["entrelazador"]
    print("\n🧩 ENTRELAZADOR:")
    print(f"   Duración flujo: {ent['duracion_bloque_profundo']} min")
    print(f"   Horarios óptimos: {', '.join(ent['horarios_optimos'])}")
    print(f"   Estilo trabajo: {ent['estilo_trabajo']}")
    print(f"   Balance: {ent['balance_profundidad']:.1f} (0=amplitud, 1=profundidad)")
    print(f"   Protecciones: {', '.join(ent['protecciones'])}")
    
    # Orquestador
    orq = config["orquestador"]
    print("\n🎼 ORQUESTADOR:")
    print(f"   Criterios: {', '.join(orq['criterios_priorizacion'][:3])}")
    print(f"   Nivel detalle: {orq['nivel_detalle']}")
    print(f"   Flexibilidad: {orq['flexibilidad']:.1f} (0=rígido, 1=flexible)")
    print(f"   Puntos decisión: {', '.join(orq['puntos_decision'])}")
    
    # Documentador
    doc = config["documentador"]
    print("\n📝 DOCUMENTADOR:")
    print(f"   Sistema: {doc['sistema_primario']}")
    print(f"   Estructura: {doc['estructura_notas']}")
    print(f"   Profundidad: {doc['profundidad']}")
    print(f"   Síntesis: {doc['frecuencia_sintesis']}")
    print(f"   Conexiones auto: {doc['conexiones_auto']}")
    
    # Guardián
    guard = config["guardian"]
    print("\n👁️ GUARDIÁN:")
    print(f"   Métricas: {', '.join(guard['metricas_clave'][:3])}")
    print(f"   Frecuencia: {guard['frecuencia_reporte']}")
    print(f"   Alertas configuradas: {len(guard['alertas'])}")
    
    print("\n" + "="*70)
    print("  ✨ CONFIGURACIÓN GUARDADA")
    print("="*70)
    
    print("\nArchivo: config/configuracion_agentes.json")
    print("\nLos agentes ahora operan según tu prisma único:")
    print(f"   • {motor.prisma.diseño_humano.tipo.value.title()} | {motor.prisma.diseño_humano.autoridad.value.title()}")
    print(f"   • {motor.prisma.perfil_psicologico.mbti.value} | Eneagrama {motor.prisma.perfil_psicologico.eneagrama_base.value}")
    print(f"   • {len(motor.prisma.manifestaciones)} manifestaciones activas")
    
    print("\n🕌 waḥdat al-wujūd: Los agentes respiran desde tu unidad")
    print("✨ al-khayāl al-faʿʿāl: La imaginación creadora guía cada decisión")
    
    print("\n💡 Próximo paso:")
    print("   Los agentes usarán esta configuración automáticamente.")
    print("   Actualiza ejecutando este script después de cambiar tu prisma.")


if __name__ == "__main__":
    main()

