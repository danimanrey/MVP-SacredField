#!/bin/bash
# 🕌 Campo Sagrado - Configurador de API Key

echo "🕌 Campo Sagrado - Configuración de API Key"
echo "============================================"
echo ""

# Navegar al directorio backend
cd "$(dirname "$0")/.." || exit

# Verificar que existe el archivo .env
if [ ! -f .env ]; then
    echo "❌ Error: No se encuentra el archivo .env"
    echo "Copiando desde env.example..."
    cp env.example .env
fi

echo "Por favor, ingresa tu ANTHROPIC_API_KEY:"
echo "(Empieza con sk-ant-api03-...)"
echo ""
read -p "API Key: " api_key

# Validar formato básico
if [[ ! $api_key =~ ^sk-ant-api03- ]]; then
    echo "⚠️  Advertencia: La API key no parece tener el formato correcto"
    echo "   Debería empezar con 'sk-ant-api03-'"
    read -p "¿Continuar de todos modos? (s/n): " continuar
    if [[ $continuar != "s" && $continuar != "S" ]]; then
        echo "❌ Cancelado"
        exit 1
    fi
fi

# Actualizar el archivo .env
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s|ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=$api_key|" .env
else
    # Linux
    sed -i "s|ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=$api_key|" .env
fi

echo ""
echo "✅ API Key configurada correctamente"
echo ""
echo "🔄 Ahora necesitas reiniciar el servidor backend:"
echo "   1. Detén el servidor actual (Ctrl+C)"
echo "   2. Ejecuta: python run.py"
echo ""
echo "🧪 Para probar que funciona:"
echo "   curl http://localhost:8000/api/health"
echo ""

