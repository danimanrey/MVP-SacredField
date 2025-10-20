#!/bin/bash
# Test de integración total - Sistema 7 Capas

echo "🔥 Testing Integración Total - Sistema 7 Capas"
echo ""

# Test 1: Endpoint /iniciar con modo_testing
echo "Test 1: POST /api/estado-cero/iniciar (modo_testing=true)"
curl -s -X POST 'http://localhost:8000/api/estado-cero/iniciar?modo_testing=true' \
  -H "Content-Type: application/json" \
  -d '{
    "momento": "dhuhr",
    "energia": 4,
    "calidad_sueno": 3,
    "resonancia_corporal": "fluido",
    "estado_emocional": "entusiasmado",
    "intensidad_emocional": 4
  }' | python3 -m json.tool

echo ""
echo "✅ Test completado"
