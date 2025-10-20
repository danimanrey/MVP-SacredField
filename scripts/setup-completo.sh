#!/bin/bash
# Setup completo del MVP

set -e

echo "🕌 ═══════════════════════════════════════"
echo "   CAMPO SAGRADO - Setup Completo MVP"
echo "═══════════════════════════════════════"

# Backend
echo "🔧 Backend..."
if [ -d "backend" ]; then
  cd backend
  python3 -m venv venv
  source venv/bin/activate
  if [ -f requirements.txt ]; then
    pip install -r requirements.txt
  fi
  if [ -f scripts/init_db.py ]; then
    python scripts/init_db.py || true
  fi
  cd ..
else
  echo "(info) Carpeta backend no encontrada aún - puedes crearla luego."
fi

# Frontend
echo "🎨 Frontend..."
if [ -d "frontend" ]; then
  cd frontend
  if command -v pnpm >/dev/null 2>&1; then
    pnpm install
  else
    echo "(aviso) pnpm no instalado. Instala con: npm i -g pnpm"
    npm install
  fi
  cd ..
else
  echo "(info) Carpeta frontend no encontrada - crea la estructura primero."
fi

echo "✅ Setup completado"
echo ""
echo "Próximo paso:"
echo "1. Edita backend/.env con tu ANTHROPIC_API_KEY"
echo "2. Ejecuta: ./scripts/iniciar-sistema.sh"



