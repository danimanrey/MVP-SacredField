#!/usr/bin/env python3
"""
Script para generar secretos seguros para producción
Ejecutar antes de deploy
"""

import secrets
import string

def generar_jwt_secret(length: int = 64) -> str:
    """Genera un secret key aleatorio para JWT."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generar_api_key(length: int = 32) -> str:
    """Genera una API key URL-safe."""
    return secrets.token_urlsafe(length)

if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════╗")
    print("║                                                        ║")
    print("║   🔐 GENERADOR DE SECRETOS SEGUROS                   ║")
    print("║                                                        ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    print("🔑 JWT SECRET KEY (para .env):")
    print(f"JWT_SECRET_KEY={generar_jwt_secret()}")
    print()
    
    print("🔑 API KEY (para integraciones):")
    print(f"API_KEY={generar_api_key()}")
    print()
    
    print("⚠️  IMPORTANTE:")
    print("  • Copia estos valores a tu archivo .env")
    print("  • NUNCA los compartas o los commits a git")
    print("  • Genera nuevos secretos para cada entorno")
    print("  • En producción, usa un secrets manager")
    print()
    
    print("مَا شَاءَ ٱللَّٰهُ")

