# 🌌 Campo Sagrado - Frontend Inmersivo (Puerto 3000)

**Next.js + TypeScript + React Three Fiber**

## 🎯 Propósito

Este es el **frontend de divulgación** del Campo Sagrado:
- **Cara al cliente**: Experiencia pública y gratuita
- **Inmersivo**: Estado Cero con visualización 3D
- **Contemplativo**: Flujo guiado, meditativo
- **Asombro**: Causa cuestionamiento y admiración

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
npm install

# Iniciar en modo desarrollo (puerto 3000)
npm run dev

# Abrir en navegador
open http://localhost:3000
```

## 🏗️ Estructura

```
app/
├── page.tsx                    # Landing inmersivo
├── estado-cero/
│   ├── page.tsx                # Estado Cero principal
│   └── components/
│       ├── UniversoEsferico.tsx # Visualización 3D
│       └── PreguntasSacrales.tsx # Preguntas binarias
├── validacion/                 # Validar actividades (TODO)
├── layout.tsx                  # Layout principal
└── globals.css                 # Estilos globales

lib/
├── api-client.ts               # Cliente del backend
└── stores/
    └── estado-cero-store.ts    # Store Zustand
```

## 🎨 Stack Tecnológico

- **Next.js 14**: Framework React con App Router
- **TypeScript**: Type safety
- **React Three Fiber**: 3D con Three.js
- **@react-three/drei**: Helpers para R3F
- **Framer Motion**: Animaciones fluidas
- **Zustand**: State management
- **Tailwind CSS**: Estilos utilitarios

## 🌊 Flujo de Usuario

```
1. Landing (page.tsx)
   ↓
2. Click "Entrar al Estado Cero"
   ↓
3. Meditación entrada (3s)
   ↓
4. Meditación expansión (3s)
   ↓
5. Backend: Iniciar Estado Cero
   ↓
6. Preguntas sacrales (6 preguntas)
   ↓
7. Síntesis de dirección
   ↓
8. Mostrar dirección emergente
   ↓
9. Redirigir a /validacion
```

## 🎯 Diferencias con Puerto 5173

| Aspecto | Puerto 3000 (Next.js) | Puerto 5173 (Svelte) |
|---------|----------------------|---------------------|
| **Propósito** | Divulgación | Ejecución |
| **Usuario** | Cliente/Público | Usuario registrado |
| **Tono** | Contemplativo | Táctico |
| **Visuales** | 3D inmersivo | Dashboard ejecutivo |
| **Flujo** | Guiado | Libre navegación |
| **Estado Cero** | ✅ SÍ (inmersivo) | ❌ NO (solo ver) |
| **Espejo Diario** | ❌ NO | ✅ SÍ (gestión) |

## 🔌 Conexión con Backend

El frontend se conecta al backend en `http://localhost:8000`:

```typescript
// lib/api-client.ts
const API_BASE = 'http://localhost:8000/api'

// Endpoints usados:
- POST /estado-cero/verificar
- POST /estado-cero/iniciar
- POST /estado-cero/{id}/responder
- POST /estado-cero/{id}/sintetizar
- POST /estado-cero/{id}/finalizar
```

## 🎨 Colores del Universo

```css
--universo: #0a0a1e          /* Fondo oscuro */
--purpura-mistico: #8B5CF6   /* Primario */
--azul-estelar: #3B82F6      /* Secundario */
--verde-vida: #22C55E         /* Acento */
```

## 📝 TODO

- [ ] Página de validación de actividades
- [ ] Onboarding de configuración
- [ ] Chat clarificador
- [ ] Audio generativo (Tone.js)
- [ ] Animaciones avanzadas
- [ ] Responsive móvil optimizado
- [ ] PWA capabilities

## 🐛 Debugging

```bash
# Ver logs en tiempo real
npm run dev

# Build para producción
npm run build

# Ejecutar build
npm start
```

## 🔗 Enlaces

- **Este puerto**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Puerto ejecutivo**: http://localhost:5173
- **Docs API**: http://localhost:8000/docs

---

**إن شاء الله - Si Dios quiere 🕌✨**

