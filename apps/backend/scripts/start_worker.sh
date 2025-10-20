#!/bin/bash

# Script para iniciar el worker de ingesta
# Campo Sagrado del Entrelazador

cd "/Users/hp/Campo sagrado MVP/backend"

# Verificar que el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Error: No se encontró el entorno virtual en backend/venv"
    exit 1
fi

# Activar entorno virtual
source venv/bin/activate

# Verificar que el worker existe
if [ ! -f "workers/ingest_worker.py" ]; then
    echo "❌ Error: No se encontró el worker en workers/ingest_worker.py"
    exit 1
fi

# Crear directorio storage si no existe
mkdir -p storage

# Verificar si ya hay un worker corriendo
if [ -f "storage/worker.pid" ] && kill -0 $(cat storage/worker.pid) 2>/dev/null; then
    echo "⚠️ Ya hay un worker corriendo (PID: $(cat storage/worker.pid))"
    echo "¿Quieres detenerlo y reiniciar? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        kill $(cat storage/worker.pid)
        rm storage/worker.pid
        echo "🛑 Worker anterior detenido"
    else
        echo "❌ No se inició el nuevo worker"
        exit 1
    fi
fi

# Iniciar worker en background
echo "🔄 Iniciando worker de ingesta..."
python workers/ingest_worker.py &
worker_pid=$!

# Guardar PID
echo $worker_pid > storage/worker.pid

# Verificar que el proceso está corriendo
sleep 2
if kill -0 $worker_pid 2>/dev/null; then
    echo "✅ Worker iniciado correctamente (PID: $worker_pid)"
    echo "📁 PID guardado en: storage/worker.pid"
    echo "📝 Logs del worker se muestran en esta terminal"
else
    echo "❌ Error: No se pudo iniciar el worker"
    rm -f storage/worker.pid
    exit 1
fi
