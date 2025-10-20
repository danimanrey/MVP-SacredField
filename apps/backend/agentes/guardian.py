from datetime import datetime, date, timedelta
from typing import Dict, Optional
import json
from sqlalchemy.orm import Session

from models.schemas import ReporteDiario
from models.database import EstadoCeroDB, SesionDB, NoNegociableTrackingDB, BiometriaDB
from models.decreto_sacral import DecretoSacral  # 🏛️ Arquitectura Sagrada
from services.claude_client import ClaudeClient


class AgenteGuardian:
    """
    🕌 AGENTE GUARDIAN - El Escribano (Sirr/Secreto)
    
    PODER JUDICIAL del gobierno del reino humano.
    
    Responsabilidades:
    - VERIFICA que el decreto fue respetado
    - REGISTRA la ejecución y resultados
    - EXTRAE sabiduría del día (Espejo Nocturno)
    - CIERRA el ciclo diario con integridad
    
    Arquitectura Sagrada:
    - Parte de los 3 Poderes de Gobierno
    - Verifica al Ejecutivo (Orquestador)
    - Guarda la memoria sagrada del sistema
    
    Referencia: core/arquitectura/TRES_PODERES_GOBIERNO_DIVINO.md
    """
    
    def __init__(self, db: Session, claude: ClaudeClient):
        self.db = db
        self.claude = claude
        
    async def generar_reporte_diario(self, fecha: date) -> ReporteDiario:
        """
        🕌 PODER JUDICIAL: Genera Espejo Nocturno
        
        VERIFICACIÓN COMPLETA:
        1. Obtiene decreto del día
        2. Recopila datos de ejecución
        3. VERIFICA cumplimiento del decreto
        4. Registra en decreto (observaciones)
        5. Genera Espejo Nocturno (sabiduría)
        
        Se ejecuta ANTES de Maghrib para cerrar el día.
        """
        # 1. Obtener decreto del día (si existe)
        decreto = self.db.query(DecretoSacral).filter(
            DecretoSacral.fecha == fecha,
            DecretoSacral.estado.in_(["pendiente", "en_ejecucion"])
        ).first()
        
        # Recopilar datos del día
        datos = await self._recopilar_datos_dia(fecha)
        
        # 2. VERIFICAR cumplimiento del decreto (si existe)
        if decreto:
            verificacion = await self._verificar_cumplimiento_decreto(decreto, datos)
            datos["verificacion_decreto"] = verificacion
        else:
            datos["verificacion_decreto"] = {
                "decreto_presente": False,
                "mensaje": "No había decreto para hoy"
            }
        
        # 3. Generar contenido con Claude
        contenido = await self._generar_contenido_reporte(datos)
        
        # Manejar estructura de respuesta de Claude
        resonancias = []
        obstrucciones = []
        semilla = "Continúa honrando tu autoridad sacral"
        
        if isinstance(contenido, dict):
            resonancias_raw = contenido.get("resonancias", ["Sistema funcionando correctamente"])
            obstrucciones_raw = contenido.get("obstrucciones", ["Ninguna obstrucción detectada"])
            semilla = contenido.get("semilla", "Continúa honrando tu autoridad sacral")
            
            # Convertir a strings si son dicts (mock de Claude a veces retorna dicts)
            resonancias = [
                r if isinstance(r, str) else r.get("pregunta", str(r))
                for r in resonancias_raw
            ]
            obstrucciones = [
                o if isinstance(o, str) else o.get("pregunta", str(o))
                for o in obstrucciones_raw
            ]
        elif isinstance(contenido, list):
            # Si es una lista, usar como resonancias
            resonancias_raw = contenido[:3]  # Tomar las primeras 3
            resonancias = [
                r if isinstance(r, str) else r.get("pregunta", str(r))
                for r in resonancias_raw
            ]
            obstrucciones = ["Sistema operativo"]
        
        # 4. REGISTRAR verificación en decreto (si existe)
        if decreto:
            observaciones = {
                "verificacion_judicial": datos["verificacion_decreto"],
                "espejo_nocturno": {
                    "resonancias": resonancias,
                    "obstrucciones": obstrucciones,
                    "semilla_mañana": semilla
                },
                "timestamp": datetime.now().isoformat()
            }
            
            decreto.observaciones_judiciales = json.dumps(observaciones, ensure_ascii=False, indent=2)
            decreto.verificado_por_escribano = True
            decreto.estado = "completado"
            
            self.db.commit()
            
            print(f"⚖️ PODER JUDICIAL: Decreto {decreto.id} verificado y cerrado")
        
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
    
    async def _verificar_cumplimiento_decreto(
        self,
        decreto: DecretoSacral,
        datos_dia: Dict
    ) -> Dict:
        """
        🕌 PODER JUDICIAL: Verifica cumplimiento del decreto
        
        Compara lo DECRETADO vs lo EJECUTADO.
        
        Args:
            decreto: DecretoSacral del día
            datos_dia: Datos recopilados del día
            
        Returns:
            Dict con resultado de la verificación
        """
        # Análisis básico de cumplimiento
        estados_cero = datos_dia.get("estados_cero_completados", 0)
        sesiones = datos_dia.get("sesiones", 0)
        no_neg_porcentaje = 0
        
        if datos_dia.get("no_neg_totales", 0) > 0:
            no_neg_porcentaje = (
                datos_dia["no_neg_cumplidos"] / datos_dia["no_neg_totales"]
            ) * 100
        
        # Criterios de cumplimiento
        cumplimiento_alto = (
            estados_cero >= 1 and  # Al menos 1 Estado Cero
            no_neg_porcentaje >= 70  # Al menos 70% de no-negociables
        )
        
        cumplimiento_medio = (
            estados_cero >= 1 or
            no_neg_porcentaje >= 50
        )
        
        if cumplimiento_alto:
            nivel = "ALTO"
            mensaje = "Decreto ejecutado con excelencia (Ihsān)"
        elif cumplimiento_medio:
            nivel = "MEDIO"
            mensaje = "Decreto ejecutado parcialmente"
        else:
            nivel = "BAJO"
            mensaje = "Decreto no ejecutado - requiere atención"
        
        verificacion = {
            "decreto_presente": True,
            "decreto_id": decreto.id,
            "accion_decretada": decreto.accion_tangible,
            "direccion_emergente": decreto.direccion_emergente,
            "nivel_cumplimiento": nivel,
            "mensaje": mensaje,
            "metricas": {
                "estados_cero": estados_cero,
                "sesiones": sesiones,
                "no_negociables_porcentaje": round(no_neg_porcentaje, 1)
            }
        }
        
        print(f"⚖️ VERIFICACIÓN JUDICIAL: {nivel}")
        print(f"   Decreto: {decreto.accion_tangible}")
        print(f"   Métricas: EC={estados_cero}, NN={no_neg_porcentaje:.0f}%")
        
        return verificacion
