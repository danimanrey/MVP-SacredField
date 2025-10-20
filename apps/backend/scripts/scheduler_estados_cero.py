#!/usr/bin/env python3
"""
🕌 Scheduler de Estados Cero
============================

Script que corre como proceso de fondo para:
1. Programar notificaciones litúrgicas diarias
2. Verificar y enviar recordatorios automáticos
3. Reprogramar notificaciones cada día

Uso: python scripts/scheduler_estados_cero.py
"""

import sys
import time
import signal
from pathlib import Path

# Añadir el directorio padre al path
sys.path.append(str(Path(__file__).parent.parent))

from services.notificador_liturgico import get_notificador


class SchedulerEstadosCero:
    """Scheduler principal para Estados Cero"""
    
    def __init__(self):
        self.notificador = get_notificador()
        self.running = False
        self.notificaciones_programadas = {}
    
    def iniciar(self):
        """Inicia el scheduler"""
        print("🕌 Iniciando Scheduler de Estados Cero...")
        print(f"📍 Ubicación: {self.notificador.lat}, {self.notificador.lon}")
        print(f"🕐 Zona horaria: {self.notificador.tz}")
        
        # Programar notificaciones para hoy
        self.notificaciones_programadas = self.notificador.programar_notificaciones_dia()
        
        if self.notificaciones_programadas:
            print("✅ Notificaciones programadas:")
            for momento, hora in self.notificaciones_programadas.items():
                print(f"   - {momento.upper()}: {hora}")
        else:
            print("⚠️ No hay notificaciones programadas para hoy")
        
        # Configurar manejo de señales
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.running = True
        print("🔄 Scheduler iniciado. Presiona Ctrl+C para detener.")
        
        # Loop principal
        self._run_loop()
    
    def _run_loop(self):
        """Loop principal del scheduler"""
        while self.running:
            try:
                # Ejecutar jobs programados
                schedule.run_pending()
                
                # Verificar estado cada minuto
                time.sleep(60)
                
                # Log de estado cada 30 minutos
                if int(time.time()) % 1800 == 0:  # Cada 30 minutos
                    self._log_estado()
                
            except KeyboardInterrupt:
                print("\n🛑 Scheduler interrumpido por usuario")
                break
            except Exception as e:
                print(f"❌ Error en loop principal: {e}")
                time.sleep(60)  # Esperar un minuto antes de reintentar
        
        self._cleanup()
    
    def _signal_handler(self, signum, frame):
        """Maneja señales del sistema"""
        print(f"\n🛑 Señal {signum} recibida. Deteniendo scheduler...")
        self.running = False
    
    def _log_estado(self):
        """Registra estado del scheduler"""
        estado = self.notificador.obtener_estado_notificaciones()
        
        print(f"📊 Estado del Scheduler - {datetime.now().strftime('%H:%M:%S')}")
        print(f"   - Notificaciones activas: {'✅' if estado['notificaciones_activas'] else '❌'}")
        print(f"   - Total enviadas: {estado['total_notificaciones_enviadas']}")
        
        if estado['ultima_notificacion']:
            ultima = estado['ultima_notificacion']
            print(f"   - Última: {ultima['titulo']} ({ultima['timestamp'][:16]})")
    
    def _cleanup(self):
        """Limpieza al finalizar"""
        print("🧹 Limpiando scheduler...")
        
        # Limpiar programaciones
        schedule.clear()
        
        # Guardar estado final
        self.notificador.guardar_historial()
        
        print("✅ Scheduler finalizado correctamente")
    
    def programar_notificaciones_manual(self):
        """Reprograma notificaciones manualmente"""
        print("🔄 Reprogramando notificaciones...")
        self.notificaciones_programadas = self.notificador.programar_notificaciones_dia()
        
        if self.notificaciones_programadas:
            print("✅ Nuevas notificaciones programadas:")
            for momento, hora in self.notificaciones_programadas.items():
                print(f"   - {momento.upper()}: {hora}")
        else:
            print("⚠️ No se programaron nuevas notificaciones")
    
    def enviar_notificacion_manual(self, momento: str):
        """Envía notificación manual para un momento"""
        print(f"🔔 Enviando notificación manual para {momento.upper()}...")
        
        if self.notificador.enviar_notificacion_manual(momento):
            print("✅ Notificación enviada")
        else:
            print("❌ Error enviando notificación")
    
    def obtener_estado(self):
        """Obtiene estado del scheduler"""
        return self.notificador.obtener_estado_notificaciones()


def main():
    """Función principal"""
    scheduler = SchedulerEstadosCero()
    
    try:
        scheduler.iniciar()
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo scheduler...")
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Importar schedule aquí para evitar problemas de importación
    import schedule
    from datetime import datetime
    
    main()
