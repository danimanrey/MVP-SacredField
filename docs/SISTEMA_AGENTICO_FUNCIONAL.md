# 🕌 Sistema Agéntico Funcional - Guía Completa

## 📍 **Navegación Rápida: Dónde Está Todo**

### **1. ¿En qué momento logramos el sistema agéntico funcional?**

**✅ AHORA - v0.1.1 (MVP Funcional)**

El sistema agéntico **YA está funcional**. Cada agente está implementado y operativo:

```
Estado Actual del Sistema Agéntico:
────────────────────────────────────────────────────────────
✅ AgenteEstadoCero       - backend/agentes/estado_cero.py
✅ AgenteOrquestador      - backend/agentes/orquestador.py
✅ AgenteGuardian         - backend/agentes/guardian.py
✅ AgenteDocumentador     - backend/agentes/documentador.py
✅ AgenteEntrelazador     - backend/agentes/entrelazador.py
```

**Lo que falta** para un sistema agéntico **MADURO**:
- 🔄 Guardian en modo activo (monitoreo automático)
- 🔄 Documentador completamente integrado
- 🔄 Mediator Pattern (orquestación centralizada)
- ⏸️ Agentes aprendiendo de feedback continuo

---

### **2. ¿Dónde encontramos los prompts de personalización de los agentes?**

#### **Estado Cero** - Prompt Principal
📁 `backend/agentes/estado_cero.py` (líneas 97-147)

```python
prompt = f"""Eres el Agente Estado Cero del Campo Sagrado.
Es momento {contexto.temporal.momento_liturgico.value}.

CONTEXTO COMPLETO:
- Temporal: {contexto.temporal.dia_semana} - {contexto.temporal.cualidad_momento}
- Mes: {contexto.temporal.mes_hijri} - {contexto.temporal.cualidad_mes}
- Biológico: Energía {contexto.biologico.energia_actual}/5...
- Financiero: Runway {contexto.financiero.runway_meses} meses...
{contexto_personal}  # ← Aquí se integra tu perfil

Tu función: Formular 3 preguntas BINARIAS ESENCIALES que:
1. Ayuden a consultar la autoridad sacral...
2. Cubran las 4 dimensiones: finanzas, biología, desarrollo, conocimiento
3. Sean específicas y concretas...
```

**Personalización automática**:
- Lee tu perfil personal (deportes, proyectos, aprendizaje)
- Adapta preguntas al momento litúrgico
- Considera tu energía y contexto actual

#### **Orquestador** - Prompt Principal
📁 `backend/agentes/orquestador.py` (líneas 64-111)

```python
prompt = f"""Eres el Agente Orquestador.

ORIENTACIÓN DEL ESTADO CERO:
Acción: {accion.descripcion}
Energía requerida: {accion.energia_requerida}/5

CONTEXTO:
- Momento: {contexto.temporal.momento_liturgico.value}
- Biología: Energía {contexto.biologico.energia_actual}/5...
- Financiero: Runway {contexto.financiero.runway_meses} meses

GENERA plan emergente de jornada que:
1. Honre la acción del Estado Cero como PRINCIPAL
2. Respete curva de energía natural
3. Mantenga 40% espacio sin asignar (emergencia)
4. Opere al borde del caos (flexible, adaptable)
```

#### **Entrelazador** - Prompt de Dashboard
📁 `backend/agentes/entrelazador.py` (líneas 60-95)

```python
# Utiliza tu perfil completo para detectar:
- Conflictos: "Gym 18:00 vs Reunión 18:30"
- Sinergias: "Correr → Mejor enfoque → Mejor código"
- Patrones de energía
- Recomendaciones personalizadas
```

---

### **3. ¿Dónde está la configuración del individuo que da vida al organismo?**

#### **Perfil Personal** (Configuración Individual)
📁 `backend/models/schemas.py` (líneas 300-335)

```python
class PerfilPersonal(BaseModel):
    """Perfil completo del usuario - EL ALMA DEL ORGANISMO"""
    
    # Información básica
    nombre: str
    timezone: str
    
    # Las 6 áreas de tu vida:
    rutinas_deportivas: List[RutinaDeportiva]
    sistema_comidas: List[ComidaConfiguracion]
    presupuesto_mensual: List[PresupuestoCategoria]
    temas_aprendizaje: List[TemaAprendizaje]          # ← APRENDIZAJE
    proyectos_desarrollo: List[ProyectoDesarrollo]
    inversiones_asuntos: List[InversionAsunto]
```

#### **Cómo Configurar tu Perfil**

**Opción A: Frontend** (Recomendado)
```
1. Abre: http://localhost:5173/configurar-perfil
2. Completa el formulario paso a paso
3. Guarda tu perfil
```

📁 `frontend/src/routes/configurar-perfil/+page.svelte`

**Opción B: Script Interactivo** (CLI)
```bash
cd backend
python scripts/personalizar_perfil.py
# → Guía interactiva te hará preguntas
# → Genera: mi_perfil_personal.json
```

📁 `backend/scripts/personalizar_perfil.py`

**Opción C: Manual** (JSON directo)
```bash
# Crear archivo de perfil
nano mi_perfil.json

# Cargar perfil
curl -X POST http://localhost:8000/api/entrelazamiento/perfil \
  -H "Content-Type: application/json" \
  -d @mi_perfil.json
```

---

### **4. ¿Dónde está el apartado de aprendizaje?**

#### **En el Perfil Personal**
📁 `backend/models/schemas.py` (líneas 265-276)

```python
class TemaAprendizaje(BaseModel):
    """Temas que estás aprendiendo activamente"""
    nombre: str                         # "Rust", "Filosofía Estoica"
    dominio: str                        # "tecnología", "filosofía"
    prioridad: int                      # 1-5
    tiempo_semanal_deseado: int         # minutos/semana
    recursos: List[str]                 # ["libro X", "curso Y"]
    progreso_porcentaje: float          # 0-100
    fecha_inicio: date
    fecha_objetivo: Optional[date]      # Meta de completar
```

#### **Cómo se Integra en el Sistema**

**Estado Cero** lee tus temas de aprendizaje:
```python
# backend/agentes/estado_cero.py (líneas 85-86)
temas_prioritarios = sorted(
    perfil.temas_aprendizaje, 
    key=lambda t: t.prioridad, 
    reverse=True
)[:2]

# Genera preguntas personalizadas:
# "¿Tu cuerpo se expande al pensar en dedicar 90 minutos a Rust?"
```

**Dashboard de Entrelazamiento** sugiere cuándo aprender:
```python
# Detecta:
- Mejor momento del día para aprender (energía alta)
- Conflictos con otras actividades
- Sinergias (aprender después de ejercicio)
```

---

### **5. ¿Dónde decidimos objetivos a largo plazo y carrera?**

**❌ FALTA IMPLEMENTAR** - Planificado para v0.2.0

#### **Lo que tenemos ahora (v0.1.1)**:

**Objetivos a corto/medio plazo**:
```python
class TemaAprendizaje:
    fecha_objetivo: Optional[date]  # Meta de completar tema

class ProyectoDesarrollo:
    deadline: Optional[date]        # Meta de completar proyecto
    hitos: List[str]                # Hitos intermedios
```

**Prioridades claras**:
```python
# Cada área tiene prioridad 1-5
temas_aprendizaje: [prioridad]
proyectos_desarrollo: [prioridad]
inversiones_asuntos: [prioridad]
```

#### **Lo que FALTA implementar** (v0.2.0):

**Visión a Largo Plazo**:
```python
class VisionLargoPlazo(BaseModel):
    """Dirección de vida - Objetivos 1-5 años"""
    
    # Tu visión del 0.01%
    vision_5_años: str              # "Dominar IA aplicada + Negocio propio"
    carrera_objetivo: str           # "Tech Lead → Founder"
    
    # Habilidades clave
    habilidades_core: List[str]     # ["Rust", "ML", "Liderazgo"]
    habilidades_complementarias: List[str]
    
    # Hitos trimestrales
    hitos: List[HitoTrimestral]
    
    # Métricas de progreso
    metricas_exito: List[str]       # "Lanzar MVP", "10K usuarios"
```

**Agente de Trayectoria** (nuevo):
```python
class AgenteTrayectoria:
    """Guía tu camino al 0.01%"""
    
    def alinear_acciones_con_vision(self, accion_hoy, vision_largo_plazo):
        """
        Verifica que cada acción de hoy
        te acerca a tu visión de 5 años
        """
        
    def sugerir_ajuste_curso(self, progreso_trimestral):
        """
        Si te desvías de la trayectoria,
        sugiere ajustes (no impone)
        """
```

---

## 🎯 **Camino al 0.01% - Roadmap Completo**

### **v0.1.1 (ACTUAL) - MVP Funcional** ✅

```
✅ Sistema agéntico funcional
✅ Perfil personal con 6 áreas
✅ Dashboard de entrelazamiento
✅ Estado Cero personalizado
✅ Orquestador al borde del caos
✅ Documentación en Obsidian

⚠️ Falta:
- Objetivos a largo plazo explícitos
- Agente de Trayectoria
- Retroalimentación continua
```

---

### **v0.2.0 - Visión y Trayectoria** ⏸️ Planificado

**Nuevos Modelos**:
```python
class VisionLargoPlazo(BaseModel):
    vision_5_años: str
    carrera_objetivo: str
    habilidades_core: List[str]
    hitos_trimestrales: List[HitoTrimestral]
    metricas_exito: List[MetricaExito]

class HitoTrimestral(BaseModel):
    trimestre: str              # "Q1 2026"
    objetivo_principal: str
    metricas: List[str]
    proyectos_asociados: List[str]

class MetricaExito(BaseModel):
    nombre: str
    valor_actual: float
    valor_objetivo: float
    fecha_objetivo: date
```

**Nuevo Agente**:
```python
class AgenteTrayectoria:
    """Guardián del camino al 0.01%"""
    
    def __init__(self, vision: VisionLargoPlazo):
        self.vision = vision
    
    async def alinear_dia_con_vision(
        self, 
        acciones_hoy: List[AccionConcreta]
    ) -> AlineacionReport:
        """
        Pregunta clave:
        "¿Estas acciones de hoy te acercan a tu visión de 5 años?"
        
        Responde:
        - % alineación
        - Acciones alineadas
        - Acciones desalineadas
        - Sugerencias de ajuste
        """
    
    async def revisar_progreso_trimestral(
        self,
        trimestre: str
    ) -> ProgresoReport:
        """
        Cada 3 meses:
        - ¿Cumpliste hitos?
        - ¿Métricas en objetivo?
        - ¿Ajustar curso?
        """
```

**Frontend**:
```svelte
<!-- frontend/src/routes/vision-largo-plazo/+page.svelte -->

<script>
  let vision = {
    titulo: "Mi Visión al 0.01%",
    descripcion_5_años: "",
    carrera_objetivo: "",
    habilidades_core: [],
    hitos_trimestrales: []
  };
</script>

<div class="vision-container">
  <h1>Tu Visión al 0.01%</h1>
  
  <!-- Formulario de visión -->
  <!-- Dashboard de progreso -->
  <!-- Timeline de hitos -->
</div>
```

---

### **v0.3.0 - Aprendizaje y Retroalimentación** ⏸️ Futuro

**Sistema de Feedback Continuo**:
```python
class SistemaRetroalimentacion:
    """Aprende de tu comportamiento real"""
    
    def observar_patrones(self):
        """
        - ¿A qué hora eres más productivo realmente?
        - ¿Qué tipo de tareas completas más?
        - ¿Dónde gastas tiempo vs donde planeabas?
        """
    
    def ajustar_recomendaciones(self):
        """
        Agentes se adaptan a TU realidad:
        - Estado Cero aprende qué preguntas resuenan
        - Orquestador aprende tu ritmo real
        - Entrelazador aprende tus prioridades reales
        """
```

**Agentes que Aprenden**:
```python
class AgenteEstadoCeroV2(AgenteEstadoCero):
    """Estado Cero que aprende de ti"""
    
    async def formular_preguntas_adaptativas(self, contexto, historial):
        """
        Analiza 30 días de Estados Cero:
        - ¿Qué preguntas generaron más claridad?
        - ¿Qué dimensiones son más relevantes para ti?
        - ¿Qué formato de pregunta resuena más?
        
        Ajusta estilo para TU forma única de consulta sacral
        """
```

---

## 📍 **Dónde Está TODO Ahora (Mapa Completo)**

### **Backend**

#### **Modelos de Datos**
```
📁 backend/models/schemas.py
├─ PerfilPersonal (líneas 300-335)
│  ├─ RutinaDeportiva
│  ├─ ComidaConfiguracion
│  ├─ PresupuestoCategoria
│  ├─ TemaAprendizaje ← APRENDIZAJE
│  ├─ ProyectoDesarrollo
│  └─ InversionAsunto
│
├─ EstadoCeroCompleto
├─ JornadaAlBordeCaos
├─ DashboardEntrelazamiento
└─ [FALTA] VisionLargoPlazo
```

#### **Agentes**
```
📁 backend/agentes/
├─ estado_cero.py
│  └─ Prompt (líneas 97-147) ← Personalización automática
│
├─ orquestador.py
│  └─ Prompt (líneas 64-111) ← Plan emergente
│
├─ guardian.py
│  └─ [Pasivo] Necesita activación (v0.1.2)
│
├─ documentador.py
│  └─ [Funcional] Archiva en Obsidian
│
├─ entrelazador.py
│  └─ [Funcional] Dashboard personal
│
└─ [FALTA] trayectoria.py ← Visión largo plazo
```

#### **APIs**
```
📁 backend/api/
├─ estado_cero.py
│  ├─ POST /iniciar
│  └─ POST /completar
│
├─ orquestador.py
│  └─ POST /generar-plan
│
├─ entrelazamiento.py ← CONFIGURACIÓN INDIVIDUAL
│  ├─ POST /perfil              ← Crear/actualizar perfil
│  ├─ GET /perfil
│  ├─ GET /dashboard-semanal    ← Ver entrelazamiento
│  └─ GET /conflictos           ← Detectar problemas
│
└─ ritual_maghrib.py
   ├─ POST /sugerir-intencion
   └─ POST /preparar-dia-siguiente
```

#### **Scripts de Configuración**
```
📁 backend/scripts/
├─ personalizar_perfil.py       ← CLI interactivo
├─ perfil_ejemplo.py            ← Ejemplo completo
└─ verificar_prefajr.py         ← Test sistema
```

### **Frontend**

```
📁 frontend/src/routes/
├─ configurar-perfil/+page.svelte    ← CONFIGURACIÓN UI
│  └─ Formulario completo multi-paso
│
├─ estado-cero/+page.svelte
│  └─ Consulta sacral con 3 preguntas
│
├─ espejo-sagrado/+page.svelte
│  └─ Plan de jornada emergente
│
├─ ritual-maghrib/+page.svelte
│  └─ Ritual completo + Google Calendar
│
├─ dashboard-entrelazamiento/+page.svelte
│  └─ Vista integrada de tu vida
│
└─ [FALTA] vision-largo-plazo/+page.svelte
   └─ Definir objetivos 1-5 años
```

---

## 🎯 **Cómo Usar el Sistema Ahora**

### **1. Configura tu Perfil**

```bash
# Opción A: Frontend
open http://localhost:5173/configurar-perfil

# Opción B: CLI
cd backend
python scripts/personalizar_perfil.py
```

**Define**:
- ✅ Rutinas deportivas semanales
- ✅ Sistema de comidas y batch cooking
- ✅ Presupuesto mensual por categorías
- ✅ **Temas de aprendizaje activos** ← APRENDIZAJE
- ✅ Proyectos de desarrollo en curso
- ✅ Inversiones y decisiones pendientes

### **2. Usa el Sistema Agéntico**

**Cada momento litúrgico** (5 veces al día):
```bash
# Frontend
open http://localhost:5173/estado-cero

# Lo que sucede:
1. Estado Cero lee TU perfil
2. Genera 3 preguntas personalizadas
3. Tú respondes con tu cuerpo
4. Claude sintetiza dirección emergente
5. (Opcional) Orquestador genera plan
6. Documentador archiva en Obsidian
```

**Cada día** - Revisa tu Dashboard:
```bash
open http://localhost:5173/dashboard-entrelazamiento

# Verás:
- Deportes de hoy
- Comidas planificadas
- Presupuesto del día
- Aprendizaje sugerido ← AQUÍ
- Proyectos prioritarios
- Conflictos detectados
- Sinergias posibles
```

**Cada noche** - Ritual Maghrib:
```bash
open http://localhost:5173/ritual-maghrib

# Preparas:
- Reflexión del día
- Intención para mañana
- Jornada en Google Calendar
- Compartir con círculo cercano
```

### **3. Documenta tu Progreso**

```bash
# Ver tu historial en Obsidian
open /Users/hp/Documents/CampoSagrado/

# Estructura:
50-Conversaciones-IA/
├── Estados-Cero/
│   ├── 2025-10-08/
│   │   ├── fajr.md
│   │   ├── dhuhr.md
│   │   └── maghrib.md
│   └── 2025-10-09/
└── Reportes-Diarios/
    └── 2025-10-08.md
```

---

## 🚀 **Próximos Pasos para el 0.01%**

### **Inmediato (Esta Semana)**

1. ✅ **Configura tu perfil personal**
   ```bash
   python scripts/personalizar_perfil.py
   ```

2. ✅ **Usa Estado Cero 3 días seguidos**
   - Observa cómo se personalizan las preguntas
   - Nota qué resuena en tu cuerpo

3. ✅ **Revisa Dashboard de Entrelazamiento**
   - ¿Detecta conflictos reales?
   - ¿Sugiere sinergias útiles?

### **v0.2.0 (Próximas 2-4 semanas)**

1. **Implementar Visión a Largo Plazo**
   - Modelo `VisionLargoPlazo`
   - Frontend para definir objetivos 1-5 años
   - Agente de Trayectoria

2. **Alinear Acciones Diarias con Visión**
   - Estado Cero pregunta: "¿Esto te acerca a tu visión?"
   - Dashboard muestra % alineación
   - Reporte semanal de progreso

3. **Hitos Trimestrales**
   - Definir métricas de éxito
   - Revisión cada 3 meses
   - Ajuste de curso si es necesario

### **v0.3.0+ (Largo Plazo)**

1. **Sistema de Retroalimentación**
   - Agentes aprenden de tu comportamiento real
   - Se adaptan a TU forma única

2. **Integración Profunda**
   - Anytype para grafos de conocimiento
   - Análisis de patrones de productividad
   - Predicción de energía y enfoque

3. **Comunidad del 0.01%**
   - Compartir aprendizajes (anónimos)
   - Patrones comunes del 0.01%
   - Mejores prácticas colectivas

---

## 📊 **Estado Actual: Resumen Ejecutivo**

### **¿Sistema Agéntico Funcional?**
✅ **SÍ** - Todos los agentes operativos

### **¿Prompts de Personalización?**
✅ **SÍ** - En cada agente, se adaptan a tu perfil

### **¿Configuración Individual?**
✅ **SÍ** - `PerfilPersonal` + Frontend + CLI

### **¿Apartado de Aprendizaje?**
✅ **SÍ** - `TemaAprendizaje` en perfil + Dashboard

### **¿Objetivos a Largo Plazo?**
⏸️ **EN DESARROLLO** - v0.2.0

### **¿Camino al 0.01%?**
🔄 **EN PROCESO** - MVP funcional, visión pendiente

---

## ✨ **Reflexión Final**

```
El sistema agéntico está VIVO.

Los agentes responden a TU perfil.
Los prompts se adaptan a TU contexto.
Las recomendaciones emergen de TU vida.

Lo que falta:
- Objetivos explícitos a 5 años
- Alineación diaria con visión
- Aprendizaje continuo de feedback

Pero el organismo YA respira.
YA se adapta.
YA te refleja.

El camino al 0.01% comienza
con el primer Estado Cero personalizado.

¿Listo para configurar tu perfil?
```

🕌 ¿Qué área quieres profundizar primero?

