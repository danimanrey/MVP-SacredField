# 🏛️ Arquitectura Dual Definitiva - Campo Sagrado

**Validada:** 10 de octubre, 2025  
**Filosofía:** Divulgación vs Ejecución

---

## 🎭 Los Dos Reinos

### 🌌 **Puerto 3000 - DIVULGACIÓN** (Next.js)
**"El Portal del Asombro"**

#### Propósito
- Cara al cliente
- Gratuito
- Causa preguntas, admiración, asombro
- Expresión libre del individuo
- **Entrada** al Campo Sagrado

#### Responsabilidades
1. **Estado Cero Inmersivo**
   - Meditación espacial con 3D (R3F)
   - Esfera/cubo sagrados
   - Preguntas emergentes
   - Dirección del día

2. **Configuración Individual**
   - No-negociables (anclados por defecto)
   - Dimensiones prioritarias
   - Contexto financiero/biológico
   - Expresión libre

3. **Generación de Actividades**
   - Procesamiento sin prisa
   - Actividades propuestas por Claude
   - **Usuario valida/modifica**

4. **Documentación**
   - Genera archivo en Obsidian
   - Añade eventos a Google Calendar
   - **Trabajo COMPLETADO** → pasa a 5173

#### Stack Tecnológico
```
- Next.js 14 (App Router)
- TypeScript
- React Three Fiber (3D)
- Framer Motion (animaciones)
- Tailwind CSS
- Zustand (state management)
```

#### Rutas Principales
```
/                    → Landing inmersivo
/estado-cero         → Estado Cero inmersivo
/onboarding          → Configuración inicial
/validacion          → Validar actividades propuestas
```

---

### 📊 **Puerto 5173 - EJECUCIÓN** (Svelte)
**"El Reino Táctico"**

#### Propósito
- Operativo/ejecutivo
- Gestión del reino
- Perspicacia analítica
- Resuelve complejidad técnica
- **Ejecución** táctica

#### Responsabilidades
1. **Espejo Diario Ejecutivo**
   - Dashboard de salud del organismo
   - Tabla dinámica de actividades
   - Tracking de completadas
   - Métricas en tiempo real

2. **Gestión Táctica**
   - Añadir/editar actividades manualmente
   - Sincronización con Google Calendar
   - Al borde del caos (40% sin asignar)

3. **Integración Anytype**
   - Vista orientada a objetos
   - Gestión visual de relaciones

4. **APIs Técnicas**
   - Universo Imaginal (testing)
   - Endpoints operativos
   - Debugging y monitoreo

5. **Validación Maghrib**
   - Revisar salud del día
   - Insights automáticos
   - Preparar descanso

#### Stack Tecnológico
```
- SvelteKit
- TypeScript
- D3.js (visualizaciones)
- Tailwind CSS
- Stores nativos de Svelte
```

#### Rutas Principales
```
/                       → Dashboard principal
/espejo-diario          → Gestión ejecutiva del día
/maghrib                → Validación de salud
/universo-imaginal      → Testing de grafo (operativo)
/api/*                  → Endpoints técnicos
```

---

## 🔄 Flujo Completo del Día

### **1. Amanecer (Fajr) - Puerto 3000**

```
Usuario → localhost:3000
         ↓
    Estado Cero Inmersivo
         ↓
    Meditación espacial
         ↓
    6 preguntas sacrales
         ↓
    Dirección emergente
         ↓
    Claude genera actividades propuestas
         ↓
    Usuario valida/modifica
         ↓
    Se genera documentación en Obsidian
         ↓
    Eventos se añaden a Google Calendar
         ↓
    ✅ TRABAJO DEL 3000 COMPLETADO
```

### **2. Durante el Día - Puerto 5173**

```
Usuario → localhost:5173
         ↓
    Espejo Diario Ejecutivo
         ↓
    Ve actividades del día en tabla
         ↓
    Ejecuta actividades tácticamente
         ↓
    Marca como completadas
         ↓
    Añade emergentes manualmente
         ↓
    Gestión del reino (40% al borde del caos)
         ↓
    Puede abrir en Anytype (futuro)
```

### **3. Atardecer (Maghrib) - Puerto 5173**

```
Usuario → localhost:5173/maghrib
         ↓
    Validación de salud del organismo
         ↓
    Tasa de completitud
         ↓
    Balance de dimensiones trabajadas
         ↓
    Insights automáticos de Claude
         ↓
    Estado: "saludable" o "necesita_atencion"
         ↓
    Sistema descansa 🌙
```

---

## 🎯 Principios de Diseño

### **Puerto 3000 - Inmersivo**

#### Visual
- Fondo oscuro espacial
- Estrellas animadas
- Geometría sagrada 3D
- Transiciones suaves
- Tipografía grande y espaciada

#### UX
- Flujo guiado (no navegación libre)
- Una cosa a la vez
- Pausas contemplativas
- Sin prisa
- Asombro y cuestionamiento

#### Tono
- Poético
- Contemplativo
- Sagrado
- Invitador
- Gratuito

### **Puerto 5173 - Ejecutivo**

#### Visual
- Interfaz limpia y funcional
- Tablas y grids
- Colores por dimensión
- Métricas visibles
- Dashboard denso

#### UX
- Navegación libre
- Multi-tarea
- Acciones rápidas
- Atajos de teclado
- Eficiencia

#### Tono
- Directo
- Analítico
- Táctico
- Operativo
- Perspicaz

---

## 🚫 Lo que NO va en cada puerto

### **Puerto 3000 NO tiene:**
❌ Tablas de datos  
❌ Dashboard ejecutivo  
❌ Edición manual de actividades  
❌ Testing técnico  
❌ APIs operativas  
❌ Espejo Diario ejecutivo  

### **Puerto 5173 NO tiene:**
❌ Estado Cero inmersivo  
❌ Meditación 3D  
❌ Onboarding del usuario  
❌ Generación de actividades  
❌ Validación inicial del plan  

---

## 📦 Estructura de Datos Compartida

### **Backend (Puerto 8000) - Fuente Única de Verdad**

```python
# Todos los datos fluyen por el backend

EstadoCero (tabla)
├── id
├── momento_liturgico
├── preguntas
├── respuestas
├── direccion_emergente
├── accion_tangible
└── archivo_path (Obsidian)

Actividad (tabla)
├── id
├── titulo
├── dimension
├── hora
├── duracion
├── completada
├── fuente ('estado_cero' | 'manual')
└── estado_cero_id (FK)

ConfiguracionIndividual (tabla)
├── user_id
├── no_negociables (JSON)
├── dimensiones_prioritarias (JSON)
├── contexto_financiero (JSON)
├── contexto_biologico (JSON)
└── expresion_libre (TEXT)

ValidacionMaghrib (tabla)
├── fecha
├── tasa_completitud
├── insights (JSON)
└── estado_salud
```

---

## 🔌 APIs por Puerto

### **APIs usadas por Puerto 3000**

```
POST /api/estado-cero/verificar
POST /api/estado-cero/iniciar
POST /api/estado-cero/{id}/responder
POST /api/estado-cero/{id}/sintetizar
POST /api/estado-cero/{id}/finalizar

POST /api/planificacion/generar-plan-dia
POST /api/planificacion/validar-plan

GET  /api/configuracion/individual
POST /api/configuracion/individual
```

### **APIs usadas por Puerto 5173**

```
GET  /api/espejo-diario/hoy
POST /api/espejo-diario/actualizar

GET  /api/actividades/hoy
POST /api/actividades/crear
PUT  /api/actividades/{id}/completar
DELETE /api/actividades/{id}

POST /api/maghrib/validar-salud

GET  /api/universo-imaginal/* (testing)
```

---

## 🎨 Paletas de Color

### **Puerto 3000 - Divulgación**
```
Fondo: #0a0a1e (azul oscuro profundo)
Primario: #8B5CF6 (púrpura místico)
Secundario: #3B82F6 (azul estelar)
Acento: #22C55E (verde vida)
Texto: #F9FAFB (blanco casi puro)
```

### **Puerto 5173 - Ejecución**
```
Fondo: #1e1e3a (azul oscuro menos intenso)
Primario: #3B82F6 (azul ejecutivo)
Secundario: #8B5CF6 (púrpura)
Dimensiones: Arcoíris completo (7 colores)
Texto: #E5E7EB (gris claro)
```

---

## 📱 Responsividad

### **Puerto 3000**
- **Móvil:** Experiencia completa (táctil)
- **Tablet:** Experiencia optimizada
- **Desktop:** Experiencia inmersiva total

### **Puerto 5173**
- **Móvil:** Vista simplificada (solo completar)
- **Tablet:** Vista ejecutiva adaptada
- **Desktop:** Dashboard completo (ideal)

---

## 🔐 Autenticación (Futuro)

### **Puerto 3000**
- Auth0 o Supabase
- Social login (Google, Apple)
- Experiencia sin fricción

### **Puerto 5173**
- Sesión compartida
- Token JWT del 3000
- Acceso directo tras onboarding

---

## 🚀 Deploy

### **Desarrollo**
```bash
# Backend (8000)
cd backend && python run.py

# Frontend Inmersivo (3000)
cd campo-sagrado-nextjs && npm run dev

# Frontend Ejecutivo (5173)
cd frontend && npm run dev
```

### **Producción (Futuro)**
```
Backend:       Render/Railway      (backend.camposagrado.com)
Puerto 3000:   Vercel              (app.camposagrado.com)
Puerto 5173:   Netlify             (dashboard.camposagrado.com)
```

---

## 🎓 Onboarding del Usuario

### **Primera Vez (Puerto 3000)**

```
1. Landing → "Entrar al Campo Sagrado"
2. Wizard de configuración:
   - Bienvenida
   - No-negociables
   - Contexto financiero
   - Contexto biológico
   - Expresión libre
3. Primer Estado Cero inmersivo
4. Generación de primer plan
5. Validación
6. → "Ahora gestiona tu día en el Dashboard"
7. Redirige a localhost:5173
```

### **Uso Diario**

```
Fajr:    localhost:3000 (Estado Cero)
         ↓
Durante: localhost:5173 (Ejecutar)
         ↓
Maghrib: localhost:5173/maghrib (Validar)
         ↓
         Sistema descansa 🌙
```

---

## 📊 Métricas de Éxito

### **Puerto 3000**
- Tasa de completitud de Estado Cero
- Tiempo promedio en meditación
- Tasa de validación de actividades
- Retención día 2, día 7, día 30

### **Puerto 5173**
- Actividades completadas / propuestas
- Balance de dimensiones trabajadas
- Uso del 40% emergente
- Tasa de validación Maghrib

---

## 🔮 Visión Futura

### **Puerto 3000 evoluciona a:**
- App móvil nativa (iOS/Android)
- Experiencia VR (Meta Quest)
- Audio generativo integrado
- Modo comunidad (compartir insights)

### **Puerto 5173 evoluciona a:**
- Desktop app (Electron)
- CLI para power users
- Modo empresa (equipos)
- Integraciones avanzadas (Notion, Linear, etc.)

---

## ✅ Checklist de Implementación

### **Semana 1: Fundación**
- [ ] Setup proyecto Next.js (3000)
- [ ] Estado Cero inmersivo con R3F
- [ ] Wizard de configuración
- [ ] Generación de actividades
- [ ] Validación de plan
- [ ] Mejorar Espejo Diario (5173)
- [ ] Validación Maghrib

### **Semana 2: Refinamiento**
- [ ] Onboarding completo
- [ ] Animaciones pulidas
- [ ] Sincronización calendario
- [ ] Testing end-to-end
- [ ] Documentación de usuario

### **Semana 3: Lanzamiento MVP**
- [ ] Beta testing con 5 usuarios
- [ ] Ajustes basados en feedback
- [ ] Deploy a producción
- [ ] Landing page pública
- [ ] Primeros usuarios reales

---

**Arquitectura definitiva. Clara, pragmática, soberana.**

**Adelante con la implementación. إن شاء الله 🕌✨**

