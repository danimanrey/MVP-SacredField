"""
📜 MODELO: DECRETO SACRAL

Representa un decreto emitido por el Poder Legislativo (Sultán/Corazón)
en Estado Cero, que será ejecutado por el Poder Ejecutivo (Primer Ministro/Intelecto)
y verificado por el Poder Judicial (Escribano/Espíritu).

Arquitectura Sagrada - 3 Poderes de Gobierno:
- LEGISLATIVO (Sultán) → Emite decreto
- EJECUTIVO (Primer Ministro) → Organiza manifestación
- JUDICIAL (Escribano) → Verifica cumplimiento

Referencia: core/arquitectura/TRES_PODERES_GOBIERNO_DIVINO.md
"""

from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from models.database import Base


class DecretoSacral(Base):
    """
    Decreto emitido por el Sultán (Poder Legislativo) en Estado Cero.
    
    Flujo:
    1. Sultán emite decreto (LEGISLATIVO)
    2. Primer Ministro organiza jornada (EJECUTIVO)
    3. Escribano verifica cumplimiento (JUDICIAL)
    """
    
    __tablename__ = "decretos_sacrales"
    
    # Identificación
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False, index=True)
    momento_liturgico = Column(String(20))  # fajr, dhuhr, asr, maghrib, isha
    
    # PODER LEGISLATIVO (Sultán/Corazón)
    direccion_emergente = Column(Text)  # Dirección recibida en Estado Cero
    accion_tangible = Column(Text, nullable=False)  # Decreto claro y específico
    validado_contra_pilares = Column(Boolean, default=False)  # ¿Validó contra 8 Pilares?
    
    # PODER EJECUTIVO (Primer Ministro/Intelecto)
    estado = Column(String(20), default="pendiente")  # pendiente, en_ejecucion, completado, cancelado
    notas_ejecucion = Column(Text)  # Notas del Primer Ministro durante ejecución
    fecha_inicio_ejecucion = Column(DateTime)
    fecha_fin_ejecucion = Column(DateTime)
    
    # PODER JUDICIAL (Escribano/Espíritu)
    verificacion_judicial = Column(Text)  # Reporte del Escribano (Espejo Nocturno)
    cumplimiento_score = Column(Integer)  # 0-100: % de cumplimiento
    sabiduria_extraida = Column(Text)  # Insights y aprendizajes
    fecha_verificacion = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DecretoSacral {self.fecha}: {self.accion_tangible[:50]}>"
    
    # Métodos de estado
    
    @property
    def fue_cumplido(self) -> bool:
        """¿El decreto fue cumplido?"""
        return self.estado == "completado" and (self.cumplimiento_score or 0) >= 70
    
    @property
    def tiene_verificacion(self) -> bool:
        """¿Tiene verificación judicial?"""
        return self.verificacion_judicial is not None
    
    @property
    def esta_activo(self) -> bool:
        """¿El decreto está activo (no completado ni cancelado)?"""
        return self.estado in ["pendiente", "en_ejecucion"]
    
    def iniciar_ejecucion(self):
        """Primer Ministro inicia ejecución del decreto"""
        self.estado = "en_ejecucion"
        self.fecha_inicio_ejecucion = datetime.utcnow()
    
    def completar_ejecucion(self, notas: str = None):
        """Primer Ministro completa ejecución del decreto"""
        self.estado = "completado"
        self.fecha_fin_ejecucion = datetime.utcnow()
        if notas:
            self.notas_ejecucion = notas
    
    def cancelar_decreto(self, razon: str = None):
        """Cancelar decreto (raro, solo si Sultán lo decide)"""
        self.estado = "cancelado"
        if razon:
            self.notas_ejecucion = f"CANCELADO: {razon}"
    
    def registrar_verificacion(
        self,
        verificacion: str,
        cumplimiento_score: int,
        sabiduria: str = None
    ):
        """Escribano registra verificación judicial"""
        self.verificacion_judicial = verificacion
        self.cumplimiento_score = cumplimiento_score
        if sabiduria:
            self.sabiduria_extraida = sabiduria
        self.fecha_verificacion = datetime.utcnow()

