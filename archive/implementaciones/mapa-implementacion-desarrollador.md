# MAPA DE IMPLEMENTACIÓN CAMPO SAGRADO
## Del Estado Actual al Sistema Funcional Completo

---

## 📊 ANÁLISIS DE CORRESPONDENCIA

### ✅ LO QUE TENEMOS (Estado Actual)

```yaml
INTERFACES_FRONTEND:
  - ✅ Estado Cero por tiempo de rezo (5 interfaces separadas)
  - ✅ Estructura básica de componentes
  - ✅ localhost funcionando
  
AGENTES_BACKEND:
  - ✅ Agente Estado Cero (Guía)
  - ✅ Agente Orquestador
  - ✅ Agente Documentador
  - ✅ Agente Guardian (mantenimiento)
  
ARQUITECTURA:
  - ✅ FastAPI backend estructurado
  - ✅ SvelteKit frontend estructurado
  - ✅ Concepto de flujo definido
  - ✅ Documentación extensa
```

### ⚠️ LO QUE FALTA (Gaps Críticos)

```yaml
CONEXIÓN_FRONTEND_BACKEND:
  - ❌ API client configurado
  - ❌ Stores conectados a endpoints reales
  - ❌ Flujo de datos completo
  
SERVICIOS_CORE:
  - ❌ Cálculo de tiempos litúrgicos
  - ❌ Cliente Claude funcional
  - ❌ Servicio de contexto
  
BASE_DE_DATOS:
  - ❌ PostgreSQL/SQLite configurado
  - ❌ Schemas definidos
  - ❌ Migraciones creadas
  
COMUNICACIÓN_AGENTES:
  - ❌ Agentes conectados entre sí
  - ❌ Event bus o sistema de mensajes
  - ❌ Flujo orquestado funcionando
  
INTEGRACIONES:
  - ❌ Anytype API conectada
  - ❌ Obsidian escritura automática
  - ❌ Exportación de datos
```

---

## 🎯 EL FLUJO REAL (Cómo Funciona Todo Junto)

### Diagrama de Flujo de Datos

```
┌──────────────────────────────────────────────────────────────┐
│                    USUARIO EN NAVEGADOR                       │
│                   http://localhost:5173                       │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ 1. Click "Iniciar Estado Cero"
                     ↓
┌──────────────────────────────────────────────────────────────┐
│              FRONTEND (SvelteKit)                             │
│  src/routes/estado-cero/+page.svelte                         │
│                                                               │
│  import { estadoCeroApi } from '$lib/api/client'             │
│  const resultado = await estadoCeroApi.iniciar('fajr')       │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ 2. HTTP POST /api/estado-cero/iniciar
                     ↓
┌──────────────────────────────────────────────────────────────┐
│              BACKEND API (FastAPI)                            │
│  backend/api/estado_cero.py                                  │
│                                                               │
│  @app.post("/estado-cero/iniciar")                          │
│  async def iniciar_estado_cero(momento: str):                │
│      # 3. Llamar al Agente Estado Cero                      │
│      contexto = servicio_contexto.recopilar()               │
│      resultado = agente_estado_cero.procesar(contexto)      │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ 4. Llamada a Agente
                     ↓
┌──────────────────────────────────────────────────────────────┐
│           AGENTE ESTADO CERO (Lógica IA)                     │
│  backend/agentes/estado_cero.py                              │
│                                                               │
│  class AgenteEstadoCero:                                     │
│      def procesar(self, contexto):                           │
│          # 5. Generar preguntas                              │
│          preguntas = self.generar_preguntas(contexto)        │
│          # 6. Llamar a Claude                                │
│          direccion = claude_client.sintetizar(respuestas)    │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ 7. Response con preguntas
                     ↓
┌──────────────────────────────────────────────────────────────┐
│              FRONTEND (Muestra Preguntas)                     │
│                                                               │
│  Usuario responde:                                            │
│  - ¿Expansión o contracción? → "expansion"                   │
│  - Intensidad 1-5 → 4                                        │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ 8. POST /estado-cero/{id}/responder
                     ↓
┌──────────────────────────────────────────────────────────────┐
│              BACKEND (Procesa Respuestas)                     │
│                                                               │
│  # Guarda respuestas en DB                                    │
│  db.save(respuestas)                                          │
│  # Cuando completa 6 preguntas:                               │
│  # 9. Llamar a Claude para síntesis                           │
│  direccion = claude_client.sintetizar_direccion(respuestas)  │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ 10. Dirección emergente generada
                     ↓
┌──────────────────────────────────────────────────────────────┐
│              FRONTEND (Muestra Dirección)                     │
│                                                               │
│  "Hoy pide ser servido: Arquitecturar sistema de agentes"    │
│  [Chat clarificador aparece]                                  │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ 11. Usuario dialoga con chat
                     ↓
┌──────────────────────────────────────────────────────────────┐
│              BACKEND (Chat Claude)                            │
│                                                               │
│  # Conversación iterativa                                     │
│  usuario: "¿Qué arquitectura específica?"                     │
│  claude: "Event-driven con Redis como bus..."                │
│  # Hasta que usuario dice "Listo"                             │
│  # 12. Genera acción concreta                                 │
│  accion = {                                                   │
│    descripcion: "Implementar event bus Redis",               │
│    resultado_observable: "Agentes se comunican",             │
│    duracion: "3 horas"                                        │
│  }                                                            │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ 13. POST /estado-cero/{id}/finalizar
                     ↓
┌──────────────────────────────────────────────────────────────┐
│         ORQUESTADOR TOMA CONTROL                              │
│  backend/agentes/orquestador.py                              │
│                                                               │
│  def generar_plan_jornada(accion, contexto):                 │
│      # 14. Analiza acción + contexto + no-negociables        │
│      plan = self.estructurar_jornada(                         │
│          accion_principal=accion,                             │
│          energia_disponible=contexto.energia,                 │
│          no_negociables=config.no_negociables                 │
│      )                                                        │
│      # 15. Genera bloques de tiempo flexibles                 │
│      return plan_al_borde_del_caos                            │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ 16. Plan generado
                     ↓
┌──────────────────────────────────────────────────────────────┐
│         FRONTEND: ESPEJO DIARIO                               │
│  src/routes/espejo-diario/+page.svelte                       │
│                                                               │
│  Muestra:                                                     │
│  06:30-10:00 → Implementar event bus Redis                    │
│  10:00-10:15 → Break + hidratación                            │
│  10:15-12:00 → [Espacio libre - emergencia]                   │
│  12:00-14:00 → Almuerzo consciente                            │
│  ...                                                          │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ 17. Usuario ejecuta durante el día
                     │     Captura insights en Anytype
                     ↓
┌──────────────────────────────────────────────────────────────┐
│         GUARDIAN MONITOREA (Background)                       │
│  backend/agentes/guardian.py                                 │
│                                                               │
│  # 18. Analiza métricas continuamente                         │
│  - ¿Cuánto tiempo en cada bloque?                             │
│  - ¿Se cumplieron no-negociables?                             │
│  - ¿Nivel de energía al final del día?                        │
│  # 19. Detecta patrones                                       │
│  - "Usuario más productivo 07:00-10:00"                       │
│  - "Ejercicio matutino → +2 puntos energía"                   │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ 20. Al final del día (Maghrib)
                     ↓
┌──────────────────────────────────────────────────────────────┐
│         DOCUMENTADOR ESCRIBE                                  │
│  backend/agentes/documentador.py                             │
│                                                               │
│  def generar_reporte_diario():                               │
│      # 21. Recopila todo el día                               │
│      data = {                                                 │
│          estado_cero: ...,                                    │
│          plan: ...,                                           │
│          ejecucion: ...,                                      │
│          insights_anytype: ...,                               │
│          metricas_guardian: ...                               │
│      }                                                        │
│      # 22. Genera markdown                                    │
│      md = self.generar_markdown(data)                         │
│      # 23. Escribe en Obsidian                                │
│      obsidian.write('40-Journal/2025-01-15.md', md)          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 IMPLEMENTACIÓN PASO A PASO

### PASO 1: Base de Datos (30 min)

**Archivo: `backend/models/database.py`**

```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class EstadoCero(Base):
    __tablename__ = 'estados_cero'
    
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    momento = Column(String(20))  # fajr, dhuhr, asr, maghrib, isha
    contexto = Column(JSON)  # Contexto completo recopilado
    respuestas = Column(JSON)  # Array de respuestas sacrales
    direccion_emergente = Column(String(500))
    accion_tangible = Column(JSON)
    chat_clarificacion = Column(JSON)
    completado = Column(Boolean, default=False)
    duracion_minutos = Column(Integer)
    claridad_promedio = Column(Float)

class PlanJornada(Base):
    __tablename__ = 'planes_jornada'
    
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    estado_cero_id = Column(Integer)
    bloques = Column(JSON)  # Array de bloques de tiempo
    no_negociables = Column(JSON)
    energia_estimada = Column(Integer)
    completado = Column(Boolean, default=False)

class MetricaGuardian(Base):
    __tablename__ = 'metricas_guardian'
    
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    tipo_metrica = Column(String(50))
    valor = Column(Float)
    contexto = Column(JSON)

# Setup
DATABASE_URL = "sqlite:///./storage/campo_sagrado.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Crear DB:**
```bash
cd backend
python -c "from models.database import init_db; init_db()"
```

---

### PASO 2: Cliente Claude (20 min)

**Archivo: `backend/services/claude_client.py`**

```python
import anthropic
import os
from typing import List, Dict

class ClaudeClient:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    
    def sintetizar_direccion(self, respuestas: List[Dict]) -> str:
        """
        Recibe las 6 respuestas sacrales y genera dirección emergente
        """
        # Construir contexto de respuestas
        respuestas_texto = "\n".join([
            f"Pregunta: {r['pregunta']}\n"
            f"Sensación: {r['sensacion']} (intensidad {r['intensidad']})\n"
            f"Nota: {r.get('nota', 'N/A')}"
            for r in respuestas
        ])
        
        prompt = f"""Eres el Agente Orientador Sacral del Campo Sagrado.

Has recibido las respuestas corporales del practicante a 6 consultas profundas:

{respuestas_texto}

Tu tarea: sintetizar UNA dirección clara y concreta que emerge de estas respuestas corporales.

Criterios:
- Máximo 2-3 frases
- Lenguaje directo y específico
- Basado en las sensaciones más fuertes (expansión/contracción)
- Orientado a acción, no reflexión abstracta
- Respeta la autoridad sacral del practicante

Genera la dirección emergente:"""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    
    def chat_clarificador(self, 
                         direccion: str, 
                         respuestas: List[Dict],
                         historial_chat: List[Dict],
                         mensaje_usuario: str) -> str:
        """
        Chat iterativo para clarificar acción específica
        """
        # Construir contexto completo
        contexto = f"""Dirección emergente: {direccion}

Respuestas originales:
{self._format_respuestas(respuestas)}

Conversación hasta ahora:
{self._format_historial(historial_chat)}

Nuevo mensaje del practicante: {mensaje_usuario}"""

        prompt = f"""Eres el Agente Orientador ayudando a clarificar la acción concreta.

{contexto}

Responde al practicante:
- Si hace pregunta, responde específicamente
- Si necesita claridad, ofrece opciones concretas
- Si está listo, ayuda a definir: QUÉ hacer, CÓMO saber que está hecho, CUÁNTO tiempo
- Mantén autoridad sacral del practicante (tú guías, él decide)

Respuesta:"""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    
    def _format_respuestas(self, respuestas):
        return "\n".join([f"- {r['pregunta']}: {r['sensacion']} ({r['intensidad']})" 
                         for r in respuestas])
    
    def _format_historial(self, historial):
        return "\n".join([f"{msg['role']}: {msg['content']}" 
                         for msg in historial])

# Singleton
claude_client = ClaudeClient()
```

---

### PASO 3: Servicio de Contexto (15 min)

**Archivo: `backend/services/contexto.py`**

```python
from datetime import datetime
import psutil
import requests

class ServicioContexto:
    def recopilar_contexto_completo(self):
        """
        Recopila todo el contexto necesario para Estado Cero
        """
        return {
            'temporal': self._contexto_temporal(),
            'biologico': self._contexto_biologico(),
            'financiero': self._contexto_financiero(),
            'conocimiento': self._contexto_conocimiento(),
            'tiempo_disponible_hoy': self._calcular_tiempo_disponible()
        }
    
    def _contexto_temporal(self):
        ahora = datetime.now()
        return {
            'fecha': ahora.strftime('%Y-%m-%d'),
            'hora': ahora.strftime('%H:%M'),
            'dia_semana': ahora.strftime('%A'),
            'momento_dia': self._determinar_momento_dia(ahora.hour),
            'estacion': self._determinar_estacion(ahora.month)
        }
    
    def _contexto_biologico(self):
        # Placeholder - se puede integrar con wearables
        return {
            'energia_estimada': 7,  # 1-10, podría venir de Oura/Whoop
            'calidad_sueno': 'buena',  # placeholder
            'ultimo_ejercicio': 'hace 1 día',  # placeholder
            'hidratacion': 'adecuada'  # placeholder
        }
    
    def _contexto_financiero(self):
        # Placeholder - se puede integrar con APIs bancarias
        return {
            'runway_actual': '6 meses',  # placeholder
            'ingreso_ultimo_mes': 'estable',  # placeholder
            'proyectos_activos': 2  # placeholder
        }
    
    def _contexto_conocimiento(self):
        # Placeholder - se puede integrar con Anytype/Obsidian
        return {
            'ultimas_capturas_anytype': [],  # Se llenará con API Anytype
            'proyectos_activos_obsidian': [],  # Se llenará con API Obsidian
            'dominios_exploracion_reciente': []
        }
    
    def _calcular_tiempo_disponible(self):
        # Basado en hora actual y no-negociables
        ahora = datetime.now()
        if ahora.hour < 12:
            return 8  # 8 horas disponibles en mañana
        elif ahora.hour < 18:
            return 4  # 4 horas en tarde
        else:
            return 2  # 2 horas en noche
    
    def _determinar_momento_dia(self, hora):
        if 5 <= hora < 12:
            return 'mañana'
        elif 12 <= hora < 18:
            return 'tarde'
        else:
            return 'noche'
    
    def _determinar_estacion(self, mes):
        if mes in [12, 1, 2]:
            return 'invierno'
        elif mes in [3, 4, 5]:
            return 'primavera'
        elif mes in [6, 7, 8]:
            return 'verano'
        else:
            return 'otoño'

# Singleton
servicio_contexto = ServicioContexto()
```

---

### PASO 4: API Endpoints (30 min)

**Archivo: `backend/api/estado_cero.py`**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from models.database import get_db, EstadoCero
from services.contexto import servicio_contexto
from services.claude_client import claude_client
from agentes.estado_cero import agente_estado_cero

router = APIRouter(prefix="/estado-cero", tags=["estado-cero"])

class IniciarEstadoCeroRequest(BaseModel):
    momento: str  # fajr, dhuhr, asr, maghrib, isha

class ResponderPreguntaRequest(BaseModel):
    pregunta_id: str
    sensacion: str  # expansion, contraccion
    intensidad: int  # 1-5
    nota: str = ""

class ChatRequest(BaseModel):
    mensaje: str

class FinalizarRequest(BaseModel):
    accion: dict

@router.post("/iniciar")
async def iniciar_estado_cero(
    request: IniciarEstadoCeroRequest,
    db: Session = Depends(get_db)
):
    """
    1. Recopila contexto
    2. Genera preguntas con Agente Estado Cero
    3. Crea registro en DB
    4. Retorna preguntas para que usuario responda
    """
    # Recopilar contexto
    contexto = servicio_contexto.recopilar_contexto_completo()
    
    # Generar preguntas con agente
    preguntas = agente_estado_cero.generar_preguntas(contexto)
    
    # Crear registro en DB
    estado = EstadoCero(
        momento=request.momento,
        contexto=contexto,
        respuestas=[],
        completado=False
    )
    db.add(estado)
    db.commit()
    db.refresh(estado)
    
    return {
        "id": estado.id,
        "momento": estado.momento,
        "contexto": contexto,
        "preguntas": preguntas
    }

@router.post("/{estado_id}/responder")
async def responder_pregunta(
    estado_id: int,
    request: ResponderPreguntaRequest,
    db: Session = Depends(get_db)
):
    """
    Guarda respuesta sacral del usuario
    """
    estado = db.query(EstadoCero).filter(EstadoCero.id == estado_id).first()
    if not estado:
        raise HTTPException(404, "Estado Cero no encontrado")
    
    # Agregar respuesta al array
    respuestas = estado.respuestas or []
    respuestas.append({
        "pregunta_id": request.pregunta_id,
        "sensacion": request.sensacion,
        "intensidad": request.intensidad,
        "nota": request.nota,
        "timestamp": datetime.utcnow().isoformat()
    })
    estado.respuestas = respuestas
    db.commit()
    
    return {"respuestas_completadas": len(respuestas), "total": 6}

@router.post("/{estado_id}/sintetizar")
async def sintetizar_direccion(
    estado_id: int,
    db: Session = Depends(get_db)
):
    """
    Cuando usuario completó las 6 preguntas, sintetiza dirección con Claude
    """
    estado = db.query(EstadoCero).filter(EstadoCero.id == estado_id).first()
    if not estado:
        raise HTTPException(404, "Estado Cero no encontrado")
    
    if len(estado.respuestas) < 6:
        raise HTTPException(400, "Faltan respuestas por completar")
    
    # Sintetizar con Claude
    direccion = claude_client.sintetizar_direccion(estado.respuestas)
    estado.direccion_emergente = direccion
    db.commit()
    
    return {"direccion": direccion}

@router.post("/{estado_id}/chat")
async def chat_clarificador(
    estado_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Chat iterativo para clarificar acción específica
    """
    estado = db.query(EstadoCero).filter(EstadoCero.id == estado_id).first()
    if not estado:
        raise HTTPException(404, "Estado Cero no encontrado")
    
    # Chat con Claude
    historial = estado.chat_clarificacion or []
    respuesta = claude_client.chat_clarificador(
        direccion=estado.direccion_emergente,
        respuestas=estado.respuestas,
        historial_chat=historial,
        mensaje_usuario=request.mensaje
    )
    
    # Guardar en historial
    historial.append({"role": "user", "content": request.mensaje})
    historial.append({"role": "assistant", "content": respuesta})
    estado.chat_clarificacion = historial
    db.commit()
    
    return {"respuesta": respuesta}

@router.post("/{estado_id}/finalizar")
async def finalizar_estado_cero(
    estado_id: int,
    request: FinalizarRequest,
    db: Session = Depends(get_db)
):
    """
    Usuario define acción concreta final
    Marca Estado Cero como completado
    Dispara Orquestador para plan de jornada
    """
    estado = db.query(EstadoCero).filter(EstadoCero.id == estado_id).first()
    if not estado:
        raise HTTPException(404, "Estado Cero no encontrado")
    
    estado.accion_tangible = request.accion
    estado.completado = True
    db.commit()
    
    # TODO: Disparar Orquestador para generar plan
    # plan = orquestador.generar_plan_jornada(estado.accion_tangible, estado.contexto)
    
    return {"success": True, "mensaje": "Estado Cero completado"}
```

---

### PASO 5: Frontend API Client (15 min)

**Archivo: `frontend/src/lib/api/client.ts`**

```typescript
const API_BASE = 'http://localhost:8000/api';

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

export const estadoCeroApi = {
  iniciar: (momento: string) =>
    request('/estado-cero/iniciar', {
      method: 'POST',
      body: JSON.stringify({ momento }),
    }),

  responderPregunta: (estadoId: number, respuesta: any) =>
    request(`/estado-cero/${estadoId}/responder`, {
      method: 'POST',
      body: JSON.stringify(respuesta),
    }),

  sintetizar: (estadoId: number) =>
    request(`/estado-cero/${estadoId}/sintetizar`, {
      method: 'POST',
    }),

  chat: (estadoId: number, mensaje: string) =>
    request(`/estado-cero/${estadoId}/chat`, {
      method: 'POST',
      body: JSON.stringify({ mensaje }),
    }),

  finalizar: (estadoId: number, accion: any) =>
    request(`/estado-cero/${estadoId}/finalizar`, {
      method: 'POST',
      body: JSON.stringify({ accion }),
    }),
};
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### Semana 1: Flujo Básico Funcionando

```bash
DÍA 1-2: Backend Core
☐ Base de datos configurada y tablas creadas
☐ Cliente Claude funcionando con API key
☐ Servicio de contexto recopilando datos
☐ Endpoints básicos de Estado Cero respondiendo

DÍA 3-4: Conexión Frontend-Backend
☐ API client configurado en frontend
☐ Componente Estado Cero llamando a endpoints
☐ Flujo completo: iniciar → responder → sintetizar → finalizar
☐ Datos guardándose correctamente en DB

DÍA 5-7: Refinamiento
☐ Agente Estado Cero generando preguntas coherentes
☐ Claude sintetizando direcciones con calidad
☐ Chat clarificador funcionando iterativamente
☐ UI mostrando feedback claro en cada paso
```

### Semana 2: Orquestación y Documentación

```bash
DÍA 8-10: Orquestador
☐ Agente Orquestador recibiendo acción de Estado Cero
☐ Generando plan de jornada con bloques flexibles
☐ Espejo Diario mostrando plan correctamente

DÍA 11-12: Guardian y Documentador
☐ Guardian monitoreando métricas básicas
☐ Documentador escribiendo en Obsidian
☐ Reporte diario generándose automáticamente

DÍA 13-14: Integraciones
☐ Anytype conectado para captura de insights
☐ Obsidian recibiendo documentos
☐ Sistema completo funcionando de punta a punta
```

---

## 🎯 PRÓXIMOS PASOS INMEDIATOS

### Para el Desarrollador - Empezar AHORA:

1. **Crear base de datos** (10 min)
   ```bash
   cd backend
   python -c "from models.database import init_db; init_db()"
   ```

2. **Probar Cliente Claude** (5 min)
   ```bash
   python -c "
   from services.claude_client import claude_client
   respuestas = [{'pregunta': 'Test', 'sensacion': 'expansion', 'intensidad': 4}]
   print(claude_client.sintetizar_direccion(respuestas))
   "
   ```

3. **Levantar backend** (2 min)
   ```bash
   cd backend
   python api/main.py
   # Visitar http://localhost:8000/docs
   ```

4. **Probar endpoint desde frontend** (5 min)
   ```bash
   # En frontend
   curl -X POST http://localhost:8000/api/estado-cero/iniciar \
     -H "Content-Type: application/json" \
     -d '{"momento": "fajr"}'
   ```

5. **Primera iteración completa** (30 min)
   - Abrir frontend en navegador
   - Click "Iniciar Estado Cero"
   - Responder 6 preguntas
   - Ver dirección sintetizada
   - Confirmar se guardó en DB

---

## 📝 NOTAS CRÍTICAS

### Lo que DEBE funcionar primero:

1. **Base de datos guardando datos** → Sin esto, nada persiste
2. **Cliente Claude respondiendo** → Sin esto, no hay inteligencia
3. **API endpoints conectados** → Sin esto, frontend es inútil
4. **Un flujo completo end-to-end** → Antes de agregar features

### Lo que puede esperar:

- Integraciones con Anytype/Obsidian
- Guardian detectando patrones avanzados
- WebSockets para notificaciones
- UI perfecta y pulida
- Calendario Hijri completo

---

**Enfoque: UN flujo funcionando completamente antes de agregar más complejidad.**
