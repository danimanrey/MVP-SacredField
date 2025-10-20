# 🚨 PROBLEMAS CRÍTICOS DEL PROYECTO

**Fecha**: 18 de Octubre de 2025
**Proyecto**: Campo Sagrado MVP
**Versión**: 2.0.0
**Total Problemas Identificados**: 24

---

## 📋 ÍNDICE

- [CATEGORÍA A: BLOQUEA DESARROLLO](#categoría-a-bloquea-desarrollo) (7 problemas)
- [CATEGORÍA B: DEUDA TÉCNICA ALTA](#categoría-b-deuda-técnica-alta) (10 problemas)
- [CATEGORÍA C: MEJORAS](#categoría-c-mejoras) (7 problemas)

---

## CATEGORÍA A: BLOQUEA DESARROLLO

**Resolver primero** - Estos problemas impiden desarrollo seguro y escalable

### A1. Sin Testing en Frontend

**Descripción**: Frontend Next.js sin tests, 0% cobertura, imposible refactorizar con confianza

**Impacto**: 🔴 **10/10** - CRÍTICO
- Imposible detectar regresiones
- Refactoring peligroso
- Bugs en producción
- No se puede escalar equipo

**Esfuerzo**: ⏱️ **40 horas**
- Setup inicial: 2h
- Tests componentes: 20h
- Tests hooks: 8h
- Tests utils: 5h
- E2E básicos: 5h

**Archivos Afectados**:
```
campo-sagrado-nextjs/
├── app/components/PuertaDeEntrada7Capas.tsx  # Sin tests
├── app/estado-cero-inmersivo/page.tsx        # Sin tests
├── lib/api/                                  # Sin tests
└── package.json                              # Falta vitest, testing-library
```

**Solución Propuesta**:

```bash
# 1. Instalar dependencias
cd campo-sagrado-nextjs/
npm install -D vitest @vitejs/plugin-react
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
npm install -D jsdom happy-dom

# 2. Crear vitest.config.ts
cat > vitest.config.ts << 'EOF'
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      exclude: ['node_modules/', 'tests/']
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './app')
    }
  }
})
EOF

# 3. Crear setup.ts
mkdir -p tests/
cat > tests/setup.ts << 'EOF'
import '@testing-library/jest-dom'
EOF

# 4. Actualizar package.json scripts
npm pkg set scripts.test="vitest"
npm pkg set scripts.test:ui="vitest --ui"
npm pkg set scripts.coverage="vitest --coverage"

# 5. Escribir primer test
mkdir -p app/components/__tests__/
cat > app/components/__tests__/PuertaDeEntrada7Capas.test.tsx << 'EOF'
import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import PuertaDeEntrada7Capas from '../PuertaDeEntrada7Capas'

describe('PuertaDeEntrada7Capas', () => {
  it('renders first step (energía)', () => {
    const mockOnComplete = vi.fn()
    render(<PuertaDeEntrada7Capas onComplete={mockOnComplete} momento="dhuhr" />)

    expect(screen.getByText(/Energía Física/i)).toBeInTheDocument()
  })
})
EOF

# 6. Ejecutar tests
npm test
```

**Validación**:
```bash
npm test -- --coverage
# Target: >50% coverage en 2 semanas
```

---

### A2. Dependencias Backend Desincronizadas

**Descripción**: `requirements.txt` y `pyproject.toml` tienen versiones diferentes, falta Google Calendar en Poetry

**Impacto**: 🔴 **9/10** - CRÍTICO
- Errores en producción
- Dependencias faltantes en Poetry
- Versiones inconsistentes dev/prod
- Google Calendar puede fallar

**Esfuerzo**: ⏱️ **1 hora**

**Archivos Afectados**:
```
backend/
├── pyproject.toml              # Falta google-auth, PyJWT, etc.
├── requirements.txt            # Versiones desactualizadas
└── poetry.lock                 # Desactualizado
```

**Diferencias Detectadas**:
| Paquete | requirements.txt | pyproject.toml | Estado |
|---------|------------------|----------------|--------|
| fastapi | 0.111.0 | ^0.115.0 | ⚠️ Desactualizado |
| anthropic | 0.34.0 | ^0.39.0 | ⚠️ Desactualizado |
| google-auth | 2.29.0 | FALTA | ❌ No en Poetry |
| google-api-python-client | 2.126.0 | FALTA | ❌ No en Poetry |
| PyJWT | 2.9.0 | FALTA | ❌ No en Poetry |
| cryptography | 43.0.3 | FALTA | ❌ No en Poetry |

**Solución Propuesta**:

```bash
cd backend/

# OPCIÓN A: Añadir dependencias faltantes a Poetry (RECOMENDADO)
poetry add google-auth@^2.29.0
poetry add google-auth-oauthlib@^1.2.0
poetry add google-api-python-client@^2.126.0
poetry add PyJWT@^2.9.0
poetry add cryptography@^43.0.0
poetry add passlib@^1.7.4
poetry add PyYAML@^6.0.0
poetry add email-validator@^2.0.0

# Actualizar lockfile
poetry lock

# Regenerar requirements.txt desde Poetry
poetry export -f requirements.txt --output requirements.txt --without-hashes

# OPCIÓN B: Si praytimes es necesario
poetry add praytimes@^2.1.0
# O usar solo ephem si es suficiente

# Verificar sincronización
poetry install
poetry show

# Validar
python -c "import google.auth; import jwt; import passlib; print('✅ Todas las dependencias OK')"
```

**Validación**:
```bash
# Comparar
diff <(poetry export -f requirements.txt --without-hashes | sort) <(sort requirements.txt)
# Debería estar vacío o mínimo
```

---

### A3. Sin Linting (ESLint) en Frontend

**Descripción**: Frontend TypeScript sin ESLint, código inconsistente, bugs potenciales no detectados

**Impacto**: 🔴 **8/10** - ALTO
- Código inconsistente
- Bugs de tipos no detectados
- Malas prácticas no identificadas
- Dificulta code review

**Esfuerzo**: ⏱️ **2 horas**

**Archivos Afectados**:
```
campo-sagrado-nextjs/
├── (todos los .ts, .tsx)       # Sin linting
├── .eslintrc.json              # No existe
└── package.json                # Falta ESLint
```

**Solución Propuesta**:

```bash
cd campo-sagrado-nextjs/

# 1. Instalar ESLint + plugins
npm install -D eslint
npm install -D @typescript-eslint/parser @typescript-eslint/eslint-plugin
npm install -D eslint-plugin-react eslint-plugin-react-hooks
npm install -D eslint-config-next
npm install -D prettier eslint-config-prettier eslint-plugin-prettier

# 2. Crear .eslintrc.json
cat > .eslintrc.json << 'EOF'
{
  "extends": [
    "next/core-web-vitals",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": 2022,
    "sourceType": "module",
    "ecmaFeatures": {
      "jsx": true
    }
  },
  "rules": {
    "react/react-in-jsx-scope": "off",
    "react/prop-types": "off",
    "@typescript-eslint/no-unused-vars": ["warn", { "argsIgnorePattern": "^_" }],
    "@typescript-eslint/no-explicit-any": "warn",
    "prefer-const": "error",
    "no-console": ["warn", { "allow": ["warn", "error"] }]
  },
  "settings": {
    "react": {
      "version": "detect"
    }
  }
}
EOF

# 3. Crear .prettierrc
cat > .prettierrc << 'EOF'
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false
}
EOF

# 4. Crear .eslintignore
cat > .eslintignore << 'EOF'
node_modules/
.next/
out/
build/
coverage/
*.config.js
*.config.ts
EOF

# 5. Actualizar scripts package.json
npm pkg set scripts.lint="next lint"
npm pkg set scripts.lint:fix="next lint --fix"
npm pkg set scripts.format="prettier --write \"**/*.{ts,tsx,js,jsx,json,md}\""
npm pkg set scripts.format:check="prettier --check \"**/*.{ts,tsx,js,jsx,json,md}\""

# 6. Ejecutar linting
npm run lint

# 7. Autofix lo posible
npm run lint:fix
npm run format
```

**Validación**:
```bash
npm run lint -- --max-warnings 0
# Debería pasar sin errores críticos
```

---

### A4. Root Directory Sobrecargado (60+ archivos MD)

**Descripción**: Raíz del proyecto con 60+ archivos Markdown, navegación confusa, difícil mantenimiento

**Impacto**: 🔴 **8/10** - ALTO
- Dificulta onboarding nuevos devs
- Pérdida de tiempo buscando archivos
- Repo poco profesional
- Git log contaminado

**Esfuerzo**: ⏱️ **2 horas**

**Archivos Afectados**:
```
/ (root)
├── ANALISIS_*.md (12 archivos)
├── ARQUITECTURA_*.md (8 archivos)
├── ESTADO_*.md (15 archivos)
├── RESUMEN_*.md (20 archivos)
├── FIX_*.md (5 archivos)
└── ... (otros 20+)
```

**Solución Propuesta**:

```bash
# 1. Crear estructura organizada
mkdir -p docs/{analisis,arquitectura,estados,guias,testing,fixes}
mkdir -p archive/{resumenes,migraciones,implementaciones}

# 2. Mover archivos por categoría
# ANÁLISIS
mv ANALISIS_*.md docs/analisis/
mv AUDITORIA_*.md docs/analisis/

# ARQUITECTURA
mv ARQUITECTURA_*.md docs/arquitectura/
mv PILARES_*.md docs/arquitectura/
mv MAPA_*.md docs/arquitectura/

# ESTADOS
mv ESTADO_*.md docs/estados/
mv SISTEMA_*.md docs/estados/

# GUÍAS
mv GUIA_*.md docs/guias/
mv INICIO_*.md docs/guias/
mv SETUP_*.md docs/guias/

# TESTING
mv TESTING_*.md docs/testing/
mv CHECKLIST_*.md docs/testing/
mv VALIDACION_*.md docs/testing/

# ARCHIVAR FIXES
mv FIX_*.md archive/fixes/
mv ERRORES_*.md archive/fixes/

# ARCHIVAR RESÚMENES
mv RESUMEN_*.md archive/resumenes/
mv SESION_*.md archive/resumenes/
mv PROGRESO_*.md archive/resumenes/

# ARCHIVAR MIGRACIONES
mv MIGRACION_*.md archive/migraciones/
mv PLAN_*.md archive/migraciones/

# MANTENER EN ROOT
# - README.md
# - README_V2.md (renombrar a README_LEGACY.md)
# - CHANGELOG.md
# - INTEGRACION_TOTAL_COMPLETADA.md (mover a docs/estados/)
# - .gitignore
# - .cursorrules

# 3. Renombrar y limpiar
mv README_V1.md archive/README_V1.md
mv README_V2.md README_LEGACY.md
mv INTEGRACION_TOTAL_COMPLETADA.md docs/estados/

# 4. Mover configs personales
mkdir -p .dotfiles/
mv .aliases .dotfiles/
mv .zshrc .dotfiles/
mv .iterm2_campo_sagrado.sh .dotfiles/

# 5. Añadir a .gitignore
echo ".dotfiles/" >> .gitignore

# 6. Crear índice maestro
cat > docs/INDEX.md << 'EOF'
# 📚 Índice Maestro de Documentación

## 🏗 Arquitectura
- [Arquitectura Organismo](./arquitectura/ARQUITECTURA_ORGANISMO_COMPLETA.md)
- [Sistema 7 Capas](./estados/SISTEMA_7_CAPAS_FUNCIONANDO.md)
- [Pilares Arquitectónicos](./arquitectura/PILARES_ARQUITECTONICOS.md)

## 📊 Estados del Sistema
- [Integración Total Completada](./estados/INTEGRACION_TOTAL_COMPLETADA.md)
- [Estado Actual](./estados/ESTADO_ACTUAL_SISTEMA.md)

## 📖 Guías
- [Inicio Rápido](./guias/INICIO_RAPIDO_SISTEMA_COMPLETO.md)
- [Guía Usuario](./guias/GUIA_USUARIO_COMPLETA.md)

## 🧪 Testing
- [Testing Completo](./testing/TESTING_FLUJO_COMPLETO.md)

## 🔍 Análisis
- [Auditoría Completa](./auditoria/00-resumen-ejecutivo.md)

## 📁 Archivo Histórico
Ver carpeta `/archive` para:
- Resúmenes de sesiones
- Fixes históricos
- Migraciones anteriores
EOF
```

**Validación**:
```bash
# Root debería tener máximo 10 archivos
ls -1 | wc -l
# Esperado: < 10

# Verificar organización
tree docs/ -L 2
tree archive/ -L 2
```

---

### A5. Frontends Duplicados (3 versiones)

**Descripción**: Tres carpetas de frontend (SvelteKit legacy, Next.js alt, Next.js actual), confusión y ~500MB desperdiciados

**Impacto**: 🔴 **7/10** - ALTO
- Confusión sobre cuál usar
- Espacio desperdiciado (~500MB)
- Riesgo de editar versión incorrecta
- Complejidad innecesaria

**Esfuerzo**: ⏱️ **0.5 horas**

**Archivos Afectados**:
```
/
├── frontend/               # LEGACY SvelteKit (eliminar)
├── frontend-next/          # LEGACY Next.js alt (eliminar)
└── campo-sagrado-nextjs/   # ACTUAL (renombrar a frontend/)
```

**Solución Propuesta**:

```bash
# 1. Backup preventivo (opcional pero recomendado)
tar -czf backup-frontends-$(date +%Y%m%d).tar.gz frontend/ frontend-next/
mv backup-frontends-*.tar.gz archive/

# 2. Eliminar frontends legacy
rm -rf frontend/
rm -rf frontend-next/

# 3. Renombrar actual a nombre estándar
mv campo-sagrado-nextjs/ frontend/

# 4. Actualizar referencias en docs y scripts
# Buscar referencias al nombre antiguo
grep -r "campo-sagrado-nextjs" . --exclude-dir=node_modules --exclude-dir=.git

# Actualizar scripts de inicio
sed -i '' 's/campo-sagrado-nextjs/frontend/g' scripts/*.sh

# 5. Actualizar README si menciona
sed -i '' 's/campo-sagrado-nextjs/frontend/g' README.md

# 6. Verificar package.json tiene nombre correcto
cd frontend/
npm pkg set name="campo-sagrado-frontend"
```

**Validación**:
```bash
# Verificar solo existe frontend/
ls -d */ | grep -E "frontend"
# Debería retornar solo: frontend/

# Verificar funciona
cd frontend/
npm install
npm run dev
# Debe iniciar en localhost:3000
```

---

### A6. Storage Duplicado

**Descripción**: Base de datos SQLite duplicada en `storage/` root y `backend/storage/`, riesgo de usar DB incorrecta

**Impacto**: 🔴 **7/10** - ALTO
- Datos inconsistentes
- Confusión sobre cuál DB es la correcta
- Riesgo de pérdida de datos
- Espacio desperdiciado

**Esfuerzo**: ⏱️ **0.5 horas**

**Archivos Afectados**:
```
/
├── storage/
│   ├── organismo.db        # ⚠️ DUPLICADO
│   └── datos_prueba.json   # ⚠️ Datos de prueba
└── backend/
    └── storage/
        ├── organismo.db    # ✅ CORRECTO
        ├── estados_cero/
        └── events/
```

**Solución Propuesta**:

```bash
# 1. Verificar cuál DB se usa actualmente
grep -r "organismo.db" backend/ --include="*.py"
# Debería apuntar a backend/storage/organismo.db

# 2. Verificar si DB root tiene datos únicos
sqlite3 storage/organismo.db ".tables"
sqlite3 backend/storage/organismo.db ".tables"

# Si son idénticas o root está vacía:
# 3. Eliminar storage/ root
rm -rf storage/

# Si root tiene datos únicos:
# 3. Mergear datos (cuidado, revisar schemas)
# Contactar con DBA o hacer dump/restore manual

# 4. Actualizar .gitignore si aplica
echo "# Storage solo en backend" >> .gitignore

# 5. Crear symlink si scripts legacy lo necesitan (temporal)
ln -s backend/storage storage
# Y documentar para eliminar después
```

**Validación**:
```bash
# Verificar solo existe backend/storage/
find . -name "organismo.db" -not -path "*/node_modules/*" -not -path "*/.next/*"
# Debería retornar solo: ./backend/storage/organismo.db

# Verificar app funciona
cd backend/
python -c "from models.database import engine; print('✅ DB OK')"
```

---

### A7. Nested Directories Incorrectos

**Descripción**: `backend/backend/.env`, `backend/~/Documents/`, `backend/app/` estructura duplicada

**Impacto**: 🔴 **6/10** - MEDIO-ALTO
- Confusión en estructura
- Home directory en repo (potencial leak de datos)
- Estructura app duplicada sin uso
- Violación convenciones

**Esfuerzo**: ⏱️ **1 hora**

**Archivos Afectados**:
```
backend/
├── backend/
│   └── .env               # ⚠️ Nested incorrectamente
├── ~/
│   └── Documents/         # ⚠️ HOME directory anidado
├── app/                   # ⚠️ Estructura alternativa duplicada
│   ├── agentes/
│   ├── api/
│   ├── services/
│   └── ...
├── agentes/               # ✅ Correcta
├── api/                   # ✅ Correcta
└── services/              # ✅ Correcta
```

**Solución Propuesta**:

```bash
cd backend/

# 1. Investigar backend/backend/
# Verificar si .env es diferente al principal
diff backend/.env .env
# Si son iguales:
rm -rf backend/

# Si .env tiene configs únicas, mergear:
cat backend/.env >> .env
rm -rf backend/

# 2. Eliminar home directory anidado (PELIGRO - verificar primero)
# Listar contenido
ls -la ~/Documents/
# Si está vacío o son archivos sistema:
rm -rf ~/

# 3. Verificar si app/ se usa
grep -r "from app\." . --include="*.py" | grep -v "app.main"
# Si no hay resultados (excepto app.main que es correcto):
# Verificar pyproject.toml packages
cat pyproject.toml | grep packages
# Si dice packages = [{include = "app"}]
# Es la estructura CORRECTA, pero está mal ubicada

# La estructura app/ en backend/ es CORRECTA según pyproject.toml
# NO eliminar si es la estructura usada

# Verificar cuál se está usando realmente:
cd backend/
python -c "import sys; print(sys.path)"
python -c "from api.main import app; print('✅ Importa de api/ directamente')"
# vs
python -c "from app.api.main import app; print('✅ Importa de app/')"

# Si usa app/:
# Consolidar: mover todo de raíz a app/
mv agentes/ api/ models/ services/ app/
# Actualizar imports

# Si usa raíz directamente:
# Eliminar app/ duplicada
rm -rf app/
# Actualizar pyproject.toml:
# packages = [{include = "."}]  # o eliminar la línea
```

**Investigación Necesaria**:
```bash
# Determinar estructura activa
cd backend/
python3 -c "
import importlib.util
import sys

# Intentar importar de ambas formas
try:
    from api.main import app
    print('✅ Usa estructura plana (agentes/, api/, etc. en raíz)')
except:
    print('❌ No puede importar de api/')

try:
    from app.api.main import app
    print('✅ Usa estructura app/ (agentes/, api/ dentro de app/)')
except:
    print('❌ No puede importar de app.api')
"
```

**Validación**:
```bash
# Después de limpieza, verificar estructura
tree -L 2 backend/
# No debería haber:
# - backend/backend/
# - backend/~/
# - Duplicación app/ vs raíz
```

---

## CATEGORÍA B: DEUDA TÉCNICA ALTA

**Resolver pronto** - Impacta calidad y mantenibilidad

### B1. Tests Backend Incompletos (Cobertura Desconocida)

**Descripción**: Backend tiene pytest configurado pero cobertura actual desconocida, posiblemente <75% target

**Impacto**: 🟡 **8/10** - ALTO
- Riesgo en refactoring backend
- Bugs potenciales no detectados
- Confianza baja en cambios

**Esfuerzo**: ⏱️ **30 horas**

**Archivos Afectados**:
```
backend/
├── tests/                  # Estructura existe pero ¿completa?
├── pytest.ini              # Target 75% coverage
└── pyproject.toml          # Coverage configurado
```

**Solución Propuesta**:

```bash
cd backend/

# 1. Ejecutar coverage actual
poetry run pytest --cov=. --cov-report=html --cov-report=term-missing

# 2. Ver reporte
open htmlcov/index.html

# 3. Identificar archivos sin tests
# Ejemplo esperado:
# agentes/estado_cero.py         45%  ⚠️
# services/orquestador_7_capas.py 60%  ⚠️
# api/estado_cero.py             80%  ✅

# 4. Escribir tests faltantes
# Priorizar por criticidad:
# - estado_cero.py (más crítico)
# - orquestador_7_capas.py
# - generador_preguntas_7_capas.py

# 5. Ejemplo test estado_cero.py
cat > tests/agentes/test_estado_cero.py << 'EOF'
import pytest
from agentes.estado_cero import AgenteEstadoCero
from models.schemas import MomentoLiturgico

@pytest.mark.asyncio
async def test_formular_preguntas_sacrales(mock_db, mock_claude, mock_recopilador):
    agente = AgenteEstadoCero(mock_db, mock_claude, mock_recopilador)

    # Mock contexto
    from models.schemas import ContextoCompleto, ContextoTemporal, ContextoBiologico
    contexto = ContextoCompleto(
        temporal=ContextoTemporal(
            momento_liturgico=MomentoLiturgico.DHUHR,
            dia_semana="Saturday",
            mes_hijri="",
            cualidad_momento="",
            cualidad_mes=""
        ),
        biologico=ContextoBiologico(
            energia_actual=4,
            hrv=None,
            luz_solar_hoy=False,
            ejercicio_hoy=False
        ),
        financiero=...,
        conocimiento=...,
        tiempo_disponible_hoy=120
    )

    preguntas = await agente.formular_preguntas_sacrales(contexto)

    assert len(preguntas) == 1  # Sistema 7 capas genera 1 pregunta
    assert preguntas[0].pregunta is not None
    assert len(preguntas[0].pregunta) > 10  # Pregunta significativa
EOF

# 6. Ejecutar tests incrementalmente
poetry run pytest tests/agentes/test_estado_cero.py -v

# 7. Repeat para otros módulos críticos
```

**Target Coverage**:
- Estado Cero: >80%
- Orquestador 7 Capas: >75%
- Generador Preguntas: >75%
- APIs: >70%
- Services: >70%

---

### B2. Zustand Instalado pero No Usado

**Descripción**: Librería de state management Zustand instalada pero sin uso en código

**Impacto**: 🟡 **5/10** - MEDIO
- Bundle size innecesario (+30KB)
- Dependency vulnerability surface
- Confusión sobre state management

**Esfuerzo**: ⏱️ **0.1 horas**

**Archivos Afectados**:
```
frontend/package.json    # zustand: ^4.5.0
```

**Solución Propuesta**:

```bash
cd frontend/

# 1. Verificar que NO se usa
grep -r "zustand" app/ lib/
grep -r "create(" app/ lib/ | grep -v "React.create"

# Si no hay resultados:
# 2. Desinstalar
npm uninstall zustand

# 3. Verificar app sigue funcionando
npm run dev
# Test manual en http://localhost:3000

# 4. Commit
git add package.json package-lock.json
git commit -m "chore: remove unused zustand dependency"
```

**Validación**:
```bash
# Verificar eliminado
cat package.json | grep zustand
# No debería retornar nada

# Bundle size comparison (opcional)
npm run build
# Comparar .next/static/chunks/ size antes/después
```

---

### B3. Lucide-React Infrautilizado

**Descripción**: Librería de iconos grande (441KB) pero posiblemente solo usa pocos iconos, considerar alternativa más ligera

**Impacto**: 🟡 **4/10** - MEDIO
- Bundle size grande si solo usa 2-3 iconos
- Performance impact menor

**Esfuerzo**: ⏱️ **3 horas**

**Archivos Afectados**:
```
frontend/
├── package.json          # lucide-react: ^0.441.0
└── app/**/*.tsx          # Imports de iconos
```

**Solución Propuesta**:

```bash
cd frontend/

# 1. Auditar uso de iconos
grep -r "lucide-react" app/ --include="*.tsx" --include="*.ts"

# Ejemplo output esperado:
# app/components/Header.tsx: import { Menu, X } from 'lucide-react'
# app/dashboard/page.tsx: import { Calendar } from 'lucide-react'

# 2. Contar iconos únicos usados
grep -roh "from 'lucide-react'" app/ | sort | uniq | wc -l

# Si usa <10 iconos:
# OPCIÓN A: Crear iconos inline SVG
mkdir -p app/components/icons/
cat > app/components/icons/Menu.tsx << 'EOF'
export const MenuIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
    <line x1="3" y1="12" x2="21" y2="12"/>
    <line x1="3" y1="6" x2="21" y2="6"/>
    <line x1="3" y1="18" x2="21" y2="18"/>
  </svg>
)
EOF

# OPCIÓN B: Usar @heroicons/react (más ligero)
npm uninstall lucide-react
npm install @heroicons/react

# Actualizar imports:
# De: import { Menu } from 'lucide-react'
# A:  import { Bars3Icon } from '@heroicons/react/24/outline'

# Si usa >10 iconos: MANTENER lucide-react (está bien)
```

**Decisión Requiere**:
- Auditar cantidad real de iconos
- Comparar bundle size
- Evaluar esfuerzo migración vs beneficio

---

### B4. @react-three/drei Sin Uso Confirmado

**Descripción**: Librería helpers Three.js instalada, uso no confirmado en código

**Impacto**: 🟡 **4/10** - MEDIO
- Bundle size innecesario si no se usa
- Dependency sin propósito

**Esfuerzo**: ⏱️ **1 hora**

**Archivos Afectados**:
```
frontend/
├── package.json                    # @react-three/drei: ^9.112.0
└── app/estado-cero-inmersivo/page.tsx  # Usa Three.js directamente
```

**Solución Propuesta**:

```bash
cd frontend/

# 1. Buscar imports de drei
grep -r "@react-three/drei" app/ lib/

# Si NO hay resultados:
# 2. Desinstalar
npm uninstall @react-three/drei

# 3. Verificar Three.js sigue funcionando
npm run dev
# Navegar a http://localhost:3000/estado-cero-inmersivo
# Verificar geometría sagrada (esfera 3D) se renderiza

# Si HAY uso:
# Documentar qué componentes usa:
# - <OrbitControls />
# - <Environment />
# - etc.
# Y mantener
```

**Validación**:
```bash
# App funciona sin drei
npm run build
# Build exitoso

# Test visual
# Estado Cero Inmersivo muestra fondo 3D correctamente
```

---

### B5. Sin Prettier en Frontend

**Descripción**: No hay formateador de código automático, estilos inconsistentes

**Impacto**: 🟡 **6/10** - MEDIO
- Código inconsistente
- Merge conflicts innecesarios
- Tiempo perdido en code reviews de estilo

**Esfuerzo**: ⏱️ **1 hora**

**Archivos Afectados**:
```
frontend/
├── (todos los archivos)   # Sin formateo consistente
└── package.json           # Falta prettier
```

**Solución Propuesta**:

```bash
cd frontend/

# 1. Instalar Prettier
npm install -D prettier eslint-config-prettier eslint-plugin-prettier

# 2. Crear .prettierrc
cat > .prettierrc << 'EOF'
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}
EOF

# 3. Crear .prettierignore
cat > .prettierignore << 'EOF'
node_modules/
.next/
out/
build/
coverage/
*.min.js
*.min.css
package-lock.json
EOF

# 4. Actualizar .eslintrc.json
# Añadir a "extends": "prettier"
# Ya incluido en solución A3

# 5. Formatear todo el código
npm run format

# 6. Añadir scripts
npm pkg set scripts.format="prettier --write \"**/*.{ts,tsx,js,jsx,json,md}\""
npm pkg set scripts.format:check="prettier --check \"**/*.{ts,tsx,js,jsx,json,md}\""

# 7. Verificar
npm run format:check
```

**Validación**:
```bash
# Todo formateado
npm run format:check
# No debería mostrar diferencias

# Pre-commit hook (opcional)
npm install -D husky lint-staged
npx husky install
npx husky add .husky/pre-commit "npm run format:check && npm run lint"
```

---

### B6. Sin Pre-commit Hooks en Frontend

**Descripción**: Frontend sin hooks de git para validar antes de commit

**Impacto**: 🟡 **5/10** - MEDIO
- Commits con código roto
- CI failures frecuentes
- Tiempo perdido

**Esfuerzo**: ⏱️ **1 hora**

**Archivos Afectados**:
```
frontend/
├── .husky/                 # No existe
└── package.json            # Sin husky/lint-staged
```

**Solución Propuesta**:

```bash
cd frontend/

# 1. Instalar Husky + lint-staged
npm install -D husky lint-staged

# 2. Inicializar Husky
npx husky install

# 3. Crear pre-commit hook
npx husky add .husky/pre-commit "npx lint-staged"

# 4. Configurar lint-staged en package.json
npm pkg set lint-staged."{ts,tsx}"[0]="eslint --fix"
npm pkg set lint-staged."{ts,tsx,js,jsx,json,md}"[1]="prettier --write"
npm pkg set lint-staged."*.{ts,tsx}"[2]="vitest related --run"

# 5. Añadir script prepare
npm pkg set scripts.prepare="husky install"

# 6. Test
echo "// test" >> app/page.tsx
git add app/page.tsx
git commit -m "test: pre-commit hook"
# Debería ejecutar linting y tests
```

**Validación**:
```bash
# Intentar commit con código roto
echo "const x = " >> app/page.tsx
git add app/page.tsx
git commit -m "test"
# Debería FALLAR por ESLint
```

---

### B7. Variables de Entorno No Validadas

**Descripción**: No hay validación de variables de entorno en startup, errores runtime

**Impacto**: 🟡 **7/10** - MEDIO-ALTO
- Errores en runtime vs startup
- Difícil debugging
- Deployment failures silenciosos

**Esfuerzo**: ⏱️ **2 horas**

**Archivos Afectados**:
```
frontend/
├── lib/config/env.ts       # No existe
└── app/layout.tsx          # No valida env

backend/
├── app/config.py           # Existe pero ¿valida todo?
└── .env                    # Sin schema validation
```

**Solución Propuesta - Frontend**:

```typescript
// frontend/lib/config/env.ts
import { z } from 'zod';

const envSchema = z.object({
  NEXT_PUBLIC_API_URL: z.string().url(),
  NEXT_PUBLIC_ENVIRONMENT: z.enum(['development', 'staging', 'production']),
  // Añadir otras variables
});

export const env = envSchema.parse({
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  NEXT_PUBLIC_ENVIRONMENT: process.env.NODE_ENV || 'development',
});

// Uso:
// import { env } from '@/lib/config/env'
// fetch(`${env.NEXT_PUBLIC_API_URL}/api/...`)
```

**Solución Propuesta - Backend**:

```python
# backend/app/config.py
from pydantic_settings import BaseSettings
from pydantic import Field, validator
import os

class Settings(BaseSettings):
    # API
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")

    # Database
    database_url: str = Field(default="sqlite:///./storage/organismo.db")

    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    # Google Calendar
    google_credentials_path: str = Field(
        default="config/google_credentials.json"
    )

    @validator("anthropic_api_key")
    def validate_api_key(cls, v):
        if not v or v.startswith("sk-ant-"):
            raise ValueError("ANTHROPIC_API_KEY inválida o faltante")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

# En app/main.py startup:
@app.on_event("startup")
async def validate_config():
    from app.config import settings
    logger.info(f"✅ Configuración validada correctamente")
```

---

### B8. Sin Bundle Analyzer

**Descripción**: No hay análisis de bundle size en frontend, posibles optimizaciones no identificadas

**Impacto**: 🟡 **5/10** - MEDIO
- Bundle size no controlado
- Performance degradation gradual
- No detección de duplicados

**Esfuerzo**: ⏱️ **1 hora**

**Archivos Afectados**:
```
frontend/
├── next.config.js          # Sin analyzer
└── package.json            # Falta @next/bundle-analyzer
```

**Solución Propuesta**:

```bash
cd frontend/

# 1. Instalar
npm install -D @next/bundle-analyzer

# 2. Actualizar next.config.js
cat > next.config.js << 'EOF'
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Tu configuración existente
}

module.exports = withBundleAnalyzer(nextConfig)
EOF

# 3. Añadir script
npm pkg set scripts.analyze="ANALYZE=true npm run build"

# 4. Ejecutar análisis
npm run analyze
# Abrirá navegador con visualización

# 5. Revisar chunks grandes
# - Buscar librerías duplicadas
# - Identificar código no usado
# - Optimizar imports
```

**Validación**:
```bash
npm run analyze
# Verificar:
# - Total bundle < 500KB (deseable)
# - No duplicados
# - Chunks balanceados
```

---

### B9. Sin Error Boundary en Frontend

**Descripción**: Frontend sin Error Boundaries, errores crash toda la app

**Impacto**: 🟡 **7/10** - MEDIO-ALTO
- UX pobre en errores
- Pérdida de estado usuario
- Difícil debugging producción

**Esfuerzo**: ⏱️ **2 horas**

**Archivos Afectados**:
```
frontend/
├── app/error.tsx           # No existe
├── app/global-error.tsx    # No existe
└── app/components/         # Sin error boundaries
```

**Solución Propuesta**:

```typescript
// app/error.tsx (Error boundary por defecto)
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="max-w-md p-8 bg-white/10 backdrop-blur-lg rounded-2xl">
        <h2 className="text-2xl font-bold text-white mb-4">
          Algo salió mal
        </h2>
        <p className="text-gray-300 mb-6">
          {error.message || 'Error inesperado'}
        </p>
        <button
          onClick={reset}
          className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg"
        >
          Intentar de nuevo
        </button>
      </div>
    </div>
  );
}

// app/global-error.tsx (Error boundary global)
'use client';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <h2>Error crítico</h2>
        <button onClick={reset}>Reintentar</button>
      </body>
    </html>
  );
}

// app/components/ErrorBoundary.tsx (Reutilizable)
'use client';

import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <div>Error</div>;
    }
    return this.props.children;
  }
}
```

---

### B10. Sin Logging Estructurado en Frontend

**Descripción**: Frontend usa console.log sin estructura, difícil debugging producción

**Impacto**: 🟡 **6/10** - MEDIO
- Logs no estructurados
- Difícil debugging producción
- No integración con error tracking

**Esfuerzo**: ⏱️ **3 horas**

**Archivos Afectados**:
```
frontend/
├── lib/logger.ts           # No existe
└── app/**/*.tsx            # console.log directo
```

**Solución Propuesta**:

```typescript
// lib/logger.ts
type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogContext {
  [key: string]: any;
}

class Logger {
  private context: LogContext = {};

  setContext(context: LogContext) {
    this.context = { ...this.context, ...context };
  }

  private log(level: LogLevel, message: string, extra?: LogContext) {
    const logData = {
      level,
      message,
      timestamp: new Date().toISOString(),
      ...this.context,
      ...extra,
    };

    if (process.env.NODE_ENV === 'production') {
      // Enviar a servicio externo (Sentry, LogRocket, etc.)
      // Sentry.captureMessage(message, { level, extra: logData });
    }

    // Console en desarrollo
    if (process.env.NODE_ENV === 'development') {
      const color = {
        debug: '\x1b[36m',
        info: '\x1b[32m',
        warn: '\x1b[33m',
        error: '\x1b[31m',
      }[level];
      console.log(`${color}[${level.toUpperCase()}]\x1b[0m`, message, extra);
    }
  }

  debug(message: string, context?: LogContext) {
    this.log('debug', message, context);
  }

  info(message: string, context?: LogContext) {
    this.log('info', message, context);
  }

  warn(message: string, context?: LogContext) {
    this.log('warn', message, context);
  }

  error(message: string, error?: Error, context?: LogContext) {
    this.log('error', message, { ...context, error: error?.message, stack: error?.stack });
  }
}

export const logger = new Logger();

// Uso:
// import { logger } from '@/lib/logger'
// logger.info('Estado Cero iniciado', { momento: 'dhuhr', userId: '123' })
// logger.error('Error API', error, { endpoint: '/api/estado-cero' })
```

---

## CATEGORÍA C: MEJORAS

**Hacer cuando haya tiempo** - Nice to have, no bloquean

### C1. Configuraciones Personales en Repo

**Descripción**: `.aliases`, `.zshrc`, `.iterm2_campo_sagrado.sh` en root del proyecto

**Impacto**: 🟢 **3/10** - BAJO
- Repo poco profesional
- Configs personales expuestas
- No afecta funcionalidad

**Esfuerzo**: ⏱️ **0.2 horas**

**Solución**: Mover a `.dotfiles/` y añadir a `.gitignore` (ver A4)

---

### C2. requirements-future.txt No Usado

**Descripción**: Archivo `backend/requirements-future.txt` parece no usarse

**Impacto**: 🟢 **2/10** - BAJO
- Confusión menor
- No afecta build

**Esfuerzo**: ⏱️ **0.1 horas**

**Solución**:
```bash
cd backend/
# Verificar si se usa
grep -r "requirements-future" .
# Si no: eliminar
rm requirements-future.txt
```

---

### C3. Nombres de Archivos Inconsistentes

**Descripción**: Algunos archivos MD en MAYÚSCULAS, otros minúsculas, algunos con guiones, otros underscores

**Impacto**: 🟢 **3/10** - BAJO
- Estética
- Navegación menor

**Esfuerzo**: ⏱️ **2 horas**

**Solución**: Estandarizar a kebab-case en reorganización docs (ver A4)

---

### C4. READMEs Faltantes en Subcarpetas

**Descripción**: Carpetas principales sin README explicativo

**Impacto**: 🟢 **4/10** - BAJO-MEDIO
- Onboarding más lento
- No crítico

**Esfuerzo**: ⏱️ **3 horas**

**Solución**:
```bash
# Crear READMEs
cat > backend/README.md << 'EOF'
# Backend - Campo Sagrado MVP

FastAPI backend con sistema de 7 capas...
EOF

cat > frontend/README.md << 'EOF'
# Frontend - Campo Sagrado MVP

Next.js 14 frontend con App Router...
EOF

# etc.
```

---

### C5. Sin CONTRIBUTING.md

**Descripción**: No hay guía para contribuir al proyecto

**Impacto**: 🟢 **3/10** - BAJO
- Dificulta open source (si aplica)
- No crítico para proyecto privado

**Esfuerzo**: ⏱️ **2 horas**

**Solución**: Crear CONTRIBUTING.md con guidelines

---

### C6. Sin CI/CD Pipeline

**Descripción**: No hay automatización de tests/deploy

**Impacto**: 🟢 **5/10** - MEDIO (pero no urgente)
- Deploy manual
- Tests manuales
- Bueno tener, no crítico en MVP

**Esfuerzo**: ⏱️ **16 horas**

**Solución**: GitHub Actions (futura implementación)

---

### C7. Sin Storybook para Componentes

**Descripción**: No hay catálogo de componentes UI

**Impacto**: 🟢 **4/10** - BAJO-MEDIO
- Útil para equipos grandes
- No crítico para MVP

**Esfuerzo**: ⏱️ **8 horas**

**Solución**: Implementar Storybook (futuro)

---

## 📊 RESUMEN EJECUTIVO

### Por Categoría

| Categoría | Problemas | Esfuerzo Total | Impacto Promedio |
|-----------|-----------|----------------|------------------|
| **A - CRÍTICO** | 7 | ~46 horas | 8.1/10 |
| **B - ALTO** | 10 | ~48 horas | 5.7/10 |
| **C - MEJORAS** | 7 | ~33 horas | 3.4/10 |
| **TOTAL** | 24 | ~127 horas | 5.7/10 |

### Top 5 Prioridades (Por Impacto × Urgencia)

1. **A1 - Sin Testing Frontend** (Impacto 10, Esfuerzo 40h)
2. **A2 - Dependencias Desincronizadas** (Impacto 9, Esfuerzo 1h)
3. **A3 - Sin ESLint Frontend** (Impacto 8, Esfuerzo 2h)
4. **A4 - Root Sobrecargado** (Impacto 8, Esfuerzo 2h)
5. **B1 - Tests Backend Incompletos** (Impacto 8, Esfuerzo 30h)

### Quick Wins (< 2 horas, Alto Impacto)

1. **A2 - Sincronizar dependencias** (1h, Impacto 9)
2. **A5 - Eliminar frontends duplicados** (0.5h, Impacto 7)
3. **A6 - Eliminar storage duplicado** (0.5h, Impacto 7)
4. **B2 - Eliminar Zustand** (0.1h, Impacto 5)

**Total Quick Wins**: 2.1 horas, Impacto combinado: 28/40

---

## 🎯 PLAN DE ACCIÓN RECOMENDADO

### Semana 1: Quick Wins + Fundamentos

**Día 1 (HOY)**:
- [ ] A2: Sincronizar dependencias (1h)
- [ ] A5: Eliminar frontends duplicados (0.5h)
- [ ] A6: Eliminar storage duplicado (0.5h)
- [ ] B2: Eliminar Zustand (0.1h)
- [ ] A3: Configurar ESLint (2h)

**Total**: 4.1 horas

**Día 2**:
- [ ] A4: Reorganizar root (2h)
- [ ] A7: Limpiar nested directories (1h)
- [ ] B5: Configurar Prettier (1h)

**Total**: 4 horas

**Día 3-5**:
- [ ] A1: Setup testing frontend (2h)
- [ ] A1: Primeros 20 tests (10h)

**Total**: 12 horas

### Semana 2-3: Testing Completo

- [ ] A1: Completar tests frontend (28h restantes)
- [ ] B1: Completar tests backend (30h)

**Total**: 58 horas

### Semana 4: Deuda Técnica

- [ ] B3-B10: Resolver deuda técnica restante (18h)
- [ ] C1-C7: Mejoras opcionales (según tiempo)

---

## ✅ CHECKLIST DE VALIDACIÓN

Después de resolver cada problema, verificar:

- [ ] Tests pasan
- [ ] Linting pasa
- [ ] Build exitoso
- [ ] App funciona manualmente
- [ ] Documentación actualizada
- [ ] Commit con mensaje descriptivo

---

**Generado**: Auditoría Completa - Problemas Críticos Priorizados
**Total Problemas**: 24 (7 críticos, 10 alta prioridad, 7 mejoras)
**Esfuerzo Total**: ~127 horas (~3.5 semanas)
**Próximo**: Ejecutar Quick Wins (2.1 horas)
