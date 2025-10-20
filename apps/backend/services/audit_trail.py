"""
Sistema completo de audit trail para tracking de eventos
Registra todo con precisión de microsegundos
"""

from pathlib import Path
from datetime import datetime, date
from typing import Dict, Optional, List
import json
import time


class AuditTrail:
    """
    Sistema completo de audit trail para tracking de eventos
    Registra:
      - Timestamp preciso (microsegundos)
      - Tipo de evento
      - Origen (user, worker, scheduler)
      - Duración
      - Estado (success, error)
      - Metadata completa
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.audit_dir = self.vault_path / "00_System" / "Audit_Trail"
        self.audit_dir.mkdir(parents=True, exist_ok=True)
    
    def log_event(
        self,
        event_type: str,
        origen: str,
        estado: str,
        metadata: Dict,
        duracion_ms: Optional[int] = None
    ):
        """
        Registra evento en audit trail
        Crea archivo diario con todos los eventos
        """
        timestamp = datetime.now()
        fecha_str = timestamp.strftime("%Y-%m-%d")
        
        # Archivo audit diario
        audit_file = self.audit_dir / f"{fecha_str}.md"
        
        # Crear frontmatter si es nuevo archivo
        if not audit_file.exists():
            content = f"""---
tipo: audit-trail
fecha: {fecha_str}
eventos_registrados: 0
---

# Audit Trail - {fecha_str}

| Timestamp | Tipo | Origen | Estado | Duración | Metadata |
|-----------|------|--------|--------|----------|----------|
"""
            audit_file.write_text(content, encoding='utf-8')
        
        # Añadir línea de evento
        metadata_str = json.dumps(metadata, ensure_ascii=False)
        evento_linea = (
            f"| {timestamp.strftime('%H:%M:%S.%f')[:-3]} "
            f"| {event_type} "
            f"| {origen} "
            f"| {estado} "
            f"| {duracion_ms or '-'}ms "
            f"| {metadata_str} |\n"
        )
        
        with open(audit_file, 'a', encoding='utf-8') as f:
            f.write(evento_linea)
        
        # Actualizar contador en frontmatter
        self._update_event_count(audit_file)
    
    def _update_event_count(self, audit_file: Path):
        """Actualiza contador de eventos en frontmatter"""
        content = audit_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Contar líneas de tabla (excluir header y separador)
        table_lines = [l for l in lines if l.startswith('|') and 'Timestamp' not in l and '---' not in l]
        count = len(table_lines)
        
        # Actualizar frontmatter
        for i, line in enumerate(lines):
            if 'eventos_registrados:' in line:
                lines[i] = f"eventos_registrados: {count}"
                break
        
        audit_file.write_text('\n'.join(lines), encoding='utf-8')
    
    def get_eventos_dia(self, fecha: date) -> List[Dict]:
        """Obtiene todos los eventos de un día específico"""
        fecha_str = fecha.strftime("%Y-%m-%d")
        audit_file = self.audit_dir / f"{fecha_str}.md"
        
        if not audit_file.exists():
            return []
        
        content = audit_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        eventos = []
        for line in lines:
            if line.startswith('|') and 'Timestamp' not in line and '---' not in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 7:  # Incluye pipes iniciales y finales
                    try:
                        evento = {
                            'timestamp': parts[1],
                            'tipo': parts[2],
                            'origen': parts[3],
                            'estado': parts[4],
                            'duracion_ms': parts[5],
                            'metadata': json.loads(parts[6]) if parts[6] != '-' else {}
                        }
                        eventos.append(evento)
                    except:
                        continue
        
        return eventos

