#!/bin/bash
# Verificar coherencia del sistema Campo Sagrado

set -e

echo "🔍 ═══════════════════════════════════════"
echo "   CAMPO SAGRADO - Verificación Coherencia"
echo "═══════════════════════════════════════"

# Verificar estructura del proyecto
echo "📁 Verificando estructura del proyecto..."
required_dirs=("backend" "frontend" "config" "storage" "scripts")
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir"
    else
        echo "❌ $dir - FALTANTE"
    fi
done

echo ""

# Verificar backend
echo "🔧 Verificando Backend..."
if [ -d "backend" ]; then
    cd backend
    
    # Ambiente virtual
    if [ -d "venv" ]; then
        echo "✅ Ambiente virtual"
    else
        echo "❌ Ambiente virtual - FALTANTE"
    fi
    
    # Dependencias
    if [ -f "requirements.txt" ]; then
        echo "✅ requirements.txt"
    else
        echo "❌ requirements.txt - FALTANTE"
    fi
    
    # Script de inicio
    if [ -f "run.py" ]; then
        echo "✅ run.py (script de inicio)"
    else
        echo "❌ run.py - FALTANTE"
    fi
    
    # API Key
    if [ -f ".env" ]; then
        if grep -q "ANTHROPIC_API_KEY" .env && ! grep -q "tu_api_key_aqui" .env; then
            echo "✅ API Key configurada"
        else
            echo "⚠️  API Key no configurada o usando valor placeholder"
        fi
    else
        echo "❌ .env - FALTANTE"
    fi
    
    # Estructura de módulos
    modules=("api" "models" "services" "integraciones")
    for module in "${modules[@]}"; do
        if [ -d "$module" ]; then
            echo "✅ $module/"
        else
            echo "❌ $module/ - FALTANTE"
        fi
    done
    
    cd ..
else
    echo "❌ Carpeta backend no encontrada"
fi

echo ""

# Verificar frontend
echo "🎨 Verificando Frontend..."
if [ -d "frontend" ]; then
    cd frontend
    
    # Dependencias
    if [ -d "node_modules" ]; then
        echo "✅ node_modules"
    else
        echo "❌ node_modules - FALTANTE"
    fi
    
    # Package.json
    if [ -f "package.json" ]; then
        echo "✅ package.json"
    else
        echo "❌ package.json - FALTANTE"
    fi
    
    # Rutas principales
    routes=("+page.svelte" "estado-cero/+page.svelte" "espejo-diario/+page.svelte" "vista-semanal/+page.svelte" "vista-anual/+page.svelte")
    for route in "${routes[@]}"; do
        if [ -f "src/routes/$route" ]; then
            echo "✅ $route"
        else
            echo "❌ $route - FALTANTE"
        fi
    done
    
    cd ..
else
    echo "❌ Carpeta frontend no encontrada"
fi

echo ""

# Verificar integraciones
echo "🔗 Verificando Integraciones..."
if [ -d "~/Documents/CampoSagrado" ]; then
    echo "✅ Vault de Obsidian creado"
else
    echo "❌ Vault de Obsidian no encontrado"
fi

# Base de datos
if [ -f "storage/organismo.db" ]; then
    echo "✅ Base de datos SQLite"
else
    echo "❌ Base de datos SQLite - FALTANTE"
fi

# Datos de prueba
if [ -f "storage/datos_prueba.json" ]; then
    echo "✅ Datos de prueba generados"
else
    echo "❌ Datos de prueba - FALTANTE"
fi

echo ""

# Verificar conectividad
echo "🌐 Verificando Conectividad..."
echo "Probando backend..."
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Backend respondiendo en http://localhost:8000"
else
    echo "❌ Backend no responde en http://localhost:8000"
fi

echo "Probando frontend..."
if curl -s http://localhost:5173/ > /dev/null 2>&1; then
    echo "✅ Frontend respondiendo en http://localhost:5173"
elif curl -s http://localhost:5174/ > /dev/null 2>&1; then
    echo "✅ Frontend respondiendo en http://localhost:5174"
else
    echo "❌ Frontend no responde en puertos 5173 ni 5174"
fi

echo ""
echo "🔍 Verificación completada"
echo ""
echo "Para iniciar el sistema: ./scripts/iniciar-sistema.sh"
echo "Para ver logs: tail -f backend/logs/*.log"
