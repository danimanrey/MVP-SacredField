# Limpieza de Backend - Directorios Nested

## Fecha
2025-10-19

## Contexto
Durante la refactorización Vía Recta Maestra se identificaron directorios nested incorrectos en `backend/` que generaban confusión estructural.

---

## Directorios Eliminados

### 1. `backend/backend/` ❌ ELIMINADO

#### Contenido:
- Solo `.env` (16 líneas)
- Tamaño: 4 KB

#### Razón de eliminación:
- **Duplicado**: backend/.env (23 líneas) es más completo
- **Sin referencias**: No se usa en ningún import activo
- **Legacy**: Creado 16 oct, no usado desde entonces

#### Contenido del .env eliminado:
```env
# 🕌 CAMPO SAGRADO - CONFIGURACIÓN DEL SISTEMA
LATITUD="40.5486"
LONGITUD="-3.6263"
TIMEZONE="Europe/Madrid"
OBSIDIAN_VAULT_PATH="/Users/hp/Documents/CampoSagrado"

# Google Calendar API Key
GOOGLE_CALENDAR_API_KEY=""
GOOGLE_CALENDAR_ID="primary"

BACKEND_PORT="8000"
DEBUG="true"
SECRET_KEY="campo-sagrado-secret-key-change-in-production"
```

**Todas estas variables ya existen en backend/.env**

---

### 2. `backend/app/` ❌ ELIMINADO

#### Contenido (117 archivos):
```
app/
├── __init__.py
├── agentes/
│   └── __init__.py
├── api/
│   └── __init__.py
├── config.py (10,493 bytes - configuración legacy)
├── core/
│   ├── __init__.py
│   ├── deps.py
│   ├── exceptions.py
│   └── logger.py
├── integraciones/
│   └── __init__.py
├── main.py (3,938 bytes - FastAPI app legacy)
├── middleware/
│   ├── __init__.py
│   ├── cors.py
│   ├── error_handler.py
│   └── timing.py
├── models/
│   ├── __init__.py
│   └── responses.py
└── services/
    └── __init__.py
```

#### Tamaño total: 116 KB

#### Razón de eliminación:
- **Estructura duplicada**:
  - `backend/app/agentes/` vs `backend/agentes/` (activo)
  - `backend/app/api/` vs `backend/api/` (activo)
  - `backend/app/services/` vs `backend/services/` (activo)
- **Sin referencias**: No hay imports a `backend.app.*` en código activo
- **Legacy**: Último commit pre-refactorización (f8fcc4a1)
- **Entry point**: El activo es `backend/api/main.py`, no `backend/app/main.py`

#### Código valioso identificado:

**config.py** (10 KB):
- Configuración legacy de FastAPI
- Algunas constantes podrían ser útiles
- **Acción**: Revisado, nada crítico no presente en versión activa

**main.py** (4 KB):
- FastAPI app con estructura antigua
- Middleware básico (CORS, error handling, timing)
- **Acción**: Middleware ya implementado en backend/middleware/

**core/** (logger, exceptions, deps):
- Logger configurado
- Excepciones custom
- Dependencies injection
- **Acción**: Funcionalidad ya en backend/core/ o backend/utils/

#### Verificación de no-referencias:
```bash
grep -r "from app\." backend/ --include="*.py" --exclude-dir=__pycache__
grep -r "import app\." backend/ --include="*.py" --exclude-dir=__pycache__
```
**Resultado**: Sin matches (confirmado que no se usa)

---

## Estructura Activa (Conservada)

```
backend/
├── .env                    # ✅ Configuración activa
├── run.py                  # ✅ Entry point principal
├── api/
│   └── main.py            # ✅ FastAPI app activa
├── agentes/               # ✅ Agentes del sistema
├── services/              # ✅ Servicios activos
├── models/                # ✅ Modelos de datos
├── middleware/            # ✅ Middleware activo
└── ...
```

---

## Impacto

### Antes de limpieza:
- Estructura confusa con duplicados
- 2 directorios `.env` diferentes
- Estructura nested `app/` no usada
- Potencial de imports erróneos

### Después de limpieza:
- ✅ Estructura clara y plana
- ✅ Un solo `.env` en ubicación correcta
- ✅ Sin directorios legacy confusos
- ✅ Espacio liberado: ~120 KB

---

## Validación Post-Limpieza

### Tests ejecutados:
```bash
# Verificar que run.py funciona
python backend/run.py --help

# Verificar imports
python -c "from api.main import app; print('OK')"

# Verificar .env carga
python -c "from dotenv import load_dotenv; load_dotenv('backend/.env'); import os; print(os.getenv('ANTHROPIC_API_KEY')[:10])"
```

**Resultado**: ✅ Todos los tests pasan

---

## Referencias a Código Activo

### Entry Points:
- **Principal**: `backend/run.py`
- **FastAPI**: `backend/api/main.py`

### Imports activos verificados:
- `from api.main import app`
- `from agentes.* import *`
- `from services.* import *`
- `from models.* import *`

**Ninguno usa** `from app.*`

---

## Próximos Pasos (Fase 2+)

- [ ] Reestructurar backend/ según DDD (Domain-Driven Design)
- [ ] Separar en capas: Domain, Application, Infrastructure
- [ ] Mover a `apps/backend/`
- [ ] Implementar Clean Architecture

---

---

## 3. Consolidación de Storage

### Antes:
- `storage/` (root) - 160 KB (organismo.db, datos_prueba.json)
- `backend/storage/` - Datos activos (estados_cero/, emocional/, etc.)

### Después:
- `data/storage/` - ✅ Consolidado (todos los datos)
- `backend/storage` → symlink a `../../data/storage`
- ~~`storage/`~~ (root) - ❌ Eliminado

### Path References en Código:

**Archivos con paths hardcoded a `storage/`**:
- `backend/scripts/generar_datos_prueba.py` (1 referencia absoluta)
- `backend/api/estado_cero_simple.py` (2 referencias `Path("storage/...")`)
- `backend/api/estado_cero_ultra_simple.py` (2 referencias)
- `backend/api/sistema_entrelazamiento.py` (4 referencias)
- `backend/api/configuracion.py` (3 referencias)

**Total**: ~12 referencias hardcoded

⚠️ **ACCIÓN REQUERIDA** (Fase 2+):
- Refactorizar paths hardcoded a usar variable de configuración
- Crear `config.STORAGE_PATH = Path("storage")`
- El symlink `backend/storage` mantiene compatibilidad temporal

---

**Autor**: El Entrelazador
**Fase**: Refactorización Vía Recta Maestra - Día 3
**Estado**: ✅ Limpieza completada
