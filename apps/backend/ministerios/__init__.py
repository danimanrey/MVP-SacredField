"""
🏛️ MINISTERIOS DEL CAMPO SAGRADO

Los 7 Ministerios representan las dimensiones irreducibles 
de la vida humana consciente.

Cada ministerio refleja un Nombre Divino y gestiona 
un territorio existencial específico.

Organización:
  - mente/      → Al-'Alīm (El Conocedor) 🧠
  - cuerpo/     → Al-Ḥayy (El Viviente) 💪
  - capital/    → Ar-Razzāq (El Proveedor) 💰
  - conexion/   → Al-Wadūd (El Amoroso) 🤝
  - creacion/   → Al-Khāliq (El Creador) 🎨
  - significado/ → Al-Hādī (El Guía) 🧭
  - soberania/  → Al-Malik (El Soberano) 👑

Referencia: core/arquitectura/MAPEO_7_MINISTERIOS.md
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

__all__ = [
    "MinisterioBase",
    "GabineteMinisterial"
]


class MinisterioBase(ABC):
    """
    Interfaz base que todos los ministerios deben implementar.
    
    Cada ministerio:
    - Refleja un Nombre Divino
    - Tiene un estado actual
    - Responde a decretos del Sultán
    - Reporta métricas de salud
    """
    
    @property
    @abstractmethod
    def nombre_divino(self) -> str:
        """Nombre Divino que este ministerio refleja"""
        pass
    
    @property
    @abstractmethod
    def pregunta_existencial(self) -> str:
        """Pregunta que este ministerio responde"""
        pass
    
    @abstractmethod
    def estado_actual(self) -> Dict[str, Any]:
        """
        Estado actual del ministerio.
        
        Returns:
            Dict con información relevante del estado
        """
        pass
    
    @abstractmethod
    def responder_a_decreto(self, decreto) -> Dict[str, Any]:
        """
        Cómo este ministerio responde al decreto del Sultán.
        
        Args:
            decreto: DecretoSacral del día/semana
            
        Returns:
            Dict con respuesta, advertencias, sugerencias
        """
        pass
    
    @abstractmethod
    def metricas_salud(self) -> Dict[str, float]:
        """
        Métricas de salud del ministerio (0-100).
        
        Returns:
            Dict con métricas específicas del ministerio
        """
        pass


class GabineteMinisterial:
    """
    Coordina los 7 Ministerios del Campo Sagrado.
    
    El Gabinete Ministerial:
    - Convoca reuniones ministeriales
    - Detecta conflictos entre ministerios
    - Propone coordinación inter-ministerial
    - Asegura atención equilibrada a todos
    
    Uso:
        gabinete = GabineteMinisterial()
        reunion = gabinete.reunion_ministerial(decreto)
    """
    
    def __init__(self):
        """
        Inicializa el Gabinete Ministerial.
        
        NOTA: Los ministerios individuales se importarán dinámicamente
        cuando estén implementados para evitar dependencias circulares.
        """
        self._ministerios_activos: Dict[str, MinisterioBase] = {}
    
    def registrar_ministerio(self, nombre: str, ministerio: MinisterioBase):
        """
        Registra un ministerio en el gabinete.
        
        Args:
            nombre: Nombre del ministerio (ej: "mente", "cuerpo")
            ministerio: Instancia del ministerio
        """
        self._ministerios_activos[nombre] = ministerio
    
    def reunion_ministerial(self, decreto) -> Dict[str, Any]:
        """
        Convoca reunión ministerial para responder a decreto del Sultán.
        
        Cada ministro:
        1. Reporta su estado actual
        2. Responde al decreto
        3. Reporta métricas de salud
        
        Args:
            decreto: DecretoSacral a responder
            
        Returns:
            Dict con reportes de cada ministerio, conflictos detectados,
            y propuestas de coordinación
        """
        reportes = {}
        
        for nombre, ministerio in self._ministerios_activos.items():
            try:
                reportes[nombre] = {
                    "nombre_divino": ministerio.nombre_divino,
                    "pregunta": ministerio.pregunta_existencial,
                    "estado": ministerio.estado_actual(),
                    "respuesta_decreto": ministerio.responder_a_decreto(decreto),
                    "metricas": ministerio.metricas_salud()
                }
            except Exception as e:
                reportes[nombre] = {
                    "error": f"Error al consultar ministerio: {str(e)}"
                }
        
        # Detectar conflictos inter-ministeriales
        conflictos = self._detectar_conflictos(reportes)
        
        # Proponer coordinación
        coordinacion = self._proponer_coordinacion(conflictos, reportes)
        
        return {
            "reportes": reportes,
            "conflictos": conflictos,
            "coordinacion": coordinacion,
            "ministerios_activos": len(self._ministerios_activos),
            "salud_global": self._calcular_salud_global(reportes)
        }
    
    def _detectar_conflictos(self, reportes: Dict[str, Any]) -> list[str]:
        """
        Detecta conflictos entre ministerios.
        
        Ejemplos de conflictos:
        - CREACIÓN requiere 8h pero CUERPO tiene energía baja
        - CAPITAL tiene runway crítico pero CREACIÓN planea sin generar ingresos
        - CONEXIÓN requiere tiempo pero SOBERANÍA requiere aislamiento
        """
        conflictos = []
        
        # TODO: Implementar lógica de detección de conflictos
        # Por ahora, retornar lista vacía
        
        return conflictos
    
    def _proponer_coordinacion(
        self, 
        conflictos: list[str], 
        reportes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Propone coordinación entre ministerios para resolver conflictos.
        """
        if not conflictos:
            return {"tipo": "sin_conflictos"}
        
        # TODO: Implementar lógica de coordinación
        return {
            "tipo": "coordinacion_necesaria",
            "sugerencias": []
        }
    
    def _calcular_salud_global(self, reportes: Dict[str, Any]) -> float:
        """
        Calcula salud global del sistema (promedio de ministerios).
        
        Returns:
            Score 0-100
        """
        if not reportes:
            return 0.0
        
        metricas_validas = []
        for reporte in reportes.values():
            if "metricas" in reporte and isinstance(reporte["metricas"], dict):
                # Promedio de métricas del ministerio
                valores = [v for v in reporte["metricas"].values() if isinstance(v, (int, float))]
                if valores:
                    metricas_validas.append(sum(valores) / len(valores))
        
        if not metricas_validas:
            return 0.0
        
        return sum(metricas_validas) / len(metricas_validas)


# Instancia global del gabinete (singleton)
_gabinete_global: Optional[GabineteMinisterial] = None


def obtener_gabinete() -> GabineteMinisterial:
    """
    Obtiene la instancia global del Gabinete Ministerial.
    
    Returns:
        GabineteMinisterial singleton
    """
    global _gabinete_global
    if _gabinete_global is None:
        _gabinete_global = GabineteMinisterial()
    return _gabinete_global

