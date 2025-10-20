#!/bin/bash

# 🕌 CAMPO SAGRADO - VERIFICACIÓN DEL SISTEMA
# Script para verificar que todos los componentes están funcionando

echo "🕌 Verificando Campo Sagrado del Entrelazador..."
echo "================================================"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar estado
show_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

# Función para mostrar advertencia
show_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# Verificar estructura de directorios
echo "📁 Verificando estructura de directorios..."
[ -d "backend" ] && show_status 0 "Backend" || show_status 1 "Backend"
[ -d "frontend" ] && show_status 0 "Frontend" || show_status 1 "Frontend"
[ -d "storage" ] && show_status 0 "Storage" || show_status 1 "Storage"
[ -d "obsidian_vault" ] && show_status 0 "Obsidian Vault" || show_status 1 "Obsidian Vault"
[ -d "config" ] && show_status 0 "Config" || show_status 1 "Config"
[ -d "scripts" ] && show_status 0 "Scripts" || show_status 1 "Scripts"

echo ""

# Verificar Python y dependencias
echo "🐍 Verificando Python y dependencias..."
cd backend

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    
    # Verificar Python
    python --version > /dev/null 2>&1 && show_status 0 "Python" || show_status 1 "Python"
    
    # Verificar dependencias críticas
    python -c "import fastapi" > /dev/null 2>&1 && show_status 0 "FastAPI" || show_status 1 "FastAPI"
    python -c "import sqlalchemy" > /dev/null 2>&1 && show_status 0 "SQLAlchemy" || show_status 1 "SQLAlchemy"
    python -c "import anthropic" > /dev/null 2>&1 && show_status 0 "Anthropic" || show_status 1 "Anthropic"
    python -c "import pytz" > /dev/null 2>&1 && show_status 0 "Pytz" || show_status 1 "Pytz"
    
else
    show_status 1 "Virtual Environment"
fi

echo ""

# Verificar Node.js y dependencias
echo "📦 Verificando Node.js y dependencias..."
cd ../frontend

if command -v node > /dev/null 2>&1; then
    show_status 0 "Node.js"
    node --version
    
    if [ -f "package.json" ]; then
        show_status 0 "Package.json"
        
        if [ -d "node_modules" ]; then
            show_status 0 "Node Modules"
        else
            show_warning "Node modules no instalados. Ejecutar: npm install"
        fi
    else
        show_status 1 "Package.json"
    fi
else
    show_status 1 "Node.js"
fi

echo ""

# Verificar base de datos
echo "🗄️ Verificando base de datos..."
cd ../backend
source venv/bin/activate

python -c "
from models.database import get_db, EstadoCeroDB
try:
    db = next(get_db())
    count = db.query(EstadoCeroDB).count()
    print('✅ Base de datos: OK')
    print(f'   Registros: {count}')
except Exception as e:
    print('❌ Base de datos: Error')
    print(f'   Error: {e}')
" 2>/dev/null || show_status 1 "Base de datos"

echo ""

# Verificar servicios
echo "🔧 Verificando servicios..."
python -c "
from services.claude_client import ClaudeClient
from services.tiempos_liturgicos import CalculadorTiemposLiturgicos
from services.calendario_hijri import CalendarioHijri

try:
    claude = ClaudeClient()
    print('✅ Claude Client: OK')
    
    calculador = CalculadorTiemposLiturgicos(40.4168, -3.7038, 'Europe/Madrid')
    print('✅ Calculador Tiempos: OK')
    
    calendario = CalendarioHijri()
    print('✅ Calendario Hijri: OK')
    
except Exception as e:
    print('❌ Servicios: Error')
    print(f'   Error: {e}')
" 2>/dev/null

echo ""

# Verificar agentes
echo "🤖 Verificando agentes..."
python -c "
from agentes.estado_cero import AgenteEstadoCero
from agentes.orquestador import AgenteOrquestador
from agentes.guardian import AgenteGuardian
from agentes.documentador import AgenteDocumentador
from services.claude_client import ClaudeClient
from models.database import get_db

try:
    db = next(get_db())
    claude = ClaudeClient()
    
    estado_cero = AgenteEstadoCero(db, claude, None)
    print('✅ Agente Estado Cero: OK')
    
    orquestador = AgenteOrquestador(db, claude, None)
    print('✅ Agente Orquestador: OK')
    
    guardian = AgenteGuardian(db, claude)
    print('✅ Agente Guardian: OK')
    
    documentador = AgenteDocumentador(db, claude, '/tmp/test')
    print('✅ Agente Documentador: OK')
    
except Exception as e:
    print('❌ Agentes: Error')
    print(f'   Error: {e}')
" 2>/dev/null

echo ""

# Verificar puertos
echo "🌐 Verificando puertos..."
cd ..

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    show_status 0 "Puerto 8000 (Backend)"
else
    show_warning "Puerto 8000 libre (Backend no ejecutándose)"
fi

if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1; then
    show_status 0 "Puerto 5173 (Frontend)"
else
    show_warning "Puerto 5173 libre (Frontend no ejecutándose)"
fi

echo ""

# Verificar archivos de configuración
echo "⚙️ Verificando configuración..."
[ -f "config/campo-sagrado.env" ] && show_status 0 "Archivo de configuración" || show_status 1 "Archivo de configuración"
[ -f "scripts/iniciar-sistema-completo.sh" ] && show_status 0 "Script de inicio" || show_status 1 "Script de inicio"

echo ""

# Resumen final
echo "📊 RESUMEN DEL SISTEMA"
echo "====================="

# Contar errores (simplificado)
ERRORS=0

# Verificaciones básicas
[ ! -d "backend" ] && ERRORS=$((ERRORS + 1))
[ ! -d "frontend" ] && ERRORS=$((ERRORS + 1))
[ ! -f "backend/venv/bin/activate" ] && ERRORS=$((ERRORS + 1))
[ ! -f "frontend/package.json" ] && ERRORS=$((ERRORS + 1))

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}🎉 SISTEMA LISTO PARA OPERACIÓN DIARIA${NC}"
    echo ""
    echo "Para iniciar el sistema completo:"
    echo "  ./scripts/iniciar-sistema-completo.sh"
    echo ""
    echo "Para iniciar solo el backend:"
    echo "  cd backend && source venv/bin/activate && python -m uvicorn api.main:app --reload"
    echo ""
    echo "Para iniciar solo el frontend:"
    echo "  cd frontend && npm run dev"
    echo ""
    echo "✨ El organismo tecnológico-espiritual está preparado"
    echo "   Respeta la autoridad sacral del usuario"
    echo "   Opera al borde del caos"
    echo "   Documenta automáticamente en Obsidian"
else
    echo -e "${RED}❌ SISTEMA REQUIERE CONFIGURACIÓN ADICIONAL${NC}"
    echo ""
    echo "Errores encontrados: $ERRORS"
    echo "Revisar los elementos marcados con ❌ arriba"
fi

echo ""
