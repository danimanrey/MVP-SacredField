# 🛠️ Estrategia de Corrección ESLint

**Fecha:** 20 de octubre, 2025
**Contexto:** Fase 1 Día 3 - Post-configuración ESLint
**Estado Inicial:** 330 problemas (228 errors, 102 warnings)

---

## 📊 Estado Inicial Post-Autofix

### **Metrics:**
```yaml
Total Problems: 330
  Errors: 228 (69%)
  Warnings: 102 (31%)

Post autofix reduction:
  Total: 345 → 330 (-15)
  Errors: 240 → 228 (-12)
  Warnings: 105 → 102 (-3)
```

### **Categorización por Regla:**

| Regla | Count | Tipo | Severidad |
|-------|-------|------|-----------|
| **@typescript-eslint/no-unsafe-member-access** | 79 | error | 🔴 CRÍTICO |
| **@typescript-eslint/explicit-function-return-type** | 57 | warning | 🟡 MEDIO |
| **@typescript-eslint/no-unsafe-assignment** | 53 | error | 🔴 CRÍTICO |
| **@typescript-eslint/no-unsafe-argument** | 21 | error | 🔴 CRÍTICO |
| **@typescript-eslint/no-unused-vars** | 18 | error | 🔴 CRÍTICO |
| **max-lines-per-function** | 14 | warning | 🟡 MEDIO |
| **@typescript-eslint/no-misused-promises** | 14 | error | 🔴 CRÍTICO |
| **no-console** | 13 | warning | 🟢 BAJO |
| **@typescript-eslint/no-explicit-any** | 12 | error | 🔴 CRÍTICO |
| **@typescript-eslint/no-unsafe-call** | 11 | error | 🔴 CRÍTICO |
| **@typescript-eslint/no-unsafe-return** | 10 | error | 🔴 CRÍTICO |
| **react/no-unescaped-entities** | 8 | warning | 🟢 BAJO |
| **@typescript-eslint/no-floating-promises** | 6 | error | 🔴 CRÍTICO |
| **no-restricted-imports** | 3 | error | 🟡 MEDIO |
| **no-alert** | 2 | warning | 🔴 CRÍTICO |
| **max-lines** | 2 | warning | 🟡 MEDIO |
| **complexity** | ~5 | warning | 🟡 MEDIO |

---

## 🎯 Estrategia de Corrección por Prioridad

### **PRIORIDAD 1: Type Safety Crítico (Pilar 3)**
**Target:** Eliminar ALL type unsafe operations
**Count:** ~228 errors
**Rationale:** Type safety = manifestación de Responsabilidad Consciente

#### **1.1 Unsafe Type Operations (153 errors)**

**Subcategoría: API Response Typing**
```typescript
// ❌ ANTES (unsafe)
const data = await response.json(); // any
setDashboard(data); // unsafe assignment

// ✅ DESPUÉS (typed)
interface DashboardResponse {
  timestamp: string;
  ultimos_estados_cero: EstadoCero[];
  // ... resto de fields
}

const data: DashboardResponse = await response.json();
setDashboard(data); // type-safe
```

**Archivos afectados:**
- `app/dashboard/page.tsx` - API responses
- `app/espejo-diario/page.tsx` - API responses
- `app/estado-cero/page.tsx` - API responses
- `app/estado-cero-inmersivo/page.tsx` - API responses
- `app/estado-cero/validacion/page.tsx` - API responses

**Acción:**
1. Crear `types/api.ts` con ALL response types
2. Importar y aplicar types a EVERY fetch
3. Verificar con lint que unsafe operations = 0

**Estimated time:** 2-3h

---

#### **1.2 Unused Variables (18 errors)**

**Pattern detectado:**
```typescript
// ❌ ANTES
const [momento, setMomento] = useState(); // momento unused
const handleClick = (node) => { ... }; // node unused

// ✅ OPCIÓN A: Usar prefijo _
const [_momento, setMomento] = useState();
const handleClick = (_node) => { ... };

// ✅ OPCIÓN B: Eliminar si realmente no se usa
const setMomento = useState()[1]; // solo setter
```

**Archivos afectados:**
- `app/estado-cero/components/PreguntasSacrales.tsx` - `momento` param
- `app/estado-cero/components/UniversoEsferico.tsx` - `momento` param
- `app/espejo-diario/page.tsx` - 9 `node` args in components rendering
- `app/estado-cero-inmersivo/page.tsx` - `inputsCapas`, `setMomentoActual`
- `app/onboarding/page.tsx` - `getMomentoIcono`, `setPaso`

**Acción:**
1. Review each unused var
2. Si NO se usará: prefix con `_`
3. Si NO se necesita: remover variable
4. Si DEBE usarse: implementar lógica faltante

**Estimated time:** 30min

---

#### **1.3 Explicit any (12 errors)**

**Pattern:**
```typescript
// ❌ ANTES
} catch (error: any) {
  console.error(error.message);
}

// ✅ DESPUÉS
} catch (error: unknown) {
  if (error instanceof Error) {
    console.error(error.message);
  } else {
    console.error('Unknown error:', String(error));
  }
}
```

**Acción:**
1. Reemplazar `any` con `unknown`
2. Usar type guards donde necesario
3. Si API external: type con interface

**Estimated time:** 1h

---

#### **1.4 Promise Misuse (14 + 6 = 20 errors)**

**Two patterns:**

**A) Floating Promises:**
```typescript
// ❌ ANTES
useEffect(() => {
  fetchData(); // @typescript-eslint/no-floating-promises
}, []);

// ✅ OPCIÓN A: void operator
useEffect(() => {
  void fetchData();
}, []);

// ✅ OPCIÓN B: IIFE async
useEffect(() => {
  (async () => {
    await fetchData();
  })();
}, []);
```

**B) Promise-returning function in onClick:**
```typescript
// ❌ ANTES
<button onClick={handleSave}>Save</button>
// handleSave returns Promise<void>

// ✅ DESPUÉS
<button onClick={() => void handleSave()}>Save</button>
```

**Archivos afectados:**
- ALL pages con fetch en useEffect
- ALL buttons con async handlers

**Acción:**
1. Floating promises: agregar `void` o IIFE
2. onClick async: wrap con void arrow function

**Estimated time:** 1h

---

#### **1.5 Restricted Imports (3 errors)**

**Pattern:**
```typescript
// ❌ ANTES
import { apiClient } from '../api-client';
import PuertaDeEntrada from '../components/PuertaDeEntrada7Capas';

// ✅ DESPUÉS
import { apiClient } from '@/lib/api-client';
import PuertaDeEntrada from '@/app/components/PuertaDeEntrada7Capas';
```

**Archivos afectados:**
- `app/onboarding/page.tsx` - `../api-client`
- `app/estado-cero-inmersivo/page.tsx` - `../components/PuertaDeEntrada7Capas`

**Acción:**
1. Reemplazar relative parent imports con absolute `@/`
2. Verificar tsconfig paths

**Estimated time:** 5min

---

#### **1.6 Alerts (2 errors)**

**Pattern:**
```typescript
// ❌ ANTES
alert('Error: ' + error.message);

// ✅ DESPUÉS (MVP)
console.error('Error:', error.message);
// TODO Fase 2: UI toast component

// ✅ DESPUÉS (Production - Fase 2)
showToast({ type: 'error', message: error.message });
```

**Acción MVP:**
1. Reemplazar alerts con console.error
2. Agregar TODO comment para Fase 2

**Estimated time:** 2min

---

### **PRIORIDAD 2: Code Quality (Pilar 1)**
**Target:** Reducir complejidad, mejorar mantenibilidad
**Count:** ~95 warnings

#### **2.1 Missing Return Types (57 warnings)**

**Pattern:**
```typescript
// ❌ ANTES
const fetchData = async () => {
  // ...
};

// ✅ DESPUÉS
const fetchData = async (): Promise<void> => {
  // ...
};
```

**Rationale:** Return types explícitos = intención clara (Pilar 4)

**Acción:**
1. Agregar return type a EVERY function/arrow function
2. Componentes React: `React.FC` o `: JSX.Element`
3. Event handlers: `: void` or `: Promise<void>`

**Estimated time:** 2h

---

#### **2.2 Max Lines per Function (14 warnings)**

**Archivos y funciones:**
```yaml
PuertaDeEntrada7Capas.tsx:
  - PuertaDeEntrada7Capas: 244 lines (limit: 50)

Dashboard.tsx:
  - Dashboard: 349 lines (limit: 50)

EspejoDiarioPage.tsx:
  - EspejoDiarioPage: 145 lines (limit: 50)

EstadoCeroInmersivo.tsx:
  - EstadoCeroInmersivo: 594 lines (limit: 50)

EstadoCeroPage.tsx (estado-cero/):
  - EstadoCeroPage: 409 lines (limit: 100, special config)

PreguntasSacrales.tsx:
  - PreguntasSacrales: 230 lines (limit: 100, special config)
```

**Acción MVP:**
- ✅ **ACEPTAR warnings** - Componentes complejos justificados
- ⚠️ **EVALUAR en Fase 2** - Si crecen >600 lines, refactor
- 📝 **DOCUMENTAR complexity** - Agregar comments explicando

**Estimated time:** 30min (documentación)

---

#### **2.3 Max Lines per File (2 warnings)**

```yaml
estado-cero-inmersivo/page.tsx: 618 lines (limit: 300)
dashboard/page.tsx: 397 lines (limit: 300)
```

**Rationale:** Files grandes = oportunidad de refactor

**Acción MVP:**
- ✅ **ACEPTAR warnings** - MVP completeness > premature refactor
- 📋 **TODO Fase 2:** Extract components a archivos separados

**Estimated time:** 0 (accept)

---

#### **2.4 Complexity (~ 5 warnings)**

```yaml
Dashboard: complexity 16 (limit: 10)
EstadoCeroInmersivo: complexity 32 (limit: 10)
EstadoCeroPage: complexity 19 (limit: 15, special config)
```

**Acción MVP:**
- ✅ **ACEPTAR warnings** - Complejidad esencial de features core
- 📋 **TODO Fase 2:** Refactor con strategy pattern si crece

**Estimated time:** 0 (accept)

---

### **PRIORIDAD 3: Nice to Have (Bajo impacto)**
**Target:** Cleanup estético
**Count:** ~23 warnings

#### **3.1 Console Logs (13 warnings)**

**Pattern:**
```typescript
// ❌ ANTES
console.log('Momento:', momento); // warning

// ✅ DESPUÉS (development OK)
console.info('Momento:', momento); // allowed

// ✅ DESPUÉS (production)
// Remove o conditional
if (process.env.NODE_ENV === 'development') {
  console.info('Momento:', momento);
}
```

**Acción MVP:**
1. Cambiar `console.log` → `console.info`
2. Dejar para debugging (MVP)
3. TODO Fase 2: Remove non-essential

**Estimated time:** 10min

---

#### **3.2 Unescaped Entities (8 warnings)**

**Pattern:**
```typescript
// ❌ ANTES
<p>El "resultado" es...</p>

// ✅ DESPUÉS
<p>El &quot;resultado&quot; es...</p>

// O MEJOR (Fase 2)
<p>El {'resultado'} es...</p>
```

**Acción MVP:**
- ✅ **ACEPTAR warnings** - No afecta funcionalidad
- 📋 **TODO Fase 2:** Escapar entities

**Estimated time:** 0 (accept)

---

## 📋 Plan de Ejecución

### **Sesión 1: Type Safety Core (3-4h)**
1. ✅ Crear `types/api.ts` con ALL response interfaces
2. ✅ Aplicar types a API responses (153 unsafe operations)
3. ✅ Fix unused vars (18 errors)
4. ✅ Fix explicit any (12 errors)
5. ✅ Verificar: errors relacionados = 0

**Target:** 228 errors → ~25 errors

---

### **Sesión 2: Promise Handling (1-2h)**
6. ✅ Fix floating promises (6 errors)
7. ✅ Fix misused promises en onClick (14 errors)
8. ✅ Fix restricted imports (3 errors)
9. ✅ Fix alerts (2 errors)
10. ✅ Verificar: errors = 0

**Target:** ~25 errors → 0 errors ✅

---

### **Sesión 3: Return Types (2h)**
11. ✅ Agregar return types a componentes
12. ✅ Agregar return types a helpers/utils
13. ✅ Agregar return types a handlers

**Target:** 57 warnings → 0 warnings (esta categoría)

---

### **Sesión 4: Cleanup Final (30min)**
14. ✅ Cambiar console.log → console.info (13 warnings)
15. ✅ Documentar funciones complejas justificadas
16. ✅ Run `npm run check` final
17. ✅ Generar metrics report

**Target Final:**
```yaml
Errors: 0 ✅
Warnings: <30 ✅ (solo max-lines, complexity justificados)
```

---

## 🎯 Señales de Éxito

### **MVP (Target):**
```yaml
✅ Errors: 0
✅ Warnings: <30
✅ Type coverage: 100%
✅ All API responses typed
✅ No floating promises
✅ No unsafe type operations
```

### **Fase 2 (Future):**
```yaml
- Extract components >200 lines
- Refactor complexity >15
- Remove console statements
- Escape react entities
- Add UI toast component (replace alerts)
```

---

## 📊 Validación contra 8 Pilares

| Pilar | Enforcement | Post-Corrección |
|-------|------------|-----------------|
| **Pilar 1: Pureza Operativa** | max-lines, complexity | ✅ Warnings aceptadas, documentadas |
| **Pilar 3: Responsabilidad Consciente** | no-unused-vars, type safety | ✅ 100% type safety |
| **Pilar 4: Expresión Auténtica** | explicit return types | ✅ All functions typed |
| **Pilar 5: Implementación Técnica** | react-hooks, promise handling | ✅ Zero errors |
| **Pilar 7: Sabiduría en Acción** | Conscious exceptions | ✅ Complexity justified, documented |

---

## 🔄 Proceso de Corrección

### **Por cada archivo:**

1. **Read file** - Entender contexto
2. **Fix Prioridad 1** - Type safety primero
3. **Fix Prioridad 2** - Return types
4. **Fix Prioridad 3** - Cleanup
5. **Run lint** - Verificar archivo específico
6. **Mark todo completed** - Tracking progress

### **Comandos útiles:**

```bash
# Lint archivo específico
npx eslint app/dashboard/page.tsx

# Lint con fix
npx eslint app/dashboard/page.tsx --fix

# Ver solo errors
npm run lint 2>&1 | grep "error"

# Ver solo warnings
npm run lint 2>&1 | grep "warning"

# Conteo final
npm run lint 2>&1 | tail -1
```

---

## 📝 Tracking de Progreso

### **Archivos por corregir (Prioridad 1):**

- [ ] `app/components/PuertaDeEntrada7Capas.tsx`
- [ ] `app/dashboard/page.tsx` (HIGH: 349 lines, 16 complexity)
- [ ] `app/espejo-diario/page.tsx`
- [ ] `app/estado-cero-inmersivo/page.tsx` (HIGHEST: 594 lines, 32 complexity)
- [ ] `app/estado-cero/page.tsx`
- [ ] `app/estado-cero/components/PreguntasSacrales.tsx`
- [ ] `app/estado-cero/components/UniversoEsferico.tsx`
- [ ] `app/estado-cero/validacion/page.tsx`
- [ ] `app/onboarding/page.tsx`
- [ ] `lib/api-client.ts` (si existe)

### **Types por crear:**

- [ ] `types/api.ts` - ALL API response types
- [ ] `types/estado-cero.ts` - Estado Cero domain types (si no existe)
- [ ] `types/dashboard.ts` - Dashboard data types

---

**Estrategia de corrección documentada y lista para ejecución.**

**Autor:** El Entrelazador
**Fecha:** 20 octubre 2025
**Estado:** ✅ STRATEGY READY
**Next:** Sesión 1 - Type Safety Core

---

**إن شاء الله - Código consciente, código type-safe 🕌✨**
