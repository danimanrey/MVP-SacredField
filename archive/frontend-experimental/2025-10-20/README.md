# Frontend Experimental - Archived 2025-10-20

## estado-cero-inmersivo/

- **Propósito**: Implementación experimental con Canvas Three.js directo
- **Features**: 
  - Sistema de 7 capas (PuertaDeEntrada7Capas)
  - Canvas Three.js sin @react-three/fiber
  - Fetch manual a endpoints
  - Animaciones sacral más complejas
  - Geometría sagrada con pulso lumínico
- **Estado**: Funcional pero duplica estado-cero/page.tsx
- **Razón archivo**: Consolidar en una sola implementación
- **Líneas**: ~695

### Componentes Rescatables

- **PuertaDeEntrada7Capas.tsx**: Ya extraído a `app/components/`
- Geometría sagrada: Preservada en este archivo para referencia
- Patrones de Canvas directo: Útil para optimizaciones futuras

### API Calls Usados

```typescript
fetch('http://localhost:8000/api/estado-cero/iniciar?modo_testing=true')
fetch(`http://localhost:8000/api/estado-cero/${id}/guardar-texto`)
fetch(`http://localhost:8000/api/estado-cero/${id}/responder`)
fetch(`http://localhost:8000/api/estado-cero/${id}/finalizar`)
```

**Diferencia vs versión principal**: Fetch directo vs API client tipado

### Decisión Técnica

**Mantener**: `app/estado-cero/page.tsx`
- Usa `estadoCeroAPI` (cliente tipado)
- Usa `useEstadoCeroStore` (estado global)
- Integrado con `UniversoEsferico` (componente dinámico)
- Flujo completo con validación

**Archivar**: `app/estado-cero-inmersivo/page.tsx`
- Canvas Three.js directo (mayor complejidad)
- Fetch manual (menos type-safety)
- PuertaDeEntrada7Capas ya disponible en components/

## Recuperación

```bash
cp -r archive/frontend-experimental/2025-10-20/estado-cero-inmersivo apps/frontend/app/
```

## Verificación de Impacto

```bash
# Búsqueda de imports rotos
$ cd apps/frontend
$ grep -r "estado-cero-inmersivo" app/
# (ningún resultado = ✓ no hay imports)

# Verificar ruta activa
$ ls apps/frontend/app/estado-cero/page.tsx
✓ Existe

$ ls apps/frontend/app/components/PuertaDeEntrada7Capas.tsx
✓ Existe (componente preservado)
```

## Notas

- Preservar lógica de Canvas directo para optimizaciones futuras
- PuertaDeEntrada7Capas ya está en components globales
- Ideas visuales útiles para mejoras v2.0
- Geometría sagrada con pulso puede inspirar UniversoEsferico
- Fecha: 2025-10-20
- Branch: consolidation/estado-cero-unificado

إن شاء الله

