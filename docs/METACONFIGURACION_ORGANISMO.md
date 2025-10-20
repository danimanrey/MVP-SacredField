# 🧬 Meta-Configuración del Organismo

## 🎯 **Concepto Central**

**Problema**: Cada persona es única en CÓMO interactúa con el mundo.

**Solución**: El organismo debe adaptarse no solo a **QUÉ haces**, sino a **CÓMO prefieres hacerlo**.

```
No es solo:
❌ "Usuario aprende Rust"

Es:
✅ "Usuario aprende Rust de forma visual, en bloques de 25min, 
    por la mañana, con ejemplos prácticos, documentando en 
    diagramas en Obsidian"
```

---

## 📊 **Niveles de Configuración**

### **Nivel 1: Contenido** (v0.1.1 - Implementado)
```python
class PerfilPersonal:
    """QUÉ hace el usuario"""
    rutinas_deportivas: List[RutinaDeportiva]
    temas_aprendizaje: List[TemaAprendizaje]
    proyectos_desarrollo: List[ProyectoDesarrollo]
```

### **Nivel 2: Meta-Configuración** (v0.2.0 - Siguiente)
```python
class MetaPerfilCognitivo:
    """CÓMO prefiere interactuar el usuario"""
    
    # Estilo de aprendizaje
    estilo_aprendizaje: EstiloAprendizaje
    
    # Modo de documentación
    sistema_documentacion_preferido: SistemaDocumentacion
    
    # Personalidad y preferencias
    tipo_personalidad: TipoPersonalidad
    
    # Sistema operacional personal
    sistema_operacional: SistemaOperacional
    
    # Modo de interacción
    modo_interaccion: ModoInteraccion
```

---

## 🧠 **Dimensiones de Meta-Configuración**

### **1. Estilo de Aprendizaje**

```python
class EstiloAprendizaje(BaseModel):
    """CÓMO aprende mejor el usuario"""
    
    # Modalidad primaria
    modalidad_primaria: Literal[
        "visual",           # Diagramas, mapas mentales
        "auditivo",         # Podcasts, explicaciones verbales
        "kinestésico",      # Hacer, experimentar, proyectos
        "lectoescritura"    # Leer, escribir, documentar
    ]
    
    # Formato preferido
    formato_contenido: List[Literal[
        "video",
        "texto",
        "audio",
        "interactivo",
        "proyecto_practico"
    ]]
    
    # Duración óptima de sesión
    duracion_sesion_optima: int  # minutos (25, 50, 90)
    
    # Necesita descansos
    tecnica_preferida: Literal[
        "pomodoro",         # 25min + 5min descanso
        "flowtime",         # Hasta que pierdas enfoque
        "ultradian",        # 90min + 20min descanso
        "custom"
    ]
    
    # Profundidad vs Amplitud
    preferencia: Literal[
        "profundo",         # Un tema a la vez, muy profundo
        "amplio",           # Múltiples temas, conexiones
        "equilibrado"
    ]
    
    # Necesita estructura
    nivel_estructura: int  # 1-5
    # 1: Totalmente libre
    # 5: Muy estructurado con checkpoints
    
    # Mejor momento del día
    momento_optimo: List[Literal[
        "madrugada",        # 5-8am
        "mañana",           # 8-12pm
        "mediodia",         # 12-3pm
        "tarde",            # 3-7pm
        "noche"             # 7-11pm
    ]]
```

**Ejemplo de uso**:
```python
usuario_visual_pomodoro = EstiloAprendizaje(
    modalidad_primaria="visual",
    formato_contenido=["video", "interactivo"],
    duracion_sesion_optima=25,
    tecnica_preferida="pomodoro",
    preferencia="profundo",
    nivel_estructura=4,
    momento_optimo=["mañana"]
)

# El organismo adapta:
# - Sugiere videos en vez de libros
# - Bloques de 25 minutos
# - Por la mañana
# - Con checkpoints claros
```

---

### **2. Sistema de Documentación Preferido**

```python
class SistemaDocumentacion(BaseModel):
    """CÓMO documenta y organiza conocimiento"""
    
    # Herramienta principal
    herramienta_primaria: Literal[
        "obsidian",         # Markdown, enlaces bidireccionales
        "anytype",          # Base de datos relacional, grafos
        "notion",           # Bloques, bases de datos
        "roam",             # Red neuronal de notas
        "logseq",           # Outliner + grafos
        "papel"             # Físico (cuadernos)
    ]
    
    # Método de organización
    metodo_organizacion: Literal[
        "zettelkasten",     # Notas atómicas + enlaces
        "para",             # Proyectos/Áreas/Recursos/Archivo
        "folders",          # Carpetas jerárquicas tradicionales
        "tags",             # Solo etiquetas, sin carpetas
        "cronologico",      # Diario/journal
        "visual"            # Mapas mentales, canvas
    ]
    
    # Frecuencia de captura
    frecuencia_captura: Literal[
        "continua",         # Todo el día
        "sesiones",         # Al final de cada sesión
        "diaria",           # Una vez al día
        "semanal"           # Resumen semanal
    ]
    
    # Nivel de procesamiento
    nivel_procesamiento: Literal[
        "raw",              # Capturas sin procesar
        "basico",           # Limpiar y categorizar
        "elaborado",        # Conectar con conocimiento existente
        "publicable"        # Listo para compartir
    ]
    
    # Preferencia visual
    usa_visual: bool  # Diagramas, mapas, canvas
    usa_texto: bool   # Prosa, markdown
    usa_listas: bool  # Bullets, checkboxes
    usa_tablas: bool  # Estructuras tabulares
```

**Impacto en el organismo**:
```python
# Usuario Obsidian + Zettelkasten
usuario_a = SistemaDocumentacion(
    herramienta_primaria="obsidian",
    metodo_organizacion="zettelkasten",
    frecuencia_captura="continua",
    nivel_procesamiento="elaborado"
)

# → AgenteDocumentador crea:
#    - Notas atómicas
#    - Enlaces bidireccionales automáticos
#    - Tags basados en contexto
#    - Capturas en tiempo real

# Usuario Anytype + PARA
usuario_b = SistemaDocumentacion(
    herramienta_primaria="anytype",
    metodo_organizacion="para",
    frecuencia_captura="semanal",
    nivel_procesamiento="publicable"
)

# → AgenteDocumentador crea:
#    - Base de datos relacional
#    - Vistas por Proyecto/Área
#    - Resúmenes semanales pulidos
```

---

### **3. Tipo de Personalidad**

```python
class TipoPersonalidad(BaseModel):
    """Marco de personalidad para adaptar interacciones"""
    
    # Big Five (OCEAN)
    apertura: int           # 1-5: Curiosidad, creatividad
    consciencia: int        # 1-5: Organización, disciplina
    extroversion: int       # 1-5: Social vs solitario
    amabilidad: int         # 1-5: Cooperación vs competencia
    neuroticismo: int       # 1-5: Estabilidad emocional
    
    # Motivadores principales
    motivadores: List[Literal[
        "logro",            # Alcanzar metas
        "autonomia",        # Libertad, control
        "maestria",         # Dominar habilidades
        "proposito",        # Impacto, significado
        "conexion",         # Relaciones, comunidad
        "seguridad",        # Estabilidad, previsibilidad
        "novedad"           # Variedad, experimentación
    ]]
    
    # Respuesta al estrés
    bajo_estres: Literal[
        "accion",           # Hacer más
        "reflexion",        # Pensar, planear
        "social",           # Hablar con otros
        "soledad",          # Retirarse
        "estructura",       # Más orden
        "libertad"          # Menos reglas
    ]
    
    # Toma de decisiones
    toma_decisiones: Literal[
        "intuitiva",        # Rápida, gut feeling
        "analitica",        # Lenta, datos
        "colaborativa",     # Con otros
        "sacral"            # Autoridad corporal (Human Design)
    ]
```

**Cómo lo usa el organismo**:
```python
# Usuario con alta apertura, baja consciencia
usuario_creativo = TipoPersonalidad(
    apertura=5,
    consciencia=2,
    motivadores=["novedad", "autonomia", "maestria"],
    bajo_estres="libertad"
)

# → Orquestador adapta:
#    - Menos estructura rígida
#    - Más espacios emergentes (50% vs 40%)
#    - Sugiere exploración vs optimización
#    - Bajo estrés: quita tareas, no añade

# Usuario con alta consciencia, baja apertura
usuario_estructurado = TipoPersonalidad(
    apertura=2,
    consciencia=5,
    motivadores=["logro", "seguridad", "maestria"],
    bajo_estres="estructura"
)

# → Orquestador adapta:
#    - Más checkpoints y métricas
#    - Rutinas predecibles
#    - Optimización vs exploración
#    - Bajo estrés: añade estructura, clarifica pasos
```

---

### **4. Sistema Operacional Personal**

```python
class SistemaOperacional(BaseModel):
    """CÓMO opera el usuario en el día a día"""
    
    # Tipo de energía
    cronot tipo: Literal[
        "alondra",          # Madrugador, pico mañana
        "buho",             # Nocturno, pico noche
        "colibri",          # Bifásico, picos mañana y tarde
        "variable"          # Depende del día
    ]
    
    # Necesidades de recuperación
    recuperacion: dict = {
        "sueno_optimo": int,           # 7-9 horas
        "siesta": bool,                # ¿Necesita siesta?
        "duracion_siesta": int,        # 20-90 minutos
        "ejercicio_requerido": bool,   # ¿Necesita moverse para pensar?
        "naturaleza": bool             # ¿Necesita tiempo en naturaleza?
    }
    
    # Modo de trabajo preferido
    modo_trabajo: Literal[
        "monocrono",        # Una tarea a la vez
        "policrono",        # Múltiples tareas paralelas
        "hibrido"
    ]
    
    # Interrupibilidad
    tolerancia_interrupciones: int  # 1-5
    # 1: Necesita bloques profundos sin interrupciones
    # 5: Puede cambiar de contexto fácilmente
    
    # Necesidad de variedad
    necesidad_variedad: int  # 1-5
    # 1: Rutinas fijas, predecibles
    # 5: Cambio constante, impredecibilidad
    
    # Umbral de decisión
    umbral_decision: Literal[
        "bajo",             # Decide rápido, menos análisis
        "medio",
        "alto"              # Necesita mucha información antes de decidir
    ]
```

**Aplicación práctica**:
```python
# Usuario "alondra" monocrono
usuario = SistemaOperacional(
    cronotipo="alondra",
    recuperacion={
        "sueno_optimo": 7,
        "siesta": False,
        "ejercicio_requerido": True,
        "naturaleza": True
    },
    modo_trabajo="monocrono",
    tolerancia_interrupciones=1,
    necesidad_variedad=2
)

# → Sistema adapta:
#    - Estados Cero en Fajr (6am) son más profundos
#    - Bloques de trabajo sin interrupciones
#    - Ejercicio matutino obligatorio
#    - Rutinas predecibles
#    - No sugiere reuniones por la mañana
```

---

### **5. Modo de Interacción con el Sistema**

```python
class ModoInteraccion(BaseModel):
    """CÓMO prefiere interactuar con el organismo"""
    
    # Nivel de guía
    nivel_guia: Literal[
        "minimo",           # Solo preguntas, sin sugerencias
        "moderado",         # Algunas sugerencias
        "completo"          # Guía activa, muchas sugerencias
    ]
    
    # Tono de comunicación
    tono: Literal[
        "formal",           # Profesional, distante
        "amigable",         # Cercano pero profesional
        "personal",         # Como un amigo
        "minimalista"       # Lo mínimo necesario
    ]
    
    # Frecuencia de check-ins
    frecuencia_checkins: Literal[
        "continua",         # Cada hora
        "momentos_liturgicos", # 5 veces al día
        "inicio_fin",       # Mañana y noche
        "manual"            # Solo cuando usuario pide
    ]
    
    # Tipo de feedback preferido
    feedback: Literal[
        "directo",          # "No cumpliste X"
        "suave",            # "¿Qué pasó con X?"
        "reflexivo",        # "¿Qué aprendiste?"
        "sin_feedback"      # No recuerda incumplimientos
    ]
    
    # Gamificación
    gamificacion: bool
    # True: Puntos, rachas, logros
    # False: Sin gamificación
    
    # Compartir progreso
    compartir: Literal[
        "privado",          # Solo para el usuario
        "circulo_cercano",  # Pareja, familia
        "comunidad",        # Grupo más amplio
        "publico"           # Abierto
    ]
```

---

## 🏗️ **Arquitectura de Meta-Configuración**

### **Estructura de Archivos**

```
obsidian_vault/
├── 00-Meta/
│   ├── perfil-cognitivo.md          ← Meta-configuración
│   ├── estilo-aprendizaje.md
│   ├── sistema-operacional.md
│   └── evolucion-preferencias.md    ← Cómo cambian tus preferencias
│
├── 10-Configuracion/                ← Configuración de contenido
│   ├── rutinas.md
│   ├── proyectos.md
│   └── aprendizaje.md
│
├── 50-Conversaciones-IA/            ← Interacciones
│   └── Estados-Cero/
│
└── 90-Reflexion/                     ← Meta-aprendizaje
    └── como-aprendo-mejor.md         ← El organismo aprende CÓMO aprendes
```

### **Anytype: Base de Datos Relacional**

```
Set: PerfilCognitivo
├─ Type: EstiloAprendizaje
│  ├─ Relation: TemadeAprendizaje
│  └─ Properties:
│     ├─ modalidad_primaria: "visual"
│     ├─ duracion_optima: 25
│     └─ momento_optimo: ["mañana"]
│
├─ Type: SistemaDocumentacion
│  ├─ Relation: Estados Cero
│  └─ Properties:
│     ├─ herramienta: "obsidian"
│     ├─ metodo: "zettelkasten"
│     └─ frecuencia: "continua"
│
└─ Type: SistemaOperacional
   ├─ Relation: Jornadas
   └─ Properties:
      ├─ cronotipo: "alondra"
      ├─ modo_trabajo: "monocrono"
      └─ tolerancia_interrupciones: 1
```

---

## 🔄 **Flujo de Adaptación**

### **1. Captura Inicial** (v0.2.0)

```python
# Frontend: /configurar-meta-perfil
class FormularioMetaPerfil:
    """Wizard interactivo para descubrir preferencias"""
    
    def paso_1_estilo_aprendizaje(self):
        """
        Preguntas:
        - ¿Prefieres ver un video o leer un artículo?
        - ¿Estudias mejor en bloques cortos o largos?
        - ¿Prefieres terminar un libro o leer varios a la vez?
        """
    
    def paso_2_documentacion(self):
        """
        - ¿Ya usas alguna herramienta? (Obsidian/Notion/etc)
        - ¿Cómo organizas tus notas ahora?
        - ¿Capturas ideas todo el día o al final?
        """
    
    def paso_3_personalidad(self):
        """
        - ¿Prefieres libertad o estructura?
        - ¿Qué te motiva más?
        - ¿Cómo respondes al estrés?
        """
    
    def paso_4_sistema_operacional(self):
        """
        - ¿Eres más productivo de día o de noche?
        - ¿Puedes cambiar de tarea fácilmente?
        - ¿Necesitas ejercicio para pensar?
        """
    
    def paso_5_interaccion(self):
        """
        - ¿Cuánta guía quieres del sistema?
        - ¿Prefieres feedback directo o suave?
        - ¿Te gusta gamificación?
        """
```

### **2. Adaptación Automática**

```python
class AgenteAdaptativo:
    """Adapta comportamiento según meta-perfil"""
    
    def __init__(self, meta_perfil: MetaPerfilCognitivo):
        self.meta_perfil = meta_perfil
    
    def adaptar_estado_cero(self, momento: MomentoLiturgico):
        """
        Si usuario es visual:
        - Preguntas con imágenes mentales
        - "¿Ves tu día fluyendo hacia X?"
        
        Si usuario es kinestésico:
        - Preguntas sobre sensación corporal
        - "¿Sientes en tu cuerpo...?"
        """
    
    def adaptar_orquestador(self, energia: int):
        """
        Si tolerancia_interrupciones = 1:
        - Bloques largos sin fragmentar
        
        Si tolerancia_interrupciones = 5:
        - Bloques cortos, tareas mezcladas
        """
    
    def adaptar_documentador(self, contenido: str):
        """
        Si herramienta = "obsidian" + metodo = "zettelkasten":
        - Notas atómicas
        - Enlaces bidireccionales
        
        Si herramienta = "anytype" + metodo = "para":
        - Relaciones en base de datos
        - Vistas por proyecto/área
        """
```

### **3. Aprendizaje Continuo** (v0.3.0)

```python
class SistemaMetaAprendizaje:
    """El organismo aprende CÓMO aprendes"""
    
    def observar_patrones(self, historial_6_meses):
        """
        Detecta:
        - ¿A qué hora completas más tareas realmente?
        - ¿Qué formato de aprendizaje tiene más progreso?
        - ¿Cuándo ignoras las sugerencias del sistema?
        - ¿Cuándo estás más en flow?
        """
    
    def ajustar_meta_perfil(self):
        """
        "Creías ser alondra, pero los datos muestran 
         que eres más productivo por la tarde.
         
         ¿Quieres que ajuste tu perfil?"
        """
    
    def sugerir_experimentos(self):
        """
        "Has estado usando bloques de 25min (pomodoro).
         
         ¿Quieres probar bloques de 90min (ultradian)
         por una semana para comparar?"
        """
```

---

## 📊 **Impacto en Escalabilidad**

### **Por qué es crítico para escalar**:

#### **1. Personalización Real**
```
Sin meta-configuración:
❌ Todos los usuarios reciben mismas sugerencias
❌ "Estudia por la mañana" (aunque seas búho)
❌ "Lee este libro" (aunque aprendas visual)

Con meta-configuración:
✅ Usuario A (visual, pomodoro): Videos de 25min
✅ Usuario B (kinestésico, flowtime): Proyectos prácticos largos
✅ Usuario C (lector, ultradian): Libros en sesiones de 90min
```

#### **2. Reducción de Fricción**
```
El organismo se adapta a TI, no tú a él.

Ejemplo:
- Usuario prefiere Obsidian + Zettelkasten
→ Sistema crea notas atómicas automáticamente
→ No tiene que reorganizar nada
→ Flujo natural
```

#### **3. Datos para Mejora**
```
Con 1000 usuarios meta-configurados:

"Usuarios visuales con pomodoro tienen 
 35% más adherencia que auditivos con flowtime"

→ Mejores defaults para nuevos usuarios
→ Sugerencias basadas en datos reales
```

#### **4. Comunidad Segmentada**
```
Puedes conectar usuarios similares:

"Otros 12 usuarios con tu perfil (visual, alondra, 
 monocrono) han encontrado útil X técnica"

→ Aprendizaje colectivo segmentado
→ Mejores prácticas por tipo
```

---

## 🛠️ **Implementación Práctica**

### **v0.2.0 - Meta-Configuración Base**

**1. Modelo de Datos**:
```python
# backend/models/schemas.py
class MetaPerfilCognitivo(BaseModel):
    estilo_aprendizaje: EstiloAprendizaje
    sistema_documentacion: SistemaDocumentacion
    tipo_personalidad: TipoPersonalidad
    sistema_operacional: SistemaOperacional
    modo_interaccion: ModoInteraccion
    
    # Metadata
    creado: datetime
    ultima_revision: datetime
    version: int  # Para tracking de cambios
```

**2. Frontend**:
```svelte
<!-- frontend/src/routes/configurar-meta-perfil/+page.svelte -->

<script>
  let paso = 1;
  let metaPerfil = {
    estilo_aprendizaje: {},
    sistema_documentacion: {},
    // ...
  };
</script>

<WizardMetaConfiguracion {paso}>
  {#if paso === 1}
    <EstiloAprendizajeForm bind:data={metaPerfil.estilo_aprendizaje} />
  {:else if paso === 2}
    <SistemaDocumentacionForm bind:data={metaPerfil.sistema_documentacion} />
  <!-- ... -->
  {/if}
</WizardMetaConfiguracion>
```

**3. Documentación Automática**:
```python
# backend/agentes/documentador.py

def documentar_meta_perfil(self, meta_perfil: MetaPerfilCognitivo):
    """
    Crea archivo en Obsidian/Anytype según preferencia
    """
    
    if meta_perfil.sistema_documentacion.herramienta_primaria == "obsidian":
        self._crear_perfil_obsidian(meta_perfil)
    elif meta_perfil.sistema_documentacion.herramienta_primaria == "anytype":
        self._crear_perfil_anytype(meta_perfil)

def _crear_perfil_obsidian(self, meta_perfil):
    """
    obsidian_vault/00-Meta/perfil-cognitivo.md
    
    # Mi Perfil Cognitivo
    
    ## Estilo de Aprendizaje
    - Modalidad: Visual
    - Técnica: Pomodoro (25min)
    - Momento óptimo: Mañana
    
    ## Sistema de Documentación
    - Herramienta: Obsidian
    - Método: Zettelkasten
    - Frecuencia: Continua
    
    ...
    """
```

---

## 🎯 **Para tu MVP**

**Tienes razón**: No es necesario ahora, pero tenerlo en cuenta para:

### **v0.2.0 - Implementación Básica**
```python
# Solo lo esencial para empezar
class MetaPerfilSimple(BaseModel):
    # Aprendizaje
    modalidad_aprendizaje: str  # "visual", "kinestésico", etc
    duracion_sesion_optima: int
    
    # Documentación
    herramienta_preferida: str  # "obsidian", "anytype"
    metodo_organizacion: str
    
    # Sistema operacional
    cronotipo: str  # "alondra", "buho"
    modo_trabajo: str  # "monocrono", "policrono"
```

### **v0.3.0 - Expansión Completa**
```python
# Todo el framework de meta-configuración
class MetaPerfilCompleto(BaseModel):
    # Todas las dimensiones
    # + Aprendizaje automático
    # + Ajuste continuo
```

---

## 📚 **Documentación de Escalabilidad**

**Archivos creados**:
- `docs/METACONFIGURACION_ORGANISMO.md` - Este documento
- Define framework para personalización profunda
- Establece base para escalar a 1000+ usuarios
- Cada usuario con organismo único adaptado a SU forma

---

## ✨ **Resumen Ejecutivo**

```
Meta-configuración = Organismo se adapta a CÓMO eres

No solo:
❌ "¿QUÉ aprendes?" → Rust

Sino:
✅ "¿CÓMO aprendes Rust?" 
   → Visual, 25min, mañana, diagramas en Obsidian

Dimensiones:
1. Estilo de aprendizaje (visual, auditivo, etc)
2. Sistema de documentación (Obsidian, Anytype, etc)
3. Tipo de personalidad (motivadores, estrés)
4. Sistema operacional (cronotipo, mono/policrono)
5. Modo de interacción (guía, tono, frecuencia)

Para MVP:
⏸️  No implementar aún

Para v0.2.0:
✅ Versión simple de meta-configuración

Para escalar:
✅ Framework completo
✅ Organismo único por usuario
✅ Comunidad segmentada por perfiles
```

🕌 ¿Esto es lo que buscabas para los próximos pasos de escalabilidad?
