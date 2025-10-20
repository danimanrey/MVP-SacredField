# 🚀 PLAN DE MIGRACIÓN: SvelteKit → Next.js 14 + React Three Fiber

**Objetivo**: Crear interfaz etérea de vanguardia a la altura de la filosofía  
**Duración**: 6-8 semanas  
**Enfoque**: Precisión quirúrgica, sin desperdiciar esfuerzo

---

## 📋 FASE 0: DOCUMENTACIÓN Y PREPARACIÓN (Semana 1)

### Tarea 1.1: Documentar Sistema Actual ✅ EN PROGRESO
**Duración**: 2 días

**Archivos a crear**:
```
docs/
  GUIA_USUARIO_COMPLETA.md
  ARQUITECTURA_TECNICA.md
  API_REFERENCE.md
  FILOSOFIA_Y_PRINCIPIOS.md
```

**Contenido crítico**:
- [ ] Flujo completo: Maghrib → Estados Cero → Espejo Diario
- [ ] Cómo definir objetivos en las 7 dimensiones
- [ ] Cómo aplicar shocks conscientes
- [ ] Todas las APIs documentadas
- [ ] Decisiones de arquitectura explicadas

### Tarea 1.2: Backup y Git
**Duración**: 1 día

```bash
# Crear branch de SvelteKit
git checkout -b sveltekit-mvp-final
git add .
git commit -m "✅ MVP SvelteKit completo - Base para migración"
git tag v0.1.0-mvp-sveltekit

# Crear branch para Next.js
git checkout -b nextjs-migration
```

### Tarea 1.3: Análisis de Componentes
**Duración**: 1 día

**Mapear componentes**:
```
SvelteKit (Actual)          →    Next.js + R3F (Destino)
─────────────────────────────────────────────────────────────
Navegacion.svelte           →    Navigation.tsx (Shadcn)
EspejoDinamico.svelte       →    EspejoDiario3D.tsx (R3F)
VistaSemanal.svelte         →    CirculoSemanal3D.tsx (R3F)
VistaAnual.svelte           →    CalendarioOrbital3D.tsx (R3F)
GeometriaSagrada.svelte     →    GeometriaSagradaShader.tsx
DashboardOctavas.svelte     →    EspiralOctavas3D.tsx (R3F)
```

**Priorización**:
1. ⭐⭐⭐ Espiral 3D (core visual)
2. ⭐⭐⭐ Timeline vertical 3D
3. ⭐⭐⭐ Navegación única (sin menú)
4. ⭐⭐ Calendario orbital
5. ⭐⭐ Geometría sagrada
6. ⭐ Audio generativo

---

## 📋 FASE 1: SETUP Y PROTOTIPO (Semana 2-3)

### Tarea 2.1: Crear Proyecto Next.js
**Duración**: 2 horas

```bash
# En el mismo directorio raíz
npx create-next-app@latest campo-sagrado-nextjs \
  --typescript \
  --tailwind \
  --app \
  --src-dir \
  --import-alias "@/*"

cd campo-sagrado-nextjs
```

### Tarea 2.2: Instalar Dependencias Core
**Duración**: 1 hora

```bash
# 3D y WebGL
npm install three @react-three/fiber @react-three/drei
npm install @react-three/rapier  # Física
npm install @react-three/postprocessing  # Shaders
npm install lamina  # Materiales procedurales
npm install maath  # Math helpers para 3D

# Animaciones
npm install framer-motion
npm install gsap @gsap/react

# UI Components
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card dialog tabs scroll-area

# Estado
npm install zustand
npm install @tanstack/react-query

# Audio
npm install tone
npm install howler

# Visualización de datos
npm install d3
npm install recharts

# Utils
npm install date-fns
npm install clsx tailwind-merge
npm install lucide-react  # Iconos
```

### Tarea 2.3: Setup Shadcn/ui
**Duración**: 1 hora

```bash
# Inicializar
npx shadcn-ui@latest init

# Responder:
# - TypeScript: Yes
# - Style: Default
# - Color: Slate
# - CSS variables: Yes

# Instalar componentes base
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add scroll-area
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add separator
```

### Tarea 2.4: Estructura de Carpetas
**Duración**: 30 min

```
campo-sagrado-nextjs/
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Layout principal
│   │   ├── page.tsx                # Home (scroll único)
│   │   ├── globals.css
│   │   └── api/                    # Proxy a backend Python
│   │       └── [...]/route.ts
│   ├── components/
│   │   ├── ui/                     # Shadcn components
│   │   ├── 3d/                     # Componentes 3D
│   │   │   ├── EspiralCosmica.tsx
│   │   │   ├── TimelineVertical3D.tsx
│   │   │   ├── CalendarioOrbital.tsx
│   │   │   └── GeometriaSagrada.tsx
│   │   ├── sections/               # Secciones del scroll único
│   │   │   ├── Hero.tsx
│   │   │   ├── ContextoTemporal.tsx
│   │   │   ├── EspejoDiario.tsx
│   │   │   ├── ObjetivosOctava.tsx
│   │   │   └── VistasSemanalAnual.tsx
│   │   └── shared/
│   │       ├── Navigation.tsx
│   │       └── AudioContexto.tsx
│   ├── lib/
│   │   ├── api.ts                  # Cliente API
│   │   ├── stores.ts               # Zustand stores
│   │   └── utils.ts
│   └── hooks/
│       ├── useApi.ts
│       ├── useAudio.ts
│       └── use3D.ts
├── public/
│   ├── sounds/                     # Sonidos litúrgicos
│   └── textures/                   # Texturas 3D
├── package.json
├── next.config.js
├── tailwind.config.ts
└── tsconfig.json
```

---

## 📋 FASE 2: PROTOTIPO CORE (Semana 3-4)

### Tarea 3.1: Espiral Cósmica 3D ⭐ PRIORIDAD 1
**Duración**: 3-4 días

**Archivo**: `src/components/3d/EspiralCosmica.tsx`

```tsx
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Line, Sphere } from '@react-three/drei';
import * as THREE from 'three';

export function EspiralCosmica({ objetivos }) {
  const groupRef = useRef();
  
  // Rotación suave continua
  useFrame((state, delta) => {
    groupRef.current.rotation.y += delta * 0.1;
  });
  
  // Generar puntos de la espiral
  const puntos = [];
  const notas = ['do', 're', 'mi', 'fa', 'sol', 'la', 'si'];
  const colores = {
    do: '#DC2626', re: '#F97316', mi: '#F59E0B',
    fa: '#10B981', sol: '#3B82F6', la: '#6366F1', si: '#8B5CF6'
  };
  
  for (let octava = 1; octava <= 5; octava++) {
    const radio = octava * 2;
    for (let i = 0; i < 7; i++) {
      const angulo = (i / 7) * Math.PI * 2;
      const altura = octava * 1.5;
      
      puntos.push({
        posicion: [
          Math.cos(angulo) * radio,
          altura,
          Math.sin(angulo) * radio
        ],
        color: colores[notas[i]],
        nota: notas[i],
        octava
      });
    }
  }
  
  return (
    <group ref={groupRef}>
      {/* Línea de la espiral */}
      <Line
        points={puntos.map(p => p.posicion)}
        color="white"
        lineWidth={2}
        opacity={0.5}
      />
      
      {/* Esferas en cada nota */}
      {puntos.map((punto, i) => (
        <Sphere
          key={i}
          args={[0.1, 32, 32]}
          position={punto.posicion}
        >
          <meshStandardMaterial
            color={punto.color}
            emissive={punto.color}
            emissiveIntensity={0.5}
          />
        </Sphere>
      ))}
      
      {/* Partículas flotantes */}
      <Particulas count={500} />
    </group>
  );
}
```

**Features**:
- ✅ Espiral 3D ascendente
- ✅ 7 colores del arcoíris
- ✅ Rotación suave automática
- ✅ Esferas brillantes (emissive)
- ✅ 500 partículas flotando

### Tarea 3.2: Timeline Vertical del Día en 3D
**Duración**: 3-4 días

**Archivo**: `src/components/3d/TimelineVertical3D.tsx`

```tsx
import { useRef, useMemo } from 'react';
import { Box, Text } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

export function TimelineVertical3D({ bloquesDia, horaActual }) {
  const timelineRef = useRef();
  
  // Bloques del día como cajas 3D flotantes
  return (
    <group ref={timelineRef} position={[5, 0, 0]}>
      {bloquesDia.map((bloque, i) => {
        const y = -(i * 0.5); // Espaciado vertical
        const esAhora = bloque.es_ahora;
        
        return (
          <group key={bloque.id} position={[0, y, 0]}>
            {/* Caja del bloque */}
            <Box args={[2, 0.3, 0.5]}>
              <meshStandardMaterial
                color={esAhora ? '#10b981' : bloque.color}
                emissive={esAhora ? '#10b981' : '#000000'}
                emissiveIntensity={esAhora ? 0.5 : 0}
              />
            </Box>
            
            {/* Texto flotante */}
            <Text
              position={[0, 0.3, 0]}
              fontSize={0.1}
              color="white"
            >
              {bloque.titulo}
            </Text>
          </group>
        );
      })}
      
      {/* Indicador "AHORA" como gota de luz */}
      <IndicadorAhora horaActual={horaActual} />
    </group>
  );
}
```

### Tarea 3.3: Página Única con Scroll (Layout principal)
**Duración**: 2 días

**Archivo**: `src/app/page.tsx`

```tsx
'use client';

import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars, Environment } from '@react-three/drei';
import { motion, useScroll } from 'framer-motion';
import { EspiralCosmica } from '@/components/3d/EspiralCosmica';
import { Hero } from '@/components/sections/Hero';
import { ContextoTemporal } from '@/components/sections/ContextoTemporal';
import { EspejoDiario } from '@/components/sections/EspejoDiario';

export default function Home() {
  const { scrollYProgress } = useScroll();
  
  return (
    <div className="relative w-full">
      {/* Canvas 3D fijo en background */}
      <div className="fixed inset-0 -z-10">
        <Canvas camera={{ position: [0, 0, 10], fov: 75 }}>
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />
          
          {/* Estrellas de fondo */}
          <Stars radius={100} count={5000} fade speed={2} />
          
          {/* Espiral cósmica principal */}
          <EspiralCosmica />
          
          {/* Entorno HDRI */}
          <Environment preset="night" />
          
          {/* Controles sutiles */}
          <OrbitControls 
            enableZoom={false} 
            autoRotate 
            autoRotateSpeed={0.5}
            enablePan={false}
          />
        </Canvas>
      </div>
      
      {/* Contenido 2D con scroll */}
      <motion.div 
        className="relative z-10"
        style={{ opacity: scrollYProgress }}
      >
        <Hero />
        <ContextoTemporal />
        <EspejoDiario />
        <ObjetivosOctava />
        <VistasSemanalAnual />
      </motion.div>
    </div>
  );
}
```

---

## 📋 FASE 3: COMPONENTES CORE (Semana 4-5)

### Prioridad según Impacto Visual:

#### 1. Espiral 3D de Octavas ⭐⭐⭐⭐⭐
**Impacto**: CRÍTICO (es la pieza central visual)  
**Duración**: 4 días  
**Complejidad**: Alta

**Features**:
- Espiral ascendente con 5+ octavas
- Esferas de colores (objetivos)
- Rotación suave continua
- Click en esfera → Zoom + expansión armónicos
- Partículas siguiendo la espiral
- Shaders de brillo y reflejos

#### 2. Timeline Vertical del Día ⭐⭐⭐⭐⭐
**Impacto**: CRÍTICO (uso diario)  
**Duración**: 4 días  
**Complejidad**: Alta

**Features**:
- Bloques 3D flotando
- Indicador "AHORA" descendiendo
- Tiempos de rezo como anclas luminosas
- Espacio libre como agua fluyendo
- Interactividad (click → detalles)

#### 3. Navegación por Scroll (Sin menú) ⭐⭐⭐⭐
**Impacto**: Alto (UX fundamental)  
**Duración**: 2 días  
**Complejidad**: Media

**Features**:
- Scroll suave entre secciones
- Parallax depth (capas a diferentes velocidades)
- Indicador de progreso sutil
- Gestures (swipe entre secciones)

#### 4. Contexto Temporal Flotante ⭐⭐⭐⭐
**Impacto**: Alto (orientación constante)  
**Duración**: 2 días  
**Complejidad**: Baja

**Features**:
- Card flotante con mes Hijri + día
- Actualización en tiempo real
- Animación de aparición elegante
- Sticky en scroll

#### 5. Círculo Semanal 3D ⭐⭐⭐
**Impacto**: Medio-Alto  
**Duración**: 3 días  
**Complejidad**: Media

**Features**:
- 7 segmentos (colores arcoíris)
- Rotación según día actual
- Hover → Expande segmento
- Click → Navega a ese día

#### 6. Calendario Lunar Orbital ⭐⭐⭐
**Impacto**: Medio-Alto  
**Duración**: 3 días  
**Complejidad**: Alta

**Features**:
- 12 lunas orbitando
- Meses sagrados con aura dorada
- Click → Cámara vuela a ese mes
- Fase lunar real sincronizada

---

## 📋 FASE 4: FEATURES AVANZADAS (Semana 5-6)

### Tarea 6.1: Audio Generativo con Tone.js
**Duración**: 2 días

```tsx
import * as Tone from 'tone';

export function AudioContexto({ notaActual, momento }) {
  useEffect(() => {
    const synth = new Tone.PolySynth().toDestination();
    
    // Tocar la frecuencia del día
    const frecuencias = {
      do: 'C4',   // 261.63 Hz
      re: 'D4',   // 293.66 Hz
      mi: 'E4',   // 329.63 Hz
      fa: 'F4',   // 349.23 Hz
      sol: 'G4',  // 392.00 Hz
      la: 'A4',   // 440.00 Hz
      si: 'B4'    // 493.88 Hz
    };
    
    // Tocar suavemente cada 30s
    const loop = new Tone.Loop((time) => {
      synth.triggerAttackRelease(frecuencias[notaActual], '4n', time);
    }, '30s');
    
    loop.start(0);
    Tone.Transport.start();
    
    return () => {
      loop.stop();
      Tone.Transport.stop();
    };
  }, [notaActual]);
}
```

### Tarea 6.2: Geometría Sagrada con Shaders
**Duración**: 3 días

```tsx
import { useMemo } from 'react';
import { shaderMaterial } from '@react-three/drei';

const GeometriaShader = shaderMaterial(
  { time: 0, color: new THREE.Color(0.2, 0.0, 0.1) },
  // Vertex shader
  `varying vec2 vUv;
   void main() {
     vUv = uv;
     gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
   }`,
  // Fragment shader (Flor de la Vida)
  `uniform float time;
   varying vec2 vUv;
   void main() {
     // Patrón de Flor de la Vida
     vec2 p = vUv * 10.0;
     float pattern = length(fract(p) - 0.5);
     
     vec3 color = vec3(0.5 + 0.5 * cos(time + pattern));
     gl_FragColor = vec4(color, 0.3);
   }`
);

export function Flor dela Vida() {
  const materialRef = useRef();
  
  useFrame((state) => {
    materialRef.current.time = state.clock.elapsedTime;
  });
  
  return (
    <mesh>
      <planeGeometry args={[20, 20]} />
      <geometriaShader ref={materialRef} transparent />
    </mesh>
  );
}
```

### Tarea 6.3: Post-Processing (Bloom, DOF)
**Duración**: 1 día

```tsx
import { EffectComposer, Bloom, DepthOfField } from '@react-three/postprocessing';

<Canvas>
  {/* Scene */}
  <EspiralCosmica />
  
  {/* Post-processing */}
  <EffectComposer>
    <Bloom 
      intensity={1.5} 
      luminanceThreshold={0.9}
      luminanceSmoothing={0.9}
    />
    <DepthOfField 
      focusDistance={0.1}
      focalLength={0.5}
      bokehScale={3}
    />
  </EffectComposer>
</Canvas>
```

---

## 📋 FASE 5: MIGRACIÓN DE LÓGICA (Semana 6-7)

### Componente por Componente:

#### Semana 6:
- [ ] Contexto Temporal → React (1 día)
- [ ] Estado Cero → React (2 días)
- [ ] Espejo Diario → React + 3D (3 días)
- [ ] Navegación → React (1 día)

#### Semana 7:
- [ ] Vista Semanal → Círculo 3D (2 días)
- [ ] Vista Anual → Orbital 3D (3 días)
- [ ] Dimensiones → Cards con animaciones (2 días)

---

## 📋 FASE 6: PULIDO Y OPTIMIZACIÓN (Semana 8)

### Tarea 9.1: Performance
- [ ] Lazy loading de componentes 3D
- [ ] Code splitting por ruta
- [ ] Memoización de cálculos pesados
- [ ] Optimizar shaders

### Tarea 9.2: Responsive
- [ ] Mobile: Simplificar 3D
- [ ] Tablet: Versión intermedia
- [ ] Desktop: Experiencia completa

### Tarea 9.3: Accesibilidad
- [ ] ARIA labels
- [ ] Keyboard navigation
- [ ] Screen reader support

---

## 📊 CRONOGRAMA DETALLADO

```
SEMANA 1: Documentación + Setup
├── Día 1-2: Documentar sistema actual
├── Día 3: Git branching y backup
├── Día 4: Crear proyecto Next.js
├── Día 5: Instalar todas las dependencias
└── Día 6-7: Setup Shadcn/ui + estructura

SEMANA 2-3: Prototipo Core
├── Día 8-11: Espiral 3D completa ⭐
├── Día 12-15: Timeline vertical 3D ⭐
├── Día 16-17: Navegación scroll único
└── Día 18-19: Contexto temporal

SEMANA 4-5: Componentes 3D Avanzados
├── Día 20-21: Círculo semanal 3D
├── Día 22-24: Calendario orbital 3D
├── Día 25-27: Geometría sagrada con shaders
└── Día 28-29: Audio generativo

SEMANA 6-7: Migración de Lógica
├── Día 30-36: Componentes uno por uno
├── Día 37-41: Integración con backend
└── Día 42-43: Testing funcional

SEMANA 8: Pulido Final
├── Día 44-46: Optimización performance
├── Día 47-48: Responsive design
├── Día 49: Testing final
└── Día 50: Deploy y documentación
```

---

## 🎯 HITOS CRÍTICOS (Checkpoints)

### Checkpoint 1: Día 7
**Entregable**: Proyecto Next.js creado con dependencias instaladas  
**Validación**: `npm run dev` funciona

### Checkpoint 2: Día 15
**Entregable**: Espiral 3D + Timeline funcionando  
**Validación**: Experiencia visual superior a SvelteKit

### Checkpoint 3: Día 29
**Entregable**: Todas las piezas 3D funcionando  
**Validación**: WOW factor presente

### Checkpoint 4: Día 43
**Entregable**: Funcionalidad completa migrada  
**Validación**: Paridad funcional con SvelteKit

### Checkpoint 5: Día 50
**Entregable**: Listo para producción  
**Validación**: Performance, accesibilidad, deploy

---

## ⚠️ RIESGOS Y MITIGACIONES

### Riesgo 1: Curva de aprendizaje R3F
**Probabilidad**: Alta  
**Impacto**: Medio  
**Mitigación**:
- Estudiar https://threejs-journey.com (días 1-3)
- Seguir ejemplos de @react-three/fiber docs
- Copiar de https://codesandbox.io/examples

### Riesgo 2: Performance en móviles
**Probabilidad**: Media  
**Impacto**: Alto  
**Mitigación**:
- Versión simplificada para móvil
- Lazy loading de 3D
- Usar `useMediaQuery` para detectar device

### Riesgo 3: Complejidad excesiva
**Probabilidad**: Media  
**Impacto**: Alto  
**Mitigación**:
- Checkpoints semanales
- Comparar con SvelteKit cada semana
- Si no supera al actual, revertir

---

## 🎨 RESULTADO ESPERADO

### Interfaz Única Etérea:
1. **Background 3D permanente**: Espiral cósmica rotando
2. **Sin navegación tradicional**: Todo es scroll fluido
3. **Timeline vertical 3D**: Tu día como río en el espacio
4. **Transiciones cinemáticas**: Viajar entre dimensiones
5. **Audio generativo**: Frecuencias del día sonando
6. **Geometría sagrada**: Patrones emergiendo
7. **Modo oscuro litúrgico**: Automático al Maghrib

### Nivel de Experiencia:
- Comparable a: **Linear**, **Pitch**, **Stripe Docs**
- Competitivo con: **Notion**, **Reflect**, **Mem.ai**
- Único en: Integración espiritual profunda + 3D inmersivo

---

## 📦 STACK FINAL

```json
{
  "dependencies": {
    "next": "14.2.0",
    "react": "18.3.0",
    "three": "^0.164.0",
    "@react-three/fiber": "^8.16.0",
    "@react-three/drei": "^9.105.0",
    "@react-three/postprocessing": "^2.16.0",
    "framer-motion": "^11.0.0",
    "gsap": "^3.12.0",
    "tone": "^14.8.0",
    "zustand": "^4.5.0",
    "@tanstack/react-query": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "shadcn-ui": "latest"
  }
}
```

---

## ✅ SIGUIENTE ACCIÓN INMEDIATA

**¿Quieres que empiece AHORA con la Fase 0?**

1. Crear toda la documentación del sistema actual
2. Hacer backup y branching en Git
3. Preparar el terreno para la migración

**Tiempo estimado**: 2-3 días  
**Resultado**: Base sólida para migración quirúrgica

**إن شاء الله** - ¿Procedemos? 🕌

