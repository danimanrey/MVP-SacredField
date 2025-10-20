"""
🏛️ API: PILARES - Verificación de Arquitectura Sagrada

Endpoints para verificar que decisiones y acciones
honran los 8 Pilares Fundamentales.

Referencia: core/pilares/
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

from services.verificador_pilares import obtener_verificador

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class VerificarDecisionRequest(BaseModel):
    """Request para verificar decisión contra pilares"""
    decision: Dict[str, Any]
    contexto: Optional[Dict[str, Any]] = None


class ResultadoPilarResponse(BaseModel):
    """Resultado de verificar un pilar"""
    pilar: str
    score: float
    cumple: bool
    fortalezas: List[str]
    violaciones: List[str]
    recomendaciones: List[str]


class VerificacionCompletaResponse(BaseModel):
    """Resultado de verificar todos los pilares"""
    score_global: float
    pilares_cumplidos: int
    total_pilares: int
    cumple_arquitectura: bool
    resultados: List[ResultadoPilarResponse]
    timestamp: str


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/verificar", response_model=VerificacionCompletaResponse)
async def verificar_contra_pilares(request: VerificarDecisionRequest):
    """
    🏛️ Verifica decisión contra los 8 Pilares Fundamentales
    
    Valida que una decisión honre la arquitectura sagrada.
    
    Ejemplo de uso:
    ```json
    {
      "decision": {
        "accion_especifica": "Implementar feature X",
        "descripcion": "...",
        "tipo": "creacion",
        "crea_dependencia_externa": false,
        "comprende_implicaciones": true
      }
    }
    ```
    
    Returns:
        Score global 0-100 y resultados por pilar
    """
    try:
        verificador = obtener_verificador()
        resultado = verificador.verificar_todos_pilares(
            request.decision,
            request.contexto
        )
        
        return VerificacionCompletaResponse(**resultado)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verificar/{pilar_id}")
async def verificar_pilar_especifico(
    pilar_id: int,
    request: VerificarDecisionRequest
):
    """
    Verifica decisión contra un pilar específico.
    
    pilar_id:
        1 = Pureza Operativa
        2 = Soberanía Creativa
        3 = Responsabilidad Consciente
        4-8 = Otros pilares
    """
    try:
        verificador = obtener_verificador()
        
        if pilar_id == 1:
            resultado = verificador.verificar_pureza_operativa(
                request.decision,
                request.contexto
            )
        elif pilar_id == 2:
            resultado = verificador.verificar_soberania_creativa(
                request.decision,
                request.contexto
            )
        elif pilar_id == 3:
            resultado = verificador.verificar_responsabilidad_consciente(
                request.decision,
                request.contexto
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Pilar {pilar_id} no tiene verificador específico aún"
            )
        
        return {
            "pilar": resultado.pilar_nombre,
            "score": resultado.score,
            "cumple": resultado.cumple,
            "fortalezas": resultado.fortalezas,
            "violaciones": resultado.violaciones,
            "recomendaciones": resultado.recomendaciones
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def info_pilares():
    """
    📚 Información sobre los 8 Pilares Fundamentales
    """
    return {
        "pilares": [
            {
                "id": 1,
                "nombre": "Pureza Operativa",
                "pregunta": "¿Es lo más simple y directo?",
                "referencia": "core/pilares/01-pureza-operativa.md"
            },
            {
                "id": 2,
                "nombre": "Soberanía Creativa",
                "pregunta": "¿Amplifica mi libertad?",
                "referencia": "core/pilares/02-soberania-creativa.md"
            },
            {
                "id": 3,
                "nombre": "Responsabilidad Consciente",
                "pregunta": "¿Asumo propiedad total?",
                "referencia": "core/pilares/03-responsabilidad-consciente.md"
            },
            {
                "id": 4,
                "nombre": "Expresión Auténtica",
                "pregunta": "¿Refleja mi singularidad?",
                "referencia": "core/pilares/04-expresion-autentica.md"
            },
            {
                "id": 5,
                "nombre": "Implementación Técnica",
                "pregunta": "¿Es técnicamente viable y modular?",
                "referencia": "core/pilares/05-implementacion-tecnica.md"
            },
            {
                "id": 6,
                "nombre": "Contribución Ecosistémica",
                "pregunta": "¿Sirve al ecosistema?",
                "referencia": "core/pilares/06-contribucion-ecosistemica.md"
            },
            {
                "id": 7,
                "nombre": "Sabiduría Integrada",
                "pregunta": "¿Integra dimensión sagrada?",
                "referencia": "core/pilares/07-sabiduria-integrada.md"
            },
            {
                "id": 8,
                "nombre": "Evolución Continua",
                "pregunta": "¿Permite crecimiento?",
                "referencia": "core/pilares/08-evolucion-continua.md"
            }
        ],
        "criterio_cumplimiento": "Score >= 70 por pilar, mínimo 6 de 8 pilares cumplidos"
    }

