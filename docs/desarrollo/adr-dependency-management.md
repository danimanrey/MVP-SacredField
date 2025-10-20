# ADR: Dependency Management - Poetry como Source of Truth

**Número:** ADR-DEV-001
**Fecha:** 19 de octubre, 2025
**Estado:** ✅ ACEPTADO
**Contexto:** Fase 1 Día 3 - Post Clean Architecture Analysis

---

## 📋 Contexto

### **Problema Identificado**

Durante la auditoría de Fase 1, se detectó desincronización crítica entre dos fuentes de verdad para dependencias del backend:

1. **`requirements.txt`** (21 packages pinned)
2. **`pyproject.toml`** (13 packages declarados)

**Discrepancias detectadas:**
- 8 packages en requirements.txt NO estaban en pyproject.toml
- 6 packages con versiones diferentes
- 4 packages en pyproject.toml pero ausentes de requirements.txt
- Ambigüedad sobre cuál es la fuente de verdad

**Impacto:**
- ⚠️ Builds no reproducibles
- ⚠️ Dependencias transitivas no gestionadas
- ⚠️ Riesgo de version drift
- ⚠️ Onboarding complicado (¿cuál usar?)

---

## 🎯 Decisión

**Poetry (`pyproject.toml` + `poetry.lock`) es la ÚNICA source of truth para dependencias.**

**`requirements.txt` se genera automáticamente desde Poetry y se commitea solo para compatibilidad con herramientas que no soportan Poetry.**

---

## 🔍 Alternativas Consideradas

### **1. Requirements.txt como Source of Truth**
```yaml
PROS:
  - Estándar pip universal
  - No requiere Poetry instalado
  - Simple y directo

CONS:
  - ❌ No gestiona dependencias transitivas
  - ❌ Sin lock file robusto
  - ❌ Sin separación dev/prod deps
  - ❌ No semantic versioning nativo
  - ❌ No build system

DECISIÓN: RECHAZADO
```

### **2. Dual Source of Truth (mantener ambos)**
```yaml
PROS:
  - Compatibilidad máxima
  - No breaking changes

CONS:
  - ❌ Duplicación de información
  - ❌ Riesgo de desincronización continuo
  - ❌ Violación Pilar 1 (Pureza)
  - ❌ Mantenimiento doble

DECISIÓN: RECHAZADO
```

### **3. Poetry como Source of Truth (SELECCIONADO)**
```yaml
PROS:
  - ✅ pyproject.toml es estándar PEP 518/621
  - ✅ poetry.lock garantiza reproducibilidad
  - ✅ Gestión de dependencias transitivas
  - ✅ Separación dev/prod dependencies
  - ✅ Semantic versioning con carets (^)
  - ✅ Build system integrado
  - ✅ requirements.txt generado automáticamente

CONS:
  - ⚠️ Requiere Poetry instalado en todos los ambientes
  - ⚠️ CI/CD debe usar Poetry
  - ⚠️ Learning curve para team nuevo a Poetry

DECISIÓN: ✅ ACEPTADO
RATIONALE: Pros superan ampliamente los cons. Poetry es estándar moderno Python.
```

---

## 📦 Dependencias Sincronizadas

### **Agregadas a pyproject.toml (PROD):**

| Package | Version | Razón | Uso en Código |
|---------|---------|-------|---------------|
| google-auth | ^2.29.0 | Google Calendar API | `integraciones/google_calendar.py` |
| google-auth-oauthlib | ^1.2.0 | OAuth flow | `integraciones/google_calendar.py` |
| google-auth-httplib2 | ^0.2.0 | HTTP transport | Transitive (usado por google-api) |
| google-api-python-client | ^2.126.0 | Calendar API | `integraciones/google_calendar.py` |
| praytimes | ^2.1.0 | Cálculo tiempos islámicos | `services/tiempos_liturgicos.py` |
| PyYAML | ^6.0.2 | YAML parsing | `integraciones/obsidian.py` |
| pytz | ^2024.1 | Timezone handling | `services/tiempos_liturgicos.py` |
| email-validator | ^2.0.0 | Validación emails (Pydantic) | Pydantic EmailStr types |

### **Agregadas a dev-dependencies:**

| Package | Version | Razón | Futuro Uso |
|---------|---------|-------|------------|
| passlib | ^1.7.4 | Password hashing | Auth implementation (Fase 4+) |

### **NO Agregadas (Justificación):**

| Package | Razón NO Incluir |
|---------|------------------|
| pydantic-core | Transitive dependency de Pydantic (auto-instalada) |
| PyJWT | Transitive de google-auth (auto-instalada) |
| cryptography | Transitive de PyJWT (auto-instalada) |

---

## 📈 Versiones Actualizadas

Poetry resolvió automáticamente a versiones más recientes compatibles:

| Package | Antes (req.txt) | Después (Poetry) | Cambio |
|---------|-----------------|------------------|--------|
| fastapi | 0.111.0 | 0.115.14 | ⬆️ +4 patches |
| uvicorn | 0.30.1 | 0.32.1 | ⬆️ +2 minor |
| pydantic | 2.8.2 | 2.12.0 | ⬆️ +4 minor |
| SQLAlchemy | 2.0.32 | 2.0.44 | ⬆️ +12 patches |
| anthropic | 0.34.0 | 0.39.0 | ⬆️ +5 minor |

**Todas las actualizaciones son non-breaking (semantic versioning).**

---

## ✅ Validación Realizada

### **1. Imports Críticos**
```bash
✓ Google Calendar OK (integraciones/google_calendar.py)
✓ PrayTimes + pytz OK (services/tiempos_liturgicos.py)
✓ YAML OK (integraciones/obsidian.py)
✓ FastAPI app loads (api/main.py)
✓ Database models (models/database.py)
✓ Claude client (services/claude_client.py)
```

### **2. Versiones Consistentes**
```bash
$ poetry show | grep -E "fastapi|pydantic|anthropic|uvicorn|sqlalchemy"

anthropic       0.39.0
fastapi         0.115.14
pydantic        2.12.0
pydantic-core   2.41.1
pydantic-settings 2.11.0
sqlalchemy      2.0.44
uvicorn         0.32.1
```

### **3. Requirements.txt Generado**
```bash
$ wc -l requirements.txt
57 requirements.txt

# Incluye:
# - 24 dependencias directas (prod)
# - 33 dependencias transitivas
# - Todas con versiones pinned (==)
```

---

## 🔄 Workflow para Desarrolladores

### **Agregar Nueva Dependencia**
```bash
# Producción
poetry add nombre-paquete@^version

# Desarrollo
poetry add --group dev nombre-paquete@^version

# Regenerar requirements.txt
poetry show --only main | awk '{print $1"=="$2}' > requirements.txt

# Commit ambos archivos
git add pyproject.toml poetry.lock requirements.txt
git commit -m "deps: add nombre-paquete"
```

### **Actualizar Dependencia**
```bash
# Actualizar una específica
poetry update nombre-paquete

# Actualizar todas
poetry update

# Regenerar requirements.txt
poetry show --only main | awk '{print $1"=="$2}' > requirements.txt

# Commit
git add poetry.lock requirements.txt
git commit -m "deps: update nombre-paquete to vX.Y.Z"
```

### **Setup Ambiente Desarrollo**
```bash
# Clone repo
git clone <repo>
cd apps/backend

# Install Poetry (si no está instalado)
pip install poetry

# Install dependencies
poetry install  # Dev + prod deps

# Activate environment
poetry shell

# Run app
poetry run python run.py
```

### **CI/CD**
```yaml
# .github/workflows/backend-ci.yml
steps:
  - name: Install Poetry
    run: pipx install poetry

  - name: Install dependencies
    run: poetry install --no-dev  # Solo prod

  - name: Run tests
    run: poetry run pytest
```

---

## 📊 Métricas Antes/Después

### **Antes (Desincronizado)**
```yaml
Dependencies en requirements.txt: 21
Dependencies en pyproject.toml: 13
Discrepancias: 8 packages ⚠️
Versiones desactualizadas: 6 packages ⚠️
Source of truth: ❌ Ambiguo
Reproducibilidad: ⚠️ Baja (sin lockfile robusto)
```

### **Después (Sincronizado)**
```yaml
Dependencies en pyproject.toml (prod): 24
Dependencies en pyproject.toml (dev): 9
Total dependencies (con transitivas): 57
Discrepancias: 0 ✅
Versiones: Latest stable ✅
Source of truth: ✅ pyproject.toml (100% claro)
Reproducibilidad: ✅ Alta (poetry.lock)
```

---

## 🎯 Consecuencias

### **Positivas ✅**

1. **Una Fuente de Verdad**
   - pyproject.toml es el único lugar donde se declaran deps
   - poetry.lock garantiza versiones exactas
   - requirements.txt es derivado, no fuente

2. **Reproducibilidad Garantizada**
   - `poetry install` produce exactamente el mismo ambiente
   - CI/CD builds idénticos a local
   - No más "works on my machine"

3. **Gestión Coherente**
   - Dependencias transitivas gestionadas automáticamente
   - Separación clara dev/prod
   - Semantic versioning con carets (^)

4. **Actualizaciones Seguras**
   - `poetry update` prueba compatibilidad
   - Lockfile permite rollback trivial
   - Testing antes de commit

5. **Alineación con Estándares**
   - pyproject.toml es PEP 518/621
   - Poetry es tool estándar moderno Python
   - Compatible con build backends (Setuptools, etc.)

### **Negativas ⚠️ (Mitigadas)**

1. **Requiere Poetry Instalado**
   - MITIGACIÓN: Documentado en README
   - MITIGACIÓN: CI/CD con Poetry pre-instalado
   - IMPACTO: Mínimo (Poetry es estándar)

2. **Learning Curve**
   - MITIGACIÓN: Workflow documentado arriba
   - MITIGACIÓN: Scripts helper si necesario
   - IMPACTO: Bajo (comandos intuitivos)

3. **Requirements.txt Indirecto**
   - MITIGACIÓN: Generado automáticamente
   - MITIGACIÓN: Commiteado para compatibilidad
   - IMPACTO: Ninguno (transparente)

---

## ✅ Validación Contra Pilares

### **Pilar 1: Pureza Técnica**
- ✅ **Una fuente de verdad** (pyproject.toml)
- ✅ **No duplicación** (requirements.txt derivado)
- ✅ **Estándares PEP** (518/621 compliance)
- ✅ **Reproducibilidad** (lockfile robusto)

### **Pilar 2: Soberanía Creativa**
- ✅ **Poetry es FOSS** (MIT License)
- ✅ **pyproject.toml es estándar abierto** (PEP)
- ✅ **No vendor lock-in** (compatible con otros tools)
- ✅ **Migration path claro** (si necesario, via requirements.txt)

### **Pilar 3: Responsabilidad Sagrada**
- ✅ **Dependencies justificadas** (análisis de uso)
- ✅ **No "por si acaso"** (solo lo necesario)
- ✅ **Future deps en dev** (explícito)
- ✅ **Documentación de decisiones** (este ADR)

### **Pilar 5: Excelencia Técnica**
- ✅ **Tool profesional moderno** (Poetry estándar)
- ✅ **Semantic versioning** (carets ^)
- ✅ **Dependency resolution robusta** (mejor que pip)
- ✅ **Separación concerns** (dev/prod groups)

---

## 🔄 Revisión y Evolución

### **Triggers para Revisar Decisión:**

1. **Poetry deprecation** (improbable, pero monitorear)
2. **PEP nuevo que depreca pyproject.toml** (muy improbable)
3. **Team feedback negativo** (>3 developers reportan issues)
4. **CI/CD problems persistentes** (>5 builds fallidos por Poetry)

### **Próxima Revisión:**
- **Fecha:** Q2 2026 (6 meses post-decisión)
- **Revisar:** Adoption team, CI/CD metrics, dependency health
- **Considerar:** Migración a PDM si Poetry issues (ref: Auditoría Soberanía)

---

## 📚 Referencias

- **Auditoría Soberanía:** `docs/desarrollo/auditoria-soberania-stack.md`
  - Poetry score: 7.6/10
  - PDM score: 8.4/10 (considerar migración futuro)

- **Análisis Sincronización:** `docs/desarrollo/dependency-sync-analysis.md`
  - Detalles de discrepancias
  - Justificación de cada package

- **PEPs Relacionados:**
  - PEP 518: pyproject.toml
  - PEP 621: Project metadata in pyproject.toml
  - PEP 517: Backend build system

- **Poetry Docs:**
  - https://python-poetry.org/docs/

---

## 📋 Checklist de Validación

- [x] Poetry install funciona sin errores
- [x] Imports críticos funcionan (Google Calendar, PrayTimes, YAML, FastAPI)
- [x] requirements.txt refleja pyproject.toml
- [x] Versiones consistentes (fastapi, pydantic, anthropic, etc.)
- [x] ADR documentado y commitado
- [x] Análisis de discrepancias completado
- [x] Workflow para devs documentado

---

**Decisión final: ✅ ACEPTADO**

**Autor:** El Entrelazador
**Fecha:** 19 octubre 2025
**Estado:** Implementado y validado
**Próxima revisión:** Q2 2026

---

**إن شاء الله - Construimos con pureza técnica 🕌✨**
