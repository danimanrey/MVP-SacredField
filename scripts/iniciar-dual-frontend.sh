#!/bin/bash

# 🌉 Script de Inicio Dual Frontend
# Inicia Backend + Svelte + Next.js simultáneamente

echo "🕌 Campo Sagrado - Arquitectura Dual Frontend"
echo "================================================"
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Directorio base
BASE_DIR="/Users/hp/Campo sagrado MVP"
SVELTE_DIR="$BASE_DIR/frontend"
NEXTJS_DIR="$BASE_DIR/campo-sagrado-nextjs"
BACKEND_DIR="$BASE_DIR/backend"

# Función para verificar si un puerto está en uso
check_port() {
    lsof -i :$1 > /dev/null 2>&1
}

# Verificar Backend
echo -e "${BLUE}[1/3]${NC} Verificando Backend (Puerto 8000)..."
if check_port 8000; then
    echo -e "${GREEN}✓${NC} Backend ya está corriendo"
else
    echo -e "${YELLOW}⚡${NC} Iniciando Backend..."
    cd "$BACKEND_DIR"
    source venv/bin/activate
    python run.py > /dev/null 2>&1 &
    sleep 3
    if check_port 8000; then
        echo -e "${GREEN}✓${NC} Backend iniciado correctamente"
    else
        echo -e "${RED}✗${NC} Error iniciando Backend"
        exit 1
    fi
fi

# Verificar Svelte
echo ""
echo -e "${BLUE}[2/3]${NC} Verificando Svelte (Puerto 5173)..."
if check_port 5173; then
    echo -e "${GREEN}✓${NC} Svelte ya está corriendo"
else
    echo -e "${YELLOW}⚡${NC} Iniciando Svelte..."
    cd "$SVELTE_DIR"
    npm run dev > /dev/null 2>&1 &
    sleep 3
    if check_port 5173; then
        echo -e "${GREEN}✓${NC} Svelte iniciado correctamente"
    else
        echo -e "${RED}✗${NC} Error iniciando Svelte"
    fi
fi

# Verificar Next.js
echo ""
echo -e "${BLUE}[3/3]${NC} Verificando Next.js (Puerto 3000)..."
if [ ! -d "$NEXTJS_DIR" ]; then
    echo -e "${YELLOW}⚠${NC} Next.js no existe todavía"
    echo -e "${YELLOW}ℹ${NC} Para crearlo, ejecuta:"
    echo ""
    echo "  cd \"$BASE_DIR\""
    echo "  npx create-next-app@latest campo-sagrado-nextjs \\"
    echo "    --typescript --tailwind --app --src-dir --import-alias \"@/*\""
    echo ""
else
    if check_port 3000; then
        echo -e "${GREEN}✓${NC} Next.js ya está corriendo"
    else
        echo -e "${YELLOW}⚡${NC} Iniciando Next.js..."
        cd "$NEXTJS_DIR"
        npm run dev > /dev/null 2>&1 &
        sleep 3
        if check_port 3000; then
            echo -e "${GREEN}✓${NC} Next.js iniciado correctamente"
        else
            echo -e "${RED}✗${NC} Error iniciando Next.js"
        fi
    fi
fi

# Resumen
echo ""
echo "================================================"
echo -e "${GREEN}✨ Sistema Dual Frontend Activo${NC}"
echo "================================================"
echo ""
echo "📊 URLs Disponibles:"
echo ""
echo -e "  ${BLUE}Backend:${NC}  http://localhost:8000"
echo -e "            http://localhost:8000/docs"
echo ""
echo -e "  ${GREEN}Svelte:${NC}   http://localhost:5173  ${YELLOW}(Ejecutivo)${NC}"
echo -e "            🎯 Validación funcional"
echo ""
if [ -d "$NEXTJS_DIR" ]; then
    echo -e "  ${GREEN}Next.js:${NC}  http://localhost:3000  ${YELLOW}(Inmersivo)${NC}"
    echo -e "            🌌 Experiencia beta testers"
else
    echo -e "  ${RED}Next.js:${NC}  (No instalado aún)"
fi
echo ""
echo "================================================"
echo ""
echo "💡 Tips:"
echo "  • Svelte (5173): Desarrollo rápido de funcionalidad"
echo "  • Next.js (3000): Testing de experiencia inmersiva"
echo "  • Backend (8000): Fuente única de verdad"
echo ""
echo "🛑 Para detener todos los servicios:"
echo "   bash scripts/detener-sistema.sh"
echo ""

