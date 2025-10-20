# 🗓️ Setup Google Calendar - Guía Rápida

## 📋 **Resumen**

Esta guía te ayudará a conectar el Campo Sagrado con tu Google Calendar para poder:
- ✨ Crear automáticamente los 5 Estados Cero diarios
- 📅 Generar bloques del plan de jornada
- 👥 Compartir tu disponibilidad con pareja/círculo
- 🔔 Recibir notificaciones nativas de Google

**Tiempo estimado**: 10-15 minutos

---

## 🚀 **Paso 1: Instalar Dependencias**

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔐 **Paso 2: Crear Proyecto en Google Cloud**

### 2.1 Ir a Google Cloud Console
Abre: https://console.cloud.google.com/

### 2.2 Crear Nuevo Proyecto
1. Haz clic en "Select a project" (arriba)
2. Clic en "New Project"
3. Nombre: **"Campo Sagrado MVP"**
4. Clic en "Create"
5. Espera unos segundos y selecciona el proyecto

---

## 📚 **Paso 3: Habilitar Google Calendar API**

1. En el menú lateral → **"APIs & Services"** → **"Library"**
2. Busca: **"Google Calendar API"**
3. Haz clic en el resultado
4. Clic en **"Enable"**
5. Espera a que se habilite (10-20 segundos)

---

## 🎫 **Paso 4: Configurar Pantalla de Consentimiento**

1. Ve a: **"APIs & Services"** → **"OAuth consent screen"**
2. Tipo de usuario: **"External"** → Clic en "Create"
3. Completa el formulario:
   - **App name**: Campo Sagrado
   - **User support email**: tu email
   - **Developer contact**: tu email
4. Clic en **"Save and Continue"**
5. En "Scopes" → Clic en **"Save and Continue"** (no añadas nada)
6. En "Test users" → Clic en **"+ Add Users"**
   - Añade tu email
   - Clic en **"Add"**
7. Clic en **"Save and Continue"**
8. Revisa el resumen → Clic en **"Back to Dashboard"**

---

## 🔑 **Paso 5: Crear Credenciales OAuth**

1. Ve a: **"APIs & Services"** → **"Credentials"**
2. Clic en **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. Application type: **"Desktop app"**
4. Name: **"Campo Sagrado Desktop"**
5. Clic en **"CREATE"**
6. Aparecerá un modal con el Client ID y Secret
   - Clic en **"DOWNLOAD JSON"**
7. Guarda el archivo descargado

---

## 📁 **Paso 6: Configurar Credenciales en el Proyecto**

```bash
# Crear carpeta config si no existe
mkdir -p backend/config

# Renombrar y mover el archivo descargado
# (reemplaza "client_secret_XXX.json" con el nombre real)
mv ~/Downloads/client_secret_*.json backend/config/google_credentials.json
```

**Verificar**:
```bash
ls -la backend/config/google_credentials.json
# Debe mostrar el archivo
```

---

## ✅ **Paso 7: Ejecutar Setup**

```bash
cd backend
source venv/bin/activate
python scripts/setup_google_calendar.py
```

**Lo que sucederá**:
1. Se abrirá tu navegador
2. Te pedirá que selecciones tu cuenta de Google
3. Verás una pantalla que dice "Google hasn't verified this app"
   - ✅ **Esto es normal** (es tu app personal)
   - Haz clic en **"Advanced"** → **"Go to Campo Sagrado (unsafe)"**
4. Autoriza los permisos de Calendar
5. Verás "The authentication flow has completed"
6. Puedes cerrar esa pestaña del navegador

**Output esperado**:
```
✅ Autenticación exitosa!
   Token guardado en: backend/config/google_token.json

🧪 Probando conexión con Google Calendar...

✅ Conexión exitosa!

📅 Calendarios disponibles:
   • tu-email@gmail.com (Principal)

✨ Todo listo para crear eventos en tu calendario.
```

---

## 🧪 **Paso 8: Probar la Integración**

### Verificar desde el Backend

```bash
# Reiniciar backend para cargar Google Calendar
pkill -f "python run.py"
cd /Users/hp/Campo\ sagrado\ MVP/backend
source venv/bin/activate
python run.py > /tmp/campo-sagrado-backend.log 2>&1 &

# Esperar 3 segundos
sleep 3

# Probar endpoint
curl http://localhost:8000/api/maghrib/verificar-google-calendar | jq .
```

**Output esperado**:
```json
{
  "conectado": true,
  "mensaje": "Google Calendar conectado correctamente",
  "calendarios_disponibles": 1,
  "listo_para_usar": true
}
```

---

## 🎯 **Paso 9: Crear Tu Primera Jornada**

```bash
# Crear jornada para mañana
curl -X POST http://localhost:8000/api/maghrib/preparar-dia-siguiente \
  -H "Content-Type: application/json" \
  -d '{
    "intencion": "Completar integración de Google Calendar con energía enfocada",
    "asistentes": []
  }' | jq .
```

**Si funciona, verás**:
```json
{
  "plan": { ... },
  "eventos_creados": 9,
  "fecha": "2025-10-09",
  "google_calendar_url": "https://calendar.google.com/..."
}
```

### Ver los eventos en Google Calendar

1. Abre: https://calendar.google.com
2. Busca la fecha de mañana
3. Deberías ver:
   - 🌅 Estado Cero - FAJR (6:00-6:30)
   - ☀️ Estado Cero - DHUHR (13:00-13:30)
   - 🌤️ Estado Cero - ASR (16:00-16:30)
   - 🌆 Estado Cero - MAGHRIB (19:00-19:30)
   - 🌙 Estado Cero - ISHA (22:00-22:30)
   - ✓ No-Negociables del Día (6:00-6:05)
   - + Bloques de trabajo sugeridos

---

## 🐛 **Troubleshooting**

### Error: "Credentials file not found"
```bash
# Verifica que el archivo exista
ls backend/config/google_credentials.json

# Si no existe, repite el Paso 6
```

### Error: "Token has been expired or revoked"
```bash
# Elimina el token antiguo y re-autentica
rm backend/config/google_token.json
python scripts/setup_google_calendar.py
```

### Error: "Access blocked: Campo Sagrado's request is invalid"
- Verifica que añadiste tu email en "Test users" (Paso 4.6)
- Usa el mismo email que estás intentando autorizar

### No se crean eventos en Calendar
```bash
# Verifica que el backend esté corriendo
curl http://localhost:8000/api/health

# Verifica conexión con Google Calendar
curl http://localhost:8000/api/maghrib/verificar-google-calendar

# Revisa logs del backend
tail -50 /tmp/campo-sagrado-backend.log
```

---

## 👥 **Compartir Jornada con Pareja/Círculo**

Para compartir tu disponibilidad:

```bash
curl -X POST http://localhost:8000/api/maghrib/preparar-dia-siguiente \
  -H "Content-Type: application/json" \
  -d '{
    "intencion": "Mi intención del día",
    "asistentes": ["pareja@email.com", "amigo@email.com"]
  }'
```

**Ellos recibirán**:
- Email de invitación automático de Google Calendar
- Podrán ver tus bloques de trabajo (NO los Estados Cero, esos son privados)
- Sincronización en tiempo real

---

## 🎨 **Próximo Paso: Frontend**

Una vez que el backend funciona, continúa con el frontend:

```bash
# Ver guía de frontend
open frontend/src/routes/ritual-maghrib/README.md
```

---

## 🆘 **¿Necesitas Ayuda?**

Si algo no funciona:
1. Revisa los logs: `tail -f /tmp/campo-sagrado-backend.log`
2. Verifica cada paso de esta guía
3. Asegúrate de usar el mismo email en Google Cloud y al autorizar

---

✨ **Una vez completado este setup, nunca tendrás que hacerlo de nuevo.** El token se renueva automáticamente. 🕌

