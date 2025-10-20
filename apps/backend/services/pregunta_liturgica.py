"""
Sistema de preguntas específicas por momento litúrgico
Preguntas binarias diseñadas para cada momento del día
"""

from typing import List, Dict
from enum import Enum


class MomentoLiturgico(str, Enum):
    FAJR = "fajr"       # Alba - Despertar
    DHUHR = "dhuhr"     # Mediodía - Expansión
    ASR = "asr"         # Tarde - Cumbre
    MAGHRIB = "maghrib" # Atardecer - Recogimiento
    ISHA = "isha"       # Noche - Integración


PREGUNTAS_POR_MOMENTO = {
    MomentoLiturgico.FAJR: [
        {
            "id": "fajr_1",
            "texto": "¿Mi cuerpo despertó con energía o necesita más descanso?",
            "dimension": "biologico",
            "polaridad": ["descanso", "energia"]
        },
        {
            "id": "fajr_2", 
            "texto": "¿Mi mente amanece clara o nebulosa?",
            "dimension": "conocimiento",
            "polaridad": ["nebulosa", "clara"]
        },
        {
            "id": "fajr_3",
            "texto": "¿Mi espíritu siente gratitud o resistencia al nuevo día?",
            "dimension": "espiritual",
            "polaridad": ["resistencia", "gratitud"]
        }
    ],
    MomentoLiturgico.DHUHR: [
        {
            "id": "dhuhr_1",
            "texto": "¿Mi energía está en su punto alto o necesito recarga?",
            "dimension": "biologico",
            "polaridad": ["recarga", "punto_alto"]
        },
        {
            "id": "dhuhr_2",
            "texto": "¿Mis acciones fluyen hacia creación o hacia mantenimiento?",
            "dimension": "financiero",
            "polaridad": ["mantenimiento", "creacion"]
        },
        {
            "id": "dhuhr_3",
            "texto": "¿Mi concentración está dispersa o enfocada?",
            "dimension": "conocimiento",
            "polaridad": ["dispersa", "enfocada"]
        }
    ],
    MomentoLiturgico.ASR: [
        {
            "id": "asr_1",
            "texto": "¿Mi cuerpo siente tensión o relajación?",
            "dimension": "biologico",
            "polaridad": ["tension", "relajacion"]
        },
        {
            "id": "asr_2",
            "texto": "¿Mis recursos se sienten escasos o abundantes?",
            "dimension": "financiero",
            "polaridad": ["escasos", "abundantes"]
        },
        {
            "id": "asr_3",
            "texto": "¿Mi propósito se siente difuso o nítido?",
            "dimension": "espiritual",
            "polaridad": ["difuso", "nitido"]
        }
    ],
    MomentoLiturgico.MAGHRIB: [
        {
            "id": "maghrib_1",
            "texto": "¿Mi cuerpo pide actividad o descanso?",
            "dimension": "biologico",
            "polaridad": ["actividad", "descanso"]
        },
        {
            "id": "maghrib_2",
            "texto": "¿Mi día se siente completo o incompleto?",
            "dimension": "espiritual",
            "polaridad": ["incompleto", "completo"]
        },
        {
            "id": "maghrib_3",
            "texto": "¿Mi balance hoy se inclina a dar o a recibir?",
            "dimension": "financiero",
            "polaridad": ["dar", "recibir"]
        }
    ],
    MomentoLiturgico.ISHA: [
        {
            "id": "isha_1",
            "texto": "¿Mi cuerpo está listo para descansar o aún activo?",
            "dimension": "biologico",
            "polaridad": ["activo", "descansar"]
        },
        {
            "id": "isha_2",
            "texto": "¿Mi aprendizaje hoy fue pasivo o activo?",
            "dimension": "conocimiento",
            "polaridad": ["pasivo", "activo"]
        },
        {
            "id": "isha_3",
            "texto": "¿Mi corazón cierra el día en paz o inquietud?",
            "dimension": "espiritual",
            "polaridad": ["inquietud", "paz"]
        }
    ]
}


class PreguntaLiturgica:
    """Gestiona preguntas específicas por momento litúrgico"""
    
    @staticmethod
    def obtener_preguntas(momento: MomentoLiturgico) -> List[Dict]:
        """Obtiene preguntas para un momento litúrgico específico"""
        return PREGUNTAS_POR_MOMENTO[momento]
    
    @staticmethod
    def calcular_dominio_activo(respuestas: List[Dict]) -> Dict[str, float]:
        """
        Calcula qué dominio está más activo según respuestas
        Retorna intensidad por dominio
        """
        dominios = {}
        for pregunta in respuestas:
            dim = pregunta['dimension']
            if dim not in dominios:
                dominios[dim] = []
            # Respuesta True = segunda polaridad (expansión)
            intensidad = 1.0 if pregunta['respuesta'] else 0.0
            dominios[dim].append(intensidad)
        
        return {
            dom: sum(vals) / len(vals) if len(vals) > 0 else 0.0
            for dom, vals in dominios.items()
        }

