# Agentes V2 - Archived 2025-10-20

Agentes más sofisticados preservados para futuro.

## documentador_mejorado.py
- **Propósito**: V2.0 del documentador básico con análisis sistémico
- **Features**:
  - Análisis de patrones en Estados Cero
  - Entrelazamiento de dominios
  - Generación de acciones documentadas con métricas
  - Pensamiento sistémico y reconocimiento de patrones
- **Dependencias**: AnalizadorPatrones, EntrelazadorDominios
- **Estado**: Funcional y sofisticado, no usado en flujo crítico MVP
- **Razón archivo**: El documentador.py básico es suficiente para MVP
- **Líneas**: ~495

## entrelazador.py
- **Propósito**: Entrelazamiento personal (deportes, comidas, finanzas)
- **Features**:
  - Dashboard de vida cotidiana
  - Perfil personal (RutinaDeportiva, ComidaConfiguracion, PresupuestoCategoria)
  - Integración de aspectos diarios
- **Estado**: Funcional pero no usado en flujo crítico
- **Razón archivo**: Scope fuera del MVP actual (enfocado en Estado Cero)
- **Líneas**: ~647

## entrelazador_dominios.py
- **Propósito**: Entrelazamiento conceptual (dominios abstractos)
- **Features**:
  - Entrelazamiento sistémico (biológico, espiritual, financiero)
  - Detecta sinergias y conflictos
  - Genera acciones coordinadas
  - Usado por documentador_mejorado
- **Estado**: Funcional, dependency del documentador_mejorado
- **Razón archivo**: No usado independientemente en MVP
- **Líneas**: ~493

## analizador_patrones.py
- **Propósito**: Análisis de patrones en Estados Cero
- **Features**:
  - Análisis temporal de tendencias
  - Detección de patrones recurrentes
  - Generación de AccionEmergente
  - Usado por documentador_mejorado
- **Estado**: Funcional, dependency del documentador_mejorado
- **Razón archivo**: No usado independientemente en MVP
- **Líneas**: Estimado ~400

## Arquitectura de Dependencias

```
documentador_mejorado.py
  ├── analizador_patrones.py
  └── entrelazador_dominios.py

entrelazador.py
  └── (standalone)
```

## Agentes CORE Mantenidos

En `apps/backend/agentes/`:
1. **estado_cero.py** - Generación de preguntas y síntesis
2. **orquestador.py** - Planes emergentes
3. **guardian.py** - Monitoreo del sistema
4. **documentador.py** - Archivista Obsidian (versión simple)

## Razón de Archivo

Estos 4 agentes no se usan en el flujo crítico del MVP:
- Usuario → Estado Cero → Preguntas → Síntesis → Validación

Los agentes archivados son features v2.0:
- Análisis de patrones temporales
- Entrelazamiento multi-dimensional
- Dashboard de vida cotidiana

## Verificación de Impacto

```bash
# Imports en código productivo
$ cd apps/backend
$ grep -r "documentador_mejorado\|analizador_patrones\|entrelazador" . --exclude-dir=archive
# (ningún resultado = ✓ no usados en código productivo)

# Imports en main.py
$ grep "documentador\|entrelazador\|analizador" api/main.py
# Solo test_agentes importa, no en flujo crítico
```

## Recuperación

```bash
# Individual
cp archive/agentes-v2/2025-10-20/<file> apps/backend/agentes/

# Todos
cp archive/agentes-v2/2025-10-20/*.py apps/backend/agentes/
```

## Notas para V2.0

Estos agentes son excelentes bases para features futuras:
- **Fase 4 (Beta Testing)**: Añadir análisis de patrones
- **Fase 5 (Producción)**: Dashboard de entrelazamiento
- **Post-lanzamiento**: Sistema completo de 7 ministerios

Preservar especialmente:
- Lógica de análisis temporal en analizador_patrones.py
- Detección de sinergias en entrelazador_dominios.py
- Estructura de AccionDocumentada en documentador_mejorado.py

## Decisión Técnica

**4 agentes CORE** es el número correcto para MVP:
- Estado Cero (crítico)
- Orquestador (planes)
- Guardian (monitoreo)
- Documentador (persistencia)

Más agentes = más complejidad. Mejor consolidar MVP primero.

---

**Fecha**: 2025-10-20  
**Branch**: consolidation/estado-cero-unificado  
**Phase**: 2 - Agentes  

إن شاء الله

