#!/usr/bin/env python3
"""
🧪 Script de Prueba de Integraciones
====================================

Verifica que los agentes puedan:
1. Escribir en Obsidian
2. Leer de Obsidian
3. (Futuro) Conectar con Anytype
"""

import sys
import os
from pathlib import Path
from datetime import datetime, date

# Añadir backend al path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from integraciones.obsidian import ObsidianVault
import os


def test_obsidian_escritura():
    """Test 1: Verificar que podemos escribir en Obsidian"""
    print("\n📝 Test 1: Escritura en Obsidian")
    print("=" * 50)
    
    try:
        vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "/Users/hp/Campo sagrado MVP/obsidian_vault")
        client = ObsidianVault(vault_path)
        
        # Crear un Estado Cero de prueba
        contenido = f"""---
fecha: {date.today()}
momento: test
tipo: estado-cero-prueba
tags: [test, verificacion]
---

# Estado Cero - Test

## Contexto de Prueba
Este es un archivo generado automáticamente para verificar la integración con Obsidian.

**Timestamp**: {datetime.now().isoformat()}

## Verificación
Si estás leyendo esto en Obsidian, ¡la integración funciona! ✅

## Preguntas de Prueba

### 1. ¿La escritura funciona?
**Respuesta**: Sí (expansión: 5)

### 2. ¿El formato es correcto?
**Respuesta**: Verificar en Obsidian

### 3. ¿Los tags se aplican?
**Respuesta**: Buscar #test en Obsidian

## Siguiente Paso
Ejecuta el Test 2 para verificar la lectura.

[[test-integraciones]]
"""
        
        # Guardar en Obsidian
        ruta_relativa = f"50-Conversaciones-IA/Estados-Cero/test/test-{datetime.now().strftime('%H%M%S')}.md"
        ruta_completa = client.guardar_documento(
            filepath=ruta_relativa,
            contenido=contenido
        )
        
        print(f"✅ Archivo creado exitosamente:")
        print(f"   📂 {ruta_completa}")
        print(f"\n📖 Para verificar:")
        print(f"   1. Abre Obsidian")
        print(f"   2. Busca: {ruta_relativa}")
        print(f"   3. Verifica que el contenido sea legible")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en escritura: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_obsidian_lectura():
    """Test 2: Verificar que podemos leer desde Obsidian"""
    print("\n📖 Test 2: Lectura desde Obsidian")
    print("=" * 50)
    
    try:
        vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "/Users/hp/Campo sagrado MVP/obsidian_vault")
        client = ObsidianVault(vault_path)
        
        # Buscar archivos de Estados Cero
        archivos = client.listar_documentos("50-Conversaciones-IA/Estados-Cero")
        
        print(f"✅ Encontrados {len(archivos)} archivos de Estados Cero")
        
        if archivos:
            # Leer el más reciente
            archivo_reciente = sorted(archivos)[-1]
            contenido = client.leer_documento(archivo_reciente)
            
            print(f"\n📄 Archivo más reciente:")
            print(f"   📂 {archivo_reciente}")
            print(f"   📏 Tamaño: {len(contenido)} caracteres")
            print(f"\n   Primeras 200 caracteres:")
            print(f"   {contenido[:200]}...")
            
            return True
        else:
            print("⚠️ No se encontraron archivos. Ejecuta Test 1 primero.")
            return False
            
    except Exception as e:
        print(f"❌ Error en lectura: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_obsidian_estructura():
    """Test 3: Verificar estructura de carpetas"""
    print("\n📁 Test 3: Estructura de Carpetas")
    print("=" * 50)
    
    try:
        vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "/Users/hp/Campo sagrado MVP/obsidian_vault")
        client = ObsidianVault(vault_path)
        vault_path = client.vault_path
        
        # Carpetas esperadas
        carpetas_esperadas = [
            "50-Conversaciones-IA/Estados-Cero",
            "40-Journal",
            "30-Sesiones",
            "20-Insights"
        ]
        
        for carpeta in carpetas_esperadas:
            ruta_completa = vault_path / carpeta
            existe = ruta_completa.exists()
            
            if existe:
                archivos = list(ruta_completa.rglob("*.md"))
                print(f"✅ {carpeta}")
                print(f"   📊 {len(archivos)} archivos Markdown")
            else:
                print(f"⚠️ {carpeta} (no existe - se creará cuando sea necesario)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        return False


def test_obsidian_tags():
    """Test 4: Verificar que los tags funcionan"""
    print("\n🏷️ Test 4: Sistema de Tags")
    print("=" * 50)
    
    try:
        vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "/Users/hp/Campo sagrado MVP/obsidian_vault")
        client = ObsidianVault(vault_path)
        
        # Buscar archivos con tags específicos
        tags_buscar = ["estado-cero", "test", "fajr", "isha"]
        
        for tag in tags_buscar:
            # Buscar en el contenido de los archivos
            archivos_con_tag = []
            for archivo in client.listar_documentos(""):
                contenido = client.leer_documento(archivo)
                if contenido and (f"#{tag}" in contenido or f"- {tag}" in contenido):
                    archivos_con_tag.append(archivo)
            
            if archivos_con_tag:
                print(f"✅ #{tag}: {len(archivos_con_tag)} archivos")
            else:
                print(f"⚠️ #{tag}: 0 archivos (normal si es primera vez)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con tags: {e}")
        return False


def test_anytype_conexion():
    """Test 5: Verificar conexión con Anytype (futuro)"""
    print("\n🌐 Test 5: Conexión con Anytype")
    print("=" * 50)
    
    print("⚠️ Anytype no está implementado aún (planificado para v0.2.0)")
    print("\nCuándo usar Anytype:")
    print("  • Insights destilados (no temporales)")
    print("  • Patrones validados por Guardian")
    print("  • Relaciones complejas entre conceptos")
    print("  • Proyectos con múltiples contextos")
    
    print("\nCuándo usar Obsidian:")
    print("  • Estados Cero diarios")
    print("  • Planes de jornada")
    print("  • Reportes temporales")
    print("  • Journal y reflexiones")
    
    return None


def crear_estructura_inicial():
    """Crea la estructura inicial de carpetas si no existe"""
    print("\n🏗️ Creando estructura inicial...")
    print("=" * 50)
    
    try:
        vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "/Users/hp/Campo sagrado MVP/obsidian_vault")
        client = ObsidianVault(vault_path)
        vault_path = client.vault_path
        
        carpetas = [
            "50-Conversaciones-IA/Estados-Cero",
            "40-Journal",
            "30-Sesiones",
            "20-Insights/emergentes",
            "10-Meta"
        ]
        
        for carpeta in carpetas:
            ruta_completa = vault_path / carpeta
            ruta_completa.mkdir(parents=True, exist_ok=True)
            print(f"✅ {carpeta}")
        
        # Crear archivo índice
        index_content = """---
tipo: indice
creado: {}
---

# 🕌 Campo Sagrado - Índice

## Estructura del Vault

### 50-Conversaciones-IA
Interacciones directas con los agentes del sistema.

- **Estados-Cero/**: Consultas sacrales diarias
  - Organizadas por fecha y momento litúrgico
  - Tags: #estado-cero #fajr #dhuhr #asr #maghrib #isha

### 40-Journal
Documentación temporal del día a día.

- **{fecha}/**: Carpeta por día
  - `plan-jornada.md`: Plan generado por Orquestador
  - `reporte-guardian.md`: Reporte diario del Guardian

### 30-Sesiones
Sesiones de trabajo profundo.

- Por proyecto
- Linkadas a Estados Cero relevantes

### 20-Insights
Conocimiento emergente.

- **emergentes/**: Insights recién descubiertos
- Los insights validados migran a Anytype

### 10-Meta
Información sobre el sistema.

## Tags Principales

- #estado-cero
- #momento-{liturgico}
- #expansion / #contraccion
- #patron
- #insight

## Flujo de Documentación

1. **Estado Cero** → `50-Conversaciones-IA/Estados-Cero/`
2. **Plan Jornada** → `40-Journal/{fecha}/plan-jornada.md`
3. **Reporte Guardian** → `40-Journal/{fecha}/reporte-guardian.md`
4. **Insight emergente** → `20-Insights/emergentes/`
5. **Insight validado** → Anytype (v0.2.0)

---

*Generado automáticamente por Campo Sagrado MVP*
""".format(datetime.now().isoformat())
        
        index_path = vault_path / "README.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"\n✅ Estructura creada en: {vault_path}")
        print(f"📖 Índice creado: README.md")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando estructura: {e}")
        return False


def main():
    """Ejecuta todos los tests"""
    print("\n" + "="*70)
    print("🕌 CAMPO SAGRADO - TEST DE INTEGRACIONES")
    print("="*70)
    
    # Crear estructura si es necesario
    crear_estructura_inicial()
    
    # Ejecutar tests
    resultados = {
        "Escritura Obsidian": test_obsidian_escritura(),
        "Lectura Obsidian": test_obsidian_lectura(),
        "Estructura": test_obsidian_estructura(),
        "Tags": test_obsidian_tags(),
        "Anytype": test_anytype_conexion()
    }
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE TESTS")
    print("="*70)
    
    for nombre, resultado in resultados.items():
        if resultado is True:
            print(f"✅ {nombre}")
        elif resultado is False:
            print(f"❌ {nombre}")
        else:
            print(f"⚠️ {nombre} (no implementado)")
    
    # Verificación final
    tests_exitosos = sum(1 for r in resultados.values() if r is True)
    tests_totales = sum(1 for r in resultados.values() if r is not None)
    
    print(f"\n📈 Resultado: {tests_exitosos}/{tests_totales} tests exitosos")
    
    if tests_exitosos == tests_totales:
        print("\n🎉 ¡Todas las integraciones funcionan correctamente!")
    elif tests_exitosos > 0:
        print("\n⚠️ Algunas integraciones necesitan atención")
    else:
        print("\n❌ Las integraciones requieren configuración")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()

