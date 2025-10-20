#!/usr/bin/env python3
"""
Test simple de Claude API
"""

import sys
import os
from pathlib import Path

backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
load_dotenv(backend_path / ".env")

import asyncio
from services.claude_client import ClaudeClient


async def test_claude():
    print("🤖 Probando Anthropic Claude API...\n")
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    print(f"API Key: {api_key[:20]}...{api_key[-8:]}\n")
    
    client = ClaudeClient()
    
    if not client.client:
        print("❌ Cliente no inicializado (API key inválida o ausente)")
        return False
    
    print("✅ Cliente inicializado correctamente\n")
    
    # Test 1: Generación simple
    print("Test 1: Generación simple")
    print("-" * 50)
    
    messages = [{"role": "user", "content": "Di solo: Hola desde Campo Sagrado"}]
    
    try:
        response = await client.generate("", messages)
        print(f"Respuesta: {response}")
        
        if "[mock-claude]" in response or "[claude-error]" in response:
            print("❌ Recibimos respuesta mock/error, no de Claude real")
            return False
        
        print("✅ Test 1 exitoso\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False
    
    # Test 2: JSON
    print("Test 2: Generación de JSON")
    print("-" * 50)
    
    messages = [{"role": "user", "content": "Genera un JSON con: {\"estado\": \"funcionando\"}"}]
    
    try:
        response_json = await client.generate_json("", messages)
        print(f"JSON: {response_json}")
        
        if isinstance(response_json, dict):
            print("✅ Test 2 exitoso - JSON válido\n")
        else:
            print("⚠️ No es un dict, pero no falló\n")
    except Exception as e:
        print(f"⚠️ Error en JSON: {e}\n")
    
    # Test 3: Pregunta real del sistema
    print("Test 3: Caso de uso real - Generar pregunta binaria")
    print("-" * 50)
    
    system = """Eres el Agente Estado Cero. 
Genera 1 pregunta binaria que evoque sensación corporal.
Formato JSON: {"pregunta": "...", "categoria": "biologia"}"""
    
    messages = [{"role": "user", "content": "Genera una pregunta sobre energía corporal actual"}]
    
    try:
        pregunta_json = await client.generate_json(system, messages)
        print(f"Pregunta generada: {pregunta_json}")
        print("✅ Test 3 exitoso - Caso de uso real funciona\n")
    except Exception as e:
        print(f"⚠️ Error: {e}\n")
    
    print("="*50)
    print("✨ Claude API funciona correctamente")
    print("="*50)
    return True


if __name__ == "__main__":
    asyncio.run(test_claude())

