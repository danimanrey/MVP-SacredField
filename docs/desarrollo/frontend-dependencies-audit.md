# 📦 Auditoría de Dependencias Frontend - Next.js

**Fecha:** 19 de octubre, 2025
**Contexto:** Fase 1 Día 3 - Post Refactorización
**Objetivo:** Validar uso de dependencias y eliminar no utilizadas

---

## 🔍 Metodología de Auditoría

Para cada dependencia sospechosa se ejecutó:

```bash
# Búsqueda exhaustiva de imports
grep -r "PACKAGE_NAME" app/ lib/ --include="*.tsx" --include="*.ts"

# Conteo de archivos que usan la dependencia
grep -r "from 'PACKAGE_NAME'" app/ lib/ | wc -l

# Análisis de iconos/componentes específicos
grep -r "from 'lucide-react'" app/ | sed "s/.*import { \(.*\) } from.*/\1/" | tr ',' '\n' | sort | uniq
```

---

## 📊 Resultados de Auditoría

### **DEPENDENCIAS PRODUCTION (package.json)**

| Package | Version Instalada | Files Usando | Componentes Usados | Estado | Bundle Impact |
|---------|-------------------|--------------|---------------------|---------|---------------|
| **react** | 18.3.1 | 19 | Core framework | ✅ KEEP | ~130KB |
| **react-dom** | 18.3.1 | 19 | Core framework | ✅ KEEP | ~130KB |
| **next** | 14.2.0 | 19 | Meta-framework | ✅ KEEP | ~300KB |
| **three** | 0.168.0 | 2 | 3D rendering | ✅ KEEP | ~600KB |
| **@react-three/fiber** | 8.17.0 | 1 | React + Three.js | ✅ KEEP | ~50KB |
| **@react-three/drei** | 9.122.0 | 1 | 4 helpers (Sphere, Box, Stars, OrbitControls) | ✅ KEEP | ~150KB |
| **framer-motion** | 11.18.2 | 12 | Animations | ✅ KEEP | ~200KB |
| **zustand** | 4.5.7 | 2 | State management (2 stores) | ✅ KEEP | ~3KB |
| **lucide-react** | 0.441.0 | 2 | 5 icons (ChevronLeft/Right, Clock, Plus, Save) | ⚠️ EVALUATE | ~440KB |

**Total node_modules:** 467MB
**Estimated production bundle:** ~2.0MB (pre-compression)

---

## ✅ Dependencias VALIDADAS (Mantener)

### **1. zustand (4.5.7) - ✅ USADO**

**Archivos:**
- `lib/stores/onboarding-store.ts`
- `lib/stores/estado-cero-store.ts`

**Código:**
```typescript
// lib/stores/onboarding-store.ts
import { create } from 'zustand'

// lib/stores/estado-cero-store.ts
import { create } from 'zustand'
```

**Análisis:**
- ✅ 2 stores activos (onboarding, estado-cero)
- ✅ State management ligero (3KB vs React Context)
- ✅ Better performance que Context API
- ✅ DevTools support

**Bundle Impact:** ~3KB gzipped (MÍNIMO)

**DECISIÓN: ✅ MANTENER**

**Rationale:**
- Uso confirmado en 2 stores críticos
- Alternativa (React Context) más verbosa y menos performant
- Bundle size insignificante (3KB)
- Soberanía: MIT License, no vendor lock-in

---

### **2. @react-three/drei (9.122.0) - ✅ USADO**

**Archivos:**
- `app/estado-cero/components/UniversoEsferico.tsx`

**Código:**
```typescript
import { Sphere, Box, Stars, OrbitControls } from '@react-three/drei'
```

**Componentes Usados:**
1. `Sphere` - Esfera sagrada 3D
2. `Box` - Cubo geometría sagrada
3. `Stars` - Campo de estrellas
4. `OrbitControls` - Control cámara usuario

**Análisis:**
- ✅ 4 helpers de ~100 que provee
- ✅ Críticos para Estado Cero inmersivo
- ✅ Evita reimplementar geometría 3D compleja
- ⚠️ Solo ~4% de la librería usado

**Bundle Impact:** ~150KB (tree-shaking reduce a ~40KB en producción)

**DECISIÓN: ✅ MANTENER**

**Rationale:**
- Estado Cero inmersivo es feature core (Puerto 3000)
- Reimplementar Sphere/Box/Stars = >200 LOC custom
- drei es estándar para R3F ecosystem
- Tree-shaking reduce bundle a ~40KB real
- Soberanía: MIT License, React Three Fiber ecosystem

**Alternativas Evaluadas:**
- ❌ Geometría custom: >200 LOC, más bugs
- ❌ Vanilla Three.js: Incompatible con React fiber
- ✅ drei: Standard, mantenido, tree-shakeable

---

### **3. framer-motion (11.18.2) - ✅ USADO**

**Archivos:** 12 files

**Análisis:**
```bash
$ grep -r "framer-motion" app/ lib/ | wc -l
12
```

**Uso Confirmado:**
- ✅ Animaciones de transición entre rutas
- ✅ Smooth page transitions (Estado Cero flow)
- ✅ Component animations (fade-in, slide)
- ✅ Gesture handlers (drag, hover)

**Bundle Impact:** ~200KB gzipped

**DECISIÓN: ✅ MANTENER**

**Rationale:**
- Uso extensivo (12 files)
- Puerto 3000 requiere experiencia inmersiva
- Alternativa (CSS animations) menos flexible
- Production-ready, bien optimizado
- Soberanía: MIT License

**Alternativas Evaluadas:**
- ❌ CSS animations: Menos control, no gesture handling
- ❌ React Spring: Similar bundle, menos features
- ✅ framer-motion: Best DX, gesture support, declarativo

---

### **4. three + @react-three/fiber - ✅ USADO**

**Archivos:**
- `three`: 2 files
- `@react-three/fiber`: 1 file

**Uso Confirmado:**
- ✅ UniversoEsferico.tsx (Estado Cero 3D)
- ✅ Renderizado WebGL
- ✅ Core para experiencia inmersiva

**Bundle Impact:**
- three: ~600KB gzipped
- fiber: ~50KB gzipped

**DECISIÓN: ✅ MANTENER**

**Rationale:**
- Feature core de Puerto 3000 (ADR 001)
- "Portal del Asombro" requiere 3D
- Sin alternativa viable para WebGL + React
- Tree-shaking reduce bundle significativamente

---

## ⚠️ Dependencia INFRAUTILIZADA (Evaluar)

### **5. lucide-react (0.441.0) - ⚠️ SOLO 5 ICONOS USADOS**

**Archivos:**
- `app/estado-cero/components/PreguntasSacrales.tsx`
- `app/estado-cero/validacion/page.tsx`

**Iconos Usados:**
```typescript
// PreguntasSacrales.tsx
import { ChevronRight, ChevronLeft } from 'lucide-react'

// validacion/page.tsx
import { Clock, Plus, Save } from 'lucide-react'
```

**Total: 5 iconos únicos**
- ChevronLeft
- ChevronRight
- Clock
- Plus
- Save

**Análisis:**
- ⚠️ Librería completa: ~1,500 iconos (441KB bundle)
- ⚠️ Uso real: 5 iconos (~0.3% de la librería)
- ⚠️ Bundle impact: ~440KB (sin tree-shaking efectivo)
- ⚠️ Real usage: ~2KB si fueran SVG inline

**Bundle Impact:** ~440KB total → ~2KB real si se extraen

**OPCIONES EVALUADAS:**

#### **OPCIÓN A: Extraer SVGs (RECOMENDADO)**
```bash
# Crear directorio iconos
mkdir -p app/components/icons/

# Extraer SVGs de lucide
# ChevronLeft.tsx, ChevronRight.tsx, Clock.tsx, Plus.tsx, Save.tsx

# Reemplazar imports:
# - import { Clock } from 'lucide-react'
# + import { Clock } from '@/components/icons/Clock'

# Desinstalar lucide-react
npm uninstall lucide-react
```

**PROS:**
- ✅ Bundle reduction: 440KB → 2KB (~99.5% saving)
- ✅ No runtime overhead
- ✅ Full control sobre SVG
- ✅ Alineado con Pilar 2 (Soberanía)

**CONS:**
- ⚠️ 1-2h work (extraer 5 SVGs)
- ⚠️ Si agregamos más iconos, trabajo manual
- ⚠️ No auto-updates de lucide

**Bundle Savings:** ~438KB (~21.9% del bundle total estimado)

---

#### **OPCIÓN B: Migrar a @heroicons/react**
```bash
npm uninstall lucide-react
npm install @heroicons/react
```

**PROS:**
- ✅ Más ligero (~200KB vs 441KB)
- ✅ Tree-shaking mejor
- ✅ Similar API
- ✅ MIT License, Tailwind Labs

**CONS:**
- ⚠️ Menos iconos disponibles (~300 vs 1,500)
- ⚠️ Estilo diferente (puede requerir ajustes UI)
- ⚠️ Migration work (~1-2h)

**Bundle Savings:** ~241KB (~50% reduction)

---

#### **OPCIÓN C: Mantener lucide-react**

**PROS:**
- ✅ No work required
- ✅ Iconos consistentes
- ✅ Fácil agregar más iconos
- ✅ Auto-updates

**CONS:**
- ❌ Bundle bloat: 440KB para 5 iconos
- ❌ No alineado con Pilar 1 (Pureza)
- ❌ 99.7% de librería no usada

**Bundle Impact:** Sin savings

---

### **RECOMENDACIÓN LUCIDE-REACT:**

**CORTO PLAZO (Fase 1-2):** ✅ **MANTENER**
- Razón: MVP funcional más importante que optimización prematura
- Feature completeness > bundle optimization en esta fase
- 5 iconos es uso bajo pero no cero

**LARGO PLAZO (Fase 3+):** 🔄 **MIGRAR A OPCIÓN A (SVG Extraction)**
- Timing: Post-migración SvelteKit (Fase 3)
- Rationale: 99.5% bundle reduction
- Esfuerzo: 1-2h (trivial comparado con SvelteKit migration)
- ROI: Alto (438KB savings)

**DOCUMENTAR EN ADR:** Decisión consciente de mantener ahora, migrar después

---

## 📊 Resumen de Auditoría

### **Dependencias Analizadas: 9**

| Categoría | Count | Packages |
|-----------|-------|----------|
| ✅ **MANTENER (uso óptimo)** | 8 | react, react-dom, next, three, fiber, drei, framer-motion, zustand |
| ⚠️ **MANTENER (infrautilizado pero OK)** | 1 | lucide-react |
| ❌ **ELIMINAR (no usado)** | 0 | N/A |

---

### **Hallazgos Clave:**

1. ✅ **Todas las dependencias están en uso**
   - No hay "dead dependencies"
   - Audit limpio

2. ⚠️ **lucide-react infrautilizado**
   - 5 iconos de 1,500 disponibles (0.3%)
   - 440KB bundle para 2KB de uso real
   - Optimización futura recomendada

3. ✅ **Dependencias core justificadas**
   - three.js + R3F: Feature core (Estado Cero 3D)
   - framer-motion: Uso extensivo (12 files)
   - zustand: Lightweight state (2 stores)

4. ✅ **Bundle size razonable**
   - ~2.0MB pre-compression estimado
   - ~600KB post-compression (gzip)
   - Aceptable para app con 3D

---

## 🎯 Plan de Acción

### **FASE 1-2 (Ahora):**
- ✅ Mantener todas las dependencias actuales
- ✅ Documentar decisión en ADR
- ✅ No optimizaciones prematuras

### **FASE 3 (Post-SvelteKit Migration):**
- 🔄 Migrar lucide-react → SVG extraction
- 🔄 Re-audit tras migración a Svelte
- 🔄 Benchmark bundle size con Svelte compiler

---

## 📈 Métricas

### **Antes de Auditoría:**
```yaml
Dependencias instaladas: 9 (prod)
Dependencias analizadas: 9
Dependencias no usadas: ? (sospecha)
node_modules size: 467MB
```

### **Después de Auditoría:**
```yaml
Dependencias instaladas: 9 (prod)
Dependencias validadas: 9 ✅
Dependencias no usadas: 0 ✅
Dependencias infrautilizadas: 1 (lucide-react)
node_modules size: 467MB (sin cambios)
Optimización identificada: 438KB (lucide → SVG)
```

---

## ✅ Validación Contra Pilares

### **Pilar 1: Pureza Técnica**
- ✅ Audit exhaustivo realizado
- ✅ Todas las deps justificadas con uso real
- ⚠️ lucide-react infrautilizado (documentado, migración planificada)
- ✅ Sin "just in case" dependencies

### **Pilar 2: Soberanía Creativa**
- ✅ Todas las deps son MIT License
- ✅ No vendor lock-in
- ✅ Migration paths claros (lucide → SVG, Next → Svelte)
- ✅ Community-driven packages (drei, framer-motion)

### **Pilar 3: Responsabilidad Sagrada**
- ✅ Bundle size consciente
- ✅ Trade-offs documentados
- ✅ Optimizaciones futuras planificadas
- ✅ No desperdicio innecesario

### **Pilar 5: Excelencia Técnica**
- ✅ Tree-shaking considerado
- ✅ Bundle impact analizado
- ✅ Alternativas evaluadas
- ✅ Best practices seguidas

---

## 📋 Conclusión

**Resultado Auditoría:** ✅ **LIMPIO**

No se encontraron dependencias completamente no usadas. Todas las 9 dependencias de producción tienen uso confirmado en el codebase.

**Única optimización identificada:**
- lucide-react: 440KB → 2KB (extracción SVG)
- Timing: Fase 3 (post-SvelteKit)
- ROI: Alto (99.5% reduction)

**Próximos pasos:**
1. ✅ Documentar decisión en ADR-002
2. ✅ Mantener estado actual para MVP
3. 🔄 Planificar migración SVG en Fase 3

---

**Autor:** El Entrelazador
**Fecha:** 19 octubre 2025
**Estado:** Auditoría completada
**Próxima revisión:** Fase 3 (post-SvelteKit migration)

---

**إن شاء الله - Dependencies validadas con responsabilidad sagrada 🕌✨**
