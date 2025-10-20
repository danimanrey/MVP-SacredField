#!/bin/bash

echo "🔍 VERIFICANDO ESTADO DEL PROYECTO"
echo "=================================="

# Backend
echo -e "\n📦 Backend:"
if [ -d "backend/venv" ]; then
    echo "  ✅ venv existe"
else
    echo "  ❌ venv NO existe - ejecuta: python3 -m venv backend/venv"
fi

if [ -f "backend/.env" ]; then
    echo "  ✅ .env existe"
    if grep -q "ANTHROPIC_API_KEY=sk-" backend/.env; then
        echo "  ✅ API key configurada"
    else
        echo "  ⚠️  API key NO configurada"
    fi
else
    echo "  ❌ .env NO existe"
fi

if [ -f "storage/organismo.db" ]; then
    echo "  ✅ Base de datos existe"
else
    echo "  ❌ Base de datos NO existe - ejecuta: python backend/scripts/init_db.py"
fi

# Frontend
echo -e "\n🎨 Frontend:"
if [ -d "frontend/node_modules" ]; then
    echo "  ✅ node_modules existe"
else
    echo "  ❌ node_modules NO existe - ejecuta: cd frontend && pnpm install"
fi

# Config
echo -e "\n⚙️  Configuración:"
if [ -f "config/campo-sagrado.yaml" ]; then
    echo "  ✅ config/campo-sagrado.yaml existe"
else
    echo "  ❌ config/campo-sagrado.yaml NO existe"
fi

if [ -f "backend/config.py" ]; then
    echo "  ✅ backend/config.py existe"
else
    echo "  ❌ backend/config.py NO existe"
fi

# Cursor
echo -e "\n🖱️  Cursor:"
if [ -f ".cursorrules" ]; then
    echo "  ✅ .cursorrules existe"
else
    echo "  ❌ .cursorrules NO existe"
fi

echo -e "\n=================================="
