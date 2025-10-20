# 🛡️ Guía de Seguridad para Producción

## Lista de Verificación Antes del Deploy

---

## ✅ 1. VERIFICACIÓN DE SECRETOS

### Generar Nuevos Secretos

```bash
cd backend
python scripts/generar_secretos.py
```

Copiar los valores generados a `.env`:
```bash
JWT_SECRET_KEY=<secret_generado>
```

### Verificar `.gitignore`

```bash
# Confirmar que .env NO esté en git
git status --ignored | grep .env

# Debe aparecer:
# .env (ignored)
```

### Rotar Claude API Key (si es necesario)

1. Ir a https://console.anthropic.com
2. Generar nueva API key
3. Actualizar en `.env`:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-api03-NUEVA_KEY_AQUI
   ```
4. Revocar la anterior

---

## ✅ 2. CONFIGURACIÓN DE ENTORNO

### Backend (`backend/.env`)

```bash
# Entorno
ENV=production

# Seguridad
JWT_SECRET_KEY=<generar_con_script>
CORS_ORIGINS=https://tu-dominio.vercel.app
ALLOWED_HOSTS=tu-dominio.vercel.app,api.tu-dominio.com

# API Keys (usar secrets manager)
ANTHROPIC_API_KEY=sk-ant-api03-...

# Base de datos (en producción, usar PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/campo_sagrado

# Localización
LATITUD=40.5472
LONGITUD=-3.6228
TIMEZONE=Europe/Madrid

# Configuración
DEBUG=false
LOG_LEVEL=WARNING
```

### Frontend (`campo-sagrado-nextjs/.env.local`)

```bash
NEXT_PUBLIC_API_URL=https://api.tu-dominio.com
NODE_ENV=production
```

---

## ✅ 3. INSTALACIÓN DE DEPENDENCIAS DE SEGURIDAD

### Backend

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Verificar que se instalaron:
pip list | grep -E "PyJWT|cryptography|passlib"
```

### Verificar Vulnerabilidades

```bash
# Instalar safety
pip install safety

# Escanear dependencias
safety check --json

# Actualizar si hay vulnerabilidades
pip install --upgrade <paquete_vulnerable>
```

---

## ✅ 4. CONFIGURACIÓN DE CORS

### Para Producción

Editar `backend/api/main.py` o configurar en `.env`:

```python
# En .env
CORS_ORIGINS=https://campo-sagrado.vercel.app,https://www.campo-sagrado.com
```

⚠️ **NUNCA usar `*` en producción:**
```python
allow_origins=["*"]  # ❌ VULNERABLE
```

✅ **Usar dominio específico:**
```python
allow_origins=["https://campo-sagrado.vercel.app"]  # ✅ SEGURO
```

---

## ✅ 5. RATE LIMITING

### Verificar que esté Activo

```bash
# En logs del backend debe aparecer:
✅ Middleware de seguridad activado
```

### Límites Configurados

```python
"estado_cero": 10 requests/minuto
"planificar":  20 requests/minuto
"general":     100 requests/minuto
"health":      300 requests/minuto
```

### Testing

```bash
# Probar rate limiting
for i in {1..15}; do
  curl http://localhost:8000/api/estado-cero/verificar-momento
  sleep 0.1
done

# Debe retornar 429 después de 10 requests
```

---

## ✅ 6. AUTENTICACIÓN (Opcional para MVP)

### Generar Token de Desarrollo

```python
from services.auth import create_dev_token
token = create_dev_token()
print(token)
```

### Usar Token en Requests

```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/protected-endpoint
```

### En Frontend

```typescript
// Guardar token al login
localStorage.setItem('auth_token', token);

// El API client lo usa automáticamente
```

---

## ✅ 7. HTTPS / TLS

### Desarrollo (HTTP ok)

```
http://localhost:8000  ✅
http://localhost:3000  ✅
```

### Producción (HTTPS requerido)

```
https://api.tu-dominio.com  ✅
https://tu-dominio.com      ✅
```

#### Configurar en Vercel

- ✅ Automático (certificado SSL gratis)

#### Configurar en Railway/Fly.io

- ✅ Automático (certificado SSL gratis)

---

## ✅ 8. BASE DE DATOS

### Desarrollo (SQLite ok)

```bash
storage/organismo.db  ✅
```

### Producción (PostgreSQL recomendado)

```bash
# Migrar de SQLite a PostgreSQL

# 1. Instalar
pip install psycopg2-binary

# 2. Configurar DATABASE_URL
postgresql://user:password@host:5432/campo_sagrado

# 3. Migrar datos (si hay)
# Usar alembic o script personalizado
```

#### Backups Automáticos

```bash
# Cron job para backups
0 */6 * * * pg_dump campo_sagrado > backup-$(date +\%Y\%m\%d).sql
```

---

## ✅ 9. SECURITY HEADERS

### Verificar Headers en Producción

```bash
curl -I https://tu-dominio.com

# Debe incluir:
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Content-Security-Policy: ...
```

---

## ✅ 10. LOGGING SEGURO

### NO Registrar:

❌ API keys
❌ Tokens JWT
❌ Passwords
❌ Información personal identificable (PII)
❌ Stack traces completos (en producción)

### SÍ Registrar:

✅ Timestamp
✅ Método HTTP
✅ Path
✅ Status code
✅ Tiempo de procesamiento
✅ IP (hasheada)

### Ejemplo Seguro:

```python
# ❌ NO hacer
logging.info(f"API Key: {api_key}")

# ✅ Hacer
logging.info(f"API request from IP: {hash(ip)}")
```

---

## ✅ 11. VARIABLES DE ENTORNO EN DEPLOY

### Vercel (Frontend)

Settings → Environment Variables:
```
NEXT_PUBLIC_API_URL = https://api.tu-dominio.com
NODE_ENV = production
```

### Railway/Fly.io (Backend)

```bash
# Railway
railway variables set ENV=production
railway variables set JWT_SECRET_KEY=<secret>
railway variables set ANTHROPIC_API_KEY=<key>

# Fly.io
fly secrets set ENV=production
fly secrets set JWT_SECRET_KEY=<secret>
fly secrets set ANTHROPIC_API_KEY=<key>
```

---

## ✅ 12. CHECKLIST FINAL

### Antes de Deploy:

- [ ] ✅ `.env` está en `.gitignore`
- [ ] ✅ No hay commits con `.env` en historial
- [ ] ✅ JWT_SECRET_KEY generado y configurado
- [ ] ✅ Claude API Key rotada (si se expuso)
- [ ] ✅ CORS configurado para dominio específico
- [ ] ✅ Rate limiting activado
- [ ] ✅ Security headers configurados
- [ ] ✅ HTTPS configurado (en producción)
- [ ] ✅ Logs sin información sensible
- [ ] ⏳ Tests de seguridad ejecutados
- [ ] ⏳ Backups configurados
- [ ] ⏳ Monitoring configurado

### Después de Deploy:

- [ ] Verificar headers de seguridad
- [ ] Probar rate limiting
- [ ] Verificar HTTPS funciona
- [ ] Monitorear logs de errores
- [ ] Configurar alertas
- [ ] Documentar proceso de rollback

---

## 🔥 COMANDOS ÚTILES

### Generar Secretos

```bash
python backend/scripts/generar_secretos.py
```

### Verificar Seguridad

```bash
# TypeScript
cd campo-sagrado-nextjs && npm run type-check

# Vulnerabilidades npm
cd campo-sagrado-nextjs && npm audit

# Vulnerabilidades pip
cd backend && pip install safety && safety check
```

### Probar Rate Limiting

```bash
# Script de prueba
for i in {1..150}; do
  curl -w "%{http_code}\n" http://localhost:8000/health
done | grep 429
```

### Verificar HTTPS

```bash
curl -I https://tu-dominio.com
```

---

## ⚠️ ALERTAS Y MONITORING

### Sentry (Errores)

```bash
pip install sentry-sdk

# En main.py
import sentry_sdk
sentry_sdk.init(dsn="tu-dsn-aqui")
```

### Datadog (Métricas)

```bash
pip install ddtrace

# Ejecutar con:
ddtrace-run python run.py
```

---

## 🚨 PLAN DE EMERGENCIA

### Si se Expone un Secreto:

1. **Rotar inmediatamente:**
   ```bash
   python scripts/generar_secretos.py
   # Actualizar .env
   # Redeploy
   ```

2. **Revocar API keys comprometidas:**
   - Claude: console.anthropic.com
   - Google: console.cloud.google.com

3. **Limpiar historial de git (si está en commits):**
   ```bash
   # ⚠️ DESTRUCTIVO - hacer backup primero
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch backend/.env" \
     --prune-empty -- --all
   ```

4. **Notificar:**
   - Revisar logs de acceso
   - Verificar uso de API
   - Cambiar todos los secretos relacionados

---

## 📊 NIVELES DE SEGURIDAD

### Desarrollo (Actual)

```
Autenticación:     ⚠️  Opcional
Rate Limiting:     ✅  Activado
HTTPS:             ⚠️  HTTP ok
Headers:           ✅  Configurados
Logging:           ✅  Completo
```

**Seguridad:** 60% - OK para desarrollo

### Producción (Requerido)

```
Autenticación:     ✅  JWT obligatorio
Rate Limiting:     ✅  Estricto
HTTPS:             ✅  Forzado
Headers:           ✅  CSP completo
Logging:           ✅  Sin info sensible
Database:          ✅  PostgreSQL
Backups:           ✅  Automáticos
Monitoring:        ✅  Sentry + Datadog
```

**Seguridad:** 95%+ - Producción-ready

---

**مَا شَاءَ ٱللَّٰهُ**

*"La seguridad es como el wudu (ablución) antes del salat.  
Una purificación necesaria antes de presentarse."*

إن شاء الله

---

**Autor:** Campo Sagrado Security Team  
**Última actualización:** 9 de octubre de 2025  
**Versión:** 1.0.0

