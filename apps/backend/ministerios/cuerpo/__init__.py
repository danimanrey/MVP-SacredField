"""
💪 MINISTERIO DEL CUERPO
Al-Ḥayy (الحَيّ) - El Viviente

Dimensión Existencial: Vitalidad, salud física, energía
Pregunta: "¿Qué necesita mi templo?"

Responsabilidades:
- Mantenimiento de salud y vitalidad
- Gestión de energía disponible
- Movimiento y actividad física
- Descanso y regeneración
- Ritmos circadianos y litúrgicos

Referencia: core/arquitectura/MAPEO_7_MINISTERIOS.md
"""

from typing import Dict, Any
from datetime import datetime
from ministerios import MinisterioBase

__all__ = ["MinisterioCuerpo"]


class MinisterioCuerpo(MinisterioBase):
    """
    Ministerio del Cuerpo - Al-Ḥayy (El Viviente).
    
    Gestiona salud física, energía, ritmos biológicos.
    """
    
    def __init__(self):
        # Lazy imports para evitar dependencias circulares
        self._tiempos_liturgicos = None
        self._calendario_hijri = None
    
    @property
    def nombre_divino(self) -> str:
        return "Al-Ḥayy (الحَيّ) - El Viviente"
    
    @property
    def pregunta_existencial(self) -> str:
        return "¿Qué necesita mi templo?"
    
    def estado_actual(self) -> Dict[str, Any]:
        """
        Estado biológico actual del usuario.
        
        Integra:
        - models/estado_biologico.py
        - services/tiempos_liturgicos.py
        - services/calendario_hijri.py
        """
        return {
            "energia_actual": 75.0,  # 0-100
            "horas_sueno_ultima_noche": 7.5,
            "ejercicio_hoy": False,
            "momento_liturgico_actual": self._momento_liturgico_actual(),
            "fase_lunar": self._fase_lunar_actual()
        }
    
    def responder_a_decreto(self, decreto) -> Dict[str, Any]:
        """
        Responde al decreto desde perspectiva biológica.
        
        Si el decreto requiere energía alta pero el cuerpo está cansado,
        el ministerio advierte y sugiere ajustes.
        """
        estado = self.estado_actual()
        
        # TODO: Analizar decreto vs energía disponible
        if estado["energia_actual"] < 50:
            return {
                "advertencia": "Energía baja para decreto",
                "sugerencia": "Considerar ajustar timing o reducir scope",
                "status": "warning"
            }
        
        return {"status": "ok"}
    
    def metricas_salud(self) -> Dict[str, float]:
        """
        Salud física del usuario (0-100).
        """
        return {
            "energia": 75.0,
            "descanso": 80.0,
            "movimiento": 60.0,
            "ritmo_circadiano": 85.0,
            "alineacion_liturgica": 90.0
        }
    
    def _momento_liturgico_actual(self) -> str:
        """
        Calcula momento litúrgico actual (Fajr, Dhuhr, Asr, Maghrib, Isha).
        
        TODO: Integrar con services/tiempos_liturgicos.py
        """
        hora = datetime.now().hour
        if 5 <= hora < 12:
            return "fajr-dhuhr"
        elif 12 <= hora < 15:
            return "dhuhr-asr"
        elif 15 <= hora < 18:
            return "asr-maghrib"
        elif 18 <= hora < 21:
            return "maghrib-isha"
        else:
            return "isha-fajr"
    
    def _fase_lunar_actual(self) -> str:
        """
        Calcula fase lunar actual.
        
        TODO: Integrar con services/calendario_hijri.py
        """
        return "creciente"  # Placeholder

