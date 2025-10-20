# 🕌 Arquitectura de Agentes y Flujo de Integración

## 🌊 **Filosofía del Organismo**

El Campo Sagrado **no es una aplicación** - es un **organismo vivo** que respira con 4 agentes especializados que se orquestan entre sí, operando **al borde del caos** (40% espacio vacío).

---

## 🎭 **Los 4 Agentes del Sistema**

### **1. Agente Estado Cero** 🌟
**Rol**: Consulta Sacral

**¿Qué hace?**
- Formula 3 preguntas binarias basadas en contexto holístico
- Escucha la autoridad sacral del usuario (expansión/contracción)
- Sintetiza dirección emergente
- Chat clarificador para dudas

**¿Cuándo actúa?**
- 5 veces al día en momentos litúrgicos:
  - Fajr (madrugada)
  - Dhuhr (mediodía)
  - Asr (tarde)
  - Maghrib (atardecer)
  - Isha (noche)

**Input**:
- Momento litúrgico actual
- Contexto temporal (día semana, mes hijri)
- Contexto biológico (energía, luz solar, ejercicio)
- Contexto financiero (runway, urgencia)
- Contexto conocimiento (capturas, insights)
- Perfil personal (si está cargado)

**Output**:
- 3 preguntas binarias con contexto
- Respuestas sacrales (expansión/contracción + intensidad)
- Dirección emergente sintetizada
- Acción concreta tangible

**Documentación**:
→ **OBSIDIAN** en `50-Conversaciones-IA/Estados-Cero/{fecha}/{momento}.md`

---

### **2. Agente Orquestador** 🎼
**Rol**: Plan Emergente al Borde del Caos

**¿Qué hace?**
- Recibe la acción del Estado Cero
- Genera jornada con 40% espacio vacío
- Define bloques fluidos vs anclados
- Establece puntos de decisión
- Gestiona no-negociables (biológicos, espirituales, financieros)

**¿Cuándo actúa?**
- Después de cada Estado Cero completado
- Cuando el usuario solicita ajuste del plan
- En momentos de decisión (ej: ¿continuar o cambiar?)

**Input**:
- Acción concreta del Estado Cero
- Contexto temporal completo
- Energía disponible
- No-negociables personales

**Output**:
- `JornadaAlBordeCaos`:
  - Bloques sugeridos (inicio, duración, actividad, rol, energía)
  - Puntos de decisión (momento, pregunta, criterio, opciones)
  - No-negociables (tipo, ventana, prioridad)
  - 40% espacio emergencia

**Documentación**:
→ **OBSIDIAN** en `40-Journal/{fecha}/plan-jornada.md`

---

### **3. Agente Guardian** 👁️
**Rol**: Monitoreo y Reportes

**¿Qué hace?**
- Observa adherencia a no-negociables
- Detecta desviaciones del plan
- Genera reportes diarios automáticos
- Identifica patrones semanales
- Alertas ante riesgos (ej: no-negociable en peligro)

**¿Cuándo actúa?**
- Monitoreo continuo en background
- Reporte al final del día (antes de Isha)
- Reporte semanal (viernes/sábado)
- Alerta inmediata si no-negociable en riesgo

**Input**:
- Plan del día
- Estados completados de no-negociables
- Tiempo transcurrido
- Contexto actual

**Output**:
- Reporte diario:
  - Estados Cero completados
  - No-negociables cumplidos/pendientes
  - Adherencia al plan
  - Observaciones emergentes
- Reporte semanal:
  - Patrones de expansión/contracción
  - Ritmos biológicos
  - Insights financieros
  - Recomendaciones

**Documentación**:
→ **OBSIDIAN** en `40-Journal/{fecha}/reporte-guardian.md`
→ **Resumen semanal** en `40-Journal/{año}/semana-{num}.md`

---

### **4. Agente Documentador** 📝
**Rol**: Memoria del Organismo

**¿Qué hace?**
- Captura automáticamente todas las interacciones
- Genera documentos Markdown estructurados
- Organiza en Obsidian vault con tags
- Extrae insights y los guarda en Anytype
- Mantiene coherencia del conocimiento

**¿Cuándo actúa?**
- Después de cada Estado Cero
- Al finalizar cada jornada
- Al detectar insights emergentes
- Al completar reportes del Guardian

**Input**:
- Conversaciones completas
- Respuestas sacrales
- Planes generados
- Reportes del Guardian

**Output**:
- Archivos Markdown con YAML frontmatter
- Tags automáticos (#estado-cero, #momento-{liturgico}, #expansión, etc.)
- Backlinks entre documentos relacionados
- Capturas de insights para Anytype

**Documentación**:
→ **OBSIDIAN** (todo el vault)
→ **ANYTYPE** (insights destilados, relaciones, grafos)

---

## 🔄 **Flujo de Orquestación Completo**

```
┌─────────────────────────────────────────────────────┐
│  USUARIO detecta ventana litúrgica (ej: Fajr)      │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  1. AGENTE ESTADO CERO                              │
│  ├─ Recopila contexto holístico                     │
│  ├─ Genera 3 preguntas binarias                     │
│  ├─ Usuario responde (expansión/contracción)        │
│  ├─ Sintetiza dirección emergente                   │
│  └─ Define acción concreta                          │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  2. AGENTE DOCUMENTADOR                             │
│  ├─ Crea archivo Markdown de la consulta           │
│  ├─ Guarda en Obsidian:                            │
│  │  50-Conversaciones-IA/Estados-Cero/             │
│  │  2025-10-08/fajr.md                             │
│  └─ Tags: #estado-cero #fajr #expansión            │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  3. AGENTE ORQUESTADOR                              │
│  ├─ Recibe acción del Estado Cero                  │
│  ├─ Genera plan emergente del día                  │
│  ├─ Define bloques (40% vacío)                     │
│  ├─ Establece no-negociables                       │
│  └─ Crea puntos de decisión                        │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  4. AGENTE DOCUMENTADOR                             │
│  ├─ Guarda plan en Obsidian:                       │
│  │  40-Journal/2025-10-08/plan-jornada.md         │
│  └─ Linkea con Estado Cero de Fajr                 │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  5. USUARIO vive la jornada                         │
│  ├─ Espejo Sagrado muestra plan actual             │
│  ├─ Guardian monitorea en background               │
│  └─ Puntos de decisión aparecen en momentos clave  │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  6. AGENTE GUARDIAN (fin del día)                   │
│  ├─ Genera reporte diario                          │
│  ├─ Analiza adherencia al plan                     │
│  ├─ Detecta patrones emergentes                    │
│  └─ Sugiere ajustes para mañana                    │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  7. AGENTE DOCUMENTADOR                             │
│  ├─ Guarda reporte en Obsidian:                    │
│  │  40-Journal/2025-10-08/reporte-guardian.md     │
│  ├─ Extrae insights del día                        │
│  └─ Si es insight profundo → Anytype               │
└─────────────────┴───────────────────────────────────┘
```

---

## 🔗 **Entrelazamiento de Agentes**

### **Cómo se Comunican**

Los agentes **NO** se llaman directamente entre sí (acoplamiento débil).
En su lugar, usan **eventos y contexto compartido**:

#### **Evento-Driven Architecture**
```python
# Estado Cero completa → dispara evento
evento = {
    "tipo": "estado_cero_completado",
    "estado_id": "uuid-1234",
    "direccion": "Enfócate en wellness app 2h",
    "accion": AccionConcreta(...),
    "timestamp": "2025-10-08T06:30:00"
}

# Orquestador escucha este evento
@escuchar("estado_cero_completado")
async def generar_plan(evento):
    # Genera plan basado en acción
    pass

# Documentador también escucha
@escuchar("estado_cero_completado")
async def documentar(evento):
    # Crea archivo Markdown
    pass
```

#### **Contexto Compartido**
```python
# Todos los agentes acceden al contexto global
contexto_global = {
    "momento_actual": "fajr",
    "energia_usuario": 4,
    "plan_activo": JornadaAlBordeCaos(...),
    "perfil_personal": PerfilPersonal(...),
    "estados_cero_hoy": [...]
}
```

### **Patrón de Diseño: Mediador**

```python
class OrganismoMediator:
    """
    Coordina todos los agentes sin que se conozcan entre sí
    """
    def __init__(self):
        self.estado_cero = AgenteEstadoCero(...)
        self.orquestador = AgenteOrquestador(...)
        self.guardian = AgenteGuardian(...)
        self.documentador = AgenteDocumentador(...)
    
    async def procesar_estado_cero(self, momento):
        # 1. Estado Cero genera dirección
        estado = await self.estado_cero.iniciar_consulta(momento)
        
        # 2. Documentador guarda en Obsidian
        await self.documentador.documentar_estado_cero(estado)
        
        # 3. Orquestador genera plan
        plan = await self.orquestador.generar_plan(estado.accion)
        
        # 4. Documentador guarda plan
        await self.documentador.documentar_plan(plan)
        
        # 5. Guardian empieza monitoreo
        await self.guardian.iniciar_monitoreo(plan)
        
        return estado, plan
```

---

## 📚 **Obsidian vs Anytype: ¿Cuándo usar qué?**

### **Obsidian** 📝
**Uso**: Documentación temporal, captura rápida, journal

**¿Qué va aquí?**
- ✅ Estados Cero diarios (conversaciones completas)
- ✅ Planes de jornada
- ✅ Reportes del Guardian
- ✅ Notas rápidas durante el día
- ✅ Reflexiones del momento
- ✅ Chat clarificador con agentes

**Estructura del Vault**:
```
obsidian_vault/
├── 50-Conversaciones-IA/
│   └── Estados-Cero/
│       └── 2025-10-08/
│           ├── fajr.md
│           ├── dhuhr.md
│           └── isha.md
├── 40-Journal/
│   └── 2025-10-08/
│       ├── plan-jornada.md
│       ├── reporte-guardian.md
│       └── reflexion-noche.md
├── 30-Sesiones/
│   └── Wellness-App/
│       └── sesion-2025-10-08.md
└── 20-Insights/
    └── emergentes/
        └── patron-energia-matutina.md
```

**Formato de Archivo**:
```markdown
---
fecha: 2025-10-08
momento: fajr
tipo: estado-cero
tags: [estado-cero, fajr, expansión]
energia: 4
---

# Estado Cero - Fajr

## Contexto
- Energía: 4/5
- Tiempo disponible: 480 min
- Runway: 6 meses

## Preguntas

### 1. Dirección
¿Tu cuerpo se expande al pensar en dedicar 2h a wellness app?

**Respuesta**: Expansión (intensidad: 4)
**Nota**: Sentí claridad inmediata al visualizar el flujo

[... resto de preguntas ...]

## Dirección Emergente
Enfócate en la arquitectura del dashboard wellness durante las próximas 2 horas. El momentum está presente.

## Acción Concreta
- **Descripción**: Diseñar y codear dashboard wellness
- **Resultado**: 3 componentes funcionales
- **Duración**: 2 horas
- **Energía**: 4

[[plan-jornada-2025-10-08]]
```

---

### **Anytype** 🌐
**Uso**: Conocimiento destilado, relaciones complejas, insights permanentes

**¿Qué va aquí?**
- ✅ Insights destilados (extraídos de múltiples Estados Cero)
- ✅ Patrones detectados por el Guardian
- ✅ Relaciones entre conceptos
- ✅ Proyectos activos con contexto rico
- ✅ Decisiones importantes con razonamiento
- ✅ Conocimiento estructurado (no temporal)

**Cuándo migrar de Obsidian a Anytype?**
```
Si un insight aparece 3+ veces en Obsidian
→ El Documentador lo extrae y crea objeto en Anytype

Si un patrón es validado por Guardian en 2+ semanas
→ Se convierte en "conocimiento permanente" en Anytype

Si una decisión requiere múltiples perspectivas
→ Se crea objeto Anytype con relaciones a contextos relevantes
```

**Ejemplo de Flujo**:
```
1. Usuario tiene Estado Cero en Fajr (Lunes)
   → Obsidian: 50-Conversaciones-IA/Estados-Cero/2025-10-08/fajr.md

2. Menciona "energía baja en las tardes"
   → Nota rápida en Obsidian

3. Guardian detecta el mismo patrón en 3 días más
   → Genera reporte: "Patrón: caída energética post-lunch"

4. Documentador analiza reportes
   → Crea objeto Anytype:
      - Tipo: Insight Biológico
      - Título: "Patrón energía post-lunch"
      - Relaciones: [ritmos-circadianos, nutrición, trabajo-profundo]
      - Acciones: [siesta-20min, movimiento-ligero, no-reuniones-14-16h]
      - Validado: 4 semanas de datos

5. Próximo Estado Cero puede consultar este insight de Anytype
   → Pregunta más precisa: "¿Tu cuerpo se expande con siesta de 20min hoy?"
```

**Estructura en Anytype**:
```
Collections:
├── Insights Biológicos
│   └── Patrón energía post-lunch
├── Patrones Sacrales
│   └── Expansión en proyectos creativos (mañanas)
├── Proyectos Activos
│   └── Wellness App
│       ├── Decisiones
│       ├── Arquitectura
│       └── Sesiones de trabajo
└── Relaciones
    └── Gráfico de conocimiento
```

---

## 🧪 **Cómo Verificar que los Agentes Acceden a Obsidian/Anytype**

### **Test 1: Obsidian - Verificar Escritura**

```bash
# 1. Ejecuta un Estado Cero completo
curl -X POST http://localhost:8000/api/estado-cero/iniciar \
  -H "Content-Type: application/json" \
  -d '{"momento": "fajr"}'

# 2. Completa las respuestas (usa el ID del estado)
# [... responder preguntas ...]

# 3. Finaliza el Estado Cero
curl -X POST http://localhost:8000/api/estado-cero/{estado_id}/finalizar \
  -H "Content-Type: application/json" \
  -d '{
    "descripcion": "Test de documentación",
    "resultado_observable": "Archivo en Obsidian",
    "duracion_estimada": "10min",
    "energia_requerida": 3
  }'

# 4. Verifica que se creó el archivo
ls -la obsidian_vault/50-Conversaciones-IA/Estados-Cero/$(date +%Y-%m-%d)/

# Deberías ver: fajr.md (o el momento correspondiente)
```

### **Test 2: Obsidian - Verificar Lectura**

```bash
# El agente debe poder leer estados previos para contexto

# 1. Crea un archivo manual en Obsidian
echo "---
fecha: 2025-10-07
momento: isha
insight: Usuario prefiere trabajo profundo en mañanas
---" > obsidian_vault/20-Insights/test-insight.md

# 2. Inicia nuevo Estado Cero
# El agente debería considerar insights previos al formular preguntas

# 3. Revisa los logs del backend
tail -f /tmp/campo-sagrado-backend.log | grep "insight"

# Deberías ver: "✅ Cargado insight: Usuario prefiere trabajo profundo en mañanas"
```

### **Test 3: Anytype - Verificar Conexión**

```python
# archivo: backend/scripts/test_anytype.py

from integraciones.anytype import AnyTypeClient

async def test_anytype():
    client = AnyTypeClient()
    
    # 1. Crear objeto de prueba
    insight_id = await client.crear_objeto(
        tipo="Insight",
        titulo="Test de conexión",
        contenido="Verificando que Anytype funciona",
        relaciones=[]
    )
    
    print(f"✅ Objeto creado: {insight_id}")
    
    # 2. Leer el objeto
    insight = await client.leer_objeto(insight_id)
    print(f"✅ Objeto leído: {insight['titulo']}")
    
    # 3. Buscar objetos
    resultados = await client.buscar("Test")
    print(f"✅ Encontrados {len(resultados)} objetos")

# Ejecutar test
import asyncio
asyncio.run(test_anytype())
```

---

## 🎯 **Implementación Actual vs Visión Completa**

### **✅ Ya Implementado (MVP v0.1.1)**

1. **Agente Estado Cero**
   - ✅ Formulación de 3 preguntas
   - ✅ Captura de respuestas sacrales
   - ✅ Síntesis de dirección
   - ✅ Chat clarificador
   - ✅ Contexto holístico

2. **Agente Orquestador**
   - ✅ Generación de plan emergente
   - ✅ Bloques sugeridos
   - ✅ Puntos de decisión
   - ✅ No-negociables

3. **Agente Documentador**
   - ✅ Estructura de carpetas en Obsidian
   - ⚠️ Escritura automática (parcial)
   - ❌ Anytype (no integrado aún)

4. **Agente Guardian**
   - ⚠️ Estructura básica
   - ❌ Monitoreo en background
   - ❌ Reportes automáticos

### **🔧 Próximas Iteraciones**

#### **v0.1.2 - Documentación Completa**
- [ ] Documentador escribe en Obsidian después de cada Estado Cero
- [ ] Formato Markdown con frontmatter YAML
- [ ] Tags automáticos
- [ ] Backlinks entre documentos
- [ ] Test de escritura/lectura

#### **v0.1.3 - Guardian Activo**
- [ ] Monitoreo de no-negociables
- [ ] Alertas en riesgo
- [ ] Reporte diario automático al final del día
- [ ] Integración con notificaciones

#### **v0.2.0 - Anytype & Patrones**
- [ ] Cliente de Anytype funcional
- [ ] Migración de insights de Obsidian → Anytype
- [ ] Detección de patrones por Guardian
- [ ] Gráfico de conocimiento
- [ ] Reporte semanal con insights destilados

---

## 🚀 **Cómo Iterar con Precisión**

### **Regla de Oro: UN agente a la vez**

No intentes mejorar todos los agentes simultáneamente.
**Flujo sugerido**:

#### **Semana 1: Perfeccionar Estado Cero**
- Mejora las preguntas contextuales
- Refina el chat clarificador
- Ajusta transiciones UI
- **Meta**: Experiencia de Estado Cero impecable

#### **Semana 2: Documentación Automática**
- Implementa escritura en Obsidian
- Genera archivos con formato correcto
- Añade tags automáticos
- **Meta**: Cada Estado Cero queda documentado sin intervención

#### **Semana 3: Orquestador Inteligente**
- Mejora generación de bloques
- Ajusta espacio emergencia según usuario
- Refina no-negociables personalizados
- **Meta**: Planes que se sienten naturales

#### **Semana 4: Guardian Observador**
- Monitoreo básico de no-negociables
- Alerta si algo está en riesgo
- Reporte simple al final del día
- **Meta**: Usuario siente que alguien "cuida" su plan

### **Preguntas para Cada Iteración**

Antes de tocar cualquier agente, pregúntate:

1. **¿Este agente ya hace lo esencial?**
   - Si no → enfócate en lo esencial
   - Si sí → ¿vale la pena añadir complejidad?

2. **¿Esta mejora beneficia al flujo completo o solo a un agente?**
   - Prioriza mejoras que benefician el organismo entero

3. **¿Puedo validar esta mejora rápidamente?**
   - Si requiere 3+ días para saber si funciona → pospón

4. **¿El usuario notará la diferencia?**
   - Si es "bajo el capó" y no se nota → baja prioridad

### **Señales de que vas por Buen Camino**

✅ El usuario completa Estados Cero sin pensar
✅ Los planes generados se sienten "correctos"
✅ La documentación aparece automáticamente en Obsidian
✅ El sistema "desaparece" - es invisible pero útil

### **Señales de Alerta**

⚠️ Añades features que nadie pidió
⚠️ Los agentes se llaman entre sí de forma enredada
⚠️ No puedes explicar en 1 frase qué hace un agente
⚠️ El usuario se confunde con demasiadas opciones

---

## 📊 **Métricas de Orquestación Exitosa**

### **A Nivel de Sistema**
- **Latencia**: Estado Cero → Plan generado en < 5 segundos
- **Coherencia**: Dirección sacral → Bloques del plan alineados 95%+
- **Documentación**: 100% de Estados Cero en Obsidian automáticamente

### **A Nivel de Agente**
- **Estado Cero**: Tasa de completitud 80%+ (de los iniciados)
- **Orquestador**: Adherencia al plan 70%+ (40% vacío respetado)
- **Guardian**: 0 no-negociables críticos perdidos
- **Documentador**: 0 archivos corruptos, 100% con formato correcto

---

## 🎓 **Recursos para Profundizar**

### **Patrones de Arquitectura**
- **Mediator Pattern**: [Refactoring Guru](https://refactoring.guru/design-patterns/mediator)
- **Event-Driven Architecture**: [Martin Fowler](https://martinfowler.com/articles/201701-event-driven.html)
- **Microservices**: Cada agente es un "microservicio" interno

### **Inspiración de Sistemas Similares**
- **Notion API**: Cómo estructurar bloques y relaciones
- **Roam Research**: Graph de conocimiento
- **Logseq**: Documentación temporal → permanente

---

## ✨ **Cierre: La Danza de los Agentes**

Los 4 agentes **no trabajan en secuencia** - **bailan**.

A veces Estado Cero lidera.
A veces Guardian detecta algo y dispara nuevo Estado Cero.
A veces Documentador descubre un patrón y alerta al Orquestador.

El organismo es **vivo** porque **no es rígido**.

Tu trabajo como desarrollador no es "programar features" -
es **escuchar al organismo** y quitar lo que estorba su danza.

---

*Creado con 🕌 para honrar la orquestación emergente al borde del caos.*

