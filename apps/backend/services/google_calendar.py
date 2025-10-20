"""
🗓️ Campo Sagrado - Integración Google Calendar Bidireccional
===========================================================

Sistema de sincronización bidireccional entre:
- Estados Cero → Eventos en Google Calendar
- No Negociables → Bloqueos automáticos
- Espejo Diario → Evento diario
- Recordatorios litúrgicos → Notificaciones

Configuración 0.01%: Precisión astronómica + automatización completa
"""

import os
import json
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path
import asyncio
import aiohttp
from dataclasses import dataclass

from .tiempos_liturgicos import CalculadorTiemposLiturgicos
from .audit_trail import AuditTrail


@dataclass
class EventoCalendario:
    """Representa un evento en Google Calendar"""
    titulo: str
    descripcion: str
    inicio: datetime
    fin: datetime
    color_id: str = "1"  # Azul por defecto
    recordatorios: List[int] = None  # Minutos antes
    ubicacion: str = ""
    metadata: Dict = None


class GoogleCalendarIntegration:
    """
    Integración completa con Google Calendar
    Opera al borde del caos: sincronización automática + manual
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.audit = AuditTrail(vault_path)
        
        # Configuración API
        self.api_key = os.getenv("GOOGLE_CALENDAR_API_KEY")
        self.calendar_id = os.getenv("GOOGLE_CALENDAR_ID", "primary")
        self.base_url = "https://www.googleapis.com/calendar/v3"
        
        # Configuración local
        self.lat = float(os.getenv("LATITUD", "40.4168"))
        self.lon = float(os.getenv("LONGITUD", "-3.7038"))
        self.tz = os.getenv("TIMEZONE", "Europe/Madrid")
        
        # Calculador de tiempos litúrgicos
        self.calculador = CalculadorTiemposLiturgicos(self.lat, self.lon, self.tz)
        
        # Colores por tipo de evento
        self.colores = {
            "estado_cero": "1",      # Azul
            "no_negociable": "2",    # Verde
            "espejo_diario": "3",    # Púrpura
            "recordatorio": "4",     # Amarillo
            "analisis": "5"          # Naranja
        }
        
        # Cache de eventos para evitar duplicados
        self.eventos_cache = {}
    
    async def crear_evento_estado_cero(
        self, 
        momento: str, 
        fecha: date,
        estado_cero_id: str,
        tendencia: str = None,
        intensidad: float = None
    ) -> str:
        """
        Crea evento en Google Calendar para Estado Cero
        Incluye metadata del Estado Cero
        """
        try:
            # Calcular tiempo litúrgico
            tiempos = self.calculador.calcular_tiempos_hoy(fecha)
            hora_inicio = tiempos.get(momento)
            
            if not hora_inicio:
                raise ValueError(f"No se pudo calcular tiempo para {momento}")
            
            # Crear evento (duración: 15 minutos)
            evento = EventoCalendario(
                titulo=f"🕌 Estado Cero - {momento.upper()}",
                descripcion=self._generar_descripcion_estado_cero(
                    momento, estado_cero_id, tendencia, intensidad
                ),
                inicio=hora_inicio,
                fin=hora_inicio + timedelta(minutes=15),
                color_id=self.colores["estado_cero"],
                recordatorios=[15, 5],  # 15 min y 5 min antes
                ubicacion="Campo Sagrado",
                metadata={
                    "estado_cero_id": estado_cero_id,
                    "momento_liturgico": momento,
                    "tipo": "estado_cero",
                    "tendencia": tendencia,
                    "intensidad": intensidad
                }
            )
            
            # Crear en Google Calendar
            event_id = await self._crear_evento_google(evento)
            
            # Cache para evitar duplicados
            cache_key = f"{momento}_{fecha.isoformat()}"
            self.eventos_cache[cache_key] = event_id
            
            # Audit trail
            self.audit.log_event(
                event_type="calendario_evento_creado",
                origen="google_calendar",
                estado="success",
                metadata={
                    "event_id": event_id,
                    "momento": momento,
                    "fecha": fecha.isoformat(),
                    "estado_cero_id": estado_cero_id
                }
            )
            
            return event_id
            
        except Exception as e:
            self.audit.log_event(
                event_type="calendario_evento_creado",
                origen="google_calendar",
                estado="error",
                metadata={
                    "momento": momento,
                    "fecha": fecha.isoformat(),
                    "error": str(e)
                }
            )
            raise
    
    async def crear_evento_espejo_diario(
        self, 
        fecha: date,
        estados_cero_count: int = 5
    ) -> str:
        """
        Crea evento para Espejo Diario post-Maghrib
        """
        try:
            # Calcular tiempo Maghrib + 15 minutos
            tiempos = self.calculador.calcular_tiempos_hoy(fecha)
            hora_maghrib = tiempos.get("maghrib")
            
            if not hora_maghrib:
                raise ValueError("No se pudo calcular tiempo Maghrib")
            
            hora_espejo = hora_maghrib + timedelta(minutes=15)
            
            evento = EventoCalendario(
                titulo="🪞 Espejo Diario",
                descripcion=f"""Generación automática del Espejo Diario

📊 Estados Cero completados: {estados_cero_count}/5
🔗 Análisis de entrelazamientos
📈 Visualización temporal del día
💡 Insights y patrones emergentes

Este evento se genera automáticamente después de completar Maghrib.""",
                inicio=hora_espejo,
                fin=hora_espejo + timedelta(minutes=30),
                color_id=self.colores["espejo_diario"],
                recordatorios=[10],  # 10 min antes
                ubicacion="Campo Sagrado",
                metadata={
                    "tipo": "espejo_diario",
                    "fecha": fecha.isoformat(),
                    "estados_cero_count": estados_cero_count
                }
            )
            
            event_id = await self._crear_evento_google(evento)
            
            self.audit.log_event(
                event_type="calendario_espejo_creado",
                origen="google_calendar",
                estado="success",
                metadata={
                    "event_id": event_id,
                    "fecha": fecha.isoformat()
                }
            )
            
            return event_id
            
        except Exception as e:
            self.audit.log_event(
                event_type="calendario_espejo_creado",
                origen="google_calendar",
                estado="error",
                metadata={
                    "fecha": fecha.isoformat(),
                    "error": str(e)
                }
            )
            raise
    
    async def crear_bloqueo_no_negociable(
        self,
        titulo: str,
        descripcion: str,
        inicio: datetime,
        fin: datetime,
        tipo: str = "no_negociable"
    ) -> str:
        """
        Crea bloqueo para No Negociable
        """
        try:
            evento = EventoCalendario(
                titulo=f"🔒 {titulo}",
                descripcion=f"**NO NEGOCIABLE**\n\n{descripcion}",
                inicio=inicio,
                fin=fin,
                color_id=self.colores["no_negociable"],
                recordatorios=[60, 15],  # 1 hora y 15 min antes
                ubicacion="Campo Sagrado",
                metadata={
                    "tipo": tipo,
                    "no_negociable": True
                }
            )
            
            event_id = await self._crear_evento_google(evento)
            
            self.audit.log_event(
                event_type="calendario_no_negociable_creado",
                origen="google_calendar",
                estado="success",
                metadata={
                    "event_id": event_id,
                    "titulo": titulo,
                    "tipo": tipo
                }
            )
            
            return event_id
            
        except Exception as e:
            self.audit.log_event(
                event_type="calendario_no_negociable_creado",
                origen="google_calendar",
                estado="error",
                metadata={
                    "titulo": titulo,
                    "error": str(e)
                }
            )
            raise
    
    async def programar_semana_estados_cero(
        self, 
        fecha_inicio: date
    ) -> List[str]:
        """
        Programa todos los Estados Cero de una semana
        Crea eventos automáticamente para los próximos 7 días
        """
        eventos_creados = []
        
        for i in range(7):
            fecha_actual = fecha_inicio + timedelta(days=i)
            momentos = ["fajr", "dhuhr", "asr", "maghrib", "isha"]
            
            for momento in momentos:
                try:
                    # Verificar si ya existe en cache
                    cache_key = f"{momento}_{fecha_actual.isoformat()}"
                    if cache_key in self.eventos_cache:
                        continue
                    
                    # Crear evento
                    event_id = await self.crear_evento_estado_cero(
                        momento=momento,
                        fecha=fecha_actual,
                        estado_cero_id=f"programado_{fecha_actual}_{momento}"
                    )
                    
                    eventos_creados.append(event_id)
                    
                except Exception as e:
                    print(f"⚠️ Error creando evento {momento} para {fecha_actual}: {e}")
                    continue
        
        self.audit.log_event(
            event_type="calendario_semana_programada",
            origen="google_calendar",
            estado="success",
            metadata={
                "fecha_inicio": fecha_inicio.isoformat(),
                "eventos_creados": len(eventos_creados),
                "event_ids": eventos_creados
            }
        )
        
        return eventos_creados
    
    async def obtener_eventos_proximos(
        self, 
        horas: int = 24
    ) -> List[Dict]:
        """
        Obtiene eventos próximos del calendario
        Útil para verificar conflictos o sincronización
        """
        try:
            ahora = datetime.now()
            tiempo_max = ahora + timedelta(hours=horas)
            
            url = f"{self.base_url}/calendars/{self.calendar_id}/events"
            params = {
                "key": self.api_key,
                "timeMin": ahora.isoformat() + "Z",
                "timeMax": tiempo_max.isoformat() + "Z",
                "singleEvents": True,
                "orderBy": "startTime"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        eventos = data.get("items", [])
                        
                        # Filtrar solo eventos del Campo Sagrado
                        eventos_campo = [
                            ev for ev in eventos 
                            if "🕌" in ev.get("summary", "") or 
                               "🪞" in ev.get("summary", "") or
                               "🔒" in ev.get("summary", "")
                        ]
                        
                        return eventos_campo
                    else:
                        raise Exception(f"Error API: {response.status}")
                        
        except Exception as e:
            self.audit.log_event(
                event_type="calendario_obtener_eventos",
                origen="google_calendar",
                estado="error",
                metadata={"error": str(e), "horas": horas}
            )
            raise
    
    async def _crear_evento_google(self, evento: EventoCalendario) -> str:
        """Crea evento en Google Calendar usando API"""
        url = f"{self.base_url}/calendars/{self.calendar_id}/events"
        
        # Preparar datos del evento
        event_data = {
            "summary": evento.titulo,
            "description": evento.descripcion,
            "start": {
                "dateTime": evento.inicio.isoformat(),
                "timeZone": self.tz
            },
            "end": {
                "dateTime": evento.fin.isoformat(),
                "timeZone": self.tz
            },
            "colorId": evento.color_id,
            "location": evento.ubicacion,
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": rem}
                    for rem in (evento.recordatorios or [])
                ]
            }
        }
        
        # Añadir metadata si existe
        if evento.metadata:
            event_data["extendedProperties"] = {
                "private": evento.metadata
            }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        params = {
            "key": self.api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, 
                json=event_data, 
                headers=headers, 
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["id"]
                else:
                    error_text = await response.text()
                    raise Exception(f"Error creando evento: {response.status} - {error_text}")
    
    def _generar_descripcion_estado_cero(
        self, 
        momento: str, 
        estado_cero_id: str,
        tendencia: str = None,
        intensidad: float = None
    ) -> str:
        """Genera descripción rica para evento de Estado Cero"""
        desc = f"""🕌 **Estado Cero - {momento.upper()}**

**ID:** {estado_cero_id}
**Momento Litúrgico:** {momento.upper()}

"""
        
        if tendencia and intensidad:
            desc += f"""**Estado:** {tendencia.title()} ({intensidad:.0%})
"""
        
        desc += f"""
**Preguntas Dinámicas:**
- Preguntas específicas para {momento.upper()}
- Respuestas binarias (expansión/contracción)
- Análisis de dominio predominante

**Después del Estado Cero:**
- Archivo automático en Obsidian
- Análisis de patrones
- Integración con Espejo Diario

---
*Campo Sagrado del Entrelazador - Sistema 0.01%*
"""
        
        return desc
    
    async def sincronizar_estado_cero_completado(
        self,
        estado_cero_id: str,
        momento: str,
        fecha: date,
        tendencia: str,
        intensidad: float
    ):
        """
        Actualiza evento existente cuando se completa un Estado Cero
        Añade metadata del resultado
        """
        try:
            # Buscar evento existente
            cache_key = f"{momento}_{fecha.isoformat()}"
            event_id = self.eventos_cache.get(cache_key)
            
            if not event_id:
                # Si no está en cache, buscar por título
                eventos = await self.obtener_eventos_proximos(24)
                for ev in eventos:
                    if f"Estado Cero - {momento.upper()}" in ev.get("summary", ""):
                        event_id = ev["id"]
                        break
            
            if not event_id:
                print(f"⚠️ No se encontró evento para {momento} {fecha}")
                return
            
            # Actualizar descripción con resultado
            nueva_descripcion = self._generar_descripcion_estado_cero(
                momento, estado_cero_id, tendencia, intensidad
            )
            
            # Actualizar evento
            url = f"{self.base_url}/calendars/{self.calendar_id}/events/{event_id}"
            
            update_data = {
                "description": nueva_descripcion,
                "extendedProperties": {
                    "private": {
                        "estado_cero_id": estado_cero_id,
                        "momento_liturgico": momento,
                        "tipo": "estado_cero",
                        "tendencia": tendencia,
                        "intensidad": intensidad,
                        "completado": True,
                        "fecha_completado": datetime.now().isoformat()
                    }
                }
            }
            
            params = {"key": self.api_key}
            
            async with aiohttp.ClientSession() as session:
                async with session.put(
                    url, 
                    json=update_data, 
                    params=params
                ) as response:
                    if response.status == 200:
                        self.audit.log_event(
                            event_type="calendario_evento_actualizado",
                            origen="google_calendar",
                            estado="success",
                            metadata={
                                "event_id": event_id,
                                "estado_cero_id": estado_cero_id,
                                "momento": momento
                            }
                        )
                    else:
                        raise Exception(f"Error actualizando evento: {response.status}")
                        
        except Exception as e:
            self.audit.log_event(
                event_type="calendario_evento_actualizado",
                origen="google_calendar",
                estado="error",
                metadata={
                    "estado_cero_id": estado_cero_id,
                    "error": str(e)
                }
            )
            print(f"⚠️ Error actualizando evento calendario: {e}")
    
    def limpiar_cache(self):
        """Limpia cache de eventos (llamar diariamente)"""
        self.eventos_cache.clear()
        print("🗑️ Cache de eventos calendario limpiado")
