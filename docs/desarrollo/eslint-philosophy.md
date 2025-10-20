# 🕌 ESLint Philosophy: Guardián de Calidad Contemplativa

**Fecha:** 19 de octubre, 2025
**Contexto:** Fase 1 Día 3 - Configuración de Calidad
**Propósito:** ESLint como expresión técnica de los 8 Pilares

---

## 🎯 Visión

**ESLint no es restricción, es guía hacia código que sirve al propósito superior.**

Este proyecto NO es "app CRUD estándar".
Es experiencia inmersiva para transformación consciente.
El código debe reflejar esta intención.

---

## 🏛️ Principios Alineados con Pilares

### **PILAR 1: PUREZA OPERATIVA**
> "Máxima verdad en mínima forma"

**Rules que previenen complejidad innecesaria:**

```javascript
'max-lines': ['warn', { max: 300 }]
```
- **Rationale:** Archivos >300 líneas señalan falta de separación de concerns
- **Acción:** Refactor en múltiples módulos cohesivos
- **Excepción:** Estado Cero inmersivo (max: 500)

```javascript
'complexity': ['warn', 10]
```
- **Rationale:** Complejidad ciclomática >10 es difícil de mantener y testear
- **Acción:** Extraer funciones, simplificar lógica
- **Excepción:** Estado Cero 3D interactions (max: 15)

```javascript
'max-depth': ['warn', 4]
```
- **Rationale:** Nesting profundo >4 indica refactor necesario
- **Acción:** Early returns, guard clauses, composición

```javascript
'max-params': ['warn', 4]
```
- **Rationale:** >4 parámetros sugiere object param o refactor
- **Acción:** Agrupar params relacionados en object

```javascript
'max-lines-per-function': ['warn', { max: 50 }]
```
- **Rationale:** Funciones >50 líneas hacen demasiado
- **Acción:** Single Responsibility Principle
- **Excepción:** Estado Cero animations (max: 100)

---

### **PILAR 3: RESPONSABILIDAD CONSCIENTE**
> "Propiedad total sobre código"

**Rules que detectan código no owned:**

```javascript
'@typescript-eslint/no-unused-vars': 'error'
```
- **Rationale:** Variables no usadas = ruido, falta de consciencia
- **Acción:** Eliminar o usar, prefijo `_` si necesario ignorar

```javascript
'@typescript-eslint/no-explicit-any': 'error'
```
- **Rationale:** `any` es escape de responsabilidad de types
- **Acción:** Type correctamente, usar `unknown` si necesario
- **Filosofía:** Type safety = safety de intención

```javascript
'@typescript-eslint/explicit-function-return-type': 'warn'
```
- **Rationale:** Return types explícitos = intención clara
- **Acción:** Declarar type de retorno
- **Excepción:** Expressions y callbacks (inferencia OK)

```javascript
'no-console': ['warn', { allow: ['warn', 'error', 'info'] }]
```
- **Rationale:** `console.log` olvidados = falta de limpieza
- **Acción:** Usar solo warn/error/info, remover logs de debug

```javascript
'no-debugger': 'error'
```
- **Rationale:** `debugger` statements = código no production-ready
- **Acción:** Remover antes de commit

```javascript
'no-alert': 'warn'
```
- **Rationale:** `alert()` = UX pobre, no contemplativa
- **Acción:** Usar UI components proper

---

### **PILAR 4: EXPRESIÓN AUTÉNTICA**
> "Código que expresa intención clara"

**Rules que enfatizan claridad:**

```javascript
'prefer-const': 'error'
```
- **Rationale:** Inmutabilidad por default = intención clara
- **Acción:** `const` si no reasignas, `let` solo si necesario

```javascript
'no-var': 'error'
```
- **Rationale:** `var` es legacy, confuso scoping
- **Acción:** Siempre `const` o `let`

```javascript
'object-shorthand': ['warn', 'always']
```
- **Rationale:** `{ name: name }` → `{ name }` = más claro
- **Acción:** Usar shorthand cuando clave === valor

```javascript
'prefer-template': 'warn'
```
- **Rationale:** Template literals > concatenación
- **Acción:** \`${name}\` > 'Hello ' + name

```javascript
'prefer-arrow-callback': 'warn'
```
- **Rationale:** Arrow functions = scope claro, menos verboso
- **Acción:** `() => {}` > `function() {}`

---

### **PILAR 5: IMPLEMENTACIÓN TÉCNICA**
> "React/Next.js best practices"

**Rules específicas del stack:**

```javascript
'react/react-in-jsx-scope': 'off'
```
- **Rationale:** Next.js auto-imports React
- **No necesario:** `import React from 'react'`

```javascript
'react-hooks/rules-of-hooks': 'error'
```
- **Rationale:** Hooks tienen reglas estrictas (no condicionales, no loops)
- **Critical:** Viola = bugs sutiles

```javascript
'react-hooks/exhaustive-deps': 'warn'
```
- **Rationale:** Dependencies faltantes = stale closures
- **Acción:** Agregar deps o justificar con comment

```javascript
'react/jsx-no-target-blank': 'error'
```
- **Rationale:** Security (rel="noopener noreferrer" requerido)
- **Acción:** Agregar rel cuando target="_blank"

```javascript
'react/jsx-key': 'error'
```
- **Rationale:** Lists sin keys = performance issues
- **Acción:** Siempre key en .map()

---

### **PILAR 6: CONTRIBUCIÓN ECOSISTÉMICA**
> "Accesibilidad como responsabilidad"

**Rules de a11y (accesibilidad):**

```javascript
'jsx-a11y/alt-text': 'error'
```
- **Rationale:** Imágenes sin alt = inaccesible para screen readers
- **Acción:** Siempre alt descriptivo

```javascript
'jsx-a11y/anchor-is-valid': 'warn'
```
- **Rationale:** Links sin href = no navegables con keyboard
- **Acción:** href válido o button si no es link

```javascript
'jsx-a11y/click-events-have-key-events': 'warn'
```
- **Rationale:** Click sin keyboard event = inaccesible
- **Acción:** Agregar onKeyDown/onKeyPress

```javascript
'jsx-a11y/no-static-element-interactions': 'warn'
```
- **Rationale:** <div onClick> sin role = no semántico
- **Acción:** Usar button o agregar role

**EXCEPCIÓN CONSCIENTE:**

```javascript
'jsx-a11y/no-autofocus': 'off'
```
- **Rationale:** Estado Cero inmersivo NECESITA autofocus
- **Justificación:** Experiencia contemplativa guiada
- **Nota:** Usarlo con intención, no por default

---

### **PILAR 8: EVOLUCIÓN CONTINUA**
> "Prevenir deprecated code"

**Rules que mantienen código moderno:**

```javascript
'@typescript-eslint/no-deprecated': 'warn'
```
- **Rationale:** Detectar APIs deprecated
- **Acción:** Migrar a alternativa moderna

```javascript
'no-restricted-imports': ['error', {
  patterns: [{ group: ['../*'], message: 'Use @/ instead' }]
}]
```
- **Rationale:** Imports relativos parent (`../../`) = frágiles
- **Acción:** Usar absolute imports con `@/`
- **Ejemplo:** `@/lib/utils` > `../../lib/utils`

---

## 🎨 Configuración Especial: Estado Cero Inmersivo

El código de Estado Cero tiene reglas relajadas porque:

```javascript
{
  files: ['**/estado-cero/**/*.tsx'],
  rules: {
    'max-lines-per-function': ['warn', { max: 100 }],
    'complexity': ['warn', 15],
    'max-lines': ['warn', { max: 500 }],
  }
}
```

### **Rationale:**

1. **Animaciones 3D son inherentemente complejas**
   - React Three Fiber code tiene complejidad esencial
   - Geometría, shaders, interactions = código sofisticado

2. **Experiencia inmersiva requiere código sofisticado**
   - Estado Cero es feature CORE del sistema
   - La experiencia vanguardista justifica mayor complejidad

3. **Complejidad esencial ≠ Complejidad accidental**
   - No es excusa para mal código
   - Es reconocimiento de dominio complejo

### **Guidelines Estado Cero:**

✅ **Permitido:**
- Funciones >50 líneas si animación compleja
- Complejidad >10 si interaction 3D
- Archivos >300 líneas si componente 3D cohesivo

❌ **No permitido:**
- Mal naming "porque es complejo"
- Código no comentado "porque es obvio"
- Lógica no testeada "porque es difícil"

**La complejidad debe estar JUSTIFICADA y DOCUMENTADA.**

---

## 🔧 Proceso de Corrección

### **1. Autofix Primero**
```bash
npm run lint:fix
```
- Aplica correcciones automáticas (prefer-const, spacing, etc.)
- 70% de warnings se arreglan automáticamente

### **2. Manual por Prioridad**

**Prioridad 1 (Errores Críticos):**
- `no-unused-vars` - Variables no usadas
- `no-explicit-any` - Types any
- `react-hooks/rules-of-hooks` - Hooks mal usados
- `jsx-a11y/alt-text` - Accesibilidad crítica

**Prioridad 2 (Warnings Importantes):**
- `complexity` - Funciones complejas
- `max-lines-per-function` - Funciones largas
- `react-hooks/exhaustive-deps` - Dependencies faltantes

**Prioridad 3 (Nice to Have):**
- `prefer-const` - const > let
- `object-shorthand` - Shorthand syntax
- `prefer-template` - Template literals

### **3. No Deshabilitar Rules Sin Justificar**

Si desactivas una rule, documenta por qué:

```typescript
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const config: any = complexExternalLibConfig;
// Reason: External lib types incorrect, will fix in v2.0
```

### **4. Revisar en PRs**

- ESLint debe pasar antes de merge
- `npm run check` debe ser 0 errors
- Warnings OK si justificadas

---

## 📊 Métricas de Calidad

### **Target (MVP):**
```yaml
Errors: 0
Warnings: <20
Complexity avg: <8
Max file size: <400 LOC (except Estado Cero)
Type coverage: >95%
```

### **Target (Production):**
```yaml
Errors: 0
Warnings: <5
Complexity avg: <6
Max file size: <300 LOC
Type coverage: 100%
```

---

## ✅ Validación contra 8 Pilares

| Pilar | ESLint Enforcement | Score |
|-------|-------------------|-------|
| **Pilar 1: Pureza Operativa** | ✅ max-lines, complexity, max-depth | 10/10 |
| **Pilar 2: Soberanía Creativa** | ⚪ No aplica directamente | N/A |
| **Pilar 3: Responsabilidad Consciente** | ✅ no-unused-vars, no-explicit-any, no-console | 10/10 |
| **Pilar 4: Expresión Auténtica** | ✅ prefer-const, prefer-template, object-shorthand | 10/10 |
| **Pilar 5: Implementación Técnica** | ✅ react-hooks/*, react/jsx-* | 10/10 |
| **Pilar 6: Contribución Ecosistémica** | ✅ jsx-a11y/* (accesibilidad) | 10/10 |
| **Pilar 7: Sabiduría en Acción** | ✅ Excepciones conscientes (Estado Cero) | 10/10 |
| **Pilar 8: Evolución Continua** | ✅ no-deprecated, no-restricted-imports | 10/10 |

**Total: 7/8 Pilares enforced ✅**

---

## 🎓 Filosofía de Excepciones

### **Cuándo Permitir Excepciones:**

1. **Feature Core Requiere** (Estado Cero 3D)
2. **Dominio Complejo Justifica** (Animaciones, shaders)
3. **Trade-off Consciente Documentado** (Performance vs legibilidad)

### **Cuándo NO Permitir:**

1. ❌ "No tengo tiempo"
2. ❌ "Es más fácil así"
3. ❌ "Nadie lo va a leer"
4. ❌ "Funciona así"

**La calidad contemplativa NO tiene atajos.**

---

## 📚 Referencias

- **ESLint Docs:** https://eslint.org/docs/latest/
- **TypeScript ESLint:** https://typescript-eslint.io/
- **React Hooks Rules:** https://react.dev/reference/rules/rules-of-hooks
- **jsx-a11y Plugin:** https://github.com/jsx-eslint/eslint-plugin-jsx-a11y
- **8 Pilares:** `core/pilares/00-ley-de-la-octava.md`

---

## 🔄 Mantenimiento

### **Revisión Trimestral:**
- Actualizar rules según evolución proyecto
- Revisar excepciones Estado Cero (¿siguen justificadas?)
- Actualizar targets de métricas

### **Cuando Agregar Nueva Rule:**
1. Identificar pattern problemático recurrente
2. Evaluar si rule ayudaría
3. Alinear con Pilares
4. Documentar rationale en este doc
5. Agregar a `eslint.config.mjs`

---

**ESLint como guardián de calidad contemplativa.**

**Autor:** El Entrelazador
**Fecha:** 19 octubre 2025
**Status:** ✅ Configurado
**Próxima revisión:** Q1 2026

---

**إن شاء الله - Código consciente, código contemplativo 🕌✨**
