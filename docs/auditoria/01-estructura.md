# AUDITORÍA 1: Estructura del Proyecto

**Fecha**: 18 de Octubre de 2025
**Proyecto**: Campo Sagrado MVP
**Total**: 91 directorios, 363 archivos

---

## 📂 ÁRBOL DE DIRECTORIOS ANOTADO

```
Campo sagrado MVP/
├── 📁 backend/                     ✅ Backend Python (FastAPI)
│   ├── agentes/                    ✅ Agentes IA (Estado Cero, Documentador, etc.)
│   ├── api/                        ✅ Endpoints FastAPI
│   ├── app/                        ⚠️ DUPLICADO - Estructura alternativa no usada
│   ├── backend/                    ⚠️ NESTED INCORRECTAMENTE - Solo .env adentro
│   ├── config/                     ✅ Credenciales Google Calendar
│   ├── integraciones/              ✅ Anytype, Obsidian, Google Calendar
│   ├── logs/                       ✅ Logs del sistema
│   ├── middleware/                 ✅ Security middleware
│   ├── models/                     ✅ Schemas Pydantic + SQLAlchemy
│   ├── scripts/                    ✅ Scripts de setup/validación
│   ├── services/                   ✅ Lógica de negocio (Orquestador, Generador, etc.)
│   ├── storage/                    ✅ Estados Cero, eventos, DB SQLite
│   ├── tests/                      ✅ Tests (si existen)
│   ├── workers/                    ✅ Background workers
│   ├── ~/                          ⚠️ HOME DIRECTORY ANIDADO - INCORRECTO
│   ├── .coveragerc                 ✅ Config cobertura tests
│   ├── .env                        ✅ Variables entorno
│   ├── .env.example                ✅ Template env
│   ├── .gitignore                  ✅ Git ignore
│   ├── poetry.lock                 ✅ Dependency lock
│   ├── pyproject.toml              ✅ Poetry config
│   ├── pytest.ini                  ✅ Pytest config
│   ├── README.md                   ✅ Docs backend
│   ├── requirements-future.txt     ⚠️ NO USADO - Usar solo Poetry
│   └── requirements.txt            ✅ Pip requirements (generado de Poetry)
│
├── 📁 campo-sagrado-nextjs/        ✅ Frontend Next.js 14 (PRINCIPAL)
│   ├── app/                        ✅ App Router Next.js 14
│   │   ├── components/             ✅ Componentes compartidos
│   │   │   ├── PuertaDeEntrada7Capas.tsx  ✅ Sistema 7 capas
│   │   │   └── ...
│   │   ├── dashboard/              ✅ Rutas dashboard
│   │   ├── espejo-diario/          ✅ Espejo diario
│   │   ├── estado-cero-inmersivo/  ✅ Estado Cero (ACTUAL)
│   │   ├── estado-cero-simple/     ⚠️ LEGACY - Reemplazado por inmersivo
│   │   ├── favicon.ico             ✅ Favicon
│   │   ├── globals.css             ✅ Estilos globales
│   │   ├── layout.tsx              ✅ Layout principal
│   │   └── page.tsx                ✅ Landing page
│   ├── lib/                        ✅ Utils y helpers
│   │   ├── api/                    ✅ Cliente API
│   │   ├── config/                 ✅ Configs
│   │   └── types/                  ✅ TypeScript types
│   ├── public/                     ✅ Assets públicos
│   ├── .gitignore                  ✅ Git ignore
│   ├── next.config.js              ✅ Next.js config
│   ├── package.json                ✅ Dependencies
│   ├── postcss.config.js           ✅ PostCSS config
│   ├── README.md                   ✅ Docs frontend
│   ├── tailwind.config.ts          ✅ Tailwind config
│   └── tsconfig.json               ✅ TypeScript config
│
├── 📁 frontend/                    ⚠️ LEGACY - SvelteKit (NO USADO)
│   ├── .svelte-kit/                ⚠️ LEGACY
│   ├── src/                        ⚠️ LEGACY
│   ├── package.json                ⚠️ LEGACY
│   └── ...                         ⚠️ CANDIDATO PARA ELIMINAR
│
├── 📁 frontend-next/               ⚠️ DUPLICADO - Estructura alternativa Next.js
│   ├── app/                        ⚠️ Similar a campo-sagrado-nextjs
│   ├── components/                 ⚠️ Componentes duplicados
│   ├── hooks/                      ⚠️ Hooks custom
│   ├── lib/                        ⚠️ Utils duplicados
│   └── ...                         ⚠️ CONSOLIDAR CON campo-sagrado-nextjs
│
├── 📁 obsidian_vault/              ✅ Vault Obsidian (Datos usuario)
│   ├── 00-Pilares/                 ✅ Pilares fundamentales
│   ├── 10-Dominios/                ✅ 10 dominios vitales
│   ├── 10-Meta/                    ✅ Meta configuración
│   ├── 20-Insights/                ✅ Insights emergentes
│   ├── 20-Proyectos/               ✅ Proyectos
│   ├── 30-Recursos/                ✅ Recursos
│   ├── 30-Sesiones/                ✅ Sesiones Estado Cero
│   ├── 40-Journal/                 ✅ Journal diario
│   └── 50-Conversaciones-IA/       ✅ Conversaciones
│       └── Estados-Cero/           ✅ Estados Cero archivados
│
├── 📁 archive/                     ✅ Docs históricos archivados
│   ├── analisis/                   ✅ Análisis anteriores
│   ├── implementaciones/           ✅ Docs de implementación
│   └── resumenes/                  ✅ Resúmenes de sesiones
│
├── 📁 docs/                        ✅ Documentación técnica
│   ├── API_REFERENCE.md            ✅ Ref API
│   ├── ARQUITECTURA_TECNICA.md     ✅ Arquitectura
│   ├── GUIA_USUARIO_COMPLETA.md    ✅ Guía usuario
│   ├── auditoria/                  ✅ ESTE DOCUMENTO
│   └── ...                         ✅ Múltiples docs
│
├── 📁 config/                      ⚠️ POCO CLARO - Solo 2 archivos
│   ├── campo-sagrado.env           ⚠️ Duplicado de backend/.env?
│   └── campo-sagrado.yaml          ⚠️ No usado?
│
├── 📁 scripts/                     ✅ Scripts de inicialización
│   ├── detener-sistema.sh          ✅ Stop servers
│   ├── iniciar-sistema.sh          ✅ Start servers
│   ├── setup-completo.sh           ✅ Setup inicial
│   ├── verificar-sistema.sh        ✅ Health check
│   └── ...                         ✅ Scripts útiles
│
├── 📁 storage/                     ⚠️ DUPLICADO con backend/storage
│   ├── datos_prueba.json           ⚠️ Datos de prueba
│   └── organismo.db                ⚠️ DUPLICADO - DB está en backend/storage
│
├── 📁 logs/                        ✅ Logs del sistema (vacío)
│
├── 📁 .claude/                     ✅ Claude Code config
├── 📁 .claude-code/                ✅ Claude Code project
├── 📁 .pids/                       ✅ Process IDs
│
└── 📄 ROOT (60+ archivos MD)       ⚠️ PROBLEMA GRAVE
    ├── README.md                   ✅ Principal
    ├── CHANGELOG.md                ✅ Changelog
    ├── INTEGRACION_TOTAL_COMPLETADA.md  ✅ Doc actual
    ├── SISTEMA_7_CAPAS_FUNCIONANDO.md   ✅ Doc actual
    ├── test_integracion.sh         ✅ Script testing
    ├── verificar_sistema.sh        ✅ Script verificación
    ├── .gitignore                  ✅ Git ignore
    ├── .cursorrules                ✅ Cursor config
    ├── .aliases                    ⚠️ Shell aliases (fuera de lugar)
    ├── .zshrc                      ⚠️ Shell config (fuera de lugar)
    ├── .iterm2_campo_sagrado.sh    ⚠️ iTerm2 config (fuera de lugar)
    └── 50+ ARCHIVOS MD             ⚠️ CAOS DOCUMENTAL
        ├── ANALISIS_*.md           ⚠️ Mover a docs/analisis/
        ├── ARQUITECTURA_*.md       ⚠️ Mover a docs/arquitectura/
        ├── ESTADO_*.md             ⚠️ Mover a docs/estados/
        ├── FIX_*.md                ⚠️ Mover a archive/fixes/
        ├── RESUMEN_*.md            ⚠️ Mover a archive/resumenes/
        └── ...                     ⚠️ 40+ archivos desordenados
```

---

## 🚨 PROBLEMAS IDENTIFICADOS

### CRÍTICOS (Resolver AHORA)

1. **⚠️ ROOT DIRECTORY SOBRECARGADO**
   - **Problema**: 60+ archivos Markdown en raíz
   - **Impacto**: Navegación confusa, difícil encontrar archivos
   - **Solución**: Mover a `docs/` o `archive/`
   - **Archivos afectados**: ~50 archivos MD

   ```bash
   # Estructura propuesta:
   docs/
   ├── analisis/        # ANALISIS_*.md
   ├── arquitectura/    # ARQUITECTURA_*.md
   ├── estados/         # ESTADO_*.md
   ├── guias/           # GUIA_*.md
   └── testing/         # TESTING_*.md

   archive/
   ├── fixes/           # FIX_*.md
   ├── resumenes/       # RESUMEN_*.md
   └── migraciones/     # MIGRACION_*.md
   ```

2. **⚠️ FRONTENDS DUPLICADOS**
   - **Problema**: 3 carpetas de frontend
     - `frontend/` (SvelteKit - LEGACY)
     - `frontend-next/` (Next.js alternativo)
     - `campo-sagrado-nextjs/` (Next.js ACTUAL)
   - **Impacto**: Confusión, código duplicado, espacio desperdiciado
   - **Solución**:
     ```bash
     # Eliminar:
     rm -rf frontend/          # LEGACY SvelteKit
     rm -rf frontend-next/     # Alternativa no usada

     # Renombrar:
     mv campo-sagrado-nextjs/ frontend/
     ```

3. **⚠️ STORAGE DUPLICADO**
   - **Problema**: `storage/` en root Y `backend/storage/`
   - **DB duplicada**: `organismo.db` en ambos lugares
   - **Solución**: Eliminar `storage/` root, usar solo `backend/storage/`

4. **⚠️ NESTED INCORRECTAMENTE**
   - `backend/backend/.env` → Debería estar en `backend/.env` (YA EXISTE)
   - `backend/~/Documents/` → Home directory anidado (ELIMINAR)
   - `backend/app/` → Estructura app duplicada no usada (ELIMINAR)

5. **⚠️ ARCHIVOS SHELL EN ROOT**
   - `.aliases`, `.zshrc`, `.iterm2_campo_sagrado.sh`
   - **Problema**: Configs personales en repo del proyecto
   - **Solución**:
     - Mover a `.dotfiles/` o
     - Añadir a `.gitignore` (configs locales)

### MODERADOS (Resolver en DÍA 7-8)

6. **📦 DEPENDENCIES POTENCIALMENTE NO USADAS**
   - `backend/requirements-future.txt` → NO USADO, usar solo Poetry
   - `config/campo-sagrado.yaml` → No usado?
   - `config/campo-sagrado.env` → Duplicado de `backend/.env`?

7. **📂 ESTRUCTURA `app/` EN BACKEND**
   - `backend/app/` parece una arquitectura alternativa
   - Tiene `agentes/`, `api/`, `services/` duplicados
   - **Acción**: Verificar si se usa, eliminar si es legacy

8. **📝 DOCUMENTACIÓN FRAGMENTADA**
   - Docs en 3 lugares: `docs/`, `archive/`, ROOT
   - Algunos archivos duplicados
   - No hay índice maestro

### MENORES (Opcional)

9. **🗂 NOMBRES INCONSISTENTES**
   - Algunos MD en MAYÚSCULAS, otros en minúsculas
   - Algunos con guiones, otros con underscores
   - **Recomendación**: Estándar kebab-case para archivos

10. **📁 CARPETAS VACÍAS/POCO USADAS**
    - `logs/` en root (vacío)
    - `backend/logs/` (solo scheduler.log)
    - `backend/tests/` (existe pero ¿hay tests?)

---

## ✅ ESTRUCTURA BIEN ORGANIZADA

### Backend
- ✅ Separación clara: `agentes/`, `api/`, `services/`, `models/`
- ✅ Config de testing: `.coveragerc`, `pytest.ini`
- ✅ Poetry para dependencies
- ✅ Scripts de setup útiles
- ✅ Middleware de seguridad

### Frontend (campo-sagrado-nextjs)
- ✅ Next.js 14 App Router
- ✅ Componentes organizados
- ✅ TypeScript configurado
- ✅ Tailwind + PostCSS
- ✅ Estructura de tipos

### Obsidian Vault
- ✅ Estructura PARA: Pilares, Dominios, Insights, Proyectos, Recursos, Sesiones
- ✅ Carpetas numeradas (00-, 10-, 20-) para orden
- ✅ Separación clara de contenido

### Scripts
- ✅ Scripts útiles de inicio/detención
- ✅ Verificación de sistema
- ✅ Setup completo

---

## 📊 MÉTRICAS DEL PROYECTO

| Métrica | Valor |
|---------|-------|
| Total directorios | 91 |
| Total archivos | 363 |
| Archivos MD en root | ~60 |
| Frontends diferentes | 3 (2 legacy) |
| Archivos duplicados | ~10 |
| Estructura principal | Backend + Frontend + Vault |

---

## 🎯 PLAN DE ACCIÓN RECOMENDADO

### Fase 1: Limpieza Crítica (HOY)
```bash
# 1. Reorganizar docs del root
mkdir -p docs/{analisis,arquitectura,estados,guias,testing}
mv ANALISIS_*.md docs/analisis/
mv ARQUITECTURA_*.md docs/arquitectura/
mv ESTADO_*.md docs/estados/
mv GUIA_*.md docs/guias/
mv TESTING_*.md docs/testing/

# 2. Archivar históricos
mv FIX_*.md archive/fixes/
mv RESUMEN_*.md archive/resumenes/
mv MIGRACION_*.md archive/migraciones/

# 3. Eliminar frontends legacy
rm -rf frontend/
rm -rf frontend-next/
mv campo-sagrado-nextjs/ frontend/

# 4. Eliminar storage duplicado
rm -rf storage/

# 5. Limpiar nested directories
rm -rf backend/backend/
rm -rf backend/~/
rm -rf backend/app/  # Si no se usa

# 6. Mover configs personales
mkdir -p .dotfiles/
mv .aliases .zshrc .iterm2_campo_sagrado.sh .dotfiles/
```

### Fase 2: Consolidación (DÍA 7)
- Verificar y eliminar dependencies no usadas
- Consolidar configuraciones duplicadas
- Crear índice maestro de documentación

### Fase 3: Estandarización (DÍA 8)
- Renombrar archivos a kebab-case
- Unificar estructura de docs
- Añadir READMEs a carpetas principales

---

## 🏆 ESTRUCTURA OBJETIVO

```
campo-sagrado-mvp/
├── backend/             # ✅ Backend Python
├── frontend/            # ✅ Frontend Next.js (renombrado)
├── obsidian_vault/      # ✅ Vault Obsidian
├── docs/                # ✅ TODA la documentación
│   ├── analisis/
│   ├── arquitectura/
│   ├── estados/
│   ├── guias/
│   ├── testing/
│   └── auditoria/
├── archive/             # ✅ Históricos
├── scripts/             # ✅ Scripts sistema
├── .dotfiles/           # ✅ Configs personales (gitignored)
├── README.md            # ✅ Principal
├── CHANGELOG.md         # ✅ Changelog
└── .gitignore           # ✅ Git ignore
```

**Total**: ~8 directorios principales, ~5 archivos en root

---

## 📝 CONCLUSIONES

### ✅ Fortalezas
1. Backend bien estructurado
2. Frontend moderno (Next.js 14)
3. Vault Obsidian organizado
4. Scripts útiles de sistema
5. Separación clara de concerns

### ⚠️ Debilidades
1. **Root sobrecargado** (60+ archivos)
2. **Frontends duplicados** (3 versiones)
3. **Docs fragmentadas** (3 ubicaciones)
4. **Nested directories incorrectos**
5. **Configs personales en repo**

### 🎯 Prioridad
**ALTA**: Limpiar root y eliminar frontends legacy
**MEDIA**: Consolidar documentación
**BAJA**: Estandarizar nombres

---

**Generado**: Auditoría 1 - Estructura del Proyecto
**Estado**: ⚠️ Requiere limpieza urgente en root y frontends
**Próximo**: Auditoría 2 - Análisis de Dependencias
