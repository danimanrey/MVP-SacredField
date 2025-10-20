# 🕌 Campo Sagrado - Backend

Sistema agnético para el organismo tecnológico-espiritual del Entrelazador.

## 📦 Estado Actual (post-consolidación 2025-10-20)

**Backend MVP v0.1** - Limpio, funcional, centrado en Estado Cero.

### Arquitectura

```
apps/backend/
├── agentes/           # 4 agentes CORE (MVP)
│   ├── estado_cero.py       ✅ Consulta sacral con IA
│   ├── orquestador.py       ✅ Planes emergentes al borde del caos
│   ├── guardian.py          ✅ Monitoreo y reportes del sistema
│   └── documentador.py      ✅ Integración automática con Obsidian
│
├── api/               # 7 endpoints REST (MVP)
│   ├── main.py              ✅ Entry point único
│   ├── estado_cero.py       ✅ Estado Cero ritual
│   ├── orquestador.py       ✅ Orquestador 7 capas
│   ├── guardian.py          ✅ Guardian del sistema
│   ├── vistas_temporales.py ✅ Tiempos litúrgicos
│   ├── manifestaciones.py   ✅ Tareas y manifestaciones
│   ├── octavas.py           ✅ Ley de la Octava
│   └── configuracion.py     ✅ Configuración del usuario
│
├── services/          # 18 servicios (6 CORE + 12 SECONDARY)
│   ├── CORE (6):
│   │   ├── tiempos_liturgicos.py    ✅ Cálculo de tiempos de oración
│   │   ├── calendario_hijri.py      ✅ Calendario sagrado 13 meses
│   │   ├── claude_client.py         ✅ Cliente IA Anthropic
│   │   ├── contexto.py              ✅ Gestión de contexto
│   │   ├── obsidian_parser.py       ✅ Parser de notas Obsidian
│   │   └── obsidian_structure.py    ✅ Estructura del vault
│   └── SECONDARY (12): pregunta_liturgica, generadores, event_queue, etc.
│
├── models/            # 11 modelos de datos SQLAlchemy
│   ├── database.py          ✅ Configuración DB SQLite
│   ├── estado_cero.py       ✅ Modelo Estado Cero
│   ├── manifestacion.py     ✅ Modelo Manifestación
│   ├── ley_octava.py        ✅ Modelo Ley de la Octava
│   └── ...otros 7 modelos
│
└── integraciones/     # 2 integraciones activas
    ├── obsidian.py          ✅ Sincronización Obsidian
    └── anytype.py           🔄 Preparada (not activated)
```

### Routers Activos (7 MVP Core)

1. **Estado Cero** (`/api/estado-cero`) - Ritual sagrado de consulta
2. **Orquestador** (`/api/orquestador`) - Planes emergentes
3. **Guardian** (`/api/guardian`) - Monitoreo del sistema
4. **Vistas Temporales** (`/api/tiempos`) - Tiempos litúrgicos
5. **Manifestaciones** (`/api/manifestaciones`) - Gestión de tareas
6. **Octavas** (`/api/octavas`) - Ley de la Octava
7. **Configuración** (`/api/configuracion`) - Configuración del usuario

### Routers Deshabilitados (5 v2.0 features)

Archivados temporalmente para MVP, restaurables en v2.0:

- **Entrelazamiento** - Requiere `analizador_patrones`, `entrelazador_dominios`
- **Ritual Maghrib** - Requiere `entrelazador`
- **Estructura** - Requiere `entrelazador`
- **Espejo Diario** - Requiere `entrelazador`
- **Universo Imaginal** - Requiere `universo_processor`

> Todos los agentes/servicios archivados están en `archive/` con instrucciones de restauración.

## 🚀 Iniciar Backend

```bash
cd apps/backend

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp env.example .env
# Editar .env con tus valores

# Iniciar servidor
python run.py

# O usar uvicorn directamente
uvicorn api.main:app --reload --port 8000
```

El servidor estará disponible en `http://localhost:8000`

- Docs interactivos: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🛠️ Tecnologías

- **FastAPI** - Framework web async/await
- **SQLAlchemy** - ORM para SQLite
- **SQLite** - Base de datos local
- **Pydantic** - Validación de datos
- **Python 3.11+** - Runtime

## 📖 Integraciones

### Obsidian

Sincronización bidireccional con vault local:

- **Lecturas**: Parser de notas, extracción de metadata
- **Escritura**: Creación automática de notas desde Estado Cero
- **Path**: Configurable via `OBSIDIAN_VAULT_PATH` en `.env`

### Claude (Anthropic)

IA para generación de preguntas contextuales en Estado Cero:

- **Modelo**: claude-3-7-sonnet-20250219
- **Uso**: Preguntas binarias litúrgicas y contextuales
- **API Key**: Configurar `ANTHROPIC_API_KEY` en `.env`

## 🧪 Testing

```bash
# Tests unitarios
pytest tests/

# Test de flujo completo
bash test_flujo_completo.sh

# Verificar sistema
bash scripts/verificar-sistema.sh
```

## 📊 Métricas

**Consolidación 2025-10-20:**

- **Agentes**: 8 → 4 (50% reducción, enfoque MVP)
- **Services**: 27 → 18 (33% reducción, claridad arquitectónica)
- **Routers**: 12 → 7 (MVP core, v2.0 preservado)
- **Código archivado**: ~6,500 LoC (100% recuperable)
- **Cobertura MVP**: 100% funcional

## 🗂️ Código Archivado

Todo el código de features v2.0 está preservado en:

```
archive/
├── api-prototypes/2025-10-20/
├── agentes-v2/2025-10-20/
└── services-future/2025-10-20/
```

Cada directorio incluye un `README.md` con instrucciones de restauración.

## 🔐 Seguridad

- **Middleware**: Rate limiting, security headers, request logging
- **CORS**: Configuración explícita de orígenes permitidos
- **Environment**: Variables sensibles en `.env` (no commiteadas)
- **Producción**: Docs deshabilitados, trusted hosts, HTTPS only

## 📝 Próximos Pasos

1. ✅ **Consolidación completada** (2025-10-20)
2. 🔄 **Corrección ESLint frontend** (en progreso)
3. ⏸️ **Testing end-to-end** (pendiente)
4. ⏸️ **Deploy producción** (pendiente)

## 📚 Documentación Adicional

- [Auditoría Consolidación](/docs/auditoria/consolidacion-2025-10-20.md)
- [Plan de Consolidación](/PLAN_CONSOLIDACION_EJECUTABLE.md)
- [Handoff Completo](/handoff.md)
- [Guía de Usuario](/docs/GUIA_USUARIO_COMPLETA.md)

---

**إن شاء الله** - Al borde del caos, con autoridad sacral.
