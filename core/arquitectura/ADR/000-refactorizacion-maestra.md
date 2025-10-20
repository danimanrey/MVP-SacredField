# ADR 000: Refactorización Maestra - Vía Recta

## Estado
🟢 ACEPTADO

## Fecha
2025-10-19

## Contexto

### Situación Actual

- Sistema funcional (7.1/10 en auditoría)
- 60+ archivos MD en raíz causando desorganización
- 3 frontends diferentes (2 legacy no usados)
- Dependencies desincronizadas (Poetry ≠ requirements.txt)
- 0% cobertura de tests en frontend
- Sin ESLint en frontend

### Problemas Identificados

#### Técnicos:

- Caos documental impide navegación
- Código duplicado en múltiples frontends
- Estructura backend funcional pero no sigue Clean Architecture
- Testing insuficiente (frontend 0%, backend parcial)
- Dependencias no gestionadas profesionalmente

#### Epistemológicos:

- Ausencia de ontología clara del conocimiento
- Jerarquías emergen de conveniencia, no principios
- Nomenclatura inconsistente
- Decisiones arquitectónicas no documentadas

#### Alineación con Pilares:

- ❌ Pilar 1 (Pureza Operativa): Estructura confusa
- ❌ Pilar 3 (Responsabilidad): Tests insuficientes
- ❌ Pilar 8 (Evolución): Difícil refactorizar

## Decisión

Refactorización completa del proyecto siguiendo:

### Arquitectura Backend

- Clean Architecture (Uncle Bob)
- Domain-Driven Design (Eric Evans)
- Capas: Domain → Application → Infrastructure
- Dependency Inversion estricta
- Repository Pattern
- Use Case Pattern

### Arquitectura Frontend

- Feature-Sliced Design (metodología moderna)
- Capas: app → features → entities → shared
- Atomic Design para componentes UI
- Hooks Pattern
- Composition over Inheritance

### Estructura del Proyecto

Monorepo con:
- core/ (pilares, ontología, ADRs)
- apps/ (backend, frontend)
- packages/ (código compartido)
- data/ (vault, storage, logs)
- docs/ (documentación organizada)
- archive/ (históricos)

### Principios Guía

1. **Pureza Técnica**: Código que cumple estándares senior/staff
2. **Coherencia Ontológica**: Estructura revela el dominio
3. **Alineación Sagrada**: Código refleja 8 Pilares

## Consecuencias

### Positivas
✅ Navegación intuitiva del proyecto
✅ Onboarding <15 minutos para nuevos devs
✅ Refactors seguros con tests comprehensivos
✅ Escalabilidad sin fricción
✅ Código profesional portfolio-ready
✅ Base sólida para visión final (interfaz inmersiva)

### Negativas
⚠️ 2 semanas de refactorización intensiva (3-4h/día)
⚠️ Breaking changes en imports
⚠️ Necesita actualizar toda documentación
⚠️ Periodo de adaptación al nuevo layout

### Riesgos Mitigados

- ✅ Backup completo antes de comenzar
- ✅ Branch separado (refactor/via-recta-maestra)
- ✅ Commits frecuentes
- ✅ Tests antes de cada commit
- ✅ Rollback plan documentado

## Implementación

Ver plan detallado en:
- docs/desarrollo/plan-refactorizacion-maestra.md
- Timeline: 14 días (Fase 0-4)

## Validación

Sistema refactorizado exitosamente cuando:

- ✓ Root con máximo 8 archivos
- ✓ ESLint 0 errores
- ✓ TypeScript strict 0 errores
- ✓ Backend coverage >75%
- ✓ Frontend coverage >50%
- ✓ CI pipeline passing
- ✓ Cada Pilar verificable en código

## Referencias

- Clean Architecture: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- Feature-Sliced Design: https://feature-sliced.design/
- DDD: Eric Evans "Domain-Driven Design"

## Autor
El Entrelazador
