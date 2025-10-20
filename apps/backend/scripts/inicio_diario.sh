#!/bin/bash

# 🕌 Script de Inicio Diario - Campo Sagrado del Entrelazador
# ===========================================================
#
# Este script automatiza el inicio completo del sistema:
# 1. Verifica que el backend esté corriendo
# 2. Inicia el worker de ingesta
# 3. Inicia el scheduler de notificaciones
# 4. Verifica Estados Cero pendientes
# 5. Genera dashboard del día anterior si es necesario
#
# Uso: ./scripts/inicio_diario.sh

set -e  # Salir si hay error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Cambiar al directorio del backend
cd "/Users/hp/Campo sagrado MVP/backend"

log "🕌 Iniciando Campo Sagrado del Entrelazador..."

# Verificar que el entorno virtual existe
if [ ! -d "venv" ]; then
    error "No se encontró el entorno virtual en backend/venv"
    exit 1
fi

# Activar entorno virtual
log "📦 Activando entorno virtual..."
source venv/bin/activate

# Verificar que el backend esté corriendo
log "🔍 Verificando estado del backend..."
if ! curl -s http://localhost:8000/api/sistema/test > /dev/null 2>&1; then
    warning "Backend no está corriendo. Iniciando..."
    
    # Iniciar backend en background
    nohup python run.py > logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > storage/backend.pid
    
    # Esperar a que el backend esté listo
    log "⏳ Esperando que el backend esté listo..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/api/sistema/test > /dev/null 2>&1; then
            success "Backend iniciado correctamente (PID: $BACKEND_PID)"
            break
        fi
        sleep 2
        if [ $i -eq 30 ]; then
            error "Backend no respondió después de 60 segundos"
            exit 1
        fi
    done
else
    success "Backend ya está corriendo"
fi

# Iniciar worker de ingesta si no está corriendo
log "🔄 Verificando worker de ingesta..."
if [ ! -f "storage/worker.pid" ] || ! kill -0 $(cat storage/worker.pid) 2>/dev/null; then
    log "Iniciando worker de ingesta..."
    ./scripts/start_worker.sh
    if [ $? -eq 0 ]; then
        success "Worker de ingesta iniciado"
    else
        error "Error iniciando worker de ingesta"
        exit 1
    fi
else
    success "Worker de ingesta ya está corriendo (PID: $(cat storage/worker.pid))"
fi

# Iniciar scheduler de notificaciones si no está corriendo
log "⏰ Verificando scheduler de notificaciones..."
if [ ! -f "storage/scheduler.pid" ] || ! kill -0 $(cat storage/scheduler.pid) 2>/dev/null; then
    log "Iniciando scheduler de notificaciones..."
    nohup python scripts/scheduler_estados_cero.py > logs/scheduler.log 2>&1 &
    SCHEDULER_PID=$!
    echo $SCHEDULER_PID > storage/scheduler.pid
    
    if kill -0 $SCHEDULER_PID 2>/dev/null; then
        success "Scheduler iniciado (PID: $SCHEDULER_PID)"
    else
        error "Error iniciando scheduler"
        exit 1
    fi
else
    success "Scheduler ya está corriendo (PID: $(cat storage/scheduler.pid))"
fi

# Verificar Estados Cero pendientes de ayer
log "📊 Verificando Estados Cero pendientes..."
AYER=$(date -v-1d '+%Y-%m-%d')
ESTADOS_AYER=$(curl -s "http://localhost:8000/api/sistema/estado-sistema" | jq -r '.archivos_estados_recientes // 0')

if [ "$ESTADOS_AYER" -lt 5 ]; then
    warning "Solo $ESTADOS_AYER Estados Cero ayer. Esperados: 5"
    log "💡 Considera completar los Estados Cero faltantes"
else
    success "$ESTADOS_AYER Estados Cero completados ayer"
fi

# Generar dashboard del día anterior si no existe
log "📈 Verificando dashboard del día anterior..."
DASHBOARD_AYER="storage/dashboards/${AYER}-dashboard.json"
if [ ! -f "$DASHBOARD_AYER" ]; then
    log "Generando dashboard del día anterior ($AYER)..."
    
    # Ejecutar análisis del día anterior
    RESPONSE=$(curl -s "http://localhost:8000/api/sistema/analisis-completo?dias=1")
    
    if echo "$RESPONSE" | jq -e '.status == "success"' > /dev/null 2>&1; then
        success "Dashboard del día anterior generado"
    else
        warning "Error generando dashboard del día anterior"
    fi
else
    success "Dashboard del día anterior ya existe"
fi

# Mostrar resumen del sistema
log "📋 Resumen del sistema:"
echo "   - Backend: $(curl -s http://localhost:8000/api/sistema/test | jq -r '.status // "ERROR"')"
echo "   - Worker: $(if [ -f storage/worker.pid ] && kill -0 $(cat storage/worker.pid) 2>/dev/null; then echo "RUNNING"; else echo "STOPPED"; fi)"
echo "   - Scheduler: $(if [ -f storage/scheduler.pid ] && kill -0 $(cat storage/scheduler.pid) 2>/dev/null; then echo "RUNNING"; else echo "STOPPED"; fi)"
echo "   - Estados Cero ayer: $ESTADOS_AYER/5"
echo "   - Dashboard ayer: $(if [ -f "$DASHBOARD_AYER" ]; then echo "GENERADO"; else echo "PENDIENTE"; fi)"

# URLs útiles
log "🌐 URLs del sistema:"
echo "   - Estado Cero Inmersivo: http://localhost:3000/estado-cero-inmersivo"
echo "   - Dashboard: http://localhost:3000/dashboard"
echo "   - API Backend: http://localhost:8000/api/sistema/test"

success "✅ Sistema iniciado correctamente"

# Mostrar próximos pasos
log "🎯 Próximos pasos recomendados:"
echo "   1. Completar Estado Cero en el momento litúrgico actual"
echo "   2. Revisar notificaciones programadas"
echo "   3. Verificar archivos generados en Obsidian"
echo "   4. Ejecutar análisis manual si es necesario: ./scripts/analizar_ahora.sh"

log "🕌 ¡Campo Sagrado del Entrelazador está listo!"
