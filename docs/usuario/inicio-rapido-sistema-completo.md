# 🚀 Inicio Rápido - Sistema Organismo Completo

## Pre-requisitos

✅ Python 3.11+ instalado  
✅ Node.js 20+ instalado  
✅ Obsidian instalado (descarga desde obsidian.md)

---

## Paso 1: Configurar Backend

```bash
cd backend

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias (si no están instaladas)
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Edita .env con tu ubicación (LAT, LON, TIMEZONE)

# Inicializar estructura de Obsidian
python scripts/setup_vault_structure.py
# Responde 's' para crear la estructura
```

**Resultado:** Se creará `~/Documents/CampoSagrado` con toda la estructura fractal.

---

## Paso 2: Configurar Frontend

```bash
cd campo-sagrado-nextjs

# Instalar dependencias
npm install

# El frontend ya está listo!
```

---

## Paso 3: Iniciar el Sistema

### Terminal 1: Backend

```bash
cd backend
source venv/bin/activate
python run.py
```

Deberías ver:
```
✅ Variables de entorno cargadas
✅ Middleware de seguridad activado
✅ Router Estado Cero Ultra Simple cargado correctamente
✅ Router Sistema Entrelazamiento cargado correctamente
🕌 Iniciando Campo Sagrado Backend...
🚀 Servidor iniciando en http://localhost:8000
```

### Terminal 2: Frontend

```bash
cd campo-sagrado-nextjs
npm run dev
```

Deberías ver:
```
✓ Ready in 2.5s
○ Local: http://localhost:3000
```

---

## Paso 4: Usar el Sistema

### 4.1 Completar tu Primer Estado Cero

1. Abre `http://localhost:3000`
2. Click en **"Entrar al Estado Cero"**
3. Escribe tu **intención** (hoja en blanco)
4. Responde las **3 preguntas binarias** (swipe izquierda/derecha)
5. Escribe tu **reflexión** (hoja en blanco)
6. Click en **"Finalizar Estado Cero"**

**✨ El sistema:**
- Calculará tu tendencia (expansión/contracción)
- Identificará dominios activos (biológico, espiritual, etc.)
- Archivará en Obsidian con estructura fractal
- Registrará el evento en audit trail

### 4.2 Ver tu Estado Cero en Obsidian

1. Abre Obsidian
2. Click en "Open folder as vault"
3. Selecciona `~/Documents/CampoSagrado`
4. Navega según el momento:
   - Fajr/Isha → `10_Biologia_Ritmos/Estados_Cero/`
   - Dhuhr → `50_Proyecto_Economia/Estados_Cero/`
   - Asr → `20_Mente_Aprendizaje/Estados_Cero/`
   - Maghrib → `30_Alma_Proposito/Estados_Cero/`

### 4.3 Generar tu Primer Espejo Diario

**Después de completar al menos 1 Estado Cero:**

1. Abre `http://localhost:3000`
2. Click en **"🪞 Espejo Diario"**
3. Click en **"✨ Generar Nuevo"**

**✨ El sistema generará:**
- Visualización ASCII del flujo del día
- Narrativa con punto alto/bajo de energía
- Transiciones significativas
- Estado de dominios
- Entrelazamientos detectados

### 4.4 Ver Audit Trail

1. En Obsidian, navega a:
   ```
   00_System/Audit_Trail/2025-10-15.md
   ```

2. Verás TODOS los eventos del día:
   ```markdown
   | Timestamp | Tipo | Origen | Estado | Duración | Metadata |
   |-----------|------|--------|--------|----------|----------|
   | 13:22:01.345 | estado_cero_iniciado | user_request | success | 15ms | {...} |
   | 13:25:33.789 | estado_cero_finalizado | user_request | success | 234ms | {...} |
   ```

---

## Paso 5: Configurar Obsidian (Recomendado)

### Plugins Esenciales

1. **Dataview** - Queries dinámicas
   - Settings → Community plugins → Browse
   - Buscar "Dataview" → Install → Enable

2. **Templater** - Automatización
   - Settings → Community plugins → Browse
   - Buscar "Templater" → Install → Enable

3. **obsidian-git** - Version control
   - Settings → Community plugins → Browse
   - Buscar "Obsidian Git" → Install → Enable

4. **Excalidraw** - Diagramas
   - Settings → Community plugins → Browse
   - Buscar "Excalidraw" → Install → Enable

### Tema Recomendado

- **Minimal** o **Things** para estética limpia

---

## Verificar que Todo Funciona

### Test 1: Backend

```bash
curl http://localhost:8000/api/estado-cero/test
```

Debería responder:
```json
{
  "status": "ok",
  "mensaje": "Estado Cero Simple funcionando",
  "timestamp": "2025-10-15T13:22:01.345678"
}
```

### Test 2: Sistema de Entrelazamiento

```bash
curl http://localhost:8000/api/sistema/test
```

Debería responder:
```json
{
  "status": "ok",
  "sistema": "entrelazamiento",
  "vault_path": "/Users/tu-usuario/Documents/CampoSagrado"
}
```

### Test 3: Frontend

Abre `http://localhost:3000` - Deberías ver:
- 🕌 Logo con estrellas animadas
- "Campo Sagrado"
- Momento litúrgico actual
- Botón "Entrar al Estado Cero"
- Botón "🪞 Espejo Diario"

---

## Troubleshooting

### ❌ Error: Port 8000 already in use

```bash
# Encontrar el proceso
lsof -i :8000

# Matar el proceso
kill -9 <PID>

# O usar el script de limpieza
./backend/scripts/kill_port_8000.sh
```

### ❌ Error: Module not found

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### ❌ Error: Obsidian vault no existe

```bash
cd backend
source venv/bin/activate
python scripts/setup_vault_structure.py
```

### ❌ Error: Cannot find module 'react-markdown'

```bash
cd campo-sagrado-nextjs
npm install react-markdown
```

---

## Próximos Pasos

Una vez que el sistema esté funcionando:

1. **Completar 5 Estados Cero en un día** (uno por momento litúrgico)
2. **Generar tu primer Espejo Diario completo**
3. **Explorar la estructura de Obsidian**
4. **Ver el Audit Trail acumulado**
5. **Leer `SISTEMA_ORGANISMO_COMPLETO.md` para detalles técnicos**

---

## Contacto y Soporte

Si encuentras algún error o tienes preguntas:

1. Revisa `SISTEMA_ORGANISMO_COMPLETO.md`
2. Revisa el audit trail en Obsidian
3. Revisa logs en `backend/backend.log`

---

**🕌 Sistema operando al borde del caos - 40% capacidad sin asignar**

*Configuración 0.01% - Elite*

*إن شاء الله - Si Dios quiere*

