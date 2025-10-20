# 🌉 Guía de Integración Next.js + Backend

## Estado Actual: ✅ INTEGRACIÓN COMPLETADA

**Fecha:** 8 de octubre de 2025
**Progreso:** 40% de la migración completa

---

## 🎯 Lo que ya funciona

### Backend (FastAPI)
✅ API completa operativa en `http://localhost:8000`
✅ 30+ endpoints documentados
✅ Calendario Hijri con precisión astronómica
✅ Ley de la Octava implementada
✅ 7 Dimensiones del Ser
✅ Estado Cero con Claude AI
✅ Guardian monitoreando el sistema

### Frontend (Next.js)
✅ Cliente API TypeScript completo
✅ 8 Custom Hooks para datos en tiempo real
✅ Dashboard principal con integración backend
✅ 6 componentes 3D funcionando
✅ Audio generativo con Tone.js
✅ Post-processing avanzado

---

## 🌐 URLs Disponibles

### Next.js (Frontend)
```
Home:       http://localhost:3000
Dashboard:  http://localhost:3000/dashboard   ⭐ NUEVO - CON DATOS REALES
Demo:       http://localhost:3000/demo        (datos mock)
```

### FastAPI (Backend)
```
API:        http://localhost:8000
Docs:       http://localhost:8000/docs
Health:     http://localhost:8000/health
```

---

## 📦 Arquitectura de Integración

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO (Browser)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              NEXT.JS FRONTEND (Port 3000)                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Pages/Routes                                        │  │
│  │  • /dashboard (datos reales)                         │  │
│  │  • /demo (datos mock)                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Custom Hooks (src/hooks/useCampoSagrado.ts)        │  │
│  │  • useContextoTemporal()                             │  │
│  │  • useDimensionPrioritaria()                         │  │
│  │  • useEspejoDiario()                                 │  │
│  │  • useVerificacionEstadoCero()                       │  │
│  │  • useEstadoSistema()                                │  │
│  │  • useDimensiones()                                  │  │
│  │  • useShocksHoy()                                    │  │
│  │  • useHoraActual()                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Client (src/lib/api/client.ts)                 │  │
│  │  • Fetch con TypeScript                              │  │
│  │  • Error handling                                    │  │
│  │  • Type safety completo                              │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────┘
                         │ HTTP/REST
                         │ (fetch API)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            FASTAPI BACKEND (Port 8000)                      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Endpoints                                       │  │
│  │  • /api/estado-cero/*                                │  │
│  │  • /api/orquestador/*                                │  │
│  │  • /api/guardian/*                                   │  │
│  │  • /api/octavas/*                                    │  │
│  │  • /api/manifestaciones/*                            │  │
│  │  • /api/tiempos-liturgicos/*                         │  │
│  │  • /api/calendario-hijri/*                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Services                                            │  │
│  │  • CalendarioHijri                                   │  │
│  │  • TiemposLiturgicos                                 │  │
│  │  • GestorOctavas                                     │  │
│  │  • MotorPrisma                                       │  │
│  │  • ClaudeClient                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Database (SQLite)                                   │  │
│  │  • Estados Cero                                      │  │
│  │  • Objetivos                                         │  │
│  │  • Fragmentos de contexto                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Componentes Clave

### 1. API Client (`src/lib/api/client.ts`)

Cliente TypeScript para comunicarse con el backend.

**Características:**
- ✅ Type-safe (interfaces TypeScript)
- ✅ Error handling automático
- ✅ Base URL configurable por env
- ✅ 30+ métodos para todos los endpoints

**Uso:**
```typescript
import { api } from '@/lib/api/client';

// Obtener contexto temporal
const contexto = await api.getContextoTemporal();

// Verificar momento de Estado Cero
const verificacion = await api.verificarMomentoEstadoCero();

// Obtener dimensión prioritaria
const dimension = await api.getDimensionPrioritariaHoy();
```

---

### 2. Custom Hooks (`src/hooks/useCampoSagrado.ts`)

Hooks de React para gestionar estado y data fetching.

**Hooks disponibles:**

#### `useContextoTemporal()`
```typescript
const { contexto, loading, error } = useContextoTemporal();
// Actualiza cada 1 minuto
// Retorna: fecha Hijri, tiempos de rezo, mes actual
```

#### `useDimensionPrioritaria()`
```typescript
const { dimension, loading, error } = useDimensionPrioritaria();
// Obtiene la dimensión del día (basada en Ley de la Octava)
// Retorna: nota, color, arquetipo, pregunta clave
```

#### `useEspejoDiario(fecha?)`
```typescript
const { espejo, loading, error } = useEspejoDiario();
// Actualiza cada 5 minutos
// Retorna: bloques del día, estadísticas, insight
```

#### `useVerificacionEstadoCero()`
```typescript
const { verificacion, loading, error, recargar } = useVerificacionEstadoCero();
// Actualiza cada 2 minutos
// Retorna: es_momento, tiempo_disponible, próximo_rezo
```

#### `useEstadoSistema()`
```typescript
const { estado, loading, error } = useEstadoSistema();
// Actualiza cada 30 segundos
// Retorna: estado del Guardian, métricas, alertas
```

#### `useBackendHealth()`
```typescript
const { isHealthy, loading } = useBackendHealth();
// Actualiza cada 10 segundos
// Retorna: true si backend responde
```

---

### 3. Dashboard Page (`src/app/dashboard/page.tsx`)

**Página principal con datos reales del backend.**

**Componentes visuales:**
- ✅ Canvas 3D con React Three Fiber
- ✅ Espiral Cósmica (evolución de octavas)
- ✅ Timeline Vertical (bloques del día - **CON DATOS REALES**)
- ✅ Círculo Semanal (7 días de la semana)
- ✅ Calendario Orbital (12 meses Hijri)
- ✅ Geometría Sagrada (Flor de la Vida shader)

**Overlays informativos:**
- ✅ Contexto Temporal (mes Hijri, cualidad)
- ✅ Dimensión Prioritaria (nota del día, pregunta clave)
- ✅ Estado Cero (verificación en tiempo real)
- ✅ Guardian (métricas del sistema)
- ✅ Indicador de conexión con backend

**Actualizaciones en tiempo real:**
- Contexto temporal: cada 1 minuto
- Espejo Diario: cada 5 minutos
- Verificación Estado Cero: cada 2 minutos
- Estado del Guardian: cada 30 segundos
- Health check: cada 10 segundos
- Hora actual: cada 1 segundo

---

## 🚀 Cómo usar

### 1. Iniciar Backend
```bash
cd "/Users/hp/Campo sagrado MVP/backend"
source venv/bin/activate
python run.py
```

### 2. Iniciar Frontend
```bash
cd "/Users/hp/campo-sagrado-nextjs"
npm run dev
```

### 3. Acceder
```
Home:       http://localhost:3000
Dashboard:  http://localhost:3000/dashboard  ⭐ USA ESTO
Demo:       http://localhost:3000/demo
```

---

## 📊 Diferencias: Demo vs Dashboard

| Característica | `/demo` | `/dashboard` |
|----------------|---------|--------------|
| Datos | Mock (hardcoded) | **Reales (backend API)** ⭐ |
| Timeline | Ejemplo estático | **Bloques dinámicos del día** |
| Contexto Temporal | Hardcoded | **Calendario Hijri real** |
| Dimensión Prioritaria | Fijo (Jueves) | **Basado en día actual** |
| Estado Cero | Mock | **Verificación en tiempo real** |
| Actualizaciones | No | **Sí (cada minuto/segundos)** |
| Guardian | No | **Sí (métricas reales)** |
| Audio | Hardcoded (SOL) | **Nota del día actual** |

**Conclusión:** El `/dashboard` es la versión **funcional real** del sistema.

---

## 🎨 Flujo de Datos

### Ejemplo: Cargar el Dashboard

1. **Usuario** accede a `http://localhost:3000/dashboard`

2. **Next.js** renderiza la página, que usa los hooks:
   ```typescript
   const { contexto } = useContextoTemporal();
   const { dimension } = useDimensionPrioritaria();
   const { espejo } = useEspejoDiario();
   ```

3. **Hooks** llaman al API client:
   ```typescript
   api.getContextoTemporal()     → GET http://localhost:8000/api/calendario-hijri/hoy
   api.getDimensionPrioritariaHoy() → GET http://localhost:8000/api/octavas/dimension-hoy
   api.getEspejoDiario()         → GET http://localhost:8000/api/orquestador/espejo-diario/...
   ```

4. **Backend** procesa las solicitudes:
   - `CalendarioHijri` calcula fecha Hijri con `hijri-converter`
   - `GestorOctavas` determina dimensión del día
   - `Orquestador` construye plan del día

5. **Backend** retorna JSON con los datos

6. **Frontend** recibe los datos y actualiza la UI:
   - Canvas 3D muestra timeline con bloques reales
   - Overlays muestran contexto temporal
   - Indicadores actualizan en tiempo real

7. **Actualizaciones automáticas** continúan en background

---

## 🔍 Debugging

### Ver logs del backend
```bash
tail -f /tmp/campo-backend.log
```

### Ver logs del frontend
```bash
tail -f /tmp/nextjs-integrated.log
```

### Verificar endpoints manualmente
```bash
# Health check
curl http://localhost:8000/health

# Contexto temporal
curl http://localhost:8000/api/calendario-hijri/hoy

# Dimensión prioritaria
curl http://localhost:8000/api/octavas/dimension-hoy

# Espejo Diario
curl http://localhost:8000/api/orquestador/espejo-diario/2025-10-08
```

### Verificar que ambos servidores estén corriendo
```bash
lsof -ti:8000  # Backend
lsof -ti:3000  # Frontend
```

---

## 🐛 Problemas Comunes

### 1. Backend desconectado
**Síntoma:** Indicador rojo en dashboard "⚠️ Backend Desconectado"

**Solución:**
```bash
cd "/Users/hp/Campo sagrado MVP/backend"
source venv/bin/activate
python run.py
```

### 2. CORS errors
**Síntoma:** Error en consola del browser: "CORS policy blocked"

**Solución:** Verificar que el backend tenga CORS habilitado para `http://localhost:3000`:
```python
# backend/api/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Datos no se actualizan
**Síntoma:** Dashboard muestra datos viejos

**Solución:** Recargar la página (F5). Los hooks tienen intervalos de actualización automática.

### 4. Error 404 en endpoints
**Síntoma:** API client recibe 404

**Solución:** Verificar que el endpoint existe en `backend/api/main.py` y que el router está incluido.

---

## 📈 Próximos Pasos

### Semana 3-4: Funcionalidad Completa
- [ ] Página de Estado Cero funcional (iniciar, responder preguntas)
- [ ] Página de Espejo Diario (vista detallada, edición)
- [ ] Integración completa con Obsidian
- [ ] Vista Semanal navegable
- [ ] Vista Anual interactiva

### Semana 5-6: Componentes Restantes
- [ ] Migrar `ConsultaSacral.svelte` → React
- [ ] Migrar `ChatClarificador.svelte` → React
- [ ] Migrar `JornadaCaos.svelte` → React
- [ ] Migrar componentes de Dimensiones
- [ ] Sistema de notificaciones

### Semana 7: Refinamiento
- [ ] Optimización de performance
- [ ] Responsive design (móvil, tablet)
- [ ] Tests E2E
- [ ] Accesibilidad (a11y)

### Semana 8: Deploy
- [ ] Build de producción
- [ ] Deploy en Vercel (frontend)
- [ ] Deploy backend (Railway/Fly.io)
- [ ] CI/CD pipeline
- [ ] Documentación final

---

## 🎉 Logros hasta ahora

✅ **Cliente API completo** (300 líneas)
✅ **8 Custom Hooks** para data fetching
✅ **Dashboard funcional** con datos reales
✅ **Integración backend exitosa**
✅ **6 componentes 3D** operativos
✅ **Audio generativo** con Tone.js
✅ **Post-processing** avanzado
✅ **Actualizaciones en tiempo real**

---

## 📚 Referencias

- **API Documentation:** `docs/API_REFERENCE.md`
- **Arquitectura Técnica:** `docs/ARQUITECTURA_TECNICA.md`
- **Plan de Migración:** `PLAN_MIGRACION_NEXTJS.md`
- **Ley de la Octava:** `LEY_DE_LA_OCTAVA_IMPLEMENTACION.md`

---

**مَا شَاءَ ٱللَّٰهُ**

La integración está viva. El organismo respira.

إن شاء الله

