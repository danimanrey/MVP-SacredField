"""
🏛️ API: GOBIERNO - 3 Poderes del Reino Divino

Endpoints para operar el gobierno del reino humano:
- LEGISLATIVO: Sultán (Corazón) emite decretos
- EJECUTIVO: Primer Ministro (Intelecto) organiza
- JUDICIAL: Escribano (Espíritu) verifica

Arquitectura Sagrada:
Los 3 Poderes operan en separación funcional pero unidad espiritual.

Referencia: core/arquitectura/TRES_PODERES_GOBIERNO_DIVINO.md
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from models.decreto_sacral import DecretoSacral
from models.database import get_db

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class EmitirDecretoRequest(BaseModel):
    """Request para emitir decreto (PODER LEGISLATIVO)"""
    direccion_emergente: str
    accion_tangible: str
    momento_liturgico: str = "fajr"
    validado_contra_pilares: bool = False


class EmitirDecretoResponse(BaseModel):
    """Response al emitir decreto"""
    success: bool
    decreto_id: int
    mensaje: str


class EstadoGobiernoResponse(BaseModel):
    """Estado de los 3 Poderes"""
    legislativo: Dict[str, Any]
    ejecutivo: Dict[str, Any]
    judicial: Dict[str, Any]


# ============================================================================
# PODER LEGISLATIVO: EL SULTÁN (Qalb/Corazón)
# ============================================================================

@router.post("/legislativo/decreto", response_model=EmitirDecretoResponse)
async def emitir_decreto(
    request: EmitirDecretoRequest,
    db: Session = Depends(get_db)
):
    """
    🕌 PODER LEGISLATIVO: Sultán emite decreto
    
    El Sultán (Corazón) RECIBE dirección en Estado Cero
    y EMITE decreto claro para el día/semana.
    
    Este decreto es LEY para el Poder Ejecutivo.
    
    Flow:
    1. Usuario realiza Estado Cero
    2. Recibe dirección emergente
    3. Formula acción tangible
    4. Valida contra 8 Pilares
    5. EMITE decreto
    """
    try:
        # Verificar que no haya decreto activo para hoy
        decreto_existente = db.query(DecretoSacral).filter(
            DecretoSacral.fecha == date.today(),
            DecretoSacral.esta_activo
        ).first()
        
        if decreto_existente:
            raise HTTPException(
                status_code=400,
                detail="Ya existe decreto activo para hoy. Un solo decreto por día."
            )
        
        # Crear nuevo decreto
        decreto = DecretoSacral(
            fecha=date.today(),
            momento_liturgico=request.momento_liturgico,
            direccion_emergente=request.direccion_emergente,
            accion_tangible=request.accion_tangible,
            validado_contra_pilares=request.validado_contra_pilares,
            estado="pendiente"
        )
        
        db.add(decreto)
        db.commit()
        db.refresh(decreto)
        
        return EmitirDecretoResponse(
            success=True,
            decreto_id=decreto.id,
            mensaje=f"🕌 Decreto emitido: {decreto.accion_tangible}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PODER EJECUTIVO: EL PRIMER MINISTRO (Aql/Intelecto)
# ============================================================================

@router.post("/ejecutivo/iniciar")
async def iniciar_ejecucion(db: Session = Depends(get_db)):
    """
    💼 PODER EJECUTIVO: Primer Ministro inicia ejecución
    
    El Primer Ministro (Intelecto) NO PUEDE actuar sin decreto del Sultán.
    
    Este endpoint:
    1. Verifica que existe decreto del día
    2. Inicia ejecución
    3. Retorna jornada a organizar
    
    Si no hay decreto → ERROR (debe realizar Estado Cero primero)
    """
    try:
        # Buscar decreto del día
        decreto = db.query(DecretoSacral).filter(
            DecretoSacral.fecha == date.today(),
            DecretoSacral.estado == "pendiente"
        ).first()
        
        if not decreto:
            raise HTTPException(
                status_code=400,
                detail="No hay decreto del Sultán para hoy. Debe realizar Estado Cero primero."
            )
        
        # Iniciar ejecución
        decreto.iniciar_ejecucion()
        db.commit()
        
        return {
            "success": True,
            "mensaje": "Ejecución iniciada por Primer Ministro",
            "decreto": {
                "id": decreto.id,
                "accion": decreto.accion_tangible,
                "direccion": decreto.direccion_emergente
            },
            "siguiente_paso": "Consultar Gabinete Ministerial y organizar jornada"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ejecutivo/completar")
async def completar_ejecucion(
    notas: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    💼 PODER EJECUTIVO: Primer Ministro completa ejecución
    
    Marca el decreto como completado.
    """
    try:
        decreto = db.query(DecretoSacral).filter(
            DecretoSacral.fecha == date.today(),
            DecretoSacral.estado == "en_ejecucion"
        ).first()
        
        if not decreto:
            raise HTTPException(
                status_code=404,
                detail="No hay decreto en ejecución para completar"
            )
        
        decreto.completar_ejecucion(notas)
        db.commit()
        
        return {
            "success": True,
            "mensaje": "Decreto completado",
            "siguiente_paso": "Espejo Nocturno (Poder Judicial)"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PODER JUDICIAL: EL ESCRIBANO (Rūḥ/Espíritu)
# ============================================================================

@router.post("/judicial/espejo-nocturno")
async def espejo_nocturno(
    cumplimiento_score: int,
    verificacion: str,
    sabiduria: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    📜 PODER JUDICIAL: Escribano verifica cumplimiento
    
    El Escribano (Espíritu) OBSERVA sin juicio moral,
    DOCUMENTA objetivamente, EXTRAE sabiduría.
    
    Espejo Nocturno:
    1. Revisa decreto del día
    2. Evalúa cumplimiento (0-100)
    3. Registra observaciones
    4. Extrae sabiduría
    5. Cierra ciclo con gratitud
    """
    try:
        decreto = db.query(DecretoSacral).filter(
            DecretoSacral.fecha == date.today()
        ).first()
        
        if not decreto:
            raise HTTPException(
                status_code=404,
                detail="No hay decreto del día para verificar"
            )
        
        # Registrar verificación
        decreto.registrar_verificacion(
            verificacion=verificacion,
            cumplimiento_score=cumplimiento_score,
            sabiduria=sabiduria
        )
        db.commit()
        
        return {
            "success": True,
            "mensaje": "Espejo Nocturno completado",
            "cumplimiento": cumplimiento_score,
            "fue_cumplido": decreto.fue_cumplido,
            "sabiduria": sabiduria
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ESTADO GENERAL DEL GOBIERNO
# ============================================================================

@router.get("/estado", response_model=EstadoGobiernoResponse)
async def estado_gobierno(db: Session = Depends(get_db)):
    """
    🏛️ Estado de los 3 Poderes del Gobierno Divino
    
    Retorna estado actual de:
    - LEGISLATIVO: ¿Decreto emitido?
    - EJECUTIVO: ¿Jornada organizada/ejecutándose?
    - JUDICIAL: ¿Verificación realizada?
    """
    try:
        decreto = db.query(DecretoSacral).filter(
            DecretoSacral.fecha == date.today()
        ).first()
        
        if not decreto:
            return EstadoGobiernoResponse(
                legislativo={
                    "decreto_emitido": False,
                    "mensaje": "Pendiente Estado Cero"
                },
                ejecutivo={
                    "jornada_organizada": False,
                    "mensaje": "Esperando decreto del Sultán"
                },
                judicial={
                    "verificacion_realizada": False,
                    "mensaje": "Pendiente para Isha (noche)"
                }
            )
        
        return EstadoGobiernoResponse(
            legislativo={
                "decreto_emitido": True,
                "decreto": decreto.accion_tangible,
                "momento": decreto.momento_liturgico,
                "validado_pilares": decreto.validado_contra_pilares
            },
            ejecutivo={
                "jornada_organizada": decreto.estado == "en_ejecucion",
                "estado": decreto.estado,
                "notas": decreto.notas_ejecucion
            },
            judicial={
                "verificacion_realizada": decreto.tiene_verificacion,
                "cumplimiento": decreto.cumplimiento_score,
                "fue_cumplido": decreto.fue_cumplido
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/historia")
async def historia_decretos(
    limit: int = 30,
    db: Session = Depends(get_db)
):
    """
    📚 Historia de decretos emitidos
    
    Retorna últimos N decretos con sus estados.
    """
    try:
        decretos = db.query(DecretoSacral).order_by(
            DecretoSacral.fecha.desc()
        ).limit(limit).all()
        
        return {
            "decretos": [
                {
                    "id": d.id,
                    "fecha": d.fecha.isoformat(),
                    "accion": d.accion_tangible,
                    "estado": d.estado,
                    "cumplimiento": d.cumplimiento_score,
                    "fue_cumplido": d.fue_cumplido
                }
                for d in decretos
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

