#!/bin/bash
# Inicia todo el sistema

echo "🚀 Iniciando Campo Sagrado..."

# Trap para detener todo al salir
trap 'kill $(jobs -p) 2>/dev/null' EXIT

# Backend
if [ -d "apps/backend" ]; then
  echo "▶️  Iniciando Backend..."
  cd apps/backend
  if [ -f venv/bin/activate ]; then
    source venv/bin/activate
  fi
  export PYTHONPATH="$(pwd)"
  if [ -f run.py ]; then
    python run.py &
    BACKEND_PID=$!
  elif [ -f api/main.py ]; then
    python api/main.py &
    BACKEND_PID=$!
  else
    echo "(error) apps/backend/run.py ni apps/backend/api/main.py existen"
  fi
  cd ../..
else
  echo "(aviso) Carpeta apps/backend no encontrada"
fi

# Frontend  
if [ -d "frontend" ]; then
  echo "▶️  Iniciando Frontend..."
  cd frontend
  if command -v pnpm >/dev/null 2>&1; then
    pnpm dev &
  else
    npm run dev &
  fi
  FRONTEND_PID=$!
  cd ..
else
  echo "(aviso) Carpeta frontend no encontrada"
fi

# Agentes
if [ -d "backend" ]; then
  echo "▶️  Iniciando Agentes..."
  cd backend
  if [ -f venv/bin/activate ]; then
    source venv/bin/activate
  fi
  if [ -f scripts/start_agentes.py ]; then
    python scripts/start_agentes.py &
    AGENTES_PID=$!
  else
    echo "(info) scripts/start_agentes.py no encontrado"
  fi
  cd ..
fi

echo ""
echo "✨ Sistema iniciado"
echo "   Backend: http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo ""
echo "Presiona Ctrl+C para detener"

# Esperar
wait



