"""
Gestor de estructura fractal modular para Obsidian
Respeta principios herméticos: "Como es arriba, es abajo"
"""

from pathlib import Path
from datetime import date, datetime
from typing import Dict, Optional
import os


class ObsidianStructureManager:
    """
    Gestor de estructura fractal modular para Obsidian
    Opera al borde del caos: 40% espacio sin asignar
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.dominios = {
            "biologia": "10_Biologia_Ritmos",
            "mente": "20_Mente_Aprendizaje", 
            "alma": "30_Alma_Proposito",
            "tecnologia": "40_Tecnologia",
            "economia": "50_Proyecto_Economia"
        }
    
    def initialize_vault_structure(self):
        """Crea estructura fractal completa si no existe"""
        print("🏗️  Creando estructura fractal en Obsidian...")
        
        folders = [
            # 00_System - Núcleo Operativo
            "00_System/Audit_Trail",
            
            # 10_Biologia_Ritmos - Cuerpo y Energía
            "10_Biologia_Ritmos/Estados_Cero",
            "10_Biologia_Ritmos/Patrones",
            "10_Biologia_Ritmos/HRV_Data",
            
            # 20_Mente_Aprendizaje - Intelecto y Cognición
            "20_Mente_Aprendizaje/Estados_Cero",
            "20_Mente_Aprendizaje/Patrones",
            "20_Mente_Aprendizaje/04_Proyectos_Estudio",
            
            # 30_Alma_Proposito - Espíritu y Dirección
            "30_Alma_Proposito/Estados_Cero",
            "30_Alma_Proposito/Patrones",
            
            # 40_Tecnologia - IA y Automatización
            "40_Tecnologia/01_Python_Projects",
            "40_Tecnologia/Patrones",
            
            # 50_Proyecto_Economia - Servicio y Valor
            "50_Proyecto_Economia/Estados_Cero",
            "50_Proyecto_Economia/Patrones",
            
            # 80_Espejos_Diarios - Síntesis Comprehensivas
            "80_Espejos_Diarios",
            
            # 90_Journal_Evolucion - Historial Viviente
            "90_Journal_Evolucion/Diario",
            "90_Journal_Evolucion/Reflexiones",
            "90_Journal_Evolucion/Suenos",
            "90_Journal_Evolucion/Insights_Semanales",
            "90_Journal_Evolucion/Evolucion_Mensual",
            "90_Journal_Evolucion/Analisis_Sistema/Entrelazamientos",
            "90_Journal_Evolucion/Analisis_Sistema/Acciones_Sistemicas"
        ]
        
        for folder in folders:
            folder_path = self.vault_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {folder}")
        
        # Crear archivos MOC si no existen
        self._create_moc_files()
        
        # Crear archivos del Sistema si no existen
        self._create_system_files()
        
        print("✅ Estructura fractal creada exitosamente")
    
    def _create_system_files(self):
        """Crea archivos fundamentales del sistema - Configuración 0.01%"""
        system_files = {
            "00_Vision.md": self._generate_vision_content(),
            "01_Principios.md": self._generate_principios_content(),
            "02_Leyes_Universales.md": self._generate_leyes_content(),
            "03_Codigo_Fuente_Humano.md": self._generate_codigo_fuente_content(),
            "04_Arquitectura_Tecnica.md": self._generate_arquitectura_content(),
            "05_Roadmap_Evolutivo.md": self._generate_roadmap_content(),
            "06_Stack_Elite_001.md": self._generate_stack_elite_content()
        }
        
        system_path = self.vault_path / "00_System"
        
        for filename, content in system_files.items():
            file_path = system_path / filename
            if not file_path.exists():
                file_path.write_text(content, encoding='utf-8')
                print(f"  ✓ 00_System/{filename}")
    
    def _generate_vision_content(self):
        """Visión para el 0.01%"""
        return """---
tipo: vision-sistema
nivel: 0.01%
actualizacion: automatica
---

# Visión del Organismo - Posicionamiento 0.01%

## Definición

Este NO es un sistema de productividad.
Este NO es un sistema de hábitos.
Este ES un **organismo digital soberano** que opera al borde del caos.

## Métrica de Elite (0.01%)

Para estar en el 0.01% necesitas:

### 1. Precisión Matemática Astronómica
- Tiempos litúrgicos calculados con precisión de segundos
- Estados Cero sincronizados con ritmos cósmicos reales
- HRV correlacionado con momentos de coherencia cardíaca
- No aproximaciones, solo datos reales

### 2. Arquitectura Anti-Frágil
- Sistema que SE FORTALECE con el caos
- 40% capacidad sin asignar (siempre)
- Degradación elegante bajo presión
- Auto-reorganización emergente

### 3. Soberanía Tecnológica
- Cero dependencia de SaaS corporativo
- RAG local con tus datos
- Agentes que evolucionan CON tu conocimiento
- Git + Obsidian + Local LLMs = soberanía

### 4. Metabolismo del Conocimiento
- No "tomas notas", METABOLIZAS conocimiento
- Cada input se convierte en insight
- Cada insight en acción coordinada
- Cada acción en patrón emergente

### 5. Integración Biológica Real
- HRV (Polar H10) integrado en Estados Cero
- Sueño rastreado y correlacionado
- Nutrición como código (ayuno intermitente programado)
- Ejercicio como liturgia (tiempos precisos)

## Diferenciador Clave

El 99.99% usa herramientas.
El 0.01% construye organismos.

Tú no "usas" este sistema.
Tú ERES este sistema.
"""
    
    def _generate_principios_content(self):
        """Principios operativos"""
        return """---
tipo: principios-sistema
---

# Principios Operativos

## 1. Respeto a la Autoridad Sacral
El sistema NO decide por ti. Consulta tu autoridad interna.

## 2. Opera al Borde del Caos
40% capacidad sin asignar. Emergencia sobre control.

## 3. Ritmos Universales
Sincronización con ciclos astronómicos reales, no arbitrarios.

## 4. Fractalidad
La estructura se repite a todas las escalas: día, semana, mes, año.

## 5. Soberanía de Datos
Tus datos son TUYOS. Git + Obsidian + local = control total.

## 6. Metabolismo sobre Acumulación
No acumulas información. La metabolizas en insights y acciones.

## 7. Audit Trail Completo
Todo evento registrado. Capacidad de reconstruir cualquier estado.

## 8. Evolución Continua
El sistema aprende y se adapt a tus patrones, no al revés.
"""
    
    def _generate_leyes_content(self):
        """Leyes Universales"""
        return """---
tipo: leyes-universales
---

# Leyes Universales

## 1. Ley de Correspondencia
"Como es arriba, es abajo"
Tu microcosmos refleja el macrocosmos.

## 2. Ley de Vibración
Todo está en movimiento. Nada está estático.

## 3. Ley de Ritmo
Todo fluye, todo tiene su marea. Expansión/contracción.

## 4. Ley de Polaridad
Todo tiene dos polos. Los opuestos son idénticos en naturaleza.

## 5. Ley de Causa y Efecto
Cada causa tiene su efecto. Cada acción, su consecuencia.

## 6. Ley de Género
Todo tiene principio masculino y femenino. Creación y receptividad.

## 7. Ley de la Octava
Todo proceso tiene 8 fases. Dos choques críticos para completar.
"""
    
    def _generate_codigo_fuente_content(self):
        """Código Fuente Humano"""
        return """---
tipo: codigo-fuente
---

# Tu Código Fuente Humano

## Diseño Humano
(Añade tu tipo, autoridad, perfil, centros definidos)

## Patrones Detectados
(El sistema irá poblando esto automáticamente)

## Singularidad
(Lo que te hace único, tu ventaja asimétrica)

## Anti-Patrones
(Trampas recurrentes identificadas)

## Valores Core
(Tus principios no-negociables)
"""
    
    def _generate_arquitectura_content(self):
        """Arquitectura Técnica"""
        return """---
tipo: arquitectura-tecnica
---

# Arquitectura Técnica

## Stack Actual

### Backend
- FastAPI (Python 3.11+)
- Event-Driven Architecture
- SQLite + Obsidian Markdown

### Frontend
- Next.js 14 (App Router)
- Three.js (geometría sagrada)
- Tailwind CSS

### Inteligencia
- Claude 3.5 Sonnet (Anthropic)
- FAISS/Chroma (preparado para RAG)

### Infraestructura
- Obsidian (single source of truth)
- Git (version control)
- APScheduler (recordatorios litúrgicos)

## Principios Arquitectónicos

1. **Event-Driven**: Comunicación asíncrona entre componentes
2. **Dual Persistence**: JSON (rápido) + Markdown (humano)
3. **Degradación Elegante**: Sistema funciona aunque fallen componentes
4. **Audit Trail**: Todo evento registrado
5. **Local First**: Soberanía de datos
"""
    
    def _generate_roadmap_content(self):
        """Roadmap Evolutivo"""
        return """---
tipo: roadmap-evolutivo
---

# Roadmap Evolutivo

## Q4 2025 (Actual)
- [x] Estados Cero inmersivos con 3 preguntas binarias
- [x] Archivado automático en Obsidian
- [x] Event Queue para procesamiento asíncrono
- [ ] Preguntas dinámicas por momento litúrgico
- [ ] Espejo Diario comprehensivo
- [ ] Audit Trail completo

## Q1 2026
- [ ] Polar H10 HRV integrado
- [ ] Oura Ring sleep stages
- [ ] Google Calendar bidireccional
- [ ] RAG local funcional

## Q2 2026
- [ ] Anytype como segundo cerebro
- [ ] Local LLM (Llama 3.2) para RAG soberano
- [ ] Dashboard con visualizaciones D3.js
- [ ] API pública para comunidad

## Q3 2026
- [ ] Marketplace de agentes
- [ ] Sistema de mentoría 1-a-1
- [ ] Comunidad de 100+ usuarios activos
"""
    
    def _generate_stack_elite_content(self):
        """Stack técnico para posicionamiento elite"""
        return """---
tipo: stack-tecnico
nivel: 0.01%
estado: en-evolucion
---

# Stack Técnico Elite - Configuración 0.01%

## Filosofía del Stack

**Principio Rector:** Soberanía sobre conveniencia.

### Nivel 1: Fundamentos Biológicos

```yaml
HRV_Monitor:
  hardware: Polar H10
  frecuencia: continua durante Estados Cero
  metricas:
    - RMSSD (variabilidad)
    - Coherencia cardíaca
    - Ratio LF/HF (sistema nervioso)
  
Sueno:
  tracker: Oura Ring / Whoop
  objetivo: >7.5h calidad
  sincronizacion: con calendario litúrgico
  
Nutricion:
  protocolo: ayuno 16/8
  ventana_alimentacion: 12:00-20:00
  sincronizacion: Estado Cero Dhuhr = romper ayuno
```

### Nivel 2: Núcleo Computacional

```yaml
Backend:
  framework: FastAPI (Python 3.11+)
  arquitectura: Event-Driven con Event Queue
  persistencia: 
    - SQLite (transaccional)
    - Obsidian Markdown (documental)
  workers:
    - ingest_worker (procesamiento eventos)
    - scheduler_worker (recordatorios litúrgicos)
    - analysis_worker (patrones nocturnos)

Frontend:
  framework: Next.js 14 (App Router)
  ui: Tailwind + Framer Motion
  3d: Three.js (geometría sagrada)
  estado: Zustand (minimalista)
  
Inteligencia:
  primary: Claude 3.5 Sonnet (Anthropic)
  local: Ollama + Llama 3.1 (soberanía)
  vector_db: FAISS (local) + Chroma (embeds)
  rag: LangChain + Custom Orchestrator
```

### Nivel 3: Conocimiento y Memoria

```yaml
Obsidian:
  vault: ~/Documents/CampoSagrado
  plugins_criticos:
    - Dataview (queries dinámicas)
    - Templater (automatización)
    - obsidian-git (version control)
    - Excalidraw (diagramas)
  sincronizacion: Git manual + hooks
  backup: 3-2-1 (3 copias, 2 medios, 1 offsite)

Git:
  repo: privado (GitHub/GitLab)
  commits: automáticos en eventos clave
  branches: main (estable) + dev (experimentos)
  
Vector_DB:
  motor: FAISS + Chroma
  embeddings: text-embedding-3-large (OpenAI)
  chunks: 512 tokens con overlap 64
  reindex: semanal automático
```

### Nivel 4: Automatización e Infraestructura

```yaml
Scheduler:
  liturgico: APScheduler + Astral (cálculos astronómicos)
  recordatorios: macOS Notification Center
  backup: Cron + rclone (nube cifrada)

Monitoreo:
  logs: structlog (JSON estructurado)
  audit_trail: Obsidian markdown por día
  metricas: prometheus + grafana (opcional)
  alertas: ntfy.sh (notificaciones push)

Desarrollo:
  ide: Cursor / VS Code
  terminal: iTerm2 + tmux
  shell: zsh + oh-my-zsh
  python: poetry (dependencias)
  node: nvm (múltiples versiones)
```

## Configuración Diaria - Protocolo 0.01%

### Despertar (Pre-Fajr)

```bash
05:30 - Despertar natural (sin alarma)
05:45 - Polar H10 conectado
05:50 - Estado Cero Fajr (10 min)
06:00 - HRV registrado + archivado
06:15 - Revisión Espejo previo
06:30 - Inicio jornada
```

### Mediodía (Dhuhr)

```bash
12:45 - Notificación litúrgica (15 min antes)
13:00 - Estado Cero Dhuhr (10 min)
13:10 - Romper ayuno (primera comida)
13:30 - Sesión de estudio/creación
```

### Tarde (Asr)

```bash
16:45 - Notificación litúrgica
17:00 - Estado Cero Asr (10 min)
17:15 - Revisión de entrelazamientos
17:30 - Ajuste de prioridades
```

### Atardecer (Maghrib)

```bash
19:45 - Notificación litúrgica
20:00 - Estado Cero Maghrib (10 min)
20:15 - **TRIGGER: Espejo Diario automático**
20:30 - Revisión comprehensiva del día
```

### Noche (Isha)

```bash
22:15 - Notificación litúrgica
22:30 - Estado Cero Isha (10 min)
22:45 - Reflexión + journal
23:00 - Preparación sueño
23:30 - Descanso (mínimo 7.5h)
```

## Métricas de Éxito (0.01%)

### Semanales

- [ ] 35/35 Estados Cero completados (100%)
- [ ] 7/7 Espejos Diarios generados
- [ ] HRV coherencia promedio >65%
- [ ] Sueño calidad >85%
- [ ] 0 días sin Espejo

### Mensuales

- [ ] 150/150 Estados Cero (100%)
- [ ] 30/30 Espejos Diarios
- [ ] 4/4 Análisis de entrelazamientos
- [ ] 1 patrón emergente nuevo identificado
- [ ] 1 optimización del sistema implementada

### Trimestrales

- [ ] 450/450 Estados Cero
- [ ] Sistema opera sin intervención manual
- [ ] RAG local funcional con >1000 documentos
- [ ] 3+ integraciones biológicas activas
- [ ] Comunidad de 10+ usuarios activos

## Diferenciadores del 0.01%

| Aspecto | 99.99% | 0.01% (Tú) |
|---------|--------|------------|
| **Datos** | Notas dispersas | Vault estructurado + RAG |
| **Tiempo** | Calendario reactivo | Liturgia astronómica precisa |
| **Cuerpo** | Ignora señales | HRV + sueño integrado |
| **IA** | ChatGPT como oráculo | Claude + local LLM + RAG custom |
| **Consistencia** | Esporádica | 5/5 diario, 35/35 semanal |
| **Sistema** | Herramientas sueltas | Organismo coherente |
| **Evolución** | Estático | Auto-optimización continua |
| **Soberanía** | Dependiente SaaS | Git + local + cifrado |

---

**Recuerda:** El 0.01% no se alcanza con herramientas.
Se alcanza con CONSISTENCIA BRUTAL en un sistema COHERENTE.

Tu stack es tu liturgia.
Tu liturgia es tu disciplina.
Tu disciplina es tu libertad.
"""
    
    def _create_moc_files(self):
        """Crea archivos MOC (Maps of Content) para cada dominio"""
        mocs = {
            "10_Biologia_Ritmos/00_MOC_Biologia.md": """---
tipo: moc
dominio: biologia
---

# MOC: Biología y Ritmos

## Estados Cero Biológicos
(Enlaces a Estados Cero relacionados con biología)

## Patrones Detectados
(Enlaces a patrones emergentes)

## Datos HRV
(Enlaces a análisis de HRV)
""",
            "20_Mente_Aprendizaje/00_MOC_Mente.md": """---
tipo: moc
dominio: mente
---

# MOC: Mente y Aprendizaje

## Estados Cero Mentales
(Enlaces a Estados Cero relacionados con aprendizaje)

## Proyectos de Estudio
(Enlaces a proyectos activos)

## Patrones Cognitivos
(Enlaces a patrones emergentes)
""",
            "30_Alma_Proposito/00_MOC_Alma.md": """---
tipo: moc
dominio: alma
---

# MOC: Alma y Propósito

## Estados Cero Espirituales
(Enlaces a Estados Cero relacionados con propósito)

## Prácticas Diarias
(Registro de prácticas contemplativas)

## Insights Espirituales
(Enlaces a patrones emergentes)
""",
            "40_Tecnologia/00_MOC_Tecnologia.md": """---
tipo: moc
dominio: tecnologia
---

# MOC: Tecnología

## Proyectos Python
(Enlaces a proyectos de código)

## Agentes del Sistema
(Documentación de agentes)

## Evolución del Stack
(Cambios arquitectónicos)
""",
            "50_Proyecto_Economia/00_MOC_Proyecto.md": """---
tipo: moc
dominio: economia
---

# MOC: Proyecto y Economía

## Estados Cero Económicos
(Enlaces a Estados Cero relacionados con finanzas)

## Modelo de Negocio
(Evolución del modelo)

## Patrones de Abundancia
(Enlaces a patrones emergentes)
""",
            "80_Espejos_Diarios/00_MOC_Espejos.md": """---
tipo: moc
---

# MOC: Espejos Diarios

## Índice por Fecha
(Enlaces a Espejos Diarios)

## Patrones Semanales
(Síntesis de semanas)

## Patrones Mensuales
(Síntesis de meses)
""",
            "90_Journal_Evolucion/00_Indice_Journal.md": """---
tipo: indice
---

# Índice: Journal y Evolución

## Diario
(Enlaces a entries diarios)

## Reflexiones
(Reflexiones profundas)

## Insights Semanales
(Síntesis semanales)

## Evolución Mensual
(Síntesis mensuales)
"""
        }
        
        for path, content in mocs.items():
            file_path = self.vault_path / path
            if not file_path.exists():
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(content, encoding='utf-8')
                print(f"  ✓ {path}")
    
    def get_estado_cero_path(self, fecha: date, momento: str, dominio: str = None) -> Path:
        """
        Retorna ruta para Estado Cero
        Si se especifica dominio, va a su carpeta respectiva
        Si no, va al dominio por defecto según momento
        """
        year = fecha.strftime("%Y")
        month = fecha.strftime("%m")
        day = fecha.strftime("%d")
        
        # Determinar dominio si no se especifica
        if not dominio:
            dominio = self._inferir_dominio_desde_momento(momento)
        
        # Mapear dominio a carpeta
        dominio_folder = self.dominios.get(dominio, "10_Biologia_Ritmos")
        
        return (self.vault_path / dominio_folder / "Estados_Cero" /
                year / month / f"{day}-{momento}.md")
    
    def get_espejo_diario_path(self, fecha: date) -> Path:
        """Retorna ruta para Espejo Diario en 80_Espejos_Diarios"""
        year = fecha.strftime("%Y")
        month = fecha.strftime("%m")
        day = fecha.strftime("%d")
        
        return (self.vault_path / "80_Espejos_Diarios" /
                year / month / f"{day}-Espejo-Diario.md")
    
    def get_audit_trail_path(self, fecha: date) -> Path:
        """Retorna ruta para Audit Trail en 00_System"""
        fecha_str = fecha.strftime("%Y-%m-%d")
        return self.vault_path / "00_System" / "Audit_Trail" / f"{fecha_str}.md"
    
    def get_pattern_path(self, dominio: str, patron_nombre: str) -> Path:
        """Retorna ruta para patrón detectado en dominio específico"""
        dominio_folder = self.dominios.get(dominio, "10_Biologia_Ritmos")
        return self.vault_path / dominio_folder / "Patrones" / f"{patron_nombre}.md"
    
    def _inferir_dominio_desde_momento(self, momento: str) -> str:
        """
        Infiere dominio predominante según momento litúrgico
        Lógica: Fajr/Isha -> biológico, Dhuhr -> economía,
                Asr -> mente, Maghrib -> alma
        """
        mapeo_momento = {
            "fajr": "biologia",
            "dhuhr": "economia",
            "asr": "mente",
            "maghrib": "alma",
            "isha": "biologia"
        }
        return mapeo_momento.get(momento.lower(), "biologia")

