"""
Worker de Ingesta - Procesa eventos de Estados Cero completados
Parte del flujo Captura → Vault → Insights → Acción
"""

import time
import json
from datetime import datetime, date
from pathlib import Path
from typing import Optional

# Importar desde el directorio padre
import sys
sys.path.append(str(Path(__file__).parent.parent))

from services.event_queue import get_event_queue


class IngestWorker:
    """Worker que procesa eventos de Estados Cero completados"""
    
    def __init__(self):
        self.queue = get_event_queue()
        self.running = False
        self.processed_count = 0
        self.error_count = 0
    
    def process_estado_cero_completed(self, event_data: dict) -> bool:
        """
        Procesa un evento de Estado Cero completado
        
        Args:
            event_data: Datos del evento
            
        Returns:
            True si se procesó correctamente, False si hubo error
        """
        try:
            archivo_path = event_data['archivo_path']
            estado_cero_id = event_data['estado_cero_id']
            fecha = event_data['fecha']
            momento = event_data['momento']
            tendencia = event_data['tendencia']
            intensidad = event_data['intensidad']
            
            print(f"📄 Procesando Estado Cero: {estado_cero_id}")
            
            # 1. Parse frontmatter del archivo MD en Obsidian
            metadata = self.parse_obsidian_frontmatter(archivo_path)
            
            # 2. Update SQLite con índice (TODO: implementar cuando tengamos SQLite)
            # self.update_sqlite_index(estado_cero_id, metadata)
            
            # 3. [FUTURO] Chunk + embed → vector DB
            # vector_store.embed_document(content, metadata)
            
            # 4. Trigger análisis si 5 Estados Cero del día
            count = self.count_estados_cero_dia(fecha)
            if count == 5:
                print(f"🎯 Día completo detectado ({fecha}): {count} Estados Cero")
                self.queue.emit("dashboard_trigger", {
                    "fecha": fecha,
                    "tipo": "dia_completo",
                    "estados_cero_count": count
                })
            
            # 5. Verificar si es el último momento del día (isha) para trigger semanal
            if momento == "isha":
                print(f"🌙 Último momento del día ({fecha}): {momento}")
                self.queue.emit("dashboard_trigger", {
                    "fecha": fecha,
                    "tipo": "fin_dia",
                    "momento": momento
                })
            
            self.processed_count += 1
            return True
            
        except Exception as e:
            print(f"❌ Error procesando Estado Cero: {e}")
            self.error_count += 1
            return False
    
    def parse_obsidian_frontmatter(self, archivo_path: str) -> dict:
        """
        Parsea el frontmatter YAML del archivo de Obsidian
        
        Args:
            archivo_path: Ruta al archivo MD
            
        Returns:
            Dict con metadata parseada
        """
        try:
            with open(archivo_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscar frontmatter entre ---
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter_str = parts[1].strip()
                    
                    # Parse simple de YAML (básico)
                    metadata = {}
                    for line in frontmatter_str.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            # Convertir tipos básicos
                            if value.lower() in ['true', 'false']:
                                value = value.lower() == 'true'
                            elif value.isdigit():
                                value = int(value)
                            elif value.replace('.', '').isdigit():
                                value = float(value)
                            
                            metadata[key] = value
                    
                    return metadata
            
            return {}
            
        except Exception as e:
            print(f"⚠️ Error parseando frontmatter de {archivo_path}: {e}")
            return {}
    
    def count_estados_cero_dia(self, fecha: str) -> int:
        """
        Cuenta Estados Cero completados en una fecha
        
        Args:
            fecha: Fecha en formato YYYY-MM-DD
            
        Returns:
            Número de Estados Cero del día
        """
        try:
            # Buscar en storage/estados_cero
            storage_dir = Path("storage/estados_cero")
            if not storage_dir.exists():
                return 0
            
            count = 0
            for archivo in storage_dir.glob("*.json"):
                try:
                    with open(archivo, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if (data.get('fecha') == fecha and 
                        data.get('completado', False) and 
                        data.get('archivado_en_obsidian', False)):
                        count += 1
                        
                except (json.JSONDecodeError, KeyError):
                    continue
            
            return count
            
        except Exception as e:
            print(f"⚠️ Error contando Estados Cero del día {fecha}: {e}")
            return 0
    
    def run(self):
        """Loop principal del worker"""
        print("🔄 Worker de ingesta iniciado...")
        self.running = True
        
        while self.running:
            try:
                # Consumir eventos de Estados Cero completados
                event = self.queue.consume("estado_cero_completed")
                
                if event:
                    self.process_estado_cero_completed(event['data'])
                else:
                    # No hay eventos, esperar un poco
                    time.sleep(5)
                
                # Log de estado cada 60 segundos
                if self.processed_count > 0 and self.processed_count % 10 == 0:
                    print(f"📊 Worker procesados: {self.processed_count}, errores: {self.error_count}")
                
            except KeyboardInterrupt:
                print("🛑 Worker interrumpido por usuario")
                break
            except Exception as e:
                print(f"❌ Error en loop principal del worker: {e}")
                time.sleep(10)  # Esperar más tiempo en caso de error
        
        print(f"✅ Worker finalizado. Total procesados: {self.processed_count}, errores: {self.error_count}")
    
    def stop(self):
        """Detiene el worker"""
        self.running = False


def main():
    """Función principal para ejecutar el worker"""
    worker = IngestWorker()
    
    try:
        worker.run()
    except KeyboardInterrupt:
        print("🛑 Deteniendo worker...")
        worker.stop()


if __name__ == "__main__":
    main()
