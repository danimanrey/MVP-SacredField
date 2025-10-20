#!/bin/bash

# 🔍 Script de Análisis Manual - Campo Sagrado del Entrelazador
# ==============================================================
#
# Este script ejecuta análisis completo bajo demanda:
# 1. Análisis de patrones
# 2. Entrelazamiento de dominios
# 3. Generación de acciones sistémicas
# 4. Actualización del dashboard
#
# Uso: ./scripts/analizar_ahora.sh [días]
# Si no se especifican días, usa 7 por defecto

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

# Parámetros
DIAS=${1:-7}

# Cambiar al directorio del backend
cd "/Users/hp/Campo sagrado MVP/backend"

log "🔍 Ejecutando análisis completo de $DIAS días..."

# Verificar que el backend esté corriendo
log "🔍 Verificando backend..."
if ! curl -s http://localhost:8000/api/sistema/test > /dev/null 2>&1; then
    error "Backend no está corriendo. Ejecuta ./scripts/inicio_diario.sh primero"
    exit 1
fi
success "Backend está corriendo"

# Verificar Estados Cero disponibles
log "📊 Verificando Estados Cero disponibles..."
ESTADO_RESPONSE=$(curl -s "http://localhost:8000/api/sistema/estado-sistema")
ESTADOS_RECIENTES=$(echo "$ESTADO_RESPONSE" | jq -r '.archivos_estados_recientes // 0')

if [ "$ESTADOS_RECIENTES" -eq 0 ]; then
    warning "No hay Estados Cero recientes para analizar"
    log "💡 Completa algunos Estados Cero primero"
    exit 1
fi

success "Encontrados $ESTADOS_RECIENTES Estados Cero recientes"

# Ejecutar análisis completo
log "🔄 Ejecutando análisis completo..."
ANALISIS_RESPONSE=$(curl -s "http://localhost:8000/api/sistema/analisis-completo?dias=$DIAS")

# Verificar si el análisis fue exitoso
if echo "$ANALISIS_RESPONSE" | jq -e '.status == "success"' > /dev/null 2>&1; then
    success "✅ Análisis completado exitosamente"
    
    # Extraer información del análisis
    TIMESTAMP=$(echo "$ANALISIS_RESPONSE" | jq -r '.timestamp')
    RESUMEN=$(echo "$ANALISIS_RESPONSE" | jq -r '.resumen')
    
    # Mostrar resumen
    log "📈 Resumen del análisis:"
    echo "   - Estados Cero analizados: $(echo "$RESUMEN" | jq -r '.estados_cero_analizados')"
    echo "   - Dominios analizados: $(echo "$RESUMEN" | jq -r '.dominios_analizados')"
    echo "   - Entrelazamientos detectados: $(echo "$RESUMEN" | jq -r '.entrelazamientos_detectados')"
    echo "   - Acciones coordinadas: $(echo "$RESUMEN" | jq -r '.acciones_coordinadas')"
    echo "   - Acciones sistémicas: $(echo "$RESUMEN" | jq -r '.acciones_sistemicas')"
    
    # Mostrar archivos generados
    ARCHIVOS=$(echo "$ANALISIS_RESPONSE" | jq -r '.archivos_generados')
    log "📁 Archivos generados:"
    
    if [ "$(echo "$ARCHIVOS" | jq -r '.patrones // empty')" ]; then
        echo "   - Patrones: $(echo "$ARCHIVOS" | jq -r '.patrones')"
    fi
    
    if [ "$(echo "$ARCHIVOS" | jq -r '.entrelazamiento // empty')" ]; then
        echo "   - Entrelazamiento: $(echo "$ARCHIVOS" | jq -r '.entrelazamiento')"
    fi
    
    if [ "$(echo "$ARCHIVOS" | jq -r '.acciones // empty')" ]; then
        echo "   - Acciones: $(echo "$ARCHIVOS" | jq -r '.acciones')"
    fi
    
    # Mostrar patrones detectados si los hay
    PATRONES=$(echo "$ANALISIS_RESPONSE" | jq -r '.patrones // empty')
    if [ "$PATRONES" ] && [ "$(echo "$PATRONES" | jq -r '.patrones_detectados // empty')" ]; then
        log "🔍 Patrones detectados:"
        echo "$PATRONES" | jq -r '.patrones_detectados[]? | "   - \(.tipo): \(.descripcion)"'
    fi
    
    # Mostrar entrelazamientos si los hay
    ENTRELAZAMIENTOS=$(echo "$ANALISIS_RESPONSE" | jq -r '.entrelazamientos // empty')
    if [ "$ENTRELAZAMIENTOS" ] && [ "$(echo "$ENTRELAZAMIENTOS" | jq length)" -gt 0 ]; then
        log "🔗 Entrelazamientos detectados:"
        echo "$ENTRELAZAMIENTOS" | jq -r '.[] | "   - \(.dominios | join(" ↔ ")): \(.descripcion)"'
    fi
    
    # Mostrar acciones prioritarias si las hay
    ACCIONES=$(echo "$ANALISIS_RESPONSE" | jq -r '.acciones_prioritarias // empty')
    if [ "$ACCIONES" ] && [ "$(echo "$ACCIONES" | jq length)" -gt 0 ]; then
        log "⚡ Acciones prioritarias:"
        echo "$ACCIONES" | jq -r '.[] | "   - \(.nombre) (Urgencia: \(.urgencia | . * 100 | floor)%, Impacto: \(.impacto_sistémico | . * 100 | floor)%)"'
    fi
    
else
    error "❌ Error en el análisis:"
    echo "$ANALISIS_RESPONSE" | jq -r '.detail // .error // .' 2>/dev/null || echo "$ANALISIS_RESPONSE"
    exit 1
fi

# Verificar que el dashboard se actualizó
log "📊 Verificando dashboard..."
DASHBOARD_RESPONSE=$(curl -s "http://localhost:8000/api/sistema/dashboard-data")

if echo "$DASHBOARD_RESPONSE" | jq -e '.timestamp' > /dev/null 2>&1; then
    DASHBOARD_TIMESTAMP=$(echo "$DASHBOARD_RESPONSE" | jq -r '.timestamp')
    success "Dashboard actualizado (timestamp: $DASHBOARD_TIMESTAMP)"
else
    warning "Dashboard no disponible o no actualizado"
fi

# URLs útiles
log "🌐 Accede a los resultados:"
echo "   - Dashboard: http://localhost:3000/dashboard"
echo "   - API Backend: http://localhost:8000/api/sistema/dashboard-data"
echo "   - Estado Cero: http://localhost:3000/estado-cero-inmersivo"

# Información de Obsidian
OBSIDIAN_PATH=$(echo "$ESTADO_RESPONSE" | jq -r '.vault_path // "~/Documents/CampoSagrado"')
log "📚 Archivos en Obsidian:"
echo "   - Vault: $OBSIDIAN_PATH"
echo "   - Estados Cero: $OBSIDIAN_PATH/Estados-Cero/"
echo "   - Análisis: $OBSIDIAN_PATH/Analisis/"
echo "   - Acciones: $OBSIDIAN_PATH/Acciones-Sistemicas/"

# Recomendaciones
log "💡 Recomendaciones:"
echo "   1. Revisa el dashboard para insights visuales"
echo "   2. Examina los archivos generados en Obsidian"
echo "   3. Considera las acciones prioritarias sugeridas"
echo "   4. Completa Estados Cero para mejorar el análisis"

success "🎯 Análisis manual completado"

# Estadísticas finales
log "📊 Estadísticas finales:"
echo "   - Período analizado: $DIAS días"
echo "   - Estados Cero procesados: $ESTADOS_RECIENTES"
echo "   - Timestamp: $TIMESTAMP"
echo "   - Archivos generados: $(echo "$ARCHIVOS" | jq -r 'to_entries | length')"

log "🕌 ¡Análisis sistémico completado!"
