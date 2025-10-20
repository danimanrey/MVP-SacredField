"""
💰 MINISTERIO DEL CAPITAL
Ar-Razzāq (الرزّاق) - El Proveedor

Dimensión Existencial: Recursos materiales, soberanía económica
Pregunta: "¿Qué recursos necesito generar?"

Responsabilidades:
- Generación de recursos materiales
- Gestión de abundancia
- Independencia económica
- Intercambio de valor

Referencia: core/arquitectura/MAPEO_7_MINISTERIOS.md
"""

from typing import Dict, Any
from ministerios import MinisterioBase

__all__ = ["MinisterioCapital"]


class MinisterioCapital(MinisterioBase):
    """
    Ministerio del Capital - Ar-Razzāq (El Proveedor).
    
    Gestiona recursos materiales, flujo de abundancia,
    y soberanía económica.
    
    NOTA: Este ministerio está POCO DESARROLLADO en MVP actual.
    Implementación futura en v2.0.
    """
    
    @property
    def nombre_divino(self) -> str:
        return "Ar-Razzāq (الرزّاق) - El Proveedor"
    
    @property
    def pregunta_existencial(self) -> str:
        return "¿Qué recursos necesito generar?"
    
    def estado_actual(self) -> Dict[str, Any]:
        """
        Estado financiero actual del usuario.
        
        TODO: Integrar con configuración: contexto_financiero
        """
        return {
            "runway_meses": 6,  # De configuración
            "urgencia_financiera": False,
            "flujo_actual": "estable",  # estable, creciente, decreciente, crítico
            "proyectos_generadores": []
        }
    
    def responder_a_decreto(self, decreto) -> Dict[str, Any]:
        """
        Responde al decreto desde perspectiva financiera.
        
        Si el decreto requiere inversión pero runway es bajo,
        el ministerio advierte.
        """
        estado = self.estado_actual()
        
        if estado["runway_meses"] < 3:
            return {
                "advertencia": "Runway crítico (<3 meses)",
                "sugerencia": "Priorizar generación de ingresos",
                "status": "critical"
            }
        
        return {"status": "ok"}
    
    def metricas_salud(self) -> Dict[str, float]:
        """
        Salud financiera del usuario (0-100).
        """
        return {
            "abundancia": 60.0,
            "flujo_recursos": 70.0,
            "independencia_economica": 65.0,
            "generosidad": 50.0
        }

