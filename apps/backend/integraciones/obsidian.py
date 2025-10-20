import os
from pathlib import Path
from typing import Optional
import yaml


class ObsidianVault:
    """Gestión del vault de Obsidian"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(os.path.expanduser(vault_path))
        self._crear_estructura()
    
    def _crear_estructura(self):
        """Crea estructura de carpetas si no existe"""
        carpetas = [
            "00-Pilares",
            "10-Dominios",
            "20-Proyectos",
            "30-Recursos",
            "40-Journal",
            "50-Conversaciones-IA",
            "50-Conversaciones-IA/Estados-Cero"
        ]
        
        for carpeta in carpetas:
            path = self.vault_path / carpeta
            path.mkdir(parents=True, exist_ok=True)
    
    def guardar_documento(self, filepath: str, contenido: str):
        """Guarda documento en el vault"""
        full_path = self.vault_path / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        return str(full_path)
    
    def leer_documento(self, filepath: str) -> Optional[str]:
        """Lee documento del vault"""
        full_path = self.vault_path / filepath
        
        if not full_path.exists():
            return None
        
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def listar_documentos(self, carpeta: str = "", extension: str = ".md"):
        """Lista documentos en una carpeta"""
        path = self.vault_path / carpeta
        
        if not path.exists():
            return []
        
        return [
            str(f.relative_to(self.vault_path))
            for f in path.rglob(f"*{extension}")
        ]
