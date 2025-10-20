#!/usr/bin/env python3
"""
Script de inicio para el backend de Campo Sagrado
Establece el PYTHONPATH correctamente y ejecuta la aplicación
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Establecer el PYTHONPATH
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

# Cargar variables de entorno desde .env
env_path = backend_path / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Variables de entorno cargadas desde {env_path}")
else:
    print(f"⚠️ No se encontró archivo .env en {env_path}")

# Importar y ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn
    from api.main import app
    
    print("🕌 Iniciando Campo Sagrado Backend...")
    print(f"📁 Backend path: {backend_path}")
    print(f"🐍 Python path: {sys.path[:3]}")
    print("🚀 Servidor iniciando en http://localhost:8000")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
