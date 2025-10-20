from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from datetime import datetime, date

from models.database import get_db, init_db
from models.schemas import HealthResponse
from services.tiempos_liturgicos import CalculadorTiemposLiturgicos
from services.calendario_hijri import CalendarioHijri

# Inicializar base de datos
init_db()

# Crear app
app = FastAPI(
    title="Campo Sagrado API",
    description="API del organismo tecnológico-espiritual",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración
LAT = float(os.getenv("LATITUD", "40.4168"))
LON = float(os.getenv("LONGITUD", "-3.7038"))
TZ = os.getenv("TIMEZONE", "Europe/Madrid")

# Servicios globales
calculador_tiempos = CalculadorTiemposLiturgicos(LAT, LON, TZ)
calendario = CalendarioHijri()

# Incluir routers de agentes
try:
    from api import estado_cero, orquestador, guardian
    app.include_router(estado_cero.router, prefix="/api/estado-cero", tags=["Estado Cero"])
    app.include_router(orquestador.router, prefix="/api/orquestador", tags=["Orquestador"])
    app.include_router(guardian.router, prefix="/api/guardian", tags=["Guardian"])
    print("✅ Routers de agentes cargados correctamente")
except Exception as e:
    print(f"❌ Error cargando routers: {e}")


@app.get("/")
async def root():
    return {
        "nombre": "Campo Sagrado del Entrelazador",
        "version": "0.1.0-mvp",
        "status": "activo"
    }


@app.get("/api/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check con información del sistema"""
    
    # Próximo Estado Cero
    proximo = calculador_tiempos.proximo_estado_cero()
    
    # Día actual
    momento_actual = calculador_tiempos.momento_actual()
    tiempos_hoy = calculador_tiempos.calcular_tiempos_hoy()
    contexto_temporal = calendario.obtener_contexto_temporal_completo(date.today())
    dia = {
        "fecha": date.today().isoformat(),
        "mes_hijri": contexto_temporal["mes_hijri"]["nombre"],
        "dia_semana": contexto_temporal["dia_semana"]["nombre"]
    }
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        proximo_estado_cero=proximo,
        dia_actual=dia
    )


@app.get("/api/tiempos-hoy")
async def obtener_tiempos_hoy():
    """Obtiene tiempos de rezo para hoy"""
    tiempos = calculador_tiempos.calcular_tiempos_hoy()
    return tiempos


@app.get("/api/verificar-momento")
async def verificar_momento():
    """Verifica si AHORA es momento de Estado Cero"""
    verificacion = calculador_tiempos.verificar_momento_estado_cero()
    return verificacion


@app.get("/api/test-agentes")
async def test_agentes():
    """Endpoint de prueba para verificar que los agentes están disponibles"""
    try:
        from agentes.estado_cero import AgenteEstadoCero
        from agentes.orquestador import AgenteOrquestador
        from agentes.guardian import AgenteGuardian
        from agentes.documentador import AgenteDocumentador
        
        return {
            "status": "ok",
            "agentes_disponibles": [
                "AgenteEstadoCero",
                "AgenteOrquestador", 
                "AgenteGuardian",
                "AgenteDocumentador"
            ],
            "mensaje": "Todos los agentes están disponibles"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "mensaje": "Error cargando agentes"
        }
