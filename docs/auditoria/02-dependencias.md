# AUDITORÍA 2: Análisis de Dependencias

**Fecha**: 18 de Octubre de 2025
**Proyecto**: Campo Sagrado MVP

---

## 📦 FRONTEND (Next.js)

### Dependencies (Producción)

| Paquete | Versión | Usado | Propósito | Acción Recomendada |
|---------|---------|-------|-----------|-------------------|
| **react** | ^18.3.1 | ✅ | Core framework | ✅ Mantener |
| **react-dom** | ^18.3.1 | ✅ | DOM renderer | ✅ Mantener |
| **next** | ^14.2.0 | ✅ | Framework Next.js | ✅ Mantener |
| **three** | ^0.168.0 | ✅ | WebGL / 3D background | ✅ Mantener (usado en geometría sagrada) |
| **@react-three/fiber** | ^8.17.0 | ✅ | React renderer para Three.js | ✅ Mantener |
| **@react-three/drei** | ^9.112.0 | ⚠️ | Helpers Three.js | ⚠️ VERIFICAR - No veo uso explícito |
| **framer-motion** | ^11.5.0 | ✅ | Animaciones UI | ✅ Mantener (usado intensivamente) |
| **zustand** | ^4.5.0 | ⚠️ | State management | ⚠️ NO USADO - Eliminar |
| **lucide-react** | ^0.441.0 | ⚠️ | Iconos | ⚠️ VERIFICAR - Pocos iconos usados |

### DevDependencies (Desarrollo)

| Paquete | Versión | Usado | Propósito | Acción Recomendada |
|---------|---------|-------|-----------|-------------------|
| **typescript** | ^5.5.0 | ✅ | Type checking | ✅ Mantener |
| **@types/node** | ^22.5.0 | ✅ | Types Node.js | ✅ Mantener |
| **@types/react** | ^18.3.0 | ✅ | Types React | ✅ Mantener |
| **@types/react-dom** | ^18.3.0 | ✅ | Types React DOM | ✅ Mantener |
| **@types/three** | ^0.168.0 | ✅ | Types Three.js | ✅ Mantener |
| **tailwindcss** | ^3.4.0 | ✅ | CSS utility framework | ✅ Mantener |
| **postcss** | ^8.4.0 | ✅ | CSS processor | ✅ Mantener |
| **autoprefixer** | ^10.4.0 | ✅ | CSS vendor prefixes | ✅ Mantener |

### ⚠️ Faltantes Recomendados

| Paquete | Propósito | Prioridad |
|---------|-----------|-----------|
| **eslint** | Linting | ALTA |
| **@typescript-eslint/parser** | TS Linting | ALTA |
| **@typescript-eslint/eslint-plugin** | TS Linting | ALTA |
| **prettier** | Code formatting | MEDIA |
| **@testing-library/react** | Testing | ALTA |
| **@testing-library/jest-dom** | Testing matchers | ALTA |
| **vitest** o **jest** | Test runner | ALTA |

---

## 🐍 BACKEND (Python)

### pyproject.toml (Poetry - Recomendado)

| Paquete | Versión | Usado | Propósito | Acción Recomendada |
|---------|---------|-------|-----------|-------------------|
| **fastapi** | ^0.115.0 | ✅ | API framework | ✅ Mantener |
| **uvicorn** | ^0.32.0 | ✅ | ASGI server | ✅ Mantener |
| **pydantic** | ^2.9.0 | ✅ | Data validation | ✅ Mantener |
| **pydantic-settings** | ^2.6.0 | ✅ | Settings management | ✅ Mantener |
| **anthropic** | ^0.39.0 | ✅ | Claude API | ✅ Mantener (actualizada) |
| **python-dotenv** | ^1.0.0 | ✅ | Env variables | ✅ Mantener |
| **ephem** | ^4.1.6 | ✅ | Cálculos astronómicos | ✅ Mantener |
| **python-multipart** | ^0.0.12 | ✅ | File uploads | ✅ Mantener |
| **httpx** | ^0.27.0 | ✅ | Async HTTP client | ✅ Mantener |
| **structlog** | ^24.4.0 | ✅ | Structured logging | ✅ Mantener |
| **tenacity** | ^9.0.0 | ✅ | Retry logic | ✅ Mantener |
| **sqlalchemy** | ^2.0.0 | ✅ | ORM | ✅ Mantener |
| **hijri-converter** | ^2.3.0 | ✅ | Calendario islámico | ✅ Mantener |

### requirements.txt (Pip - Actual)

| Paquete | Versión | Estado | Problema |
|---------|---------|--------|----------|
| fastapi | 0.111.0 | ⚠️ | DESACTUALIZADA (Poetry tiene 0.115.0) |
| uvicorn | 0.30.1 | ⚠️ | DESACTUALIZADA (Poetry tiene 0.32.0) |
| anthropic | 0.34.0 | ⚠️ | DESACTUALIZADA (Poetry tiene 0.39.0) |
| google-auth | 2.29.0 | ⚠️ | NO EN POETRY |
| google-auth-oauthlib | 1.2.0 | ⚠️ | NO EN POETRY |
| google-api-python-client | 2.126.0 | ⚠️ | NO EN POETRY |
| praytimes | 2.1.0 | ⚠️ | NO EN POETRY (usa ephem) |
| PyJWT | 2.9.0 | ⚠️ | NO EN POETRY |
| cryptography | 43.0.3 | ⚠️ | NO EN POETRY |
| passlib | 1.7.4 | ⚠️ | NO EN POETRY |
| PyYAML | 6.0.2 | ⚠️ | NO EN POETRY |

### Dev Dependencies (Poetry)

| Paquete | Versión | Usado | Propósito | Acción Recomendada |
|---------|---------|-------|-----------|-------------------|
| **pytest** | ^8.3.0 | ✅ | Testing framework | ✅ Mantener |
| **pytest-asyncio** | ^0.24.0 | ✅ | Async testing | ✅ Mantener |
| **pytest-cov** | ^6.0.0 | ✅ | Coverage | ✅ Mantener |
| **pytest-mock** | ^3.14.0 | ✅ | Mocking | ✅ Mantener |
| **black** | ^24.10.0 | ✅ | Code formatter | ✅ Mantener |
| **ruff** | ^0.7.0 | ✅ | Linter | ✅ Mantener |
| **mypy** | ^1.13.0 | ✅ | Type checking | ✅ Mantener |
| **pre-commit** | ^4.0.0 | ✅ | Git hooks | ✅ Mantener |

---

## 🚨 PROBLEMAS CRÍTICOS

### 1. ⚠️ DEPENDENCIAS DESINCRONIZADAS

**Problema**: `requirements.txt` está desactualizado respecto a `pyproject.toml`

**Impacto**:
- Sistema puede usar versiones diferentes en dev vs prod
- Dependencias faltantes en Poetry
- Dependencias adicionales en requirements.txt no documentadas

**Solución**:
```bash
# Opción A: Generar requirements.txt desde Poetry (RECOMENDADO)
cd backend/
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Opción B: Sincronizar Poetry con requirements.txt
# Añadir a pyproject.toml:
[tool.poetry.dependencies]
google-auth = "^2.29.0"
google-auth-oauthlib = "^1.2.0"
google-api-python-client = "^2.126.0"
PyJWT = "^2.9.0"
cryptography = "^43.0.0"
passlib = "^1.7.4"
PyYAML = "^6.0.0"
praytimes = "^2.1.0"  # Si se usa, o eliminar si ephem es suficiente

# Ejecutar:
poetry lock
poetry install
```

### 2. ⚠️ ZUSTAND NO USADO (Frontend)

**Problema**: `zustand` instalado pero NO usado

**Evidencia**:
```bash
# Buscar uso de zustand:
$ grep -r "zustand" campo-sagrado-nextjs/app/
# Sin resultados
```

**Solución**:
```bash
cd campo-sagrado-nextjs/
npm uninstall zustand
```

**Ahorro**: ~30KB bundle size

### 3. ⚠️ LUCIDE-REACT INFRAUTILIZADO

**Problema**: Librería de iconos grande (441KB) para pocos iconos

**Alternativa**:
```typescript
// En lugar de:
import { Icon1, Icon2 } from 'lucide-react';

// Considerar:
// 1. Solo importar SVGs necesarios
// 2. Usar @heroicons/react (más ligero)
// 3. O eliminar si solo usas emojis
```

**Análisis requerido**: Contar cuántos iconos se usan realmente

### 4. ⚠️ @REACT-THREE/DREI SIN USO CLARO

**Problema**: Librería helpers Three.js instalada, uso no confirmado

**Acción**: Auditar uso en código:
```bash
grep -r "@react-three/drei" campo-sagrado-nextjs/app/
```

Si no se usa → Eliminar

---

## ✅ DEPENDENCIAS BIEN GESTIONADAS

### Backend
- ✅ Poetry configurado correctamente
- ✅ Herramientas de calidad (black, ruff, mypy, pytest)
- ✅ Pre-commit hooks
- ✅ Coverage target 75%
- ✅ Tipos estrictos (mypy strict mode)

### Frontend
- ✅ TypeScript configurado
- ✅ Tailwind + PostCSS
- ✅ Versiones React recientes
- ✅ Next.js 14 (App Router)

---

## 📊 MÉTRICAS

### Frontend
| Métrica | Valor |
|---------|-------|
| Total dependencies | 9 |
| Total devDependencies | 8 |
| Potencialmente no usadas | 2-3 |
| Faltantes críticas (ESLint, tests) | 6 |
| Tamaño estimado node_modules | ~350MB |

### Backend
| Métrica | Valor |
|---------|-------|
| Total dependencies (Poetry) | 13 |
| Total dependencies (requirements.txt) | 18 |
| Dev dependencies | 8 |
| Desincronizadas | 5 |
| Faltantes en Poetry | 7 |

---

## 🎯 PLAN DE ACCIÓN

### Prioridad ALTA (HOY)

1. **Sincronizar Poetry y requirements.txt**
   ```bash
   # Añadir dependencias faltantes a pyproject.toml
   # O regenerar requirements.txt desde Poetry
   ```

2. **Eliminar Zustand del frontend**
   ```bash
   cd campo-sagrado-nextjs/
   npm uninstall zustand
   ```

3. **Añadir ESLint al frontend**
   ```bash
   npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
   npx eslint --init
   ```

### Prioridad MEDIA (DÍA 7)

4. **Auditar uso de @react-three/drei y lucide-react**
   - Confirmar uso real
   - Eliminar si no se necesitan

5. **Añadir testing al frontend**
   ```bash
   npm install -D vitest @testing-library/react @testing-library/jest-dom
   ```

6. **Actualizar versiones desactualizadas**
   ```bash
   # Backend
   poetry update

   # Frontend
   npm update
   ```

### Prioridad BAJA (DÍA 8)

7. **Añadir Prettier al frontend**
8. **Configurar Husky para pre-commit hooks**
9. **Analizar bundle size del frontend**
   ```bash
   npm install -D @next/bundle-analyzer
   ```

---

## 📝 CONCLUSIONES

### ✅ Fortalezas
1. Backend con Poetry bien configurado
2. Herramientas de calidad (black, ruff, mypy)
3. Testing framework en backend
4. Versiones modernas de frameworks

### ⚠️ Debilidades
1. **requirements.txt desincronizado** con Poetry
2. **Dependencias no usadas** (zustand, posiblemente drei)
3. **Falta testing** en frontend
4. **Falta linting** (ESLint) en frontend
5. **Dependencias faltantes** en Poetry (Google APIs)

### 🎯 Impacto
- **Seguridad**: BAJO (versiones relativamente actuales)
- **Mantenibilidad**: MEDIO (desincronización Poetry/pip)
- **Performance**: BAJO (dependencias no usadas pesan poco)
- **Desarrollo**: MEDIO (falta tooling frontend)

---

**Generado**: Auditoría 2 - Análisis de Dependencias
**Estado**: ⚠️ Sincronización urgente Poetry/requirements.txt
**Próximo**: Auditoría 3 - Calidad de Código
