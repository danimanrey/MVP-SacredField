"""
📝 Campo Sagrado - Documentador Mejorado
========================================

Genera acciones claras y específicas basándose en:
1. Análisis de patrones de Estados Cero
2. Entrelazamiento entre dominios
3. Validación de orquestación en armonía

Opera con pensamiento sistémico y reconocimiento de patrones.
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Any, Tuple
import json
from dataclasses import dataclass
from pathlib import Path

from .analizador_patrones import AnalizadorPatrones, AccionEmergente
from .entrelazador_dominios import EntrelazadorDominios, AccionCoordinada

@dataclass
class AccionDocumentada:
    """Acción clara y específica generada por el Documentador"""
    id: str
    nombre: str
    tipo: str  # "inmediata", "planificada", "rutina", "experimento", "coordinada"
    prioridad: int  # 1-5 (1 = máxima prioridad)
    urgencia: float  # 0.0 - 1.0
    impacto_sistémico: float  # 0.0 - 1.0
    
    # Detalles de la acción
    descripcion: str
    contexto: str
    dominios_implicados: List[str]
    
    # Ejecución
    tiempo_estimado: str
    recursos_requeridos: List[str]
    prerequisitos: List[str]
    secuencia_pasos: List[str]
    
    # Resultados esperados
    resultado_observable: str
    indicadores_exito: List[str]
    metricas_seguimiento: List[str]
    
    # Metadatos
    fuente_patrones: List[str]
    fuente_entrelazamiento: List[str]
    validacion_armonia: bool
    fecha_creacion: str
    fecha_vencimiento: Optional[str]
    
    # Integración con calendario
    momento_optimo: str  # Momento litúrgico óptimo para ejecutar
    frecuencia: str  # "única", "diaria", "semanal", "mensual"
    recordatorios: List[str]

class DocumentadorMejorado:
    """
    Genera acciones claras basándose en análisis sistémico
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.analizador_patrones = AnalizadorPatrones(vault_path)
        self.entrelazador_dominios = EntrelazadorDominios(vault_path)
        
    def generar_acciones_sistemicas(self, dias_analisis: int = 7) -> List[AccionDocumentada]:
        """
        Genera acciones sistémicas basándose en análisis completo
        """
        print(f"🔍 Analizando últimos {dias_analisis} días...")
        
        # 1. Análisis de patrones
        analisis_patrones = self.analizador_patrones.analizar_ultimos_estados(dias_analisis)
        print(f"✅ Patrones analizados: {analisis_patrones.get('total_estados', 0)} Estados Cero")
        
        # 2. Análisis de entrelazamiento
        dominios = self.entrelazador_dominios.analizar_estado_dominios(dias_analisis)
        entrelazamientos = self.entrelazador_dominios.detectar_entrelazamientos(dominios)
        acciones_coordinadas = self.entrelazador_dominios.generar_acciones_coordinadas(dominios, entrelazamientos)
        print(f"✅ Entrelazamientos detectados: {len(entrelazamientos)}")
        
        # 3. Generar acciones documentadas
        acciones_documentadas = []
        
        # Convertir acciones emergentes de patrones
        acciones_patrones = analisis_patrones.get('acciones_emergentes', [])
        for accion_patron in acciones_patrones:
            accion_doc = self._convertir_accion_patron(accion_patron, analisis_patrones)
            if accion_doc:
                acciones_documentadas.append(accion_doc)
        
        # Convertir acciones coordinadas de entrelazamiento
        for accion_coord in acciones_coordinadas:
            accion_doc = self._convertir_accion_coordinada(accion_coord, entrelazamientos)
            if accion_doc:
                acciones_documentadas.append(accion_doc)
        
        # 4. Validar armonía y priorizar
        acciones_validadas = self._validar_armonia_acciones(acciones_documentadas, dominios, entrelazamientos)
        acciones_priorizadas = self._priorizar_acciones(acciones_validadas)
        
        print(f"✅ {len(acciones_priorizadas)} acciones sistémicas generadas")
        
        return acciones_priorizadas
    
    def _convertir_accion_patron(self, accion_patron: AccionEmergente, analisis: Dict[str, Any]) -> Optional[AccionDocumentada]:
        """Convierte una acción emergente de patrones en acción documentada"""
        
        # Determinar prioridad basada en urgencia e impacto
        prioridad = self._calcular_prioridad(accion_patron.urgencia, accion_patron.impacto_esperado)
        
        # Determinar momento óptimo basado en patrón de energía
        patron_energia = analisis.get('patron_energia')
        momento_optimo = patron_energia.momento_predominante if patron_energia else 'fajr'
        
        # Generar ID único
        accion_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(accion_patron.descripcion) % 1000}"
        
        return AccionDocumentada(
            id=accion_id,
            nombre=f"Patrón: {accion_patron.descripcion[:50]}...",
            tipo=accion_patron.tipo,
            prioridad=prioridad,
            urgencia=accion_patron.urgencia,
            impacto_sistémico=accion_patron.impacto_esperado,
            
            descripcion=accion_patron.descripcion,
            contexto=f"Emergente del análisis de patrones en {analisis.get('periodo_analisis', 'N/A')}",
            dominios_implicados=[accion_patron.dominio],
            
            tiempo_estimado=accion_patron.tiempo_estimado,
            recursos_requeridos=accion_patron.recursos_requeridos,
            prerequisitos=self._generar_prerequisitos(accion_patron),
            secuencia_pasos=self._generar_secuencia_pasos(accion_patron),
            
            resultado_observable=f"Resultado observable: {accion_patron.descripcion}",
            indicadores_exito=accion_patron.indicadores_exito,
            metricas_seguimiento=self._generar_metricas_seguimiento(accion_patron),
            
            fuente_patrones=[f"Análisis {analisis.get('periodo_analisis', 'N/A')}"],
            fuente_entrelazamiento=[],
            validacion_armonia=False,  # Se validará después
            
            fecha_creacion=datetime.now().isoformat(),
            fecha_vencimiento=self._calcular_fecha_vencimiento(accion_patron.urgencia),
            
            momento_optimo=momento_optimo,
            frecuencia=self._determinar_frecuencia(accion_patron.tipo),
            recordatorios=self._generar_recordatorios(accion_patron, momento_optimo)
        )
    
    def _convertir_accion_coordinada(self, accion_coord: AccionCoordinada, entrelazamientos: List) -> Optional[AccionDocumentada]:
        """Convierte una acción coordinada de entrelazamiento en acción documentada"""
        
        # Determinar prioridad
        prioridad = self._calcular_prioridad(accion_coord.urgencia, accion_coord.impacto_sistémico)
        
        # Determinar momento óptimo basado en dominios implicados
        momento_optimo = self._determinar_momento_optimo_dominios(accion_coord.dominios_implicados)
        
        # Generar ID único
        accion_id = f"coord_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(accion_coord.nombre) % 1000}"
        
        return AccionDocumentada(
            id=accion_id,
            nombre=f"Coord: {accion_coord.nombre}",
            tipo="coordinada",
            prioridad=prioridad,
            urgencia=accion_coord.urgencia,
            impacto_sistémico=accion_coord.impacto_sistémico,
            
            descripcion=accion_coord.resultado_esperado,
            contexto=f"Coordinación entre dominios: {', '.join(accion_coord.dominios_implicados)}",
            dominios_implicados=accion_coord.dominios_implicados,
            
            tiempo_estimado=accion_coord.tiempo_total,
            recursos_requeridos=accion_coord.recursos_totales,
            prerequisitos=self._generar_prerequisitos_coordinados(accion_coord),
            secuencia_pasos=accion_coord.secuencia,
            
            resultado_observable=accion_coord.resultado_esperado,
            indicadores_exito=accion_coord.indicadores_exito,
            metricas_seguimiento=self._generar_metricas_coordinadas(accion_coord),
            
            fuente_patrones=[],
            fuente_entrelazamiento=[f"Entrelazamiento entre {', '.join(accion_coord.dominios_implicados)}"],
            validacion_armonia=False,  # Se validará después
            
            fecha_creacion=datetime.now().isoformat(),
            fecha_vencimiento=self._calcular_fecha_vencimiento(accion_coord.urgencia),
            
            momento_optimo=momento_optimo,
            frecuencia=self._determinar_frecuencia_coordinada(accion_coord),
            recordatorios=self._generar_recordatorios_coordinados(accion_coord, momento_optimo)
        )
    
    def _validar_armonia_acciones(self, acciones: List[AccionDocumentada], dominios: Dict, entrelazamientos: List) -> List[AccionDocumentada]:
        """Valida que las acciones estén en armonía con el sistema"""
        
        acciones_armonizadas = []
        
        for accion in acciones:
            # Verificar compatibilidad con estado actual de dominios
            es_armonica = self._verificar_compatibilidad_dominios(accion, dominios)
            
            # Verificar que no genere conflictos con otras acciones
            es_compatible = self._verificar_compatibilidad_acciones(accion, acciones_armonizadas)
            
            if es_armonica and es_compatible:
                accion.validacion_armonia = True
                acciones_armonizadas.append(accion)
            else:
                # Intentar ajustar la acción para que sea armónica
                accion_ajustada = self._ajustar_accion_armonia(accion, dominios)
                if accion_ajustada:
                    accion_ajustada.validacion_armonia = True
                    acciones_armonizadas.append(accion_ajustada)
        
        return acciones_armonizadas
    
    def _priorizar_acciones(self, acciones: List[AccionDocumentada]) -> List[AccionDocumentada]:
        """Prioriza las acciones basándose en múltiples criterios"""
        
        def calcular_score(accion: AccionDocumentada) -> float:
            # Score basado en urgencia, impacto y prioridad
            score_urgencia = accion.urgencia * 0.4
            score_impacto = accion.impacto_sistémico * 0.4
            score_prioridad = (6 - accion.prioridad) / 5 * 0.2  # Invertir prioridad (1=5, 5=1)
            
            return score_urgencia + score_impacto + score_prioridad
        
        # Ordenar por score descendente
        acciones_ordenadas = sorted(acciones, key=calcular_score, reverse=True)
        
        # Renumerar prioridades
        for i, accion in enumerate(acciones_ordenadas, 1):
            accion.prioridad = min(i, 5)  # Máximo prioridad 5
        
        return acciones_ordenadas
    
    def generar_reporte_acciones(self, acciones: List[AccionDocumentada]) -> str:
        """Genera reporte completo de acciones en formato Markdown"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        reporte = f"""---
tipo: acciones-sistemicas
fecha: {date.today().isoformat()}
total_acciones: {len(acciones)}
timestamp: {timestamp}
---

# 📝 Acciones Sistémicas - {date.today().strftime("%d/%m/%Y")}

**Total de acciones generadas:** {len(acciones)}  
**Fecha de análisis:** {date.today().strftime("%d/%m/%Y")}

## 🎯 Resumen Ejecutivo

"""
        
        # Estadísticas generales
        tipos_acciones = {}
        dominios_implicados = set()
        urgencia_total = 0
        impacto_total = 0
        
        for accion in acciones:
            tipos_acciones[accion.tipo] = tipos_acciones.get(accion.tipo, 0) + 1
            dominios_implicados.update(accion.dominios_implicados)
            urgencia_total += accion.urgencia
            impacto_total += accion.impacto_sistémico
        
        # Evitar división por cero
        total_acciones = len(acciones) if len(acciones) > 0 else 1
        
        reporte += f"""- **Tipos de acciones:** {', '.join([f"{tipo} ({count})" for tipo, count in tipos_acciones.items()])}
- **Dominios implicados:** {', '.join(sorted(dominios_implicados))}
- **Urgencia promedio:** {urgencia_total / total_acciones:.1%}
- **Impacto sistémico promedio:** {impacto_total / total_acciones:.1%}

"""
        
        # Acciones por prioridad
        reporte += "## 🚀 Acciones por Prioridad\n\n"
        
        for i, accion in enumerate(acciones, 1):
            reporte += f"""### {i}. {accion.nombre} (Prioridad {accion.prioridad})
- **Tipo:** {accion.tipo.title()}
- **Urgencia:** {accion.urgencia:.1%}
- **Impacto sistémico:** {accion.impacto_sistémico:.1%}
- **Dominios:** {', '.join(accion.dominios_implicados)}
- **Tiempo estimado:** {accion.tiempo_estimado}
- **Momento óptimo:** {accion.momento_optimo.upper()}

**Descripción:** {accion.descripcion}

**Contexto:** {accion.contexto}

**Recursos requeridos:**
"""
            for recurso in accion.recursos_requeridos:
                reporte += f"- {recurso}\n"
            
            reporte += "\n**Secuencia de pasos:**\n"
            for j, paso in enumerate(accion.secuencia_pasos, 1):
                reporte += f"{j}. {paso}\n"
            
            reporte += "\n**Indicadores de éxito:**\n"
            for indicador in accion.indicadores_exito:
                reporte += f"- {indicador}\n"
            
            reporte += f"\n**Recordatorios:** {', '.join(accion.recordatorios)}\n\n"
        
        reporte += f"""---

*Acciones generadas automáticamente por Campo Sagrado del Entrelazador - {timestamp}*

## 📋 Próximos Pasos

1. **Revisar acciones prioritarias** (1-3) para ejecución inmediata
2. **Programar en calendario** según momentos óptimos
3. **Configurar recordatorios** para seguimiento
4. **Ejecutar y documentar** resultados en próximos Estados Cero
"""
        
        return reporte
    
    def guardar_reporte_acciones(self, acciones: List[AccionDocumentada]) -> str:
        """Guarda el reporte de acciones en Obsidian"""
        
        reporte = self.generar_reporte_acciones(acciones)
        
        # Crear directorio de acciones
        acciones_dir = self.vault_path / "Acciones-Sistemicas"
        acciones_dir.mkdir(exist_ok=True)
        
        # Guardar archivo
        fecha_str = date.today().strftime("%Y-%m-%d")
        archivo = acciones_dir / f"Acciones-Sistemicas-{fecha_str}.md"
        
        archivo.write_text(reporte, encoding='utf-8')
        
        return str(archivo)
    
    # Métodos auxiliares
    def _calcular_prioridad(self, urgencia: float, impacto: float) -> int:
        """Calcula prioridad basada en urgencia e impacto"""
        score = (urgencia + impacto) / 2
        if score >= 0.8:
            return 1
        elif score >= 0.6:
            return 2
        elif score >= 0.4:
            return 3
        elif score >= 0.2:
            return 4
        else:
            return 5
    
    def _generar_prerequisitos(self, accion_patron) -> List[str]:
        """Genera prerequisitos para una acción de patrón"""
        prerequisitos = ["Estado Cero completado"]
        
        if accion_patron.tipo == "inmediata":
            prerequisitos.append("Tiempo disponible inmediato")
        elif accion_patron.tipo == "planificada":
            prerequisitos.append("Planificación previa")
        elif accion_patron.tipo == "experimento":
            prerequisitos.append("Mentalidad experimental")
        
        return prerequisitos
    
    def _generar_secuencia_pasos(self, accion_patron) -> List[str]:
        """Genera secuencia de pasos para una acción"""
        pasos = [
            "Preparar entorno y recursos",
            f"Ejecutar: {accion_patron.descripcion}",
            "Observar resultados",
            "Documentar en próximo Estado Cero"
        ]
        return pasos
    
    def _generar_metricas_seguimiento(self, accion_patron) -> List[str]:
        """Genera métricas de seguimiento"""
        return [
            "Completitud de la acción",
            "Calidad de resultados",
            "Impacto en energía personal",
            "Efecto en dominios relacionados"
        ]
    
    def _calcular_fecha_vencimiento(self, urgencia: float) -> str:
        """Calcula fecha de vencimiento basada en urgencia"""
        if urgencia >= 0.8:
            return (date.today() + timedelta(days=1)).isoformat()
        elif urgencia >= 0.6:
            return (date.today() + timedelta(days=3)).isoformat()
        elif urgencia >= 0.4:
            return (date.today() + timedelta(days=7)).isoformat()
        else:
            return (date.today() + timedelta(days=14)).isoformat()
    
    def _determinar_frecuencia(self, tipo: str) -> str:
        """Determina frecuencia basada en tipo de acción"""
        frecuencias = {
            "inmediata": "única",
            "planificada": "única",
            "rutina": "diaria",
            "experimento": "semanal"
        }
        return frecuencias.get(tipo, "única")
    
    def _generar_recordatorios(self, accion_patron, momento_optimo: str) -> List[str]:
        """Genera recordatorios para una acción"""
        return [
            f"Recordar en próximo {momento_optimo.upper()}",
            "Verificar progreso en Estado Cero vespertino"
        ]
    
    def _determinar_momento_optimo_dominios(self, dominios: List[str]) -> str:
        """Determina momento óptimo basado en dominios implicados"""
        momentos_dominios = {
            "biologico": "fajr",
            "espiritual": "isha",
            "financiero": "dhuhr",
            "conocimiento": "asr"
        }
        
        # Si hay múltiples dominios, usar el primero
        if dominios:
            return momentos_dominios.get(dominios[0], "fajr")
        return "fajr"
    
    def _generar_prerequisitos_coordinados(self, accion_coord) -> List[str]:
        """Genera prerequisitos para acción coordinada"""
        return [
            "Múltiples dominios disponibles",
            "Tiempo suficiente para coordinación",
            "Recursos distribuidos entre dominios"
        ]
    
    def _generar_metricas_coordinadas(self, accion_coord) -> List[str]:
        """Genera métricas para acción coordinada"""
        return [
            "Sincronización entre dominios",
            "Impacto multiplicador observable",
            "Eficiencia de recursos",
            "Satisfacción general"
        ]
    
    def _determinar_frecuencia_coordinada(self, accion_coord) -> str:
        """Determina frecuencia para acción coordinada"""
        return "semanal"  # Las acciones coordinadas suelen ser semanales
    
    def _generar_recordatorios_coordinados(self, accion_coord, momento_optimo: str) -> List[str]:
        """Genera recordatorios para acción coordinada"""
        return [
            f"Planificar en {momento_optimo.upper()}",
            "Coordinar recursos entre dominios",
            "Evaluar impacto sistémico"
        ]
    
    def _verificar_compatibilidad_dominios(self, accion: AccionDocumentada, dominios: Dict) -> bool:
        """Verifica compatibilidad con estado actual de dominios"""
        # Lógica simple: verificar que los dominios implicados tengan suficiente energía
        for dominio_nombre in accion.dominios_implicados:
            if dominio_nombre in dominios:
                dominio = dominios[dominio_nombre]
                if dominio.energia < 0.3:  # Dominio con muy poca energía
                    return False
        return True
    
    def _verificar_compatibilidad_acciones(self, accion: AccionDocumentada, acciones_existentes: List[AccionDocumentada]) -> bool:
        """Verifica compatibilidad con otras acciones"""
        # Lógica simple: no permitir conflictos de recursos o tiempo
        for accion_existente in acciones_existentes:
            # Verificar conflicto de recursos
            recursos_comunes = set(accion.recursos_requeridos) & set(accion_existente.recursos_requeridos)
            if recursos_comunes and accion.urgencia < 0.8:  # Solo permitir si es muy urgente
                return False
        return True
    
    def _ajustar_accion_armonia(self, accion: AccionDocumentada, dominios: Dict) -> Optional[AccionDocumentada]:
        """Ajusta una acción para que sea armónica"""
        # Lógica simple: reducir recursos requeridos si hay conflictos
        accion_ajustada = accion
        accion_ajustada.recursos_requeridos = ["tiempo", "atención"]  # Recursos mínimos
        accion_ajustada.tiempo_estimado = "30 min"  # Tiempo reducido
        return accion_ajustada
