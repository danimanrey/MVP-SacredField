# 🏗️ ARQUITECTURA TÉCNICA - CAMPO SAGRADO

**Versión**: 0.1.0-mvp (SvelteKit)  
**Próxima versión**: 0.2.0-alpha (Next.js + R3F)  
**Fecha**: 9 de Octubre de 2025

---

## 📐 ARQUITECTURA GENERAL

```
┌─────────────────────────────────────────────────────────────┐
│                        USUARIO                              │
│                          ↓↑                                 │
│              http://localhost:5173                          │
└─────────────────────────────────────────────────────────────┘
                           ↓↑
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (SvelteKit)                     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Espejo     │  │   Estados    │  │    Vistas    │    │
│  │   Diario     │  │     Cero     │  │   Temporales │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │     7        │  │   Ley de     │  │  Geometría   │    │
│  │ Dimensiones  │  │   la Octava  │  │   Sagrada    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           ↓↑
                    Fetch API (REST)
                           ↓↑
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI + Python)                 │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                    API LAYER                          │ │
│  │                                                       │ │
│  │  /api/estado-cero/*    /api/espejo-diario/*         │ │
│  │  /api/octavas/*        /api/manifestaciones/*        │ │
│  │  /api/vista-semanal    /api/contexto-temporal        │ │
│  │  /api/guardian/*       /api/orquestador/*            │ │
│  └──────────────────────────────────────────────────────┘ │
│                           ↓↑                               │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                  AGENTES LAYER                        │ │
│  │                                                       │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │ │
│  │  │ Estado   │ │Entrelaz  │ │Orquest   │ │Documen │ │ │
│  │  │  Cero    │ │  ador    │ │ ador     │ │ tador  │ │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └────────┘ │ │
│  │       ↓↑            ↓↑           ↓↑          ↓↑      │ │
│  │  ┌──────────────────────────────────────────────┐   │ │
│  │  │              Guardián                         │   │ │
│  │  └──────────────────────────────────────────────┘   │ │
│  └──────────────────────────────────────────────────────┘ │
│                           ↓↑                               │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                 SERVICES LAYER                        │ │
│  │                                                       │ │
│  │  - Motor Prisma (personalización)                    │ │
│  │  - Gestor Octavas (Ley del 7)                        │ │
│  │  - Calendario Hijri (12 meses)                       │ │
│  │  - Tiempos Litúrgicos (PrayTimes)                    │ │
│  │  - Claude Client (IA)                                │ │
│  │  - Metabolizador Metadatos (aprendizaje)             │ │
│  │  - Sumario Contexto (compresión)                     │ │
│  └──────────────────────────────────────────────────────┘ │
│                           ↓↑                               │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                   DATA LAYER                          │ │
│  │                                                       │ │
│  │  - SQLAlchemy ORM                                     │ │
│  │  - Pydantic Models                                    │ │
│  │  - SQLite Database (storage/organismo.db)            │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ↓↑
┌─────────────────────────────────────────────────────────────┐
│                INTEGRACIONES EXTERNAS                       │
│                                                             │
│  - Anthropic Claude API (IA generativa)                    │
│  - Obsidian Vault (documentación automática)               │
│  - Google Calendar (próximamente)                          │
│  - Anytype (preparado)                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 TECNOLOGÍAS Y VERSIONES

### Backend (Python 3.11)

```txt
fastapi==0.111.0           # Framework web
uvicorn==0.30.1            # Servidor ASGI
SQLAlchemy==2.0.32         # ORM
pydantic==2.8.2            # Validación de datos
anthropic==0.34.0          # Claude API
praytimes==2.1.0           # Cálculos astronómicos
hijri-converter==2.3.2     # Calendario lunar
pytz==2024.1               # Timezones
```

### Frontend (SvelteKit 5)

```json
{
  "svelte": "^5.0.0",
  "sveltekit": "^2.0.0",
  "typescript": "^5.0.0",
  "vite": "^5.0.0"
}
```

---

## 📦 ESTRUCTURA DE ARCHIVOS

### Backend

```
backend/
├── agentes/                    # Los 4 agentes + Guardián
│   ├── estado_cero.py         # Consultas sacrales
│   ├── entrelazador.py        # Estructura semanal
│   ├── orquestador.py         # Plan diario
│   ├── documentador.py        # Integración Obsidian
│   └── guardian.py            # Monitoreo
├── api/                        # Endpoints REST
│   ├── main.py                # App principal
│   ├── estado_cero.py
│   ├── espejo_diario.py
│   ├── vistas_temporales.py
│   ├── octavas.py             # Ley de la Octava
│   └── manifestaciones.py     # 7 Dimensiones
├── models/                     # Modelos de datos
│   ├── schemas.py             # Schemas Pydantic
│   ├── database.py            # Models SQLAlchemy
│   ├── prisma_personal.py     # Configuración usuario
│   └── ley_octava.py          # Sistema de octavas
├── services/                   # Lógica de negocio
│   ├── calendario_hijri.py    # 12 meses lunares
│   ├── tiempos_liturgicos.py  # Cálculos astronómicos
│   ├── motor_prisma.py        # Personalización
│   ├── gestor_octavas.py      # Ley del 7
│   ├── claude_client.py       # IA
│   ├── contexto.py            # Recopilación contexto
│   ├── sumario_contexto.py    # Compresión inteligente
│   └── metabolizador_metadatos.py  # Aprendizaje patrones
├── integraciones/
│   ├── obsidian.py            # Vault integration
│   └── anytype.py             # Preparado
├── scripts/
│   ├── configurar_prisma.py   # CLI interactivo
│   └── init_db.py             # Inicializar DB
├── config.py                   # Configuración central
├── requirements.txt
└── run.py                      # Entry point
```

### Frontend

```
frontend/
├── src/
│   ├── routes/                         # Páginas
│   │   ├── +layout.svelte             # Layout principal
│   │   ├── +page.svelte               # Home
│   │   ├── espejo-diario/
│   │   ├── estado-cero/
│   │   ├── dimensiones/
│   │   ├── ley-octava/
│   │   ├── vista-semanal/
│   │   └── vista-anual/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── EspejoDiario/
│   │   │   │   ├── EspejoDinamico.svelte
│   │   │   │   ├── JornadaCaos.svelte
│   │   │   │   └── NoNegociables.svelte
│   │   │   ├── EstadoCero/
│   │   │   │   ├── ConsultaSacral.svelte
│   │   │   │   ├── ChatClarificador.svelte
│   │   │   │   └── VerificacionMomento.svelte
│   │   │   ├── Vistas/
│   │   │   │   ├── VistaSemanal.svelte
│   │   │   │   └── VistaAnual.svelte
│   │   │   ├── Octavas/
│   │   │   │   ├── DashboardOctavas.svelte
│   │   │   │   └── EspiralOctavas.svelte
│   │   │   ├── Dimensiones/
│   │   │   │   └── VistaDimensiones.svelte
│   │   │   └── Shared/
│   │   │       ├── Navegacion.svelte
│   │   │       ├── GeometriaSagrada.svelte
│   │   │       └── TiempoLiturgico.svelte
│   │   ├── api/
│   │   │   └── client.ts              # Cliente API
│   │   └── stores/
│   │       ├── estadoCero.ts
│   │       ├── jornada.ts
│   │       └── tiempo.ts
│   ├── app.css
│   └── app.html
├── package.json
├── svelte.config.js
└── vite.config.ts
```

---

## 🔄 FLUJO DE DATOS

### 1. Estado Cero

```
Usuario → Frontend → POST /api/estado-cero/iniciar
                       ↓
              AgenteEstadoCero
                       ↓
              1. Verificar ventana litúrgica
              2. Recopilar contexto (Calendario, Tiempos, Prisma)
              3. Generar preguntas con Claude (dinámicas 1-20)
                       ↓
              ← Retorna preguntas
                       ↓
Usuario responde → POST /api/estado-cero/responder
                       ↓
              AgenteEstadoCero
                       ↓
              1. Analizar respuestas
              2. Sintetizar dirección (Claude Haiku)
              3. Generar acción concreta
              4. Actualizar Espejo Diario
                       ↓
              AgenteDocumentador
                       ↓
              Guardar en Obsidian Vault
                       ↓
              ← Retorna dirección + acción
```

### 2. Espejo Diario

```
Usuario → GET /api/espejo-diario/hoy
             ↓
     ¿Existe espejo hoy?
             ↓
        No → Generar
             ↓
     AgenteEntrelazador
             ↓
     1. Obtener estructura base (anclas + no-neg)
     2. Consultar Prisma (horarios, duración flujo)
     3. Obtener contexto temporal (mes Hijri, día semana)
             ↓
     AgenteOrquestador
             ↓
     1. Generar plan coordinado con Claude
     2. Asignar bloques profundos
     3. Respetar espacio libre dinámico (25-60%)
     4. Priorizar según dimensión del día
             ↓
     ← Retorna JornadaAlBordeCaos
             ↓
     Se actualiza con cada Estado Cero
```

### 3. Objetivo en Octava

```
Usuario → POST /api/octavas/crear-objetivo
             ↓
     GestorOctavas
             ↓
     1. Determinar nota fundamental (según dimensión)
     2. Generar 7 armónicos (todas las dimensiones)
     3. Crear plan semanal de 7 fases
     4. Programar 2 shocks conscientes
             ↓
     ← Retorna ObjetivoOctava
             ↓
     Cada día:
     GET /api/octavas/dimension-hoy
             ↓
     Sistema indica qué dimensión priorizar
             ↓
     Entrelazador ajusta plan según nota del día
```

---

## 🗄️ MODELO DE DATOS

### Tablas Principales (SQLite)

```sql
-- Estados Cero
CREATE TABLE estados_cero (
    id TEXT PRIMARY KEY,
    fecha DATETIME,
    momento TEXT,  -- fajr, dhuhr, asr, maghrib, isha
    contexto TEXT,  -- JSON
    preguntas TEXT,  -- JSON
    respuestas TEXT,  -- JSON
    direccion TEXT,
    accion TEXT,  -- JSON
    chat TEXT,  -- JSON
    completado BOOLEAN
);

-- Sesiones de trabajo
CREATE TABLE sesiones (
    id TEXT PRIMARY KEY,
    fecha DATE,
    inicio DATETIME,
    fin DATETIME,
    duracion_minutos INTEGER,
    rol TEXT,  -- deep_work, shallow, meeting
    calidad_flujo INTEGER,  -- 1-5
    dimension TEXT,
    notas TEXT
);

-- No-negociables tracking
CREATE TABLE no_negociables_tracking (
    id TEXT PRIMARY KEY,
    fecha DATE,
    no_negociable_id TEXT,
    completado BOOLEAN,
    hora_completado DATETIME
);

-- Biometría
CREATE TABLE biometria (
    id TEXT PRIMARY KEY,
    fecha DATE,
    hrv FLOAT,
    calidad_sueno INTEGER,
    energia_despertar INTEGER,
    luz_solar_am BOOLEAN,
    ejercicio BOOLEAN
);
```

### Modelos Pydantic Clave

```python
# Contexto Completo
class ContextoCompleto(BaseModel):
    temporal: ContextoTemporal
    biologico: ContextoBiologico
    financiero: ContextoFinanciero
    conocimiento: ContextoConocimiento
    tiempo_disponible_hoy: int

# Estado Cero
class EstadoCeroCompleto(BaseModel):
    id: str
    fecha: datetime
    momento: MomentoLiturgico
    contexto: ContextoCompleto
    preguntas: List[PreguntaBinaria]
    respuestas: List[RespuestaSacral]
    direccion: str
    accion: AccionConcreta
    chat: List[MensajeChat]

# Jornada al Borde del Caos
class JornadaAlBordeCaos(BaseModel):
    fecha: date
    estructura: EstructuraDia
    bloques_asignados: List[BloqueAsignado]
    espacio_libre_minutos: int
    espacio_libre_porcentaje: float
    coherencia: float

# Objetivo Octava
class ObjetivoOctava(BaseModel):
    id: str
    nombre: str
    nota_fundamental: Nota
    dimension_primaria: DimensionOctava
    armonicos: Dict[DimensionOctava, Armonico]
    plan_octava: Dict[DiaSemanaOctava, FaseSemanal]
    shocks: List[ShockConsciente]
    octava_actual: int
    nivel_frecuencia: float
```

---

## 🎯 COMPONENTES CLAVE

### 1. Motor del Prisma

**Propósito**: Traduce tu configuración única en parámetros operativos.

**Input**: `PrismaPersonal` (config/prisma_personal.json)

**Output**: Configuraciones específicas para cada agente

```python
class MotorPrisma:
    def configurar_estado_cero() -> Dict:
        return {
            "numero_preguntas": calcular_dinamico(),  # 1-20
            "estilo_preguntas": adaptar_a_personalidad(),
            "categorias_prioritarias": desde_manifestaciones()
        }
    
    def configurar_entrelazador() -> Dict:
        return {
            "duracion_bloque": usuario.duracion_optima_flujo,
            "horarios_pico": usuario.mejor_momento_dia,
            "espacio_libre": calcular_dinamico()  # 25-60%
        }
```

### 2. Gestor de Octavas

**Propósito**: Implementa la Ley del Siete en objetivos.

**Features**:
- Crea objetivos con 7 armónicos
- Tracking semanal por nota
- Detecta shocks pendientes
- Calcula coherencia armónica
- Evoluciona en espiral ascendente

**API Principal**:
```python
gestor.crear_objetivo_octava(...)
gestor.obtener_estado_octava_actual(objetivo_id, fecha)
gestor.aplicar_shock_consciente(objetivo_id, tipo_shock, notas)
gestor.analizar_armonicos(objetivo_id)
gestor.visualizar_espiral_octavas(objetivo_id)
```

### 3. Calculador Tiempos Litúrgicos

**Propósito**: Calcula con precisión astronómica los 5 tiempos de rezo.

**Método**: `PrayTimes` con coordenadas exactas (San Sebastián de los Reyes)

**Precisión**: Al minuto

```python
calculador = CalculadorTiemposLiturgicos(
    latitud=40.5472,  # 40°32'50"N
    longitud=-3.6228,  # 3°37'22"W
    timezone="Europe/Madrid"
)

tiempos = calculador.calcular_tiempos_hoy()
# → Fajr: 06:46-08:19
# → Dhuhr: 14:02-17:13
# → Asr: 17:13-19:43
# → Maghrib: 19:43-21:09
# → Isha: 21:09-01:25
```

### 4. Calendario Hijri

**Propósito**: Calendario lunar islámico auténtico con profundidad mística.

**Librería**: `hijri-converter` (conversión precisa)

**Features**:
- 12 meses lunares REALES
- Enseñanzas místicas sufíes por mes
- Ayat del Corán relacionadas
- 4 meses sagrados identificados
- Propósito de cada día de la semana

```python
calendario = CalendarioHijri()

mes_actual = calendario.obtener_mes_actual()
# → nombre: "Rabi' al-Thani"
# → enseñanza: "Tu existencia es acto creativo..."
# → ayat: "Corán 55:1-4"

dia_hoy = calendario.obtener_dia_semana()
# → nombre: "Jueves"
# → proposito: "Expansión y sabiduría..."
# → alerta_sesgo: "Exceso de optimismo sin realismo"
```

---

## 🔌 API REFERENCE RESUMIDA

### Estado Cero
```
POST /api/estado-cero/iniciar
POST /api/estado-cero/responder
POST /api/estado-cero/chat
POST /api/estado-cero/completar
GET  /api/estado-cero/ventanas-perdidas
```

### Espejo Diario
```
GET  /api/espejo-diario/hoy
POST /api/espejo-diario/actualizar
GET  /api/espejo-diario/estados-cero-hoy
```

### Vistas Temporales
```
GET /api/contexto-temporal
GET /api/vista-semanal
GET /api/vista-mensual
GET /api/vista-anual
GET /api/dias-semana
GET /api/meses-hijri
```

### Ley de la Octava
```
GET  /api/octavas/correspondencias
GET  /api/octavas/dimension-hoy
POST /api/octavas/crear-objetivo
GET  /api/octavas/objetivo/{id}
GET  /api/octavas/objetivo/{id}/estado
GET  /api/octavas/objetivo/{id}/armonicos
POST /api/octavas/objetivo/{id}/shock
GET  /api/octavas/shocks-hoy
GET  /api/octavas/objetivo/{id}/espiral
```

### Guardián
```
GET  /api/guardian/salud-sistema
GET  /api/guardian/patrones
GET  /api/guardian/alertas
GET  /api/guardian/estado-general
POST /api/guardian/reporte-diario
```

---

## ⚡ PERFORMANCE Y OPTIMIZACIÓN

### Backend

**Optimizaciones actuales**:
- Claude Haiku para tareas simples (92% menos costo)
- Compresión de prompts (75% reducción)
- Cache de cálculos astronómicos (24h)
- Sumario incremental de contexto

**Métricas**:
- Latencia promedio: <200ms
- Estado Cero completo: <5s
- Costo por Estado Cero: ~$0.02

### Frontend

**Optimizaciones actuales**:
- CSS nativo (sin framework, bundle pequeño)
- Lazy loading de componentes
- Fetch solo cuando necesario
- Revalidación cada 5 minutos

**Métricas**:
- Bundle size: ~80 KB
- First Contentful Paint: <1s
- Time to Interactive: <2s

---

## 🔒 SEGURIDAD Y PRIVACIDAD

### Datos Sensibles:
- Todos los Estados Cero se guardan localmente (SQLite)
- Claude solo recibe contexto mínimo (sin info personal)
- Obsidian vault es local
- No hay tracking de terceros

### Configuración:
```python
# backend/.env
ANTHROPIC_API_KEY=sk-...
OBSIDIAN_VAULT_PATH=/ruta/a/vault
LATITUD=40.5472
LONGITUD=-3.6228
```

---

## 🚀 DEPLOYMENT

### Desarrollo

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python run.py

# Terminal 2: Frontend
cd frontend
npm run dev

# Acceso: http://localhost:5173
```

### Producción (próximamente)

**Backend**: Railway / Render / DigitalOcean  
**Frontend**: Vercel / Netlify  
**Base de datos**: PostgreSQL (migración desde SQLite)

---

## 📊 MÉTRICAS DEL SISTEMA

### Código:
- **Backend**: ~5000 líneas Python
- **Frontend**: ~3000 líneas Svelte/TS
- **Total**: ~8000 líneas

### Endpoints:
- **Total**: 30+ endpoints
- **Cobertura**: Completa

### Componentes:
- **Backend**: 15 archivos principales
- **Frontend**: 15+ componentes
- **Documentación**: 5 archivos completos

---

## 🔮 PRÓXIMA VERSIÓN: 0.2.0-alpha (Next.js)

### Cambios Mayores:
- ✅ Frontend: Next.js 14 + React 18
- ✅ 3D: React Three Fiber (experiencia inmersiva)
- ✅ Animaciones: Framer Motion + GSAP
- ✅ UI: Shadcn/ui (componentes beautiful)
- ✅ Interfaz única: Scroll continuo sin navegación
- ✅ Audio: Tone.js (frecuencias generativas)

### Sin Cambios:
- ✅ Backend Python/FastAPI (se mantiene)
- ✅ Toda la lógica de agentes (se mantiene)
- ✅ Filosofía y principios (se mantiene)

---

**🕌 Documentación viva. Se actualiza con el organismo.**

**مَا شَاءَ ٱللَّٰهُ**

