"""
Sistema de cola de eventos simple basado en archivos JSON
Para el flujo Captura → Vault → Insights → Acción
"""

import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


class EventQueue:
    """Cola de eventos simple basada en archivos JSON"""
    
    def __init__(self, base_dir: str = "storage/events"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def emit(self, event_type: str, data: Dict[str, Any]) -> str:
        """
        Emite un evento creando un archivo JSON
        
        Args:
            event_type: Tipo de evento (ej: "estado_cero_completed")
            data: Datos del evento
            
        Returns:
            event_id: ID único del evento creado
        """
        # Crear ID único con timestamp y UUID
        timestamp = int(time.time())
        uuid_short = uuid.uuid4().hex[:8]
        event_id = f"{timestamp}_{uuid_short}"
        
        # Crear directorio para el tipo de evento
        event_dir = self.base_dir / event_type
        event_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear archivo JSON
        event_file = event_dir / f"event_{event_id}.json"
        
        event_data = {
            "event_id": event_id,
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        with open(event_file, 'w', encoding='utf-8') as f:
            json.dump(event_data, f, indent=2, ensure_ascii=False)
        
        return event_id
    
    def consume(self, event_type: str) -> Optional[Dict[str, Any]]:
        """
        Consume el primer evento del tipo especificado
        
        Args:
            event_type: Tipo de evento a consumir
            
        Returns:
            Dict con los datos del evento o None si no hay eventos
        """
        event_dir = self.base_dir / event_type
        
        if not event_dir.exists():
            return None
        
        # Buscar archivos de eventos ordenados por nombre (timestamp)
        event_files = sorted(event_dir.glob("event_*.json"))
        
        if not event_files:
            return None
        
        # Leer y eliminar el primer archivo
        event_file = event_files[0]
        
        try:
            with open(event_file, 'r', encoding='utf-8') as f:
                event_data = json.load(f)
            
            # Eliminar archivo después de leerlo
            event_file.unlink()
            
            return event_data
            
        except (json.JSONDecodeError, FileNotFoundError) as e:
            # Si hay error, eliminar archivo corrupto
            if event_file.exists():
                event_file.unlink()
            return None
    
    def peek(self, event_type: str) -> Optional[Dict[str, Any]]:
        """
        Lee el primer evento sin eliminarlo
        
        Args:
            event_type: Tipo de evento a leer
            
        Returns:
            Dict con los datos del evento o None si no hay eventos
        """
        event_dir = self.base_dir / event_type
        
        if not event_dir.exists():
            return None
        
        event_files = sorted(event_dir.glob("event_*.json"))
        
        if not event_files:
            return None
        
        try:
            with open(event_files[0], 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    
    def list_pending(self) -> Dict[str, int]:
        """
        Lista eventos pendientes por tipo
        
        Returns:
            Dict con {tipo_evento: cantidad_pendiente}
        """
        pending = {}
        
        if not self.base_dir.exists():
            return pending
        
        for event_dir in self.base_dir.iterdir():
            if event_dir.is_dir():
                event_files = list(event_dir.glob("event_*.json"))
                pending[event_dir.name] = len(event_files)
        
        return pending
    
    def clear_events(self, event_type: str = None) -> int:
        """
        Limpia eventos del tipo especificado o todos
        
        Args:
            event_type: Tipo específico o None para todos
            
        Returns:
            Número de archivos eliminados
        """
        deleted = 0
        
        if event_type:
            event_dir = self.base_dir / event_type
            if event_dir.exists():
                for event_file in event_dir.glob("event_*.json"):
                    event_file.unlink()
                    deleted += 1
        else:
            # Limpiar todos los tipos
            for event_dir in self.base_dir.iterdir():
                if event_dir.is_dir():
                    for event_file in event_dir.glob("event_*.json"):
                        event_file.unlink()
                        deleted += 1
        
        return deleted


# Instancia global para uso en la aplicación
event_queue = EventQueue()


def get_event_queue() -> EventQueue:
    """Obtiene la instancia global de EventQueue"""
    return event_queue
