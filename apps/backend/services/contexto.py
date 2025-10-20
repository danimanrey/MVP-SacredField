from __future__ import annotations

from typing import Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from models.schemas import (
    ContextoCompleto, ContextoTemporal, ContextoBiologico,
    ContextoFinanciero, ContextoConocimiento, MomentoLiturgico
)


class RecopiladorContexto:
    """Recopila contexto completo usando sistema de 7 capas."""

    def __init__(self, db: Session, calculador, calendario):
        self.db = db
        self.calculador = calculador
        self.calendario = calendario

    async def recopilar_contexto_completo(
        self,
        momento: MomentoLiturgico,
        energia: Optional[int] = None,
        calidad_sueno: Optional[int] = None,
        resonancia_corporal: Optional[str] = None,
        estado_emocional: Optional[str] = None,
        intensidad_emocional: Optional[int] = None
    ) -> ContextoCompleto:
        """
        Recopila contexto completo usando el orquestador de 7 capas.

        Si se proporcionan inputs del usuario (energía, sueño, etc.), se usan.
        Si no, se usan valores por defecto del sistema.
        """
        from services.orquestador_7_capas import obtener_contexto_7_capas

        # Usar función de orquestador de 7 capas para obtener contexto completo
        contexto_7_capas = obtener_contexto_7_capas(
            momento=momento.value,
            energia=energia,
            calidad_sueno=calidad_sueno,
            resonancia_corporal=resonancia_corporal,
            estado_emocional=estado_emocional,
            intensidad_emocional=intensidad_emocional
        )

        # Mapear contexto de 7 capas a ContextoCompleto (schema legacy)
        # Esto mantiene compatibilidad con el resto del sistema

        # Temporal - de Capa 1 (Física)
        capa_fisica = contexto_7_capas["capas"]["1_fisica"]
        temporal = ContextoTemporal(
            momento_liturgico=momento,
            dia_semana=capa_fisica["dia_semana"],
            mes_hijri=capa_fisica.get("mes_hijri", ""),
            cualidad_momento=capa_fisica.get("hora_planetaria", ""),
            cualidad_mes=capa_fisica.get("cualidad_mes_hijri", "")
        )

        # Biológico - de Capa 3 (Biológica)
        capa_biologica = contexto_7_capas["capas"]["3_biologica"]
        energia_valor = energia if energia is not None else 3
        biologico = ContextoBiologico(
            energia_actual=energia_valor,
            hrv=None,
            luz_solar_hoy=False,
            ejercicio_hoy=False
        )

        # Financiero - datos mínimos (se enriquecerá en Tier 1)
        financiero = ContextoFinanciero(
            runway_meses=6.0,
            urgencia_financiera=False,
            proyectos_activos=[]
        )

        # Conocimiento - datos mínimos (se enriquecerá en Tier 1)
        conocimiento = ContextoConocimiento(
            capturas_sin_procesar=0,
            insights_listos=0
        )

        # Tiempo disponible aproximado: hasta siguiente momento
        proximo = self.calculador.proximo_estado_cero()
        minutos = int((proximo.hora - self.calculador._hoy()).total_seconds() // 60)
        minutos = max(minutos, 15)

        return ContextoCompleto(
            temporal=temporal,
            biologico=biologico,
            financiero=financiero,
            conocimiento=conocimiento,
            tiempo_disponible_hoy=minutos
        )


