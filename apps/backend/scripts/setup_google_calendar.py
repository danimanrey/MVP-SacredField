#!/usr/bin/env python3
"""
🔐 Setup de Google Calendar API
================================

Script interactivo para configurar las credenciales de Google Calendar.
"""

import sys
from pathlib import Path

# Añadir backend al path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from integraciones.google_calendar import GoogleCalendarClient


def print_instrucciones():
    """Muestra instrucciones detalladas"""
    print("""
═══════════════════════════════════════════════════════════════
🗓️  SETUP DE GOOGLE CALENDAR - Campo Sagrado
═══════════════════════════════════════════════════════════════

Para usar Google Calendar necesitas crear credenciales OAuth 2.0.
Sigue estos pasos:

PASO 1: Crear Proyecto en Google Cloud
─────────────────────────────────────────────────────────────
1. Ve a: https://console.cloud.google.com/
2. Haz clic en "Select a project" → "New Project"
3. Nombre: "Campo Sagrado MVP"
4. Haz clic en "Create"

PASO 2: Habilitar Google Calendar API
─────────────────────────────────────────────────────────────
1. En el proyecto, ve a: "APIs & Services" → "Library"
2. Busca: "Google Calendar API"
3. Haz clic en "Enable"

PASO 3: Crear Credenciales OAuth
─────────────────────────────────────────────────────────────
1. Ve a: "APIs & Services" → "Credentials"
2. Haz clic en "+ CREATE CREDENTIALS" → "OAuth client ID"
3. Si te pide configurar pantalla de consentimiento:
   a. Haz clic en "CONFIGURE CONSENT SCREEN"
   b. Tipo: "External"
   c. Nombre: "Campo Sagrado"
   d. Email: tu email
   e. Guarda y continúa
   
4. Vuelve a "Credentials" → "+ CREATE CREDENTIALS" → "OAuth client ID"
5. Tipo de aplicación: "Desktop app"
6. Nombre: "Campo Sagrado Desktop"
7. Haz clic en "CREATE"

PASO 4: Descargar Credenciales
─────────────────────────────────────────────────────────────
1. En la lista de OAuth 2.0 Client IDs, busca el que creaste
2. Haz clic en el icono de descarga (⬇️)
3. Guarda el archivo como: google_credentials.json
4. Mueve el archivo a: backend/config/google_credentials.json

PASO 5: Ejecutar este script nuevamente
─────────────────────────────────────────────────────────────
Una vez que tengas google_credentials.json en su lugar:

    python scripts/setup_google_calendar.py

Se abrirá tu navegador para autorizar la aplicación.

═══════════════════════════════════════════════════════════════
""")


def verificar_credenciales():
    """Verifica si existen las credenciales"""
    creds_path = backend_path / "config" / "google_credentials.json"
    return creds_path.exists()


def setup_oauth():
    """Ejecuta el flujo OAuth"""
    print("\n🔐 Iniciando flujo OAuth...\n")
    print("Se abrirá tu navegador para autorizar Campo Sagrado.")
    print("Por favor:")
    print("  1. Selecciona tu cuenta de Google")
    print("  2. Haz clic en 'Allow' cuando te pida permisos")
    print("  3. Puedes cerrar la ventana del navegador después\n")
    
    input("Presiona ENTER para continuar...")
    
    try:
        client = GoogleCalendarClient()
        
        if client.is_authenticated():
            print("\n✅ ¡Autenticación exitosa!")
            print(f"   Token guardado en: {client.token_path}")
            print("\n🎉 Google Calendar está listo para usar.\n")
            return True
        else:
            print("\n❌ Error: No se pudo completar la autenticación")
            return False
            
    except Exception as e:
        print(f"\n❌ Error durante setup: {e}")
        return False


def test_calendar():
    """Prueba la conexión con Calendar"""
    print("\n🧪 Probando conexión con Google Calendar...\n")
    
    try:
        client = GoogleCalendarClient()
        
        if not client.is_authenticated():
            print("❌ No autenticado")
            return False
        
        # Listar calendarios disponibles
        calendars = client.service.calendarList().list().execute()
        
        print("✅ Conexión exitosa!")
        print(f"\n📅 Calendarios disponibles:")
        
        for calendar in calendars.get('items', []):
            nombre = calendar.get('summary', 'Sin nombre')
            es_primario = ' (Principal)' if calendar.get('primary') else ''
            print(f"   • {nombre}{es_primario}")
        
        print("\n✨ Todo listo para crear eventos en tu calendario.\n")
        return True
        
    except Exception as e:
        print(f"❌ Error probando calendar: {e}")
        return False


def main():
    print("\n")
    print("═" * 70)
    print("🕌  CAMPO SAGRADO - Setup Google Calendar")
    print("═" * 70)
    
    # Verificar si ya tiene credenciales
    if not verificar_credenciales():
        print("\n⚠️  No se encontró google_credentials.json\n")
        print_instrucciones()
        return
    
    print("\n✅ Credenciales encontradas: config/google_credentials.json")
    
    # Verificar si ya está autenticado
    token_path = backend_path / "config" / "google_token.json"
    if token_path.exists():
        print("✅ Token de acceso encontrado")
        print("\n¿Deseas re-autenticar? (s/N): ", end='')
        respuesta = input().lower()
        
        if respuesta != 's':
            print("\nUsando token existente...")
            if test_calendar():
                return
            else:
                print("\n⚠️  Token inválido, re-autenticando...")
    
    # Ejecutar OAuth
    if setup_oauth():
        test_calendar()
    else:
        print("\n❌ Setup falló. Por favor revisa los pasos e intenta nuevamente.\n")
        print_instrucciones()


if __name__ == "__main__":
    main()

