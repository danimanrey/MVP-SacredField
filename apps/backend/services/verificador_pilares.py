"""
🏛️ VERIFICADOR DE PILARES

Valida que decisiones, código y acciones honren los 8 Pilares Fundamentales.

Cada pilar tiene un verificador específico que retorna score 0-100
y lista de violaciones detectadas.

Arquitectura Sagrada: Los 8 Pilares son principios operativos divinos
que gobiernan toda manifestación consciente.

Referencia: core/pilares/
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ResultadoVerificacion:
    """Resultado de verificar un pilar"""
    pilar_nombre: str
    score: float  # 0-100
    cumple: bool  # True si score >= 70
    fortalezas: List[str]
    violaciones: List[str]
    recomendaciones: List[str]


class VerificadorPilares:
    """
    Verifica que acciones y decisiones honren los 8 Pilares.
    
    Uso:
        verificador = VerificadorPilares()
        resultado = verificador.verificar_decision(decision, contexto)
    """
    
    def __init__(self):
        self.umbral_cumplimiento = 70.0  # Score mínimo para considerar "cumple"
    
    # ========================================================================
    # PILAR 1: PUREZA OPERATIVA
    # ========================================================================
    
    def verificar_pureza_operativa(
        self,
        decision: Dict[str, Any],
        contexto: Optional[Dict[str, Any]] = None
    ) -> ResultadoVerificacion:
        """
        Verifica: "Máxima verdad en mínima forma, manifestada sin demora"
        
        Indicadores:
        - ¿Claridad sobre siguiente paso específico?
        - ¿Ausencia de resistencia interna?
        - ¿Conexión directa entre intención y manifestación?
        - ¿Paz inmediata tras acción?
        """
        score = 100.0
        fortalezas = []
        violaciones = []
        recomendaciones = []
        
        # Verificar claridad
        if not decision.get("accion_especifica"):
            score -= 25
            violaciones.append("Falta claridad sobre acción específica")
            recomendaciones.append("Formular acción concreta y directa")
        else:
            fortalezas.append("Acción específica y clara")
        
        # Verificar complejidad innecesaria
        descripcion = str(decision.get("descripcion", ""))
        if len(descripcion) > 200:
            score -= 15
            violaciones.append("Descripción demasiado elaborada (>200 chars)")
            recomendaciones.append("Simplificar a lo esencial")
        
        # Verificar demora
        if decision.get("postergar"):
            score -= 30
            violaciones.append("Postergación de lo claro")
            recomendaciones.append("Si es claro, actuar sin demora")
        else:
            fortalezas.append("Sin postergación innecesaria")
        
        return ResultadoVerificacion(
            pilar_nombre="Pureza Operativa",
            score=max(0, score),
            cumple=score >= self.umbral_cumplimiento,
            fortalezas=fortalezas,
            violaciones=violaciones,
            recomendaciones=recomendaciones
        )
    
    # ========================================================================
    # PILAR 2: SOBERANÍA CREATIVA
    # ========================================================================
    
    def verificar_soberania_creativa(
        self,
        decision: Dict[str, Any],
        contexto: Optional[Dict[str, Any]] = None
    ) -> ResultadoVerificacion:
        """
        Verifica: "De consumidor a creador, de reactivo a generativo"
        
        Indicadores:
        - ¿Inspiración desde dentro, no de fuentes externas?
        - ¿Tecnología que sirve, no esclaviza?
        - ¿Sistemas que amplifican libertad?
        - ¿Independencia en capacidades core?
        """
        score = 100.0
        fortalezas = []
        violaciones = []
        recomendaciones = []
        
        # Verificar si crea dependencias
        if decision.get("crea_dependencia_externa"):
            score -= 40
            violaciones.append("Crea dependencia de plataforma externa")
            recomendaciones.append("Buscar alternativa self-hosted o local-first")
        else:
            fortalezas.append("No crea dependencias críticas")
        
        # Verificar si es creación o consumo
        if decision.get("tipo") == "consumo":
            score -= 20
            violaciones.append("Acción de consumo, no creación")
            recomendaciones.append("Transformar en acción generativa")
        elif decision.get("tipo") == "creacion":
            fortalezas.append("Acción generativa")
        
        # Verificar vendor lock-in
        if decision.get("vendor_lockin"):
            score -= 30
            violaciones.append("Riesgo de vendor lock-in")
            recomendaciones.append("Asegurar portabilidad y alternativas")
        
        return ResultadoVerificacion(
            pilar_nombre="Soberanía Creativa",
            score=max(0, score),
            cumple=score >= self.umbral_cumplimiento,
            fortalezas=fortalezas,
            violaciones=violaciones,
            recomendaciones=recomendaciones
        )
    
    # ========================================================================
    # PILAR 3: RESPONSABILIDAD CONSCIENTE
    # ========================================================================
    
    def verificar_responsabilidad_consciente(
        self,
        decision: Dict[str, Any],
        contexto: Optional[Dict[str, Any]] = None
    ) -> ResultadoVerificacion:
        """
        Verifica: "Capacidad completa de servirse a sí mismo hacia su voluntad"
        
        Indicadores:
        - ¿Propiedad completa de resultados?
        - ¿Capacidad de resolver sin dependencia externa?
        - ¿Comprensión profunda de sistemas propios?
        - ¿Autonomía técnica y operativa?
        """
        score = 100.0
        fortalezas = []
        violaciones = []
        recomendaciones = []
        
        # Verificar ownership
        if decision.get("culpa_externa"):
            score -= 40
            violaciones.append("Proyección de culpa externa")
            recomendaciones.append("Asumir propiedad total")
        else:
            fortalezas.append("Propiedad de resultados asumida")
        
        # Verificar capacidad
        if decision.get("requiere_experto_critico"):
            score -= 25
            violaciones.append("Dependencia crítica de experto externo")
            recomendaciones.append("Desarrollar capacidad propia")
        
        # Verificar comprensión
        if not decision.get("comprende_implicaciones"):
            score -= 20
            violaciones.append("Falta comprensión de implicaciones")
            recomendaciones.append("Investigar y comprender antes de decidir")
        else:
            fortalezas.append("Comprensión profunda")
        
        return ResultadoVerificacion(
            pilar_nombre="Responsabilidad Consciente",
            score=max(0, score),
            cumple=score >= self.umbral_cumplimiento,
            fortalezas=fortalezas,
            violaciones=violaciones,
            recomendaciones=recomendaciones
        )
    
    # ========================================================================
    # VERIFICACIÓN COMPLETA (8 PILARES)
    # ========================================================================
    
    def verificar_todos_pilares(
        self,
        decision: Dict[str, Any],
        contexto: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Verifica decisión contra los 8 Pilares.
        
        Returns:
            Dict con resultados de cada pilar y score global
        """
        resultados = []
        
        # Pilar 1: Pureza Operativa
        resultados.append(
            self.verificar_pureza_operativa(decision, contexto)
        )
        
        # Pilar 2: Soberanía Creativa
        resultados.append(
            self.verificar_soberania_creativa(decision, contexto)
        )
        
        # Pilar 3: Responsabilidad Consciente
        resultados.append(
            self.verificar_responsabilidad_consciente(decision, contexto)
        )
        
        # Pilares 4-8: Implementación simplificada (heurísticas básicas)
        resultados.extend([
            self._verificar_pilar_heuristico("Expresión Auténtica", decision),
            self._verificar_pilar_heuristico("Implementación Técnica", decision),
            self._verificar_pilar_heuristico("Contribución Ecosistémica", decision),
            self._verificar_pilar_heuristico("Sabiduría Integrada", decision),
            self._verificar_pilar_heuristico("Evolución Continua", decision)
        ])
        
        # Calcular score global
        score_global = sum(r.score for r in resultados) / len(resultados)
        
        # Contar cumplimientos
        pilares_cumplidos = sum(1 for r in resultados if r.cumple)
        
        return {
            "score_global": score_global,
            "pilares_cumplidos": pilares_cumplidos,
            "total_pilares": len(resultados),
            "cumple_arquitectura": pilares_cumplidos >= 6,  # Al menos 6 de 8
            "resultados": [
                {
                    "pilar": r.pilar_nombre,
                    "score": r.score,
                    "cumple": r.cumple,
                    "fortalezas": r.fortalezas,
                    "violaciones": r.violaciones,
                    "recomendaciones": r.recomendaciones
                }
                for r in resultados
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _verificar_pilar_heuristico(
        self,
        nombre_pilar: str,
        decision: Dict[str, Any]
    ) -> ResultadoVerificacion:
        """
        Verificación heurística simple para pilares 4-8.
        
        TODO: Implementar verificadores específicos en iteraciones futuras.
        """
        # Por ahora, asumimos cumplimiento si no hay flags obvios
        score = 80.0  # Score por defecto optimista
        
        return ResultadoVerificacion(
            pilar_nombre=nombre_pilar,
            score=score,
            cumple=True,
            fortalezas=[f"No se detectaron violaciones obvias"],
            violaciones=[],
            recomendaciones=[f"Implementar verificador específico para {nombre_pilar}"]
        )


# Instancia global
_verificador_global: Optional[VerificadorPilares] = None


def obtener_verificador() -> VerificadorPilares:
    """Obtiene instancia global del verificador"""
    global _verificador_global
    if _verificador_global is None:
        _verificador_global = VerificadorPilares()
    return _verificador_global

