"""
🕌 Campo Sagrado - API de Entrelazamiento Personal
==================================================

Endpoints para gestionar el perfil personal y dashboard de entrelazamiento
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional

from models.database import get_db
from models.schemas import (
    PerfilPersonal,
    DashboardEntrelazamiento,
    RutinaDeportiva,
    ComidaConfiguracion,
    PresupuestoCategoria,
    TemaAprendizaje,
    ProyectoDesarrollo,
    InversionAsunto
)
from agentes.entrelazador import agente_entrelazador


router = APIRouter(prefix="/entrelazamiento", tags=["entrelazamiento"])


@router.post("/perfil", response_model=dict)
async def crear_perfil(perfil: PerfilPersonal):
    """
    Crea o actualiza el perfil personal del usuario
    
    Este perfil incluye:
    - Rutinas deportivas semanales
    - Sistema de comidas y batch cooking
    - Presupuesto y gestión financiera
    - Temas de aprendizaje activos
    - Proyectos de desarrollo
    - Asuntos de inversión
    """
    try:
        # Cargar perfil en el agente
        agente_entrelazador.cargar_perfil(perfil)
        
        return {
            "success": True,
            "mensaje": f"✅ Perfil de {perfil.nombre} cargado correctamente",
            "resumen": {
                "rutinas_deportivas": len(perfil.rutinas_deportivas),
                "sistema_comidas": len(perfil.sistema_comidas),
                "categorias_presupuesto": len(perfil.presupuesto_mensual),
                "temas_aprendizaje": len(perfil.temas_aprendizaje),
                "proyectos_desarrollo": len(perfil.proyectos_desarrollo),
                "inversiones_asuntos": len(perfil.inversiones_asuntos)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar perfil: {str(e)}")


@router.get("/dashboard-semanal", response_model=DashboardEntrelazamiento)
async def obtener_dashboard_semanal(fecha_inicio: Optional[str] = None):
    """
    Genera el dashboard completo de entrelazamiento semanal
    
    Analiza y entrelaza:
    - Deportes y cuándo encajan mejor según energía
    - Comidas y planificación de batch cooking
    - Presupuesto y cuándo hacer compras
    - Aprendizaje y bloques de estudio
    - Proyectos de desarrollo y sus hitos
    - Asuntos de inversión y decisiones pendientes
    
    Detecta:
    - Conflictos de tiempo o energía
    - Sinergias positivas entre actividades
    - Espacios de emergencia (40% regla)
    - Optimizaciones posibles
    """
    try:
        # Verificar que hay perfil cargado
        if not agente_entrelazador.perfil_usuario:
            raise HTTPException(
                status_code=400,
                detail="❌ No hay perfil cargado. Usa POST /entrelazamiento/perfil primero"
            )
        
        # Parsear fecha si se proporciona
        fecha = None
        if fecha_inicio:
            try:
                fecha = date.fromisoformat(fecha_inicio)
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DD")
        
        # Generar dashboard
        dashboard = agente_entrelazador.generar_dashboard_semanal(fecha_inicio=fecha)
        
        return dashboard
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar dashboard: {str(e)}")


@router.get("/perfil-actual", response_model=PerfilPersonal)
async def obtener_perfil_actual():
    """
    Obtiene el perfil personal actualmente cargado
    """
    if not agente_entrelazador.perfil_usuario:
        raise HTTPException(
            status_code=404,
            detail="No hay perfil cargado"
        )
    
    return agente_entrelazador.perfil_usuario


@router.post("/perfil/rutina-deportiva")
async def agregar_rutina_deportiva(rutina: RutinaDeportiva):
    """Agrega una nueva rutina deportiva al perfil"""
    if not agente_entrelazador.perfil_usuario:
        raise HTTPException(status_code=400, detail="No hay perfil cargado")
    
    agente_entrelazador.perfil_usuario.rutinas_deportivas.append(rutina)
    agente_entrelazador.perfil_usuario.actualizado = datetime.now()
    
    return {
        "success": True,
        "mensaje": f"Rutina '{rutina.nombre}' agregada",
        "total_rutinas": len(agente_entrelazador.perfil_usuario.rutinas_deportivas)
    }


@router.post("/perfil/comida")
async def agregar_comida(comida: ComidaConfiguracion):
    """Agrega una configuración de comida al perfil"""
    if not agente_entrelazador.perfil_usuario:
        raise HTTPException(status_code=400, detail="No hay perfil cargado")
    
    agente_entrelazador.perfil_usuario.sistema_comidas.append(comida)
    agente_entrelazador.perfil_usuario.actualizado = datetime.now()
    
    return {
        "success": True,
        "mensaje": f"Comida '{comida.tipo}' agregada",
        "total_comidas": len(agente_entrelazador.perfil_usuario.sistema_comidas)
    }


@router.post("/perfil/presupuesto")
async def agregar_categoria_presupuesto(categoria: PresupuestoCategoria):
    """Agrega una categoría de presupuesto"""
    if not agente_entrelazador.perfil_usuario:
        raise HTTPException(status_code=400, detail="No hay perfil cargado")
    
    agente_entrelazador.perfil_usuario.presupuesto_mensual.append(categoria)
    agente_entrelazador.perfil_usuario.actualizado = datetime.now()
    
    return {
        "success": True,
        "mensaje": f"Categoría '{categoria.nombre}' agregada",
        "asignado": categoria.asignado_mensual
    }


@router.post("/perfil/tema-aprendizaje")
async def agregar_tema_aprendizaje(tema: TemaAprendizaje):
    """Agrega un tema de aprendizaje"""
    if not agente_entrelazador.perfil_usuario:
        raise HTTPException(status_code=400, detail="No hay perfil cargado")
    
    agente_entrelazador.perfil_usuario.temas_aprendizaje.append(tema)
    agente_entrelazador.perfil_usuario.actualizado = datetime.now()
    
    return {
        "success": True,
        "mensaje": f"Tema '{tema.nombre}' agregado al aprendizaje",
        "dominio": tema.dominio,
        "prioridad": tema.prioridad
    }


@router.post("/perfil/proyecto")
async def agregar_proyecto_desarrollo(proyecto: ProyectoDesarrollo):
    """Agrega un proyecto de desarrollo"""
    if not agente_entrelazador.perfil_usuario:
        raise HTTPException(status_code=400, detail="No hay perfil cargado")
    
    agente_entrelazador.perfil_usuario.proyectos_desarrollo.append(proyecto)
    agente_entrelazador.perfil_usuario.actualizado = datetime.now()
    
    return {
        "success": True,
        "mensaje": f"Proyecto '{proyecto.nombre}' agregado",
        "tipo": proyecto.tipo,
        "horas_semanales": proyecto.horas_semanales_deseadas
    }


@router.post("/perfil/inversion")
async def agregar_inversion_asunto(asunto: InversionAsunto):
    """Agrega un asunto de inversión"""
    if not agente_entrelazador.perfil_usuario:
        raise HTTPException(status_code=400, detail="No hay perfil cargado")
    
    agente_entrelazador.perfil_usuario.inversiones_asuntos.append(asunto)
    agente_entrelazador.perfil_usuario.actualizado = datetime.now()
    
    return {
        "success": True,
        "mensaje": f"Asunto '{asunto.nombre}' agregado",
        "tipo": asunto.tipo,
        "monto": asunto.monto_involucrado
    }


@router.get("/analisis/conflictos")
async def analizar_conflictos_semana(fecha_inicio: Optional[str] = None):
    """
    Analiza conflictos en la semana planificada
    
    Detecta:
    - Días sobrecargados
    - Actividades que compiten por tiempo/energía
    - Incompatibilidades en la programación
    """
    if not agente_entrelazador.perfil_usuario:
        raise HTTPException(status_code=400, detail="No hay perfil cargado")
    
    fecha = None
    if fecha_inicio:
        fecha = date.fromisoformat(fecha_inicio)
    
    dashboard = agente_entrelazador.generar_dashboard_semanal(fecha_inicio=fecha)
    
    # Extraer todos los conflictos
    conflictos_por_dia = {}
    for dia in dashboard.dias_semana:
        dia_nombre = agente_entrelazador._nombre_dia(dia.fecha)
        if dia.conflictos_detectados:
            conflictos_por_dia[dia_nombre] = dia.conflictos_detectados
    
    return {
        "conflictos_totales": sum(len(dia.conflictos_detectados) for dia in dashboard.dias_semana),
        "conflictos_por_dia": conflictos_por_dia,
        "dias_criticos": [
            agente_entrelazador._nombre_dia(dia.fecha)
            for dia in dashboard.dias_semana
            if len(dia.conflictos_detectados) > 2
        ]
    }


@router.get("/analisis/sinergias")
async def analizar_sinergias_semana(fecha_inicio: Optional[str] = None):
    """
    Analiza sinergias positivas en la semana
    
    Identifica:
    - Combinaciones beneficiosas de actividades
    - Patrones que potencian productividad
    - Balances óptimos detectados
    """
    if not agente_entrelazador.perfil_usuario:
        raise HTTPException(status_code=400, detail="No hay perfil cargado")
    
    fecha = None
    if fecha_inicio:
        fecha = date.fromisoformat(fecha_inicio)
    
    dashboard = agente_entrelazador.generar_dashboard_semanal(fecha_inicio=fecha)
    
    # Extraer todas las sinergias
    sinergias_por_dia = {}
    for dia in dashboard.dias_semana:
        dia_nombre = agente_entrelazador._nombre_dia(dia.fecha)
        if dia.sinergias_detectadas:
            sinergias_por_dia[dia_nombre] = dia.sinergias_detectadas
    
    return {
        "sinergias_totales": sum(len(dia.sinergias_detectadas) for dia in dashboard.dias_semana),
        "sinergias_por_dia": sinergias_por_dia,
        "dias_optimizados": [
            agente_entrelazador._nombre_dia(dia.fecha)
            for dia in dashboard.dias_semana
            if len(dia.sinergias_detectadas) >= 2
        ]
    }


@router.get("/resumen-semana")
async def obtener_resumen_semana(fecha_inicio: Optional[str] = None):
    """
    Obtiene un resumen ejecutivo de la semana planificada
    """
    if not agente_entrelazador.perfil_usuario:
        raise HTTPException(status_code=400, detail="No hay perfil cargado")
    
    fecha = None
    if fecha_inicio:
        fecha = date.fromisoformat(fecha_inicio)
    
    dashboard = agente_entrelazador.generar_dashboard_semanal(fecha_inicio=fecha)
    
    return {
        "periodo": {
            "inicio": dashboard.semana_inicio.isoformat(),
            "fin": dashboard.semana_fin.isoformat()
        },
        "deportes": {
            "sesiones_planificadas": dashboard.sesiones_deportivas_semana,
            "objetivo_cumplido": dashboard.objetivo_cumplido_deporte
        },
        "finanzas": {
            "gasto_proyectado": dashboard.gasto_semana_proyectado,
            "presupuesto_disponible": dashboard.presupuesto_disponible,
            "alertas": dashboard.alertas_financieras
        },
        "desarrollo": {
            "horas_aprendizaje": dashboard.horas_aprendizaje_semana,
            "temas_prioridad": dashboard.temas_prioridad,
            "horas_proyectos": dashboard.horas_desarrollo_semana,
            "proyectos_activos": len(dashboard.proyectos_avance)
        },
        "optimizacion": {
            "sugerencias": dashboard.sugerencias_optimizacion,
            "espacios_emergencia": len(dashboard.espacios_emergencia),
            "patron_energia": dashboard.patron_energia_semanal
        }
    }



