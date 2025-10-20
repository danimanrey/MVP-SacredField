# 🧪 Guía de Testing Completa - MVP

**Fecha:** 10 de octubre, 2025  
**Sistema:** Arquitectura Dual Funcional

---

## 🚀 **Pre-Testing: Verificar que Todo Esté Corriendo**

### **1. Verificar Puertos:**

```bash
lsof -i :8000 -i :3000 -i :5173 | grep LISTEN
```

Deberías ver:
```
Python  [PID]  ... *:8000  (Backend)
node    [PID]  ... *:3000  (Next.js)
node    [PID]  ... *:5173  (Svelte)
```

### **2. Si Falta Alguno, Iniciar:**

```bash
# Backend (si no está)
cd backend && source venv/bin/activate && python run.py &

# Next.js (si no está)
cd campo-sagrado-nextjs && npm run dev &

# Svelte (si no está)  
cd frontend && npm run dev &
```

### **3. Verificar Endpoints:**

```bash
# Backend
curl http://localhost:8000/api/configuracion/dimensiones
# Debe retornar JSON con 7 dimensiones

# Next.js
curl http://localhost:3000
# Debe retornar HTML

# Svelte
curl http://localhost:5173
# Debe retornar HTML
```

---

## 🧪 **Testing del Flujo Completo**

### **FASE 1: Wizard de Onboarding** (Primera vez)

#### **Paso 1.1: Abrir aplicación**
```
Abrir: http://localhost:3000
```

**Esperado:**
- ✅ Ver "🕌 Preparando tu espacio..."
- ✅ Redirige a landing (permitido sin config temporalmente)
- ✅ Ver estrellas animadas de fondo
- ✅ Ver momento litúrgico actual
- ✅ Ver botón "Entrar al Estado Cero"

**Resultado:** _______

---

#### **Paso 1.2: Ir al Onboarding (manual)**
```
Navegar a: http://localhost:3000/onboarding
```

**Esperado:**
- ✅ Ver barra de progreso (4 pasos)
- ✅ Ver universo 3D de fondo
- ✅ Ver Paso 1: Bienvenida

**Resultado:** _______

---

#### **Paso 1.3: Completar Paso 1**

**Verificar:**
- ✅ Logo 🕌 grande
- ✅ Título "Bienvenido al Campo Sagrado"
- ✅ 3 cards de características
- ✅ Frase filosófica
- ✅ Botón "Comenzar Configuración →"

**Acción:** Click en "Comenzar Configuración"

**Esperado:**
- ✅ Transición suave
- ✅ Barra de progreso avanza
- ✅ Aparece Paso 2

**Resultado:** _______

---

#### **Paso 1.4: Completar Paso 2 (No-Negociables)**

**Verificar:**
- ✅ Título "Tus No-Negociables"
- ✅ 5 cards de momentos litúrgicos:
  - 🌅 Fajr (✓ por defecto)
  - ☀️ Dhuhr (✓ por defecto)
  - 🌤️ Asr (✗ por defecto)
  - 🌅 Maghrib (✓ por defecto)
  - 🌙 Isha (✗ por defecto)
- ✅ Contador "3 momentos activos"

**Acciones:**
1. Click en diferentes toggles
2. Verificar que se marcan/desmarcan
3. Click "Siguiente →"

**Esperado:**
- ✅ Transición a Paso 3

**Resultado:** _______

---

#### **Paso 1.5: Completar Paso 3 (Contexto)**

**Verificar:**
- ✅ Sección Financiera:
  - Input de runway (meses)
  - Botones urgencia Sí/No
- ✅ Dimensiones prioritarias:
  - (Si cargan) 7 dimensiones con colores
  - (Si no cargan) Mensaje de error
- ✅ Sección Biológica:
  - Slider energía (1-5)
  - Patrón de sueño (3 opciones)
  - Ejercicio regular (Sí/No)

**Acciones:**
1. Configurar runway: 12 meses
2. Urgencia: Sí
3. Dimensiones: Click en 2-3 (si cargan)
4. Energía: Ajustar a 3/5
5. Sueño: Regular
6. Ejercicio: Sí
7. Click "Siguiente →"

**Esperado:**
- ✅ Botón SIEMPRE funciona (con o sin dimensiones)
- ✅ Transición a Paso 4

**Resultado:** _______

---

#### **Paso 1.6: Completar Paso 4 (Expresión Libre)**

**Verificar:**
- ✅ Icono ✍️
- ✅ Título "Expresión Libre"
- ✅ Textarea grande (1000 caracteres)
- ✅ Contador de caracteres
- ✅ Ejemplos de qué compartir
- ✅ Resumen de configuración
- ✅ Botón "✓ Guardar y Comenzar"

**Acciones:**
1. Escribir algo (opcional)
2. Click "Guardar y Comenzar"

**Esperado:**
- ✅ Botón cambia a "Guardando..."
- ✅ En consola del navegador (F12):
  ```
  💾 Guardando configuración: {...}
  ✅ Configuración guardada: {...}
  ```
- ✅ Archivo creado: `backend/storage/configuracion_usuario.json`
- ✅ Redirige a `/estado-cero`

**Resultado:** _______

---

### **FASE 2: Estado Cero Inmersivo**

#### **Paso 2.1: Inicio del Estado Cero**

**URL:** `http://localhost:3000/estado-cero`

**Esperado:**
- ✅ Ver universo 3D de fondo
- ✅ Ver "Respira profundo"
- ✅ Ver "Estás en el centro del universo"
- ✅ Ver momento actual (🌅 Fajr, etc.)
- ✅ Botón "Entrar al Estado Cero" aparece después de 3s

**Resultado:** _______

---

#### **Paso 2.2: Meditación Guiada**

**Acción:** Click "Entrar al Estado Cero"

**Esperado:**
- ✅ Texto "Respira" (3 segundos)
- ✅ Esfera púrpura animándose
- ✅ Texto "Expande tu consciencia" (3 segundos)
- ✅ Esfera azul expandiéndose
- ✅ Loading "Procesando..."
- ✅ Backend llama a Claude
- ✅ Aparecen preguntas

**Resultado:** _______

---

#### **Paso 2.3: Preguntas Sacrales**

**Verificar:**
- ✅ Pregunta 1 de 6
- ✅ Barra de progreso animada
- ✅ Contexto de la pregunta (arriba)
- ✅ Pregunta principal (grande, centro)
- ✅ Categoría (badge pequeño)
- ✅ Dos botones:
  - ✨ Expansión
  - 🌑 Contracción

**Acciones por pregunta:**
1. Click en "Expansión" o "Contracción"
2. Ver que se ilumina el botón
3. Slider de intensidad aparece
4. Ajustar intensidad (1-5)
5. (Opcional) Escribir nota
6. Click "Siguiente →"

**Repetir 6 veces**

**En la última pregunta:**
- ✅ Botón dice "Completar"

**Resultado:** _______

---

#### **Paso 2.4: Síntesis**

**Esperado:**
- ✅ Universo cambia a cubo verde
- ✅ Texto "La claridad emerge"
- ✅ Loading "Procesando..."
- ✅ Backend llama a Claude para sintetizar
- ✅ Aparece dirección emergente en card
- ✅ Espera 5 segundos

**Resultado:** _______

---

#### **Paso 2.5: Completado**

**Esperado:**
- ✅ Icono ✓ grande
- ✅ "Estado Cero Completado"
- ✅ Dirección emergente en blockquote
- ✅ Botón "Continuar → Organizar mi Día"

**Acción:** Click "Organizar mi Día"

**Esperado:**
- ✅ Redirige a `/estado-cero/validacion`

**Resultado:** _______

---

### **FASE 3: Validación de Calendario**

#### **Paso 3.1: Ver Calendario**

**URL:** `http://localhost:3000/estado-cero/validacion`

**Esperado:**
- ✅ Título "📅 Validación de Calendario"
- ✅ Tu dirección emergente (arriba)
- ✅ Métrica "Al Borde del Caos"
  - Porcentaje sin asignar
  - Barra visual
  - ✓ o ⚠️ según balance

**Si Google Calendar configurado:**
- ✅ Ver eventos del día
- ✅ Categorizados (🔴 🟢 🟡)

**Si NO configurado:**
- ✅ Mensaje "No hay eventos para hoy"
- ✅ Botón "+" Añadir Actividad

**Resultado:** _______

---

#### **Paso 3.2: Editar Eventos**

**Acciones:**
1. Click en título de evento → Editar inline
2. Cambiar hora de inicio/fin
3. Cambiar categoría en dropdown
4. Click ✏️ para editar
5. Click 🗑️ para eliminar (si no es no-negociable)

**Esperado:**
- ✅ Cambios se reflejan inmediatamente
- ✅ Métrica "al borde del caos" se actualiza

**Resultado:** _______

---

#### **Paso 3.3: Añadir Evento**

**Acción:** Click botón "➕ Añadir Actividad"

**Esperado:**
- ✅ Aparece nuevo evento en la lista
- ✅ Título: "Nueva actividad"
- ✅ Hora: Ahora
- ✅ Duración: 1h
- ✅ Puede editarse

**Resultado:** _______

---

#### **Paso 3.4: Guardar y Finalizar**

**Acción:** Click "✓ Guardar y Finalizar"

**Esperado:**
- ✅ Botón muestra "Guardando..."
- ✅ Backend procesa (puede tardar unos segundos)
- ✅ Alert "✅ Calendario validado"
- ✅ Redirige a `/`

**Verificar en consola del navegador:**
```
POST /api/calendario/validar-calendario
```

**Resultado:** _______

---

### **FASE 4: Espejo Diario (Puerto 5173)**

#### **Paso 4.1: Abrir Espejo Diario**

```
Abrir: http://localhost:5173/espejo-diario
```

**Esperado:**
- ✅ Título "📊 Espejo Diario Ejecutivo"
- ✅ Fecha de hoy
- ✅ 3 métricas:
  - % Al borde del caos
  - % Completitud
  - 😊 Salud del organismo

**Si Google Calendar configurado:**
- ✅ Tabla de eventos del día
- ✅ Con categorías y colores

**Resultado:** _______

---

#### **Paso 4.2: Marcar Completadas**

**Acciones:**
1. Click en checkbox de un evento
2. Ver que se marca como completada
3. Ver que la fila se atenúa (opacity 0.6)
4. Ver que el título tiene line-through

**Esperado:**
- ✅ Métrica de completitud actualiza
- ✅ Salud del organismo cambia
- ✅ Emoji cambia según salud

**Resultado:** _______

---

#### **Paso 4.3: Actualizar**

**Acción:** Click "🔄 Actualizar"

**Esperado:**
- ✅ Recarga eventos de Google Calendar
- ✅ Refleja cambios hechos en puerto 3000

**Resultado:** _______

---

## 📊 **Checklist de Endpoints del Backend**

### **API de Configuración:**
```bash
# Obtener dimensiones
curl http://localhost:8000/api/configuracion/dimensiones
# Debe retornar 7 dimensiones

# Obtener configuración
curl http://localhost:8000/api/configuracion/individual
# Debe retornar config o not_found

# Guardar configuración
curl -X POST http://localhost:8000/api/configuracion/individual \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test", ...}'
# Debe retornar success
```

- [ ] GET /dimensiones funciona
- [ ] GET /individual funciona
- [ ] POST /individual funciona

---

### **API de Estado Cero:**
```bash
# Verificar momento
curl http://localhost:8000/api/estado-cero/verificar

# Iniciar Estado Cero
curl -X POST http://localhost:8000/api/estado-cero/iniciar \
  -H "Content-Type: application/json" \
  -d '{"momento_liturgico":"fajr"}'
```

- [ ] GET /verificar funciona
- [ ] POST /iniciar funciona
- [ ] POST /{id}/responder funciona
- [ ] POST /{id}/sintetizar funciona

---

### **API de Calendario:**
```bash
# Obtener eventos de hoy
curl http://localhost:8000/api/calendario/eventos/hoy

# Crear evento
curl -X POST http://localhost:8000/api/calendario/eventos \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Test", "inicio":"2025-10-10T10:00:00", "duracion_minutos":60}'
```

- [ ] GET /eventos/hoy funciona
- [ ] POST /eventos funciona
- [ ] PUT /eventos/{id} funciona
- [ ] DELETE /eventos/{id} funciona

---

## 🎯 **Testing de Integración**

### **Test 1: Flujo Completo Sin Google Calendar**

**Escenario:** Google Calendar NO configurado

**Flujo:**
1. Estado Cero completo
2. Validación de calendario muestra vacío
3. Añadir 3 eventos manualmente
4. Guardar
5. Espejo Diario muestra "Error cargando eventos"

**Resultado esperado:**
- ⚠️ Funciona pero sin sincronización
- ✅ Eventos se pueden crear localmente

---

### **Test 2: Flujo Completo CON Google Calendar**

**Escenario:** Google Calendar configurado

**Flujo:**
1. Estado Cero completo
2. Validación carga eventos reales
3. Editar algún evento
4. Añadir un evento nuevo
5. Guardar
6. Abrir Google Calendar web
7. Verificar que los cambios están

**Resultado esperado:**
- ✅ Sincronización bidireccional
- ✅ Cambios visibles en Google Calendar

---

### **Test 3: Persistencia**

**Flujo:**
1. Completar onboarding
2. Verificar archivos:
   ```bash
   ls backend/storage/configuracion_usuario.json
   ls obsidian_vault/00-Pilares/Configuracion-Individual.md
   ```
3. Completar Estado Cero
4. Verificar:
   ```bash
   ls obsidian_vault/50-Conversaciones-IA/Estados-Cero/
   ```

**Resultado esperado:**
- ✅ Archivos JSON creados
- ✅ Archivos Markdown en Obsidian
- ✅ Editables manualmente

---

## 🐛 **Troubleshooting**

### **Problema: Puerto ocupado**
```bash
lsof -ti :3000 | xargs kill -9
lsof -ti :5173 | xargs kill -9
lsof -ti :8000 | xargs kill -9
```

### **Problema: Backend no responde**
```bash
cd backend
tail -50 /tmp/backend.log
```

### **Problema: Dimensiones no cargan**
```bash
curl http://localhost:8000/api/configuracion/dimensiones
```
Si da error → Backend no tiene el router registrado

### **Problema: Google Calendar no funciona**
- Verificar que existe `backend/config/google_credentials.json`
- Si no: Ver `SETUP_GOOGLE_CALENDAR.md`

---

## ✅ **Criterios de Éxito**

### **Mínimo Viable:**
- [ ] Onboarding completa
- [ ] Estado Cero funciona end-to-end
- [ ] Dirección emergente se genera
- [ ] Configuración se guarda
- [ ] Espejo Diario muestra algo

### **Completo:**
- [ ] Todo lo anterior +
- [ ] Validación de calendario funciona
- [ ] Google Calendar sincroniza
- [ ] Archivos en Obsidian se crean
- [ ] Métricas se calculan correctamente

---

## 📝 **Reporte de Testing**

**Fecha:** _______________  
**Tester:** _______________  

### **Resultados:**

| Fase | Estado | Notas |
|------|--------|-------|
| Onboarding | ⬜ PASS / ⬜ FAIL | |
| Estado Cero | ⬜ PASS / ⬜ FAIL | |
| Validación Cal | ⬜ PASS / ⬜ FAIL | |
| Espejo Diario | ⬜ PASS / ⬜ FAIL | |

### **Issues Encontrados:**
```




```

---

**¡Adelante con el testing!** 🧪✨

إن شاء الله 🕌

