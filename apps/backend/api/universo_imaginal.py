"""
🌌 API - Universo Imaginal
===========================

Endpoints para visualizar el knowledge graph de Obsidian como universo de estrellas
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import os

# from services.universo_processor import UniversoProcessor  # Archivado en Phase 3
from models.universo import (
    UniversoImaginal, ObtenerEstrellasRequest, ObtenerOrbitasRequest,
    EstadisticasUniverso
)


router = APIRouter()

# Configuración
VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "/Users/hp/Campo sagrado MVP/obsidian_vault")


@router.get("/test")
async def test_endpoint():
    """Test de conectividad"""
    return {
        "status": "ok",
        "message": "Universo Imaginal API funcionando",
        "vault_path": VAULT_PATH
    }


@router.get("/universo")
async def obtener_universo_completo(
    tipo: str = "individual",
    owner_id: str = "default"
):
    """
    Obtiene el universo imaginal completo
    
    Incluye:
    - Todas las estrellas (notas de Obsidian)
    - Constelaciones identificadas
    - Estadísticas del grafo
    """
    try:
        processor = UniversoProcessor(VAULT_PATH)
        universo = processor.generar_universo(tipo=tipo, owner_id=owner_id)
        
        return universo
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando universo: {str(e)}"
        )


@router.get("/estrellas")
async def obtener_estrellas(
    dimension: Optional[str] = None,
    min_enlaces: Optional[int] = None,
    solo_hubs: bool = False,
    solo_orphans: bool = False
):
    """
    Obtiene lista de estrellas (notas) filtradas
    
    Parámetros:
    - dimension: Filtrar por dimensión específica
    - min_enlaces: Solo estrellas con al menos N enlaces
    - solo_hubs: Solo estrellas muy conectadas (>= 3 enlaces)
    - solo_orphans: Solo estrellas sin conexiones
    """
    try:
        processor = UniversoProcessor(VAULT_PATH)
        universo = processor.generar_universo()
        
        estrellas = universo.grafo_conocimiento.estrellas
        
        # Filtrar por dimensión
        if dimension:
            estrellas = [e for e in estrellas if e.dimension == dimension]
        
        # Filtrar por número de enlaces
        if min_enlaces:
            estrellas = [e for e in estrellas if e.num_enlaces >= min_enlaces]
        
        # Solo hubs
        if solo_hubs:
            estrellas = [e for e in estrellas if e.num_enlaces >= 3]
        
        # Solo orphans
        if solo_orphans:
            estrellas = [e for e in estrellas if e.num_enlaces == 0]
        
        return {
            "total": len(estrellas),
            "estrellas": estrellas
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo estrellas: {str(e)}"
        )


@router.get("/estrellas/{estrella_id}")
async def obtener_estrella_detalle(estrella_id: str):
    """
    Obtiene detalle completo de una estrella específica
    Incluye contenido completo y conexiones
    """
    try:
        processor = UniversoProcessor(VAULT_PATH)
        universo = processor.generar_universo()
        
        # Buscar estrella
        estrella = next(
            (e for e in universo.grafo_conocimiento.estrellas if e.id == estrella_id),
            None
        )
        
        if not estrella:
            raise HTTPException(status_code=404, detail="Estrella no encontrada")
        
        # Obtener nota completa
        from services.obsidian_parser import ObsidianParser
        parser = ObsidianParser(VAULT_PATH)
        notas = parser.listar_notas()
        nota = next((n for n in notas if n.filepath == estrella_id), None)
        
        if nota:
            return {
                **estrella.dict(),
                "contenido_completo": nota.contenido,
                "metadata_completa": nota.metadata
            }
        
        return estrella
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo detalle: {str(e)}"
        )


@router.get("/constelaciones")
async def obtener_constelaciones(
    dimension: Optional[str] = None,
    min_estrellas: int = 2
):
    """
    Obtiene lista de constelaciones (clusters de notas relacionadas)
    
    Parámetros:
    - dimension: Filtrar por dimensión principal
    - min_estrellas: Mínimo de estrellas en la constelación
    """
    try:
        processor = UniversoProcessor(VAULT_PATH)
        universo = processor.generar_universo()
        
        constelaciones = universo.grafo_conocimiento.constelaciones
        
        # Filtrar por dimensión
        if dimension:
            constelaciones = [
                c for c in constelaciones 
                if c.dimension_principal == dimension
            ]
        
        # Filtrar por tamaño
        constelaciones = [
            c for c in constelaciones 
            if len(c.estrellas) >= min_estrellas
        ]
        
        return {
            "total": len(constelaciones),
            "constelaciones": constelaciones
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo constelaciones: {str(e)}"
        )


@router.get("/estadisticas")
async def obtener_estadisticas():
    """
    Obtiene estadísticas generales del universo imaginal
    """
    try:
        processor = UniversoProcessor(VAULT_PATH)
        universo = processor.generar_universo()
        
        return universo.estadisticas
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo estadísticas: {str(e)}"
        )


@router.get("/balance-dimensiones")
async def obtener_balance_dimensiones():
    """
    Obtiene el balance de dimensiones (distribución del arcoíris)
    """
    try:
        processor = UniversoProcessor(VAULT_PATH)
        universo = processor.generar_universo()
        
        balance = universo.grafo_conocimiento.dimensiones_balance
        total = sum(balance.values())
        
        # Calcular porcentajes
        balance_porcentajes = {}
        for dimension, count in balance.items():
            porcentaje = (count / total * 100) if total > 0 else 0
            balance_porcentajes[dimension] = {
                "count": count,
                "porcentaje": round(porcentaje, 1)
            }
        
        # Identificar dimensiones desbalanceadas
        promedio = total / 7 if total > 0 else 0
        desbalances = {}
        
        for dimension in ['finanzas', 'biologia', 'conocimiento', 'desarrollo', 
                         'relaciones', 'creatividad', 'espiritualidad']:
            count = balance.get(dimension, 0)
            diferencia = count - promedio
            
            if abs(diferencia) > promedio * 0.5:  # >50% de diferencia
                if diferencia > 0:
                    desbalances[dimension] = "sobrerepresentada"
                else:
                    desbalances[dimension] = "subrepresentada"
        
        return {
            "balance": balance_porcentajes,
            "total_estrellas": total,
            "promedio_por_dimension": round(promedio, 1),
            "desbalances": desbalances,
            "recomendacion": generar_recomendacion_balance(desbalances)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo balance: {str(e)}"
        )


def generar_recomendacion_balance(desbalances: dict) -> str:
    """Genera recomendación textual sobre el balance"""
    if not desbalances:
        return "Tu espectro está equilibrado. Todas las dimensiones tienen representación similar."
    
    sobre = [d for d, tipo in desbalances.items() if tipo == "sobrerepresentada"]
    sub = [d for d, tipo in desbalances.items() if tipo == "subrepresentada"]
    
    msg = []
    
    if sobre:
        msg.append(f"Dimensiones con mucha atención: {', '.join(sobre)}.")
    
    if sub:
        msg.append(f"Dimensiones que necesitan más atención: {', '.join(sub)}.")
    
    return " ".join(msg)


@router.get("/hubs")
async def obtener_hubs(top: int = 10):
    """
    Obtiene las estrellas más conectadas (hubs de conocimiento)
    """
    try:
        processor = UniversoProcessor(VAULT_PATH)
        universo = processor.generar_universo()
        
        estrellas = universo.grafo_conocimiento.estrellas
        
        # Ordenar por número de enlaces
        hubs = sorted(estrellas, key=lambda e: e.num_enlaces, reverse=True)[:top]
        
        return {
            "total_hubs": len([e for e in estrellas if e.num_enlaces >= 3]),
            "top_hubs": hubs
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo hubs: {str(e)}"
        )


@router.get("/orphans")
async def obtener_orphans():
    """
    Obtiene estrellas huérfanas (sin conexiones)
    Estas son oportunidades de integración
    """
    try:
        processor = UniversoProcessor(VAULT_PATH)
        universo = processor.generar_universo()
        
        estrellas = universo.grafo_conocimiento.estrellas
        orphans = [e for e in estrellas if e.num_enlaces == 0]
        
        return {
            "total": len(orphans),
            "orphans": orphans,
            "sugerencia": "Estas notas no están conectadas. Considera añadir enlaces [[]] para integrarlas en tu conocimiento."
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo orphans: {str(e)}"
        )


@router.post("/regenerar")
async def regenerar_universo():
    """
    Regenera el universo imaginal
    (En producción, esto se haría automáticamente con webhooks de Obsidian)
    """
    try:
        processor = UniversoProcessor(VAULT_PATH)
        universo = processor.generar_universo()
        
        return {
            "status": "regenerado",
            "fecha": universo.fecha_actualizacion,
            "total_estrellas": len(universo.grafo_conocimiento.estrellas),
            "total_constelaciones": len(universo.grafo_conocimiento.constelaciones)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error regenerando universo: {str(e)}"
        )

