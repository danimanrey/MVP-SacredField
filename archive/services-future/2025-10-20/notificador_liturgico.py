"""
🕌 Sistema de Notificaciones Litúrgicas
======================================

Sistema de recordatorios automáticos para los 5 momentos litúrgicos diarios:
- Fajr (alba)
- Dhuhr (mediodía) 
- Asr (tarde)
- Maghrib (atardecer)
- Isha (noche)

Integra con macOS Notification Center para recordatorios nativos.
"""

import schedule
import subprocess
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
from pathlib import Path


class NotificadorLiturgico:
    """Sistema de notificaciones para momentos litúrgicos"""
    
    def __init__(self, lat: float = 40.4168, lon: float = -3.7038, tz: str = "Europe/Madrid"):
        """
        Inicializa el notificador
        
        Args:
            lat: Latitud
            lon: Longitud  
            tz: Zona horaria
        """
        self.lat = lat
        self.lon = lon
        self.tz = tz
        
        # URL base para Estado Cero
        self.estado_cero_url = "http://localhost:3000/estado-cero-inmersivo"
        
        # Configuración de notificaciones
        self.notificaciones_activas = True
        self.minutos_antes = 5  # Notificar 5 minutos antes
        
        # Historial de notificaciones
        self.historial_file = Path("storage/notificaciones_historial.json")
        self.cargar_historial()
    
    def notificar_macOS(self, titulo: str, mensaje: str, url: Optional[str] = None) -> bool:
        """
        Envía notificación nativa de macOS
        
        Args:
            titulo: Título de la notificación
            mensaje: Mensaje de la notificación
            url: URL opcional para abrir al hacer clic
            
        Returns:
            True si la notificación se envió correctamente
        """
        try:
            # Construir script AppleScript
            if url:
                script = f'''
                display notification "{mensaje}" with title "{titulo}" sound name "Crystal"
                delay 2
                open location "{url}"
                '''
            else:
                script = f'''
                display notification "{mensaje}" with title "{titulo}" sound name "Crystal"
                '''
            
            # Ejecutar script
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Registrar en historial
                self.registrar_notificacion(titulo, mensaje, url)
                return True
            else:
                print(f"❌ Error en notificación macOS: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout en notificación macOS")
            return False
        except Exception as e:
            print(f"❌ Error enviando notificación: {e}")
            return False
    
    def calcular_tiempos_liturgicos_hoy(self) -> Dict[str, datetime]:
        """
        Calcula los tiempos litúrgicos para hoy
        
        Returns:
            Dict con {momento: datetime}
        """
        # Para MVP, usar tiempos aproximados basados en hora solar
        # En implementación completa, usar CalculadorTiemposLiturgicos
        
        hoy = datetime.now().date()
        
        # Tiempos aproximados (ajustar según ubicación y época del año)
        tiempos_aproximados = {
            "fajr": datetime.combine(hoy, datetime.min.time().replace(hour=6, minute=30)),  # ~6:30 AM
            "dhuhr": datetime.combine(hoy, datetime.min.time().replace(hour=13, minute=0)),  # ~1:00 PM
            "asr": datetime.combine(hoy, datetime.min.time().replace(hour=16, minute=30)),   # ~4:30 PM
            "maghrib": datetime.combine(hoy, datetime.min.time().replace(hour=19, minute=0)), # ~7:00 PM
            "isha": datetime.combine(hoy, datetime.min.time().replace(hour=20, minute=30)),  # ~8:30 PM
        }
        
        return tiempos_aproximados
    
    def programar_notificaciones_dia(self) -> Dict[str, str]:
        """
        Programa notificaciones para todos los momentos del día
        
        Returns:
            Dict con {momento: hora_programada}
        """
        tiempos = self.calcular_tiempos_liturgicos_hoy()
        programadas = {}
        
        # Limpiar programaciones anteriores
        schedule.clear()
        
        for momento, hora in tiempos.items():
            # Calcular hora de notificación (5 minutos antes)
            hora_notif = hora - timedelta(minutes=self.minutos_antes)
            
            # Solo programar si la hora de notificación es futura
            if hora_notif > datetime.now():
                # Programar notificación
                schedule.every().day.at(hora_notif.strftime("%H:%M")).do(
                    self._enviar_notificacion_momento,
                    momento,
                    hora
                )
                
                programadas[momento] = hora_notif.strftime("%H:%M")
                print(f"⏰ Programada notificación para {momento.upper()} a las {hora_notif.strftime('%H:%M')}")
            else:
                print(f"⏭️ Saltando {momento.upper()} - ya pasó la hora de notificación")
        
        # Programar reprogramación diaria a medianoche
        schedule.every().day.at("00:00").do(self.programar_notificaciones_dia)
        
        return programadas
    
    def _enviar_notificacion_momento(self, momento: str, hora_momento: datetime):
        """
        Envía notificación para un momento específico
        
        Args:
            momento: Momento litúrgico
            hora_momento: Hora exacta del momento
        """
        if not self.notificaciones_activas:
            return
        
        # Preparar mensaje
        emojis = {
            "fajr": "🌅",
            "dhuhr": "☀️", 
            "asr": "🌤️",
            "maghrib": "🌇",
            "isha": "🌙"
        }
        
        titulo = f"{emojis.get(momento, '🕌')} {momento.upper()}"
        mensaje = f"Es momento de tu Estado Cero {momento.upper()}"
        
        # Enviar notificación
        self.notificar_macOS(titulo, mensaje, self.estado_cero_url)
        
        print(f"🔔 Notificación enviada: {momento.upper()}")
    
    def enviar_notificacion_manual(self, momento: str) -> bool:
        """
        Envía notificación manual para un momento
        
        Args:
            momento: Momento litúrgico
            
        Returns:
            True si se envió correctamente
        """
        tiempos = self.calcular_tiempos_liturgicos_hoy()
        
        if momento not in tiempos:
            print(f"❌ Momento no válido: {momento}")
            return False
        
        hora_momento = tiempos[momento]
        self._enviar_notificacion_momento(momento, hora_momento)
        return True
    
    def obtener_estado_notificaciones(self) -> Dict:
        """
        Obtiene el estado actual del sistema de notificaciones
        
        Returns:
            Dict con estado del sistema
        """
        tiempos = self.calcular_tiempos_liturgicos_hoy()
        programadas = []
        
        # Obtener jobs programados
        for job in schedule.jobs:
            if hasattr(job, 'job_func') and job.job_func == self._enviar_notificacion_momento:
                programadas.append({
                    "hora": job.next_run.strftime("%H:%M") if job.next_run else None,
                    "momento": "programado"
                })
        
        return {
            "notificaciones_activas": self.notificaciones_activas,
            "minutos_antes": self.minutos_antes,
            "tiempos_hoy": {momento: hora.strftime("%H:%M") for momento, hora in tiempos.items()},
            "programadas": programadas,
            "total_notificaciones_enviadas": len(self.historial),
            "ultima_notificacion": self.historial[-1] if self.historial else None
        }
    
    def activar_notificaciones(self):
        """Activa las notificaciones"""
        self.notificaciones_activas = True
        print("✅ Notificaciones activadas")
    
    def desactivar_notificaciones(self):
        """Desactiva las notificaciones"""
        self.notificaciones_activas = False
        print("❌ Notificaciones desactivadas")
    
    def cargar_historial(self):
        """Carga historial de notificaciones desde archivo"""
        if self.historial_file.exists():
            try:
                with open(self.historial_file, 'r', encoding='utf-8') as f:
                    self.historial = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.historial = []
        else:
            self.historial = []
    
    def guardar_historial(self):
        """Guarda historial de notificaciones en archivo"""
        self.historial_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.historial_file, 'w', encoding='utf-8') as f:
            json.dump(self.historial, f, indent=2, ensure_ascii=False)
    
    def registrar_notificacion(self, titulo: str, mensaje: str, url: Optional[str] = None):
        """
        Registra notificación en historial
        
        Args:
            titulo: Título de la notificación
            mensaje: Mensaje de la notificación
            url: URL opcional
        """
        registro = {
            "timestamp": datetime.now().isoformat(),
            "titulo": titulo,
            "mensaje": mensaje,
            "url": url
        }
        
        self.historial.append(registro)
        
        # Mantener solo últimos 100 registros
        if len(self.historial) > 100:
            self.historial = self.historial[-100:]
        
        self.guardar_historial()


# Instancia global
notificador = NotificadorLiturgico()


def get_notificador() -> NotificadorLiturgico:
    """Obtiene la instancia global del notificador"""
    return notificador
