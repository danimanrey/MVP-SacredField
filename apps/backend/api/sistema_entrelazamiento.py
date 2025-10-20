"""
🔗 Campo Sagrado - API Sistema de Entrelazamiento
=================================================

API endpoints para el sistema completo de entrelazamiento y orquestación:
1. Análisis de patrones
2. Entrelazamiento de dominios  
3. Generación de acciones sistémicas
4. Validación de armonía

Opera con pensamiento sistémico y reconocimiento de patrones.
"""

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Any
import os
import json
from pathlib import Path

from agentes.analizador_patrones import AnalizadorPatrones
from agentes.entrelazador_dominios import EntrelazadorDominios
from agentes.documentador_mejorado import DocumentadorMejorado
from services.espejo_diario_generator import EspejoDiarioGenerator
from services.obsidian_structure import ObsidianStructureManager

router = APIRouter()

# Configuración
VAULT_PATH = os.path.expanduser(os.getenv("OBSIDIAN_VAULT_PATH", "~/Documents/CampoSagrado"))

# Inicializar agentes y servicios
analizador = AnalizadorPatrones(VAULT_PATH)
entrelazador = EntrelazadorDominios(VAULT_PATH)
documentador = DocumentadorMejorado(VAULT_PATH)
espejo_generator = EspejoDiarioGenerator(VAULT_PATH)
vault_manager = ObsidianStructureManager(VAULT_PATH)

@router.get("/test")
async def test_sistema():
    """Endpoint de prueba del sistema de entrelazamiento"""
    return {
        "status": "ok",
        "sistema": "entrelazamiento",
        "vault_path": VAULT_PATH,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/analisis-patrones")
async def obtener_analisis_patrones(dias: int = 7):
    """
    Obtiene análisis de patrones de los últimos N días
    """
    try:
        analisis = analizador.analizar_ultimos_estados(dias)
        
        # Guardar reporte en Obsidian
        if "error" not in analisis:
            archivo_reporte = analizador.guardar_reporte(analisis)
            analisis["archivo_reporte"] = archivo_reporte
        
        return {
            "status": "success",
            "analisis": analisis,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis de patrones: {str(e)}")

@router.get("/entrelazamiento-dominios")
async def obtener_entrelazamiento_dominios(dias: int = 7):
    """
    Obtiene análisis de entrelazamiento entre dominios
    """
    try:
        # Analizar estado de dominios
        dominios = entrelazador.analizar_estado_dominios(dias)
        
        # Detectar entrelazamientos
        entrelazamientos = entrelazador.detectar_entrelazamientos(dominios)
        
        # Generar acciones coordinadas
        acciones_coordinadas = entrelazador.generar_acciones_coordinadas(dominios, entrelazamientos)
        
        # Guardar reporte en Obsidian
        archivo_reporte = entrelazador.guardar_reporte_entrelazamiento(
            dominios, entrelazamientos, acciones_coordinadas
        )
        
        return {
            "status": "success",
            "dominios": {
                nombre: {
                    "estado": dominio.estado,
                    "energia": dominio.energia,
                    "urgencia": dominio.urgencia,
                    "recursos_disponibles": dominio.recursos_disponibles,
                    "necesidades": dominio.necesidades
                } for nombre, dominio in dominios.items()
            },
            "entrelazamientos": [
                {
                    "dominios": e.dominios,
                    "tipo": e.tipo,
                    "intensidad": e.intensidad,
                    "descripcion": e.descripcion,
                    "accion_sugerida": e.accion_sugerida
                } for e in entrelazamientos
            ],
            "acciones_coordinadas": [
                {
                    "nombre": a.nombre,
                    "dominios_implicados": a.dominios_implicados,
                    "secuencia": a.secuencia,
                    "tiempo_total": a.tiempo_total,
                    "urgencia": a.urgencia,
                    "impacto_sistémico": a.impacto_sistémico,
                    "resultado_esperado": a.resultado_esperado
                } for a in acciones_coordinadas
            ],
            "archivo_reporte": archivo_reporte,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en entrelazamiento de dominios: {str(e)}")

@router.get("/acciones-sistemicas")
async def obtener_acciones_sistemicas(dias: int = 7):
    """
    Obtiene acciones sistémicas completas basadas en análisis integral
    """
    try:
        # Generar acciones sistémicas
        acciones = documentador.generar_acciones_sistemicas(dias)
        
        # Guardar reporte en Obsidian
        archivo_reporte = documentador.guardar_reporte_acciones(acciones)
        
        # Formatear respuesta
        acciones_formateadas = []
        for accion in acciones:
            acciones_formateadas.append({
                "id": accion.id,
                "nombre": accion.nombre,
                "tipo": accion.tipo,
                "prioridad": accion.prioridad,
                "urgencia": accion.urgencia,
                "impacto_sistémico": accion.impacto_sistémico,
                "descripcion": accion.descripcion,
                "contexto": accion.contexto,
                "dominios_implicados": accion.dominios_implicados,
                "tiempo_estimado": accion.tiempo_estimado,
                "recursos_requeridos": accion.recursos_requeridos,
                "prerequisitos": accion.prerequisitos,
                "secuencia_pasos": accion.secuencia_pasos,
                "resultado_observable": accion.resultado_observable,
                "indicadores_exito": accion.indicadores_exito,
                "metricas_seguimiento": accion.metricas_seguimiento,
                "momento_optimo": accion.momento_optimo,
                "frecuencia": accion.frecuencia,
                "recordatorios": accion.recordatorios,
                "validacion_armonia": accion.validacion_armonia,
                "fecha_creacion": accion.fecha_creacion,
                "fecha_vencimiento": accion.fecha_vencimiento
            })
        
        return {
            "status": "success",
            "total_acciones": len(acciones),
            "acciones": acciones_formateadas,
            "archivo_reporte": archivo_reporte,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando acciones sistémicas: {str(e)}")

@router.get("/analisis-completo")
async def obtener_analisis_completo(dias: int = 7):
    """
    Obtiene análisis completo del sistema: patrones + entrelazamiento + acciones
    """
    try:
        print(f"🔍 Iniciando análisis completo de {dias} días...")
        
        # 1. Análisis de patrones
        print("📊 Analizando patrones...")
        analisis_patrones = analizador.analizar_ultimos_estados(dias)
        
        # 2. Entrelazamiento de dominios
        print("🔗 Analizando entrelazamiento de dominios...")
        dominios = entrelazador.analizar_estado_dominios(dias)
        entrelazamientos = entrelazador.detectar_entrelazamientos(dominios)
        acciones_coordinadas = entrelazador.generar_acciones_coordinadas(dominios, entrelazamientos)
        
        # 3. Acciones sistémicas
        print("📝 Generando acciones sistémicas...")
        acciones_sistemicas = documentador.generar_acciones_sistemicas(dias)
        
        # 4. Guardar reportes
        print("💾 Guardando reportes...")
        archivo_patrones = None
        archivo_entrelazamiento = None
        archivo_acciones = None
        
        if "error" not in analisis_patrones:
            archivo_patrones = analizador.guardar_reporte(analisis_patrones)
        
        archivo_entrelazamiento = entrelazador.guardar_reporte_entrelazamiento(
            dominios, entrelazamientos, acciones_coordinadas
        )
        
        archivo_acciones = documentador.guardar_reporte_acciones(acciones_sistemicas)
        
        print("✅ Análisis completo terminado")
        
        # Preparar respuesta completa
        response_data = {
            "status": "success",
            "periodo_analisis": f"{dias} días",
            "timestamp": datetime.now().isoformat(),
            
            "resumen": {
                "estados_cero_analizados": analisis_patrones.get("total_estados", 0),
                "dominios_analizados": len(dominios),
                "entrelazamientos_detectados": len(entrelazamientos),
                "acciones_coordinadas": len(acciones_coordinadas),
                "acciones_sistemicas": len(acciones_sistemicas)
            },
            
            "patrones": analisis_patrones,
            
            "dominios": {
                nombre: {
                    "estado": dominio.estado,
                    "energia": dominio.energia,
                    "urgencia": dominio.urgencia
                } for nombre, dominio in dominios.items()
            },
            
            "entrelazamientos": [
                {
                    "dominios": e.dominios,
                    "tipo": e.tipo,
                    "intensidad": e.intensidad,
                    "descripcion": e.descripcion
                } for e in entrelazamientos
            ],
            
            "acciones_prioritarias": [
                {
                    "nombre": a.nombre,
                    "prioridad": a.prioridad,
                    "urgencia": a.urgencia,
                    "impacto_sistémico": a.impacto_sistémico,
                    "momento_optimo": a.momento_optimo,
                    "tiempo_estimado": a.tiempo_estimado
                } for a in acciones_sistemicas[:5]  # Top 5
            ],
            
            "archivos_generados": {
                "patrones": archivo_patrones,
                "entrelazamiento": archivo_entrelazamiento,
                "acciones": archivo_acciones
            }
        }
        
        # Guardar para dashboard
        try:
            analisis_file = Path("storage/ultimo_analisis.json")
            analisis_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(analisis_file, 'w', encoding='utf-8') as f:
                json.dump(response_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Datos guardados para dashboard en {analisis_file}")
            
        except Exception as e:
            print(f"⚠️ Error guardando datos para dashboard: {e}")
        
        return response_data
    
    except Exception as e:
        print(f"❌ Error en análisis completo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en análisis completo: {str(e)}")

@router.get("/estado-sistema")
async def obtener_estado_sistema():
    """
    Obtiene el estado actual del sistema de entrelazamiento
    """
    try:
        # Verificar archivos recientes
        vault_path = Path(VAULT_PATH)
        estados_dir = vault_path / "Estados-Cero"
        
        archivos_recientes = 0
        if estados_dir.exists():
            # Contar archivos de los últimos 7 días
            for i in range(7):
                fecha = date.today() - timedelta(days=i)
                año = fecha.year
                mes = f"{fecha.month:02d}"
                dia = f"{fecha.day:02d}"
                
                dir_fecha = estados_dir / str(año) / mes
                if dir_fecha.exists():
                    archivos_recientes += len(list(dir_fecha.glob(f"{dia}-*.md")))
        
        return {
            "status": "ok",
            "sistema": "entrelazamiento",
            "vault_path": VAULT_PATH,
            "vault_existe": vault_path.exists(),
            "estados_cero_dir_existe": estados_dir.exists(),
            "archivos_estados_recientes": archivos_recientes,
            "agentes_inicializados": {
                "analizador_patrones": True,
                "entrelazador_dominios": True,
                "documentador_mejorado": True
            },
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estado del sistema: {str(e)}")


@router.get("/dashboard-data")
async def obtener_dashboard_data():
    """
    Obtiene datos para el dashboard Next.js
    Lee el último análisis generado desde storage/ultimo_analisis.json
    """
    try:
        # Leer último análisis generado
        analisis_file = Path("storage/ultimo_analisis.json")
        
        if not analisis_file.exists():
            return {
                "error": "No hay análisis disponible",
                "timestamp": datetime.now().isoformat(),
                "suggestion": "Ejecuta /api/sistema/analisis-completo para generar datos"
            }
        
        with open(analisis_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error leyendo datos del dashboard: {str(e)}")

@router.get("/test-dashboard")
async def test_dashboard():
    """Endpoint de prueba para verificar que el router funciona"""
    return {"status": "ok", "message": "Dashboard test funcionando"}


@router.post("/guardar-analisis")
async def guardar_ultimo_analisis(analisis_data: Dict[str, Any]):
    """
    Guarda el último análisis generado para el dashboard
    """
    try:
        analisis_file = Path("storage/ultimo_analisis.json")
        analisis_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(analisis_file, 'w', encoding='utf-8') as f:
            json.dump(analisis_data, f, indent=2, ensure_ascii=False)
        
        return {
            "status": "success",
            "message": "Análisis guardado para dashboard",
            "file_path": str(analisis_file),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando análisis: {str(e)}")


@router.post("/generar-espejo-diario")
async def generar_espejo_manual(fecha: str = None):
    """
    Genera Espejo Diario manualmente para fecha específica
    Si no se provee fecha, usa hoy
    """
    try:
        if fecha:
            target_date = date.fromisoformat(fecha)
        else:
            target_date = date.today()
        
        print(f"🪞 Generando Espejo Diario para {target_date}...")
        
        # Generar espejo
        espejo_md = espejo_generator.generar_espejo_completo(target_date)
        
        # Guardar en Obsidian
        espejo_path = vault_manager.get_espejo_diario_path(target_date)
        espejo_path.parent.mkdir(parents=True, exist_ok=True)
        espejo_path.write_text(espejo_md, encoding='utf-8')
        
        print(f"✅ Espejo Diario generado en {espejo_path}")
        
        return {
            "status": "success",
            "fecha": target_date.isoformat(),
            "archivo": str(espejo_path),
            "mensaje": f"Espejo Diario generado para {target_date}"
        }
    
    except Exception as e:
        print(f"❌ Error generando Espejo Diario: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generando Espejo Diario: {str(e)}")


@router.get("/espejo-diario")
async def obtener_espejo_diario(fecha: str = None):
    """
    Obtiene el Espejo Diario para una fecha específica
    Si no se provee fecha, usa hoy
    """
    try:
        if fecha:
            target_date = date.fromisoformat(fecha)
        else:
            target_date = date.today()
        
        # Buscar archivo de Espejo Diario
        espejo_path = vault_manager.get_espejo_diario_path(target_date)
        
        if not espejo_path.exists():
            # Intentar generar automáticamente
            print(f"🔄 Espejo Diario no existe para {target_date}, generando...")
            espejo_md = espejo_generator.generar_espejo_completo(target_date)
            espejo_path.parent.mkdir(parents=True, exist_ok=True)
            espejo_path.write_text(espejo_md, encoding='utf-8')
        
        # Leer contenido
        contenido = espejo_path.read_text(encoding='utf-8')
        
        return {
            "status": "success",
            "fecha": target_date.isoformat(),
            "archivo": str(espejo_path),
            "contenido": contenido
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo Espejo Diario: {str(e)}")
