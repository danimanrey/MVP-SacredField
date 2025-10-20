"""
🎵 API - Ley de la Octava
==========================

Endpoints para gestionar objetivos según la Ley de la Octava.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import Optional

from services.gestor_octavas import GestorOctavas
from models.ley_octava import (
    ObjetivoOctava, DimensionOctava, TipoShock,
    DiaSemanaOctava, CORRESPONDENCIAS_OCTAVA
)


router = APIRouter()

# Gestor global (en producción sería persistente en DB)
gestor = GestorOctavas()


class CrearObjetivoRequest(BaseModel):
    """Request para crear un nuevo objetivo con estructura de octava"""
    nombre: str
    descripcion: str
    dimension_primaria: str  # espiritual, biologico, financiero, etc.
    fecha_objetivo: str  # YYYY-MM-DD
    practica_diaria: str
    resultado_observable: str


class AplicarShockRequest(BaseModel):
    """Request para aplicar un shock consciente"""
    tipo_shock: str  # revision_profunda, celebracion_integracion
    notas: str  # Reflexiones del usuario


@router.get("/correspondencias")
async def obtener_correspondencias():
    """
    Obtiene todas las correspondencias de la Ley de la Octava.
    
    Retorna:
    - 7 notas con sus correspondencias
    - Días de la semana
    - Dimensiones
    - Colores
    - Frecuencias
    - Intervalos críticos
    """
    correspondencias = []
    
    from models.ley_octava import Nota, FRECUENCIAS_OCTAVA
    
    for nota in Nota:
        corresp = CORRESPONDENCIAS_OCTAVA[nota]
        freq_data = FRECUENCIAS_OCTAVA[nota]
        
        correspondencias.append({
            "nota": nota.value,
            "dia": corresp["dia"].value,
            "dimension": corresp["dimension"].value,
            "color": corresp["color"].value,
            "arquetipo": corresp["arquetipo"],
            "energia": corresp["energia"],
            "fase": corresp["fase"],
            "pregunta": corresp["pregunta"],
            "frecuencia": freq_data.frecuencia,
            "frecuencia_hz": corresp["frecuencia_hz"],
            "es_intervalo_critico": freq_data.es_intervalo_critico,
            "shock_requerido": corresp.get("shock_requerido")
        })
    
    return {
        "total_notas": 7,
        "correspondencias": correspondencias,
        "ley": "Ley de la Octava - Toda evolución procede en intervalos de 7",
        "intervalos_criticos": ["MI-FA (Miércoles)", "SI-DO (Domingo)"]
    }


@router.post("/crear-objetivo", response_model=ObjetivoOctava)
async def crear_objetivo(request: CrearObjetivoRequest):
    """
    Crea un nuevo objetivo estructurado como octava.
    
    Genera automáticamente:
    - 7 armónicos (todas las dimensiones)
    - Plan semanal de 7 fases
    - 2 shocks conscientes
    """
    try:
        # Parsear dimensión
        dimension = DimensionOctava(request.dimension_primaria)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Dimensión inválida. Debe ser una de: {[d.value for d in DimensionOctava]}"
        )
    
    # Parsear fecha
    fecha_obj = date.fromisoformat(request.fecha_objetivo)
    
    objetivo = gestor.crear_objetivo_octava(
        nombre=request.nombre,
        descripcion=request.descripcion,
        dimension_primaria=dimension,
        fecha_inicio=date.today(),
        fecha_objetivo=fecha_obj,
        practica_diaria=request.practica_diaria,
        resultado_observable=request.resultado_observable
    )
    
    return objetivo


@router.get("/objetivo/{objetivo_id}")
async def obtener_objetivo(objetivo_id: str):
    """Obtiene un objetivo completo con toda su estructura de octava"""
    
    if objetivo_id not in gestor.objetivos:
        raise HTTPException(status_code=404, detail="Objetivo no encontrado")
    
    return gestor.objetivos[objetivo_id]


@router.get("/objetivo/{objetivo_id}/estado")
async def obtener_estado_octava(objetivo_id: str):
    """
    Obtiene el estado actual de la octava para un objetivo.
    
    Retorna:
    - En qué nota/día estamos
    - Próximo shock consciente
    - Progreso de la semana
    - Alertas si es necesario
    """
    try:
        estado = gestor.obtener_estado_octava_actual(objetivo_id, date.today())
        return estado
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/objetivo/{objetivo_id}/armonicos")
async def analizar_armonicos(objetivo_id: str):
    """
    Analiza la coherencia armónica de un objetivo.
    
    Identifica:
    - Qué dimensiones están satisfechas
    - Qué dimensiones necesitan atención
    - Nivel de coherencia holística
    - Recomendaciones para equilibrar
    """
    try:
        analisis = gestor.analizar_armonicos(objetivo_id)
        return analisis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/objetivo/{objetivo_id}/shock")
async def aplicar_shock(objetivo_id: str, request: AplicarShockRequest):
    """
    Aplica un shock consciente a un objetivo.
    
    Los shocks son CRÍTICOS para que la octava continúe:
    - MI-FA (Miércoles): Revisión profunda
    - SI-DO (Domingo): Celebración e integración
    
    Sin shocks, la octava pierde momentum y no completa.
    """
    try:
        tipo = TipoShock(request.tipo_shock)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de shock inválido. Debe ser: {[t.value for t in TipoShock]}"
        )
    
    try:
        shock = gestor.aplicar_shock_consciente(objetivo_id, tipo, request.notas)
        return {
            "mensaje": "Shock consciente aplicado exitosamente",
            "shock": shock,
            "proxima_octava": gestor.objetivos[objetivo_id].octava_actual
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/shocks-hoy")
async def obtener_shocks_hoy():
    """
    Obtiene todos los shocks conscientes que deben aplicarse HOY.
    
    Para que el Orquestador los priorice en el plan del día.
    """
    shocks_hoy = gestor.obtener_shocks_pendientes_hoy(date.today())
    
    return {
        "fecha": date.today().isoformat(),
        "total_shocks": len(shocks_hoy),
        "shocks": [
            {
                "objetivo_id": obj.id,
                "objetivo_nombre": obj.nombre,
                "tipo_shock": shock.tipo.value,
                "intervalo": shock.intervalo,
                "accion_sugerida": shock.accion_sugerida,
                "pregunta_clave": shock.pregunta_clave,
                "duracion_minutos": shock.duracion_minutos
            }
            for obj, shock in shocks_hoy
        ],
        "mensaje": "⚡ Estos shocks son CRÍTICOS para que tus objetivos continúen evolucionando"
    }


@router.get("/dimension-hoy")
async def obtener_dimension_prioritaria_hoy():
    """
    Retorna qué dimensión debe priorizarse HOY según el día de la semana.
    
    El Entrelazador usa esto para estructurar el día con coherencia.
    """
    dimension_hoy = gestor.calcular_dimension_prioritaria_hoy(date.today())
    
    # Obtener correspondencia completa
    nota_hoy = None
    for nota, corresp in CORRESPONDENCIAS_OCTAVA.items():
        if corresp["dimension"] == dimension_hoy:
            nota_hoy = nota
            break
    
    corresp = CORRESPONDENCIAS_OCTAVA[nota_hoy]
    
    return {
        "fecha": date.today().isoformat(),
        "dimension_prioritaria": dimension_hoy.value,
        "nota": nota_hoy.value,
        "dia": corresp["dia"].value,
        "arquetipo": corresp["arquetipo"],
        "energia": corresp["energia"],
        "fase": corresp["fase"],
        "pregunta_clave": corresp["pregunta"],
        "color": corresp["color"].value,
        "mensaje": f"HOY es día de {corresp['arquetipo']}. Prioriza la dimensión {dimension_hoy.value}."
    }


@router.get("/resumen-octavas")
async def obtener_resumen_octavas():
    """
    Resumen de todas las octavas activas.
    
    Para dashboard principal.
    """
    return gestor.generar_resumen_octavas_activas()


@router.get("/objetivo/{objetivo_id}/espiral")
async def visualizar_espiral(objetivo_id: str):
    """
    Genera datos para visualizar la espiral de octavas de un objetivo.
    
    Retorna coordenadas para dibujar:
    - Espiral ascendente
    - Posición actual
    - Shocks aplicados
    """
    try:
        return gestor.visualizar_espiral_octavas(objetivo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/objetivos-por-dia/{dia}")
async def obtener_objetivos_por_dia(dia: str):
    """
    Obtiene todos los objetivos que tienen actividad en un día específico.
    
    Útil para planificación semanal.
    """
    try:
        dia_octava = DiaSemanaOctava(dia)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Día inválido. Debe ser: {[d.value for d in DiaSemanaOctava]}"
        )
    
    objetivos_dia = gestor.obtener_objetivos_por_dia(dia_octava)
    
    return {
        "dia": dia,
        "total_objetivos": len(objetivos_dia),
        "objetivos": [
            {
                "objetivo_id": obj.id,
                "nombre": obj.nombre,
                "nota": fase.nota.value,
                "fase": fase.fase,
                "actividad_sugerida": fase.actividad_sugerida,
                "es_intervalo_critico": fase.es_intervalo_critico
            }
            for obj, fase in objetivos_dia
        ]
    }

