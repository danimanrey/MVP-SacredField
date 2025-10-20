"""
📚 Sumario de Contexto Incremental
===================================

Sistema para mantener memoria coherente del día sin perder información crítica.

ESTRATEGIA:
- Cada Estado Cero genera un fragmento de contexto
- Los fragmentos se acumulan y comprimen inteligentemente
- Obsidian guarda el historial completo (respaldo permanente)
- Memoria en caliente mantiene lo esencial para próximo Estado Cero

NIVELES DE MEMORIA:
1. Memoria Caliente (en RAM): Últimas 6 horas
2. Memoria Día (DB): Todo el día actual
3. Memoria Permanente (Obsidian): Historial completo
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models.database import EstadoCeroDB
from services.claude_client import ClaudeClient
import json


class FragmentoContexto(BaseModel):
    """Fragmento de contexto de un Estado Cero"""
    momento: str
    hora: datetime
    direccion: str
    respuestas_clave: List[Dict]  # Solo expansión/contracción
    accion_principal: Optional[str] = None
    notas_usuario: List[str] = []


class SumarioContextoDia(BaseModel):
    """Sumario comprimido de todo el día"""
    fecha: date
    fragmentos: List[FragmentoContexto]
    patron_energia: str  # "ascendente", "descendente", "estable", "irregular"
    direcciones_principales: List[str]
    acciones_completadas: List[str]
    acciones_pendientes: List[str]
    insights_clave: List[str]
    token_count_aproximado: int


class GestorSumarioContexto:
    """
    Gestiona la sumarización inteligente del contexto del día.
    
    Comprime información sin perder lo esencial.
    """
    
    def __init__(self, db: Session, claude: ClaudeClient):
        self.db = db
        self.claude = claude
    
    async def obtener_sumario_dia(self, fecha: date = None) -> SumarioContextoDia:
        """
        Obtiene sumario del día comprimido inteligentemente.
        """
        
        if not fecha:
            fecha = date.today()
        
        # Obtener todos los Estados Cero del día
        estados = self.db.query(EstadoCeroDB).filter(
            EstadoCeroDB.fecha >= datetime.combine(fecha, datetime.min.time()),
            EstadoCeroDB.fecha < datetime.combine(fecha + timedelta(days=1), datetime.min.time())
        ).order_by(EstadoCeroDB.fecha).all()
        
        if not estados:
            return SumarioContextoDia(
                fecha=fecha,
                fragmentos=[],
                patron_energia="desconocido",
                direcciones_principales=[],
                acciones_completadas=[],
                acciones_pendientes=[],
                insights_clave=[],
                token_count_aproximado=0
            )
        
        # Extraer fragmentos
        fragmentos = []
        direcciones = []
        
        for estado in estados:
            respuestas = json.loads(estado.respuestas) if estado.respuestas else []
            respuestas_clave = [
                {
                    "sensacion": r.get("sensacion", ""),
                    "intensidad": r.get("intensidad", 0)
                }
                for r in respuestas
            ]
            
            fragmento = FragmentoContexto(
                momento=estado.momento,
                hora=estado.fecha,
                direccion=estado.direccion or "",
                respuestas_clave=respuestas_clave,
                accion_principal=None,  # TODO: Extraer de plan si existe
                notas_usuario=[]
            )
            
            fragmentos.append(fragmento)
            
            if estado.direccion:
                direcciones.append(estado.direccion)
        
        # Detectar patrón de energía
        patron = self._detectar_patron_energia(fragmentos)
        
        # Comprimir si hay muchos fragmentos (>3)
        if len(fragmentos) > 3:
            sumario_comprimido = await self._comprimir_fragmentos(fragmentos, direcciones)
        else:
            sumario_comprimido = {
                "direcciones_principales": direcciones,
                "acciones_completadas": [],
                "acciones_pendientes": [],
                "insights_clave": []
            }
        
        # Estimar tokens (aprox)
        token_count = self._estimar_tokens(fragmentos, sumario_comprimido)
        
        return SumarioContextoDia(
            fecha=fecha,
            fragmentos=fragmentos,
            patron_energia=patron,
            direcciones_principales=sumario_comprimido["direcciones_principales"],
            acciones_completadas=sumario_comprimido.get("acciones_completadas", []),
            acciones_pendientes=sumario_comprimido.get("acciones_pendientes", []),
            insights_clave=sumario_comprimido.get("insights_clave", []),
            token_count_aproximado=token_count
        )
    
    def _detectar_patron_energia(self, fragmentos: List[FragmentoContexto]) -> str:
        """
        Detecta patrón de energía del día basándose en respuestas sacrales.
        """
        
        if len(fragmentos) < 2:
            return "estable"
        
        # Calcular score de expansión por fragmento
        scores = []
        for f in fragmentos:
            expansiones = sum(1 for r in f.respuestas_clave if r.get("sensacion") == "expansion")
            total = len(f.respuestas_clave) or 1
            scores.append(expansiones / total)
        
        # Analizar tendencia
        if len(scores) < 3:
            return "estable"
        
        primera_mitad = sum(scores[:len(scores)//2]) / (len(scores)//2)
        segunda_mitad = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
        
        diferencia = segunda_mitad - primera_mitad
        
        if diferencia > 0.2:
            return "ascendente"
        elif diferencia < -0.2:
            return "descendente"
        elif max(scores) - min(scores) > 0.4:
            return "irregular"
        else:
            return "estable"
    
    async def _comprimir_fragmentos(
        self,
        fragmentos: List[FragmentoContexto],
        direcciones: List[str]
    ) -> Dict:
        """
        Comprime fragmentos usando Claude Haiku (barato).
        
        Extrae lo esencial sin perder coherencia.
        """
        
        # Preparar resumen de fragmentos
        resumen_fragmentos = "\n".join([
            f"- {f.momento.upper()} ({f.hora.strftime('%H:%M')}): {f.direccion[:50]}..."
            for f in fragmentos
        ])
        
        prompt = f"""Tienes {len(fragmentos)} Estados Cero de hoy:

{resumen_fragmentos}

Extrae en 1-2 líneas:
1. Direcciones principales (máx 3)
2. Acciones completadas
3. Pendientes
4. 1 insight clave

JSON:
{{"direcciones_principales": [...], "acciones_completadas": [...], "acciones_pendientes": [...], "insights_clave": [...]}}"""
        
        messages = [{"role": "user", "content": prompt}]
        
        try:
            result = await self.claude.generate_json_haiku(
                system="Comprimes contexto sin perder esencia.",
                messages=messages
            )
            # Asegurar que result es dict
            if isinstance(result, list):
                # Mock devolvió lista, usar fallback
                return {
                    "direcciones_principales": direcciones[:3],
                    "acciones_completadas": [],
                    "acciones_pendientes": [],
                    "insights_clave": ["Día en progreso"]
                }
            return result
        except Exception as e:
            print(f"⚠️ Error comprimiendo contexto: {e}")
            # Fallback
            return {
                "direcciones_principales": direcciones[:3],
                "acciones_completadas": [],
                "acciones_pendientes": [],
                "insights_clave": ["Día en progreso"]
            }
    
    def _estimar_tokens(
        self,
        fragmentos: List[FragmentoContexto],
        sumario: Dict | List
    ) -> int:
        """
        Estima tokens aproximados del contexto.
        """
        
        # Regla general: 1 token ≈ 4 caracteres
        texto_total = ""
        
        for f in fragmentos:
            texto_total += f.direccion
            texto_total += " ".join([str(r) for r in f.respuestas_clave])
        
        if isinstance(sumario, dict):
            for key, value in sumario.items():
                if isinstance(value, list):
                    texto_total += " ".join([str(v) for v in value])
                else:
                    texto_total += str(value)
        elif isinstance(sumario, list):
            texto_total += " ".join([str(item) for item in sumario])
        
        return len(texto_total) // 4
    
    async def generar_contexto_para_estado_cero(
        self,
        momento: str,
        incluir_historia_completa: bool = False
    ) -> str:
        """
        Genera contexto comprimido para el próximo Estado Cero.
        
        Args:
            momento: Momento litúrgico actual
            incluir_historia_completa: Si True, incluye todos los fragmentos (Fajr)
        
        Returns:
            String compacto con contexto relevante (< 200 tokens)
        """
        
        sumario = await self.obtener_sumario_dia()
        
        if not sumario.fragmentos:
            return "Primer Estado Cero del día."
        
        # Para FAJR: incluir más contexto (está iniciando el día)
        if momento == "fajr" or incluir_historia_completa:
            return self._generar_contexto_completo(sumario)
        
        # Para otros momentos: solo lo esencial
        return self._generar_contexto_compacto(sumario, momento)
    
    def _generar_contexto_completo(self, sumario: SumarioContextoDia) -> str:
        """Contexto completo para FAJR (inicio de día)"""
        
        fragmentos_texto = "\n".join([
            f"- {f.momento.upper()}: {f.direccion[:60]}"
            for f in sumario.fragmentos
        ])
        
        return f"""Día hasta ahora:
{fragmentos_texto}

Patrón energía: {sumario.patron_energia}
Direcciones principales: {", ".join(sumario.direcciones_principales[:2])}"""
    
    def _generar_contexto_compacto(self, sumario: SumarioContextoDia, momento: str) -> str:
        """Contexto ultra-compacto para DHUHR/ASR/MAGHRIB/ISHA"""
        
        ultimo_fragmento = sumario.fragmentos[-1] if sumario.fragmentos else None
        
        if not ultimo_fragmento:
            return "Sin contexto previo."
        
        return f"""Último Estado Cero ({ultimo_fragmento.momento}): {ultimo_fragmento.direccion[:80]}
Patrón: {sumario.patron_energia}"""
    
    async def guardar_sumario_permanente(
        self,
        fecha: date,
        vault_path: str
    ) -> str:
        """
        Guarda sumario del día en Obsidian (cierre en Maghrib/Isha).
        """
        
        sumario = await self.obtener_sumario_dia(fecha)
        
        contenido = self._generar_markdown_sumario(sumario)
        
        # Filepath
        import os
        fecha_str = fecha.strftime("%Y-%m-%d")
        filepath = os.path.join(
            vault_path,
            "40-Journal",
            f"{fecha_str}-sumario-dia.md"
        )
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        return filepath
    
    def _generar_markdown_sumario(self, sumario: SumarioContextoDia) -> str:
        """Genera Markdown del sumario del día"""
        
        fragmentos_md = "\n".join([
            f"### {f.momento.upper()} - {f.hora.strftime('%H:%M')}\n\n{f.direccion}\n"
            for f in sumario.fragmentos
        ])
        
        return f"""---
tipo: sumario-dia
fecha: {sumario.fecha}
patron_energia: {sumario.patron_energia}
---

# Sumario del Día: {sumario.fecha.strftime('%d de %B, %Y')}

## Patrón de Energía

{sumario.patron_energia.capitalize()}

## Estados Cero del Día

{fragmentos_md}

## Direcciones Principales

{chr(10).join([f"- {d}" for d in sumario.direcciones_principales])}

## Acciones Completadas

{chr(10).join([f"- ✅ {a}" for a in sumario.acciones_completadas]) if sumario.acciones_completadas else "- (Ninguna registrada)"}

## Pendientes

{chr(10).join([f"- ⏳ {p}" for p in sumario.acciones_pendientes]) if sumario.acciones_pendientes else "- (Ninguno)"}

## Insights Clave

{chr(10).join([f"- 💡 {i}" for i in sumario.insights_clave]) if sumario.insights_clave else "- (Ninguno)"}

---

**Tokens aproximados**: {sumario.token_count_aproximado}
*Generado por Campo Sagrado - {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

