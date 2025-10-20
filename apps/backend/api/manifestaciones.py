"""
🎯 API - Manifestaciones y Dimensiones
========================================

Endpoints para gestionar las 7 dimensiones del ser y sus manifestaciones.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel

from models.database import get_db


router = APIRouter()


class Manifestacion(BaseModel):
    """Manifestación u objetivo en una dimensión"""
    id: str
    dimension: str  # espiritual, biologico, financiero, conocimiento, relacional, desarrollo, creativo
    nombre: str
    descripcion: str
    tipo: str  # corto_plazo, medio_plazo, largo_plazo
    fecha_inicio: date
    fecha_objetivo: date
    practica_diaria: str
    resultado_observable: str
    progreso_porcentaje: float = 0.0
    estado: str = "activa"  # activa, pausada, completada, abandonada


class Dimension(BaseModel):
    """Una de las 7 dimensiones del ser"""
    nombre: str
    icono: str
    color: str
    descripcion: str
    pregunta_clave: str
    manifestaciones: List[Manifestacion]
    progreso_general: float
    ultima_revision: Optional[datetime] = None


# Mock data - En producción vendría de la base de datos
DIMENSIONES = {
    "espiritual": {
        "nombre": "Espiritual",
        "icono": "🕌",
        "color": "#8b5cf6",
        "descripcion": "Conexión con lo trascendente, purificación del corazón, práctica contemplativa",
        "pregunta_clave": "¿Estoy viviendo desde mi centro sagrado?",
        "manifestaciones": []
    },
    "biologico": {
        "nombre": "Biológico/Físico",
        "icono": "💪",
        "color": "#10b981",
        "descripcion": "Salud física, energía vital, movimiento, descanso, nutrición",
        "pregunta_clave": "¿Mi cuerpo es un templo cuidado?",
        "manifestaciones": []
    },
    "financiero": {
        "nombre": "Financiero",
        "icono": "💰",
        "color": "#f59e0b",
        "descripcion": "Abundancia material, generación de valor, libertad económica",
        "pregunta_clave": "¿Genero valor alineado con mi esencia?",
        "manifestaciones": []
    },
    "conocimiento": {
        "nombre": "Conocimiento",
        "icono": "📚",
        "color": "#3b82f6",
        "descripcion": "Aprendizaje profundo, dominio técnico, síntesis de sabiduría",
        "pregunta_clave": "¿Estoy profundizando en lo que importa?",
        "manifestaciones": []
    },
    "relacional": {
        "nombre": "Relacional",
        "icono": "❤️",
        "color": "#ec4899",
        "descripcion": "Vínculos sagrados, familia, comunidad, amor consciente",
        "pregunta_clave": "¿Nutro las conexiones que importan?",
        "manifestaciones": []
    },
    "desarrollo": {
        "nombre": "Desarrollo",
        "icono": "🚀",
        "color": "#06b6d4",
        "descripcion": "Crecimiento profesional, impacto en el mundo, servicio",
        "pregunta_clave": "¿Mi trabajo materializa mi visión?",
        "manifestaciones": []
    },
    "creativo": {
        "nombre": "Creativo",
        "icono": "🎨",
        "color": "#f97316",
        "descripcion": "Expresión artística, belleza, al-khayāl al-faʿʿāl",
        "pregunta_clave": "¿Expreso la belleza que habita en mí?",
        "manifestaciones": []
    }
}


@router.get("/dimensiones")
async def obtener_todas_dimensiones():
    """
    Obtiene las 7 dimensiones del ser con sus manifestaciones.
    
    Retorna:
    - Lista de dimensiones con sus objetivos
    - Progreso general por dimensión
    - Estado actual de cada manifestación
    """
    
    dimensiones_response = []
    
    for key, dim in DIMENSIONES.items():
        # Calcular progreso general (mock)
        if dim["manifestaciones"]:
            progreso = sum(m.get("progreso_porcentaje", 0) for m in dim["manifestaciones"]) / len(dim["manifestaciones"])
        else:
            progreso = 0.0
        
        dimensiones_response.append({
            "id": key,
            "nombre": dim["nombre"],
            "icono": dim["icono"],
            "color": dim["color"],
            "descripcion": dim["descripcion"],
            "pregunta_clave": dim["pregunta_clave"],
            "manifestaciones": dim["manifestaciones"],
            "total_manifestaciones": len(dim["manifestaciones"]),
            "progreso_general": progreso,
            "ultima_revision": None
        })
    
    return {
        "dimensiones": dimensiones_response,
        "total_dimensiones": 7,
        "mensaje": "Las 7 dimensiones del ser humano integral"
    }


@router.get("/dimension/{dimension_id}")
async def obtener_dimension(dimension_id: str):
    """
    Obtiene detalle de una dimensión específica.
    """
    
    if dimension_id not in DIMENSIONES:
        raise HTTPException(status_code=404, detail="Dimensión no encontrada")
    
    dim = DIMENSIONES[dimension_id]
    
    return {
        "id": dimension_id,
        **dim,
        "total_manifestaciones": len(dim["manifestaciones"]),
        "progreso_general": 0.0
    }


@router.post("/manifestacion")
async def crear_manifestacion(manifestacion: Manifestacion):
    """
    Crea una nueva manifestación/objetivo en una dimensión.
    """
    
    if manifestacion.dimension not in DIMENSIONES:
        raise HTTPException(status_code=400, detail="Dimensión no válida")
    
    # En producción: guardar en base de datos
    DIMENSIONES[manifestacion.dimension]["manifestaciones"].append(manifestacion.dict())
    
    return {
        "mensaje": "Manifestación creada con éxito",
        "manifestacion": manifestacion
    }


@router.put("/manifestacion/{manifestacion_id}/progreso")
async def actualizar_progreso(manifestacion_id: str, progreso: float):
    """
    Actualiza el progreso de una manifestación.
    """
    
    # En producción: actualizar en base de datos
    for dim in DIMENSIONES.values():
        for man in dim["manifestaciones"]:
            if man.get("id") == manifestacion_id:
                man["progreso_porcentaje"] = progreso
                return {
                    "mensaje": "Progreso actualizado",
                    "manifestacion_id": manifestacion_id,
                    "progreso": progreso
                }
    
    raise HTTPException(status_code=404, detail="Manifestación no encontrada")


@router.get("/auditoria-dimensiones")
async def auditar_dimensiones():
    """
    Realiza una auditoría de todas las dimensiones.
    
    Identifica:
    - Dimensiones sin manifestaciones
    - Dimensiones con bajo progreso
    - Desequilibrios entre dimensiones
    """
    
    auditoria = {
        "fecha": date.today().isoformat(),
        "dimensiones_sin_manifestaciones": [],
        "dimensiones_bajo_progreso": [],
        "dimension_mas_avanzada": None,
        "dimension_menos_avanzada": None,
        "equilibrio_general": 0.0,
        "recomendaciones": []
    }
    
    progresos = {}
    
    for key, dim in DIMENSIONES.items():
        if not dim["manifestaciones"]:
            auditoria["dimensiones_sin_manifestaciones"].append({
                "dimension": dim["nombre"],
                "pregunta": dim["pregunta_clave"]
            })
        else:
            progreso = sum(m.get("progreso_porcentaje", 0) for m in dim["manifestaciones"]) / len(dim["manifestaciones"])
            progresos[key] = progreso
            
            if progreso < 30:
                auditoria["dimensiones_bajo_progreso"].append({
                    "dimension": dim["nombre"],
                    "progreso": progreso
                })
    
    if progresos:
        max_key = max(progresos, key=progresos.get)
        min_key = min(progresos, key=progresos.get)
        
        auditoria["dimension_mas_avanzada"] = {
            "dimension": DIMENSIONES[max_key]["nombre"],
            "progreso": progresos[max_key]
        }
        
        auditoria["dimension_menos_avanzada"] = {
            "dimension": DIMENSIONES[min_key]["nombre"],
            "progreso": progresos[min_key]
        }
        
        # Calcular equilibrio (menor desviación estándar = mayor equilibrio)
        promedio = sum(progresos.values()) / len(progresos)
        desviacion = sum((p - promedio) ** 2 for p in progresos.values()) / len(progresos)
        auditoria["equilibrio_general"] = max(0, 100 - desviacion)
    
    # Generar recomendaciones
    if auditoria["dimensiones_sin_manifestaciones"]:
        auditoria["recomendaciones"].append(
            f"Define manifestaciones en: {', '.join([d['dimension'] for d in auditoria['dimensiones_sin_manifestaciones']])}"
        )
    
    if auditoria["dimensiones_bajo_progreso"]:
        auditoria["recomendaciones"].append(
            f"Aumenta enfoque en: {', '.join([d['dimension'] for d in auditoria['dimensiones_bajo_progreso']])}"
        )
    
    if auditoria["equilibrio_general"] < 70:
        auditoria["recomendaciones"].append(
            "Busca mayor equilibrio entre las 7 dimensiones del ser"
        )
    
    return auditoria


@router.get("/manifestaciones-prioritarias")
async def obtener_manifestaciones_prioritarias():
    """
    Retorna las manifestaciones que requieren atención inmediata.
    
    Prioriza:
    - Corto plazo cercanas a fecha objetivo
    - Bajo progreso pero fecha próxima
    - Manifestaciones abandonadas que deberían reactivarse
    """
    
    prioritarias = []
    hoy = date.today()
    
    for dim_key, dim in DIMENSIONES.items():
        for man in dim["manifestaciones"]:
            fecha_obj = man.get("fecha_objetivo")
            if isinstance(fecha_obj, str):
                fecha_obj = datetime.strptime(fecha_obj, "%Y-%m-%d").date()
            
            dias_restantes = (fecha_obj - hoy).days if fecha_obj else 999
            progreso = man.get("progreso_porcentaje", 0)
            
            # Priorizar si:
            # - Menos de 30 días y progreso < 70%
            # - Menos de 7 días independiente del progreso
            es_prioritaria = (dias_restantes < 30 and progreso < 70) or dias_restantes < 7
            
            if es_prioritaria:
                prioritarias.append({
                    **man,
                    "dimension": dim["nombre"],
                    "dias_restantes": dias_restantes,
                    "urgencia": "alta" if dias_restantes < 7 else "media"
                })
    
    # Ordenar por urgencia
    prioritarias.sort(key=lambda x: x["dias_restantes"])
    
    return {
        "fecha": hoy.isoformat(),
        "total": len(prioritarias),
        "manifestaciones": prioritarias
    }

