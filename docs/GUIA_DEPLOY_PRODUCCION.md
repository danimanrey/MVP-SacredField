# 🚀 Guía de Deploy a Producción - Campo Sagrado

## Paso a Paso con Precisión Quirúrgica

**Tiempo estimado:** 4-6 horas  
**Dificultad:** Media  
**Prerequisitos:** Cuenta en Vercel y Railway/Fly.io

---

## 📋 CHECKLIST PRE-DEPLOY

### ✅ Verificaciones Obligatorias

- [x] ✅ Todas las páginas funcionales (8/8)
- [x] ✅ TypeScript sin errores
- [x] ✅ ESLint limpio (solo warnings menores)
- [x] ✅ Build de Next.js exitoso
- [x] ✅ Backend corriendo sin errores
- [x] ✅ `.env` en `.gitignore`
- [x] ✅ Secretos generados
- [x] ✅ Rate limiting activo
- [x] ✅ Security headers configurados
- [x] ✅ Documentación completa

**Estado:** ✅ **LISTO PARA DEPLOY**

---

## 🎯 ARQUITECTURA DE PRODUCCIÓN

```
┌─────────────────────────────────────────────────────┐
│                   USUARIOS                          │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              VERCEL CDN (Edge)                      │
│         https://campo-sagrado.vercel.app            │
│                                                      │
│  ┌────────────────────────────────────────────┐   │
│  │  Next.js 15 (Frontend)                     │   │
│  │  • React 18 + TypeScript                    │   │
│  │  • React Three Fiber (3D)                   │   │
│  │  • 8 páginas funcionales                    │   │
│  │  • SSL automático                           │   │
│  └────────────────────────────────────────────┘   │
└──────────────────┬──────────────────────────────────┘
                   │ HTTPS
                   │ API Calls
                   ▼
┌─────────────────────────────────────────────────────┐
│         RAILWAY/FLY.IO (Backend)                    │
│         https://api.campo-sagrado.com               │
│                                                      │
│  ┌────────────────────────────────────────────┐   │
│  │  FastAPI (Backend)                         │   │
│  │  • Python 3.11                              │   │
│  │  • 30+ endpoints REST                       │   │
│  │  • PostgreSQL                               │   │
│  │  • SSL automático                           │   │
│  └────────────────────────────────────────────┘   │
│                                                      │
│  ┌────────────────────────────────────────────┐   │
│  │  PostgreSQL Database                        │   │
│  │  • Backups automáticos                      │   │
│  │  • Persistencia                             │   │
│  └────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 📦 PARTE 1: DEPLOY DEL FRONTEND (Vercel)

### Paso 1: Preparar el Repositorio

```bash
cd "/Users/hp/campo-sagrado-nextjs"

# 1. Inicializar git (si no está)
git init

# 2. Crear .gitignore
echo "node_modules
.next
out
.env.local
.DS_Store
*.log" > .gitignore

# 3. Hacer commit inicial
git add .
git commit -m "🚀 Initial commit: Campo Sagrado Next.js v1.0"

# 4. Crear repositorio en GitHub (opcional)
# gh repo create campo-sagrado-nextjs --private --source=. --remote=origin
```

---

### Paso 2: Configurar Vercel

#### 2.1 Crear Cuenta
1. Ir a https://vercel.com
2. Sign up con GitHub
3. Verificar email

#### 2.2 Instalar Vercel CLI

```bash
npm install -g vercel

# Login
vercel login
```

#### 2.3 Deploy Inicial

```bash
cd "/Users/hp/campo-sagrado-nextjs"

# Deploy (modo interactivo)
vercel

# Responder:
# Set up and deploy? Y
# Which scope? <tu-usuario>
# Link to existing project? N
# What's your project's name? campo-sagrado
# In which directory is your code located? ./
# Want to override settings? N
```

---

### Paso 3: Configurar Variables de Entorno en Vercel

#### 3.1 Via Dashboard

1. Ir a https://vercel.com/dashboard
2. Seleccionar proyecto `campo-sagrado`
3. Settings → Environment Variables
4. Añadir:

```
NEXT_PUBLIC_API_URL
  Production:  https://api.campo-sagrado.railway.app
  Preview:     https://api-preview.campo-sagrado.railway.app
  Development: http://localhost:8000

NODE_ENV
  Production:  production
```

#### 3.2 Via CLI

```bash
vercel env add NEXT_PUBLIC_API_URL production
# Pegar: https://api.campo-sagrado.railway.app

vercel env add NODE_ENV production
# Pegar: production
```

---

### Paso 4: Deploy a Producción

```bash
# Build local (verificar que funciona)
npm run build

# Deploy a producción
vercel --prod

# Obtener URL
# https://campo-sagrado.vercel.app
```

---

### Paso 5: Configurar Dominio Personalizado (Opcional)

```bash
# En Vercel Dashboard
# Settings → Domains → Add Domain

# Ejemplo: campo-sagrado.com
# Configurar DNS:
# A record: 76.76.21.21
# CNAME: cname.vercel-dns.com
```

---

## 🖥️ PARTE 2: DEPLOY DEL BACKEND (Railway)

### Paso 1: Preparar el Backend

```bash
cd "/Users/hp/Campo sagrado MVP/backend"

# 1. Crear Procfile para Railway
echo "web: uvicorn api.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 2. Crear runtime.txt
echo "python-3.11" > runtime.txt

# 3. Verificar requirements.txt completo
cat requirements.txt

# 4. Crear .railwayignore
echo "venv/
__pycache__/
*.pyc
.env
.env.local
*.db
logs/" > .railwayignore
```

---

### Paso 2: Configurar Railway

#### 2.1 Crear Cuenta
1. Ir a https://railway.app
2. Sign up con GitHub
3. Verificar email

#### 2.2 Instalar Railway CLI

```bash
# macOS
brew install railway

# O con npm
npm install -g @railway/cli

# Login
railway login
```

#### 2.3 Crear Proyecto

```bash
cd "/Users/hp/Campo sagrado MVP/backend"

# Inicializar Railway
railway init

# Responder:
# Project name: campo-sagrado-backend
# Environment: production
```

---

### Paso 3: Configurar Base de Datos PostgreSQL

```bash
# Añadir PostgreSQL al proyecto
railway add

# Seleccionar: PostgreSQL

# Railway genera automáticamente:
# DATABASE_URL=postgresql://postgres:...@...railway.app:5432/railway
```

---

### Paso 4: Configurar Variables de Entorno

```bash
# Generar secretos (ya generados antes)
# Usar los valores del script generar_secretos.py

# Configurar variables
railway variables set ENV=production
railway variables set JWT_SECRET_KEY="W(}X;xvaq{SyW8Aljx(~RJuKq2A+w!z.@4bRKKZ5=BrB*>(+A&Tqd3p44*UW>\`k:"
railway variables set CORS_ORIGINS="https://campo-sagrado.vercel.app"
railway variables set ALLOWED_HOSTS="campo-sagrado-backend.railway.app"
railway variables set ANTHROPIC_API_KEY="sk-ant-api03-TU_CLAVE_AQUI"
railway variables set LATITUD="40.5472"
railway variables set LONGITUD="-3.6228"
railway variables set TIMEZONE="Europe/Madrid"

# Verificar
railway variables
```

---

### Paso 5: Deploy a Railway

```bash
# Deploy
railway up

# Esperar build (3-5 minutos)
# Railway construirá:
# 1. Instalar dependencias (pip install -r requirements.txt)
# 2. Ejecutar migraciones (si las hay)
# 3. Iniciar uvicorn

# Obtener URL
railway domain
# https://campo-sagrado-backend.railway.app
```

---

### Paso 6: Verificar Deploy del Backend

```bash
# Health check
curl https://campo-sagrado-backend.railway.app/api/health

# Debe retornar JSON con status: "healthy"

# Verificar headers de seguridad
curl -I https://campo-sagrado-backend.railway.app/api/health

# Debe incluir:
# x-ratelimit-limit
# x-content-type-options
# x-frame-options
```

---

## 🔄 PARTE 3: CONECTAR FRONTEND ↔ BACKEND

### Paso 1: Actualizar Variable de Entorno en Vercel

```bash
# Actualizar URL del backend
vercel env rm NEXT_PUBLIC_API_URL production
vercel env add NEXT_PUBLIC_API_URL production
# Pegar: https://campo-sagrado-backend.railway.app
```

---

### Paso 2: Redeploy Frontend

```bash
cd "/Users/hp/campo-sagrado-nextjs"

# Redeploy para que tome nueva URL
vercel --prod

# Esperar build (2-3 minutos)
```

---

### Paso 3: Actualizar CORS en Backend

```bash
# En Railway dashboard
railway variables set CORS_ORIGINS="https://campo-sagrado.vercel.app,https://www.campo-sagrado.com"

# Redeploy
railway up
```

---

### Paso 4: Verificar Integración

```bash
# Abrir frontend en producción
# https://campo-sagrado.vercel.app

# Verificar en consola del navegador:
# - API calls exitosos
# - Sin errores CORS
# - Headers de seguridad presentes
```

---

## 🗄️ PARTE 4: MIGRACIÓN DE BASE DE DATOS

### Opción A: Migrar SQLite → PostgreSQL

```bash
# 1. Exportar datos de SQLite
cd "/Users/hp/Campo sagrado MVP"
sqlite3 storage/organismo.db .dump > backup-sqlite.sql

# 2. Convertir a formato PostgreSQL
# (Editar backup-sqlite.sql manualmente o usar pgloader)

# 3. Importar a PostgreSQL de Railway
railway run psql < backup-postgresql.sql
```

### Opción B: Empezar con BD Vacía (Recomendado para MVP)

```bash
# Railway crea PostgreSQL vacío automáticamente
# Backend inicializa tablas al arrancar (init_db())
# Empezar fresh en producción
```

---

## 🔒 PARTE 5: CONFIGURACIÓN DE SEGURIDAD FINAL

### Paso 1: Verificar Secretos en Producción

```bash
# Vercel
vercel env ls

# Railway
railway variables

# ⚠️ NUNCA exponer estos valores públicamente
```

---

### Paso 2: Configurar Monitoring

#### Sentry (Errores)

```bash
# 1. Crear cuenta en sentry.io
# 2. Crear proyecto "campo-sagrado"
# 3. Obtener DSN

# Backend
pip install sentry-sdk
railway variables set SENTRY_DSN="https://...@sentry.io/..."

# Frontend
npm install @sentry/nextjs
vercel env add NEXT_PUBLIC_SENTRY_DSN production
```

#### Railway Logs

```bash
# Ver logs en tiempo real
railway logs

# Filtrar errores
railway logs | grep ERROR
```

---

### Paso 3: Configurar Backups

```bash
# Railway hace backups automáticos de PostgreSQL
# Configurar retención:
# Dashboard → Database → Backups → Configure

# Backup manual
railway run pg_dump > backup-$(date +%Y%m%d).sql
```

---

## 🧪 PARTE 6: TESTING EN PRODUCCIÓN

### Paso 1: Smoke Tests

```bash
# Health check
curl https://campo-sagrado-backend.railway.app/api/health

# Calendario Hijri
curl https://campo-sagrado-backend.railway.app/api/calendario-hijri/hoy

# Dimensión prioritaria
curl https://campo-sagrado-backend.railway.app/api/octavas/dimension-hoy

# Rate limiting
for i in {1..12}; do
  curl -w "%{http_code} " https://campo-sagrado-backend.railway.app/api/health
done
# Debe retornar 429 después del límite
```

---

### Paso 2: Testing del Frontend

```bash
# Abrir en navegador
open https://campo-sagrado.vercel.app

# Verificar:
# ✅ Todas las páginas cargan
# ✅ 3D renderiza correctamente
# ✅ API calls funcionan
# ✅ No hay errores en consola
# ✅ Headers de seguridad presentes
```

---

### Paso 3: Performance Testing

```bash
# Lighthouse CI
npx lighthouse https://campo-sagrado.vercel.app --view

# Métricas objetivo:
# Performance: > 80
# Accessibility: > 85
# Best Practices: > 90
# SEO: > 85
```

---

## 🔐 PARTE 7: HARDENING FINAL

### Paso 1: Revisar Logs

```bash
# Backend
railway logs --tail 100

# Buscar:
# ❌ Errores críticos
# ❌ API keys expuestas
# ❌ Stack traces completos
# ✅ Rate limiting funcionando
```

---

### Paso 2: Configurar Alertas

```bash
# Railway Webhooks
# Dashboard → Settings → Webhooks
# URL: https://hooks.slack.com/... (o Discord)
# Events: deployments, crashes
```

---

### Paso 3: Documentar URLs de Producción

```bash
# Crear archivo de URLs
cat > URLS_PRODUCCION.md << 'EOL'
# 🌐 URLs de Producción

## Frontend
- **Principal:** https://campo-sagrado.vercel.app
- **Dashboard:** https://campo-sagrado.vercel.app/dashboard
- **Estado Cero:** https://campo-sagrado.vercel.app/estado-cero

## Backend
- **API:** https://campo-sagrado-backend.railway.app
- **Health:** https://campo-sagrado-backend.railway.app/api/health
- **Docs:** (Ocultos en producción)

## Monitoring
- **Sentry:** https://sentry.io/organizations/.../projects/campo-sagrado/
- **Railway Logs:** railway logs

## Administración
- **Vercel Dashboard:** https://vercel.com/dashboard
- **Railway Dashboard:** https://railway.app/dashboard

---

🔐 Mantener este archivo PRIVADO
EOL
```

---

## 🚨 PARTE 8: PLAN DE ROLLBACK

### Si algo falla:

```bash
# Frontend (Vercel)
vercel rollback
# Seleccionar deployment anterior

# Backend (Railway)
railway rollback
# Seleccionar deployment anterior

# Variables de entorno
railway variables set <VAR>=<valor_anterior>
```

---

## 📊 PARTE 9: MONITORING POST-DEPLOY

### Primera Hora

```bash
# Ver logs en tiempo real
railway logs

# Verificar métricas
# - Requests/minuto
# - Errores
# - Tiempo de respuesta
# - Rate limiting
```

### Primera Semana

```bash
# Diariamente:
# 1. Revisar Sentry para errores
# 2. Ver logs de Railway
# 3. Verificar backups de BD
# 4. Monitorear costos de Claude API
# 5. Revisar métricas de Vercel Analytics
```

---

## 🔧 COMANDOS ÚTILES

### Vercel

```bash
# Ver deployments
vercel ls

# Ver logs
vercel logs <deployment-url>

# Alias (dominio personalizado)
vercel alias <deployment-url> campo-sagrado.com

# Rollback
vercel rollback

# Variables de entorno
vercel env ls
vercel env pull  # Descargar a .env.local
```

### Railway

```bash
# Ver proyectos
railway list

# Logs en tiempo real
railway logs

# Conectar a DB
railway run psql

# Ejecutar comando
railway run python manage.py migrate

# Variables
railway variables
railway variables set KEY=value

# Rollback
railway rollback
```

---

## 🎯 CHECKLIST POST-DEPLOY

### Verificaciones Obligatorias

- [ ] ✅ Frontend accesible vía HTTPS
- [ ] ✅ Backend accesible vía HTTPS
- [ ] ✅ API calls funcionando
- [ ] ✅ Sin errores CORS
- [ ] ✅ Headers de seguridad presentes
- [ ] ✅ Rate limiting funcionando
- [ ] ✅ SSL certificates válidos
- [ ] ✅ Lighthouse score > 80
- [ ] ✅ Sentry capturando errores
- [ ] ✅ Logs limpios (sin errores)
- [ ] ✅ Backups configurados
- [ ] ✅ Variables de entorno correctas
- [ ] ✅ Costos de Claude API monitoreados

---

## 📈 COSTOS ESTIMADOS

### Vercel
```
Free Tier (Hobby):
- 100 GB bandwidth/mes
- Despliegues ilimitados
- SSL automático
- Dominio .vercel.app

Costo: $0/mes ✅
```

### Railway
```
Starter Plan:
- $5/mes de crédito incluido
- PostgreSQL: ~$2-3/mes
- Backend: ~$2-3/mes

Costo: ~$5/mes ✅
```

### Anthropic Claude
```
Variable según uso:
- Estado Cero: ~$0.05/sesión
- 5 sesiones/día = ~$0.25/día
- Mes: ~$7.50

Optimizar con:
- Caché de respuestas
- Prompts más cortos
- Usar Haiku para tareas simples
```

**Total estimado:** ~$15-20/mes

---

## 🔐 SEGURIDAD POST-DEPLOY

### Auditoría Semanal

```bash
# 1. Verificar headers
curl -I https://campo-sagrado.vercel.app

# 2. Test de penetración básico
# https://observatory.mozilla.org
# https://securityheaders.com

# 3. Revisar dependencias
npm audit
pip install safety && safety check

# 4. Verificar logs de acceso
railway logs | grep 401
railway logs | grep 429

# 5. Revisar uso de Claude API
# console.anthropic.com → Usage
```

---

## 🚨 PLAN DE EMERGENCIA

### Si el Backend Cae

```bash
# 1. Ver logs
railway logs --tail 100

# 2. Rollback
railway rollback

# 3. Reiniciar
railway restart

# 4. Escalar recursos (si es necesario)
# Dashboard → Settings → Resources
```

### Si el Frontend Falla

```bash
# 1. Ver logs
vercel logs

# 2. Rollback
vercel rollback

# 3. Verificar variables de entorno
vercel env ls

# 4. Redeploy
vercel --prod
```

### Si se Expone un Secreto

```bash
# 1. Rotar inmediatamente
python backend/scripts/generar_secretos.py

# 2. Actualizar en Railway
railway variables set JWT_SECRET_KEY="<nuevo>"

# 3. Revocar Claude API key
# console.anthropic.com → Settings → Revoke

# 4. Generar nueva
# Actualizar en Railway

# 5. Redeploy
railway up
```

---

## ✅ VERIFICACIÓN FINAL

### Lista de Comprobación

```bash
# Frontend
✅ https://campo-sagrado.vercel.app → Carga
✅ Dashboard 3D → Renderiza
✅ Estado Cero → Funcional
✅ Vista Semanal → Interactiva
✅ Vista Anual → Orbital
✅ Espejo Diario → Datos reales
✅ 7 Dimensiones → Grid arcoíris

# Backend
✅ https://api.railway.app/api/health → {"status": "healthy"}
✅ Rate limiting → 429 después de límite
✅ Headers → Presentes
✅ CORS → Sin errores
✅ PostgreSQL → Conectado

# Seguridad
✅ HTTPS → Forzado
✅ SSL → Válido
✅ Headers → Completos
✅ Secrets → Protegidos
✅ Logs → Sin info sensible
```

---

## 🎊 CELEBRACIÓN

Una vez completados todos los pasos:

```
╔════════════════════════════════════════════════╗
║                                                ║
║  🎉 DEPLOY COMPLETADO CON ÉXITO              ║
║                                                ║
║  Frontend:  https://campo-sagrado.vercel.app  ║
║  Backend:   https://api.railway.app           ║
║                                                ║
║  🌍 EL ORGANISMO ESTÁ VIVO EN EL MUNDO       ║
║                                                ║
╚════════════════════════════════════════════════╝
```

---

**مَا شَاءَ ٱللَّٰهُ**

*"Del localhost al mundo.  
De la visión a la manifestación.  
Del código a la realidad.  
El organismo respira en la nube."*

إن شاء الله

---

**Autor:** Campo Sagrado DevOps Team  
**Última actualización:** 9 de octubre de 2025  
**Versión:** 1.0.0  
**Estado:** ✅ Ready for Production

