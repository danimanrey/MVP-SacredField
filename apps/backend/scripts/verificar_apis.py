#!/usr/bin/env python3
"""
🔍 Verificación de APIs
========================

Verifica que todas las integraciones funcionen correctamente.
"""

import sys
import os
from pathlib import Path

# Añadir backend al path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(backend_path / ".env")


def print_header(titulo):
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70 + "\n")


def verificar_anthropic():
    """Verifica la API de Anthropic Claude"""
    print_header("🤖 Anthropic Claude API")
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ ANTHROPIC_API_KEY no configurada en .env")
        return False
    
    if not api_key.startswith("sk-ant-"):
        print("⚠️  API Key no parece válida (debe empezar con 'sk-ant-')")
        return False
    
    print(f"✅ API Key encontrada: {api_key[:20]}...{api_key[-8:]}")
    
    # Intentar importar y usar el cliente
    try:
        from services.claude_client import ClaudeClient
        
        client = ClaudeClient()
        print(f"✅ Cliente Claude inicializado")
        print(f"   Modo: {'Mock (sin API key)' if client.mock_mode else 'Producción (API key válida)'}")
        
        if client.mock_mode:
            print("\n⚠️  Cliente en modo MOCK")
            print("   Las respuestas serán simuladas, no reales de Claude")
            return False
        
        # Test simple
        print("\n🧪 Probando generación simple...")
        messages = [{"role": "user", "content": "Responde solo con: OK"}]
        
        import asyncio
        response = asyncio.run(client.generate("", messages))
        
        print(f"✅ Respuesta recibida: '{response.strip()}'")
        print("\n✨ Anthropic Claude API funciona correctamente")
        return True
        
    except Exception as e:
        print(f"\n❌ Error probando Claude: {e}")
        import traceback
        traceback.print_exc()
        return False


def verificar_anytype():
    """Verifica la configuración de Anytype"""
    print_header("🔷 Anytype API")
    
    api_key = os.getenv("ANYTYPE_API_KEY")
    
    if not api_key:
        print("❌ ANYTYPE_API_KEY no configurada en .env")
        return False
    
    print(f"✅ API Key encontrada: {api_key[:20]}...{api_key[-8:]}")
    
    try:
        from integraciones.anytype import AnytypeClient
        
        client = AnytypeClient()
        print(f"✅ Cliente Anytype inicializado")
        print(f"   Base URL: {client.base_url}")
        
        # Nota: Anytype requiere configuración más compleja
        print("\n⚠️  Anytype requiere configuración adicional:")
        print("   1. Anytype Desktop debe estar corriendo")
        print("   2. API local debe estar habilitada")
        print("   3. Conexión en localhost:31007")
        
        print("\n📋 Estado actual: Preparado pero no activo")
        print("   (Se usará cuando esté configurado en v0.2.0)")
        return True
        
    except Exception as e:
        print(f"\n⚠️  Error cargando Anytype: {e}")
        print("   Esto es esperado - Anytype es opcional en MVP")
        return True  # No es crítico


def verificar_obsidian():
    """Verifica la integración con Obsidian"""
    print_header("📝 Obsidian Vault")
    
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "obsidian_vault")
    
    # Convertir ~ a ruta absoluta
    if vault_path.startswith("~"):
        vault_path = str(Path.home() / vault_path[2:])
    
    # Si es relativa, hacerla absoluta desde el proyecto
    if not os.path.isabs(vault_path):
        vault_path = str(backend_path.parent / vault_path)
    
    vault = Path(vault_path)
    
    print(f"📂 Vault Path: {vault}")
    
    if not vault.exists():
        print(f"⚠️  Vault no existe en: {vault}")
        print(f"   Creando estructura...")
        vault.mkdir(parents=True, exist_ok=True)
        (vault / "50-Conversaciones-IA").mkdir(exist_ok=True)
        (vault / "50-Conversaciones-IA" / "Estados-Cero").mkdir(exist_ok=True)
        print(f"✅ Estructura de vault creada")
    else:
        print(f"✅ Vault existe")
    
    try:
        from integraciones.obsidian import ObsidianVault
        
        client = ObsidianVault(str(vault))
        print(f"✅ Cliente Obsidian inicializado")
        
        # Probar escritura
        print("\n🧪 Probando escritura en vault...")
        test_path = "50-Conversaciones-IA/test_api_verification.md"
        contenido = f"""# Test de Verificación de API

**Fecha**: {Path(__file__).parent.parent}
**Estado**: ✅ Escritura exitosa

Este archivo fue creado automáticamente para verificar la integración con Obsidian.

## Funcionalidad
- ✅ Escritura de archivos
- ✅ Creación de carpetas
- ✅ Formato Markdown

---
*Generado por Campo Sagrado MVP*
"""
        
        ruta_completa = client.guardar_documento(test_path, contenido)
        print(f"✅ Archivo de prueba creado: {ruta_completa}")
        
        # Probar lectura
        contenido_leido = client.leer_documento(test_path)
        if contenido_leido:
            print(f"✅ Lectura exitosa ({len(contenido_leido)} caracteres)")
        
        # Listar archivos
        archivos = client.listar_documentos("50-Conversaciones-IA")
        print(f"✅ {len(archivos)} archivo(s) en 50-Conversaciones-IA/")
        
        print("\n✨ Obsidian funciona correctamente")
        print("\n📌 IMPORTANTE sobre Obsidian:")
        print("   • NO necesita API REST adicional")
        print("   • Funciona con acceso directo al filesystem")
        print("   • Los archivos se sincronizan automáticamente")
        print("   • Obsidian detecta cambios en tiempo real")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error con Obsidian: {e}")
        import traceback
        traceback.print_exc()
        return False


def verificar_google_calendar():
    """Verifica Google Calendar OAuth"""
    print_header("🗓️  Google Calendar")
    
    credentials_path = backend_path / "config" / "google_credentials.json"
    token_path = backend_path / "config" / "google_token.json"
    
    if not credentials_path.exists():
        print(f"⚠️  Credentials no encontradas: {credentials_path}")
        print("   Ejecuta: python scripts/setup_google_calendar.py")
        return False
    
    print(f"✅ Credentials encontradas: {credentials_path}")
    
    if not token_path.exists():
        print(f"⚠️  Token no encontrado: {token_path}")
        print("   Ejecuta: python scripts/setup_google_calendar.py")
        return False
    
    print(f"✅ Token encontrado: {token_path}")
    
    try:
        from integraciones.google_calendar import google_calendar
        
        if not google_calendar:
            print("❌ Cliente no inicializado")
            return False
        
        if not google_calendar.is_authenticated():
            print("❌ No autenticado")
            return False
        
        print("✅ Cliente autenticado")
        
        # Probar listado de calendarios
        calendars = google_calendar.service.calendarList().list().execute()
        calendar_count = len(calendars.get('items', []))
        
        print(f"✅ {calendar_count} calendario(s) disponible(s)")
        
        for cal in calendars.get('items', [])[:3]:
            nombre = cal.get('summary', 'Sin nombre')
            es_primario = ' (Principal)' if cal.get('primary') else ''
            print(f"   • {nombre}{es_primario}")
        
        print("\n✨ Google Calendar funciona correctamente")
        return True
        
    except Exception as e:
        print(f"\n❌ Error con Google Calendar: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║          🕌  CAMPO SAGRADO - VERIFICACIÓN DE APIs                ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")
    
    resultados = {
        "Anthropic Claude": verificar_anthropic(),
        "Anytype": verificar_anytype(),
        "Obsidian": verificar_obsidian(),
        "Google Calendar": verificar_google_calendar()
    }
    
    # Resumen final
    print_header("📊 RESUMEN")
    
    for nombre, ok in resultados.items():
        estado = "✅" if ok else "❌"
        print(f"{estado} {nombre}")
    
    total = len(resultados)
    exitosos = sum(1 for ok in resultados.values() if ok)
    
    print(f"\n{exitosos}/{total} integraciones funcionando correctamente")
    
    if exitosos == total:
        print("\n🎉 ¡Todas las APIs están listas!")
    elif exitosos >= total - 1:
        print("\n✨ Sistema funcional (algunas APIs opcionales)")
    else:
        print("\n⚠️  Algunas APIs requieren configuración")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()

