# 🗺️ Mapa Visual - Arquitectura del Organismo

---

## 🌊 **El Organismo Completo**

```
                    👤 USUARIO
                       │
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ Estado  │   │ Espejo  │   │Dashboard│
   │  Cero   │   │ Sagrado │   │ Personal│
   └────┬────┘   └────┬────┘   └────┬────┘
        │             │              │
        │      FRONTEND (SvelteKit)  │
        └─────────────┼──────────────┘
                      │ REST API
        ┌─────────────┼──────────────┐
        │      BACKEND (FastAPI)     │
        │                            │
        │   ┌─────────────────┐      │
        │   │    MEDIATOR     │      │
        │   │  (Coordinador)  │      │
        │   └────────┬────────┘      │
        │            │               │
        │   ┌────────┴────────┐      │
        │   │                 │      │
        │   ▼                 ▼      │
        │ ┌───────┐  ┌──────────┐   │
        │ │Estado │  │Orquestador│  │
        │ │ Cero  │  │           │  │
        │ └───┬───┘  └─────┬────┘   │
        │     │            │        │
        │     ▼            ▼        │
        │ ┌────────────────────┐   │
        │ │   DOCUMENTADOR     │   │
        │ └─────────┬──────────┘   │
        │           │              │
        │     ┌─────┼─────┐        │
        │     ▼     ▼     ▼        │
        │  ┌────┐ ┌────┐ ┌────┐   │
        │  │ DB │ │Obs.│ │Any-│   │
        │  │    │ │    │ │type│   │
        │  └────┘ └────┘ └────┘   │
        └─────────────────────────┘

        SQLite  Obsidian  Anytype
                (ahora)   (v0.2.0)
```

---

## 🎭 **Los 4 Agentes - Vista Detallada**

### **1️⃣ Agente Estado Cero**

```
INPUT:
┌─────────────────────────────────────┐
│ • Momento litúrgico (fajr/dhuhr...) │
│ • Contexto temporal                 │
│ • Contexto biológico (energía 1-5)  │
│ • Contexto financiero (runway)      │
│ • Contexto conocimiento (capturas)  │
│ • Perfil personal (opcional)        │
└─────────────────────────────────────┘
              │
              ▼
      ┌───────────────┐
      │ FORMULAR      │
      │ 3 PREGUNTAS   │
      │ BINARIAS      │
      └───────┬───────┘
              │
              ▼
      ┌───────────────┐
      │ USUARIO       │
      │ RESPONDE      │
      │ (expansión/   │
      │ contracción)  │
      └───────┬───────┘
              │
              ▼
      ┌───────────────┐
      │ SINTETIZAR    │
      │ DIRECCIÓN     │
      │ EMERGENTE     │
      └───────┬───────┘
              │
              ▼
      ┌───────────────┐
      │ DEFINIR       │
      │ ACCIÓN        │
      │ CONCRETA      │
      └───────┬───────┘
              │
              ▼
OUTPUT:
┌─────────────────────────────────────┐
│ • EstadoCeroCompleto                │
│   - 3 preguntas + respuestas        │
│   - Dirección emergente             │
│   - Acción concreta                 │
│   - Chat clarificación (opcional)   │
└─────────────────────────────────────┘
```

**Frecuencia**: 5x/día (fajr, dhuhr, asr, maghrib, isha)  
**Duración**: ~2-3 minutos  
**Documentación**: → Obsidian automático

---

### **2️⃣ Agente Orquestador**

```
INPUT:
┌─────────────────────────────────────┐
│ • Acción del Estado Cero            │
│ • Contexto completo del día         │
│ • Energía disponible                │
│ • Perfil personal                   │
└─────────────────────────────────────┘
              │
              ▼
      ┌───────────────┐
      │ GENERAR       │
      │ BLOQUES       │
      │ SUGERIDOS     │
      └───────┬───────┘
              │
              ▼
      ┌───────────────┐
      │ 40% ESPACIO   │
      │ EMERGENCIA    │
      └───────┬───────┘
              │
              ▼
      ┌───────────────┐
      │ DEFINIR       │
      │ NO-           │
      │ NEGOCIABLES   │
      └───────┬───────┘
              │
              ▼
      ┌───────────────┐
      │ PUNTOS DE     │
      │ DECISIÓN      │
      └───────┬───────┘
              │
              ▼
OUTPUT:
┌─────────────────────────────────────┐
│ • JornadaAlBordeCaos                │
│   - Bloques (flexibles/anclados)    │
│   - 40% vacío respetado             │
│   - No-negociables (bio/espir/fin)  │
│   - Puntos de decisión              │
└─────────────────────────────────────┘
```

**Trigger**: Después del primer Estado Cero del día  
**Actualización**: Bajo demanda (ajustes)  
**Documentación**: → Obsidian automático

---

### **3️⃣ Agente Guardian** (v0.1.3)

```
INPUT:
┌─────────────────────────────────────┐
│ • Plan del día actual               │
│ • Estado de no-negociables          │
│ • Hora actual                       │
└─────────────────────────────────────┘
              │
              ▼
      ┌───────────────┐
      │ MONITOREO     │
      │ CONTINUO      │
      │ (cada 30 min) │
      └───────┬───────┘
              │
          ┌───┴───┐
          ▼       ▼
    ┌──────┐  ┌──────┐
    │¿En   │  │¿Qué  │
    │riesgo│  │falta?│
    └──┬───┘  └───┬──┘
       │          │
       ▼          ▼
    ┌──────────────┐
    │  ALERTAR     │
    │  si crítico  │
    └──────┬───────┘
           │
           ▼
      ┌─────────┐
      │ REPORTE │
      │ DIARIO  │
      │ (23:30) │
      └────┬────┘
           │
           ▼
OUTPUT:
┌─────────────────────────────────────┐
│ • Alertas en tiempo real            │
│ • Reporte diario:                   │
│   - No-negociables cumplidos        │
│   - Adherencia al plan              │
│   - Patrones observados             │
│   - Recomendaciones                 │
└─────────────────────────────────────┘
```

**Frecuencia**: 
- Monitoreo: cada 30 min
- Reporte: diario 23:30
- Alertas: inmediatas

**Documentación**: → Obsidian automático

---

### **4️⃣ Agente Documentador**

```
INPUT:
┌─────────────────────────────────────┐
│ • Estado Cero completado            │
│ • Plan de jornada generado          │
│ • Reporte del Guardian              │
│ • Cualquier evento del sistema      │
└─────────────────────────────────────┘
              │
              ▼
      ┌───────────────┐
      │ GENERAR       │
      │ MARKDOWN      │
      │ + YAML        │
      └───────┬───────┘
              │
              ▼
      ┌───────────────┐
      │ AÑADIR        │
      │ TAGS          │
      │ AUTOMÁTICOS   │
      └───────┬───────┘
              │
              ▼
      ┌───────────────┐
      │ CREAR         │
      │ BACKLINKS     │
      └───────┬───────┘
              │
              ▼
      ┌───────────────┐
      │ DETECTAR      │
      │ INSIGHTS      │
      │ (repetidos)   │
      └───────┬───────┘
              │
          ┌───┴────┐
          ▼        ▼
    ┌────────┐ ┌──────┐
    │Obsidian│ │Anytype│
    │(siempre)│ │(v0.2)│
    └────────┘ └───────┘

OUTPUT:
┌─────────────────────────────────────┐
│ • Archivos Markdown estructurados   │
│ • Tags aplicados                    │
│ • Backlinks entre documentos        │
│ • Insights destilados (Anytype)     │
└─────────────────────────────────────┘
```

**Trigger**: Automático después de cada evento  
**Frecuencia**: Continua  
**Storage**: Obsidian + Anytype (futuro)

---

## 🔄 **Flujo de un Día Típico**

```
06:00  ┌──────────────┐
FAJR   │ Estado Cero  │
       │ 3 preguntas  │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │Documentador  │
       │→ Obsidian    │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │Orquestador   │
       │Plan del día  │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │Documentador  │
       │→ Obsidian    │
       └──────┬───────┘
              │
              ▼
06:30  ┌──────────────┐
       │Usuario vive  │
       │la jornada    │
       │(Espejo       │
       │ Sagrado)     │
       └──────┬───────┘
              │
       ┌──────┴─────────┐
       ▼                ▼
  [Guardian    ]  [Puntos de  ]
  [monitorea   ]  [decisión   ]
  [cada 30 min ]  [aparecen   ]
       │                │
       ▼                ▼
  [Alerta si ]  [Usuario elige]
  [en riesgo ]  [continuar/   ]
                [cambiar      ]

13:00  ┌──────────────┐
DHUHR  │ Estado Cero  │
       │ Refinamiento │
       └──────────────┘

16:00  ┌──────────────┐
ASR    │ Estado Cero  │
       │ Completar    │
       └──────────────┘

19:00  ┌──────────────┐
MAGHRIB│ Estado Cero  │
       │ Reflexión    │
       └──────────────┘

22:00  ┌──────────────┐
ISHA   │ Estado Cero  │
       │ Integración  │
       └──────────────┘

23:30  ┌──────────────┐
       │ Guardian     │
       │ Reporte      │
       │ Diario       │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │Documentador  │
       │→ Obsidian    │
       └──────────────┘
```

---

## 📁 **Estructura de Obsidian**

```
obsidian_vault/
│
├── 50-Conversaciones-IA/
│   └── Estados-Cero/
│       └── 2025-10-08/
│           ├── fajr.md      ← Consulta matutina
│           ├── dhuhr.md     ← Refinamiento
│           ├── asr.md       ← Completar ciclos
│           ├── maghrib.md   ← Reflexión
│           └── isha.md      ← Integración
│
├── 40-Journal/
│   └── 2025-10-08/
│       ├── plan-jornada.md          ← Plan del Orquestador
│       └── reporte-guardian.md      ← Reporte diario
│
├── 30-Sesiones/
│   └── Wellness-App/
│       └── sesion-2025-10-08.md     ← Trabajo profundo
│
├── 20-Insights/
│   ├── emergentes/
│   │   └── patron-energia-matutina.md
│   └── destilados/                  ← Insights validados
│       └── ritmo-biologico-optimo.md
│
└── 10-Meta/
    └── sistema/
        └── changelog.md
```

**Tags importantes**:
- `#estado-cero`
- `#momento-{fajr|dhuhr|asr|maghrib|isha}`
- `#expansion` / `#contraccion`
- `#patron`
- `#insight`

---

## 🔗 **Comunicación entre Agentes**

### **Patrón Actual (v0.1.1)** - Acoplado ⚠️

```
┌──────────────┐
│   Endpoint   │
│ estado_cero  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│AgenteEstado  │
│    Cero      │
└──────┬───────┘
       │
       ? ← ¿Quién documenta?
       ? ← ¿Quién orquesta?
```

### **Patrón Propuesto (v0.1.2)** - Mediator ✅

```
┌──────────────┐
│   Endpoint   │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────┐
│    ORGANISMO MEDIATOR        │
│  (Coordinación Centralizada) │
└──────┬───────────────────────┘
       │
       ├─→ Estado Cero
       ├─→ Documentador
       ├─→ Orquestador
       └─→ Documentador
```

**Beneficio**: Un solo lugar para ver TODO el flujo.

---

## 🎯 **Decisiones Clave - Tabla Rápida**

| Tecnología    | Decisión | Cuándo Cambiar | Razón |
|---------------|----------|----------------|-------|
| SQLite        | ✅ Usar  | v1.0.0 (10+ users) | Simple, suficiente |
| Obsidian      | ✅ Usar  | Nunca | Perfecto para docs |
| Anytype       | ⏸️ Esperar | v0.2.0 (100+ notas) | Obsidian suficiente |
| WebSockets    | ⏸️ Esperar | v0.2.0 (Guardian activo) | Polling funciona |
| PostgreSQL    | ⏸️ Esperar | v1.0.0 (multi-user) | SQLite suficiente |
| Microservices | ❌ NO | Nunca para MVP | Over-engineering |
| Message Queue | ❌ NO | Nunca para MVP | Innecesario |
| GraphQL       | ❌ NO | Si frontend pide | REST funciona |

---

## 🚀 **Roadmap Visual**

```
v0.1.1 (ACTUAL) ✅
├─ 4 agentes definidos
├─ Obsidian funcional
├─ Colores beige
└─ Estado Cero mejorado

        ↓  (Semana 1-2)

v0.1.2 (Documentación Auto)
├─ AgenteDocumentador completo
├─ Mediator centralizado
├─ Logging estructurado
└─ Estados Cero → Obsidian 100%

        ↓  (Semana 3-4)

v0.1.3 (Guardian Activo)
├─ Scheduler funcionando
├─ Monitoreo cada 30 min
├─ Reporte diario auto
└─ Notificaciones en UI

        ↓  (Semana 5-6)

v0.1.4 (Calidad)
├─ 80%+ tests coverage
├─ CI/CD GitHub Actions
└─ Documentación completa

        ↓  (Mes 2)

v0.2.0 (Expansión)
├─ Anytype si se necesita
├─ WebSockets si Guardian lo requiere
└─ Patrones semanales avanzados
```

---

## 💡 **Reglas de Oro**

1. **Un agente a la vez**
   - No toques 2 agentes simultáneamente
   - Completa Documentador → luego Guardian

2. **Documentar antes de olvidar**
   - Decisión importante → archivo en docs/
   - Bug extraño → comentario en código

3. **Simplificar antes de añadir**
   - ¿Esto se puede hacer sin código? → no añadas código
   - ¿Esto se puede hacer con lo existente? → úsalo

4. **Validar con uso real**
   - Usa el sistema TÚ cada día
   - Si algo te molesta → arréglalo
   - Si no lo notas → no era importante

---

🕌 **El organismo respira. No lo asfixies con complejidad.** ✨

