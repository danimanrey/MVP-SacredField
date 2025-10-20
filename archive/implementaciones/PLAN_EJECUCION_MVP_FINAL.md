# 🎯 Plan de Ejecución MVP - Arquitectura Final

**Fecha:** 10 de octubre, 2025  
**Objetivo:** Implementar la arquitectura completa con excelencia

---

## 🌌 **Puerto 3000 (Next.js) - DIVULGACIÓN PURA**

### **Flujo del Usuario:**

```
Primera Vez:
  localhost:3000
      ↓
  Wizard de Onboarding (4 pasos)
      ↓
  Configuración guardada
      ↓
  Redirige a primer Estado Cero

Visitas Posteriores:
  localhost:3000
      ↓
  SOLO Estado Cero Inmersivo
      ↓
  Meditación + Preguntas Sacrales
      ↓
  Dirección Emergente
      ↓
  Validación de Eventos en Google Calendar
      ↓
  Editar/Añadir/Borrar con IA
      ↓
  Guardar y Finalizar
```

### **Componentes a Implementar:**

1. **Wizard de Onboarding** (`/onboarding`)
   - Paso 1: Bienvenida
   - Paso 2: No-Negociables (5 toggles)
   - Paso 3: Contexto (financiero + biológico)
   - Paso 4: Expresión Libre
   - Guardar en backend

2. **Detección de Primera Vez**
   - Middleware que verifica si hay configuración
   - Si no hay → `/onboarding`
   - Si hay → `/estado-cero`

3. **Estado Cero Mejorado**
   - Mantener flujo inmersivo actual
   - Añadir paso final: "Validación de Calendario"
   - Mostrar eventos del día desde Google Calendar
   - Permitir editar con IA

4. **Validación de Calendario** (`/estado-cero/validacion`)
   - Mostrar eventos de Google Calendar del día
   - Estructura:
     - No-negociables (anclados, no editables)
     - Tareas hacia objetivos (editables)
     - 40% espacio emergente (editable)
   - Botones:
     - ✏️ Editar evento (con sugerencia IA)
     - ➕ Añadir evento
     - 🗑️ Eliminar evento
     - ✓ Guardar y Finalizar

---

## 📊 **Puerto 5173 (Svelte) - EJECUCIÓN**

### **Base: Espejo Diario**

```
localhost:5173
    ↓
Espejo Diario (Dashboard Principal)
    ↓
Google Calendar en tiempo real
    ↓
4 vistas temporales:
  - Diaria (horas)
  - Semanal (días + significado)
  - Mensual (semanas + significado)
  - Anual (meses + propósito)
```

### **Funcionalidades:**

1. **Espejo Diario** (`/espejo-diario`)
   - Sincronización con Google Calendar
   - Vista de horas del día
   - Eventos categorizados:
     - 🔴 No-negociables
     - 🟢 Tareas hacia objetivos
     - 🟡 Emergentes
   - Tracking: Marcar como completada
   - Salud del organismo (%)

2. **Documentación Inteligente**
   - Por cada evento, generar:
     - **Qué:** Descripción clara
     - **Cuándo:** Timing óptimo
     - **Cómo:** Pasos concretos
     - **Referencias:** Enlaces a Obsidian
   - Botón "Ver Documentación" en cada evento

3. **Consulta de Actividades**
   - Sidebar con búsqueda
   - Grafo de Obsidian integrado
   - "¿Cómo hago X?" → Claude + Obsidian

4. **Vistas Temporales**

   **Vista Semanal:**
   ```
   Semana del 7-13 Oct, 2025
   "Semana de Consolidación Financiera"
   
   Lun: Día de Planificación (🔵)
   Mar: Día de Ejecución Profunda (🟢)
   Mié: Día de Relaciones (🟣)
   Jue: Día de Creatividad (🔴)
   Vie: Día de Cierre (🟡)
   Sáb: Día de Descanso Activo (⚪)
   Dom: Día de Reflexión (🟤)
   ```

   **Vista Mensual:**
   ```
   Octubre 2025 (Mes Hijri: Rabi' al-Awwal)
   "Mes de Renacimiento y Nuevos Comienzos"
   
   Semana 1: Planificación del mes
   Semana 2: Ejecución inicial
   Semana 3: Ajuste y pivote
   Semana 4: Consolidación
   ```

   **Vista Anual:**
   ```
   2025 - Año del Entrelazamiento
   
   Cada mes con su significado:
   Enero: Nacimiento
   Febrero: Crecimiento
   ...
   Diciembre: Cierre y Reflexión
   ```

---

## 🔧 **Tareas Técnicas**

### **Fase 1: Wizard de Onboarding** (Hoy)

#### **Backend:**

1. **Modelo de Configuración:**
```python
# backend/models/schemas.py
class ConfiguracionIndividual(BaseModel):
    user_id: str
    no_negociables: NoNegociables
    dimensiones_prioritarias: List[str]
    energia_disponible: int
    contexto_financiero: ContextoFinanciero
    contexto_biologico: ContextoBiologico
    expresion_libre: Optional[str]
    fecha_creacion: datetime
```

2. **Endpoint:**
```python
# backend/api/configuracion.py
@router.post("/individual")
async def guardar_configuracion(config: ConfiguracionIndividual)

@router.get("/individual/{user_id}")
async def obtener_configuracion(user_id: str)
```

#### **Frontend (3000):**

1. **Páginas:**
   - `/onboarding/page.tsx` (wizard principal)
   - `/onboarding/components/Paso1Bienvenida.tsx`
   - `/onboarding/components/Paso2NoNegociables.tsx`
   - `/onboarding/components/Paso3Contexto.tsx`
   - `/onboarding/components/Paso4ExpresionLibre.tsx`

2. **Store:**
   - `lib/stores/onboarding-store.ts` (Zustand)

3. **Middleware:**
   - Verificar si hay configuración
   - Redirigir según caso

---

### **Fase 2: Validación de Calendario** (Mañana)

#### **Backend:**

1. **Integración Google Calendar:**
```python
# backend/integraciones/google_calendar.py (ya existe, mejorar)
def obtener_eventos_dia(fecha: date) -> List[Evento]
def crear_evento(evento: Evento) -> str
def actualizar_evento(evento_id: str, evento: Evento)
def eliminar_evento(evento_id: str)
```

2. **Endpoint de Validación:**
```python
@router.post("/validar-calendario")
async def validar_calendario(
    estado_cero_id: str,
    eventos: List[Evento]
)
```

#### **Frontend (3000):**

1. **Página de Validación:**
   - `/estado-cero/validacion/page.tsx`
   - Mostrar eventos de Google Calendar
   - Editar con sugerencias IA
   - Guardar cambios

---

### **Fase 3: Espejo Diario Funcional** (Día 3)

#### **Backend:**

1. **Endpoint Espejo:**
```python
@router.get("/espejo-diario/hoy")
async def obtener_espejo_hoy()
# Retorna eventos + salud + stats
```

2. **Documentación por Evento:**
```python
@router.get("/documentacion/{evento_id}")
async def generar_documentacion(evento_id: str)
# Claude genera qué/cuándo/cómo
```

#### **Frontend (5173):**

1. **Mejorar Espejo Diario:**
   - Integrar Google Calendar
   - Vista de horas
   - Tracking de completadas
   - Salud del organismo

---

### **Fase 4: Vistas Temporales** (Día 4-5)

1. **Vista Semanal:**
   - `/espejo-diario/semanal`
   - 7 días con significados
   - Código de colores

2. **Vista Mensual:**
   - `/espejo-diario/mensual`
   - 4 semanas + significado

3. **Vista Anual:**
   - `/espejo-diario/anual`
   - 12/13 meses + propósito

---

## 📅 **Cronograma de Ejecución**

### **Día 1 (Hoy):** Wizard de Onboarding
- ✅ Diseñar estructura
- ✅ Implementar 4 pasos
- ✅ Backend endpoints
- ✅ Guardar configuración
- ✅ Middleware de redirección

### **Día 2:** Validación de Calendario
- Mejorar integración Google Calendar
- Página de validación
- Edición con IA
- Guardar eventos

### **Día 3:** Espejo Diario Funcional
- Puerto 5173 operativo
- Google Calendar en tiempo real
- Tracking de eventos
- Salud del organismo

### **Día 4:** Documentación Inteligente
- Generar docs por evento
- Integración Obsidian
- Consulta de actividades

### **Día 5:** Vistas Temporales
- Vista semanal
- Vista mensual
- Vista anual
- Significados

---

## 🎯 **Criterios de Éxito**

### **Puerto 3000:**
✅ Primera vez → Onboarding completo  
✅ Visitas posteriores → SOLO Estado Cero  
✅ Estado Cero termina con validación de calendario  
✅ Edición inteligente de eventos  
✅ Experiencia inmersiva perfecta  

### **Puerto 5173:**
✅ Espejo Diario operativo  
✅ Google Calendar sincronizado  
✅ Documentación por evento  
✅ 4 vistas temporales funcionando  
✅ Tracking y salud visible  

---

## 🚀 **Comenzamos con Wizard de Onboarding**

Voy a implementarlo ahora mismo.

**¿Alguna preferencia de diseño o ajuste antes de comenzar?**

إن شاء الله 🕌✨

