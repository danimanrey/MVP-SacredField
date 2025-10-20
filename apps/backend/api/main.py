from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
import os
from datetime import datetime, date

from models.database import get_db, init_db
from models.schemas import HealthResponse
from services.tiempos_liturgicos import CalculadorTiemposLiturgicos
from services.calendario_hijri import CalendarioHijri

# Middleware de seguridad
try:
    from middleware.security import (
        SecurityHeadersMiddleware,
        RateLimitMiddleware,
        RequestLoggingMiddleware,
        SecurityValidationMiddleware
    )
    SECURITY_ENABLED = True
except ImportError:
    print("⚠️ Middleware de seguridad no disponible")
    SECURITY_ENABLED = False

# Inicializar base de datos
init_db()

# Crear app
app = FastAPI(
    title="Campo Sagrado API",
    description="API del organismo tecnológico-espiritual",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENV") != "production" else None,  # Ocultar docs en producción
    redoc_url="/redoc" if os.getenv("ENV") != "production" else None,
)

# Middleware de seguridad (orden importa)
if SECURITY_ENABLED:
    # 1. Validación de seguridad (primero)
    app.add_middleware(SecurityValidationMiddleware)
    
    # 2. Rate limiting
    app.add_middleware(RateLimitMiddleware)
    
    # 3. Security headers
    app.add_middleware(SecurityHeadersMiddleware)
    
    # 4. Request logging
    app.add_middleware(RequestLoggingMiddleware)
    
    print("✅ Middleware de seguridad activado")

# Trusted Host (solo en producción)
if os.getenv("ENV") == "production":
    allowed_hosts = os.getenv("ALLOWED_HOSTS", "").split(",")
    if allowed_hosts and allowed_hosts[0]:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
        print(f"✅ Trusted hosts configurado: {allowed_hosts}")

# CORS
cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Request-ID"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-Process-Time"],
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
    from api import estado_cero, orquestador, guardian, vistas_temporales, manifestaciones, octavas, universo_imaginal, configuracion, gobierno, pilares, arquitectura_sagrada
    
# ===== CORE ROUTERS (MVP) =====
app.include_router(estado_cero.router, prefix="/api/estado-cero", tags=["Estado Cero"])
app.include_router(orquestador.router, prefix="/api/orquestador", tags=["Orquestador"])
app.include_router(guardian.router, prefix="/api/guardian", tags=["Guardian"])
app.include_router(vistas_temporales.router, prefix="/api", tags=["Vistas Temporales"])
app.include_router(manifestaciones.router, prefix="/api/manifestaciones", tags=["Manifestaciones"])
app.include_router(octavas.router, prefix="/api/octavas", tags=["Ley de la Octava"])
# app.include_router(universo_imaginal.router, prefix="/api/universo-imaginal", tags=["Universo Imaginal"])  # Depende de universo_processor (Phase 3)
app.include_router(configuracion.router, prefix="/api/configuracion", tags=["Configuración"])

# ===== ARQUITECTURA SAGRADA: 3 PODERES DE GOBIERNO =====
app.include_router(gobierno.router, prefix="/api/gobierno", tags=["🏛️ Gobierno: 3 Poderes"])

# ===== ARQUITECTURA SAGRADA: 8 PILARES FUNDAMENTALES =====
app.include_router(pilares.router, prefix="/api/pilares", tags=["🏛️ Pilares: Verificación"])

# ===== ARQUITECTURA SAGRADA: DASHBOARD COMPLETO =====
app.include_router(arquitectura_sagrada.router, prefix="/api/arquitectura-sagrada", tags=["🕌 Arquitectura Sagrada"])
    
    # ===== V2.0 ROUTERS (dependen de agentes archivados) =====
    # from api import entrelazamiento, ritual_maghrib, estructura, espejo_diario
    # app.include_router(entrelazamiento.router, prefix="/api", tags=["Entrelazamiento"])  # Usa analizador_patrones, entrelazador_dominios
    # app.include_router(ritual_maghrib.router, prefix="/api/maghrib", tags=["Ritual Maghrib"])  # Usa entrelazador
    # app.include_router(estructura.router, prefix="/api/estructura", tags=["Estructura"])  # Usa entrelazador
    # app.include_router(espejo_diario.router, prefix="/api/espejo-diario", tags=["Espejo Diario"])  # Usa entrelazador
    
    # from api import calendario  # GoogleCalendarService pendiente
    # app.include_router(calendario.router, prefix="/api/calendario", tags=["Calendario"])
    
    print("✅ Routers CORE cargados correctamente (8 routers)")
    print("⚠️ 4 routers deshabilitados temporalmente (v2.0): entrelazamiento, ritual_maghrib, estructura, espejo_diario")
except Exception as e:
    print(f"❌ Error cargando routers: {e}")
    import traceback
    traceback.print_exc()


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


@app.get("/api/tiempos-precisos")
async def obtener_tiempos_precisos(fecha: str = None):
    """
    Obtiene tiempos litúrgicos PRECISOS en formato legible.
    
    Query params:
    - fecha: YYYY-MM-DD (opcional, default: hoy)
    
    Retorna tiempos calculados astronómicamente para tu ubicación.
    """
    if fecha:
        from datetime import datetime
        dia = datetime.strptime(fecha, "%Y-%m-%d").date()
    else:
        dia = None
    
    return calculador_tiempos.obtener_tiempos_formato_legible(dia)


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


# ==================== CALENDARIO HIJRI ====================

@app.get("/api/calendario-hijri/hoy")
async def obtener_dia_hijri_hoy():
    """Obtiene el contexto del día actual en el calendario Hijri"""
    contexto = calendario.obtener_contexto_temporal_completo(date.today())
    return contexto


@app.get("/api/calendario-hijri/año")
async def obtener_año_hijri(año_hijri: int = None):
    """
    Obtiene todos los meses de un año Hijri específico.
    Si no se especifica año, retorna el año actual.
    """
    return calendario.obtener_vista_anual(date.today())


@app.get("/api/tiempos-liturgicos/hoy")
async def obtener_tiempos_liturgicos_hoy():
    """Obtiene los tiempos de rezo precisos para el día actual"""
    tiempos = calculador_tiempos.calcular_tiempos_hoy()
    momento_actual = calculador_tiempos.momento_actual()
    proximo_rezo = calculador_tiempos.proximo_estado_cero()
    
    return {
        "fecha": date.today().isoformat(),
        "ubicacion": {
            "latitud": LAT,
            "longitud": LON,
            "ciudad": "San Sebastián de los Reyes"
        },
        "tiempos_rezo": tiempos,
        "momento_actual": momento_actual["nombre"],
        "proximo_rezo": proximo_rezo["nombre"],
        "tiempo_hasta_proximo": proximo_rezo.get("minutos_hasta", 0)
    }

