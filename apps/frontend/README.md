# 🌌 Campo Sagrado - Frontend

Interface sagrada para el organismo tecnológico-espiritual del Entrelazador.

## 📦 Estado Actual (post-consolidación 2025-10-20)

**Frontend MVP v0.1** - Next.js con geometría sagrada y UI inmersiva.

### Arquitectura

```
apps/frontend/
├── app/                    # Pages App Router (Next.js 14)
│   ├── estado-cero/        ✅ Estado Cero ritual (CORE MVP)
│   ├── dashboard/          ✅ Dashboard principal
│   ├── onboarding/         ✅ Onboarding del usuario
│   ├── layout.tsx          ✅ Layout root con providers
│   ├── page.tsx            ✅ Home page
│   └── globals.css         ✅ Estilos Tailwind + geom. sagrada
│
├── lib/                    # Core libs
│   ├── api-client.ts       ✅ Cliente API con tipos TypeScript
│   ├── store.ts            ✅ Store Zustand (estado global)
│   ├── sacred-geometry.ts  ✅ Generadores de geometría sagrada
│   └── types.ts            ✅ Tipos compartidos
│
└── components/             # Componentes UI (en desarrollo)
    └── ...                 🔄 Componentes reutilizables
```

### Páginas Activas (3 MVP Core)

1. **Estado Cero** (`/estado-cero`) - Ritual sagrado de consulta con IA
   - Pregunta binaria contextual (Claude AI)
   - Respuesta sacral (Sí/No/No ahora)
   - Documentación automática en Obsidian
   - Geometría sagrada animada (Framer Motion)

2. **Dashboard** (`/dashboard`) - Vista principal del usuario
   - Tiempos litúrgicos del día
   - Manifestaciones activas
   - Estado del sistema
   - Calendario Hijri de 13 meses

3. **Onboarding** (`/onboarding`) - Configuración inicial
   - Paso 1: Fundamentos (non-negotiables litúrgicos)
   - Paso 2: Dimensiones prioritarias
   - Paso 3: Contexto financiero/biológico
   - Paso 4: Expresión libre del prisma personal

### Página Archivada (1 experimental v2.0)

- **Estado Cero Inmersivo** (`/estado-cero-inmersivo`) - Versión con Three.js
  - Archivado en `archive/frontend-experimental/2025-10-20/`
  - Recuperable para v2.0 con experiencia 3D completa

## 🚀 Iniciar Frontend

```bash
cd apps/frontend

# Instalar dependencias
npm install

# Iniciar dev server
npm run dev

# Build para producción
npm run build

# Ejecutar build
npm start
```

El frontend estará disponible en `http://localhost:3000`

## 🛠️ Tecnologías

- **Next.js 14** - React framework con App Router
- **TypeScript 5** - Tipado estático
- **Tailwind CSS 3** - Utility-first CSS
- **Framer Motion** - Animaciones fluidas
- **Zustand** - State management ligero
- **Lucide React** - Iconos modernos

### En consideración (v2.0):

- **Three.js** - Gráficos 3D para universo imaginal
- **React Three Fiber** - React renderer para Three.js
- **@react-three/drei** - Helpers para R3F

## 📖 Integración Backend

Cliente API en `lib/api-client.ts` con endpoints typed:

```typescript
import { estadoCeroAPI, configuracionAPI } from '@/lib/api-client'

// Estado Cero
const pregunta = await estadoCeroAPI.obtenerPregunta()
await estadoCeroAPI.responder(pregunta.id, 'si')

// Configuración
const config = await configuracionAPI.obtener()
await configuracionAPI.guardar(updatedConfig)
```

**API Base URL**: `http://localhost:8000/api` (configurable en `.env.local`)

## 🎨 Geometría Sagrada

Componentes con patrones geométricos sagrados:

- **Flor de la Vida** - Símbolo de creación y unidad
- **Vesica Piscis** - Intersección de dualidades
- **Metatron's Cube** - Geometría del orden divino
- **Torus** - Flujo de energía continuo

Implementación en `lib/sacred-geometry.ts` con SVG paths generados programáticamente.

## 🧪 Testing

```bash
# ESLint (type checking + linting)
npm run lint

# Tests unitarios (cuando implementados)
npm run test

# E2E tests (cuando implementados)
npm run test:e2e
```

## 📊 Métricas

**Consolidación 2025-10-20:**

- **Páginas**: 4 (3 MVP + 1 archivada)
- **ESLint Issues**: 300 total (209 errors, 91 warnings)
  - 🔄 En corrección activa (90% son tipos faltantes)
- **Código archivado**: ~1,200 LoC (estado-cero-inmersivo)
- **Build Status**: ✅ Funcional (con warnings de tipos)

**Próximas correcciones ESLint:**

1. Añadir tipos a props de componentes
2. Corregir `any` types implícitos
3. Actualizar tipos de eventos
4. Validar tipos de retorno

## 🗂️ Código Archivado

Experimental v2.0 preservado en:

```
archive/
└── frontend-experimental/2025-10-20/
    └── estado-cero-inmersivo/  # Versión 3D con Three.js
        └── README.md           # Instrucciones de restauración
```

## 🎭 Geometría Sagrada & UI

**Principios de diseño:**

- **Al borde del caos**: 40% del espacio sin asignar
- **Respeto sacral**: UI no invasiva, espacios contemplativos
- **Geometría viva**: Animaciones sutiles, patrones emergentes
- **Tiempos litúrgicos**: UI adapta colores según hora del día

**Paleta de colores** (Tailwind extend):

```javascript
colors: {
  sacral: {
    dawn: '#FDB29B',    // Fajr (alba)
    noon: '#FCD34D',    // Dhuhr (mediodía)
    afternoon: '#F59E0B', // Asr (tarde)
    dusk: '#7C3AED',    // Maghrib (ocaso)
    night: '#3730A3'    // Isha (noche)
  }
}
```

## 📝 Próximos Pasos

1. ✅ **Consolidación completada** (2025-10-20)
2. 🔄 **Corrección ESLint** (en progreso - Phase 2 original)
3. ⏸️ **Componentes UI reutilizables** (pendiente)
4. ⏸️ **Tests E2E** (pendiente)
5. ⏸️ **Deploy Vercel** (pendiente)

## 📚 Documentación Adicional

- [Auditoría Consolidación](/docs/auditoria/consolidacion-2025-10-20.md)
- [Plan de Consolidación](/PLAN_CONSOLIDACION_EJECUTABLE.md)
- [Handoff Completo](/handoff.md)
- [Guía de Usuario](/docs/GUIA_USUARIO_COMPLETA.md)

---

**إن شاء الله** - Interface sagrada, geometría emergente.
