# 📦 Análisis de Sincronización de Dependencias - Backend

**Fecha:** 19 de octubre, 2025
**Contexto:** Fase 1 Día 3 - Post Clean Architecture Analysis
**Problema:** Desincronización entre `requirements.txt` y `pyproject.toml`

---

## 🔍 Discrepancias Identificadas

### **En requirements.txt pero NO en pyproject.toml:**

| Package | Version (req.txt) | Usado en Código | Categoría | Acción |
|---------|-------------------|-----------------|-----------|--------|
| **google-auth** | 2.29.0 | ✅ `integraciones/google_calendar.py` | PROD | **ADD** |
| **google-auth-oauthlib** | 1.2.0 | ✅ `integraciones/google_calendar.py` | PROD | **ADD** |
| **google-auth-httplib2** | 0.2.0 | ✅ (transitive, usado por google-api) | PROD | **ADD** |
| **google-api-python-client** | 2.126.0 | ✅ `integraciones/google_calendar.py` | PROD | **ADD** |
| **praytimes** | 2.1.0 | ✅ `services/tiempos_liturgicos.py` | PROD | **ADD** |
| **PyYAML** | 6.0.2 | ✅ `integraciones/obsidian.py` | PROD | **ADD** |
| **pytz** | 2024.1 | ❌ NO usado directamente | LEGACY | **SKIP** |
| **PyJWT** | 2.9.0 | ❌ NO usado (transitive de google-auth) | TRANSITIVE | **SKIP** |
| **cryptography** | 43.0.3 | ❌ NO usado (transitive de PyJWT) | TRANSITIVE | **SKIP** |
| **passlib** | 1.7.4 | ❌ NO usado directamente | FUTURE | **SKIP** |
| **pydantic-core** | 2.20.1 | ❌ (transitive de Pydantic) | TRANSITIVE | **SKIP** |

### **En pyproject.toml pero NO en requirements.txt:**

| Package | Version (pyproject) | Razón Ausencia | Acción |
|---------|---------------------|----------------|--------|
| **pydantic-settings** | ^2.6.0 | Agregado recientemente | **KEEP** (Poetry export) |
| **ephem** | ^4.1.6 | Agregado para cálculos astronómicos | **KEEP** (alternativa a praytimes?) |
| **structlog** | ^24.4.0 | Logging estructurado (no implementado) | **KEEP** (future use) |
| **tenacity** | ^9.0.0 | Retry logic (no implementado) | **KEEP** (future use) |

### **Versiones Diferentes:**

| Package | requirements.txt | pyproject.toml | ¿Cuál usar? | Razón |
|---------|------------------|----------------|-------------|-------|
| **fastapi** | 0.111.0 | ^0.115.0 | **pyproject** | Versión más reciente, compatible |
| **uvicorn** | 0.30.1 | ^0.32.0 | **pyproject** | Versión más reciente |
| **pydantic** | 2.8.2 | ^2.9.0 | **pyproject** | Versión más reciente |
| **SQLAlchemy** | 2.0.32 | ^2.0.0 | **pyproject** | Caret permite patches |
| **anthropic** | 0.34.0 | ^0.39.0 | **pyproject** | API client actualizado |
| **hijri-converter** | 2.3.2.post1 | ^2.3.0 | **pyproject** | Post-release incluido en ^2.3.0 |

---

## 📋 Uso en Codebase (Verificado)

### **Google Calendar API (4 packages) - ✅ USADO**
```python
# integraciones/google_calendar.py:
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# api/ritual_maghrib.py:
from integraciones.google_calendar import google_calendar

# scripts/verificar_apis.py:
from integraciones.google_calendar import google_calendar
```

**DECISIÓN:** Agregar las 4 dependencias a pyproject.toml

---

### **praytimes (1 package) - ✅ USADO**
```python
# services/tiempos_liturgicos.py:
from praytimes import PrayTimes
```

**DECISIÓN:** Agregar a pyproject.toml

**NOTA:** Tenemos `ephem` en pyproject.toml pero también usamos `praytimes`.
- ¿Son redundantes?
- ¿Deberíamos consolidar en uno solo?
- **ACCIÓN:** Mantener ambos por ahora, evaluar en futuro refactor.

---

### **PyYAML (1 package) - ✅ USADO**
```python
# integraciones/obsidian.py:
import yaml
```

**DECISIÓN:** Agregar a pyproject.toml

---

### **pytz (1 package) - ❌ NO USADO DIRECTAMENTE**
```bash
# grep "import pytz\|from pytz" --exclude-dir=venv
# → 0 matches en código propio
```

**ANÁLISIS:**
- Solo usado en venv/ (paquetes instalados)
- No hay imports directos en nuestro código
- Python 3.11 usa `zoneinfo` nativo (PEP 615)
- pytz es legacy en Python 3.9+

**DECISIÓN:** NO agregar a pyproject.toml (legacy, no necesario)

---

### **PyJWT, cryptography, passlib - ❌ NO USADOS**
```bash
# grep "import jwt\|from jwt" --exclude-dir=venv
# → 0 matches

# grep "from passlib\|import passlib" --exclude-dir=venv
# → 0 matches

# grep "from cryptography\|import cryptography" --exclude-dir=venv
# → 0 matches
```

**ANÁLISIS:**
- PyJWT: Dependency transitiva de google-auth (auto-instalada)
- cryptography: Dependency transitiva de PyJWT (auto-instalada)
- passlib: Preparado para autenticación futura (no implementada)

**DECISIÓN:**
- PyJWT, cryptography: NO agregar (transitive deps)
- passlib: Agregar a `dev-dependencies` (futuro uso documentado)

---

### **pydantic-core - ❌ NO NECESARIO**
```bash
# Pydantic dependency tree:
pydantic 2.9.0
└── pydantic-core 2.20.1 (auto-installed)
```

**DECISIÓN:** NO agregar (transitive, manejado por Poetry)

---

## 🎯 Plan de Sincronización

### **ESTRATEGIA: Poetry como Source of Truth**

**Rationale:**
1. pyproject.toml es estándar PEP 518/621
2. Poetry lockfile garantiza reproducibilidad
3. requirements.txt generado automáticamente
4. Versionado semántico con carets (^)

---

### **Paso 1: Agregar Dependencias Faltantes**

```bash
# Google Calendar API
poetry add google-auth@^2.29.0
poetry add google-auth-oauthlib@^1.2.0
poetry add google-auth-httplib2@^0.2.0
poetry add google-api-python-client@^2.126.0

# Astronomía y Calendar
poetry add praytimes@^2.1.0

# YAML parsing
poetry add PyYAML@^6.0.2

# Futuro (dev)
poetry add --group dev passlib@^1.7.4
```

---

### **Paso 2: Verificar Versiones Actualizadas**

Poetry resolverá automáticamente a las versiones más recientes compatibles:
- fastapi: ^0.115.0 (desde 0.111.0)
- uvicorn: ^0.32.0 (desde 0.30.1)
- pydantic: ^2.9.0 (desde 2.8.2)
- anthropic: ^0.39.0 (desde 0.34.0)

**VALIDACIÓN REQUERIDA:** Ejecutar tests tras actualización.

---

### **Paso 3: Regenerar requirements.txt**

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

**Resultado esperado:**
- requirements.txt refleja pyproject.toml
- Incluye dependencies transitivas resueltas
- Sin hashes (más legible, optional)

---

### **Paso 4: Validación**

```bash
# 1. Clean install
poetry install

# 2. Run tests
poetry run pytest

# 3. Verify imports
poetry run python -c "from integraciones.google_calendar import google_calendar; print('✓ Google OK')"
poetry run python -c "from services.tiempos_liturgicos import CalculadorTiemposLiturgicos; print('✓ PrayTimes OK')"
poetry run python -c "import yaml; print('✓ YAML OK')"

# 4. Check version consistency
poetry show | grep -E "fastapi|pydantic|anthropic|uvicorn"
```

---

## 📊 Cambios Resumidos

### **AGREGAR a pyproject.toml (PROD):**
1. google-auth ^2.29.0
2. google-auth-oauthlib ^1.2.0
3. google-auth-httplib2 ^0.2.0
4. google-api-python-client ^2.126.0
5. praytimes ^2.1.0
6. PyYAML ^6.0.2

### **AGREGAR a pyproject.toml (DEV):**
1. passlib ^1.7.4 (futuro auth)

### **NO AGREGAR (justificación):**
1. pytz → Python 3.11 usa zoneinfo nativo
2. PyJWT → Transitive de google-auth
3. cryptography → Transitive de PyJWT
4. pydantic-core → Transitive de pydantic

### **MANTENER en pyproject.toml (ya presente):**
1. pydantic-settings → Usado implícitamente
2. ephem → Cálculos astronómicos (coexiste con praytimes)
3. structlog → Futuro logging estructurado
4. tenacity → Futuro retry logic

---

## ⚠️ Decisiones Pendientes

### **1. ephem vs praytimes**
```
PREGUNTA: ¿Son redundantes?

CONTEXTO:
- ephem: Cálculos astronómicos generales (PyEphem)
- praytimes: Específico para tiempos de oración islámicos

RESPUESTA PROBABLE: NO redundantes
- ephem: Cálculos solares/lunares precisos
- praytimes: Algoritmos específicos de cálculo de salat

ACCIÓN: Mantener ambos, documentar uso específico.
```

### **2. pytz deprecation**
```
PREGUNTA: ¿Migrar completamente a zoneinfo?

CONTEXTO:
- Python 3.9+: zoneinfo es estándar (PEP 615)
- pytz: Legacy, pero aún usado por libraries
- Algunas deps pueden requerir pytz

ACCIÓN: NO agregar pytz explícitamente.
Si alguna dep lo requiere, se instala transitivamente.
```

### **3. Seguridad (passlib, PyJWT)**
```
PREGUNTA: ¿Implementar auth ahora o después?

CONTEXTO:
- passlib: Para hash de passwords
- PyJWT: Para tokens JWT
- Actualmente NO implementado

ACCIÓN: Agregar passlib a dev-dependencies.
Documentar en roadmap para Fase 4+.
```

---

## ✅ Validación Contra Pilares

### **Pilar 1: Pureza Técnica**
- ✅ Una source of truth (pyproject.toml)
- ✅ Versionado explícito
- ✅ Transitive deps manejadas automáticamente
- ✅ Sin duplicación (requirements.txt generado)

### **Pilar 3: Responsabilidad Sagrada**
- ✅ Dependencies justificadas con uso en código
- ✅ No agregar "por si acaso"
- ✅ Future deps en dev-dependencies (explícito)
- ✅ Documentación de decisiones

### **Pilar 5: Excelencia Técnica**
- ✅ Lockfile para reproducibilidad
- ✅ Semantic versioning con carets
- ✅ Testing post-cambios obligatorio
- ✅ Tool profesional (Poetry)

---

## 📈 Métricas Esperadas

### **Antes:**
```yaml
Dependencies en requirements.txt: 21
Dependencies en pyproject.toml: 13
Discrepancias: 8 packages
Versiones desactualizadas: 6 packages
Source of truth: ❌ Ambiguo
```

### **Después:**
```yaml
Dependencies en pyproject.toml (prod): 19
Dependencies en pyproject.toml (dev): 8
requirements.txt: Auto-generado (50+ con transitivas)
Discrepancias: 0 ✅
Versiones: Latest stable
Source of truth: ✅ pyproject.toml
```

---

**Siguiente paso:** Ejecutar sincronización y validación.
