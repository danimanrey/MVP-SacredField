# 🏗️ Plan Tangible: Arquitectura Dual MVP

**Fecha:** 10 de octubre, 2025  
**Validación:** ✅ Arquitectura correcta y brillante  
**Prioridad:** Estado Cero en 3000 → Ejecución en 5173

---

## 🎯 Arquitectura Validada

### **Puerto 3000 (Next.js) - DIVULGACIÓN**
- Estado Cero inmersivo (asombro, cuestionamiento)
- Gratuito, cara al cliente
- No-negociables + configuración individual
- Genera actividades propuestas
- Usuario valida/modifica
- **Output:** Documentación → pasa a 5173

### **Puerto 5173 (Svelte) - EJECUCIÓN**
- Espejo Diario ejecutivo
- Dashboard analítico de salud
- Gestión táctica del reino
- Añade eventos al calendario
- Integración Anytype
- APIs técnicas y operativas

### **Maghrib - VALIDACIÓN**
- Se valida salud del organismo
- Sistema descansa

---

## 📅 Plan de Implementación Tangible

### **FASE 1: Estado Cero en 3000 (PRIORIDAD)** ⏰ 3-5 días

#### **Día 1: Setup Next.js + Migración Base**

**QUÉ:**
- Crear proyecto Next.js en puerto 3000
- Configurar TypeScript + Tailwind
- Instalar React Three Fiber (R3F) para 3D
- Crear estructura básica

**CÓMO:**
```bash
# Crear proyecto
cd "/Users/hp/Campo sagrado MVP"
npx create-next-app@latest campo-sagrado-nextjs --typescript --tailwind --app

# Mover a puerto 3000
cd campo-sagrado-nextjs
# Editar package.json: "dev": "next dev -p 3000"

# Instalar dependencias inmersivas
npm install three @react-three/fiber @react-three/drei
npm install framer-motion lucide-react
npm install zustand
```

**Estructura:**
```
campo-sagrado-nextjs/
├── app/
│   ├── page.tsx                 # Landing inmersivo
│   ├── estado-cero/
│   │   ├── page.tsx             # Estado Cero principal
│   │   └── components/
│   │       ├── UniversoEsferico.tsx
│   │       ├── PreguntasSacrales.tsx
│   │       └── DireccionEmergente.tsx
│   └── layout.tsx
├── lib/
│   ├── api-client.ts            # Cliente para backend:8000
│   └── stores/
│       └── estado-cero-store.ts # Zustand store
└── public/
    └── sounds/                  # Audio generativo (futuro)
```

**Salida esperada:**
✅ Proyecto Next.js funcionando en `localhost:3000`

---

#### **Día 2: Estado Cero Inmersivo (Core)**

**QUÉ:**
- Componente UniversoEsferico con R3F
- Esfera/cubo animados
- Transiciones suaves
- Integración con backend

**CÓMO:**

**1. Crear API Client:**
```typescript
// lib/api-client.ts
const API_BASE = 'http://localhost:8000/api';

export const estadoCeroAPI = {
  verificarMomento: () => fetch(`${API_BASE}/estado-cero/verificar`),
  iniciar: (momento: string) => fetch(`${API_BASE}/estado-cero/iniciar`, {
    method: 'POST',
    body: JSON.stringify({ momento_liturgico: momento })
  }),
  responder: (id: string, respuesta: any) => 
    fetch(`${API_BASE}/estado-cero/${id}/responder`, {
      method: 'POST',
      body: JSON.stringify(respuesta)
    }),
  sintetizar: (id: string) => 
    fetch(`${API_BASE}/estado-cero/${id}/sintetizar`, { method: 'POST' }),
  finalizar: (id: string, accion: any) => 
    fetch(`${API_BASE}/estado-cero/${id}/finalizar`, {
      method: 'POST',
      body: JSON.stringify(accion)
    })
};
```

**2. Crear Universo 3D:**
```typescript
// app/estado-cero/components/UniversoEsferico.tsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Sphere, Box } from '@react-three/drei';

export default function UniversoEsferico({ fase }) {
  return (
    <Canvas camera={{ position: [0, 0, 5] }}>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      
      {/* Esfera */}
      <Sphere args={[1, 32, 32]} visible={fase === 'esfera'}>
        <meshStandardMaterial 
          color="#8B5CF6" 
          wireframe 
          transparent 
          opacity={0.6} 
        />
      </Sphere>
      
      {/* Cubo */}
      <Box args={[2, 2, 2]} visible={fase === 'cubo'}>
        <meshStandardMaterial color="#3B82F6" wireframe />
      </Box>
      
      {/* Estrellas de fondo */}
      <Stars radius={100} depth={50} count={5000} factor={4} />
    </Canvas>
  );
}
```

**3. Flujo de Fases:**
```typescript
// app/estado-cero/page.tsx
const fases = [
  'entrada',      // Respiración + esfera
  'expansion',    // Esfera crece
  'preguntas',    // Preguntas emergen
  'sintesis',     // Dirección emergente
  'validacion',   // Usuario valida
  'documentacion' // Se genera doc
];
```

**Salida esperada:**
✅ Estado Cero inmersivo funcional con 3D

---

#### **Día 3: No-Negociables + Configuración**

**QUÉ:**
- Wizard de configuración inicial
- No-negociables por defecto
- Personalización del individuo

**CÓMO:**

**1. Crear modelo de configuración:**
```typescript
// lib/types.ts
interface ConfiguracionIndividual {
  no_negociables: {
    fajr_estado_cero: boolean;      // true por defecto
    dhuhr_estado_cero: boolean;     // true por defecto
    asr_estado_cero: boolean;       // false por defecto
    maghrib_validacion: boolean;    // true por defecto
    isha_estado_cero: boolean;      // false por defecto
  };
  dimensiones_prioritarias: string[]; // ['finanzas', 'biologia', ...]
  energia_disponible: 1 | 2 | 3 | 4 | 5;
  contexto_financiero: {
    runway_meses: number;
    urgencia: boolean;
  };
  contexto_biologico: {
    patron_sueno: string;
    nivel_energia: number;
  };
  expresion_libre: string; // Campo abierto
}
```

**2. Wizard de onboarding:**
```typescript
// app/onboarding/page.tsx
<OnboardingWizard>
  <Paso1 title="Bienvenido al Campo Sagrado">
    <p>Este organismo respeta tu autoridad sacral...</p>
  </Paso1>
  
  <Paso2 title="No-Negociables">
    <Toggle defaultOn label="Estado Cero Fajr (amanecer)" />
    <Toggle defaultOn label="Estado Cero Dhuhr (mediodía)" />
    <Toggle defaultOff label="Estado Cero Asr (tarde)" />
    <Toggle defaultOn label="Validación Maghrib (atardecer)" />
  </Paso2>
  
  <Paso3 title="Tu Configuración">
    <Input label="Runway financiero (meses)" type="number" />
    <Slider label="Energía disponible" min={1} max={5} />
    <MultiSelect label="Dimensiones prioritarias" options={dimensiones} />
  </Paso3>
  
  <Paso4 title="Expresión Libre">
    <Textarea placeholder="Comparte lo que necesites expresar..." />
  </Paso4>
</OnboardingWizard>
```

**Salida esperada:**
✅ Configuración individual guardada en backend

---

#### **Día 4: Generación de Actividades + Validación**

**QUÉ:**
- Procesar información sin prisa
- Generar actividades propuestas
- Usuario valida/modifica
- Generar documentación

**CÓMO:**

**1. Endpoint nuevo en backend:**
```python
# backend/api/planificacion.py
@router.post("/generar-plan-dia")
async def generar_plan_dia(
    estado_cero_id: str,
    configuracion: ConfiguracionIndividual,
    db: Session = Depends(get_db)
):
    """
    Genera plan del día basado en:
    - Estado Cero completado
    - Configuración individual
    - Contexto temporal
    """
    # 1. Obtener Estado Cero
    estado = obtener_estado_cero(estado_cero_id, db)
    
    # 2. Generar actividades con Claude
    prompt = f"""
    Basándote en:
    - Dirección emergente: {estado.direccion_emergente}
    - Acción tangible: {estado.accion_tangible}
    - Runway: {configuracion.runway_meses} meses
    - Energía: {configuracion.energia_disponible}/5
    - Prioridades: {configuracion.dimensiones_prioritarias}
    
    Genera 3-5 actividades concretas para HOY.
    Formato: título, duración, energía, momento sugerido
    """
    
    actividades = await claude.generar(prompt)
    
    # 3. Retornar para validación
    return {
        "actividades_propuestas": actividades,
        "requiere_validacion": True
    }

@router.post("/validar-plan")
async def validar_plan(
    plan_id: str,
    actividades_validadas: List[Actividad],
    db: Session = Depends(get_db)
):
    """
    Usuario valida/modifica actividades
    """
    # 1. Guardar actividades en DB
    for actividad in actividades_validadas:
        crear_actividad(actividad, db)
    
    # 2. Generar documentación en Obsidian
    documentador = AgenteDocumentador(db, claude, vault_path)
    archivo = await documentador.documentar_plan_dia(actividades_validadas)
    
    # 3. Añadir eventos al Google Calendar
    calendar = GoogleCalendarService()
    for actividad in actividades_validadas:
        calendar.crear_evento(actividad)
    
    return {
        "status": "plan_validado",
        "archivo_path": archivo,
        "eventos_creados": len(actividades_validadas),
        "siguiente_paso": "abrir_puerto_5173_para_ejecutar"
    }
```

**2. Componente de validación en 3000:**
```typescript
// app/estado-cero/validacion/page.tsx
<ValidacionPlan>
  {actividades.map(actividad => (
    <ActividadCard key={actividad.id} editable>
      <Input value={actividad.titulo} onChange={...} />
      <TimeSelect value={actividad.hora} onChange={...} />
      <DuracionSlider value={actividad.duracion} onChange={...} />
      <DimensionBadge dimension={actividad.dimension} />
      <Button variant="eliminar">✕</Button>
    </ActividadCard>
  ))}
  
  <Button onClick={agregarActividad}>+ Agregar actividad</Button>
  
  <Button variant="primary" onClick={validarYGenerar}>
    ✓ Validar y Generar Documentación
  </Button>
</ValidacionPlan>
```

**Salida esperada:**
✅ Plan validado
✅ Documentación generada en Obsidian
✅ Eventos añadidos a Google Calendar
✅ **Trabajo del puerto 3000 COMPLETADO**

---

### **FASE 2: Espejo Diario en 5173 (EJECUCIÓN)** ⏰ 2-3 días

#### **Día 5: Dashboard Ejecutivo**

**QUÉ:**
- Tabla dinámica de actividades del día
- Tracking de completadas
- Salud del organismo
- Gestión táctica

**CÓMO:**

**1. Mejorar Espejo Diario existente:**
```typescript
// frontend/src/routes/espejo-diario/+page.svelte (ya existe, mejorar)

<section class="dashboard-ejecutivo">
  <!-- Salud del Organismo -->
  <HealthWidget>
    <MetricBar label="Energía" value={4} max={5} color="#22C55E" />
    <MetricBar label="Claridad mental" value={3} max={5} color="#3B82F6" />
    <MetricBar label="Runway" value={6} max={12} color="#DC2626" />
  </HealthWidget>
  
  <!-- Actividades del Día -->
  <ActividadesTable>
    <thead>
      <tr>
        <th>Hora</th>
        <th>Actividad</th>
        <th>Dimensión</th>
        <th>Duración</th>
        <th>Estado</th>
        <th>Acciones</th>
      </tr>
    </thead>
    <tbody>
      {#each actividades as act}
        <tr class:completada={act.completada}>
          <td>{act.hora}</td>
          <td>{act.titulo}</td>
          <td><Badge color={act.dimension_color}>{act.dimension}</Badge></td>
          <td>{act.duracion}min</td>
          <td>
            <Checkbox 
              checked={act.completada} 
              onChange={() => marcarCompletada(act.id)}
            />
          </td>
          <td>
            <Button size="sm" onClick={() => editarActividad(act)}>✏️</Button>
            <Button size="sm" onClick={() => eliminarActividad(act)}>🗑️</Button>
          </td>
        </tr>
      {/each}
    </tbody>
  </ActividadesTable>
  
  <!-- Al borde del caos: 40% sin asignar -->
  <EspacioEmergente>
    <p>40% del día sin asignar para lo emergente</p>
    <Canvas>
      <!-- Visualización no-lineal del tiempo -->
    </Canvas>
  </EspacioEmergente>
</section>
```

**2. Integración con Google Calendar:**
```typescript
// lib/calendar-sync.ts
export async function sincronizarCalendario() {
  const eventos = await fetch('http://localhost:8000/api/calendario/hoy');
  // Actualizar tabla automáticamente
  actualizarActividades(eventos);
}

// Polling cada 5 minutos
setInterval(sincronizarCalendario, 5 * 60 * 1000);
```

**Salida esperada:**
✅ Dashboard ejecutivo funcional
✅ Sincronización con calendario
✅ Tracking de actividades

---

#### **Día 6: Integración Anytype (Placeholder)**

**QUÉ:**
- Preparar integración con Anytype
- Botón para "Abrir en Anytype"
- Visual orientado a objetos

**CÓMO:**

```typescript
// frontend/src/routes/espejo-diario/+page.svelte

<Button onClick={abrirEnAnytype}>
  📦 Ver en Anytype (orientado a objetos)
</Button>

// Función
async function abrirEnAnytype() {
  // Por ahora, preparar el payload
  const payload = {
    actividades: actividades,
    tipo: 'plan-dia',
    fecha: new Date().toISOString()
  };
  
  // TODO: Implementar Anytype API cuando esté lista
  console.log('Payload para Anytype:', payload);
  
  // Placeholder: abrir en nueva pestaña
  window.open('https://anytype.io', '_blank');
}
```

**Salida esperada:**
✅ Preparación para Anytype (futuro)

---

### **FASE 3: Validación Maghrib** ⏰ 1 día

#### **Día 7: Ritual Maghrib Mejorado**

**QUÉ:**
- Validación de salud del organismo
- Revisión del día
- Sistema descansa

**CÓMO:**

**1. Mejorar endpoint existente:**
```python
# backend/api/ritual_maghrib.py (ya existe, mejorar)

@router.post("/validar-salud")
async def validar_salud_organismo(
    db: Session = Depends(get_db)
):
    """
    Valida salud del organismo al final del día
    """
    # 1. Obtener actividades del día
    actividades = obtener_actividades_hoy(db)
    completadas = [a for a in actividades if a.completada]
    
    # 2. Calcular métricas
    tasa_completitud = len(completadas) / len(actividades) if actividades else 0
    
    # 3. Analizar balance de dimensiones
    dimensiones_trabajadas = Counter([a.dimension for a in completadas])
    
    # 4. Generar insights con Claude
    prompt = f"""
    Día completado:
    - Actividades: {len(completadas)}/{len(actividades)}
    - Dimensiones trabajadas: {dict(dimensiones_trabajadas)}
    
    Genera 3 insights breves sobre la salud del organismo.
    """
    
    insights = await claude.generar(prompt)
    
    # 5. Guardar en DB
    validacion = ValidacionMaghrib(
        fecha=date.today(),
        tasa_completitud=tasa_completitud,
        insights=insights,
        estado_salud="saludable" if tasa_completitud > 0.6 else "necesita_atencion"
    )
    db.add(validacion)
    db.commit()
    
    return {
        "estado_salud": validacion.estado_salud,
        "tasa_completitud": tasa_completitud,
        "insights": insights,
        "recomendacion": "El organismo puede descansar" if validacion.estado_salud == "saludable" else "Ajustar mañana"
    }
```

**2. Vista en 5173:**
```svelte
<!-- frontend/src/routes/maghrib/+page.svelte -->

<div class="validacion-maghrib">
  <h1>🌅 Validación Maghrib</h1>
  
  <HealthSummary>
    <CircularProgress value={tasaCompletitud * 100} />
    <p>{(tasaCompletitud * 100).toFixed(0)}% del día completado</p>
  </HealthSummary>
  
  <InsightsSection>
    {#each insights as insight}
      <InsightCard>{insight}</InsightCard>
    {/each}
  </InsightsSection>
  
  <RecomendacionFinal estado={estadoSalud}>
    {#if estadoSalud === 'saludable'}
      <p>✅ El organismo está saludable. Puede descansar.</p>
    {:else}
      <p>⚠️ Necesita atención. Ajustar mañana en Estado Cero.</p>
    {/if}
  </RecomendacionFinal>
  
  <Button onClick={cerrarDia}>🌙 Cerrar día y descansar</Button>
</div>
```

**Salida esperada:**
✅ Validación Maghrib funcional
✅ Insights automáticos
✅ Sistema preparado para descansar

---

## 📊 Resumen de Entregas

### **Semana 1: Fundación (Días 1-7)**

| Día | Entrega | Puerto | Estado |
|-----|---------|--------|--------|
| 1 | Setup Next.js + estructura | 3000 | ⏳ Por hacer |
| 2 | Estado Cero inmersivo 3D | 3000 | ⏳ Por hacer |
| 3 | No-negociables + configuración | 3000 | ⏳ Por hacer |
| 4 | Generación + validación actividades | 3000 + Backend | ⏳ Por hacer |
| 5 | Dashboard ejecutivo mejorado | 5173 | ⏳ Por hacer |
| 6 | Preparación Anytype | 5173 | ⏳ Por hacer |
| 7 | Validación Maghrib | 5173 + Backend | ⏳ Por hacer |

### **Al Final de la Semana:**

✅ **Puerto 3000 funcional:**
- Estado Cero inmersivo completo
- Configuración individual
- Generación de actividades
- Validación del usuario
- Documentación automática

✅ **Puerto 5173 funcional:**
- Dashboard ejecutivo
- Tracking de actividades
- Integración calendario
- Validación Maghrib

✅ **Backend completo:**
- Endpoints de planificación
- Documentador extendido
- Google Calendar sync
- Validación de salud

---

## 🚀 Próximos Pasos (Post-MVP)

### **Prioridad Media (Semanas 2-4):**
1. **Software de escritura soberana**
   - Diferenciación IA vs humano
   - Validación de autoría
   - Firma digital

2. **Extensión de finanzas**
   - Tracking de ingresos/gastos
   - Proyecciones de runway
   - Alertas de urgencia

### **Prioridad Baja (Meses 2-3):**
1. Anytype full integration
2. Modo empresa (entrelazamiento)
3. Audio generativo (Tone.js)
4. Visualización 3D del universo imaginal

---

## 🎯 Checklist de Validación MVP

### **Flujo Completo:**
- [ ] Usuario entra a `localhost:3000`
- [ ] Hace Estado Cero inmersivo
- [ ] Configura no-negociables
- [ ] Recibe actividades propuestas
- [ ] Valida y modifica
- [ ] Se genera documentación en Obsidian
- [ ] Eventos se añaden a Google Calendar
- [ ] Abre `localhost:5173` (Espejo Diario)
- [ ] Ve actividades del día en tabla
- [ ] Marca actividades como completadas
- [ ] Al Maghrib, valida salud del organismo
- [ ] Sistema descansa

---

## 💎 Validación de Arquitectura

**TU ARQUITECTURA ES:**
✅ **Clara** - Separación perfecta de concerns  
✅ **Pragmática** - Divulgación vs Ejecución  
✅ **Escalable** - Cada puerto tiene su rol  
✅ **Soberana** - Respeta autoridad del individuo  
✅ **Al borde del caos** - 40% sin asignar  

**ES CORRECTA PARA EL MVP. ✅**

---

## 🛠️ Comandos de Inicio (Cuando esté listo)

```bash
# Iniciar todo el sistema
cd "/Users/hp/Campo sagrado MVP"

# Terminal 1: Backend
cd backend && source venv/bin/activate && python run.py

# Terminal 2: Frontend Ejecutivo (5173)
cd frontend && npm run dev

# Terminal 3: Frontend Inmersivo (3000)
cd campo-sagrado-nextjs && npm run dev

# Abrir navegadores
open http://localhost:3000  # Divulgación
open http://localhost:5173  # Ejecución
```

---

**Arquitectura validada. Plan tangible entregado.**

**Adelante con el MVP. إن شاء الله 🕌✨**

