# Services Future - Archived 2025-10-20

Services no usados en flujo MVP actual. Preservados para v2.0.

## Archivados (9 services)

### 1. metabolizador_metadatos.py
- **Propósito**: Procesamiento avanzado de metadatos
- **Features**: Extracción y análisis de metadata compleja
- **Razón archivo**: No usado en flujo crítico Estado Cero

### 2. motor_prisma.py
- **Propósito**: Configuración personalizada según tipología
- **Features**: MBTI, Eneagrama, Human Design integration
- **Razón archivo**: Configuración estática suficiente para MVP

### 3. sumario_contexto.py
- **Propósito**: Generación de sumarios contextuales
- **Features**: GestorSumarioContexto para análisis
- **Razón archivo**: No usado activamente

### 4. gestor_octavas.py
- **Propósito**: Implementación de Ley de la Octava
- **Features**: Gestión de interrupciones y shocks
- **Razón archivo**: Feature avanzada para v2.0

### 5. notificador_liturgico.py
- **Propósito**: Notificaciones de tiempos litúrgicos
- **Features**: Alerts y recordatorios automáticos
- **Razón archivo**: MVP no incluye notificaciones push

### 6. universo_processor.py
- **Propósito**: Procesamiento de datos de universo imaginal
- **Features**: Análisis de patrones en dimensiones
- **Razón archivo**: Feature avanzada para v2.0

### 7. propositos.py
- **Propósito**: Gestión de propósitos y anclas diarias
- **Features**: obtener_proposito_dia_semana, calcular_espacio_libre
- **Razón archivo**: Usado solo por entrelazador (archivado)

### 8. calculador_cosmico.py
- **Propósito**: Cálculos astronómicos avanzados
- **Features**: Fases lunares, posiciones planetarias
- **Razón archivo**: tiempos_liturgicos.py es suficiente para MVP

### 9. calendario_hijri_backup.py
- **Propósito**: Backup de implementación de calendario
- **Features**: Alternativa a calendario_hijri.py
- **Razón archivo**: calendario_hijri.py es la versión activa

## Services Mantenidos (18 services)

### CORE (6 services - críticos):
1. **tiempos_liturgicos.py** - Cálculo astronómico preciso
2. **calendario_hijri.py** - Sistema de 13 meses  
3. **claude_client.py** - IA generativa (Anthropic)
4. **contexto.py** - Recopilación de contexto
5. **obsidian_parser.py** - Parseo de vault
6. **obsidian_structure.py** - Estructura de vault

### SECONDARY (12 services - condicionales):
7. **pregunta_liturgica.py** - Generación de preguntas
8. **generador_preguntas.py** - Preguntas emergentes
9. **generador_preguntas_7_capas.py** - Sistema 7 capas
10. **orquestador_7_capas.py** - Orquestación compleja
11. **event_queue.py** - Cola de eventos
12. **audit_trail.py** - Trazabilidad
13. **google_calendar.py** - Integración Google Calendar
14. **hrv_integration.py** - HRV (Heart Rate Variability)
15. **vector_store.py** - Almacenamiento vectorial
16. **espejo_diario_generator.py** - Generador de espejo
17. **auth.py** - Autenticación
18. **rate_limiter.py** - Rate limiting

## Decisión Técnica

**18 services** es el número correcto para MVP:
- 6 CORE: Absolutamente críticos para Estado Cero
- 12 SECONDARY: Usados condicionalmente o por routers específicos

Los 9 archivados son features v2.0 que añaden complejidad sin valor inmediato.

## Verificación de Impacto

```bash
# Buscar imports de services archivados
cd apps/backend
grep -r "metabolizador_metadatos\|motor_prisma\|sumario_contexto\|gestor_octavas\|notificador_liturgico\|universo_processor\|propositos\|calculador_cosmico\|calendario_hijri_backup" . --exclude-dir=archive --exclude-dir=__pycache__

# Resultado esperado: 
# - Algunos matches en archivos archivados (agentes v2.0, routers deshabilitados)
# - No matches en código activo (agentes CORE, routers activos)
```

**Imports encontrados** (esperados):
- agentes/estado_cero.py → motor_prisma, sumario_contexto (safe, try/except)
- api archivados → propositos, etc (safe, routers deshabilitados)

**No imports** en:
- Routers activos (estado_cero.router, orquestador.router, guardian.router)
- Agentes CORE activos

## Recuperación

```bash
# Individual
cp archive/services-future/2025-10-20/<file> apps/backend/services/

# Todos
cp archive/services-future/2025-10-20/*.py apps/backend/services/
```

## Notas para V2.0

Estos services son bases para features futuras:

**Fase 4 (Beta Testing)**:
- notificador_liturgico.py (push notifications)
- calculador_cosmico.py (lunar phases UI)

**Fase 5 (Producción)**:
- motor_prisma.py (personalización profunda)
- universo_processor.py (análisis dimensional)
- metabolizador_metadatos.py (insights automáticos)

**Post-lanzamiento**:
- gestor_octavas.py (Ley de la Octava completa)
- Reactivar entrelazamiento completo

## Impacto

Services count: 27 → 18 (-33%)
Code preserved: 100% (~3,500 LoC archived)
Complexity: Significativa reducción
Clarity: 100% (CORE vs SECONDARY vs FUTURE)

---

**Fecha**: 2025-10-20  
**Branch**: consolidation/estado-cero-unificado  
**Phase**: 3 - Services  

إن شاء الله

