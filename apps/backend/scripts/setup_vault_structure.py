#!/usr/bin/env python3
"""
Script para inicializar la estructura fractal de Obsidian
Ejecutar una vez para crear toda la jerarquía de carpetas y archivos base
"""

import sys
import os
from pathlib import Path

# Añadir backend al path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from services.obsidian_structure import ObsidianStructureManager

def main():
    """Inicializa la estructura del vault de Obsidian"""
    print("🏗️  Iniciando configuración de estructura fractal en Obsidian...")
    print("=" * 70)
    
    # Obtener path del vault
    vault_path = os.path.expanduser(os.getenv("OBSIDIAN_VAULT_PATH", "~/Documents/CampoSagrado"))
    print(f"\n📁 Vault path: {vault_path}\n")
    
    # Confirmar creación
    response = input("¿Crear estructura fractal completa? (s/n): ")
    if response.lower() != 's':
        print("❌ Operación cancelada")
        return
    
    # Crear estructura
    manager = ObsidianStructureManager(vault_path)
    manager.initialize_vault_structure()
    
    print("\n" + "=" * 70)
    print("✅ Estructura fractal creada exitosamente!")
    print(f"\n📚 Tu vault está en: {vault_path}")
    print("\n🔮 Próximos pasos:")
    print("  1. Abre Obsidian y selecciona este vault")
    print("  2. Instala plugins recomendados:")
    print("     - Dataview")
    print("     - Templater")
    print("     - obsidian-git")
    print("     - Excalidraw")
    print("  3. Inicia tu primer Estado Cero desde el frontend")
    print("\n🕌 Sistema operando al borde del caos - 40% capacidad sin asignar")

if __name__ == "__main__":
    main()

