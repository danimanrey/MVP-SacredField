# 🧪 Testing Estado Cero - AHORA

**Fecha:** 10 de octubre, 2025  
**Error:** Corregido ✅

---

## ✅ **Fixes Aplicados**

1. ✅ Campo "momento" corregido (era "momento_liturgico")
2. ✅ Errores ahora son legibles (no "[object Object]")
3. ✅ Logging mejorado en consola
4. ✅ Referencias a "13 meses" removidas

---

## 🚀 **TESTING - Paso a Paso**

### **1. Refresca la Página**

```
Presiona: Cmd+R (o F5)
En: http://localhost:3000/estado-cero
```

---

### **2. Abre la Consola del Navegador**

```
Presiona: F12
Ve a: Console (pestaña)
```

**Deberías ver logs cuando hagas acciones**

---

### **3. Click "Entrar al Estado Cero"**

**En consola deberías ver:**
```
🔮 Iniciando Estado Cero...
✅ Estado Cero iniciado: {id: "...", momento: "fajr", preguntas: [...]}
```

**Si ves error en consola, cópialo aquí:** _______________

---

### **4. Si Todo Funciona:**

Deberías ver:
- ✅ Meditación "Respira" (3s)
- ✅ Meditación "Expande tu consciencia" (3s)
- ✅ Aparecen 6 preguntas sacrales
- ✅ Puedes responder cada una
- ✅ Dirección emergente se genera
- ✅ Click "Organizar mi Día" → Validación

---

## 🐛 **Si AÚN da Error**

### **Posibles Causas:**

#### **A. Claude API Key no configurada**

**Verificar:**
```bash
cd backend
cat .env | grep ANTHROPIC_API_KEY
```

**Debe mostrar:** `ANTHROPIC_API_KEY=sk-ant-...`

**Si NO está:**
```bash
echo 'ANTHROPIC_API_KEY=tu-api-key-aqui' >> .env
```

Luego reiniciar backend.

---

#### **B. Base de datos no inicializada**

**Verificar:**
```bash
ls -la storage/organismo.db
```

**Si NO existe:**
```bash
cd backend
python scripts/init_db.py
```

---

#### **C. Backend tiene otro error**

**Ver logs:**
```bash
tail -50 /tmp/backend.log
```

**Buscar líneas con "ERROR" o "Exception"**

---

## 📋 **Checklist de Diagnóstico**

Si hay error, verificar en orden:

1. [ ] Backend está corriendo (`ps aux | grep "python run.py"`)
2. [ ] Claude API key configurada (`cat backend/.env`)
3. [ ] Base de datos existe (`ls backend/storage/organismo.db`)
4. [ ] Endpoint responde (`curl http://localhost:8000/api/estado-cero/verificar`)
5. [ ] Frontend puede alcanzar backend (sin CORS)

---

## ✅ **Si Funciona Correctamente:**

**Continúa testeando:**

1. Responde las 6 preguntas
2. Ve la dirección emergente
3. Valida el calendario
4. Guarda
5. Ve al espejo diario (puerto 5173)

---

## 🔧 **Comandos de Emergencia**

### **Reiniciar Todo:**

```bash
# Matar procesos
pkill -f "python run.py"
pkill -f "next dev"
pkill -f "vite"

# Iniciar de nuevo
cd backend && source venv/bin/activate && python run.py &
cd campo-sagrado-nextjs && npm run dev &
cd frontend && npm run dev &
```

---

## 📝 **Reporta el Error Exacto**

Si sigue dando error, copia y pega:

1. **Error de la consola del navegador (F12 → Console)**
2. **Error visual en pantalla**
3. **Logs del backend** (`tail -20 /tmp/backend.log`)

---

**Sistema listo. Errores corregidos. Adelante con el testing. إن شاء الله 🕌✨**

