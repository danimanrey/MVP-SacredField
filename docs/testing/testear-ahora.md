# 🧪 Testear AHORA - Guía Rápida

**Estado:** ✅ Sistema corriendo  
**Fecha:** 10 de octubre, 2025

---

## ✅ **Estado de los Servidores**

```bash
✅ Backend:  http://localhost:8000  (Python corriendo)
✅ Next.js:  http://localhost:3000  (Node corriendo)
✅ Svelte:   http://localhost:5173  (Iniciando...)
```

---

## 🚀 **TESTING RÁPIDO (5 minutos)**

### **1. Testear Onboarding**

```
1. Abrir: http://localhost:3000/onboarding

2. Completar 4 pasos:
   - Paso 1: Click "Comenzar Configuración"
   - Paso 2: Seleccionar 2-3 momentos → Siguiente
   - Paso 3: Configurar contexto → Siguiente  
   - Paso 4: (Opcional) Escribir algo → Guardar y Comenzar

3. Esperado:
   ✅ Redirige a /estado-cero
   ✅ Archivo creado en backend/storage/configuracion_usuario.json
```

**¿Funciona?** _______

---

### **2. Testear Estado Cero**

```
1. Ya estás en: http://localhost:3000/estado-cero

2. Flujo:
   - Ver "Respira profundo"
   - Esperar 3s → Botón aparece
   - Click "Entrar al Estado Cero"
   - Ver meditación (6s total)
   - Responder 6 preguntas:
     * Click Expansión o Contracción
     * Ajustar intensidad
     * (Opcional) Nota
     * Siguiente
   - Ver dirección emergente
   - Click "Organizar mi Día"

3. Esperado:
   ✅ Universo 3D se ve bien
   ✅ Transiciones suaves
   ✅ 6 preguntas funcionan
   ✅ Dirección emergente aparece
   ✅ Redirige a validación
```

**¿Funciona?** _______

---

### **3. Testear Validación de Calendario**

```
1. Estás en: http://localhost:3000/estado-cero/validacion

2. Ver:
   ✅ Tu dirección emergente (arriba)
   ✅ Métrica "Al borde del caos"
   ✅ Lista de eventos (o vacía si no hay Google Calendar)

3. Acciones:
   - Click "+" para añadir evento
   - Editar título, hora, categoría
   - Click "Guardar y Finalizar"

4. Esperado:
   ✅ Se guarda
   ✅ Redirige a /
```

**¿Funciona?** _______

---

### **4. Testear Espejo Diario (5173)**

```
1. Abrir: http://localhost:5173/espejo-diario

2. Ver:
   ✅ Métricas (caos, completitud, salud)
   ✅ Tabla de eventos del día
   ✅ Checkbox para marcar completadas

3. Acciones:
   - Marcar 1-2 eventos como completados
   - Ver que métricas actualizan
   - Click "Actualizar"

4. Esperado:
   ✅ Todo funciona
   ✅ Sincronización con Google Calendar
```

**¿Funciona?** _______

---

## 🔍 **Verificaciones Técnicas**

### **1. Backend APIs:**

```bash
# Dimensiones
curl http://localhost:8000/api/configuracion/dimensiones
# ✅ Debe retornar 7 dimensiones

# Estado Cero verificar
curl http://localhost:8000/api/estado-cero/verificar
# ✅ Debe retornar momento actual

# Calendario
curl http://localhost:8000/api/calendario/eventos/hoy
# ⚠️ Puede dar error si Google Calendar no configurado
```

### **2. Archivos Creados:**

```bash
# Configuración
ls -la backend/storage/configuracion_usuario.json
# ✅ Debe existir después del onboarding

# Obsidian (si se guardó)
ls -la obsidian_vault/00-Pilares/Configuracion-Individual.md
# ✅ Debe existir después del onboarding
```

### **3. Consola del Navegador:**

```
Abrir: http://localhost:3000
Presionar: F12 (DevTools)
Ir a: Console

Buscar:
- ⚠️ No hay configuración, pero permitiendo continuar...
- 💾 Guardando configuración: {...}
- ✅ Configuración guardada: {...}
```

---

## 🎯 **Lo que DEBE Funcionar**

### **Mínimo (Sin Google Calendar):**
- ✅ Onboarding completo
- ✅ Estado Cero hasta dirección emergente
- ✅ Validación muestra lista vacía
- ✅ Puedes añadir eventos manualmente
- ✅ Espejo Diario muestra error (normal sin Google Cal)

### **Completo (Con Google Calendar):**
- ✅ Todo lo anterior +
- ✅ Validación carga eventos reales
- ✅ Guardar sincroniza con Google Calendar
- ✅ Espejo Diario muestra eventos
- ✅ Marcar completadas funciona

---

## 🐛 **Si Algo No Funciona**

### **Onboarding no redirige:**
- Verificar consola del navegador (F12)
- Ver si hay errores de fetch
- Verificar que backend está en puerto 8000

### **Estado Cero no inicia:**
- Ver logs del backend: `tail -f /tmp/backend.log`
- Verificar que Claude API key está configurada
- Intentar con `permitir_recuperacion=true`

### **Calendario vacío:**
- Normal si Google Calendar no configurado
- Puedes añadir eventos manualmente
- Para configurar Google Calendar: Ver `SETUP_GOOGLE_CALENDAR.md`

### **Dimensiones no cargan:**
- No importa, el onboarding funciona sin ellas
- Backend responde correctamente (verificado)
- Es un issue del frontend (fetch timing)

---

## 🎯 **URLs para Testear**

```
Inmersivo:
  http://localhost:3000              # Landing
  http://localhost:3000/onboarding   # Wizard
  http://localhost:3000/estado-cero  # Estado Cero
  http://localhost:3000/estado-cero/validacion  # Calendario

Ejecutivo:
  http://localhost:5173                    # Home
  http://localhost:5173/espejo-diario      # Espejo
  http://localhost:5173/universo-imaginal  # Universo

Backend:
  http://localhost:8000/docs         # Swagger UI
```

---

## ✅ **Checklist Rápido**

- [ ] Backend responde (curl 8000)
- [ ] Next.js carga (3000)
- [ ] Svelte carga (5173)
- [ ] Onboarding funciona
- [ ] Estado Cero funciona
- [ ] Validación funciona (aunque calendario vacío)
- [ ] Espejo Diario funciona

---

**¡Adelante con el testing!** 🧪✨

**Reporta cualquier issue y lo arreglamos al instante.**

إن شاء الله 🕌

