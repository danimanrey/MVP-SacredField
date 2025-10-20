from datetime import datetime
from typing import Dict, Optional
from sqlalchemy.orm import Session
import os

from models.schemas import EstadoCeroCompleto
from services.claude_client import ClaudeClient
from services.obsidian_parser import asignar_dimension_automatica


class AgenteDocumentador:
    """
    Agente Archivista
    Genera documentación permanente en Obsidian
    """
    
    def __init__(self, db: Session, claude: ClaudeClient, vault_path: str):
        self.db = db
        self.claude = claude
        self.vault_path = vault_path
        
    async def documentar_estado_cero(
        self,
        estado: EstadoCeroCompleto
    ) -> str:
        """
        Genera documento Markdown del Estado Cero
        Guarda en Obsidian vault
        """
        
        # Generar contenido
        contenido = await self._generar_contenido_estado_cero(estado)
        
        # Determinar filepath
        fecha_str = estado.fecha.strftime("%Y-%m-%d")
        filepath = os.path.join(
            self.vault_path,
            "50-Conversaciones-IA",
            "Estados-Cero",
            f"{fecha_str}",
            f"{estado.momento.value}.md"
        )
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Guardar archivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        return filepath
    
    def _asignar_dimension_estado_cero(self, estado: EstadoCeroCompleto) -> str:
        """Asigna dimensión basándose en las categorías de las preguntas"""
        # Contar categorías
        categorias = {}
        for pregunta in estado.preguntas:
            cat = pregunta.categoria
            categorias[cat] = categorias.get(cat, 0) + 1
        
        # Retornar la más común
        if categorias:
            return max(categorias, key=categorias.get)
        
        return 'espiritualidad'  # Por defecto para Estados Cero
    
    async def _generar_contenido_estado_cero(
        self,
        estado: EstadoCeroCompleto
    ) -> str:
        """Genera Markdown del Estado Cero con metadata completa"""
        
        # Asignar dimensión automáticamente
        dimension = self._asignar_dimension_estado_cero(estado)
        
        # Formatear respuestas
        respuestas_formateadas = []
        for i, resp in enumerate(estado.respuestas, 1):
            pregunta = next(p for p in estado.preguntas if p.id == resp.pregunta_id)
            emoji = "↗️" if resp.sensacion.value == "expansion" else "↘️"
            barras = "█" * resp.intensidad + "░" * (5 - resp.intensidad)
            
            respuestas_formateadas.append(f"""
### Pregunta {i}: {pregunta.pregunta}

**Categoría**: {pregunta.categoria}  
**Respuesta**: {emoji} {resp.sensacion.value.capitalize()} - {barras} ({resp.intensidad}/5)
{f'**Nota**: {resp.nota}' if resp.nota else ''}
""")
        
        # Preparar variables para evitar backslashes en f-string
        fecha_str = estado.fecha.strftime("%Y-%m-%d")
        hora_str = estado.fecha.strftime("%H:%M")
        fecha_larga = estado.fecha.strftime("%d de %B, %Y")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Construir documento con metadata completa
        contenido = f"""---
tipo: estado-cero
momento: {estado.momento.value}
fecha: {fecha_str}
hora: {hora_str}
dimension: {dimension}
tags:
  - estado-cero
  - {estado.momento.value}
  - {dimension}
enlaces:
  - "[[Estados Cero]]"
  - "[[{fecha_str}]]"
---

# Estado Cero: {estado.momento.value.capitalize()}

**{fecha_larga} - {hora_str}**

## Contexto

### Temporal
- **Momento**: {estado.contexto.temporal.momento_liturgico.value}
- **Cualidad**: {estado.contexto.temporal.cualidad_momento}
- **Día**: {estado.contexto.temporal.dia_semana}
- **Mes**: {estado.contexto.temporal.mes_hijri} - {estado.contexto.temporal.cualidad_mes}

### Biológico
- **Energía**: {estado.contexto.biologico.energia_actual}/5
- **HRV**: {estado.contexto.biologico.hrv or 'N/A'}
- **Luz solar hoy**: {"✓" if estado.contexto.biologico.luz_solar_hoy else "✗"}
- **Ejercicio hoy**: {"✓" if estado.contexto.biologico.ejercicio_hoy else "✗"}

### Financiero
- **Runway**: {estado.contexto.financiero.runway_meses} meses
- **Urgencia**: {"⚠️ ALTA" if estado.contexto.financiero.urgencia_financiera else "Normal"}

### Conocimiento
- **Capturas sin procesar**: {estado.contexto.conocimiento.capturas_sin_procesar}
- **Insights listos**: {estado.contexto.conocimiento.insights_listos}

---

## Consulta Sacral

{"".join(respuestas_formateadas)}

---

## Dirección Emergente

{estado.direccion_emergente}

---

## Acción Tangible

**{estado.accion_tangible.descripcion}**

- **Resultado observable**: {estado.accion_tangible.resultado_observable}
- **Duración estimada**: {estado.accion_tangible.duracion_estimada}
- **Energía requerida**: {estado.accion_tangible.energia_requerida}/5
{f'- **Rol**: {estado.accion_tangible.rol}' if estado.accion_tangible.rol else ''}

---

## Chat de Clarificación

{chr(10).join([f"**{msg.role.capitalize()}**: {msg.content}" for msg in estado.chat_clarificacion])}

---

*Generado por Campo Sagrado - {timestamp}*
"""
        
        return contenido
    
    async def documentar_reporte_diario(
        self,
        reporte: 'ReporteDiario'
    ) -> str:
        """
        Genera documento de reporte diario
        """
        
        contenido = await self._generar_contenido_reporte_diario(reporte)
        
        # Determinar filepath
        fecha_str = reporte.fecha.strftime("%Y-%m-%d")
        filepath = os.path.join(
            self.vault_path,
            "40-Journal",
            f"{fecha_str}-reporte-diario.md"
        )
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Guardar archivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        return filepath
    
    async def _generar_contenido_reporte_diario(
        self,
        reporte: 'ReporteDiario'
    ) -> str:
        """Genera Markdown del reporte diario"""
        
        # Calcular métricas
        porcentaje_no_neg = (reporte.no_negociables_cumplidos / max(reporte.no_negociables_totales, 1)) * 100
        
        contenido = f"""---
tipo: reporte-diario
fecha: {reporte.fecha.strftime("%Y-%m-%d")}
---

# Reporte Diario: {reporte.fecha.strftime("%d de %B, %Y")}

**Generado**: {reporte.generado_timestamp.strftime("%H:%M")}

## Resumen Ejecutivo

- **Estados Cero**: {reporte.estados_cero_completados}/5 completados
- **No-negociables**: {reporte.no_negociables_cumplidos}/{reporte.no_negociables_totales} ({porcentaje_no_neg:.1f}%)
- **Sesiones**: {len(reporte.sesiones)}

---

## Resonancias del Día

{''.join([f"- {resonancia}" for resonancia in reporte.resonancias])}

---

## Obstrucciones Observadas

{''.join([f"- {obstruccion}" for obstruccion in reporte.obstrucciones])}

---

## Semilla para Mañana

{reporte.semilla_mañana}

---

## Datos Biológicos

- **Energía promedio**: {reporte.biologia.get('energia_promedio', 'N/A')}/5
- **HRV**: {reporte.biologia.get('hrv', 'N/A')}
- **Calidad sueño**: {reporte.biologia.get('calidad_sueno', 'N/A')}
- **Luz solar**: {"✓" if reporte.biologia.get('luz_solar', False) else "✗"}
- **Ejercicio**: {"✓" if reporte.biologia.get('ejercicio', False) else "✗"}

---

## Datos Financieros

- **Runway**: {reporte.finanzas.get('runway', 'N/A')} meses
- **Tiempo en generación**: {reporte.finanzas.get('tiempo_generacion', 0):.1f}h

---

## Sesiones del Día

{''.join([f"- **{sesion.get('rol', 'Sesión')}**: {sesion.get('duracion', 0)}min (Flujo: {sesion.get('calidad_flujo', 'N/A')})" for sesion in reporte.sesiones])}

---

*Generado automáticamente por Campo Sagrado - {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
        
        return contenido
    
    async def documentar_insight_semanal(
        self,
        insights: Dict,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> str:
        """
        Genera documento de insights semanales
        """
        
        contenido = f"""---
tipo: insight-semanal
periodo: {fecha_inicio.strftime("%Y-%m-%d")} a {fecha_fin.strftime("%Y-%m-%d")}
---

# Insights Semanales: {fecha_inicio.strftime("%d %B")} - {fecha_fin.strftime("%d %B, %Y")}

## Patrones Detectados

{''.join([f"- {patron}" for patron in insights.get('patrones', [])])}

## Métricas Clave

- **Estados Cero promedio**: {insights.get('promedio_estados_cero_dia', 0):.1f}/día
- **Total Estados Cero**: {insights.get('total_estados_cero', 0)}
- **Total sesiones**: {insights.get('total_sesiones', 0)}
- **Día más productivo**: {insights.get('dia_mas_productivo', ['N/A', 0])[0] if insights.get('dia_mas_productivo') else 'N/A'}

## Recomendaciones

{''.join([f"- {rec}" for rec in insights.get('recomendaciones', [])])}

---

*Generado automáticamente por Campo Sagrado - {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
        
        # Determinar filepath
        semana_str = fecha_inicio.strftime("%Y-%m-%d")
        filepath = os.path.join(
            self.vault_path,
            "40-Journal",
            f"semana-{semana_str}-insights.md"
        )
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Guardar archivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        return filepath
