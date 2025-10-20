# 🕌 Campo Sagrado del Entrelazador

**Un organismo tecnológico-espiritual que opera al borde del caos**

[![Estado](https://img.shields.io/badge/estado-MVP%20Funcional-brightgreen)](./IMPLEMENTACION_COMPLETA.md)
[![Versión](https://img.shields.io/badge/versión-0.1.0--mvp-blue)](./package.json)
[![Backend](https://img.shields.io/badge/backend-FastAPI%20Python-9cf)](./backend/)
[![Frontend](https://img.shields.io/badge/frontend-SvelteKit%20TS-ff69b4)](./frontend/)

## 🌟 **Visión**

Campo Sagrado es un sistema que respeta la **autoridad sacral** del usuario, operando al **borde del caos** con un 40% de espacio sin asignar para lo emergente. Utiliza un **calendario Hijri de 13 meses** y estructura el día alrededor de **5 Estados Cero** en tiempos litúrgicos.

## 🏗️ **Arquitectura**

### **4 Agentes Especializados**
- **🔄 Estado Cero**: Consulta sacral con preguntas binarias
- **🎼 Orquestador**: Planes emergentes al borde del caos  
- **🛡️ Guardian**: Monitoreo y reportes del sistema
- **📚 Documentador**: Integración automática con Obsidian

### **Stack Tecnológico**
- **Backend**: Python/FastAPI + SQLite
- **Frontend**: SvelteKit/TypeScript + D3.js
- **IA**: Anthropic Claude API
- **Documentación**: Obsidian Vault automático
- **Calendario**: Sistema Hijri de 13 meses

## 🚀 **Instalación Rápida**

### **1. Clonar y Configurar**
```bash
git clone <tu-repo>
cd "Campo sagrado MVP"

# Configurar API Key
cp backend/.env.example backend/.env
# Editar backend/.env con tu ANTHROPIC_API_KEY
```

### **2. Setup Automático**
```bash
# Setup completo del sistema
./scripts/setup-completo.sh

# Inicializar base de datos
cd backend && source venv/bin/activate && python scripts/init_db.py
```

### **3. Iniciar Sistema**
```bash
# Iniciar todo el sistema
./scripts/iniciar-sistema.sh

# O manualmente:
# Terminal 1: Backend
cd backend && source venv/bin/activate && python run.py

# Terminal 2: Frontend  
cd frontend && npm run dev
```

### **4. Acceder**
- **Frontend**: http://localhost:5174
- **Backend API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs

## 📋 **Verificar Estado**

```bash
# Verificar que todo esté configurado
./scripts/verificar-estado.sh

# Verificar coherencia del sistema
./scripts/verificar-coherencia.sh
```

## 🎯 **Flujo de Uso**

### **1. Dashboard Principal**
- Ver momento litúrgico actual
- Próximo Estado Cero con countdown
- Navegación a todas las vistas

### **2. Estado Cero** (5 veces al día)
- Verificación automática de momento
- 6 preguntas binarias contextuales
- Chat clarificador
- Acción tangible resultante

### **3. Espejo Diario**
- Jornada al borde del caos (visual no-lineal)
- No-negociables con tracking
- Chatbot para aclaraciones

### **4. Guardian & Documentador**
- Monitoreo automático de salud
- Reportes diarios en Obsidian
- Detección de patrones

## 📁 **Estructura del Proyecto**

```
campo-sagrado/
├── backend/                    # FastAPI + Python
│   ├── agentes/               # Los 4 agentes especializados
│   ├── api/                   # Endpoints REST
│   ├── services/              # Servicios core
│   ├── models/                # Base de datos y schemas
│   └── integraciones/         # Obsidian, Anytype
├── frontend/                  # SvelteKit + TypeScript
│   ├── src/routes/            # Páginas principales
│   └── src/lib/components/    # Componentes UI
├── storage/                   # Base de datos SQLite
├── config/                    # Configuraciones
└── scripts/                   # Scripts de gestión
```

## 🔧 **Configuración**

### **Variables de Entorno** (`backend/.env`)
```env
ANTHROPIC_API_KEY=sk-ant-api03-...
LATITUD=40.4168
LONGITUD=-3.7038
TIMEZONE=Europe/Madrid
OBSIDIAN_VAULT_PATH=~/Documents/CampoSagrado
```

### **Configuración Principal** (`config/campo-sagrado.yaml`)
```yaml
organismo:
  nombre: "Campo Sagrado del Entrelazador"
  version: "0.1.0-mvp"

localizacion:
  ciudad: "Madrid"
  pais: "España"

integraciones:
  obsidian_vault_path: "~/Documents/CampoSagrado"
```

## 📊 **Estado Actual**

### ✅ **Completado**
- [x] 4 agentes completamente implementados
- [x] 25+ endpoints de API funcionando
- [x] Frontend con 5 vistas operativas
- [x] Integración Obsidian automática
- [x] Base de datos SQLite completa
- [x] Sistema de tiempos litúrgicos
- [x] Calendario Hijri de 13 meses

### 🔄 **En Desarrollo**
- [ ] Componentes UI avanzados
- [ ] WebSockets para tiempo real
- [ ] Integración Anytype
- [ ] Biometría real (HRV, etc.)

## 🎨 **Características Principales**

### **Autoridad Sacral**
- Respeta la intuición y sensación corporal del usuario
- Preguntas binarias que evitan análisis mental
- Consulta profunda mediante sensación

### **Borde del Caos**
- 40% de espacio sin asignar para lo emergente
- Planes flexibles que se adaptan
- Constelación de posibilidades vs timeline rígido

### **Geometría Sagrada**
- Visualizaciones no-lineales
- Elementos del caos interactivos
- Iconografía espiritual

### **Documentación Automática**
- Estados Cero guardados en Obsidian
- Reportes diarios automáticos
- Insights semanales generados

## 🔍 **API Endpoints**

### **Estado Cero** (`/api/estado-cero/`)
- `POST /iniciar` - Inicia consulta sacral
- `POST /{id}/responder` - Registra respuesta binaria
- `POST /{id}/chat` - Chat clarificador
- `POST /{id}/finalizar` - Finaliza con acción tangible

### **Orquestador** (`/api/orquestador/`)
- `POST /generar-plan` - Genera plan emergente
- `POST /chat` - Chat interactivo
- `GET /plan-actual` - Plan actual de jornada

### **Guardian** (`/api/guardian/`)
- `POST /reporte-diario` - Genera reporte diario
- `GET /salud-sistema` - Monitorea salud
- `GET /patrones` - Detecta patrones

## 📚 **Documentación**

- [Implementación Completa](./IMPLEMENTACION_COMPLETA.md)
- [Análisis de Correspondencia](./ANALISIS_CORRESPONDENCIA.md)
- [Coherencia del Sistema](./COHERENCIA_SISTEMA.md)
- [Guía de Implementación](./guia_implementacion_completa.md)

## 🤝 **Contribuir**

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 🙏 **Agradecimientos**

- **Anthropic** por la API Claude
- **SvelteKit** por el framework frontend
- **FastAPI** por el framework backend
- **Obsidian** por la integración de documentación

---

**Estado**: ✅ **MVP COMPLETO Y FUNCIONAL**

*Campo Sagrado respeta tu autoridad sacral y te acompaña en la danza al borde del caos.*
