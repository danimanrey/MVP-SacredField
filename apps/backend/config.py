"""
Configuración centralizada del Campo Sagrado
"""
import os
from pathlib import Path
from typing import Optional

# Rutas del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_ROOT = Path(__file__).parent
FRONTEND_ROOT = PROJECT_ROOT / "frontend"
STORAGE_ROOT = PROJECT_ROOT / "storage"
CONFIG_ROOT = PROJECT_ROOT / "config"

# Configuración de la aplicación
APP_NAME = "Campo Sagrado del Entrelazador"
APP_VERSION = "0.1.0-mvp"
APP_DESCRIPTION = "Organismo tecnológico-espiritual que opera al borde del caos"

# Configuración de base de datos
DATABASE_URL = f"sqlite:///{STORAGE_ROOT}/organismo.db"

# Configuración de localización
# San Sebastián de los Reyes, Madrid (coordenadas precisas)
LATITUD = float(os.getenv("LATITUD", "40.5472"))  # 40°32'50"N
LONGITUD = float(os.getenv("LONGITUD", "-3.6228"))  # 3°37'22"W
TIMEZONE = os.getenv("TIMEZONE", "Europe/Madrid")
CIUDAD = "San Sebastián de los Reyes"
PAIS = "España"

# Configuración de API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY no está configurada en las variables de entorno")

# Configuración de integraciones
OBSIDIAN_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "~/Documents/CampoSagrado")
ANYTYPE_API_KEY = os.getenv("ANYTYPE_API_KEY")  # Opcional

# Configuración de CORS
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174", 
    "http://localhost:3000",
    "http://localhost:8080"
]

# Configuración de Estados Cero
ESTADOS_CERO_DIARIOS = [
    "fajr",
    "dhuhr", 
    "asr",
    "maghrib",
    "isha"
]

# Configuración de calendario Hijri (12 meses lunares)
MESES_HIJRI = [
    "Muharram", "Safar", "Rabi' al-Awwal", "Rabi' al-Thani",
    "Jumada al-Awwal", "Jumada al-Thani", "Rajab", "Sha'ban",
    "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"
]

# Meses sagrados (حُرُم)
MESES_SAGRADOS_HIJRI = [1, 7, 11, 12]  # Muharram, Rajab, Dhu al-Qi'dah, Dhu al-Hijjah

# Configuración de no-negociables
TIPOS_NO_NEGOCIABLES = [
    "biologico",
    "espiritual", 
    "financiero"
]

# Configuración de energía
ESCALA_ENERGIA = {
    "min": 1,
    "max": 5,
    "default": 3
}

# Configuración de jornada
ESPACIO_EMERGENCIA_PORCENTAJE = 40
BLOQUES_TIEMPO_DEFAULT = 120  # minutos

# Configuración de documentación
DOCUMENTOS_OBSIDIAN = {
    "estados_cero": "50-Conversaciones-IA/Estados-Cero",
    "reportes_diarios": "40-Journal",
    "insights_semanales": "40-Journal",
    "sesiones_trabajo": "30-Sesiones"
}

# Configuración de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configuración de desarrollo
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
RELOAD = DEBUG

# Configuración de servidor
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Validación de configuración
def validar_configuracion():
    """Valida que la configuración esté completa"""
    errores = []
    
    if not ANTHROPIC_API_KEY:
        errores.append("ANTHROPIC_API_KEY no configurada")
    
    if not os.path.exists(STORAGE_ROOT):
        errores.append(f"Directorio storage no existe: {STORAGE_ROOT}")
    
    if not os.path.exists(CONFIG_ROOT):
        errores.append(f"Directorio config no existe: {CONFIG_ROOT}")
    
    if errores:
        raise ValueError(f"Configuración incompleta: {', '.join(errores)}")
    
    return True

# Inicializar configuración
if __name__ == "__main__":
    try:
        validar_configuracion()
        print("✅ Configuración válida")
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
