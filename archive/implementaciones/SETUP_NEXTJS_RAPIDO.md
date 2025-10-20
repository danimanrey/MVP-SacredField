# 🚀 Setup Rápido Next.js - Puerto 3000

## Si Next.js NO existe todavía

### Paso 1: Crear Proyecto Next.js

```bash
cd /Users/hp/Campo\ sagrado\ MVP

npx create-next-app@latest campo-sagrado-nextjs \
  --typescript \
  --tailwind \
  --app \
  --src-dir \
  --import-alias "@/*"
```

**Respuestas a las preguntas:**
- ✅ TypeScript: **Yes**
- ✅ ESLint: **Yes**
- ✅ Tailwind CSS: **Yes**
- ✅ `src/` directory: **Yes**
- ✅ App Router: **Yes**
- ✅ Import alias: **Yes** (`@/*`)

### Paso 2: Instalar Dependencias 3D (Opcional - para experiencias inmersivas)

```bash
cd campo-sagrado-nextjs

# 3D Core
npm install three @react-three/fiber @react-three/drei

# Animaciones
npm install framer-motion

# Audio (opcional)
npm install tone

# UI Components
npx shadcn-ui@latest init
```

### Paso 3: Copiar Cliente API

```bash
# Si ya tienes el cliente API de la guía anterior
cp -r ../frontend/src/lib/api ./src/lib/
cp -r ../frontend/src/lib/types ./src/lib/

# O crear manualmente según docs/GUIA_INTEGRACION_NEXTJS.md
```

### Paso 4: Iniciar

```bash
npm run dev

# Abre: http://localhost:3000
```

---

## Si Next.js YA existe

### Verificar Estado

```bash
cd /Users/hp/Campo\ sagrado\ MVP/campo-sagrado-nextjs

# Ver qué hay instalado
cat package.json

# Instalar dependencias faltantes
npm install

# Iniciar
npm run dev
```

---

## Estructura Recomendada

```
campo-sagrado-nextjs/
├── src/
│   ├── app/
│   │   ├── page.tsx                    # Home
│   │   ├── layout.tsx                  # Layout global
│   │   ├── dashboard/
│   │   │   └── page.tsx                # Dashboard con datos reales
│   │   ├── estado-cero/
│   │   │   └── page.tsx                # Estado Cero 3D
│   │   └── demo/
│   │       └── page.tsx                # Demo con datos mock
│   │
│   ├── components/
│   │   ├── 3d/                         # Componentes Three.js
│   │   ├── ui/                         # Componentes UI (Shadcn)
│   │   └── layout/                     # Navegación, etc.
│   │
│   ├── lib/
│   │   ├── api/
│   │   │   └── client.ts               # Cliente para Backend (8000)
│   │   ├── types/
│   │   │   └── index.ts                # TypeScript types
│   │   └── utils.ts
│   │
│   └── hooks/
│       └── useCampoSagrado.ts          # Custom hooks
│
├── public/
├── package.json
└── tsconfig.json
```

---

## Conexión con Backend

### Configurar URL del Backend

```typescript
// src/lib/api/client.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchAPI(endpoint: string) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);
  if (!response.ok) throw new Error(`API Error: ${response.status}`);
  return response.json();
}
```

### Variables de Entorno

```bash
# .env.local (crear si no existe)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Testing Rápido

### 1. Verificar que el Backend funciona

```bash
# En otra terminal
curl http://localhost:8000/health

# Debe devolver: {"status":"ok"}
```

### 2. Página de Test Simple

```typescript
// src/app/test/page.tsx
'use client';

import { useEffect, useState } from 'react';

export default function TestPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/contexto-temporal')
      .then(res => res.json())
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Cargando...</div>;
  if (!data) return <div>Error conectando con Backend</div>;

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Test Backend Connection</h1>
      <pre className="bg-gray-100 p-4 rounded">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}
```

Visita: `http://localhost:3000/test`

---

## Diferencias con Svelte (5173)

| Aspecto | Svelte (5173) | Next.js (3000) |
|---------|---------------|----------------|
| **Propósito** | Funcionalidad | Experiencia |
| **Velocidad** | Muy rápida | Normal |
| **3D** | ❌ No | ✅ Sí |
| **Complejidad** | Baja | Alta |
| **Para** | Desarrollo | Beta testers |

---

## Comandos Útiles

```bash
# Desarrollo
npm run dev

# Build para producción
npm run build
npm run start

# Linting
npm run lint

# Agregar componente Shadcn
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
```

---

## Troubleshooting

### Puerto 3000 ya en uso

```bash
# Ver qué usa el puerto 3000
lsof -i :3000

# Matar el proceso
kill -9 <PID>

# O cambiar puerto en package.json
# "dev": "next dev -p 3001"
```

### Cannot connect to Backend

```bash
# Verificar que el backend está corriendo
curl http://localhost:8000/health

# Si no está, iniciarlo:
cd /Users/hp/Campo\ sagrado\ MVP/backend
source venv/bin/activate
python run.py
```

### TypeScript errors

```bash
# Regenerar tipos
npm run build

# O ignorar temporalmente
# tsconfig.json: "strict": false
```

---

## Next Steps

1. **Copiar Estado Cero inmersivo de Svelte**
   - Usar como referencia: `frontend/src/routes/estado-cero/+page.svelte`
   - Mantener mismo flujo, agregar 3D

2. **Implementar Dashboard 3D**
   - Usar React Three Fiber
   - Datos del endpoint: `/api/orquestador/espejo-diario/hoy`

3. **Crear Timeline 3D**
   - Visualización vertical del día
   - Interacción con scroll

4. **Audio Generativo**
   - Tone.js según momento litúrgico
   - Frecuencias específicas por tiempo de rezo

---

## Documentación Completa

- **Arquitectura Dual:** `ARQUITECTURA_DUAL_FRONTEND.md`
- **Integración Next.js:** `docs/GUIA_INTEGRACION_NEXTJS.md`
- **Plan Migración:** `PLAN_MIGRACION_NEXTJS.md`

---

**¿Listo? Ejecuta:**

```bash
bash scripts/iniciar-dual-frontend.sh
```

Esto iniciará:
- ✅ Backend (8000)
- ✅ Svelte (5173)
- ✅ Next.js (3000) - si existe

**Adelante! 🚀**

