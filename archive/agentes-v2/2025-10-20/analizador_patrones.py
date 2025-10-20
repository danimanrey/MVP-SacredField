"""
🔍 Campo Sagrado - Analizador de Patrones
=========================================

Analiza patrones emergentes en los Estados Cero para detectar:
- Tendencias de energía y dirección
- Conflictos entre dominios
- Oportunidades de sinergia
- Acciones emergentes específicas

Opera con pensamiento sistémico y reconocimiento de patrones.
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Any, Tuple
import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

@dataclass
class PatronEnergia:
    """Patrón de energía detectado en Estados Cero"""
    tendencia: str  # "expansión", "contracción", "equilibrio"
    intensidad: float  # 0.0 - 1.0
    consistencia: float  # Qué tan consistente es el patrón
    momento_predominante: str  # En qué momento litúrgico se da más

@dataclass
class ConflictoDominio:
    """Conflicto detectado entre dominios"""
    dominios: List[str]  # ["biologico", "espiritual", "financiero"]
    tipo: str  # "energia", "tiempo", "recursos", "direccion"
    intensidad: float  # 0.0 - 1.0
    recomendacion: str

@dataclass
class SinergiaDominio:
    """Sinergia detectada entre dominios"""
    dominios: List[str]
    tipo: str  # "apoyo_mutuo", "secuencia_optima", "amplificacion"
    potencial: float  # 0.0 - 1.0
    accion_sugerida: str

@dataclass
class AccionEmergente:
    """Acción específica emergente del análisis de patrones"""
    tipo: str  # "inmediata", "planificada", "rutina", "experimento"
    dominio: str
    descripcion: str
    urgencia: float  # 0.0 - 1.0
    impacto_esperado: float  # 0.0 - 1.0
    recursos_requeridos: List[str]
    tiempo_estimado: str
    indicadores_exito: List[str]

class AnalizadorPatrones:
    """
    Analiza patrones en Estados Cero y genera insights sistémicos
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.estados_cero_dir = self.vault_path / "Estados-Cero"
        
    def analizar_ultimos_estados(self, dias: int = 7) -> Dict[str, Any]:
        """
        Analiza los últimos N días de Estados Cero
        """
        estados = self._cargar_estados_ultimos_dias(dias)
        
        if not estados:
            return {"error": "No hay Estados Cero suficientes para analizar"}
        
        # Análisis de patrones
        patron_energia = self._analizar_patron_energia(estados)
        conflictos = self._detectar_conflictos_dominios(estados)
        sinergias = self._detectar_sinergias_dominios(estados)
        acciones_emergentes = self._generar_acciones_emergentes(estados, patron_energia, conflictos, sinergias)
        
        return {
            "periodo_analisis": f"{dias} días",
            "total_estados": len(estados),
            "patron_energia": patron_energia,
            "conflictos_detectados": conflictos,
            "sinergias_detectadas": sinergias,
            "acciones_emergentes": acciones_emergentes,
            "timestamp_analisis": datetime.now().isoformat()
        }
    
    def _cargar_estados_ultimos_dias(self, dias: int) -> List[Dict]:
        """Carga Estados Cero de los últimos N días"""
        estados = []
        fecha_inicio = date.today() - timedelta(days=dias)
        
        for i in range(dias):
            fecha_actual = fecha_inicio + timedelta(days=i)
            año = fecha_actual.year
            mes = f"{fecha_actual.month:02d}"
            
            # Buscar archivos de Estados Cero para esta fecha
            dir_fecha = self.estados_cero_dir / str(año) / mes
            if dir_fecha.exists():
                for archivo in dir_fecha.glob(f"{fecha_actual.strftime('%d')}-*.md"):
                    estado = self._parsear_estado_cero(archivo)
                    if estado:
                        estados.append(estado)
        
        return estados
    
    def _parsear_estado_cero(self, archivo: Path) -> Optional[Dict]:
        """Parsea un archivo de Estado Cero"""
        try:
            contenido = archivo.read_text(encoding='utf-8')
            
            # Extraer metadata del frontmatter
            if contenido.startswith('---'):
                partes = contenido.split('---', 2)
                if len(partes) >= 3:
                    frontmatter = partes[1].strip()
                    cuerpo = partes[2].strip()
                    
                    # Parsear frontmatter simple
                    metadata = {}
                    for linea in frontmatter.split('\n'):
                        if ':' in linea:
                            key, value = linea.split(':', 1)
                            metadata[key.strip()] = value.strip()
                    
                    # Extraer información del cuerpo
                    estado = {
                        "archivo": str(archivo),
                        "fecha": metadata.get("fecha", ""),
                        "momento": metadata.get("momento", ""),
                        "tendencia": metadata.get("tendencia", ""),
                        "intensidad": float(metadata.get("intensidad", 0)),
                        "timestamp": metadata.get("timestamp", ""),
                        "contenido": cuerpo
                    }
                    
                    return estado
        except Exception as e:
            print(f"Error parseando {archivo}: {e}")
        
        return None
    
    def _analizar_patron_energia(self, estados: List[Dict]) -> PatronEnergia:
        """Analiza el patrón de energía en los Estados Cero"""
        if not estados:
            return PatronEnergia("equilibrio", 0.0, 0.0, "fajr")
        
        # Contar tendencias por momento
        tendencias_por_momento = {}
        intensidades = []
        
        for estado in estados:
            momento = estado.get("momento", "")
            tendencia = estado.get("tendencia", "")
            intensidad = estado.get("intensidad", 0)
            
            if momento not in tendencias_por_momento:
                tendencias_por_momento[momento] = []
            
            tendencias_por_momento[momento].append(tendencia)
            intensidades.append(intensidad)
        
        # Calcular tendencia predominante
        todas_tendencias = [estado.get("tendencia", "") for estado in estados]
        tendencia_predominante = max(set(todas_tendencias), key=todas_tendencias.count) if todas_tendencias else "equilibrio"
        
        # Calcular intensidad promedio
        intensidad_promedio = sum(intensidades) / len(intensidades) if len(intensidades) > 0 else 0.0
        
        # Calcular consistencia (qué tan seguido se repite la tendencia predominante)
        consistencia = todas_tendencias.count(tendencia_predominante) / len(todas_tendencias) if todas_tendencias else 0.0
        
        # Encontrar momento predominante
        momento_predominante = "fajr"
        max_apariciones = 0
        for momento, tendencias in tendencias_por_momento.items():
            if len(tendencias) > max_apariciones:
                max_apariciones = len(tendencias)
                momento_predominante = momento
        
        return PatronEnergia(
            tendencia=tendencia_predominante,
            intensidad=intensidad_promedio,
            consistencia=consistencia,
            momento_predominante=momento_predominante
        )
    
    def _detectar_conflictos_dominios(self, estados: List[Dict]) -> List[ConflictoDominio]:
        """Detecta conflictos entre dominios basándose en los Estados Cero"""
        conflictos = []
        
        # Análisis simple de conflictos basado en patrones
        tendencias_biologicas = []
        tendencias_espirituales = []
        tendencias_financieras = []
        
        for estado in estados:
            contenido = estado.get("contenido", "").lower()
            
            # Detectar menciones de dominios
            if any(palabra in contenido for palabra in ["cuerpo", "energía", "ejercicio", "movimiento", "salud"]):
                tendencias_biologicas.append(estado.get("tendencia", ""))
            
            if any(palabra in contenido for palabra in ["espíritu", "conexión", "propósito", "significado", "fe"]):
                tendencias_espirituales.append(estado.get("tendencia", ""))
            
            if any(palabra in contenido for palabra in ["dinero", "finanzas", "trabajo", "proyecto", "inversión"]):
                tendencias_financieras.append(estado.get("tendencia", ""))
        
        # Detectar conflicto entre dominios
        if tendencias_biologicas and tendencias_espirituales:
            bio_expansion = tendencias_biologicas.count("expansión") / len(tendencias_biologicas)
            esp_contraccion = tendencias_espirituales.count("contracción") / len(tendencias_espirituales)
            
            if abs(bio_expansion - esp_contraccion) > 0.6:
                conflictos.append(ConflictoDominio(
                    dominios=["biologico", "espiritual"],
                    tipo="energia",
                    intensidad=abs(bio_expansion - esp_contraccion),
                    recomendacion="Buscar equilibrio entre movimiento físico y quietud espiritual"
                ))
        
        return conflictos
    
    def _detectar_sinergias_dominios(self, estados: List[Dict]) -> List[SinergiaDominio]:
        """Detecta sinergias entre dominios"""
        sinergias = []
        
        # Análisis simple de sinergias
        for estado in estados:
            contenido = estado.get("contenido", "").lower()
            tendencia = estado.get("tendencia", "")
            
            # Sinergia: Expansión en múltiples dominios
            dominios_expansion = 0
            if any(palabra in contenido for palabra in ["cuerpo", "energía", "movimiento"]) and tendencia == "expansión":
                dominios_expansion += 1
            if any(palabra in contenido for palabra in ["espíritu", "conexión", "propósito"]) and tendencia == "expansión":
                dominios_expansion += 1
            if any(palabra in contenido for palabra in ["dinero", "trabajo", "proyecto"]) and tendencia == "expansión":
                dominios_expansion += 1
            
            if dominios_expansion >= 2:
                sinergias.append(SinergiaDominio(
                    dominios=["biologico", "espiritual", "financiero"],
                    tipo="amplificacion",
                    potencial=dominios_expansion / 3.0,
                    accion_sugerida="Aprovechar momento de expansión general para acciones significativas"
                ))
        
        return sinergias
    
    def _generar_acciones_emergentes(
        self, 
        estados: List[Dict], 
        patron_energia: PatronEnergia, 
        conflictos: List[ConflictoDominio],
        sinergias: List[SinergiaDominio]
    ) -> List[AccionEmergente]:
        """Genera acciones específicas basadas en el análisis de patrones"""
        acciones = []
        
        # Acción basada en patrón de energía
        if patron_energia.consistencia > 0.7:  # Patrón muy consistente
            if patron_energia.tendencia == "expansión":
                acciones.append(AccionEmergente(
                    tipo="inmediata",
                    dominio="general",
                    descripcion=f"Aprovechar patrón consistente de expansión en {patron_energia.momento_predominante}",
                    urgencia=0.8,
                    impacto_esperado=0.9,
                    recursos_requeridos=["tiempo", "energía"],
                    tiempo_estimado="2-3 horas",
                    indicadores_exito=["sensación de logro", "progreso visible", "energía mantenida"]
                ))
            elif patron_energia.tendencia == "contracción":
                acciones.append(AccionEmergente(
                    tipo="rutina",
                    dominio="espiritual",
                    descripcion="Establecer rutina de cuidado y reflexión durante momentos de contracción",
                    urgencia=0.6,
                    impacto_esperado=0.7,
                    recursos_requeridos=["espacio tranquilo", "tiempo"],
                    tiempo_estimado="30-45 min",
                    indicadores_exito=["sensación de calma", "claridad mental", "recuperación energética"]
                ))
        
        # Acciones basadas en conflictos
        for conflicto in conflictos:
            if conflicto.tipo == "energia":
                acciones.append(AccionEmergente(
                    tipo="planificada",
                    dominio=conflicto.dominios[0],
                    descripcion=f"Resolver conflicto energético entre {' y '.join(conflicto.dominios)}",
                    urgencia=conflicto.intensidad,
                    impacto_esperado=0.8,
                    recursos_requeridos=["tiempo", "atención", "experimentación"],
                    tiempo_estimado="1-2 semanas",
                    indicadores_exito=["equilibrio energético", "menos tensión", "flujo natural"]
                ))
        
        # Acciones basadas en sinergias
        for sinergia in sinergias:
            if sinergia.tipo == "amplificacion":
                acciones.append(AccionEmergente(
                    tipo="experimento",
                    dominio="general",
                    descripcion=f"Experimentar con sinergia de amplificación en dominios: {', '.join(sinergia.dominios)}",
                    urgencia=0.7,
                    impacto_esperado=sinergia.potencial,
                    recursos_requeridos=["creatividad", "tiempo", "atención"],
                    tiempo_estimado="1 semana",
                    indicadores_exito=["efectos multiplicadores", "mayor eficiencia", "satisfacción general"]
                ))
        
        return acciones
    
    def generar_reporte(self, analisis: Dict[str, Any]) -> str:
        """Genera un reporte de acciones en formato Markdown para Obsidian"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        reporte = f"""---
tipo: analisis-patrones
fecha: {date.today().isoformat()}
periodo: {analisis.get('periodo_analisis', 'N/A')}
total_estados: {analisis.get('total_estados', 0)}
timestamp: {timestamp}
---

# 🔍 Análisis de Patrones - {date.today().strftime("%d/%m/%Y")}

**Período analizado:** {analisis.get('periodo_analisis', 'N/A')}  
**Estados Cero analizados:** {analisis.get('total_estados', 0)}

## 🎯 Patrón de Energía

"""
        
        patron = analisis.get('patron_energia')
        if patron and hasattr(patron, 'tendencia'):
            reporte += f"""- **Tendencia predominante:** {patron.tendencia.title()}
- **Intensidad promedio:** {patron.intensidad:.1%}
- **Consistencia:** {patron.consistencia:.1%}
- **Momento más activo:** {patron.momento_predominante.upper()}

"""
        
        # Conflictos
        conflictos = analisis.get('conflictos_detectados', [])
        if conflictos:
            reporte += "## ⚠️ Conflictos Detectados\n\n"
            for conflicto in conflictos:
                reporte += f"""### {', '.join(conflicto.dominios).title()}
- **Tipo:** {conflicto.tipo}
- **Intensidad:** {conflicto.intensidad:.1%}
- **Recomendación:** {conflicto.recomendacion}

"""
        
        # Sinergias
        sinergias = analisis.get('sinergias_detectadas', [])
        if sinergias:
            reporte += "## ✨ Sinergias Detectadas\n\n"
            for sinergia in sinergias:
                reporte += f"""### {', '.join(sinergia.dominios).title()}
- **Tipo:** {sinergia.tipo}
- **Potencial:** {sinergia.potencial:.1%}
- **Acción sugerida:** {sinergia.accion_sugerida}

"""
        
        # Acciones emergentes
        acciones = analisis.get('acciones_emergentes', [])
        if acciones:
            reporte += "## 🎯 Acciones Emergentes\n\n"
            for i, accion in enumerate(acciones, 1):
                reporte += f"""### {i}. {accion.descripcion}
- **Tipo:** {accion.tipo.title()}
- **Dominio:** {accion.dominio.title()}
- **Urgencia:** {accion.urgencia:.1%}
- **Impacto esperado:** {accion.impacto_esperado:.1%}
- **Tiempo estimado:** {accion.tiempo_estimado}
- **Recursos requeridos:** {', '.join(accion.recursos_requeridos)}
- **Indicadores de éxito:**
"""
                for indicador in accion.indicadores_exito:
                    reporte += f"  - {indicador}\n"
                reporte += "\n"
        
        reporte += f"""---

*Análisis generado automáticamente por Campo Sagrado del Entrelazador - {timestamp}*
"""
        
        return reporte
    
    def guardar_reporte(self, analisis: Dict[str, Any]) -> str:
        """Guarda el reporte de análisis en Obsidian"""
        reporte = self.generar_reporte(analisis)
        
        # Crear directorio de análisis
        analisis_dir = self.vault_path / "Analisis-Patrones"
        analisis_dir.mkdir(exist_ok=True)
        
        # Guardar archivo
        fecha_str = date.today().strftime("%Y-%m-%d")
        archivo = analisis_dir / f"Analisis-Patrones-{fecha_str}.md"
        
        archivo.write_text(reporte, encoding='utf-8')
        
        return str(archivo)
