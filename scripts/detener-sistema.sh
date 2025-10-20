#!/bin/bash

echo "🛑 DETENIENDO CAMPO SAGRADO"
echo "=========================="

# Detener backend
echo "📦 Deteniendo backend..."
if pgrep -f "python run.py" > /dev/null; then
    pkill -f "python run.py"
    echo "  ✅ Backend detenido"
else
    echo "  ℹ️  Backend no estaba ejecutándose"
fi

# Detener frontend
echo "🎨 Deteniendo frontend..."
if pgrep -f "vite dev" > /dev/null; then
    pkill -f "vite dev"
    echo "  ✅ Frontend detenido"
else
    echo "  ℹ️  Frontend no estaba ejecutándose"
fi

# Detener procesos en puertos específicos
echo "🔌 Liberando puertos..."
if lsof -ti:8000 > /dev/null 2>&1; then
    lsof -ti:8000 | xargs kill -9
    echo "  ✅ Puerto 8000 liberado"
fi

if lsof -ti:5173 > /dev/null 2>&1; then
    lsof -ti:5173 | xargs kill -9
    echo "  ✅ Puerto 5173 liberado"
fi

if lsof -ti:5174 > /dev/null 2>&1; then
    lsof -ti:5174 | xargs kill -9
    echo "  ✅ Puerto 5174 liberado"
fi

echo ""
echo "🎉 Sistema detenido completamente"
echo "=========================="

