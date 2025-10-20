"""
Parser avanzado de Obsidian Vault
Lee notas, extrae metadata, identifica enlaces, asigna dimensiones
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Set
from datetime import datetime
import yaml


class NotaObsidian:
    """Representa una nota de Obsidian con toda su metadata"""
    
    def __init__(
        self,
        filepath: str,
        titulo: str,
        contenido: str,
        metadata: Dict,
        enlaces: List[str],
        tags: List[str],
        dimension: Optional[str] = None
    ):
        self.filepath = filepath
        self.titulo = titulo
        self.contenido = contenido
        self.metadata = metadata
        self.enlaces = enlaces
        self.tags = tags
        self.dimension = dimension or self._inferir_dimension()
        self.fecha_creacion = metadata.get('fecha') or self._extraer_fecha_filepath()
        self.fecha_modificacion = None  # Se puede obtener del filesystem
    
    def _inferir_dimension(self) -> str:
        """Infiere dimensión desde tags o metadata"""
        # Primero intentar desde metadata YAML
        if 'dimension' in self.metadata:
            return self.metadata['dimension']
        
        # Luego desde tags
        dimension_tags = {
            'finanzas', 'dinero', 'ingresos', 'gastos', 'inversiones',
            'biologia', 'salud', 'energia', 'ejercicio', 'alimentacion',
            'conocimiento', 'aprendizaje', 'libros', 'cursos', 'estudio',
            'desarrollo', 'proyectos', 'codigo', 'creacion', 'build',
            'relaciones', 'familia', 'amigos', 'comunidad', 'networking',
            'creatividad', 'arte', 'musica', 'escritura', 'diseño',
            'espiritualidad', 'meditacion', 'filosofia', 'proposito'
        }
        
        for tag in self.tags:
            tag_lower = tag.lower()
            for dim_tag in dimension_tags:
                if dim_tag in tag_lower:
                    # Mapear a dimensión correcta
                    if dim_tag in ['finanzas', 'dinero', 'ingresos', 'gastos', 'inversiones']:
                        return 'finanzas'
                    elif dim_tag in ['biologia', 'salud', 'energia', 'ejercicio', 'alimentacion']:
                        return 'biologia'
                    elif dim_tag in ['conocimiento', 'aprendizaje', 'libros', 'cursos', 'estudio']:
                        return 'conocimiento'
                    elif dim_tag in ['desarrollo', 'proyectos', 'codigo', 'creacion', 'build']:
                        return 'desarrollo'
                    elif dim_tag in ['relaciones', 'familia', 'amigos', 'comunidad', 'networking']:
                        return 'relaciones'
                    elif dim_tag in ['creatividad', 'arte', 'musica', 'escritura', 'diseño']:
                        return 'creatividad'
                    elif dim_tag in ['espiritualidad', 'meditacion', 'filosofia', 'proposito']:
                        return 'espiritualidad'
        
        # Inferir desde carpeta
        if 'Finanzas' in self.filepath or '10-Dominios' in self.filepath:
            return self._inferir_desde_carpeta()
        
        # Por defecto
        return 'conocimiento'
    
    def _inferir_desde_carpeta(self) -> str:
        """Infiere dimensión desde la carpeta donde está la nota"""
        carpeta_map = {
            '00-Pilares': 'espiritualidad',
            '10-Dominios': 'desarrollo',
            '20-Proyectos': 'desarrollo',
            '30-Recursos': 'conocimiento',
            '40-Journal': 'biologia',
            'Estados-Cero': 'espiritualidad'
        }
        
        for carpeta, dimension in carpeta_map.items():
            if carpeta in self.filepath:
                return dimension
        
        return 'conocimiento'
    
    def _extraer_fecha_filepath(self) -> Optional[datetime]:
        """Extrae fecha del nombre del archivo si tiene formato YYYY-MM-DD"""
        match = re.search(r'(\d{4}-\d{2}-\d{2})', self.filepath)
        if match:
            try:
                return datetime.strptime(match.group(1), '%Y-%m-%d')
            except:
                pass
        return None
    
    def obtener_color(self) -> str:
        """Retorna color hexadecimal según dimensión"""
        colores = {
            'finanzas': '#DC2626',       # Rojo
            'biologia': '#F97316',       # Naranja
            'conocimiento': '#EAB308',   # Amarillo
            'desarrollo': '#22C55E',     # Verde
            'relaciones': '#3B82F6',     # Azul
            'creatividad': '#8B5CF6',    # Índigo/Púrpura
            'espiritualidad': '#A855F7'  # Violeta
        }
        return colores.get(self.dimension, '#6B7280')  # Gris por defecto
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario para serialización"""
        return {
            'filepath': self.filepath,
            'titulo': self.titulo,
            'contenido_preview': self.contenido[:200] + '...' if len(self.contenido) > 200 else self.contenido,
            'metadata': self.metadata,
            'enlaces': self.enlaces,
            'tags': self.tags,
            'dimension': self.dimension,
            'color': self.obtener_color(),
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'num_enlaces': len(self.enlaces),
            'num_caracteres': len(self.contenido)
        }


class ObsidianParser:
    """Parser completo del vault de Obsidian"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(os.path.expanduser(vault_path))
        if not self.vault_path.exists():
            raise ValueError(f"Vault no encontrado en: {vault_path}")
    
    def listar_notas(self, extension: str = ".md") -> List[NotaObsidian]:
        """Lista todas las notas del vault"""
        notas = []
        
        for archivo in self.vault_path.rglob(f"*{extension}"):
            # Ignorar archivos ocultos y templates
            if archivo.name.startswith('.') or 'templates' in str(archivo).lower():
                continue
            
            try:
                nota = self.parsear_nota(archivo)
                if nota:
                    notas.append(nota)
            except Exception as e:
                print(f"⚠️ Error parseando {archivo}: {e}")
                continue
        
        return notas
    
    def parsear_nota(self, filepath: Path) -> Optional[NotaObsidian]:
        """Parsea una nota individual"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                contenido_completo = f.read()
            
            # Extraer frontmatter YAML
            metadata = self._extraer_frontmatter(contenido_completo)
            
            # Extraer título (primera línea # o nombre del archivo)
            titulo = self._extraer_titulo(contenido_completo, filepath.stem)
            
            # Extraer enlaces [[nombre]]
            enlaces = self._extraer_enlaces(contenido_completo)
            
            # Extraer tags #tag
            tags = self._extraer_tags(contenido_completo)
            
            # Crear nota
            nota = NotaObsidian(
                filepath=str(filepath.relative_to(self.vault_path)),
                titulo=titulo,
                contenido=contenido_completo,
                metadata=metadata,
                enlaces=enlaces,
                tags=tags
            )
            
            return nota
            
        except Exception as e:
            print(f"Error parseando {filepath}: {e}")
            return None
    
    def _extraer_frontmatter(self, contenido: str) -> Dict:
        """Extrae metadata YAML del frontmatter"""
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(frontmatter_pattern, contenido, re.DOTALL)
        
        if match:
            try:
                return yaml.safe_load(match.group(1)) or {}
            except yaml.YAMLError:
                return {}
        
        return {}
    
    def _extraer_titulo(self, contenido: str, filename: str) -> str:
        """Extrae título de la nota"""
        # Primero buscar línea con # Título
        match = re.search(r'^#\s+(.+)$', contenido, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # Si no, usar nombre del archivo
        return filename
    
    def _extraer_enlaces(self, contenido: str) -> List[str]:
        """Extrae todos los enlaces [[nombre]] o [[nombre|alias]]"""
        # Patrón para enlaces tipo [[nota]] o [[nota|alias]]
        enlaces = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', contenido)
        return list(set(enlaces))  # Remover duplicados
    
    def _extraer_tags(self, contenido: str) -> List[str]:
        """Extrae todos los tags #tag"""
        tags = re.findall(r'#([a-zA-Z0-9_-]+)', contenido)
        return list(set(tags))  # Remover duplicados
    
    def obtener_grafo_enlaces(self, notas: List[NotaObsidian]) -> Dict[str, List[str]]:
        """Crea un grafo de enlaces entre notas"""
        grafo = {}
        
        # Crear mapa de títulos a filepath
        titulo_a_filepath = {nota.titulo: nota.filepath for nota in notas}
        
        for nota in notas:
            enlaces_reales = []
            
            for enlace in nota.enlaces:
                # Buscar nota enlazada
                if enlace in titulo_a_filepath:
                    enlaces_reales.append(titulo_a_filepath[enlace])
            
            grafo[nota.filepath] = enlaces_reales
        
        return grafo
    
    def obtener_backlinks(self, filepath: str, grafo: Dict[str, List[str]]) -> List[str]:
        """Obtiene lista de notas que enlazan a esta nota"""
        backlinks = []
        
        for nota_origen, enlaces in grafo.items():
            if filepath in enlaces:
                backlinks.append(nota_origen)
        
        return backlinks
    
    def identificar_hubs(self, notas: List[NotaObsidian], min_enlaces: int = 3) -> List[NotaObsidian]:
        """Identifica notas hub (muchos enlaces)"""
        grafo = self.obtener_grafo_enlaces(notas)
        
        hubs = []
        for nota in notas:
            backlinks = self.obtener_backlinks(nota.filepath, grafo)
            total_conexiones = len(nota.enlaces) + len(backlinks)
            
            if total_conexiones >= min_enlaces:
                hubs.append(nota)
        
        # Ordenar por número de conexiones
        hubs.sort(key=lambda n: len(n.enlaces) + len(self.obtener_backlinks(n.filepath, grafo)), reverse=True)
        
        return hubs
    
    def identificar_orphans(self, notas: List[NotaObsidian]) -> List[NotaObsidian]:
        """Identifica notas huérfanas (sin enlaces)"""
        grafo = self.obtener_grafo_enlaces(notas)
        
        orphans = []
        for nota in notas:
            backlinks = self.obtener_backlinks(nota.filepath, grafo)
            
            if len(nota.enlaces) == 0 and len(backlinks) == 0:
                orphans.append(nota)
        
        return orphans
    
    def obtener_estadisticas(self, notas: List[NotaObsidian]) -> Dict:
        """Obtiene estadísticas del vault"""
        if not notas:
            return {}
        
        grafo = self.obtener_grafo_enlaces(notas)
        
        # Contar por dimensión
        por_dimension = {}
        for nota in notas:
            dim = nota.dimension
            por_dimension[dim] = por_dimension.get(dim, 0) + 1
        
        # Calcular promedios
        total_enlaces = sum(len(nota.enlaces) for nota in notas)
        total_caracteres = sum(len(nota.contenido) for nota in notas)
        
        return {
            'total_notas': len(notas),
            'total_enlaces': total_enlaces,
            'promedio_enlaces_por_nota': round(total_enlaces / len(notas), 2),
            'promedio_caracteres_por_nota': round(total_caracteres / len(notas)),
            'por_dimension': por_dimension,
            'hubs': len(self.identificar_hubs(notas)),
            'orphans': len(self.identificar_orphans(notas))
        }


# Función de utilidad
def asignar_dimension_automatica(texto: str, tags: List[str] = None) -> str:
    """
    Asigna dimensión basándose en el contenido del texto
    Usa palabras clave y machine learning básico
    """
    texto_lower = texto.lower()
    tags = tags or []
    tags_lower = [t.lower() for t in tags]
    
    # Diccionario de palabras clave por dimensión
    keywords = {
        'finanzas': ['dinero', 'euros', 'dólares', 'ingreso', 'gasto', 'inversión', 'ahorro', 'presupuesto', 'factura', 'pago'],
        'biologia': ['salud', 'ejercicio', 'dormir', 'comida', 'energía', 'cuerpo', 'médico', 'vitamina', 'deporte', 'fitness'],
        'conocimiento': ['aprender', 'libro', 'curso', 'estudio', 'lectura', 'conocimiento', 'investigación', 'educación'],
        'desarrollo': ['proyecto', 'código', 'desarrollo', 'crear', 'build', 'feature', 'app', 'software', 'programar'],
        'relaciones': ['persona', 'familia', 'amigo', 'llamada', 'reunión', 'conversación', 'networking', 'equipo'],
        'creatividad': ['diseño', 'arte', 'música', 'escritura', 'creativo', 'inspiración', 'belleza', 'estética'],
        'espiritualidad': ['meditación', 'filosofía', 'propósito', 'valores', 'significado', 'transcendencia', 'consciencia']
    }
    
    # Contar coincidencias
    scores = {}
    for dimension, palabras in keywords.items():
        score = 0
        
        # Puntos por palabras clave en texto
        for palabra in palabras:
            score += texto_lower.count(palabra) * 2
        
        # Puntos por tags
        for tag in tags_lower:
            if any(palabra in tag for palabra in palabras):
                score += 5
        
        scores[dimension] = score
    
    # Retornar dimensión con mayor score
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)
    
    # Por defecto
    return 'conocimiento'

