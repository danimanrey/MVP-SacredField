# 🕌 CAMPO SAGRADO DEL ENTRELAZADOR
## GUÍA DEFINITIVA DE IMPLEMENTACIÓN - MVP COMPLETO

---

## 📋 ÍNDICE EJECUTIVO

Esta guía te llevará desde cero hasta un sistema completamente funcional en **~4 horas**.

### Estado Actual
✅ Especificación técnica completa (Conversación anterior)  
✅ 55 archivos de código generados  
✅ Arquitectura de 4 agentes diseñada  
✅ Frontend completo en SvelteKit  
✅ Backend completo en FastAPI  

### Lo que vas a construir
Un organismo tecnológico-espiritual que:
- Calcula tiempos litúrgicos exactos para tu ubicación
- Facilita 5 Estados Cero diarios con consulta sacral
- Orquesta tu jornada al borde del caos
- Genera documentación automática en Obsidian
- Opera con calendario Hijri de 13 meses
- Respeta tu autoridad sacral como brújula

---

## 🎯 PLAN DE IMPLEMENTACIÓN (4 fases)

### FASE 1: Setup Inicial (30 min)
1. Crear estructura de proyecto
2. Instalar dependencias
3. Configurar entornos
4. Verificar conexiones

### FASE 2: Backend Core (90 min)
5. Base de datos
6. Servicios core (tiempos, calendario, contexto)
7. Los 4 agentes
8. API REST

### FASE 3: Frontend (90 min)
9. Setup SvelteKit
10. Componentes UI
11. Páginas principales
12. Integración con API

### FASE 4: Testing y Launch (30 min)
13. Tests del sistema
14. Primer Estado Cero real
15. Ajustes finales

---

## 📦 FASE 1: SETUP INICIAL (30 min)

### 1.1 Prerrequisitos

Verifica que tienes instalado:

```bash
# Node.js 18+
node --version

# Python 3.11+
python3 --version

# pnpm
pnpm --version

# Git
git --version
```

Si falta algo:
```bash
# macOS
brew install node python@3.11 pnpm

# Linux (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs python3.11 python3.11-venv
npm install -g pnpm
```

### 1.2 Crear Estructura del Proyecto

```bash
# Crear directorio raíz
mkdir campo-sagrado
cd campo-sagrado

# Estructura completa
mkdir -p {backend/{api,agentes,models,services,integraciones,scripts},frontend/src/{routes,lib/{api,stores,components/{EstadoCero,EspejoDiario,Shared}}},config,storage,docs,scripts}

# Verificar
tree -L 2
```

### 1.3 Inicializar Git

```bash
git init

# .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
venv/
.env

# Node
node_modules/
.svelte-kit/
dist/

# Storage
storage/
logs/
backups/

# IDE
.vscode/
.idea/

# OS
.DS_Store
EOF

git add .
git commit -m "Initial structure"
```

### 1.4 README Principal

```bash
cat > README.md << 'EOF'
# 🕌 Campo Sagrado del Entrelazador

Sistema de conocimiento personal vivo.

## Quick Start

```bash
# 1. Setup
./scripts/setup-completo.sh

# 2. Configurar API key
nano backend/.env

# 3. Iniciar
./scripts/iniciar-sistema.sh
```

## Estado: MVP en desarrollo
Ver `docs/IMPLEMENTACION.md` para progreso.
EOF
```

### 1.5 API Key de Anthropic

1. Ve a: https://console.anthropic.com/
2. Crea cuenta o inicia sesión
3. Settings → API Keys → Create Key
4. Guarda la key (la usarás después)

---

## 🐍 FASE 2: BACKEND CORE (90 min)

### 2.1 Setup Backend Base

```bash
cd backend

# requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
anthropic==0.7.7
chromadb==0.4.18
sqlalchemy==2.0.23
python-dotenv==1.0.0
pyyaml==6.0.1
pytz==2023.3
python-dateutil==2.8.2
httpx==0.25.2
EOF

# Crear venv
python3 -m venv venv
source venv/bin/activate

# Instalar
pip install --upgrade pip
pip install -r requirements.txt

# .env.example
cat > .env.example << 'EOF'
ANTHROPIC_API_KEY=your_key_here
DATABASE_URL=sqlite:///./storage/organismo.db
CHROMA_PATH=./storage/chroma_db
OBSIDIAN_VAULT_PATH=~/Documents/CampoSagrado
CIUDAD=Madrid
LATITUD=40.4168
LONGITUD=-3.7038
TIMEZONE=Europe/Madrid
ENVIRONMENT=development
LOG_LEVEL=INFO
EOF

# Copiar a .env
cp .env.example .env

echo "⚠️  IMPORTANTE: Edita .env y agrega tu ANTHROPIC_API_KEY"
```

### 2.2 Base de Datos

Crea `backend/models/database.py` con el contenido del **Archivo 05** (ya generado en artifacts anteriores).

```bash
# Crear archivo
nano models/database.py
# Pega el contenido del Archivo 05
```

Crea `backend/models/schemas.py` con el contenido del **Archivo 04**.

```bash
nano models/schemas.py
# Pega el contenido del Archivo 04
```

### 2.3 Scripts de Inicialización

Crea `backend/scripts/init_db.py` con el contenido del **Archivo 21**.

```bash
mkdir -p scripts
nano scripts/init_db.py
# Pega contenido del Archivo 21

# Ejecutar
python scripts/init_db.py
```

Deberías ver:
```
🗄️  Creando tablas de base de datos...
✓ Tablas creadas:
  - estados_cero
  - sesiones
  - biometria_diaria
  - no_negociables_tracking
  - documentos
  - capturas
✨ Base de datos inicializada correctamente
```

### 2.4 Servicios Core

Crea cada servicio en `backend/services/`:

**tiempos_liturgicos.py** (Archivo 06):
```bash
nano services/tiempos_liturgicos.py
# Pega contenido completo del Archivo 06
```

**calendario_hijri.py** (Archivo 07):
```bash
nano services/calendario_hijri.py
# Pega contenido del Archivo 07
```

**contexto.py** (Archivo 08):
```bash
nano services/contexto.py
# Pega contenido
```

**claude_client.py** (Archivo 09):
```bash
nano services/claude_client.py
# Pega contenido
```

### 2.5 Verificar Servicios

Crea `backend/scripts/calcular_tiempos.py` (Archivo 23) y ejecútalo:

```bash
python scripts/calcular_tiempos.py
```

Deberías ver:
```
🕌 TIEMPOS DE REZO - Madrid
📅 Jueves, 02 de Enero de 2025
═══════════════════════════════════
Momento      Ventana Estado Cero    Fin del tiempo
────────────────────────────────────
🌅 FAJR      06:45                  08:15
☀️ DHUHR     13:40                  16:15
🌤️ ASR       16:15                  18:00
🌆 MAGHRIB   18:00                  19:30
🌙 ISHA      19:30                  06:45

⏰ Próximo Estado Cero: MAGHRIB
   Hora: 18:00
   En: 5h 30m
```

### 2.6 Los 4 Agentes

Crea cada agente en `backend/agentes/`:

1. **estado_cero.py** (Archivo 10)
2. **orquestador.py** (Archivo 11)
3. **guardian.py** (Archivo 12)
4. **documentador.py** (Archivo 13)

```bash
cd agentes

# Crear cada archivo
nano estado_cero.py      # Pega Archivo 10
nano orquestador.py      # Pega Archivo 11
nano guardian.py         # Pega Archivo 12
nano documentador.py     # Pega Archivo 13

cd ..
```

### 2.7 API REST

Crea endpoints en `backend/api/`:

```bash
cd api

# Archivos de API
nano main.py              # Archivo 14
nano estado_cero.py       # Archivo 15
nano orquestador.py       # Archivo 16
nano guardian.py          # Archivo 17
nano websockets.py        # Archivo 18

cd ..
```

### 2.8 Integraciones

```bash
cd integraciones

nano obsidian.py          # Archivo 19
nano anytype.py           # Archivo 20

cd ..
```

### 2.9 Test del Backend

```bash
# Test completo
python scripts/test_sistema.py
```

Todos los tests deben pasar ✅

### 2.10 Iniciar Backend

```bash
# Desde backend/
python api/main.py
```

Deberías ver:
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Abre http://localhost:8000/docs - verás la documentación Swagger de tu API.

**Deja este terminal corriendo** y abre uno nuevo.

---

## 🎨 FASE 3: FRONTEND (90 min)

### 3.1 Setup SvelteKit

```bash
# En nueva terminal
cd campo-sagrado/frontend

# package.json
cat > package.json << 'EOF'
{
  "name": "campo-sagrado-frontend",
  "version": "0.1.0",
  "scripts": {
    "dev": "vite dev",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "@sveltejs/adapter-auto": "^3.0.0",
    "@sveltejs/kit": "^2.0.0",
    "@sveltejs/vite-plugin-svelte": "^3.0.0",
    "svelte": "^4.2.7",
    "typescript": "^5.0.0",
    "vite": "^5.0.3"
  },
  "dependencies": {
    "d3": "^7.8.5",
    "@types/d3": "^7.4.3"
  },
  "type": "module"
}
EOF

# Instalar
pnpm install
```

### 3.2 Configuración

```bash
# svelte.config.js (Archivo 27)
cat > svelte.config.js << 'EOF'
import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

export default {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter()
	}
};
EOF

# vite.config.ts (Archivo 28)
cat > vite.config.ts << 'EOF'
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		port: 5173,
		proxy: {
			'/api': {
				target: 'http://localhost:8000',
				changeOrigin: true
			}
		}
	}
});
EOF

# tsconfig.json
cat > tsconfig.json << 'EOF'
{
	"extends": "./.svelte-kit/tsconfig.json",
	"compilerOptions": {
		"allowJs": true,
		"checkJs": true,
		"esModuleInterop": true,
		"forceConsistentCasingInFileNames": true,
		"resolveJsonModule": true,
		"skipLibCheck": true,
		"sourceMap": true,
		"strict": true
	}
}
EOF
```

### 3.3 Estilos Globales

```bash
# src/app.css (Archivo 29)
nano src/app.css
# Pega el contenido del Archivo 29
```

### 3.4 API Client

```bash
mkdir -p src/lib/api
nano src/lib/api/client.ts
# Pega contenido del Archivo 30
```

### 3.5 Stores

```bash
mkdir -p src/lib/stores

nano src/lib/stores/tiempo.ts          # Archivo 31
nano src/lib/stores/estadoCero.ts      # Archivo 32
nano src/lib/stores/jornada.ts         # Archivo 33
```

### 3.6 Componentes UI

```bash
mkdir -p src/lib/components/{EstadoCero,EspejoDiario,Shared}

# Componentes Estado Cero
cd src/lib/components/EstadoCero
nano VerificacionMomento.svelte        # Archivo 34
nano ContextoDisplay.svelte            # Archivo 35
nano ConsultaSacral.svelte             # Archivo 36
nano ChatClarificador.svelte           # Archivo 37

# Componentes compartidos
cd ../Shared
nano GeometriaSagrada.svelte

# GeometriaSagrada básico
cat > GeometriaSagrada.svelte << 'EOF'
<script lang="ts">
	export let tipo: string = 'fajr';
	export let animacion: string = 'pulsante';
</script>

<div class="geometria {tipo} {animacion}">
	<svg viewBox="0 0 100 100">
		<circle cx="50" cy="50" r="40" fill="none" stroke="currentColor" stroke-width="2" />
		<circle cx="50" cy="50" r="30" fill="none" stroke="currentColor" stroke-width="1" />
		<circle cx="50" cy="50" r="20" fill="none" stroke="currentColor" stroke-width="1" />
	</svg>
</div>

<style>
	.geometria {
		width: 100px;
		height: 100px;
		margin: 0 auto;
	}
	
	.pulsante {
		animation: pulso 2s infinite;
	}
	
	@keyframes pulso {
		0%, 100% { opacity: 1; transform: scale(1); }
		50% { opacity: 0.7; transform: scale(1.05); }
	}
</style>
EOF

cd ../../../../..
```

### 3.7 Páginas

```bash
mkdir -p src/routes/{estado-cero,espejo-diario}

# Página principal
nano src/routes/+page.svelte           # Archivo 43

# Estado Cero
nano src/routes/estado-cero/+page.svelte    # Archivo 44

# Espejo Diario
nano src/routes/espejo-diario/+page.svelte  # Archivo 45
```

### 3.8 Layout Base

```bash
cat > src/routes/+layout.svelte << 'EOF'
<script>
	import '../app.css';
</script>

<slot />
EOF
```

### 3.9 Iniciar Frontend

```bash
pnpm dev
```

Deberías ver:
```
VITE v5.0.8  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

## 🧪 FASE 4: TESTING Y LAUNCH (30 min)

### 4.1 Verificar Sistema Completo

Con **3 terminales abiertas**:

**Terminal 1 - Backend:**
```bash
cd campo-sagrado/backend
source venv/bin/activate
python api/main.py
```

**Terminal 2 - Frontend:**
```bash
cd campo-sagrado/frontend
pnpm dev
```

**Terminal 3 - Tests:**
```bash
cd campo-sagrado/backend
source venv/bin/activate
python scripts/test_sistema.py
```

### 4.2 Abrir en Navegador

http://localhost:5173

Deberías ver el dashboard con:
- 🕌 Campo Sagrado del Entrelazador
- Widget de próximo Estado Cero
- Navegación a Espejo Diario

### 4.3 Primer Estado Cero Real

**Espera al próximo tiempo litúrgico** (o simula en desarrollo):

1. Click en "Iniciar Estado Cero" cuando esté disponible
2. Verás el contexto completo recopilado
3. Responde las 6 preguntas binarias
4. Chat clarificador para definir acción
5. Finaliza → se documenta en Obsidian

### 4.4 Configurar Vault de Obsidian

```bash
# Crear estructura
mkdir -p ~/Documents/CampoSagrado/{00-Pilares,10-Dominios,20-Proyectos,30-Recursos,40-Journal,50-Conversaciones-IA}

# Abrir Obsidian
# File → Open Vault → ~/Documents/CampoSagrado
```

### 4.5 Script de Inicio Automático

```bash
cd campo-sagrado/scripts

cat > iniciar-sistema.sh << 'EOF'
#!/bin/bash

echo "🚀 Iniciando Campo Sagrado..."

trap 'kill $(jobs -p) 2>/dev/null' EXIT

# Backend
cd backend
source venv/bin/activate
python api/main.py &
cd ..

# Frontend
cd frontend
pnpm dev &
cd ..

# Agentes (opcional)
# cd backend
# python scripts/start_agentes.py &
# cd ..

echo "✨ Sistema iniciado"
echo "   Backend: http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo ""
echo "Ctrl+C para detener"

wait
EOF

chmod +x iniciar-sistema.sh
```

Ahora puedes iniciar todo con:
```bash
./scripts/iniciar-sistema.sh
```

---

## 📊 VERIFICACIÓN FINAL

### Checklist de Funcionalidades

- [ ] ✅ Backend responde en http://localhost:8000
- [ ] ✅ Frontend carga en http://localhost:5173
- [ ] ✅ Dashboard muestra próximo Estado Cero
- [ ] ✅ Tiempos litúrgicos calculados correctamente
- [ ] ✅ Estado Cero se puede iniciar en ventana correcta
- [ ] ✅ Preguntas binarias se generan con Claude
- [ ] ✅ Chat clarificador funciona
- [ ] ✅ Documentos se crean en Obsidian
- [ ] ✅ No-negociables se trackean
- [ ] ✅ Espejo Diario muestra plan

### Tests Manuales

1. **Test Tiempos:**
   ```bash
   cd backend
   python scripts/calcular_tiempos.py
   ```
   ✅ Debe mostrar 5 tiempos de hoy

2. **Test API:**
   ```bash
   curl http://localhost:8000/api/health
   ```
   ✅ Debe retornar JSON con próximo Estado Cero

3. **Test Frontend:**
   - Abre http://localhost:5173
   - Verifica que carga sin errores en consola
   - Click en cada sección

4. **Test Estado Cero Completo:**
   - Espera momento litúrgico
   - Inicia consulta
   - Completa todo el flujo
   - Verifica documento en Obsidian

---

## 🎓 SIGUIENTES PASOS

### Uso Diario

1. **Cada día:**
   - Inicia sistema: `./scripts/iniciar-sistema.sh`
   - Realiza 5 Estados Cero en ventanas litúrgicas
   - Revisa Espejo Diario
   - Al final del día: reporte automático en Maghrib

2. **Cada semana:**
   - Revisa vista semanal
   - Observa patrones de no-negociables
   - Ajusta según aprendizajes

3. **Cada mes:**
   - Revisa progreso mensual
   - Actualiza intenciones
   - Celebra lo manifestado

### Evolución del Sistema

**Prioridad Alta (próximas 2 semanas):**
- Vista Semanal completa
- Vista Anual con 13 meses
- Integración real con biométricos (Oura/Whoop)
- Dashboard de mantenimiento

**Prioridad Media (próximo mes):**
- Integración Anytype completa
- Sistema de capturas con propósito
- Evolución del sistema mediante insights
- Visualización avanzada de jornada caos

**Prioridad Baja (largo plazo):**
- App móvil
- Sincronización en la nube
- Comunidad de Entrelazadores
- Plantillas personalizables

---

## 🆘 TROUBLESHOOTING

### Error: "Module not found"
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
pnpm install
```

### Error: "ANTHROPIC_API_KEY not set"
```bash
nano backend/.env
# Agrega: ANTHROPIC_API_KEY=tu_key_real
```

### Error: "Port already in use"
```bash
# Matar procesos
lsof -ti:8000 | xargs kill
lsof -ti:5173 | xargs kill
```

### Base de datos corrupta
```bash
cd backend
rm ../storage/organismo.db
python scripts/init_db.py
```

### Frontend no conecta con Backend
```bash
# Verificar proxy en vite.config.ts
# Verificar que backend esté en puerto 8000
curl http://localhost:8000/api/health
```

---

## 📞 SOPORTE

Si encuentras problemas:
1. Revisa logs en consola
2. Verifica que todos los servicios estén corriendo
3. Consulta documentación de Anthropic Claude
4. Revisa issues en dependencias (FastAPI, SvelteKit)

---

## 🙏 CONCLUSIÓN

Has construido un sistema completo y funcional que:

✅ Integra 5 tiempos litúrgicos diarios  
✅ Facilita consulta sacral profunda  
✅ Orquesta tu jornada con inteligencia  
✅ Documenta automáticamente tu viaje  
✅ Respeta tu autoridad sacral  
✅ Opera al borde del caos con estructura sagrada  

**El Campo Sagrado ahora vive.**

Que te sirva bien en tu camino como Entrelazador.

🕌 ✨

---

*Última actualización: 2025-01-08*
*Versión: 1.0.0-MVP*
