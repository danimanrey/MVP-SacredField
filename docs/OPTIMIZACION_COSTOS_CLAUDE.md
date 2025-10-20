# 💰 Optimización de Costos - Claude API

## 🚨 **Problema Identificado**

**Costo actual**: 5 céntimos por consulta  
**5 Estados Cero/día**: 0.25€/día = **7.5€/mes**  
**Esto es 15x más caro que necesario**

---

## 📊 **Análisis de Costos**

### **Claude Sonnet 3.5 Pricing**:
- Input: $3 / millón tokens
- Output: $15 / millón tokens

### **Uso Actual por Estado Cero**:
```
Prompt (input):  ~800 tokens  →  $0.0024  (0.24¢)
Respuesta (output): ~300 tokens  →  $0.0045  (0.45¢)
Síntesis (input):  ~500 tokens  →  $0.0015  (0.15¢)
Síntesis (output): ~200 tokens  →  $0.0030  (0.30¢)
────────────────────────────────────────────────────────
TOTAL por Estado Cero: ~$0.0114  (1.14¢)
```

**¿Por qué estás pagando 5¢?**
- Prompt demasiado largo (800 tokens)
- Contexto repetitivo innecesario
- Chat clarificador usa tokens adicionales
- No hay caché de prompts

---

## ✅ **Optimizaciones Inmediatas**

### **1. Reducir Prompt de 800 → 200 tokens** ⏱️ 30 min

**Antes** (800 tokens):
```python
prompt = f"""Eres el Agente Estado Cero del Campo Sagrado.
Es momento {contexto.temporal.momento_liturgico.value}.

CONTEXTO COMPLETO:
- Temporal: {contexto.temporal.dia_semana} - {contexto.temporal.cualidad_momento}
- Mes: {contexto.temporal.mes_hijri} - {contexto.temporal.cualidad_mes}
- Biológico: Energía {contexto.biologico.energia_actual}/5...
- Financiero: Runway {contexto.financiero.runway_meses} meses...
- Conocimiento: {contexto.conocimiento.capturas_sin_procesar} capturas...

IMPORTANTE - Ajustes según momento litúrgico:
- Si es ISHA (noche): NO preguntes sobre comida...
- Si es FAJR (madrugada): Enfoca en inicio...
[... 15 líneas más ...]

Tu función: Formular 3 preguntas BINARIAS ESENCIALES que:
1. Ayuden a consultar la autoridad sacral...
2. Cubran las 4 dimensiones...
[... 20 líneas más ...]
"""
```

**Después** (200 tokens):
```python
prompt = f"""Estado Cero - {momento.value}

Contexto: {dia_semana}, E:{energia}/5, R:{runway}m
{contexto_personal_resumido}

3 preguntas binarias (expansión/contracción corporal):
1. DIRECCIÓN: ¿qué hacer?
2. BIOLOGÍA: ¿cómo está cuerpo?
3. TIMING: ¿es ahora?

JSON: [{{"id": "p1", "pregunta": "...", "categoria": "..."}}]
"""
```

**Ahorro**: 75% menos tokens = **-75% costo**

---

### **2. Caché de System Prompts** ⏱️ 15 min

```python
# Claude permite cachear el system prompt
# No se cobra por tokens cacheados

SYSTEM_PROMPT = """Eres Estado Cero del Campo Sagrado.
Generas 3 preguntas binarias que evocan sensación corporal.
Formato: JSON con id, pregunta, categoria."""

# Este prompt se cachea, solo pagas 1 vez
# Luego es gratis durante 5 minutos
```

**Ahorro**: 50-80% en system prompts

---

### **3. Usar Haiku para Preguntas Simples** ⏱️ 20 min

```python
# Claude Haiku: $0.25/M input, $1.25/M output
# 12x más barato que Sonnet

# Para generar preguntas (tarea simple):
USAR: Haiku  →  $0.0003 por consulta

# Para síntesis compleja (crucial):
USAR: Sonnet →  $0.005 por consulta
```

**Ahorro**: 90% en generación de preguntas

---

### **4. Reducir Llamadas a Claude** ⏱️ 30 min

**Actual**:
```
Estado Cero:
1. Generar 3 preguntas     → Claude call
2. Sintetizar dirección    → Claude call
3. Chat clarificador (opcional) → Claude calls

= 2-5 llamadas por Estado Cero
```

**Optimizado**:
```
Estado Cero:
1. Generar preguntas + síntesis en UNA llamada → 1 Claude call

= 1 llamada por Estado Cero
```

**Ahorro**: 50-75% menos llamadas

---

## 🎯 **Plan de Optimización**

### **Inmediato** (Hoy - 2 horas)

1. ✅ **Reducir prompt a 200 tokens**
   - Eliminar contexto verboso
   - Solo info esencial
   - **Ahorro: 75%**

2. ✅ **Usar Haiku para preguntas**
   - Cambiar modelo para generar preguntas
   - Sonnet solo para síntesis
   - **Ahorro: 90%**

3. ✅ **Combinar llamadas**
   - Una llamada en vez de dos
   - **Ahorro: 50%**

**Resultado**: De 5¢ → **0.3¢ por consulta** (94% ahorro)

### **v0.1.2** (Próxima semana)

4. ✅ **Caché de system prompts**
   - Implementar prompt caching
   - **Ahorro adicional: 50%**

5. ✅ **Preguntas template**
   - Banco de preguntas pre-generadas
   - Claude solo para personalizar
   - **Ahorro adicional: 80%**

**Resultado**: De 0.3¢ → **0.05¢ por consulta** (99% ahorro total)

---

## 📐 **Implementación Optimizada**

### **Prompt Minimalista**:

```python
# backend/agentes/estado_cero_optimizado.py

async def formular_preguntas_optimizadas(self, contexto):
    """Prompt ultra-compacto"""
    
    # Contexto mínimo
    ctx = f"{contexto.temporal.momento_liturgico.value}, E:{contexto.biologico.energia_actual}/5"
    
    # Prompt compacto (150 tokens)
    prompt = f"""{ctx}

3 preguntas binarias (expansión/contracción corporal):
1. Dirección: ¿qué hacer?
2. Biología: ¿cómo cuerpo?
3. Timing: ¿ahora?

JSON: [{{"id":"p1","pregunta":"...","cat":"..."}}]"""
    
    # Usar Haiku (12x más barato)
    resultado = await self.claude.generate_json_haiku(prompt)
    return resultado
```

### **Caché del System**:

```python
# Claude cachea automáticamente con header especial
self.client.messages.create(
    model="claude-3-5-sonnet-20241022",
    system=[{
        "type": "text",
        "text": SYSTEM_PROMPT_CACHED,  # Se cachea
        "cache_control": {"type": "ephemeral"}
    }],
    messages=messages
)
```

---

## 🎨 **Problema 2: UX/UI del Espejo Diario**

Entiendo perfectamente tu visión:

```
Estado Cero (Dhuhr) →  Dirección emergente
         ↓
   [Botón: "Ver Espejo Diario"]
         ↓
Espejo Diario Actualizado
   • Integra dirección de Dhuhr
   • Actualiza bloques del día
   • Muestra no-negociables
   • Refinamiento incremental
   • Est ética simbólica
```

### **Flujo Ideal**:

```
MAGHRIB (noche anterior)
   ↓
Ritual Maghrib: Intención mañana
   ↓
ESPEJO DIARIO BASE creado
   • No-negociables como anclas
   • Bloques sugeridos inicial
   • 40% espacio libre
   ↓
FAJR (06:59)
   ↓
Estado Cero → Dirección emergente
   ↓
ESPEJO SE ACTUALIZA
   • Integra dirección Fajr
   • Ajusta bloques
   • Mantiene no-negociables
   ↓
DHUHR (14:02)
   ↓
Estado Cero → Refinamiento
   ↓
ESPEJO SE ACTUALIZA
   • Integra feedback de mañana
   • Ajusta bloques de tarde
   • Refina prioridades
   ↓
[Continúa actualizándose con cada Estado Cero]
```

---

## 🚀 **Próximos Pasos Priorizados**

### **1. Optimizar Costos** 🔴 URGENTE (2h)
- Reducir prompts 75%
- Usar Haiku para preguntas
- Combinar llamadas

### **2. Flujo Estado Cero → Espejo** 🔴 CRÍTICO (3h)
- Botón "Ver Espejo Diario" después del chat
- Actualización incremental del Espejo
- Navegación fluida

### **3. Refinar Espejo Diario** 🟡 IMPORTANTE (4h)
- Estética simbólica mejorada
- Visualizar no-negociables como anclas
- Mostrar actualizaciones de cada Estado Cero

---

## 💎 **Buenas Prácticas**

**Estás siendo crítico correctamente**:
- ✅ Identificaste problema de costos
- ✅ Notaste flujo UX incompleto
- ✅ Visión clara del Espejo como centro

**Respuesta**:
- ⚠️ Prompts actuales NO son óptimos (demasiado largos)
- ✅ Arquitectura permite optimizar fácilmente
- ✅ Podemos reducir costos 94% en 2 horas

---

🕌 **¿Empezamos con la optimización de costos ahora o prefieres primero el flujo UX?**
