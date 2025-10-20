"""
🗓️ Google Calendar Integration
================================

Gestión de eventos en Google Calendar para compartir jornadas.
"""

import os
from datetime import datetime, timedelta, date, time as dt_time
from pathlib import Path
from typing import List, Optional, Dict
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from models.schemas import JornadaAlBordeCaos, AccionConcreta


SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarClient:
    """Cliente para interactuar con Google Calendar API"""
    
    def __init__(self, credentials_path: str = None, token_path: str = None):
        """
        Inicializa el cliente de Google Calendar
        
        Args:
            credentials_path: Ruta a credentials.json de Google Cloud
            token_path: Ruta donde guardar/leer el token de acceso
        """
        self.base_path = Path(__file__).parent.parent / "config"
        self.base_path.mkdir(exist_ok=True)
        
        self.credentials_path = credentials_path or str(self.base_path / "google_credentials.json")
        self.token_path = token_path or str(self.base_path / "google_token.json")
        
        self.creds = None
        self.service = None
        
        # Intentar cargar credenciales
        if os.path.exists(self.credentials_path):
            self._authenticate()
    
    def _authenticate(self):
        """Autentica con Google Calendar API"""
        # Verificar si ya tenemos token válido
        if os.path.exists(self.token_path):
            try:
                self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            except Exception as e:
                print(f"⚠️ Token existente inválido: {e}")
                self.creds = None
        
        # Si no hay credenciales o están expiradas
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    print(f"⚠️ Error refrescando token: {e}")
                    self.creds = None
            
            if not self.creds:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_path}\n"
                        "Por favor ejecuta: python scripts/setup_google_calendar.py"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path,
                    SCOPES
                )
                # Intentar con varios puertos
                for port in [8080, 8090, 8888, 0]:  # 0 = puerto aleatorio
                    try:
                        self.creds = flow.run_local_server(port=port)
                        print(f"✅ Autenticación exitosa en puerto {port}")
                        break
                    except OSError as e:
                        if port == 0:  # Último intento
                            raise Exception(f"No se pudo iniciar servidor OAuth: {e}")
                        continue
            
            # Guardar credenciales para próxima vez
            if self.creds:
                with open(self.token_path, 'w') as token:
                    token.write(self.creds.to_json())
        
        # Construir servicio
        if self.creds:
            self.service = build('calendar', 'v3', credentials=self.creds)
    
    def is_authenticated(self) -> bool:
        """Verifica si está autenticado"""
        return self.service is not None
    
    def crear_evento(
        self,
        titulo: str,
        inicio: datetime,
        fin: datetime,
        descripcion: str = "",
        ubicacion: str = "",
        asistentes: List[str] = None,
        color_id: str = None,
        recordatorios: List[Dict] = None
    ) -> Dict:
        """
        Crea un evento en Google Calendar
        
        Args:
            titulo: Título del evento
            inicio: Fecha/hora de inicio
            fin: Fecha/hora de fin
            descripcion: Descripción opcional
            ubicacion: Ubicación opcional
            asistentes: Lista de emails para invitar
            color_id: ID de color (1-11)
            recordatorios: Lista de recordatorios personalizados
        
        Returns:
            Evento creado
        """
        if not self.is_authenticated():
            raise Exception("No autenticado. Ejecuta setup_google_calendar.py")
        
        evento = {
            'summary': titulo,
            'description': descripcion,
            'start': {
                'dateTime': inicio.isoformat(),
                'timeZone': 'Europe/Madrid',
            },
            'end': {
                'dateTime': fin.isoformat(),
                'timeZone': 'Europe/Madrid',
            },
        }
        
        if ubicacion:
            evento['location'] = ubicacion
        
        if color_id:
            evento['colorId'] = str(color_id)
        
        if asistentes:
            evento['attendees'] = [{'email': email} for email in asistentes]
            evento['guestsCanSeeOtherGuests'] = True
            evento['guestsCanModify'] = False
        
        if recordatorios:
            evento['reminders'] = {
                'useDefault': False,
                'overrides': recordatorios
            }
        else:
            evento['reminders'] = {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 10},
                ],
            }
        
        try:
            evento_creado = self.service.events().insert(
                calendarId='primary',
                body=evento,
                sendUpdates='all'  # Envía invitaciones por email
            ).execute()
            
            return evento_creado
        
        except HttpError as error:
            print(f"❌ Error creando evento: {error}")
            raise
    
    def crear_jornada_completa(
        self,
        fecha: date,
        plan: JornadaAlBordeCaos,
        intencion: str,
        asistentes: List[str] = None
    ) -> List[Dict]:
        """
        Crea todos los eventos de una jornada en Google Calendar
        
        Args:
            fecha: Fecha de la jornada
            plan: Plan generado por el Orquestador
            intencion: Intención del día
            asistentes: Emails para compartir (opcional)
        
        Returns:
            Lista de eventos creados
        """
        if not self.is_authenticated():
            raise Exception("No autenticado con Google Calendar")
        
        eventos_creados = []
        
        # 1. Estados Cero (5 momentos litúrgicos)
        momentos_liturgicos = {
            'fajr': ('06:00', '06:30', '🌅', '9'),      # Azul claro
            'dhuhr': ('13:00', '13:30', '☀️', '5'),    # Amarillo
            'asr': ('16:00', '16:30', '🌤️', '6'),     # Naranja
            'maghrib': ('19:00', '19:30', '🌆', '11'), # Rojo
            'isha': ('22:00', '22:30', '🌙', '1'),     # Azul oscuro
        }
        
        for momento, (hora_inicio, hora_fin, emoji, color) in momentos_liturgicos.items():
            inicio = datetime.combine(
                fecha,
                datetime.strptime(hora_inicio, '%H:%M').time()
            )
            fin = datetime.combine(
                fecha,
                datetime.strptime(hora_fin, '%H:%M').time()
            )
            
            evento = self.crear_evento(
                titulo=f"{emoji} Estado Cero - {momento.upper()}",
                inicio=inicio,
                fin=fin,
                descripcion=f"""Consulta sacral - Momento {momento}

Intención del día: {intencion}

Este es un momento personal de consulta con tu autoridad sacral.
No disponible para reuniones.""",
                color_id=color,
                asistentes=None  # Estados Cero son privados
            )
            eventos_creados.append(evento)
        
        # 2. Bloques del plan (compartidos si hay asistentes)
        for i, bloque in enumerate(plan.bloques_sugeridos):
            try:
                # Parsear hora de inicio
                hora_inicio = datetime.strptime(bloque.inicio_aprox, '%H:%M').time()
                inicio = datetime.combine(fecha, hora_inicio)
                
                # Parsear duración
                duracion_str = bloque.duracion.lower()
                if 'h' in duracion_str:
                    horas = float(duracion_str.replace('h', '').replace('min', '').strip())
                    duracion_min = int(horas * 60)
                elif 'min' in duracion_str:
                    duracion_min = int(duracion_str.replace('min', '').strip())
                else:
                    duracion_min = 60  # Default 1 hora
                
                fin = inicio + timedelta(minutes=duracion_min)
                
                # Determinar color según energía
                energia = bloque.energia_optima or 3
                color_map = {1: '8', 2: '8', 3: '7', 4: '10', 5: '11'}  # Verde a Rojo
                color = color_map.get(energia, '7')
                
                # Descripción rica
                descripcion_partes = [
                    f"Rol: {bloque.rol}" if bloque.rol else "",
                    f"Energía óptima: {'🔥' * energia} ({energia}/5)",
                    f"Tipo: {'Flexible (se puede ajustar)' if bloque.flexible else 'Anclado (importante mantener)'}",
                    "",
                    "Alternativas si es necesario ajustar:",
                ]
                
                if bloque.opciones_alternativas:
                    for opt in bloque.opciones_alternativas:
                        descripcion_partes.append(f"  • {opt}")
                else:
                    descripcion_partes.append("  • Sin alternativas definidas")
                
                descripcion_partes.append("")
                descripcion_partes.append(f"Parte del plan: {intencion}")
                
                titulo_emoji = "🌊" if bloque.flexible else "⚓"
                
                evento = self.crear_evento(
                    titulo=f"{titulo_emoji} {bloque.actividad}",
                    inicio=inicio,
                    fin=fin,
                    descripcion="\n".join(descripcion_partes),
                    color_id=color,
                    asistentes=asistentes  # Compartir con pareja/círculo
                )
                eventos_creados.append(evento)
                
            except Exception as e:
                print(f"⚠️ Error creando bloque {i}: {e}")
                continue
        
        # 3. Recordatorio de No-Negociables (evento especial)
        if plan.no_negociables:
            # Crear un evento al inicio del día con checklist
            inicio_dia = datetime.combine(fecha, dt_time(6, 0))
            fin_checklist = datetime.combine(fecha, dt_time(6, 5))
            
            no_neg_text = "\n".join([
                f"☐ {nn.nombre} - {nn.ventana} ({nn.duracion_min})"
                for nn in plan.no_negociables
            ])
            
            evento = self.crear_evento(
                titulo="✓ No-Negociables del Día",
                inicio=inicio_dia,
                fin=fin_checklist,
                descripcion=f"""Estos son tus no-negociables de hoy.
El Guardian verificará su cumplimiento.

{no_neg_text}

Intención: {intencion}""",
                color_id='4',  # Rojo pálido
                asistentes=None
            )
            eventos_creados.append(evento)
        
        return eventos_creados
    
    def listar_eventos_dia(self, fecha: date) -> List[Dict]:
        """Lista todos los eventos de un día específico"""
        if not self.is_authenticated():
            raise Exception("No autenticado")
        
        inicio = datetime.combine(fecha, dt_time(0, 0))
        fin = datetime.combine(fecha, dt_time(23, 59))
        
        try:
            eventos = self.service.events().list(
                calendarId='primary',
                timeMin=inicio.isoformat() + 'Z',
                timeMax=fin.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return eventos.get('items', [])
        
        except HttpError as error:
            print(f"❌ Error listando eventos: {error}")
            return []
    
    def eliminar_eventos_dia(self, fecha: date) -> int:
        """
        Elimina todos los eventos del Campo Sagrado de un día
        (útil para re-planificar)
        """
        if not self.is_authenticated():
            raise Exception("No autenticado")
        
        eventos = self.listar_eventos_dia(fecha)
        eliminados = 0
        
        for evento in eventos:
            titulo = evento.get('summary', '')
            # Solo eliminar eventos del Campo Sagrado
            if any(x in titulo for x in ['Estado Cero', 'No-Negociables', '🌊', '⚓']):
                try:
                    self.service.events().delete(
                        calendarId='primary',
                        eventId=evento['id']
                    ).execute()
                    eliminados += 1
                except HttpError:
                    pass
        
        return eliminados


# Cliente global (se inicializa si existen credenciales)
try:
    google_calendar = GoogleCalendarClient()
except Exception as e:
    print(f"⚠️ Google Calendar no configurado: {e}")
    google_calendar = None

