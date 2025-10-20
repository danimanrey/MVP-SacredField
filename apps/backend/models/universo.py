"""
Modelos para el Universo Imaginal
Representación de estrellas, constelaciones y el grafo de conocimiento
"""

from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime


class Vector3D(BaseModel):
    """Posición en espacio 3D"""
    x: float
    y: float
    z: float


class Estrella(BaseModel):
    """
    Representa una nota de Obsidian como estrella en el universo
    """
    id: str  # filepath relativo al vault
    titulo: str
    contenido_preview: str
    dimension: str  # finanzas, biologia, conocimiento, etc.
    color: str  # Hex color del arcoíris
    posicion: Vector3D
    luminosidad: float  # 0.0 - 1.0, basada en relevancia
    enlaces: List[str]  # IDs de estrellas conectadas
    tags: List[str]
    metadata: Dict
    fecha_creacion: Optional[datetime]
    num_enlaces: int  # Total de conexiones (enlaces + backlinks)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class Orbita(BaseModel):
    """
    Representa un evento del calendario como órbita temporal
    """
    id: str  # ID del evento
    titulo: str
    descripcion: Optional[str]
    inicio: datetime
    fin: datetime
    dimension: str
    color: str
    radio: float  # Distancia temporal del centro (0 = ahora, 1 = lejano)
    angulo: float  # Posición en la órbita (0-360)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Constelacion(BaseModel):
    """
    Grupo de estrellas relacionadas (cluster de notas)
    """
    id: str
    nombre: str
    estrellas: List[str]  # IDs de estrellas en el cluster
    dimension_principal: str
    color: str
    centro: Vector3D  # Centro de masa del cluster
    densidad: float  # Qué tan conectadas están las estrellas
    importancia: float  # Basada en número de estrellas y conexiones


class GrafoConocimiento(BaseModel):
    """
    Grafo completo del conocimiento (todas las estrellas y conexiones)
    """
    estrellas: List[Estrella]
    constelaciones: List[Constelacion]
    total_enlaces: int
    dimensiones_balance: Dict[str, int]  # Número de estrellas por dimensión
    fecha_generacion: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UniversoImaginal(BaseModel):
    """
    Representación completa del universo imaginal
    Incluye estrellas (conocimiento) y órbitas (calendario)
    """
    tipo: str  # "individual" o "empresa"
    owner_id: str  # ID del usuario o empresa
    grafo_conocimiento: GrafoConocimiento
    orbitas: List[Orbita]
    estadisticas: Dict
    fecha_actualizacion: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# Schemas para requests/responses

class ObtenerEstrellasRequest(BaseModel):
    """Request para obtener estrellas filtradas"""
    dimension: Optional[str] = None  # Filtrar por dimensión
    min_enlaces: Optional[int] = None  # Solo hubs
    fecha_desde: Optional[datetime] = None
    fecha_hasta: Optional[datetime] = None


class ObtenerOrbitasRequest(BaseModel):
    """Request para obtener órbitas filtradas"""
    dias: int = 30  # Eventos próximos N días
    dimension: Optional[str] = None


class CrearEntrelazamientoRequest(BaseModel):
    """Request para crear entrelazamiento individual-empresa"""
    estrella_individual_id: str
    estrella_empresa_id: str
    tipo: str  # "proyecto", "tarea", "objetivo"
    permisos: Dict = {}


class EstadisticasUniverso(BaseModel):
    """Estadísticas del universo imaginal"""
    total_estrellas: int
    total_enlaces: int
    promedio_enlaces_por_estrella: float
    estrellas_por_dimension: Dict[str, int]
    hubs_count: int  # Estrellas con muchos enlaces
    orphans_count: int  # Estrellas sin enlaces
    constelaciones_count: int
    densidad_grafo: float  # Qué tan conectado está el grafo (0-1)

