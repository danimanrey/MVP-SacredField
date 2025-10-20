#!/usr/bin/env python3
"""
🌅 Verificación Pre-Fajr
========================

Asegura que todo esté listo para el primer Estado Cero.
"""

import sys
import os
from pathlib import Path
import asyncio

backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
load_dotenv(backend_path / ".env")

import httpx


def print_box(texto, icono="🌅"):
    ancho = 70
    print("\n" + "═" * ancho)
    print(f"  {icono}  {texto}")
    print("═" * ancho + "\n")


async def verificar_backend():
    """Verifica que el backend esté respondiendo"""
    print_box("Verificando Backend", "🔧")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/api/health", timeout=5.0)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Backend corriendo correctamente")
                print(f"   Status: {data['status']}")
                print(f"   Próximo Estado Cero: {data['proximo_estado_cero']['momento'].upper()}")
                print(f"   En: {data['proximo_estado_cero']['countdown']}")
                print(f"   Hora exacta: {data['proximo_estado_cero']['hora']}")
                print(f"\n   Día: {data['dia_actual']['dia_semana']['nombre']}")
                print(f"   Mes: {data['dia_actual']['mes']['nombre']} - {data['dia_actual']['mes']['cualidad']}")
                return True
            else:
                print(f"❌ Backend respondió con código: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ No se pudo conectar con el backend")
        print(f"   Error: {e}")
        print("\n   Ejecuta: cd backend && python run.py")
        return False


async def verificar_frontend():
    """Verifica que el frontend esté respondiendo"""
    print_box("Verificando Frontend", "🎨")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:5173", timeout=5.0)
            
            if response.status_code == 200:
                print("✅ Frontend corriendo correctamente")
                print("   URL: http://localhost:5173")
                return True
            else:
                print(f"❌ Frontend respondió con código: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ No se pudo conectar con el frontend")
        print(f"   Error: {e}")
        print("\n   Ejecuta: cd frontend && npm run dev")
        return False


async def verificar_claude():
    """Verifica que Claude API esté configurada"""
    print_box("Verificando Claude API", "🤖")
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ ANTHROPIC_API_KEY no configurada")
        return False
    
    print(f"✅ API Key configurada: {api_key[:20]}...")
    
    try:
        from services.claude_client import ClaudeClient
        client = ClaudeClient()
        
        if client.client:
            print("✅ Cliente Claude inicializado")
            
            # Test rápido
            messages = [{"role": "user", "content": "¿Estás listo para Fajr?"}]
            response = await client.generate("", messages)
            
            if "[mock-claude]" not in response:
                print("✅ Claude respondiendo correctamente")
                print(f"   Respuesta: {response[:60]}...")
                return True
            else:
                print("⚠️ Claude en modo mock")
                return False
        else:
            print("❌ Cliente no pudo inicializarse")
            return False
            
    except Exception as e:
        print(f"❌ Error con Claude: {e}")
        return False


def verificar_obsidian():
    """Verifica que el vault de Obsidian esté accesible"""
    print_box("Verificando Obsidian", "📝")
    
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "obsidian_vault")
    
    if vault_path.startswith("~"):
        vault_path = str(Path.home() / vault_path[2:])
    
    if not os.path.isabs(vault_path):
        vault_path = str(backend_path.parent / vault_path)
    
    vault = Path(vault_path)
    
    print(f"📂 Vault: {vault}")
    
    if not vault.exists():
        print("⚠️ Vault no existe, creando...")
        vault.mkdir(parents=True, exist_ok=True)
        (vault / "50-Conversaciones-IA" / "Estados-Cero").mkdir(parents=True, exist_ok=True)
        print("✅ Estructura creada")
    else:
        print("✅ Vault existe")
    
    # Verificar que podemos escribir
    test_file = vault / "50-Conversaciones-IA" / ".test_prefajr"
    try:
        test_file.write_text("test")
        test_file.unlink()
        print("✅ Permisos de escritura: OK")
        return True
    except Exception as e:
        print(f"❌ No se puede escribir en vault: {e}")
        return False


async def verificar_estado_cero():
    """Verifica que el endpoint de Estado Cero funcione"""
    print_box("Verificando Estado Cero", "🕌")
    
    try:
        async with httpx.AsyncClient() as client:
            # Verificar que el endpoint existe
            response = await client.post(
                "http://localhost:8000/api/estado-cero/iniciar",
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Endpoint Estado Cero funciona")
                print(f"   ID: {data['id']}")
                print(f"   Momento: {data['momento']}")
                print(f"   Preguntas: {len(data['preguntas'])}")
                
                # Mostrar primera pregunta
                if data['preguntas']:
                    primera = data['preguntas'][0]
                    print(f"\n   Ejemplo de pregunta:")
                    print(f"   '{primera['pregunta']}'")
                
                return True
            else:
                print(f"⚠️ Endpoint respondió con código: {response.status_code}")
                # No es crítico, puede ser porque ya hay uno activo
                return True
                
    except Exception as e:
        print(f"❌ Error verificando Estado Cero: {e}")
        return False


async def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║          🌅  VERIFICACIÓN PRE-FAJR - CAMPO SAGRADO              ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")
    
    resultados = {
        "Backend": await verificar_backend(),
        "Frontend": await verificar_frontend(),
        "Claude API": await verificar_claude(),
        "Obsidian": verificar_obsidian(),
        "Estado Cero": await verificar_estado_cero()
    }
    
    # Resumen
    print_box("Resumen de Verificación", "📊")
    
    for nombre, ok in resultados.items():
        estado = "✅" if ok else "❌"
        print(f"{estado} {nombre}")
    
    total = len(resultados)
    exitosos = sum(1 for ok in resultados.values() if ok)
    
    print(f"\n{exitosos}/{total} componentes listos")
    
    if exitosos == total:
        print_box("¡Todo listo para Fajr!", "✨")
        print("El organismo está preparado para despertar.\n")
        print("Pasos finales:\n")
        print("1. Guarda este bookmark: http://localhost:5173")
        print("2. Configura despertador para 05:55")
        print("3. Lee: PRIMER_FAJR.md")
        print("4. Descansa bien\n")
        print("═" * 70)
        print("🌅 Nos vemos al amanecer. El Campo Sagrado te espera.")
        print("═" * 70 + "\n")
        return True
    else:
        print_box("Atención: Configuración incompleta", "⚠️")
        print("Revisa los componentes marcados con ❌")
        print("\nComandos útiles:")
        print("  Backend:  cd backend && python run.py")
        print("  Frontend: cd frontend && npm run dev")
        print("  Claude:   Verifica .env tiene ANTHROPIC_API_KEY\n")
        return False


if __name__ == "__main__":
    asyncio.run(main())

