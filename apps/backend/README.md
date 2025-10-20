# 🕌 Campo Sagrado MVP - Backend

Backend FastAPI de producción para Campo Sagrado MVP, un organismo tecnológico-espiritual que integra **Sufismo** (waḥdat al-wujūd), **Gurdjieff** (Ley de Octava) y **Human Design** (autoridad sacral).

## 📊 Stack Tecnológico

- **Python 3.11+**: Tipado estático, performance moderno
- **FastAPI**: Framework async de alto rendimiento
- **Pydantic v2**: Validación y serialización type-safe
- **Structlog**: Logging estructurado (JSON en producción)
- **Poetry**: Gestión de dependencias profesional
- **Pytest**: Testing comprehensivo con cobertura >75%
- **Ruff + Black + Mypy**: Linting y type checking estricto

## 🏗️ Arquitectura

```
app/
├── core/              # Utilidades core (logger, exceptions, deps)
├── agentes/           # 2 agentes fusionados (Estado Cero, Orquestador)
├── api/               # Endpoints REST (12 endpoints core)
├── services/          # Lógica de negocio
├── integraciones/     # Sistemas externos (Claude AI, Obsidian)
├── models/            # Schemas Pydantic
└── middleware/        # Middleware FastAPI (CORS, timing, errors)

tests/                 # Tests con >75% coverage
```

## 🚀 Setup

### 1. Requisitos

- Python 3.11+
- Poetry 1.5+

### 2. Instalación

```bash
# Instalar Poetry (si no lo tienes)
curl -sSL https://install.python-poetry.org | python3 -

# Clonar repo e ir a backend
cd backend/

# Instalar dependencias
poetry install

# Activar entorno virtual
poetry shell
```

### 3. Configuración

```bash
# Copiar template de variables de entorno
cp .env.example .env

# Editar .env y añadir tu API key de Claude
nano .env
```

**Variables requeridas**:
```env
ANTHROPIC_API_KEY=sk-ant-api03-xxx  # OBLIGATORIO
```

### 4. Ejecutar

```bash
# Desarrollo (hot reload)
poetry run dev

# O manualmente
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visita:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## 🧪 Testing

```bash
# Ejecutar todos los tests
poetry run pytest

# Con cobertura
poetry run pytest --cov=app --cov-report=html

# Solo tests unitarios (rápidos)
poetry run pytest -m unit

# Solo tests de integración
poetry run pytest -m integration

# Ver reporte de cobertura
open htmlcov/index.html
```

**Coverage mínimo**: 75% (configurado en `pytest.ini`)

## 🔍 Code Quality

```bash
# Linting (Ruff)
poetry run ruff check .

# Auto-fix
poetry run ruff check --fix .

# Formatting (Black)
poetry run black .

# Type checking (Mypy)
poetry run mypy app/
```

## 📝 Convenciones de Código

### Estilo

- **Línea máxima**: 100 caracteres
- **Formato**: Black (opinionated, sin discusión)
- **Imports**: Ordenados con isort (integrado en Ruff)
- **Docstrings**: Google style

### Type Hints

```python
# ✅ BIEN - Type hints completos
def calcular_tiempos(fecha: date, lat: float, lon: float) -> dict[str, datetime]:
    ...

# ❌ MAL - Sin type hints
def calcular_tiempos(fecha, lat, lon):
    ...
```

### Exceptions

```python
# ✅ BIEN - Excepciones custom del dominio
from app.core.exceptions import MomentoInvalidoError

raise MomentoInvalidoError(momento="fajr")

# ❌ MAL - Excepciones genéricas
raise ValueError("Momento inválido")
```

### Logging

```python
# ✅ BIEN - Structured logging
from app.core.logger import get_logger

logger = get_logger(__name__)
logger.info("estado_cero_iniciado", momento="fajr", user_id=123)

# ❌ MAL - Print statements
print(f"Estado Cero iniciado: {momento}")
```

## 🌍 Variables de Entorno

Ver `.env.example` para lista completa. Principales:

| Variable | Requerido | Default | Descripción |
|----------|-----------|---------|-------------|
| `ANTHROPIC_API_KEY` | ✅ Sí | - | API key de Claude |
| `APP_ENV` | No | `development` | `development` \| `staging` \| `production` |
| `API_PORT` | No | `8000` | Puerto del servidor |
| `LOG_LEVEL` | No | `INFO` | Nivel de logging |
| `LOG_FORMAT` | No | `json` | Formato: `json` \| `pretty` |
| `DATABASE_URL` | No | SQLite local | URL de conexión DB |
| `LATITUDE` | No | `40.5472` | Latitud para cálculo de rezos |
| `LONGITUDE` | No | `-3.6228` | Longitud para cálculo de rezos |
| `OBSIDIAN_VAULT_PATH` | No | `~/Documents/CampoSagrado` | Path a vault Obsidian |

## 📦 Dependencias Principales

```toml
[tool.poetry.dependencies]
fastapi = "^0.115.0"        # Framework web async
uvicorn = "^0.32.0"         # ASGI server
pydantic = "^2.9.0"         # Validación data
anthropic = "^0.39.0"       # Cliente Claude AI
structlog = "^24.4.0"       # Logging estructurado
tenacity = "^9.0.0"         # Retry logic
ephem = "^4.1.6"            # Cálculos astronómicos
```

## 🛡️ Security

- **No secrets en código**: Todo en `.env`
- **Sensitive data redactada**: Logger censura API keys/tokens
- **CORS configurado**: Solo origins permitidos
- **Rate limiting**: 60 requests/min por IP
- **Input validation**: Pydantic schemas estrictos
- **Error handling**: No stack traces en producción

## 📊 Performance

- **Response time**: <500ms (p95)
- **Claude API**: ~2-4s (Estado Cero completo)
- **Costo Claude/día**: ~$0.01-0.02 (5 Estados Cero)
- **Memoria**: ~150MB con 1 worker
- **Workers recomendados**: 2-4 en producción

## 🚢 Deploy

### Railway/Render

```bash
# Procfile ya configurado
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Copy code
COPY app/ ./app/

# Run
CMD ["poetry", "run", "prod"]
```

## 📖 API Endpoints

### Core (MVP)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/estado-cero/iniciar` | POST | Iniciar Estado Cero |
| `/api/estado-cero/responder` | POST | Responder preguntas sacrales |
| `/api/estado-cero/sintetizar` | POST | Sintetizar dirección emergente |
| `/api/plan-dia/estructura` | GET | Obtener estructura del día |
| `/api/plan-dia/actualizar` | POST | Actualizar plan del día |
| `/api/maghrib/validar` | POST | Validación Maghrib |
| `/api/dimensiones` | GET | 7 Dimensiones del Ser |
| `/api/tiempos/hoy` | GET | Tiempos litúrgicos hoy |

Docs interactivos: http://localhost:8000/docs

## 🎯 Filosofía del Código

> *"La simplicidad es la sofisticación suprema." - Leonardo da Vinci*

Este backend sigue principios del **0.01% de ingenieros**:

1. **Type Safety First**: Mypy en modo estricto, sin `Any`
2. **Fail Fast**: Validación en boundaries, errores explícitos
3. **Structured Logging**: JSON logs, trazabilidad completa
4. **Test Coverage**: >75% como mínimo no negociable
5. **Zero Secrets in Code**: Configuración en entorno
6. **Immutable Config**: Settings cargados 1 vez al inicio
7. **Dependency Injection**: FastAPI Depends para todo
8. **Custom Exceptions**: Errores del dominio, no genéricos
9. **Async by Default**: Operaciones I/O siempre async
10. **Production Ready**: Logging, monitoring, error handling desde día 1

## 🤝 Contribuir

1. Crear branch: `git checkout -b feature/nueva-feature`
2. Escribir tests primero (TDD)
3. Implementar feature
4. Asegurar >75% coverage: `pytest --cov`
5. Pasar quality checks: `ruff check . && black . && mypy app/`
6. Commit: `git commit -m "feat: descripción"`
7. Push y crear PR

## 📄 Licencia

Privado - Campo Sagrado Team © 2025

---

**Desarrollado con** 🕌 **por el equipo de Campo Sagrado**
