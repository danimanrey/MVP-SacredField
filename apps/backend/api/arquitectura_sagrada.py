"""
🕌 API: ARQUITECTURA SAGRADA - Dashboard Completo

Endpoint consolidado que retorna estado completo del sistema:
- 8 Pilares Fundamentales
- 3 Poderes de Gobierno
- 7 Ministerios Existenciales

Este es el dashboard maestro que muestra la salud
de la arquitectura sagrada completa.

Referencia: carta_magna.md
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import Dict, Any

from models.database import get_db
from models.decreto_sacral import DecretoSacral
from ministerios import obtener_gabinete
from services.verificador_pilares import obtener_verificador

router = APIRouter()


@router.get("/dashboard")
async def dashboard_arquitectura_sagrada(db: Session = Depends(get_db)):
    """
    🕌 DASHBOARD DE ARQUITECTURA SAGRADA
    
    Retorna estado completo del sistema:
    - 8 Pilares: ¿Se honran?
    - 3 Poderes: ¿Están operando correctamente?
    - 7 Ministerios: ¿Cuál es su salud?
    
    Este endpoint es el "corazón" del sistema,
    mostrando la unidad del ser a través de la multiplicidad.
    """
    try:
        # =====================================================================
        # 8 PILARES FUNDAMENTALES
        # =====================================================================
        
        verificador = obtener_verificador()
        
        # Por ahora, verificamos con decisión vacía para obtener info general
        verificacion_pilares = verificador.verificar_todos_pilares({})
        
        pilares_status = {
            "score_global": verificacion_pilares["score_global"],
            "pilares_cumplidos": verificacion_pilares["pilares_cumplidos"],
            "total_pilares": verificacion_pilares["total_pilares"],
            "cumple_arquitectura": verificacion_pilares["cumple_arquitectura"],
            "pilares": [
                {
                    "nombre": p["pilar"],
                    "score": p["score"],
                    "cumple": p["cumple"]
                }
                for p in verificacion_pilares["resultados"]
            ]
        }
        
        # =====================================================================
        # 3 PODERES DE GOBIERNO
        # =====================================================================
        
        decreto_hoy = db.query(DecretoSacral).filter(
            DecretoSacral.fecha == date.today()
        ).first()
        
        if decreto_hoy:
            poderes_status = {
                "legislativo": {
                    "nombre": "El Sultán (Qalb/Corazón)",
                    "decreto_emitido": True,
                    "decreto": decreto_hoy.accion_tangible,
                    "momento": decreto_hoy.momento_liturgico,
                    "validado_pilares": decreto_hoy.validado_contra_pilares,
                    "estado": "✅ Activo"
                },
                "ejecutivo": {
                    "nombre": "El Primer Ministro (Aql/Intelecto)",
                    "estado_ejecucion": decreto_hoy.estado,
                    "jornada_organizada": decreto_hoy.estado == "en_ejecucion",
                    "estado": "✅ Sirviendo" if decreto_hoy.estado == "en_ejecucion" else "⏸️ Esperando"
                },
                "judicial": {
                    "nombre": "El Escribano (Rūḥ/Espíritu)",
                    "verificacion_realizada": decreto_hoy.tiene_verificacion,
                    "cumplimiento": decreto_hoy.cumplimiento_score,
                    "fue_cumplido": decreto_hoy.fue_cumplido,
                    "estado": "✅ Verificado" if decreto_hoy.tiene_verificacion else "⏳ Pendiente Espejo Nocturno"
                }
            }
            separacion_poderes = "✅ Operando correctamente"
        else:
            poderes_status = {
                "legislativo": {
                    "nombre": "El Sultán (Qalb/Corazón)",
                    "decreto_emitido": False,
                    "estado": "⚠️ Pendiente Estado Cero"
                },
                "ejecutivo": {
                    "nombre": "El Primer Ministro (Aql/Intelecto)",
                    "estado": "⏸️ Esperando decreto del Sultán"
                },
                "judicial": {
                    "nombre": "El Escribano (Rūḥ/Espíritu)",
                    "estado": "⏸️ Esperando ejecución"
                }
            }
            separacion_poderes = "⚠️ Sin decreto - Sistema en espera"
        
        # =====================================================================
        # 7 MINISTERIOS EXISTENCIALES
        # =====================================================================
        
        gabinete = obtener_gabinete()
        
        # Si hay decreto, hacer reunión ministerial
        if decreto_hoy:
            try:
                reunion = gabinete.reunion_ministerial(decreto_hoy)
                ministerios_status = {
                    "salud_global": reunion["salud_global"],
                    "ministerios_activos": reunion["ministerios_activos"],
                    "ministerios": [
                        {
                            "nombre": nombre,
                            "nombre_divino": reporte.get("nombre_divino", ""),
                            "salud": round(sum(reporte["metricas"].values()) / len(reporte["metricas"]), 1)
                                if "metricas" in reporte and reporte["metricas"]
                                else 0
                        }
                        for nombre, reporte in reunion["reportes"].items()
                    ]
                }
            except Exception as e:
                ministerios_status = {
                    "salud_global": 0,
                    "ministerios_activos": 0,
                    "error": str(e)
                }
        else:
            ministerios_status = {
                "salud_global": 0,
                "ministerios_activos": 0,
                "mensaje": "Sin decreto - Ministerios en espera"
            }
        
        # =====================================================================
        # WAḤDAT AL-WUJŪD (Unidad del Ser)
        # =====================================================================
        
        # Calcular salud global del organismo (promedio de las 3 dimensiones)
        salud_global_organismo = (
            pilares_status["score_global"] +
            ministerios_status["salud_global"] +
            (100 if decreto_hoy and decreto_hoy.estado == "en_ejecucion" else 50)
        ) / 3
        
        unidad_status = {
            "salud_organismo": round(salud_global_organismo, 1),
            "estado": "🌟 Floreciendo" if salud_global_organismo >= 80
                else "🌱 Creciendo" if salud_global_organismo >= 60
                else "🌾 Emergiendo" if salud_global_organismo >= 40
                else "⚠️ Necesita atención",
            "wahdat_al_wujud": "Unidad del Ser manifestándose en multiplicidad sagrada"
        }
        
        # =====================================================================
        # DASHBOARD COMPLETO
        # =====================================================================
        
        return {
            "arquitectura_sagrada": {
                "version": "1.0.0",
                "estado": "Bajo la observabilidad divina",
                "fecha": date.today().isoformat()
            },
            "unidad_del_ser": unidad_status,
            "pilares": pilares_status,
            "poderes": {
                "separacion": separacion_poderes,
                "legislativo": poderes_status["legislativo"],
                "ejecutivo": poderes_status["ejecutivo"],
                "judicial": poderes_status["judicial"]
            },
            "ministerios": ministerios_status,
            "referencias": {
                "carta_magna": "carta_magna.md",
                "pilares": "core/pilares/",
                "poderes": "core/arquitectura/TRES_PODERES_GOBIERNO_DIVINO.md",
                "ministerios": "core/arquitectura/MAPEO_7_MINISTERIOS.md"
            },
            "invocacion": "إن شاء الله - Si Dios quiere 🕌✨"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar dashboard: {str(e)}"
        )


@router.get("/salud")
async def salud_organismo(db: Session = Depends(get_db)):
    """
    🏥 Salud Global del Organismo
    
    Retorna métricas resumidas de salud.
    """
    try:
        # Obtener dashboard completo
        dashboard = await dashboard_arquitectura_sagrada(db)
        
        return {
            "salud_global": dashboard["unidad_del_ser"]["salud_organismo"],
            "estado": dashboard["unidad_del_ser"]["estado"],
            "pilares_cumplidos": f"{dashboard['pilares']['pilares_cumplidos']}/8",
            "decreto_activo": dashboard["poderes"]["legislativo"].get("decreto_emitido", False),
            "ministerios_activos": dashboard["ministerios"].get("ministerios_activos", 0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

