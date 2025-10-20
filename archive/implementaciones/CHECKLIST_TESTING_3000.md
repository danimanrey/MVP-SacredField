# ✅ Checklist de Testing - Puerto 3000

**Proyecto:** Campo Sagrado Next.js  
**Puerto:** 3000  
**Estado:** ✅ SERVIDOR CORRIENDO

---

## 🚀 Pre-requisitos

### 1. Backend corriendo (8000)
```bash
cd backend
source venv/bin/activate
python run.py
```
✅ Verificar: http://localhost:8000/health

### 2. Next.js corriendo (3000)
```bash
cd campo-sagrado-nextjs
npm run dev
```
✅ Verificar: http://localhost:3000

---

## 📋 Checklist de Testing

### **Fase 1: Landing Page** (localhost:3000)

- [ ] **1.1** Abrir http://localhost:3000
- [ ] **1.2** Ver título "🕌 Campo Sagrado"
- [ ] **1.3** Ver estrellas animadas de fondo (parpadeando)
- [ ] **1.4** Ver momento litúrgico actual (Fajr/Dhuhr/etc)
- [ ] **1.5** Ver "Próximo Estado Cero: [hora]"
- [ ] **1.6** Esperar 3 segundos
- [ ] **1.7** Ver botón "Entrar al Estado Cero" aparecer con animación

**Resultado esperado:** Landing inmersivo con estrellas, título y CTA

---

### **Fase 2: Inicio de Meditación**

- [ ] **2.1** Click en "Entrar al Estado Cero"
- [ ] **2.2** Ver universo 3D aparecer de fondo
- [ ] **2.3** Ver texto "Respira profundo"
- [ ] **2.4** Ver texto "Estás en el centro del universo"
- [ ] **2.5** Ver icono del momento actual (🌅 Fajr, ☀️ Dhuhr, etc)
- [ ] **2.6** Botón "Preparando el espacio..." aparece después de 3s

**Resultado esperado:** Pantalla contemplativa con universo 3D

---

### **Fase 3: Meditación Guiada**

- [ ] **3.1** Click en "Entrar al Estado Cero" (segunda vez)
- [ ] **3.2** Ver "Respira" con esfera púrpura animada (3s)
- [ ] **3.3** Esfera se expande y contrae suavemente
- [ ] **3.4** Ver "Expande tu consciencia" con esfera azul (3s)
- [ ] **3.5** Backend inicializa (ver loading overlay)

**Resultado esperado:** Transición suave entrada → expansión

---

### **Fase 4: Preguntas Sacrales**

- [ ] **4.1** Ver primera pregunta aparecer
- [ ] **4.2** Ver contexto de la pregunta (ej: "Energía")
- [ ] **4.3** Ver pregunta principal (grande, centrada)
- [ ] **4.4** Ver categoría (badge pequeño)
- [ ] **4.5** Ver barra de progreso (arriba, animada)
- [ ] **4.6** Ver "Pregunta 1 de 6"

#### **Interacción con pregunta:**
- [ ] **4.7** Ver dos botones grandes:
  - Expansión (✨) - Verde cuando activo
  - Contracción (🌑) - Gris cuando activo
- [ ] **4.8** Click en "Expansión"
- [ ] **4.9** Botón se ilumina en verde
- [ ] **4.10** Slider de intensidad aparece
- [ ] **4.11** Campo de nota opcional aparece
- [ ] **4.12** Mover slider (1-5)
- [ ] **4.13** Escribir nota opcional
- [ ] **4.14** Botón "Siguiente" se activa (gradiente púrpura/azul)
- [ ] **4.15** Click "Siguiente"
- [ ] **4.16** Pregunta actual desaparece con animación
- [ ] **4.17** Nueva pregunta aparece
- [ ] **4.18** Barra de progreso avanza

#### **Navegación:**
- [ ] **4.19** Click "Anterior" (si disponible)
- [ ] **4.20** Volver a pregunta anterior
- [ ] **4.21** Respuesta anterior se mantiene
- [ ] **4.22** Completar todas las 6 preguntas
- [ ] **4.23** Última pregunta: Botón dice "Completar"

**Resultado esperado:** 6 preguntas fluidas con navegación

---

### **Fase 5: Síntesis**

- [ ] **5.1** Click "Completar" en última pregunta
- [ ] **5.2** Ver "La claridad emerge" (cubo verde animado)
- [ ] **5.3** Ver "Tu dirección se revela"
- [ ] **5.4** Loading overlay con spinner
- [ ] **5.5** Backend procesa respuestas
- [ ] **5.6** Dirección emergente aparece en card
- [ ] **5.7** Ver texto de dirección (generado por Claude)
- [ ] **5.8** Esperar 5 segundos

**Resultado esperado:** Dirección emergente clara y visible

---

### **Fase 6: Completado**

- [ ] **6.1** Ver ícono de check (✓) grande
- [ ] **6.2** Ver "Estado Cero Completado"
- [ ] **6.3** Ver dirección emergente en blockquote
- [ ] **6.4** Ver botón "Continuar → Validar Actividades"
- [ ] **6.5** Ver texto "Ahora generaremos actividades..."
- [ ] **6.6** Click en botón "Continuar"
- [ ] **6.7** Redirige a /validacion

**Resultado esperado:** Pantalla de éxito con siguiente paso

---

## 🎨 Verificaciones Visuales

### **Universo 3D:**
- [ ] Estrellas de fondo (5000) visibles
- [ ] Partículas (1000) rotando lentamente
- [ ] Esfera wireframe en entrada/expansión
- [ ] Cubo wireframe en preguntas/síntesis
- [ ] Anillo de luz visible
- [ ] Colores cambian por fase:
  - Entrada: Púrpura (#8B5CF6)
  - Expansión: Azul (#3B82F6)
  - Preguntas: Verde (#22C55E)
  - Síntesis: Violeta (#A855F7)

### **Animaciones:**
- [ ] Fade in/out suave
- [ ] Transiciones entre fases fluidas
- [ ] Botones con hover effect
- [ ] Slider responde al drag
- [ ] Loading spinner rota continuamente

### **Responsive:**
- [ ] Desktop (>1024px) - Layout completo
- [ ] Tablet (768-1024px) - Layout adaptado
- [ ] Móvil (<768px) - Layout simplificado

---

## 🐛 Testing de Errores

### **Error 1: Backend no responde**
- [ ] Detener backend
- [ ] Intentar iniciar Estado Cero
- [ ] Ver mensaje de error
- [ ] Botón "Reintentar" funciona

### **Error 2: Momento incorrecto**
- [ ] Intentar Estado Cero fuera de momento litúrgico
- [ ] Ver error: "No es momento para Estado Cero"

### **Error 3: Navegación rápida**
- [ ] Click "Siguiente" sin seleccionar sensación
- [ ] Botón debe estar deshabilitado
- [ ] No debe avanzar

---

## 📊 Verificación de Datos

### **Backend recibe datos:**
```bash
# En otra terminal, ver logs del backend
cd backend
tail -f logs/app.log
```

- [ ] Ver POST /api/estado-cero/iniciar
- [ ] Ver POST /api/estado-cero/{id}/responder (6 veces)
- [ ] Ver POST /api/estado-cero/{id}/sintetizar
- [ ] Ver respuestas con:
  - pregunta_id
  - sensacion (expansion/contraccion)
  - intensidad (1-5)
  - nota (si existe)

---

## 🎯 Criterios de Éxito

### **Must Have (Crítico):**
✅ Landing page funcional  
✅ Universo 3D renderiza  
✅ Meditación guiada fluye  
✅ 6 preguntas se responden  
✅ Backend recibe respuestas  
✅ Dirección emergente aparece  
✅ Navegación funciona  

### **Should Have (Importante):**
✅ Animaciones fluidas  
✅ Error handling visible  
✅ Loading states claros  
✅ Responsive design  

### **Nice to Have (Bonus):**
- Transiciones 3D complejas
- Audio generativo
- Efectos de partículas avanzados
- PWA capabilities

---

## 📝 Reporte de Issues

### **Template:**
```
Fase: [Landing/Meditación/Preguntas/Síntesis/Completado]
Paso: [Número del checklist]
Issue: [Descripción breve]
Esperado: [Qué debería pasar]
Actual: [Qué pasó realmente]
Navegador: [Chrome/Firefox/Safari]
Screenshot: [Si aplica]
```

---

## ✅ Sign-off

**Testing completado por:** _______________  
**Fecha:** _______________  
**Navegador:** _______________  
**Resultado:** ⬜ PASS / ⬜ FAIL  

**Notas adicionales:**
```




```

---

## 🚀 Próximo Paso

Una vez completado este testing:
→ **Día 2: Wizard de Onboarding**

---

**¡Testing exitoso!** إن شاء الله 🕌✨

