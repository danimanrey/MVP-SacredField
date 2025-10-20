"""
Integración con Anytype para captura con propósito
"""
import os
import httpx
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from dataclasses import dataclass

@dataclass
class CapturaAnytype:
    """Representa una captura de Anytype"""
    id: str
    titulo: str
    contenido: str
    tipo: str  # 'nota', 'enlace', 'imagen', 'audio'
    timestamp: datetime
    etiquetas: List[str]
    contexto: Optional[str] = None
    procesado: bool = False

class AnytypeClient:
    """
    Cliente para interactuar con Anytype API
    Permite capturar información con propósito específico
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANYTYPE_API_KEY")
        self.base_url = "https://api.anytype.io/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        } if self.api_key else {}
        
    async def obtener_capturas_pendientes(
        self, 
        desde: Optional[datetime] = None,
        limit: int = 50
    ) -> List[CapturaAnytype]:
        """
        Obtiene capturas pendientes de procesar
        """
        if not self.api_key:
            return await self._simular_capturas_pendientes()
        
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "limit": limit,
                    "status": "pending"
                }
                if desde:
                    params["since"] = desde.isoformat()
                
                response = await client.get(
                    f"{self.base_url}/captures",
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                
                data = response.json()
                return [
                    CapturaAnytype(
                        id=item["id"],
                        titulo=item["title"],
                        contenido=item["content"],
                        tipo=item["type"],
                        timestamp=datetime.fromisoformat(item["created_at"]),
                        etiquetas=item.get("tags", []),
                        contexto=item.get("context"),
                        procesado=item.get("processed", False)
                    )
                    for item in data.get("captures", [])
                ]
                
        except Exception as e:
            print(f"Error obteniendo capturas de Anytype: {e}")
            return await self._simular_capturas_pendientes()
    
    async def procesar_captura(
        self, 
        captura_id: str,
        accion: str = "metabolizar"
    ) -> Dict[str, Any]:
        """
        Procesa una captura con una acción específica
        """
        if not self.api_key:
            return await self._simular_procesamiento(captura_id, accion)
        
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "action": accion,
                    "timestamp": datetime.now().isoformat()
                }
                
                response = await client.post(
                    f"{self.base_url}/captures/{captura_id}/process",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                
                return response.json()
                
        except Exception as e:
            print(f"Error procesando captura {captura_id}: {e}")
            return {"error": str(e)}
    
    async def crear_captura_con_proposito(
        self,
        contenido: str,
        proposito: str,
        contexto: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crea una nueva captura con propósito específico
        """
        if not self.api_key:
            return await self._simular_creacion_captura(contenido, proposito)
        
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "content": contenido,
                    "purpose": proposito,
                    "context": contexto,
                    "tags": ["campo-sagrado", proposito],
                    "created_at": datetime.now().isoformat()
                }
                
                response = await client.post(
                    f"{self.base_url}/captures",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                
                return response.json()
                
        except Exception as e:
            print(f"Error creando captura: {e}")
            return {"error": str(e)}
    
    async def obtener_insights_relacionados(
        self,
        tema: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Obtiene insights relacionados con un tema específico
        """
        if not self.api_key:
            return await self._simular_insights_relacionados(tema)
        
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "topic": tema,
                    "limit": limit,
                    "type": "insight"
                }
                
                response = await client.get(
                    f"{self.base_url}/insights",
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                
                return response.json().get("insights", [])
                
        except Exception as e:
            print(f"Error obteniendo insights: {e}")
            return await self._simular_insights_relacionados(tema)
    
    async def _simular_capturas_pendientes(self) -> List[CapturaAnytype]:
        """Simula capturas pendientes cuando no hay API key"""
        return [
            CapturaAnytype(
                id="capture-1",
                titulo="Idea sobre productividad",
                contenido="Implementar sistema de pomodoro con descansos activos",
                tipo="nota",
                timestamp=datetime.now(),
                etiquetas=["productividad", "pomodoro"],
                contexto="Durante sesión de trabajo"
            ),
            CapturaAnytype(
                id="capture-2",
                titulo="Enlace interesante",
                contenido="https://example.com/articulo-sobre-ritmos-circadianos",
                tipo="enlace",
                timestamp=datetime.now(),
                etiquetas=["salud", "ritmos"],
                contexto="Investigación sobre sueño"
            ),
            CapturaAnytype(
                id="capture-3",
                titulo="Reflexión personal",
                contenido="Me doy cuenta de que trabajo mejor en bloques de 90 minutos",
                tipo="nota",
                timestamp=datetime.now(),
                etiquetas=["reflexion", "patrones"],
                contexto="Autoobservación"
            )
        ]
    
    async def _simular_procesamiento(self, captura_id: str, accion: str) -> Dict[str, Any]:
        """Simula procesamiento de captura"""
        await asyncio.sleep(0.5)  # Simular delay
        return {
            "id": captura_id,
            "action": accion,
            "status": "processed",
            "timestamp": datetime.now().isoformat(),
            "result": f"Captura {captura_id} procesada con acción '{accion}'"
        }
    
    async def _simular_creacion_captura(self, contenido: str, proposito: str) -> Dict[str, Any]:
        """Simula creación de captura"""
        await asyncio.sleep(0.3)
        return {
            "id": f"capture-{datetime.now().timestamp()}",
            "content": contenido,
            "purpose": proposito,
            "status": "created",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _simular_insights_relacionados(self, tema: str) -> List[Dict[str, Any]]:
        """Simula insights relacionados"""
        await asyncio.sleep(0.2)
        return [
            {
                "id": f"insight-{tema}-1",
                "title": f"Insight sobre {tema}",
                "content": f"Patrón observado relacionado con {tema}",
                "relevance": 0.85,
                "tags": [tema, "insight"],
                "created_at": datetime.now().isoformat()
            }
        ]

class ProcesadorCapturas:
    """
    Procesa capturas de Anytype con propósito específico
    """
    
    def __init__(self, anytype_client: AnytypeClient):
        self.anytype = anytype_client
    
    async def metabolizar_capturas(
        self,
        capturas: List[CapturaAnytype],
        contexto_actual: str
    ) -> Dict[str, Any]:
        """
        Metaboliza capturas convirtiéndolas en conocimiento accionable
        """
        resultado = {
            "capturas_procesadas": 0,
            "insights_generados": [],
            "acciones_sugeridas": [],
            "conocimiento_cristalizado": []
        }
        
        for captura in capturas:
            if captura.procesado:
                continue
            
            # Determinar propósito de la captura
            proposito = await self._determinar_proposito(captura, contexto_actual)
            
            # Procesar según propósito
            if proposito == "metabolizar":
                insight = await self._generar_insight(captura)
                resultado["insights_generados"].append(insight)
            
            elif proposito == "accionar":
                accion = await self._generar_accion(captura)
                resultado["acciones_sugeridas"].append(accion)
            
            elif proposito == "cristalizar":
                conocimiento = await self._cristalizar_conocimiento(captura)
                resultado["conocimiento_cristalizado"].append(conocimiento)
            
            # Marcar como procesada
            await self.anytype.procesar_captura(captura.id, proposito)
            resultado["capturas_procesadas"] += 1
        
        return resultado
    
    async def _determinar_proposito(
        self, 
        captura: CapturaAnytype, 
        contexto: str
    ) -> str:
        """Determina el propósito de procesamiento para una captura"""
        
        # Lógica simple basada en contenido y contexto
        contenido_lower = captura.contenido.lower()
        
        if any(palabra in contenido_lower for palabra in ["idea", "pensamiento", "reflexion"]):
            return "metabolizar"
        elif any(palabra in contenido_lower for palabra in ["hacer", "implementar", "crear", "desarrollar"]):
            return "accionar"
        elif any(palabra in contenido_lower for palabra in ["aprender", "entender", "comprender"]):
            return "cristalizar"
        else:
            return "metabolizar"  # Por defecto
    
    async def _generar_insight(self, captura: CapturaAnytype) -> Dict[str, Any]:
        """Genera insight a partir de una captura"""
        return {
            "id": f"insight-{captura.id}",
            "titulo": f"Insight: {captura.titulo}",
            "contenido": f"Patrón observado: {captura.contenido}",
            "fuente": captura.id,
            "timestamp": datetime.now().isoformat(),
            "relevancia": 0.8
        }
    
    async def _generar_accion(self, captura: CapturaAnytype) -> Dict[str, Any]:
        """Genera acción a partir de una captura"""
        return {
            "id": f"accion-{captura.id}",
            "titulo": f"Acción: {captura.titulo}",
            "descripcion": f"Implementar: {captura.contenido}",
            "fuente": captura.id,
            "timestamp": datetime.now().isoformat(),
            "prioridad": "media"
        }
    
    async def _cristalizar_conocimiento(self, captura: CapturaAnytype) -> Dict[str, Any]:
        """Cristaliza conocimiento a partir de una captura"""
        return {
            "id": f"conocimiento-{captura.id}",
            "titulo": f"Conocimiento: {captura.titulo}",
            "contenido": f"Aprendizaje: {captura.contenido}",
            "fuente": captura.id,
            "timestamp": datetime.now().isoformat(),
            "nivel": "intermedio"
        }

# Función de utilidad para obtener cliente Anytype
def obtener_cliente_anytype() -> AnytypeClient:
    """Obtiene cliente de Anytype configurado"""
    return AnytypeClient()

# Función de utilidad para procesar capturas
async def procesar_capturas_anytype(contexto: str = "") -> Dict[str, Any]:
    """Procesa capturas pendientes de Anytype"""
    cliente = obtener_cliente_anytype()
    procesador = ProcesadorCapturas(cliente)
    
    capturas = await cliente.obtener_capturas_pendientes()
    resultado = await procesador.metabolizar_capturas(capturas, contexto)
    
    return resultado
