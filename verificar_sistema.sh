#!/bin/bash

# Script de verificación del Sistema Organismo Completo
# Verifica que todos los componentes estén implementados correctamente

echo "🕌 Verificando Sistema Organismo Completo - Configuración 0.01%"
echo "================================================================"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
TOTAL=0
PASSED=0
FAILED=0

check() {
    TOTAL=$((TOTAL + 1))
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗${NC} $1"
        FAILED=$((FAILED + 1))
    fi
}

# 1. Verificar archivos del backend
echo "📦 1. Verificando Backend..."
[ -f "backend/services/obsidian_structure.py" ]
check "obsidian_structure.py"

[ -f "backend/services/pregunta_liturgica.py" ]
check "pregunta_liturgica.py"

[ -f "backend/services/audit_trail.py" ]
check "audit_trail.py"

[ -f "backend/services/espejo_diario_generator.py" ]
check "espejo_diario_generator.py"

[ -f "backend/services/hrv_integration.py" ]
check "hrv_integration.py"

[ -f "backend/api/estado_cero_ultra_simple.py" ]
check "estado_cero_ultra_simple.py"

[ -f "backend/api/sistema_entrelazamiento.py" ]
check "sistema_entrelazamiento.py"

[ -f "backend/scripts/setup_vault_structure.py" ]
check "setup_vault_structure.py"

echo ""

# 2. Verificar frontend
echo "🎨 2. Verificando Frontend..."
[ -f "campo-sagrado-nextjs/app/espejo-diario/page.tsx" ]
check "espejo-diario/page.tsx"

[ -f "campo-sagrado-nextjs/package.json" ]
check "package.json"

# Verificar si react-markdown está instalado
if [ -d "campo-sagrado-nextjs/node_modules/react-markdown" ]; then
    echo -e "${GREEN}✓${NC} react-markdown instalado"
    PASSED=$((PASSED + 1))
    TOTAL=$((TOTAL + 1))
else
    echo -e "${YELLOW}⚠${NC} react-markdown no instalado (ejecuta: cd campo-sagrado-nextjs && npm install react-markdown)"
    TOTAL=$((TOTAL + 1))
fi

echo ""

# 3. Verificar documentación
echo "📚 3. Verificando Documentación..."
[ -f "SISTEMA_ORGANISMO_COMPLETO.md" ]
check "SISTEMA_ORGANISMO_COMPLETO.md"

[ -f "INICIO_RAPIDO_SISTEMA_COMPLETO.md" ]
check "INICIO_RAPIDO_SISTEMA_COMPLETO.md"

[ -f "README_V2.md" ]
check "README_V2.md"

echo ""

# 4. Verificar estructura de directorios
echo "📁 4. Verificando Estructura de Directorios..."
[ -d "backend/services" ]
check "backend/services/"

[ -d "backend/scripts" ]
check "backend/scripts/"

[ -d "backend/agentes" ]
check "backend/agentes/"

[ -d "campo-sagrado-nextjs/app" ]
check "campo-sagrado-nextjs/app/"

echo ""

# 5. Verificar Obsidian Vault (si existe)
echo "🗂️  5. Verificando Obsidian Vault..."
VAULT_PATH="$HOME/Documents/CampoSagrado"

if [ -d "$VAULT_PATH" ]; then
    echo -e "${GREEN}✓${NC} Vault existe en $VAULT_PATH"
    PASSED=$((PASSED + 1))
    TOTAL=$((TOTAL + 1))
    
    # Verificar carpetas principales
    [ -d "$VAULT_PATH/00_System" ]
    check "00_System/"
    
    [ -d "$VAULT_PATH/10_Biologia_Ritmos" ]
    check "10_Biologia_Ritmos/"
    
    [ -d "$VAULT_PATH/80_Espejos_Diarios" ]
    check "80_Espejos_Diarios/"
    
    [ -d "$VAULT_PATH/00_System/Audit_Trail" ]
    check "00_System/Audit_Trail/"
else
    echo -e "${YELLOW}⚠${NC} Vault no existe. Ejecuta: cd backend && python scripts/setup_vault_structure.py"
    TOTAL=$((TOTAL + 1))
fi

echo ""

# Resumen
echo "================================================================"
echo "📊 Resumen de Verificación"
echo "================================================================"
echo -e "Total de checks: $TOTAL"
echo -e "${GREEN}Pasados: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Fallidos: $FAILED${NC}"
fi

echo ""

# Evaluación final
PERCENTAGE=$((PASSED * 100 / TOTAL))

if [ $PERCENTAGE -eq 100 ]; then
    echo -e "${GREEN}🎉 ¡Sistema 100% Completo! Configuración 0.01% verificada.${NC}"
    echo ""
    echo "🚀 Próximos pasos:"
    echo "  1. Iniciar backend: cd backend && python run.py"
    echo "  2. Iniciar frontend: cd campo-sagrado-nextjs && npm run dev"
    echo "  3. Abrir http://localhost:3000"
elif [ $PERCENTAGE -ge 80 ]; then
    echo -e "${YELLOW}⚠️  Sistema casi completo ($PERCENTAGE%). Revisar warnings arriba.${NC}"
else
    echo -e "${RED}❌ Sistema incompleto ($PERCENTAGE%). Revisar errores arriba.${NC}"
fi

echo ""
echo "📖 Documentación completa en:"
echo "  - INICIO_RAPIDO_SISTEMA_COMPLETO.md"
echo "  - SISTEMA_ORGANISMO_COMPLETO.md"
echo ""
echo "🕌 Sistema operando al borde del caos - 40% capacidad sin asignar"

