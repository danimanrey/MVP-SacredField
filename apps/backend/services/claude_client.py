from __future__ import annotations

import os
import json
from typing import List, Dict, Any
import anthropic


class ClaudeClient:
    """
    Cliente real de Claude con fallback a mock si no hay API key.
    """

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = None
        
        if self.api_key:
            try:
                self.client = anthropic.Anthropic(api_key=self.api_key)
                print("✅ Claude client inicializado con API key real")
            except Exception as e:
                print(f"❌ Error inicializando Claude: {e}")
                self.client = None
        else:
            print("⚠️ No hay API key de Anthropic, usando modo mock")

    async def generate(self, system: str, messages: List[Dict[str, str]], model: str = "claude-3-5-sonnet-20241022", max_tokens: int = 1000) -> str:
        """
        Genera texto con Claude.
        
        Args:
            system: System prompt
            messages: Lista de mensajes
            model: Modelo a usar (default: Sonnet, usa Haiku para ahorrar)
            max_tokens: Máximo de tokens de salida
        """
        if self.client:
            try:
                # Convertir mensajes al formato de Claude
                claude_messages = []
                for msg in messages:
                    claude_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                response = self.client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    system=system,
                    messages=claude_messages
                )
                
                return response.content[0].text
            except Exception as e:
                print(f"❌ Error en Claude API: {e}")
                # Fallback a mock
                ultimo = messages[-1]["content"] if messages else ""
                return f"[claude-error] {ultimo[:140]}"
        else:
            # Mock simple: devolver eco conciso
            ultimo = messages[-1]["content"] if messages else ""
            return f"[mock-claude] {ultimo[:140]}"
    
    async def generate_haiku(self, system: str, messages: List[Dict[str, str]], max_tokens: int = 500) -> str:
        """
        Genera con Haiku (12x más barato que Sonnet).
        Úsalo para tareas simples como generar preguntas.
        """
        return await self.generate(system, messages, model="claude-3-5-haiku-20241022", max_tokens=max_tokens)

    async def generate_json(self, system: str, messages: List[Dict[str, str]], use_haiku: bool = False):
        """
        Genera JSON con Claude.
        
        Args:
            use_haiku: Si True, usa Haiku (12x más barato). Úsalo para tareas simples.
        """
        if self.client:
            try:
                # Agregar instrucción de formato JSON
                system_with_json = f"{system}\n\nResponde SOLO con JSON válido, sin texto adicional."
                
                # Elegir modelo
                model = "claude-3-5-haiku-20241022" if use_haiku else "claude-3-5-sonnet-20241022"
                
                response = await self.generate(system_with_json, messages, model=model, max_tokens=800)
                
                # Intentar parsear JSON
                try:
                    return json.loads(response)
                except json.JSONDecodeError:
                    # Si no es JSON válido, usar mock
                    print("⚠️ Claude no devolvió JSON válido, usando mock")
                    return self._get_mock_response(messages)
                    
            except Exception as e:
                print(f"❌ Error en Claude JSON: {e}")
                return self._get_mock_response(messages)
        else:
            return self._get_mock_response(messages)
    
    async def generate_json_haiku(self, system: str, messages: List[Dict[str, str]]):
        """Genera JSON con Haiku (tareas simples, 12x más barato)"""
        return await self.generate_json(system, messages, use_haiku=True)
    
    def _generar_recomendacion_simple(self, contexto: str) -> str:
        """
        Genera una recomendación simple para el día usando Claude
        Si no hay API key, usa una recomendación genérica
        """
        if self.client:
            try:
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=150,
                    messages=[{
                        "role": "user",
                        "content": contexto
                    }]
                )
                return response.content[0].text.strip()
            except Exception as e:
                print(f"❌ Error generando recomendación: {e}")
                return "Enfócate en las prioridades del día manteniendo energía balanceada"
        else:
            return "Día de balance - mantén flexibilidad para lo emergente"
    
    def _get_mock_response(self, messages: List[Dict[str, str]]):
        """Respuesta mock basada en el contenido del mensaje"""
        contenido = messages[-1]["content"] if messages else ""
        
        if "Preguntas BINARIAS" in contenido or "Preguntas" in contenido or "JSON" in contenido or "preguntas" in contenido:
            # Mock reducido a 3 preguntas esenciales
            return [
                {"id": "pregunta-1", "pregunta": "¿Tu cuerpo se expande al pensar en la acción principal del día?", "contexto": "Dirección emergente", "categoria": "desarrollo"},
                {"id": "pregunta-2", "pregunta": "¿Hay claridad en tu energía disponible ahora?", "contexto": "Estado biológico actual", "categoria": "biologia"},
                {"id": "pregunta-3", "pregunta": "¿Se siente alineado dedicar tiempo profundo a esto?", "contexto": "Compromiso temporal", "categoria": "conocimiento"}
            ]
        
        # Para orquestador plan emergente
        try:
            data = {
                "bloques_sugeridos": [
                    {
                        "id": "bloque-1",
                        "inicio_aprox": "10:00",
                        "duracion": "90min",
                        "actividad": "Acción principal",
                        "rol": "hacedor",
                        "energia_optima": 4,
                        "flexible": True,
                        "opciones_alternativas": ["corto 45min", "dividir en 2 bloques"]
                    }
                ],
                "puntos_decision": [
                    {
                        "momento": "12:30",
                        "pregunta": "¿Continuar o cambiar?",
                        "criterio": "Si energía > 3 y momentum fuerte",
                        "opciones": ["Continuar", "Descanso", "Emergente"]
                    }
                ]
            }
            return data
        except Exception:
            return {}


# Instancia global del cliente
claude_client = ClaudeClient()
