# API Endpoints Actuales

Fecha: 20-oct-2025

Nota: Solo se listan endpoints activos según `apps/backend/api/main.py`. El router de `calendario` está comentado y por tanto NO está expuesto.

## Implementados

### Raíz y Salud del sistema (main)
- GET `/` → Información básica del organismo
- GET `/api/health` → Status del backend y contexto temporal
- GET `/api/tiempos-hoy` → Tiempos de rezo de hoy
- GET `/api/tiempos-precisos` → Tiempos litúrgicos precisos (opcional `fecha`)
- GET `/api/verificar-momento` → Verifica si ahora es momento de Estado Cero
- GET `/api/test-agentes` → Verifica disponibilidad de agentes
- GET `/api/calendario-hijri/hoy` → Contexto del día Hijri
- GET `/api/calendario-hijri/año` → Vista anual Hijri
- GET `/api/tiempos-liturgicos/hoy` → Tiempos litúrgicos detallados de hoy

### Estado Cero (`/api/estado-cero`)
- GET `/api/estado-cero/test`
- POST `/api/estado-cero/simple`
- GET `/api/estado-cero/verificar-momento`
- GET `/api/estado-cero/ventanas-perdidas`
- POST `/api/estado-cero/iniciar-test`
- POST `/api/estado-cero/iniciar` (query: `permitir_recuperacion`, `modo_testing`)
- POST `/api/estado-cero/{estado_id}/guardar-texto`
- POST `/api/estado-cero/{estado_id}/responder`
- POST `/api/estado-cero/{estado_id}/sintetizar`
- POST `/api/estado-cero/{estado_id}/chat`
- POST `/api/estado-cero/{estado_id}/finalizar`
- GET `/api/estado-cero/asr-test/`
- GET `/api/estado-cero/{estado_id}`
- GET `/api/estado-cero/` (listar)

### Orquestador (`/api/orquestador`)
- POST `/api/orquestador/generar-plan`
- GET `/api/orquestador/plan-actual`
- POST `/api/orquestador/chat`
- POST `/api/orquestador/ajustar-plan`
- POST `/api/orquestador/establecer-no-negociables`
- GET `/api/orquestador/estado-jornada`
- POST `/api/orquestador/reiniciar-jornada`
- GET `/api/orquestador/espejo-diario/{fecha}`

### Guardián (`/api/guardian`)
- POST `/api/guardian/reporte-diario`
- GET `/api/guardian/salud-sistema`
- GET `/api/guardian/patrones`
- GET `/api/guardian/metricas-hoy`
- GET `/api/guardian/metricas-semana`
- GET `/api/guardian/estado-general`
- POST `/api/guardian/reporte-automatico`
- GET `/api/guardian/alertas`
- GET `/api/guardian/estado-sistema`
- GET `/api/guardian/reportes/diario`

### Entrelazamiento (prefijo `/api`)
- Varias rutas en `entrelazamiento.py` (expuestas bajo `/api/...`) — consultar archivo para detalle fino (no se detectaron firmas adicionales por grep más allá del include general).

### Ritual Maghrib (`/api/maghrib`)
- Rutas definidas en `ritual_maghrib.py` (consultar archivo para detalle; no todas tienen firmas capturadas por el grep rápido).

### Estructura (`/api/estructura`)
- Rutas en `estructura.py` para estructura del día (consultar archivo para listado completo).

### Espejo Diario (`/api/espejo-diario`)
- GET `/api/espejo-diario/hoy` (según firmas en archivo; ver `espejo_diario.py`)

### Vistas Temporales (prefijo `/api`)
- GET `/api/contexto-temporal`
- GET `/api/vista-semanal`
- GET `/api/vista-mensual`
- GET `/api/vista-anual`
- GET `/api/dias-semana`
- GET `/api/meses-hijri`

### Manifestaciones (`/api/manifestaciones`)
- GET `/api/manifestaciones/dimensiones`
- GET `/api/manifestaciones/dimension/{dimension_id}`
- POST `/api/manifestaciones/manifestacion`
- PUT `/api/manifestaciones/manifestacion/{manifestacion_id}/progreso`
- GET `/api/manifestaciones/auditoria-dimensiones`
- GET `/api/manifestaciones/manifestaciones-prioritarias`

### Octavas (`/api/octavas`)
- GET `/api/octavas/correspondencias`
- POST `/api/octavas/crear-objetivo`
- GET `/api/octavas/objetivo/{objetivo_id}`
- GET `/api/octavas/objetivo/{objetivo_id}/estado`
- GET `/api/octavas/objetivo/{objetivo_id}/armonicos`
- POST `/api/octavas/objetivo/{objetivo_id}/shock`
- GET `/api/octavas/shocks-hoy`
- GET `/api/octavas/dimension-hoy`
- GET `/api/octavas/resumen-octavas`
- GET `/api/octavas/objetivo/{objetivo_id}/espiral`
- GET `/api/octavas/objetivos-por-dia/{dia}`

### Universo Imaginal (`/api/universo-imaginal`)
- GET `/api/universo-imaginal/test`
- GET `/api/universo-imaginal/universo`
- GET `/api/universo-imaginal/estrellas`
- GET `/api/universo-imaginal/estrellas/{estrella_id}`
- GET `/api/universo-imaginal/constelaciones`
- GET `/api/universo-imaginal/estadisticas`
- GET `/api/universo-imaginal/balance-dimensiones`
- GET `/api/universo-imaginal/hubs`
- GET `/api/universo-imaginal/orphans`
- POST `/api/universo-imaginal/regenerar`

### Configuración (`/api/configuracion`)
- POST `/api/configuracion/individual`
- GET `/api/configuracion/individual`
- PUT `/api/configuracion/individual`
- DELETE `/api/configuracion/individual`
- GET `/api/configuracion/dimensiones`

## Necesarios para Hito 1
- POST `/estado-cero` → Guardar sesión
- GET `/estado-cero/recent` → Últimas 7 sesiones
- POST `/consulta-sacral` → Guardar consulta
- GET `/consulta-sacral/historia` → Historial

## Missing critical
- Falta alias simple `POST /estado-cero` (existe `POST /api/estado-cero/iniciar` y flujos por `/{id}/finalizar`).
- Falta `GET /estado-cero/recent` explícito (hay `GET /api/estado-cero/` listar; no hay endpoint "recent" dedicado).
- No existen endpoints de `consulta-sacral` (crear e historial).
- Rutas de Calendario están implementadas en `api/calendario.py` pero el router está comentado en `main.py` (no expuestas):
  - GET `/api/calendario/eventos/hoy`, POST `/api/calendario/eventos`, PUT/DELETE evento, POST `/api/calendario/validar-calendario`, etc. — requieren reactivar `app.include_router(calendario.router, prefix="/api/calendario", ...)`.



