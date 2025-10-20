# 🕌 Arquitectura de Agentes - Campo Sagrado

**Pregunta**: ¿Cómo estamos realizando la arquitectura de los agentes? ¿Utilizamos LangGraph?

**Respuesta**: **NO usamos LangGraph**. Y esto es **intencional y correcto** para este proyecto.

---

## 📊 **Arquitectura Actual**

### **Patrón: Especialización Simple + Composición**

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO (Frontend)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  CAPA API (FastAPI)                         │
│  • /api/estado-cero/iniciar                                 │
│  • /api/orquestador/generar-plan                            │
│  • /api/guardian/reporte-diario                             │
│  • /api/maghrib/preparar-dia-siguiente                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              AGENTES (Clases Python)                        │
│                                                              │
│  ┌──────────────────┐   ┌──────────────────┐              │
│  │ AgenteEstadoCero │   │AgenteOrquestador│              │
│  │  - iniciar()     │   │ - recibir()     │              │
│  │  - formular()    │   │ - generar_plan()│              │
│  │  - sintetizar()  │   │ - ajustar()     │              │
│  └────────┬─────────┘   └────────┬─────────┘              │
│           │                      │                          │
│  ┌────────┴─────────┐   ┌───────┴──────────┐             │
│  │  AgenteGuardian  │   │AgenteDocumentador│             │
│  │  - monitorear()  │   │ - documentar()   │             │
│  │  - reportar()    │   │ - archivar()     │             │
│  └──────────────────┘   └──────────────────┘             │
│                                                              │
│  ┌──────────────────────────────────────────┐             │
│  │      AgenteEntrelazador                   │             │
│  │      - cargar_perfil()                    │             │
│  │      - generar_dashboard()                │             │
│  │      - detectar_conflictos()              │             │
│  └──────────────────────────────────────────┘             │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              SERVICIOS COMPARTIDOS                          │
│  • ClaudeClient (Anthropic API)                             │
│  • RecopiladorContexto                                      │
│  • CalculadorTiemposLiturgicos                              │
│  • CalendarioHijri                                          │
└─────────────────────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                    INTEGRACIONES                            │
│  • ObsidianVault (filesystem)                               │
│  • GoogleCalendarClient (OAuth)                             │
│  • SQLite (persistencia)                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 **¿Por qué NO usamos LangGraph?**

### **1. Simplicidad vs Complejidad**

**LangGraph es para**:
```python
# Flujos complejos con muchas decisiones
graph = StateGraph()
graph.add_node("agent1", agent1_function)
graph.add_node("agent2", agent2_function)
graph.add_edge("agent1", "agent2")
graph.add_conditional_edges(
    "agent2",
    lambda x: "continue" if x > 0 else "end",
    {"continue": "agent3", "end": END}
)
```

**Nuestro flujo es lineal y simple**:
```python
# Estado Cero → Orquestador → Documentador
estado = await agente_estado_cero.iniciar_consulta(momento)
direccion = estado_cero.direccion_emergente

plan = await agente_orquestador.recibir_orientacion(direccion, contexto)

await agente_documentador.documentar(estado_cero, plan)
```

**Resultado**: Nuestro código es más fácil de leer, debuggear y mantener.

---

### **2. Control Total vs Framework Lock-in**

**Con LangGraph**:
- Dependes de la API de LangGraph
- Actualizaciones pueden romper tu código
- Más difícil customizar comportamiento
- Mayor curva de aprendizaje

**Nuestro enfoque**:
- Clases Python simples
- Control total sobre cada interacción
- Fácil de modificar y extender
- Cero dependencias externas (excepto Claude)

---

### **3. Orquestación Explícita vs Implícita**

**Nuestro patrón actual**:

```python
# backend/agentes/estado_cero.py
class AgenteEstadoCero:
    def __init__(self, db: Session, claude: ClaudeClient, recopilador: RecopiladorContexto):
        self.db = db
        self.claude = claude
        self.recopilador = recopilador
    
    async def iniciar_consulta(self, momento: MomentoLiturgico):
        # 1. Recopilar contexto
        contexto = await self.recopilador.recopilar_contexto_completo(momento)
        
        # 2. Formular preguntas
        preguntas = await self.formular_preguntas(contexto)
        
        # 3. Retornar para que usuario responda
        return EstadoCeroCompleto(
            id=str(uuid.uuid4()),
            momento=momento,
            preguntas=preguntas,
            contexto=contexto
        )
```

**¿Qué pasa aquí?**
- ✅ Es obvio qué hace cada línea
- ✅ Puedes debuggear con `print()` o breakpoints
- ✅ No hay "magia" de framework
- ✅ Fácil de modificar

---

### **4. Flujo Natural del Dominio**

**Tu dominio tiene un flujo natural**:

```
06:00 FAJR
  ↓
Estado Cero (3 preguntas)
  ↓
Respuestas del usuario
  ↓
Síntesis con Claude
  ↓
Dirección emergente
  ↓
(Opcional) Orquestador genera plan
  ↓
Documentador archiva en Obsidian
```

Este flujo es **secuencial y determinista**. No necesitas:
- Grafos complejos
- Decisiones condicionales múltiples
- Backtracking
- Loops entre agentes

**LangGraph es overkill** para esto.

---

## 📐 **Arquitectura Actual: Composición Simple**

### **Cada Agente es Independiente**

```python
# backend/agentes/estado_cero.py
class AgenteEstadoCero:
    """
    Responsabilidad: Facilitar consulta sacral
    Input: MomentoLiturgico
    Output: EstadoCeroCompleto con preguntas
    """
    pass

# backend/agentes/orquestador.py
class AgenteOrquestador:
    """
    Responsabilidad: Generar plan emergente
    Input: AccionConcreta + ContextoCompleto
    Output: JornadaAlBordeCaos
    """
    pass

# backend/agentes/guardian.py
class AgenteGuardian:
    """
    Responsabilidad: Monitorear y reportar
    Input: Fecha
    Output: ReporteDiario
    """
    pass

# backend/agentes/documentador.py
class AgenteDocumentador:
    """
    Responsabilidad: Archivar en Obsidian
    Input: EstadoCeroCompleto, JornadaAlBordeCaos
    Output: void (archivos en filesystem)
    """
    pass

# backend/agentes/entrelazador.py
class AgenteEntrelazador:
    """
    Responsabilidad: Dashboard personal integrado
    Input: PerfilPersonal
    Output: DashboardEntrelazamiento
    """
    pass
```

### **Coordinación en la Capa API**

```python
# backend/api/estado_cero.py
@router.post("/iniciar")
async def iniciar_estado_cero(db: Session = Depends(get_db)):
    # 1. Crear agente
    agente = AgenteEstadoCero(db, claude_client, recopilador)
    
    # 2. Iniciar consulta
    estado_cero = await agente.iniciar_consulta(momento_actual)
    
    # 3. Retornar al frontend
    return estado_cero

@router.post("/completar")
async def completar_estado_cero(
    respuestas: List[RespuestaSacral],
    db: Session = Depends(get_db)
):
    # 1. Sintetizar con Claude
    direccion = await agente.sintetizar_direccion(respuestas)
    
    # 2. (Opcional) Pasar al Orquestador
    if usuario_quiere_plan:
        orquestador = AgenteOrquestador(db, claude_client, calculador)
        plan = await orquestador.recibir_orientacion(direccion, contexto)
    
    # 3. Documentar
    documentador = AgenteDocumentador(obsidian_vault)
    await documentador.documentar_estado_cero(estado_cero, direccion)
    
    return {"direccion": direccion, "plan": plan}
```

**Ventajas**:
- ✅ Cada endpoint coordina su propio flujo
- ✅ No hay "estado global" compartido
- ✅ Cada request es independiente
- ✅ Fácil de testear

---

## 🔄 **Comunicación Entre Agentes**

### **Patrón Actual: Paso de Mensajes Explícito**

```python
# Estado Cero genera dirección
direccion = await agente_estado_cero.sintetizar_direccion(respuestas)
# → AccionConcreta

# Orquestador recibe dirección
plan = await agente_orquestador.recibir_orientacion(direccion, contexto)
# → JornadaAlBordeCaos

# Documentador archiva todo
await agente_documentador.documentar(estado_cero, direccion, plan)
# → Archivos en Obsidian
```

**No hay**:
- ❌ Estado compartido entre agentes
- ❌ Message broker (RabbitMQ, Redis)
- ❌ Event bus
- ❌ Grafos de ejecución

**Solo hay**:
- ✅ Llamadas de función asíncronas
- ✅ Objetos Pydantic bien tipados
- ✅ Flujo de datos explícito

---

## 🎨 **Cuando SÍ Usarías LangGraph**

### **Casos de Uso Ideales para LangGraph**:

1. **Flujos complejos con múltiples caminos**
```python
# Ejemplo: Agente que decide qué hacer basándose en contexto
if user_confused:
    → clarification_agent
elif user_needs_data:
    → data_retrieval_agent
elif user_wants_action:
    → action_agent
```

2. **Loops entre agentes**
```python
# Ejemplo: Refinamiento iterativo
researcher → critic → researcher → critic → final_output
```

3. **Backtracking**
```python
# Ejemplo: Si falla, reintentar con diferente estrategia
agent_1 → agent_2 → (falla) → volver a agent_1 con diferente enfoque
```

4. **Múltiples agentes en paralelo**
```python
# Ejemplo: Consultar varios expertos simultáneamente
query → [finance_expert, tech_expert, legal_expert] → synthesizer
```

### **Tu Caso (Campo Sagrado)**:

- ✅ Flujo lineal y secuencial
- ✅ No hay decisiones complejas
- ✅ No hay loops necesarios
- ✅ No hay paralelismo entre agentes

**Conclusión**: LangGraph sería **over-engineering**

---

## 🚀 **¿Cuándo Migraríamos a LangGraph?**

Si en v0.3.0+ necesitas:

### **Escenario 1: Guardian Proactivo**
```python
# Guardian detecta algo → Activa Orquestador → Notifica usuario
graph.add_node("guardian_monitor", monitor_function)
graph.add_conditional_edges(
    "guardian_monitor",
    decide_if_intervention_needed,
    {
        "needs_intervention": "orquestador",
        "all_good": END
    }
)
```

### **Escenario 2: Chat Multi-Agente**
```python
# Usuario hace pregunta compleja
# → Decide qué agente(s) pueden responder
# → Consulta múltiples agentes
# → Sintetiza respuesta
graph.add_node("router", route_query)
graph.add_conditional_edges(
    "router",
    lambda x: x["query_type"],
    {
        "state_zero": "estado_cero_agent",
        "plan_adjustment": "orquestador_agent",
        "report": "guardian_agent"
    }
)
```

### **Escenario 3: Sistema de Feedback Continuo**
```python
# Plan → Usuario ejecuta → Guardian observa → Ajusta plan → Repite
graph.add_node("execute", execute_plan)
graph.add_node("observe", guardian_observe)
graph.add_node("adjust", orquestador_adjust)
graph.add_edge("execute", "observe")
graph.add_conditional_edges(
    "observe",
    lambda x: "adjust" if needs_adjustment(x) else END,
    {"adjust": "adjust", END: END}
)
graph.add_edge("adjust", "execute")  # Loop
```

**Por ahora**: Ninguno de estos escenarios es necesario en el MVP.

---

## 📚 **Comparación Técnica**

### **Con LangGraph**

```python
# Dependencias adicionales
pip install langgraph langchain

# Código más verboso
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    messages: List[str]
    next: str
    
graph = StateGraph(AgentState)

def estado_cero_node(state):
    # ... lógica
    return {"messages": [...], "next": "orquestador"}

graph.add_node("estado_cero", estado_cero_node)
graph.add_node("orquestador", orquestador_node)
graph.set_entry_point("estado_cero")
graph.add_conditional_edges(...)

app = graph.compile()
result = app.invoke({"messages": []})
```

### **Actual (Sin LangGraph)**

```python
# Sin dependencias adicionales
# Solo: anthropic, fastapi, pydantic

# Código directo
async def flujo_estado_cero(momento: MomentoLiturgico):
    # 1. Estado Cero
    estado = await agente_estado_cero.iniciar_consulta(momento)
    
    # 2. Usuario responde (en frontend)
    # ...
    
    # 3. Sintetizar
    direccion = await agente_estado_cero.sintetizar_direccion(respuestas)
    
    # 4. Orquestador (opcional)
    if generar_plan:
        plan = await agente_orquestador.recibir_orientacion(direccion, contexto)
    
    # 5. Documentar
    await agente_documentador.documentar(estado, direccion, plan)
    
    return {"direccion": direccion, "plan": plan}
```

**Diferencia**:
- LangGraph: 50+ líneas, más abstracción
- Actual: 15 líneas, más directo

---

## ✅ **Ventajas de la Arquitectura Actual**

### **1. Transparencia Total**
```python
# Puedes ver exactamente qué hace cada agente
print(f"Estado Cero: {estado_cero}")
print(f"Dirección: {direccion}")
print(f"Plan: {plan}")
```

### **2. Zero Lock-in**
- No dependes de LangGraph/LangChain
- Puedes migrar a cualquier framework fácilmente
- O continuar sin framework

### **3. Debugging Simple**
```python
# Puedes poner breakpoints en cualquier lugar
async def iniciar_consulta(self, momento):
    contexto = await self.recopilador.recopilar_contexto_completo(momento)
    # 👆 Breakpoint aquí para inspeccionar contexto
    
    preguntas = await self.formular_preguntas(contexto)
    # 👆 O aquí para ver preguntas generadas
    
    return EstadoCeroCompleto(...)
```

### **4. Testable**
```python
# Tests unitarios simples
async def test_estado_cero():
    agente = AgenteEstadoCero(mock_db, mock_claude, mock_recopilador)
    
    resultado = await agente.iniciar_consulta(MomentoLiturgico.FAJR)
    
    assert len(resultado.preguntas) == 3
    assert resultado.momento == MomentoLiturgico.FAJR
```

### **5. Performance**
- Sin overhead de framework
- Llamadas directas asíncronas
- Mínima latencia

---

## 🎯 **Decisión Arquitectónica**

### **Para Campo Sagrado MVP:**

✅ **CORRECTO**: Clases Python simples + Composición  
❌ **INCORRECTO**: LangGraph (over-engineering)

### **Razones**:

1. **Flujo lineal y simple** → No necesitas grafos
2. **Control total** → Mejor experiencia de desarrollo
3. **Fácil de entender** → Mejor para iterar rápido
4. **Sin dependencias** → Menos superficie de ataque
5. **Más rápido** → Menos overhead

### **Migración Futura**:

Si en v0.3.0+ necesitas:
- Flujos complejos con decisiones
- Loops entre agentes
- Múltiples agentes en paralelo

**Entonces** considera LangGraph.

**Pero no antes.**

---

## 📖 **Documentación de Referencia**

### **Nuestros Agentes**:
- `backend/agentes/estado_cero.py` - Consulta sacral
- `backend/agentes/orquestador.py` - Plan emergente
- `backend/agentes/guardian.py` - Monitoreo
- `backend/agentes/documentador.py` - Archivo en Obsidian
- `backend/agentes/entrelazador.py` - Dashboard personal

### **Coordinación**:
- `backend/api/estado_cero.py` - Endpoints Estado Cero
- `backend/api/orquestador.py` - Endpoints Orquestador
- `backend/api/ritual_maghrib.py` - Ritual completo

### **Servicios Compartidos**:
- `backend/services/claude_client.py` - Cliente Anthropic
- `backend/services/contexto.py` - Recopilación de contexto
- `backend/services/tiempos_liturgicos.py` - Cálculo de momentos

---

## 🔮 **Respuesta Directa a tu Pregunta**

### **¿Cómo estamos realizando la arquitectura de los agentes?**

**Respuesta**: 
- Clases Python simples e independientes
- Cada agente tiene una responsabilidad clara
- Comunicación por paso de mensajes explícito
- Coordinación en la capa API (FastAPI)
- Sin framework de orquestación

### **¿Utilizamos LangGraph?**

**Respuesta**: **NO**

**¿Por qué?**
1. Nuestro flujo es lineal y simple
2. LangGraph sería over-engineering
3. Más control y transparencia sin framework
4. Mejor experiencia de desarrollo
5. Más fácil de mantener y debuggear

### **¿Cuándo lo usaríamos?**

**Respuesta**: Solo si en v0.3.0+ necesitamos:
- Flujos complejos con múltiples decisiones
- Loops entre agentes
- Backtracking
- Múltiples agentes en paralelo

**Para el MVP**: La arquitectura actual es **perfecta**.

---

✨ **Simplicidad es sofisticación.** 🕌

