# Migración de Frontends Legacy

## Resumen
- **Fecha**: 2025-10-19
- **Frontends eliminados**: `frontend/` (SvelteKit), `frontend-next/` (Next.js 15 vacío)
- **Frontend final**: `apps/frontend/` (anteriormente `campo-sagrado-nextjs/`)
- **Código rescatado**: `/tmp/frontend-rescue/`

---

## Análisis Pre-Eliminación

### Frontend 1: `frontend/` (SvelteKit)
- **Framework**: SvelteKit 2.0 + Svelte 4.2.7
- **Tamaño**: 68 MB
- **Componentes**: 33 archivos .svelte
- **Estado**: ✅ Funcional pero obsoleto (Puerto 5173 legacy)
- **Último commit**: 5a9f89d6 (pre-refactorización)

### Frontend 2: `frontend-next/` (Next.js 15)
- **Framework**: Next.js 15.1.3 + React 19
- **Tamaño**: 486 MB
- **Componentes**: 2 archivos .tsx (solo esqueleto)
- **Estado**: ⚠️ Abandonado - Experimento sin implementación
- **Último commit**: f8fcc4a1 (checkpoint)

### Frontend 3: `campo-sagrado-nextjs/` → `apps/frontend/`
- **Framework**: Next.js 14.2 + React 18.3
- **Tamaño**: 609 MB
- **Componentes**: 16 archivos .tsx
- **Estado**: ✅ ACTIVO - Frontend principal en producción
- **Features implementadas**:
  - ✅ Sistema 7 capas
  - ✅ Estado Cero (3 variantes)
  - ✅ Onboarding (4 pasos)
  - ✅ Dashboard
  - ✅ Espejo Diario

---

## Código Rescatado

### Componentes Únicos Extraídos

Todos los componentes fueron copiados a `/tmp/frontend-rescue/componentes/`:

#### 1. **Octavas/** (Ley de la Octava)
- `EspiralOctavas.svelte` - Visualización en espiral de la Ley de la Octava
- `DashboardOctavas.svelte` - Dashboard de seguimiento de octavas
- **Razón**: ❌ NO existe en `apps/frontend/`
- **Prioridad**: 🔴 ALTA - Feature filosófica fundamental
- **Acción pendiente**: Reescribir en React + Three.js

#### 2. **Dimensiones/** (Las 7 Dimensiones del Ser)
- `VistaDimensiones.svelte` - Visualización de las 7 dimensiones
- **Razón**: ❌ NO existe en `apps/frontend/`
- **Prioridad**: 🔴 ALTA - Pilar arquitectónico del sistema
- **Acción pendiente**: Implementar en React

#### 3. **Vistas/** (Temporal)
- `VistaSemanal.svelte` - Vista semanal del calendario
- `VistaAnual.svelte` - Vista anual del calendario
- **Razón**: ❌ NO existe en `apps/frontend/`
- **Prioridad**: 🟡 MEDIA - UX mejorado
- **Acción pendiente**: Implementar vistas calendario

#### 4. **EspejoDiario/** (Features avanzadas)
- `NoNegociables.svelte` - Gestión de no-negociables
- `JornadaCaos.svelte` - Planificación al borde del caos (40% libre)
- `ChatbotAclaraciones.svelte` - Chatbot de aclaraciones
- `EspejoDinamico.svelte` - Espejo dinámico adaptativo
- **Razón**: ⚠️ Espejo Diario básico existe, pero sin estas features avanzadas
- **Prioridad**: 🟡 MEDIA - Mejoras de UX
- **Acción pendiente**: Evaluar e integrar lógica

#### 5. **EstadoCero/** (Componentes complementarios)
- `ChatClarificador.svelte` - Chat de clarificación
- `EsferaCuboMeditacion.svelte` - Geometría 3D meditativa
- `ConsultaSacralMejorada.svelte` - Versión mejorada de consulta
- `VerificacionMomento.svelte` - Validación de momento litúrgico
- **Razón**: ✅ Estado Cero existe en `apps/frontend/`, pero sin estas variantes
- **Prioridad**: 🟢 BAJA - Estado Cero actual es funcional
- **Acción pendiente**: Revisar si aportan valor incremental

#### 6. **Shared/** (Componentes reutilizables)
- `GeometriaSagrada.svelte` - Componente de geometría reutilizable
- `TiempoLiturgico.svelte` - Display de tiempo litúrgico
- `Navegacion.svelte` - Navegación
- **Razón**: ✅ Existen equivalentes en `apps/frontend/`
- **Prioridad**: ⚪ NINGUNA - Ya implementados
- **Acción**: Descartar

---

### Configuraciones Rescatadas

Copiadas a `/tmp/frontend-rescue/config/`:

#### De `frontend/` (SvelteKit):
- `svelte.config.js` - Config de SvelteKit
- `vite.config.ts` - Config de Vite
- **Uso**: Referencia para build tooling

#### De `frontend-next/` (Next.js 15):
- `next.config.ts` - Config de Next.js 15
- `tailwind.config.ts` - Config de Tailwind 3.4
- `tsconfig.json` - TypeScript strict config
- **Uso**: Referencia para futuro upgrade a Next.js 15 + React 19

---

### Assets Únicos

- **Resultado**: ❌ No se encontraron assets únicos
- Ningún frontend tenía imágenes, fonts o recursos propios
- Todo se genera programáticamente con Three.js/SVG

---

## Código Descartado

### Frontend SvelteKit (`frontend/`)
**Razón de descarte**:
- Stack tecnológico diferente (Svelte vs React)
- Componentes Shared ya reimplementados en Next.js
- Puerto 5173 no usado en producción
- Código rescatado está preservado en `/tmp/frontend-rescue/`

**Componentes descartados directamente**:
- Todo `src/routes/` - Routing específico de SvelteKit
- `src/lib/stores/` - Stores de Svelte (Next.js usa Zustand)
- Componentes Shared - Ya existen en `apps/frontend/`

### Frontend Next.js 15 (`frontend-next/`)
**Razón de descarte**:
- ⚠️ **Proyecto abandonado** - Solo 2 archivos básicos
- No tiene implementación real (solo `layout.tsx` y `page.tsx` vacíos)
- Era un experimento para probar Next.js 15 + React 19
- Config rescatada para referencia futura

**Todo descartado**:
- `app/layout.tsx` - Layout básico sin customización
- `app/page.tsx` - Homepage vacía
- 486 MB de `node_modules` innecesarios

---

## Features Faltantes en `apps/frontend/`

### 🔴 CRÍTICAS (Pilares del sistema)
1. **Octavas** - Ley de la Octava (visualización + dashboard)
2. **7 Dimensiones** - Las dimensiones del ser

### 🟡 IMPORTANTES (UX mejorado)
3. **Vistas Calendario** - Semanal/Anual
4. **No-Negociables** - Gestión avanzada
5. **Jornada al Caos** - Planificación 40% libre

### 🟢 OPCIONALES (Nice to have)
6. Estado Cero variantes adicionales
7. Chat clarificador

---

## Tamaño y Espacio

| Métrica | Antes | Después | Ahorro |
|---------|-------|---------|--------|
| **Frontends totales** | 3 | 1 | -2 frontends |
| **Espacio en disco** | ~1.16 GB | ~609 MB | **~554 MB liberados** |
| **Componentes** | 51 archivos | 16 archivos | -35 archivos |

---

## Próximos Pasos

### Inmediato (Fase 1)
- [x] Extraer componentes únicos a `/tmp/frontend-rescue/`
- [x] Documentar en `migracion-frontends.md`
- [ ] Eliminar `frontend/`
- [ ] Eliminar `frontend-next/`
- [ ] Renombrar `campo-sagrado-nextjs/` → `apps/frontend/`

### Futuro (Fase 2+)
- [ ] **Implementar Octavas** - Reescribir `EspiralOctavas` y `DashboardOctavas` en React/Three.js
- [ ] **Implementar 7 Dimensiones** - Reescribir `VistaDimensiones` en React
- [ ] **Añadir Vistas Calendario** - Implementar vistas semanal/anual
- [ ] **Evaluar No-Negociables** - Decidir si integrar en Espejo Diario
- [ ] **Evaluar Jornada al Caos** - Decidir si integrar algoritmo 40% libre
- [ ] **Limpiar `/tmp/frontend-rescue/`** - Una vez confirmado que no se necesita

---

## Comandos de Rescate Ejecutados

```bash
# Crear estructura de rescate
mkdir -p /tmp/frontend-rescue/{componentes,config,assets,docs}

# Copiar componentes únicos críticos
cp -r frontend/src/lib/components/Octavas /tmp/frontend-rescue/componentes/
cp -r frontend/src/lib/components/Dimensiones /tmp/frontend-rescue/componentes/
cp -r frontend/src/lib/components/Vistas /tmp/frontend-rescue/componentes/
cp -r frontend/src/lib/components/EspejoDiario /tmp/frontend-rescue/componentes/

# Copiar configs de referencia
cp frontend/svelte.config.js /tmp/frontend-rescue/config/
cp frontend/vite.config.ts /tmp/frontend-rescue/config/
cp frontend-next/next.config.ts /tmp/frontend-rescue/config/
cp frontend-next/tailwind.config.ts /tmp/frontend-rescue/config/
cp frontend-next/tsconfig.json /tmp/frontend-rescue/config/
```

---

## Ubicación del Código Rescatado

```
/tmp/frontend-rescue/
├── componentes/
│   ├── Octavas/          # 🔴 CRÍTICO
│   ├── Dimensiones/      # 🔴 CRÍTICO
│   ├── Vistas/           # 🟡 IMPORTANTE
│   └── EspejoDiario/     # 🟡 IMPORTANTE
├── config/
│   ├── next.config.ts    # Next.js 15 (referencia)
│   ├── svelte.config.js  # SvelteKit (referencia)
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── vite.config.ts
├── assets/               # (vacío)
└── docs/                 # (este documento)
```

---

## Notas Importantes

1. **⚠️ Código Temporal**: `/tmp/frontend-rescue/` se borrará al reiniciar
   - Copiar a ubicación permanente si se necesita preservar
   - Sugerencia: `archive/frontend-svelte-legacy/` si se quiere archivar

2. **Tecnología Diferente**: Componentes son Svelte, no React
   - No se pueden copiar directamente
   - Requieren reescritura completa en React
   - Lógica de negocio sí es reutilizable

3. **Priorización**: Implementar en este orden:
   1. Octavas (Pilar filosófico)
   2. 7 Dimensiones (Pilar arquitectónico)
   3. Vistas calendario (UX)
   4. Resto según necesidad

---

**Autor**: El Entrelazador
**Fecha**: 2025-10-19
**Fase**: Refactorización Maestra - Vía Recta (Día 2)
