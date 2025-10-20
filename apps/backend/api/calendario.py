"""
📅 API - Google Calendar
========================

Endpoints para gestionar eventos del calendario con inteligencia
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date, timedelta
from pydantic import BaseModel

from models.database import get_db
from integraciones.google_calendar import GoogleCalendarClient as GoogleCalendarService


router = APIRouter()


# ==================== SCHEMAS ====================

class Evento(BaseModel):
    """Evento del calendario"""
    id: Optional[str] = None
    titulo: str
    descripcion: Optional[str] = None
    inicio: datetime
    fin: datetime
    categoria: str  # 'no-negociable', 'tarea-objetivo', 'emergente'
    dimension: Optional[str] = None  # finanzas, biologia, etc.
    color: Optional[str] = None
    completado: bool = False
    

class CrearEventoRequest(BaseModel):
    """Request para crear evento"""
    titulo: str
    descripcion: Optional[str] = None
    inicio: datetime
    duracion_minutos: int = 60
    categoria: str = 'tarea-objetivo'
    dimension: Optional[str] = None


class EditarEventoConIARequest(BaseModel):
    """Request para editar evento con sugerencia de IA"""
    evento_id: str
    que_cambiar: str  # "Hazlo más corto", "Muévelo a la mañana", etc.


class ValidarCalendarioRequest(BaseModel):
    """Request para validar calendario después de Estado Cero"""
    estado_cero_id: str
    eventos: List[Evento]


# ==================== ENDPOINTS ====================

@router.get("/eventos/hoy")
async def obtener_eventos_hoy(
    fecha: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Obtiene eventos del día desde Google Calendar
    """
    try:
        calendar_service = GoogleCalendarService()
        
        # Usar fecha de hoy si no se especifica
        if not fecha:
            fecha = date.today()
        
        # Obtener eventos
        eventos = calendar_service.obtener_eventos_dia(fecha)
        
        # Categorizar automáticamente
        eventos_categorizados = []
        for evento in eventos:
            # Detectar categoría basada en título o descripción
            categoria = detectar_categoria(evento)
            dimension = detectar_dimension(evento)
            
            eventos_categorizados.append({
                **evento,
                "categoria": categoria,
                "dimension": dimension,
                "color": obtener_color_dimension(dimension)
            })
        
        # Calcular porcentaje al borde del caos
        total_minutos = 16 * 60  # 16 horas activas
        minutos_asignados = sum(
            (e['fin'] - e['inicio']).total_seconds() / 60
            for e in eventos_categorizados
        )
        porcentaje_asignado = (minutos_asignados / total_minutos) * 100
        porcentaje_caos = 100 - porcentaje_asignado
        
        return {
            "fecha": fecha.isoformat(),
            "eventos": eventos_categorizados,
            "total_eventos": len(eventos_categorizados),
            "porcentaje_asignado": round(porcentaje_asignado, 1),
            "porcentaje_caos": round(porcentaje_caos, 1),
            "al_borde_del_caos": 30 <= porcentaje_caos <= 50  # Ideal: 30-50%
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo eventos: {str(e)}"
        )


@router.post("/eventos")
async def crear_evento(
    request: CrearEventoRequest,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo evento en Google Calendar
    """
    try:
        calendar_service = GoogleCalendarService()
        
        # Calcular fin basado en duración
        fin = request.inicio + timedelta(minutes=request.duracion_minutos)
        
        # Crear evento
        evento_id = calendar_service.crear_evento(
            titulo=request.titulo,
            descripcion=request.descripcion or "",
            inicio=request.inicio,
            fin=fin,
            metadata={
                "categoria": request.categoria,
                "dimension": request.dimension
            }
        )
        
        return {
            "status": "created",
            "evento_id": evento_id,
            "titulo": request.titulo
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creando evento: {str(e)}"
        )


@router.put("/eventos/{evento_id}")
async def actualizar_evento(
    evento_id: str,
    evento: Evento,
    db: Session = Depends(get_db)
):
    """
    Actualiza un evento existente
    """
    try:
        calendar_service = GoogleCalendarService()
        
        calendar_service.actualizar_evento(
            evento_id=evento_id,
            titulo=evento.titulo,
            descripcion=evento.descripcion or "",
            inicio=evento.inicio,
            fin=evento.fin
        )
        
        return {
            "status": "updated",
            "evento_id": evento_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error actualizando evento: {str(e)}"
        )


@router.delete("/eventos/{evento_id}")
async def eliminar_evento(
    evento_id: str,
    db: Session = Depends(get_db)
):
    """
    Elimina un evento del calendario
    """
    try:
        calendar_service = GoogleCalendarService()
        calendar_service.eliminar_evento(evento_id)
        
        return {
            "status": "deleted",
            "evento_id": evento_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error eliminando evento: {str(e)}"
        )


@router.post("/eventos/{evento_id}/editar-con-ia")
async def editar_evento_con_ia(
    evento_id: str,
    request: EditarEventoConIARequest,
    db: Session = Depends(get_db)
):
    """
    Edita un evento usando IA para interpretar el cambio
    
    Ejemplos:
    - "Hazlo más corto" → Reduce duración
    - "Muévelo a la mañana" → Cambia hora a AM
    - "Añade contexto sobre reunión" → Mejora descripción
    """
    try:
        from services.claude_client import ClaudeClient
        
        calendar_service = GoogleCalendarService()
        claude = ClaudeClient()
        
        # Obtener evento actual
        evento_actual = calendar_service.obtener_evento(evento_id)
        
        # Claude interpreta el cambio
        prompt = f"""
        Tienes este evento:
        - Título: {evento_actual['summary']}
        - Inicio: {evento_actual['start']}
        - Fin: {evento_actual['end']}
        - Descripción: {evento_actual.get('description', 'Sin descripción')}
        
        El usuario quiere: "{request.que_cambiar}"
        
        Retorna JSON con los campos a actualizar:
        {{
          "titulo": "nuevo título si cambia",
          "descripcion": "nueva descripción si cambia",
          "inicio": "nueva fecha/hora si cambia",
          "fin": "nueva fecha/hora si cambia"
        }}
        
        Solo incluye los campos que cambien.
        """
        
        resultado = await claude.generar_json(prompt)
        
        # Aplicar cambios
        if resultado.get('titulo'):
            evento_actual['summary'] = resultado['titulo']
        if resultado.get('descripcion'):
            evento_actual['description'] = resultado['descripcion']
        # ... aplicar otros cambios
        
        # Actualizar en Google Calendar
        calendar_service.actualizar_evento(evento_id, **evento_actual)
        
        return {
            "status": "updated",
            "cambios_aplicados": resultado,
            "sugerencia_ia": f"Claude interpretó: {request.que_cambiar}"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error editando con IA: {str(e)}"
        )


@router.post("/validar-calendario")
async def validar_calendario_post_estado_cero(
    request: ValidarCalendarioRequest,
    db: Session = Depends(get_db)
):
    """
    Valida el calendario después de completar un Estado Cero
    
    Guarda los eventos actualizados y marca Estado Cero como finalizado
    """
    try:
        calendar_service = GoogleCalendarService()
        
        eventos_creados = []
        eventos_actualizados = []
        
        for evento in request.eventos:
            if evento.id:
                # Actualizar existente
                calendar_service.actualizar_evento(
                    evento_id=evento.id,
                    titulo=evento.titulo,
                    descripcion=evento.descripcion or "",
                    inicio=evento.inicio,
                    fin=evento.fin
                )
                eventos_actualizados.append(evento.id)
            else:
                # Crear nuevo
                evento_id = calendar_service.crear_evento(
                    titulo=evento.titulo,
                    descripcion=evento.descripcion or "",
                    inicio=evento.inicio,
                    fin=evento.fin,
                    metadata={
                        "categoria": evento.categoria,
                        "dimension": evento.dimension
                    }
                )
                eventos_creados.append(evento_id)
        
        return {
            "status": "validated",
            "eventos_creados": len(eventos_creados),
            "eventos_actualizados": len(eventos_actualizados),
            "siguiente_paso": "espejo_diario"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error validando calendario: {str(e)}"
        )


# ==================== HELPERS ====================

def detectar_categoria(evento: dict) -> str:
    """Detecta categoría del evento basándose en título/descripción"""
    titulo = evento.get('summary', '').lower()
    desc = evento.get('description', '').lower()
    texto = f"{titulo} {desc}"
    
    # No-negociables
    if any(palabra in texto for palabra in ['estado cero', 'fajr', 'dhuhr', 'maghrib', 'meditación']):
        return 'no-negociable'
    
    # Tareas hacia objetivos
    if any(palabra in texto for palabra in ['proyecto', 'desarrollar', 'crear', 'escribir', 'objetivo']):
        return 'tarea-objetivo'
    
    # Emergente por defecto
    return 'emergente'


def detectar_dimension(evento: dict) -> Optional[str]:
    """Detecta dimensión del evento"""
    titulo = evento.get('summary', '').lower()
    desc = evento.get('description', '').lower()
    texto = f"{titulo} {desc}"
    
    keywords = {
        'finanzas': ['dinero', 'pago', 'factura', 'cliente', 'venta'],
        'biologia': ['ejercicio', 'gym', 'médico', 'dormir', 'comida'],
        'conocimiento': ['leer', 'curso', 'aprender', 'estudio'],
        'desarrollo': ['código', 'programar', 'desarrollo', 'build', 'deploy'],
        'relaciones': ['reunión', 'llamada', 'familia', 'amigo'],
        'creatividad': ['diseño', 'música', 'arte', 'escritura'],
        'espiritualidad': ['meditación', 'reflexión', 'estado cero']
    }
    
    for dimension, palabras in keywords.items():
        if any(palabra in texto for palabra in palabras):
            return dimension
    
    return None


def obtener_color_dimension(dimension: Optional[str]) -> str:
    """Retorna color hexadecimal de la dimensión"""
    colores = {
        'finanzas': '#DC2626',
        'biologia': '#F97316',
        'conocimiento': '#EAB308',
        'desarrollo': '#22C55E',
        'relaciones': '#3B82F6',
        'creatividad': '#8B5CF6',
        'espiritualidad': '#A855F7'
    }
    return colores.get(dimension, '#6B7280')

