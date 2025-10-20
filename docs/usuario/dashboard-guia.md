# 🕌 Dashboard de Entrelazamiento Personal - Guía Completa

## ✅ Estado: FUNCIONANDO

El **Dashboard de Entrelazamiento Personal** está completamente implementado y operativo en el MVP de Campo Sagrado.

---

## 🎯 ¿Qué es el Dashboard de Entrelazamiento?

Es un sistema inteligente que reconoce tu configuración individual y entrelaza TODOS los aspectos de tu vida:

- 💪 **Rutinas Deportivas** - Cuándo, qué tipo, intensidad
- 🍽️ **Sistema de Comidas** - Planificación, batch cooking, tiempos de preparación
- 💰 **Gestión Financiera** - Presupuesto, categorías, alertas, compras
- 📚 **Aprendizaje** - Temas activos, prioridades, tiempo semanal
- 💻 **Desarrollo** - Proyectos, hitos, deadlines
- 📈 **Inversiones** - Decisiones pendientes, seguimiento

El agente detecta automáticamente:
- ⚠️ **Conflictos** - Días sobrecargados, actividades que compiten
- ✨ **Sinergias** - Combinaciones que potencian productividad
- 🔄 **Optimizaciones** - Sugerencias para mejor balance
- 🌀 **Espacios de Emergencia** - 40% de la semana para lo imprevisto

---

## 🚀 Cómo Usar el Sistema

### **Paso 1: Configurar tu API Key**

Edita el archivo `.env`:

```bash
cd "Campo sagrado MVP/backend"
nano .env

# Reemplaza con tu API key real:
ANTHROPIC_API_KEY=sk-ant-api03-TU-CLAVE-AQUI
```

> **Nota**: El sistema funciona SIN API key (modo mock), pero con ella obtienes recomendaciones personalizadas de Claude.

### **Paso 2: Iniciar el Backend**

```bash
cd "Campo sagrado MVP/backend"
source venv/bin/activate
python run.py
```

El servidor estará en: `http://localhost:8000`

### **Paso 3: Cargar tu Perfil Personal**

Edita el archivo `backend/scripts/perfil_ejemplo.py` con TUS datos reales:

```python
# Personaliza:
- Tus rutinas deportivas (días, horarios, tipo)
- Tu sistema de comidas (batch cooking, recetas, restricciones)
- Tu presupuesto mensual (categorías, montos)
- Tus temas de aprendizaje (prioridades, recursos)
- Tus proyectos de desarrollo (deadlines, hitos)
- Tus asuntos de inversión (decisiones pendientes)
```

Luego carga tu perfil:

```bash
cd backend/scripts
python perfil_ejemplo.py

# Esto genera perfil_ejemplo.json

# Cárgalo en el sistema:
curl -X POST http://localhost:8000/api/entrelazamiento/perfil \
  -H "Content-Type: application/json" \
  -d @perfil_ejemplo.json
```

### **Paso 4: Ver tu Dashboard Semanal**

```bash
# Dashboard completo
curl http://localhost:8000/api/entrelazamiento/dashboard-semanal | python -m json.tool

# Resumen ejecutivo (más compacto)
curl http://localhost:8000/api/entrelazamiento/resumen-semana | python -m json.tool

# Análisis de sinergias
curl http://localhost:8000/api/entrelazamiento/analisis/sinergias | python -m json.tool

# Análisis de conflictos
curl http://localhost:8000/api/entrelazamiento/analisis/conflictos | python -m json.tool
```

---

## 📊 Endpoints Disponibles

### **Gestión de Perfil**

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/entrelazamiento/perfil` | POST | Cargar perfil completo |
| `/api/entrelazamiento/perfil-actual` | GET | Ver perfil cargado |
| `/api/entrelazamiento/perfil/rutina-deportiva` | POST | Agregar rutina deportiva |
| `/api/entrelazamiento/perfil/comida` | POST | Agregar configuración de comida |
| `/api/entrelazamiento/perfil/presupuesto` | POST | Agregar categoría de presupuesto |
| `/api/entrelazamiento/perfil/tema-aprendizaje` | POST | Agregar tema de aprendizaje |
| `/api/entrelazamiento/perfil/proyecto` | POST | Agregar proyecto de desarrollo |
| `/api/entrelazamiento/perfil/inversion` | POST | Agregar asunto de inversión |

### **Dashboard y Análisis**

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/entrelazamiento/dashboard-semanal` | GET | Dashboard completo de la semana |
| `/api/entrelazamiento/resumen-semana` | GET | Resumen ejecutivo |
| `/api/entrelazamiento/analisis/conflictos` | GET | Conflictos detectados |
| `/api/entrelazamiento/analisis/sinergias` | GET | Sinergias identificadas |

---

## 💡 Ejemplo de Respuesta del Dashboard

```json
{
  "semana_inicio": "2025-10-07",
  "semana_fin": "2025-10-13",
  "deportes": {
    "sesiones_planificadas": 6,
    "objetivo_cumplido": true
  },
  "finanzas": {
    "gasto_proyectado": 300.0,
    "presupuesto_disponible": 590.0,
    "alertas": ["Gimnasio: 100% usado"]
  },
  "desarrollo": {
    "horas_aprendizaje": 19.0,
    "temas_prioridad": ["Machine Learning Avanzado", "Filosofía Estoica"],
    "horas_proyectos": 28.0,
    "proyectos_activos": 3
  },
  "optimizacion": {
    "sugerencias": [
      "🔄 Semana muy demandante - considera mover actividades no urgentes",
      "⚡ 6 días sobrecargados - redistribuye carga"
    ],
    "patron_energia": {
      "lunes": 10,
      "martes": 10,
      "promedio": 9.7,
      "dia_pico": "lunes"
    }
  }
}
```

---

## 🔗 Integración con Estado Cero

El **Estado Cero** ahora usa tu perfil personal para generar preguntas más relevantes:

```bash
# Iniciar Estado Cero
curl -X POST http://localhost:8000/api/estado-cero/iniciar \
  -H "Content-Type: application/json" \
  -d '{"momento": "fajr"}'
```

Las preguntas binarias considerarán:
- Tus deportes programados hoy
- Tus proyectos activos
- Tus temas de aprendizaje prioritarios
- Tus decisiones financieras pendientes
- Tu configuración de batch cooking

---

## 📈 Análisis Inteligente

### **Detección de Conflictos**

El sistema detecta automáticamente:
- ⚠️ Días sobrecargados (energía > 8)
- ⚠️ Batch cooking + proyecto demandante el mismo día
- ⚠️ Tiempo total excesivo (>8 horas)
- ⚠️ Múltiples actividades de alta intensidad

### **Detección de Sinergias**

El sistema identifica:
- ✨ Ejercicio matutino + proyectos creativos
- ✨ Batch cooking libera tiempo futuro
- ✨ Día balanceado (cuerpo, mente, creación)

### **Espacios de Emergencia**

Siguiendo la regla del **40% sin asignar**, el sistema identifica automáticamente días de baja demanda perfectos para lo emergente.

---

## 🎯 Próximos Pasos

### **Frontend Visualización**

El backend está listo. Próximo: crear componentes visuales en SvelteKit:

- 📊 Dashboard visual con gráficos
- 📅 Calendario semanal interactivo
- ⚡ Indicadores de energía por día
- 🎨 Visualización de sinergias y conflictos

### **Recomendaciones con IA**

Con tu API key configurada, Claude generará:
- Recomendaciones específicas por día
- Ajustes de planificación optimizados
- Insights sobre patrones personales

### **Tracking Real**

Agregar funcionalidad de tracking:
- ✅ Marcar deportes completados
- ✅ Tracking de presupuesto en tiempo real
- ✅ Avance de proyectos
- ✅ Biometría (HRV, sueño)

---

## 🧪 Tests Realizados

✅ Perfil de ejemplo cargado correctamente
✅ Dashboard semanal generado
✅ Resumen ejecutivo funcionando
✅ Análisis de sinergias (8 detectadas)
✅ Análisis de conflictos (3 detectados)
✅ Integración con Estado Cero
✅ Detección de días sobrecargados
✅ Patrón de energía semanal calculado

---

## 📝 Notas Importantes

1. **Sin API Key**: El sistema funciona en modo mock, generando datos básicos
2. **Con API Key**: Obtienes recomendaciones personalizadas de Claude Sonnet 4
3. **Perfil Persistente**: El perfil se mantiene en memoria mientras el servidor corre
4. **Base de Datos**: Próximo paso es persistir el perfil en SQLite
5. **Documentación Automática**: Ver Swagger docs en `http://localhost:8000/docs`

---

## 🔥 ¡Tu Agente de Entrelazamiento está FUNCIONANDO!

El sistema está operativo y listo para uso real. Solo necesitas:

1. ✅ Configurar tu ANTHROPIC_API_KEY en `.env`
2. ✅ Personalizar `perfil_ejemplo.py` con tus datos
3. ✅ Cargar tu perfil en el sistema
4. ✅ Consultar tu dashboard y ajustar tu semana

---

**Estado**: ✅ **MVP COMPLETO Y PROBADO**

**Fecha**: 7 de Octubre, 2025 - 21:45 hrs

🕌 *Campo Sagrado respeta tu autoridad sacral y entrelaza todos los aspectos de tu vida al borde del caos.*



