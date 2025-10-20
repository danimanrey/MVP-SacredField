from datetime import datetime, date, timedelta
from typing import Dict, Optional
import json
from sqlalchemy.orm import Session

from models.schemas import ReporteDiario
from models.database import EstadoCeroDB, SesionDB, NoNegociableTrackingDB, BiometriaDB
from services.claude_client import ClaudeClient


class AgenteGuardian:
    """
    Agente Vigilante del Ciclo
    Monitorea salud, genera reportes, detecta mejoras
    """
    
    def __init__(self, db: Session, claude: ClaudeClient):
        self.db = db
        self.claude = claude
        
    async def generar_reporte_diario(self, fecha: date) -> ReporteDiario:
        """
        Genera reporte diario ANTES de Maghrib
        Cierra el día que termina
        """
        
        # Recopilar datos del día
        datos = await self._recopilar_datos_dia(fecha)
        
        # Generar contenido con Claude
        contenido = await self._generar_contenido_reporte(datos)
        
        # Manejar estructura de respuesta de Claude
        resonancias = []
        obstrucciones = []
        semilla = "Continúa honrando tu autoridad sacral"
        
        if isinstance(contenido, dict):
            resonancias = contenido.get("resonancias", ["Sistema funcionando correctamente"])
            obstrucciones = contenido.get("obstrucciones", ["Ninguna obstrucción detectada"])
            semilla = contenido.get("semilla", "Continúa honrando tu autoridad sacral")
        elif isinstance(contenido, list):
            # Si es una lista, usar como resonancias
            resonancias = contenido[:3]  # Tomar las primeras 3
            obstrucciones = ["Sistema operativo"]
        
        # Construir reporte
        return ReporteDiario(
            fecha=fecha,
            estados_cero_completados=datos["estados_cero_completados"],
            sesiones=datos["sesiones"],
            no_negociables_cumplidos=datos["no_neg_cumplidos"],
            no_negociables_totales=datos["no_neg_totales"],
            biologia=datos["biologia"],
            finanzas=datos["finanzas"],
            conocimiento=datos["conocimiento"],
            resonancias=resonancias,
            obstrucciones=obstrucciones,
            semilla_mañana=semilla,
            generado_timestamp=datetime.now()
        )
    
    async def _recopilar_datos_dia(self, fecha: date) -> Dict:
        """Recopila todos los datos del día"""
        
        # Estados Cero
        estados_cero = self.db.query(EstadoCeroDB).filter(
            EstadoCeroDB.fecha >= datetime.combine(fecha, datetime.min.time()),
            EstadoCeroDB.fecha < datetime.combine(fecha + timedelta(days=1), datetime.min.time())
        ).all()
        
        # Sesiones
        sesiones = self.db.query(SesionDB).filter(
            SesionDB.fecha == fecha
        ).all()
        
        # No-negociables
        no_neg_tracking = self.db.query(NoNegociableTrackingDB).filter(
            NoNegociableTrackingDB.fecha == fecha
        ).all()
        
        # Biometría
        biometria = self.db.query(BiometriaDB).filter(
            BiometriaDB.fecha == fecha
        ).first()
        
        return {
            "estados_cero_completados": len(estados_cero),
            "sesiones": [self._sesion_to_dict(s) for s in sesiones],
            "no_neg_cumplidos": sum(1 for nn in no_neg_tracking if nn.completado),
            "no_neg_totales": len(no_neg_tracking),
            "biologia": {
                "hrv": biometria.hrv if biometria else None,
                "calidad_sueno": biometria.calidad_sueno if biometria else None,
                "energia_promedio": self._calcular_energia_promedio(biometria),
                "luz_solar": biometria.luz_solar_am if biometria else False,
                "ejercicio": biometria.ejercicio if biometria else False
            },
            "finanzas": {
                "runway": 4.5,  # TODO: Calcular real
                "tiempo_generacion": sum(s.duracion_minutos or 0 for s in sesiones) / 60
            },
            "conocimiento": {
                "capturas_nuevas": 0,  # TODO: Integrar Anytype
                "metabolizadas": 0,
                "cristalizaciones": 0
            }
        }
    
    async def _generar_contenido_reporte(self, datos: Dict) -> Dict:
        """Genera el contenido contemplativo del reporte"""
        
        prompt = f"""Eres el Agente Guardián. Es Maghrib, momento de cierre.

DATOS DEL DÍA:
{json.dumps(datos, indent=2)}

Genera reporte contemplativo del día. Responde con JSON:
{{
  "resonancias": ["Lo que resonó profundamente", "Otro insight"],
  "obstrucciones": ["Lo que no fluyó", "Patrón observado"],
  "semilla": "Una intención emergente para mañana"
}}

TONO: Contemplativo, agradecido, honesto, curioso. Sin juicio.
"""
        
        messages = [{"role": "user", "content": prompt}]
        return await self.claude.generate_json(
            system="Generas reportes contemplativos del día.",
            messages=messages
        )
    
    def _sesion_to_dict(self, sesion: SesionDB) -> Dict:
        """Convierte sesión DB a dict"""
        return {
            "id": sesion.id,
            "inicio": sesion.inicio.isoformat(),
            "duracion": sesion.duracion_minutos,
            "rol": sesion.rol,
            "calidad_flujo": sesion.calidad_flujo
        }
    
    def _calcular_energia_promedio(self, biometria: Optional[BiometriaDB]) -> float:
        """Calcula energía promedio del día"""
        if not biometria:
            return 3.0
        # TODO: Implementar tracking de energía durante el día
        return float(biometria.energia_despertar or 3)
    
    async def monitorear_salud_sistema(self) -> Dict:
        """
        Monitorea la salud general del sistema
        """
        
        hoy = date.today()
        
        # Estados Cero de hoy
        estados_hoy = self.db.query(EstadoCeroDB).filter(
            EstadoCeroDB.fecha >= datetime.combine(hoy, datetime.min.time())
        ).count()
        
        # Sesiones de hoy
        sesiones_hoy = self.db.query(SesionDB).filter(
            SesionDB.fecha == hoy
        ).count()
        
        # No-negociables de hoy
        no_neg_hoy = self.db.query(NoNegociableTrackingDB).filter(
            NoNegociableTrackingDB.fecha == hoy
        ).all()
        
        cumplidos = sum(1 for nn in no_neg_hoy if nn.completado)
        total = len(no_neg_hoy)
        
        return {
            "fecha": hoy.isoformat(),
            "estados_cero": estados_hoy,
            "sesiones": sesiones_hoy,
            "no_negociables": {
                "cumplidos": cumplidos,
                "total": total,
                "porcentaje": (cumplidos / total * 100) if total > 0 else 0
            },
            "salud_general": "buena" if estados_hoy > 0 and cumplidos / max(total, 1) > 0.7 else "requiere_atencion"
        }
    
    async def detectar_patrones(self, dias_atras: int = 7) -> Dict:
        """
        Detecta patrones en los últimos N días
        """
        
        fecha_inicio = date.today() - timedelta(days=dias_atras)
        
        # Recopilar datos del período
        estados = self.db.query(EstadoCeroDB).filter(
            EstadoCeroDB.fecha >= fecha_inicio
        ).all()
        
        sesiones = self.db.query(SesionDB).filter(
            SesionDB.fecha >= fecha_inicio
        ).all()
        
        # Análisis básico
        promedio_estados_dia = len(estados) / dias_atras
        
        # Días más productivos
        dias_productivos = {}
        for sesion in sesiones:
            dia = sesion.fecha.isoformat()
            if dia not in dias_productivos:
                dias_productivos[dia] = 0
            dias_productivos[dia] += sesion.duracion_minutos or 0
        
        dia_mas_productivo = max(dias_productivos.items(), key=lambda x: x[1]) if dias_productivos else None
        
        return {
            "periodo_dias": dias_atras,
            "promedio_estados_cero_dia": round(promedio_estados_dia, 2),
            "total_estados_cero": len(estados),
            "total_sesiones": len(sesiones),
            "dia_mas_productivo": dia_mas_productivo,
            "patrones_detectados": [
                "Mayor actividad en días laborables" if promedio_estados_dia > 3 else "Actividad constante",
                "Buena consistencia en Estados Cero" if promedio_estados_dia > 2 else "Necesita más Estados Cero"
            ]
        }
