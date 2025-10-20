# 🗓️ Correspondencia Calendario-Agentes

## 🎯 **Concepto Central**

El calendario es el **reflejo visual** de la orquestación de agentes:

```
Entrelazador  →  Vista Semanal (estrategia)
      ↓
Orquestador   →  Vista Diaria (táctica)
      ↓
Estado Cero   →  Refinamiento en tiempo real
      ↓
Google Calendar  →  Manifestación visible
```

---

## 📊 **Flujo Completo de Correspondencia**

### **DOMINGO NOCHE - Preparación Semanal**

```
1. ENTRELAZADOR genera Vista Semanal
   ────────────────────────────────────────────────────────────
   Input:
   • PerfilPersonal (rutinas, proyectos, aprendizaje)
   • Semana del calendario (Lun 9 - Dom 15 Oct)
   
   Proceso:
   • Distribuye rutinas deportivas en días correspondientes
   • Planifica batch cooking si corresponde
   • Asigna tiempo a proyectos según prioridad
   • Detecta conflictos (Gym 18:00 vs Reunión 18:30)
   • Identifica sinergias (Correr → Mejor enfoque)
   
   Output:
   • DashboardEntrelazamiento (vista semanal)
   • 7 días con estructura base
   • Conflictos y sinergias identificados
   
   Visualización:
   → frontend/vista-semanal
   → Calendario semanal con bloques de colores
   → No-negociables marcados como anclas ⚓
```

### **CADA NOCHE (MAGHRIB) - Preparación Diaria**

```
2. RITUAL MAGHRIB genera Vista Diaria
   ────────────────────────────────────────────────────────────
   Input:
   • Intención del usuario para mañana
   • DashboardEntrelazamiento (estructura semanal)
   • Tiempos litúrgicos precisos de mañana
   
   Proceso:
   • ORQUESTADOR toma intención
   • Consulta estructura semanal del Entrelazador
   • Genera plan emergente del día
   • Respeta no-negociables
   • Mantiene 40% espacio libre
   
   Output:
   • JornadaAlBordeCaos (plan del día)
   • Bloques sugeridos con horarios
   • Puntos de decisión
   • No-negociables del día
   
   Acción:
   → Crear eventos en Google Calendar
   → 5 Estados Cero (tiempos precisos)
   → Bloques del plan
   → No-negociables como recordatorios
```

### **DURANTE EL DÍA - Refinamiento en Tiempo Real**

```
3. ESTADOS CERO refinan el plan
   ────────────────────────────────────────────────────────────
   FAJR (06:59)
   ├─ Estado Cero: Dirección emergente
   ├─ Actualiza plan del día
   └─ Espejo Diario se REFINA
   
   DHUHR (14:02)
   ├─ Estado Cero: Revisión de progreso
   ├─ Ajusta bloques de tarde
   └─ Espejo Diario se ACTUALIZA
   
   ASR (17:14)
   ├─ Estado Cero: Completar ciclos
   ├─ Cierra bloques pendientes
   └─ Espejo Diario se AJUSTA
   
   MAGHRIB (20:02)
   ├─ Estado Cero: Reflexión e integración
   ├─ Cierra día actual
   └─ Prepara día siguiente
```

---

## 🏗️ **Arquitectura de Correspondencia**

### **Nivel 1: Estrategia Semanal (ENTRELAZADOR)**

```python
class AgenteEntrelazador:
    """Vista semanal - Estrategia"""
    
    def generar_dashboard_semanal(self, fecha_inicio: date):
        """
        Genera estructura base de la semana
        
        Output:
        {
            "lunes": {
                "deportes": ["Gym 18:00"],
                "comidas": ["Batch cooking 12:00"],
                "proyectos": ["Proyecto A: 4h"],
                "aprendizaje": ["Rust: 2h"],
                "no_negociables": [
                    "Movimiento: 30min (7-9am)",
                    "Lectura: 45min",
                    "Comida nutritiva: 12-2pm"
                ]
            },
            "martes": {...},
            ...
        }
        """
```

**Visualización Semanal**:
```
┌─────────────────────────────────────────────────────────────┐
│              VISTA SEMANAL (Estrategia)                     │
├────────┬────────┬────────┬────────┬────────┬────────┬──────┤
│  LUN   │  MAR   │  MIÉ   │  JUE   │  VIE   │  SÁB   │ DOM  │
├────────┼────────┼────────┼────────┼────────┼────────┼──────┤
│⚓ Gym   │⚓ Correr│⚓ Gym   │⚓ Correr│⚓ Gym   │⚓ Yoga  │ Libre│
│ 18:00  │ 07:00  │ 18:00  │ 07:00  │ 18:00  │ 09:00  │      │
├────────┼────────┼────────┼────────┼────────┼────────┼──────┤
│💻 Proy A│💻 Proy A│💻 Proy B│💻 Proy B│💻 Proy A│🌊 Libre │🌊 Libre│
│ 4h     │ 4h     │ 3h     │ 3h     │ 2h     │        │      │
├────────┼────────┼────────┼────────┼────────┼────────┼──────┤
│📚 Rust │📚 Rust │📚 IA   │📚 IA   │📚 Rust │📚 Libre│🌊 Libre│
│ 2h     │ 2h     │ 2h     │ 2h     │ 1h     │        │      │
└────────┴────────┴────────┴────────┴────────┴────────┴──────┘

⚓ = No-negociable (anclado)
💻 = Proyecto desarrollo
📚 = Aprendizaje
🌊 = Espacio libre (40%)
```

---

### **Nivel 2: Táctica Diaria (ORQUESTADOR)**

```python
class AgenteOrquestador:
    """Vista diaria - Táctica"""
    
    async def generar_plan_dia(
        self,
        intencion: str,
        estructura_semanal: EntrelazamientoDia,
        tiempos_liturgicos: TiemposRezoDia
    ):
        """
        Toma estructura semanal del Entrelazador
        + Intención del usuario
        + Tiempos litúrgicos precisos
        
        Genera plan emergente del día
        
        Output:
        {
            "bloques_sugeridos": [
                {
                    "inicio": "07:00",  # Preciso
                    "fin": "07:30",
                    "actividad": "Correr",
                    "origen": "entrelazador",  # Viene de rutina semanal
                    "tipo": "no_negociable",
                    "flexible": False
                },
                {
                    "inicio": "09:00",
                    "fin": "11:00",
                    "actividad": "Proyecto A - Feature X",
                    "origen": "estado_cero",  # Viene de dirección emergente
                    "tipo": "trabajo_profundo",
                    "flexible": True
                },
                {
                    "inicio": "14:02",
                    "fin": "14:32",
                    "actividad": "Estado Cero - DHUHR",
                    "origen": "liturgico",  # Tiempo astronómico
                    "tipo": "ritual",
                    "flexible": False
                }
            ],
            "espacio_libre": "40%",  # 9.6h de 24h
            "puntos_decision": [...]
        }
        """
```

**Visualización Diaria (Espejo)**:
```
┌─────────────────────────────────────────────────────────────┐
│           ESPEJO DIARIO - Miércoles 9 Octubre               │
│                                                              │
│  Intención: "Avanzar Proyecto A con energía enfocada"      │
└─────────────────────────────────────────────────────────────┘

06:46 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 08:19
      🌅 FAJR - Estado Cero
      └─ Dirección emergente del día

09:00 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 11:00
      💻 Proyecto A - Feature X (Trabajo profundo)
      🌊 Flexible | Energía: 🔥🔥🔥🔥

11:30 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12:00
      ⚓ Movimiento + Comida (No-negociable)

14:02 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 14:32
      ☀️ DHUHR - Estado Cero
      └─ Refinamiento de dirección

15:00 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 17:00
      📚 Rust - Capítulo 5 (Aprendizaje)
      🌊 Flexible | Energía: 🔥🔥🔥

17:14 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 17:44
      🌤️ ASR - Estado Cero
      └─ Ajuste de tarde

18:00 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 19:00
      ⚓ Gym (No-negociable)

20:02 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20:32
      🌆 MAGHRIB - Estado Cero + Ritual
      └─ Reflexión + Preparar mañana

      ╔═══════════════════════════════════════════════╗
      ║  ESPACIO EMERGENTE: 40% (9.6 horas)          ║
      ║  Para lo impredecible, serendipia, descanso  ║
      ╚═══════════════════════════════════════════════╝
```

---

## 🔄 **Correspondencia Completa**

### **1. ENTRELAZADOR → Estructura Semanal**

```python
# Domingo noche o Lunes mañana
dashboard_semanal = entrelazador.generar_dashboard_semanal(
    fecha_inicio=date(2025, 10, 9)  # Lunes
)

# Output:
{
    "semana": "9-15 Octubre 2025",
    "dias": {
        "lunes": {
            "deportes": ["Gym 18:00-19:00"],
            "comidas": ["Batch cooking 12:00-14:00"],
            "proyectos": ["Proyecto A: 4h"],
            "aprendizaje": ["Rust: 2h"],
            "finanzas": ["Compra semanal"],
            "no_negociables": [
                "Movimiento: 30min (7-9am)",
                "Lectura: 45min",
                "Comida nutritiva: 12-2pm"
            ],
            "conflictos": ["Gym 18:00 vs Posible reunión tarde"],
            "sinergias": ["Correr am → Mejor enfoque → Proyecto A"]
        },
        "martes": {...},
        ...
    },
    "resumen_ejecutivo": "Semana enfocada en Proyecto A...",
    "energia_total_requerida": 85,
    "horas_comprometidas": 60,
    "horas_libres": 48  # 40% de 120h útiles
}
```

---

### **2. MAGHRIB → Plan Diario (Orquestador)**

```python
# Cada noche a las 20:02 (Maghrib)
# Usuario hace Ritual Maghrib

# Input del usuario:
intencion = "Avanzar Proyecto A con energía enfocada"

# Orquestador consulta:
estructura_dia = entrelazador.obtener_estructura_dia(fecha=mañana)
tiempos_liturgicos = calculador.calcular_tiempos_hoy(fecha=mañana)

# Orquestador genera:
plan_dia = orquestador.generar_plan_emergente(
    intencion=intencion,
    estructura_base=estructura_dia,  # Del Entrelazador
    tiempos_liturgicos=tiempos_liturgicos  # Precisos
)

# Output:
{
    "fecha": "2025-10-09",
    "intencion": "Avanzar Proyecto A con energía enfocada",
    
    "bloques": [
        # Estados Cero (tiempos precisos astronómicos)
        {
            "inicio": "06:46",
            "fin": "08:19",
            "tipo": "estado_cero",
            "momento": "fajr",
            "origen": "liturgico",
            "flexible": False,
            "compartir": False
        },
        
        # No-negociables (del Entrelazador)
        {
            "inicio": "07:00",
            "fin": "07:30",
            "tipo": "no_negociable",
            "actividad": "Movimiento",
            "origen": "entrelazador",
            "flexible": False,  # Anclado
            "compartir": False
        },
        
        # Bloques de trabajo (del Orquestador basado en intención)
        {
            "inicio": "09:00",
            "fin": "11:00",
            "tipo": "trabajo_profundo",
            "actividad": "Proyecto A - Feature X",
            "origen": "estado_cero",  # Basado en dirección emergente
            "energia_optima": 4,
            "flexible": True,  # Puede moverse
            "compartir": True  # Se comparte con asistentes
        },
        
        # Rutinas (del Entrelazador)
        {
            "inicio": "18:00",
            "fin": "19:00",
            "tipo": "rutina",
            "actividad": "Gym",
            "origen": "entrelazador",
            "flexible": False,
            "compartir": True
        }
    ],
    
    "espacio_libre": [
        {"inicio": "11:00", "fin": "12:00"},  # 1h
        {"inicio": "15:00", "fin": "17:14"},  # 2h 14m
        {"inicio": "19:00", "fin": "20:02"}   # 1h 2m
        # Total: ~9.6h de 24h = 40%
    ]
}
```

---

### **3. GOOGLE CALENDAR → Manifestación Visual**

```python
# Google Calendar recibe el plan y crea eventos

google_calendar.crear_jornada_completa(
    fecha=mañana,
    plan=plan_dia,
    intencion=intencion,
    asistentes=["pareja@email.com"]
)

# Eventos creados:
[
    # Estados Cero (privados, tiempos precisos)
    {
        "titulo": "🌅 Estado Cero - FAJR",
        "inicio": "2025-10-09T06:46:00+02:00",
        "fin": "2025-10-09T08:19:00+02:00",
        "color": "azul_claro",
        "privado": True,
        "descripcion": "Consulta sacral - Ventana completa de Fajr"
    },
    
    # No-negociables (privados, anclas)
    {
        "titulo": "⚓ Movimiento",
        "inicio": "2025-10-09T07:00:00+02:00",
        "fin": "2025-10-09T07:30:00+02:00",
        "color": "verde",
        "privado": True,
        "descripcion": "No-negociable: 30min movimiento"
    },
    
    # Bloques de trabajo (compartidos)
    {
        "titulo": "🌊 Proyecto A - Feature X",
        "inicio": "2025-10-09T09:00:00+02:00",
        "fin": "2025-10-09T11:00:00+02:00",
        "color": "naranja",
        "privado": False,
        "asistentes": ["pareja@email.com"],
        "descripcion": "Trabajo profundo\nEnergía: 🔥🔥🔥🔥\nFlexible: Sí"
    }
]
```

---

## 📱 **Vistas del Sistema**

### **Vista Semanal** (Entrelazador)

```
frontend/src/routes/vista-semanal/+page.svelte

Muestra:
• Calendario de 7 días
• Rutinas distribuidas
• Proyectos asignados
• Aprendizaje planificado
• Conflictos detectados (⚠️)
• Sinergias identificadas (✨)
• % de tiempo asignado vs libre

Interacción:
• Clic en día → Ver vista diaria
• Clic en conflicto → Sugerencias de resolución
• Drag & drop para ajustar (futuro)
```

### **Vista Diaria / Espejo Sagrado** (Orquestador)

```
frontend/src/routes/espejo-sagrado/+page.svelte

Muestra:
• Intención del día (grande, prominente)
• Timeline vertical con bloques
• Estados Cero marcados con tiempos precisos
• No-negociables como anclas ⚓
• Bloques de trabajo con energía requerida
• Espacio libre visualizado (40%)
• Actualización en tiempo real

Interacción:
• Se actualiza con cada Estado Cero
• Muestra dirección emergente actual
• Permite ajustes manuales
• Sincroniza con Google Calendar
```

---

## 🔄 **Flujo de Actualización en Tiempo Real**

### **Ejemplo: Miércoles 9 Octubre**

```
DOMINGO 6 OCT (23:00)
├─ Entrelazador genera estructura semanal
└─ Vista Semanal disponible

MARTES 8 OCT (20:02 - Maghrib)
├─ Usuario: "Avanzar Proyecto A con energía enfocada"
├─ Orquestador consulta estructura semanal
├─ Genera plan emergente para Miércoles
├─ Google Calendar: 16 eventos creados
└─ Espejo Diario BASE creado

MIÉRCOLES 9 OCT (06:46 - Fajr)
├─ Estado Cero: 3 preguntas
├─ Dirección: "Enfócate en Feature X con bloques profundos"
├─ Espejo Diario se ACTUALIZA:
│  └─ Bloque 09:00-11:00 se refina: "Feature X específicamente"
└─ Google Calendar se actualiza (opcional)

MIÉRCOLES 9 OCT (14:02 - Dhuhr)
├─ Estado Cero: Revisión
├─ Dirección: "Continúa momentum, añade documentación"
├─ Espejo Diario se REFINA:
│  └─ Bloque 15:00-17:00 se añade: "Documentar Feature X"
└─ Usuario ve cambios en tiempo real

MIÉRCOLES 9 OCT (17:14 - Asr)
├─ Estado Cero: Completar
├─ Dirección: "Cierra Feature X, prepara PR"
├─ Espejo Diario se AJUSTA:
│  └─ Bloque 17:30-18:30 se añade: "Preparar PR"
└─ Plan del día se completa

MIÉRCOLES 9 OCT (20:02 - Maghrib)
├─ Estado Cero: Reflexión
├─ Ritual Maghrib: Preparar Jueves
└─ Ciclo se repite
```

---

## 🛠️ **Implementación Técnica**

### **Lo que YA tenemos** ✅

```
✅ Entrelazador: Genera dashboard semanal
✅ Orquestador: Genera plan diario
✅ Google Calendar: Crea eventos
✅ Tiempos precisos: Astronómicos
✅ Estado Cero: Genera direcciones
```

### **Lo que FALTA** ⏸️

```
⏸️ Correspondencia explícita Entrelazador → Orquestador
⏸️ Actualización incremental del Espejo
⏸️ Visualización de espacio libre (40%)
⏸️ Sincronización en tiempo real
⏸️ Botones de navegación Estado Cero → Espejo
```

---

## 📋 **Necesitamos Implementar**

### **1. Método de Correspondencia** ⏱️ 2h

```python
# backend/agentes/orquestador.py

async def generar_plan_con_estructura_semanal(
    self,
    intencion: str,
    fecha: date,
    entrelazador: AgenteEntrelazador
):
    """
    Genera plan diario BASADO en estructura semanal
    """
    
    # 1. Obtener estructura del día desde Entrelazador
    estructura_dia = entrelazador.obtener_estructura_dia(fecha)
    
    # 2. Obtener tiempos litúrgicos precisos
    tiempos = self.calculador_tiempos.calcular_tiempos_hoy(fecha)
    
    # 3. Crear bloques base (no-negociables + rutinas)
    bloques_base = []
    
    # No-negociables del Entrelazador
    for no_neg in estructura_dia.no_negociables:
        bloques_base.append({
            "tipo": "no_negociable",
            "actividad": no_neg,
            "flexible": False,
            "origen": "entrelazador"
        })
    
    # Rutinas deportivas
    for deporte in estructura_dia.deportes_hoy:
        bloques_base.append({
            "tipo": "rutina",
            "actividad": deporte.nombre,
            "inicio": deporte.hora_preferida,
            "duracion": deporte.duracion_minutos,
            "flexible": False,
            "origen": "entrelazador"
        })
    
    # 4. Generar bloques emergentes basados en intención
    bloques_emergentes = await self._generar_bloques_emergentes(
        intencion=intencion,
        bloques_base=bloques_base,
        tiempo_disponible=estructura_dia.tiempo_libre
    )
    
    # 5. Combinar todo
    plan = JornadaAlBordeCaos(
        fecha=fecha,
        intencion=intencion,
        bloques_sugeridos=bloques_base + bloques_emergentes,
        no_negociables=estructura_dia.no_negociables,
        espacio_libre_porcentaje=40
    )
    
    return plan
```

### **2. Actualización Incremental del Espejo** ⏱️ 3h

```python
# backend/agentes/orquestador.py

async def actualizar_espejo_con_estado_cero(
    self,
    plan_actual: JornadaAlBordeCaos,
    direccion_emergente: str,
    momento: MomentoLiturgico
):
    """
    Actualiza el plan del día basándose en Estado Cero
    """
    
    # 1. Analizar dirección emergente
    ajustes = await self._analizar_direccion(direccion_emergente)
    
    # 2. Ajustar bloques según momento del día
    if momento == MomentoLiturgico.FAJR:
        # Refinar plan completo del día
        plan_actualizado = await self._refinar_plan_completo(
            plan_actual, 
            ajustes
        )
    
    elif momento == MomentoLiturgico.DHUHR:
        # Ajustar solo bloques de tarde
        plan_actualizado = await self._ajustar_tarde(
            plan_actual,
            ajustes
        )
    
    elif momento == MomentoLiturgico.ASR:
        # Completar ciclos abiertos
        plan_actualizado = await self._completar_ciclos(
            plan_actual,
            ajustes
        )
    
    # 3. Mantener no-negociables intactos
    plan_actualizado.no_negociables = plan_actual.no_negociables
    
    return plan_actualizado
```

### **3. Frontend - Espejo con Actualización** ⏱️ 4h

```svelte
<!-- frontend/src/routes/espejo-sagrado/+page.svelte -->

<script lang="ts">
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  
  let planDia = null;
  let ultimaActualizacion = null;
  let estadosCeroHoy = [];
  
  onMount(async () => {
    // Cargar plan del día
    planDia = await cargarPlanDia();
    
    // Cargar Estados Cero completados hoy
    estadosCeroHoy = await cargarEstadosCeroHoy();
    
    // Polling cada 30 segundos para actualizaciones
    setInterval(verificarActualizaciones, 30000);
  });
  
  async function verificarActualizaciones() {
    const nuevosEstados = await cargarEstadosCeroHoy();
    
    if (nuevosEstados.length > estadosCeroHoy.length) {
      // Hay nuevo Estado Cero
      const ultimoEstado = nuevosEstados[nuevosEstados.length - 1];
      
      // Actualizar plan con nueva dirección
      planDia = await actualizarPlanConEstadoCero(
        planDia,
        ultimoEstado
      );
      
      estadosCeroHoy = nuevosEstados;
      ultimaActualizacion = new Date();
      
      // Mostrar notificación
      mostrarNotificacion("Espejo actualizado con dirección de " + ultimoEstado.momento);
    }
  }
</script>

<div class="espejo-sagrado">
  <!-- Intención del día -->
  <section class="intencion-principal">
    <h1>{planDia.intencion}</h1>
    {#if ultimaActualizacion}
      <p class="ultima-actualizacion">
        Actualizado: {ultimaActualizacion.toLocaleTimeString()}
      </p>
    {/if}
  </section>
  
  <!-- Timeline del día -->
  <section class="timeline-dia">
    {#each planDia.bloques as bloque}
      <div class="bloque" class:no-negociable={bloque.tipo === 'no_negociable'}>
        <!-- Visualización del bloque -->
      </div>
    {/each}
  </section>
  
  <!-- Espacio libre visualizado -->
  <section class="espacio-emergente">
    <h3>Espacio Emergente (40%)</h3>
    <div class="visualizacion-libre">
      <!-- Mostrar horas libres -->
    </div>
  </section>
  
  <!-- Estados Cero del día -->
  <section class="estados-cero-completados">
    {#each estadosCeroHoy as estado}
      <div class="estado-card">
        <h4>{estado.momento}</h4>
        <p>{estado.direccion_emergente}</p>
      </div>
    {/each}
  </section>
</div>
```

---

## 🎨 **Visualización de Correspondencia**

### **Colores y Símbolos**

```
⚓ No-negociables    Verde oscuro   (anclas, no se mueven)
🌊 Bloques flexibles Azul           (pueden moverse)
💻 Trabajo profundo  Naranja        (requiere energía alta)
📚 Aprendizaje       Morado         (crecimiento)
🏃 Rutinas           Verde claro    (hábitos)
🕌 Estados Cero     Según momento   (rituales sagrados)
🌫️ Espacio libre    Gris suave     (40%, emergente)
```

### **Intensidad Visual**

```
Energía requerida:
🔥     (1/5) - Baja
🔥🔥   (2/5) - Media-baja
🔥🔥🔥 (3/5) - Media
🔥🔥🔥🔥 (4/5) - Alta
🔥🔥🔥🔥🔥 (5/5) - Muy alta

Flexibilidad:
⚓ Anclado (no mover)
🌊 Flexible (puede ajustarse)
```

---

## 📊 **Resumen de Correspondencia**

```
┌─────────────────────────────────────────────────────────────┐
│                    DOMINGO NOCHE                            │
│              ENTRELAZADOR (Estrategia)                      │
│  • Genera estructura semanal                                │
│  • Distribuye rutinas, proyectos, aprendizaje              │
│  • Detecta conflictos y sinergias                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  CADA NOCHE (MAGHRIB)                       │
│              ORQUESTADOR (Táctica)                          │
│  • Toma intención del usuario                               │
│  • Consulta estructura semanal                              │
│  • Genera plan emergente del día                            │
│  • Respeta no-negociables                                   │
│  • Mantiene 40% libre                                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 GOOGLE CALENDAR                             │
│  • 5 Estados Cero (tiempos precisos)                        │
│  • No-negociables (anclas)                                  │
│  • Bloques de trabajo                                       │
│  • Rutinas                                                  │
│  • Invitaciones a asistentes                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              DURANTE EL DÍA (5 Estados Cero)                │
│  • Cada Estado Cero refina el plan                          │
│  • Espejo Diario se actualiza                               │
│  • Ajustes en tiempo real                                   │
│  • 40% espacio para lo emergente                            │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ **Lo que Necesitamos**

### **Backend** (2-3 horas)

1. Método `orquestador.generar_plan_con_estructura_semanal()`
2. Método `orquestador.actualizar_espejo_con_estado_cero()`
3. Endpoint `/api/espejo-diario/actualizar`
4. Integración Entrelazador ↔ Orquestador

### **Frontend** (4-5 horas)

1. Actualizar `espejo-sagrado/+page.svelte`
2. Polling para actualizaciones en tiempo real
3. Visualización de espacio libre (40%)
4. Botón "Ver Espejo" después de Estado Cero
5. Timeline vertical con bloques de colores

### **Google Calendar** (1 hora)

1. Usar tiempos litúrgicos precisos (ya implementado)
2. Actualizar eventos cuando Espejo cambia (opcional)

---

🕌 **¿Empezamos con la correspondencia Entrelazador ↔ Orquestador?**

Esto es el núcleo de cómo el calendario se diseña correctamente.
