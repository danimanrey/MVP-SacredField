# 🚀 Inicio Rápido - Campo Sagrado MVP

## **Paso 1: Configurar API Key (2 minutos)**

### Opción A: Script Interactivo (Recomendado)

```bash
cd "Campo sagrado MVP/backend/scripts"
./configurar_api_key.sh
```

El script te pedirá tu API key de Anthropic.

### Opción B: Manual

```bash
cd "Campo sagrado MVP/backend"
nano .env

# Reemplaza esta línea:
ANTHROPIC_API_KEY=sk-ant-api03-tu-clave-aqui

# Con tu API key real:
ANTHROPIC_API_KEY=sk-ant-api03-TU_CLAVE_REAL_AQUI

# Guarda: Ctrl+O, Enter, Ctrl+X
```

### ¿No tienes API Key?

1. Ve a: https://console.anthropic.com/
2. Inicia sesión o crea cuenta
3. Ve a "API Keys" → "Create Key"
4. Copia la clave (empieza con `sk-ant-api03-`)

---

## **Paso 2: Reiniciar el Servidor (1 minuto)**

```bash
# Detener servidor actual
lsof -ti:8000 | xargs kill -9

# Iniciar con la nueva configuración
cd "Campo sagrado MVP/backend"
source venv/bin/activate
python run.py
```

Verás:
```
✅ Claude client inicializado con API key real
✅ Routers de agentes cargados correctamente
INFO: Uvicorn running on http://0.0.0.0:8000
```

---

## **Paso 3: Personalizar tu Perfil (5-10 minutos)**

### Opción A: Asistente Interactivo (Recomendado)

```bash
cd "Campo sagrado MVP/backend/scripts"
python personalizar_perfil.py
```

El asistente te preguntará paso a paso:

- 💪 **Rutinas deportivas** (días, horarios, tipo)
- 🍽️ **Sistema de comidas** (batch cooking, recetas)
- 💰 **Presupuesto mensual** (categorías, montos)
- 📚 **Temas de aprendizaje** (prioridades, recursos)
- 💻 **Proyectos de desarrollo** (deadlines, hitos)
- 📈 **Inversiones** (decisiones pendientes)

Al final genera: `mi_perfil_personal.json`

### Opción B: Editar Ejemplo

```bash
cd "Campo sagrado MVP/backend/scripts"
nano perfil_ejemplo.py

# Edita con TUS datos:
- Línea 50: Tus rutinas deportivas
- Línea 90: Tu sistema de comidas
- Línea 130: Tu presupuesto
- Línea 170: Tus temas de aprendizaje
- Línea 220: Tus proyectos
- Línea 280: Tus inversiones

# Genera el JSON:
python perfil_ejemplo.py
```

---

## **Paso 4: Cargar tu Perfil (30 segundos)**

```bash
cd "Campo sagrado MVP/backend/scripts"

# Si usaste el asistente:
curl -X POST http://localhost:8000/api/entrelazamiento/perfil \
  -H "Content-Type: application/json" \
  -d @mi_perfil_personal.json

# Si editaste el ejemplo:
curl -X POST http://localhost:8000/api/entrelazamiento/perfil \
  -H "Content-Type: application/json" \
  -d @perfil_ejemplo.json
```

Deberías ver:
```json
{
  "success": true,
  "mensaje": "✅ Perfil de [Tu Nombre] cargado correctamente",
  "resumen": {
    "rutinas_deportivas": 3,
    "sistema_comidas": 3,
    ...
  }
}
```

---

## **Paso 5: Consultar tu Dashboard (¡YA ESTÁ LISTO!)**

### Resumen Ejecutivo

```bash
curl -s http://localhost:8000/api/entrelazamiento/resumen-semana | python -m json.tool
```

Verás:
- ✅ Sesiones deportivas planificadas
- 💰 Presupuesto disponible y alertas
- 📚 Horas de aprendizaje y temas prioritarios
- 💻 Proyectos activos y horas planificadas
- 🔄 Sugerencias de optimización
- ⚡ Patrón de energía semanal

### Dashboard Completo

```bash
curl -s http://localhost:8000/api/entrelazamiento/dashboard-semanal | python -m json.tool
```

Incluye día por día:
- Deportes programados
- Comidas y batch cooking
- Temas de estudio sugeridos
- Proyectos con tiempo asignado
- Decisiones financieras urgentes

### Análisis de Sinergias

```bash
curl -s http://localhost:8000/api/entrelazamiento/analisis/sinergias | python -m json.tool
```

Detecta combinaciones beneficiosas:
- ✨ "Ejercicio matutino potencia creatividad"
- ✨ "Batch cooking libera tiempo futuro"
- ✨ "Día balanceado: cuerpo, mente, creación"

### Análisis de Conflictos

```bash
curl -s http://localhost:8000/api/entrelazamiento/analisis/conflictos | python -m json.tool
```

Detecta problemas:
- ⚠️ Días sobrecargados
- ⚠️ Actividades que compiten
- ⚠️ Tiempo total excesivo

---

## **Paso 6: Usar Estado Cero Personalizado**

Ahora el Estado Cero usa tu perfil para generar preguntas más relevantes:

```bash
# Iniciar Estado Cero
curl -X POST http://localhost:8000/api/estado-cero/iniciar \
  -H "Content-Type: application/json" \
  -d '{"momento": "fajr"}'
```

Las preguntas considerarán:
- Tus deportes de hoy
- Tus proyectos activos
- Tus decisiones pendientes
- Tu configuración de batch cooking

---

## **Acceso Rápido**

### Documentación Interactiva
```
http://localhost:8000/docs
```

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Ver Perfil Actual
```bash
curl http://localhost:8000/api/entrelazamiento/perfil-actual
```

---

## **Comandos Útiles**

### Ver todos los endpoints disponibles
```bash
curl -s http://localhost:8000/openapi.json | \
  python -c "import sys, json; print('\n'.join(sorted(json.load(sys.stdin)['paths'].keys())))"
```

### Detener servidor
```bash
lsof -ti:8000 | xargs kill -9
```

### Ver logs en tiempo real
```bash
tail -f /tmp/campo-sagrado.log
```

### Actualizar perfil
```bash
# Edita tu archivo JSON y recarga:
curl -X POST http://localhost:8000/api/entrelazamiento/perfil \
  -H "Content-Type: application/json" \
  -d @mi_perfil_personal.json
```

---

## **Próximos Pasos**

### 1. Frontend Visual (Opcional)

```bash
# En otra terminal
cd "Campo sagrado MVP/frontend"
npm install
npm run dev

# Acceder a: http://localhost:5173
```

### 2. Usa el Sistema Diariamente

- **5 veces al día**: Estado Cero en momentos litúrgicos
- **Cada mañana**: Consulta tu dashboard semanal
- **Cada domingo**: Revisa sinergias y conflictos, ajusta tu semana

### 3. Evoluciona tu Perfil

A medida que conoces mejor tus patrones:
- Ajusta rutinas deportivas
- Optimiza batch cooking
- Refina presupuesto
- Actualiza prioridades de proyectos

---

## **Solución de Problemas**

### "Module not found"
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### "Address already in use"
```bash
lsof -ti:8000 | xargs kill -9
```

### "API Key no funciona"
- Verifica que empiece con `sk-ant-api03-`
- Asegúrate de no tener espacios al inicio/final
- Verifica que tienes créditos en tu cuenta Anthropic

### "Perfil no cargado"
```bash
# Verifica que el servidor esté corriendo
curl http://localhost:8000/api/health

# Recarga el perfil
curl -X POST http://localhost:8000/api/entrelazamiento/perfil \
  -H "Content-Type: application/json" \
  -d @mi_perfil_personal.json
```

---

## **¿Necesitas Ayuda?**

- 📖 Guía completa: `DASHBOARD_ENTRELAZAMIENTO_GUIA.md`
- 🔧 API Docs: http://localhost:8000/docs
- 📝 Ver ejemplos: `backend/scripts/perfil_ejemplo.py`

---

🕌 **¡Tu agente de entrelazamiento personal está listo!**

*Campo Sagrado respeta tu autoridad sacral y entrelaza todos los aspectos de tu vida al borde del caos.*

