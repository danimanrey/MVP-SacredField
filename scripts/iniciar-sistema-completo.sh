#!/bin/bash

# 🕌 CAMPO SAGRADO - SCRIPT DE INICIO COMPLETO
# Sistema de operación diaria

echo "🕌 Iniciando Campo Sagrado del Entrelazador..."
echo "================================================"

# Verificar que estamos en el directorio correcto
if [ ! -f "backend/api/main.py" ]; then
    echo "❌ Error: Ejecutar desde el directorio raíz del proyecto"
    exit 1
fi

# Función para verificar si un puerto está en uso
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️ Puerto $1 ya está en uso"
        return 1
    else
        echo "✅ Puerto $1 disponible"
        return 0
    fi
}

# Verificar puertos
echo "🔍 Verificando puertos..."
check_port 8000 || echo "   Backend ya ejecutándose"
check_port 5173 || echo "   Frontend ya ejecutándose"

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p "obsidian_vault/50-Conversaciones-IA/Estados-Cero"
mkdir -p "obsidian_vault/40-Journal"
mkdir -p "storage"

# Iniciar backend
echo "🚀 Iniciando backend..."
cd backend
source venv/bin/activate

# Verificar dependencias
echo "📦 Verificando dependencias..."
python -c "import anthropic, fastapi, sqlalchemy; print('✅ Dependencias OK')" || {
    echo "❌ Error en dependencias"
    exit 1
}

# Iniciar servidor backend en background
echo "🌐 Iniciando servidor API..."
nohup python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Esperar a que el backend esté listo
echo "⏳ Esperando backend..."
sleep 3

# Verificar que el backend responde
if curl -s http://localhost:8000/api/health > /dev/null; then
    echo "✅ Backend funcionando correctamente"
else
    echo "❌ Error: Backend no responde"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Volver al directorio raíz
cd ..

# Iniciar frontend
echo "🎨 Iniciando frontend..."
cd frontend

# Verificar dependencias de frontend
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias de frontend..."
    npm install
fi

# Iniciar servidor frontend en background
echo "🌐 Iniciando servidor frontend..."
nohup npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

# Volver al directorio raíz
cd ..

# Crear archivo de PIDs para detener el sistema
echo "$BACKEND_PID" > .pids/backend.pid
echo "$FRONTEND_PID" > .pids/frontend.pid

# Esperar a que el frontend esté listo
echo "⏳ Esperando frontend..."
sleep 5

# Verificar que el frontend responde
if curl -s http://localhost:5173 > /dev/null; then
    echo "✅ Frontend funcionando correctamente"
else
    echo "⚠️ Frontend puede estar iniciándose aún..."
fi

echo ""
echo "🎉 CAMPO SAGRADO INICIADO CORRECTAMENTE"
echo "======================================"
echo "📊 Backend API: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo "🎨 Frontend: http://localhost:5173"
echo "📝 Obsidian Vault: $(pwd)/obsidian_vault"
echo ""
echo "🛑 Para detener: ./scripts/detener-sistema.sh"
echo "📋 Para logs: tail -f logs/backend.log logs/frontend.log"
echo ""
echo "✨ El organismo tecnológico-espiritual está operativo"
echo "   Respeta la autoridad sacral del usuario"
echo "   Opera al borde del caos"
echo "   Documenta automáticamente en Obsidian"
echo ""
