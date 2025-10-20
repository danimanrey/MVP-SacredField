"""
Procesador del Universo Imaginal
Convierte notas de Obsidian en estrellas 3D con posicionamiento inteligente
"""

import math
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

from services.obsidian_parser import ObsidianParser, NotaObsidian
from models.universo import (
    Estrella, Vector3D, Constelacion, GrafoConocimiento,
    Orbita, UniversoImaginal, EstadisticasUniverso
)


class UniversoProcessor:
    """Procesador principal del universo imaginal"""
    
    def __init__(self, vault_path: str):
        self.parser = ObsidianParser(vault_path)
        
        # Ángulos por dimensión (distribución circular uniforme)
        self.dimension_angulos = {
            'finanzas': 0,          # Rojo - Norte
            'biologia': 51.43,      # Naranja
            'conocimiento': 102.86, # Amarillo
            'desarrollo': 154.29,   # Verde
            'relaciones': 205.71,   # Azul
            'creatividad': 257.14,  # Índigo
            'espiritualidad': 308.57 # Violeta
        }
    
    def generar_universo(
        self,
        tipo: str = "individual",
        owner_id: str = "default"
    ) -> UniversoImaginal:
        """Genera universo imaginal completo"""
        
        # 1. Parsear todas las notas
        notas = self.parser.listar_notas()
        
        # 2. Convertir a estrellas con posiciones 3D
        estrellas = self.generar_estrellas(notas)
        
        # 3. Identificar constelaciones (clusters)
        constelaciones = self.identificar_constelaciones(estrellas, notas)
        
        # 4. Crear grafo de conocimiento
        grafo = self._crear_grafo_conocimiento(estrellas, constelaciones, notas)
        
        # 5. Generar estadísticas
        estadisticas = self.generar_estadisticas(estrellas, notas)
        
        # 6. Órbitas (por ahora vacío, se integrará con calendario)
        orbitas = []
        
        return UniversoImaginal(
            tipo=tipo,
            owner_id=owner_id,
            grafo_conocimiento=grafo,
            orbitas=orbitas,
            estadisticas=estadisticas,
            fecha_actualizacion=datetime.now()
        )
    
    def generar_estrellas(self, notas: List[NotaObsidian]) -> List[Estrella]:
        """Convierte notas en estrellas con posiciones 3D"""
        
        # Obtener grafo de enlaces para calcular backlinks
        grafo = self.parser.obtener_grafo_enlaces(notas)
        
        estrellas = []
        
        for nota in notas:
            # Calcular backlinks
            backlinks = self.parser.obtener_backlinks(nota.filepath, grafo)
            total_conexiones = len(nota.enlaces) + len(backlinks)
            
            # Calcular posición 3D
            posicion = self.calcular_posicion_3d(nota, total_conexiones)
            
            # Calcular luminosidad (relevancia)
            luminosidad = self.calcular_luminosidad(total_conexiones, len(notas))
            
            # Crear estrella
            estrella = Estrella(
                id=nota.filepath,
                titulo=nota.titulo,
                contenido_preview=nota.contenido[:200] + '...' if len(nota.contenido) > 200 else nota.contenido,
                dimension=nota.dimension,
                color=nota.obtener_color(),
                posicion=posicion,
                luminosidad=luminosidad,
                enlaces=nota.enlaces,
                tags=nota.tags,
                metadata=nota.metadata,
                fecha_creacion=nota.fecha_creacion,
                num_enlaces=total_conexiones
            )
            
            estrellas.append(estrella)
        
        return estrellas
    
    def calcular_posicion_3d(
        self,
        nota: NotaObsidian,
        total_conexiones: int
    ) -> Vector3D:
        """
        Calcula posición 3D de una estrella
        
        - Distancia del centro: Basada en relevancia (más conexiones = más cerca)
        - Ángulo: Basado en dimensión
        - Altura (Z): Basada en fecha (más reciente = más arriba)
        """
        
        # 1. DISTANCIA (radio)
        # Más conexiones = más cerca del centro
        # Rango: 100 (muy conectada) a 500 (poco conectada)
        distancia_base = 500
        reduccion_por_enlace = 20
        distancia = max(100, distancia_base - (total_conexiones * reduccion_por_enlace))
        
        # 2. ÁNGULO (basado en dimensión)
        angulo_base = self.dimension_angulos.get(nota.dimension, 0)
        # Añadir variación para no amontonar todas en el mismo ángulo
        variacion = (hash(nota.filepath) % 60) - 30  # ±30 grados
        angulo = angulo_base + variacion
        
        # 3. ALTURA Z (basada en fecha)
        altura = self.calcular_altura_temporal(nota.fecha_creacion)
        
        # 4. Convertir coordenadas polares a cartesianas
        angulo_rad = math.radians(angulo)
        x = distancia * math.cos(angulo_rad)
        y = distancia * math.sin(angulo_rad)
        z = altura
        
        return Vector3D(x=x, y=y, z=z)
    
    def calcular_altura_temporal(self, fecha: datetime = None) -> float:
        """
        Calcula altura Z basada en la fecha
        Más reciente = más arriba
        """
        if not fecha:
            return 0.0
        
        ahora = datetime.now()
        dias_antiguedad = (ahora - fecha).days
        
        # Rango: -200 (muy antigua) a 200 (muy reciente)
        if dias_antiguedad <= 7:  # Semana reciente
            return 200
        elif dias_antiguedad <= 30:  # Mes reciente
            return 100
        elif dias_antiguedad <= 90:  # 3 meses
            return 0
        elif dias_antiguedad <= 180:  # 6 meses
            return -100
        else:  # Más antigua
            return -200
    
    def calcular_luminosidad(
        self,
        total_conexiones: int,
        total_notas: int
    ) -> float:
        """
        Calcula luminosidad de una estrella (0.0 - 1.0)
        Basada en su relevancia relativa
        """
        if total_notas == 0:
            return 0.3
        
        # Normalizar: 0 conexiones = 0.2, max conexiones = 1.0
        max_esperado = total_notas * 0.1  # Asumimos max 10% del total
        luminosidad = 0.2 + (0.8 * min(total_conexiones / max_esperado, 1.0))
        
        return round(luminosidad, 2)
    
    def identificar_constelaciones(
        self,
        estrellas: List[Estrella],
        notas: List[NotaObsidian]
    ) -> List[Constelacion]:
        """
        Identifica constelaciones (clusters de notas relacionadas)
        Usa algoritmo simple de clustering basado en enlaces
        """
        # Obtener grafo
        grafo = self.parser.obtener_grafo_enlaces(notas)
        
        # Identificar componentes conectados
        visitados = set()
        clusters = []
        
        def dfs(nota_id, cluster_actual):
            if nota_id in visitados:
                return
            visitados.add(nota_id)
            cluster_actual.append(nota_id)
            
            # Visitar vecinos
            for vecino in grafo.get(nota_id, []):
                dfs(vecino, cluster_actual)
        
        # Ejecutar DFS para cada nota no visitada
        for estrella in estrellas:
            if estrella.id not in visitados:
                cluster = []
                dfs(estrella.id, cluster)
                
                # Solo considerar clusters con al menos 2 estrellas
                if len(cluster) >= 2:
                    clusters.append(cluster)
        
        # Convertir clusters a Constelaciones
        constelaciones = []
        for i, cluster in enumerate(clusters):
            # Obtener estrellas del cluster
            estrellas_cluster = [e for e in estrellas if e.id in cluster]
            
            # Determinar dimensión principal
            dimensiones = [e.dimension for e in estrellas_cluster]
            dimension_principal = max(set(dimensiones), key=dimensiones.count)
            
            # Color de la dimensión principal
            color = estrellas_cluster[0].obtener_color() if estrellas_cluster else "#6B7280"
            
            # Calcular centro de masa
            centro = self._calcular_centro_masa(estrellas_cluster)
            
            # Calcular densidad (qué tan conectadas están)
            total_enlaces_internos = sum(
                len([e for e in estrella.enlaces if e in cluster])
                for estrella in estrellas_cluster
            )
            max_enlaces_posibles = len(cluster) * (len(cluster) - 1)
            densidad = total_enlaces_internos / max_enlaces_posibles if max_enlaces_posibles > 0 else 0
            
            constelacion = Constelacion(
                id=f"constelacion-{i}",
                nombre=f"Constelación {dimension_principal.capitalize()}",
                estrellas=cluster,
                dimension_principal=dimension_principal,
                color=color,
                centro=centro,
                densidad=round(densidad, 2),
                importancia=len(cluster) * densidad  # Tamaño × densidad
            )
            
            constelaciones.append(constelacion)
        
        # Ordenar por importancia
        constelaciones.sort(key=lambda c: c.importancia, reverse=True)
        
        return constelaciones
    
    def _calcular_centro_masa(self, estrellas: List[Estrella]) -> Vector3D:
        """Calcula el centro de masa de un grupo de estrellas"""
        if not estrellas:
            return Vector3D(x=0, y=0, z=0)
        
        x_promedio = sum(e.posicion.x for e in estrellas) / len(estrellas)
        y_promedio = sum(e.posicion.y for e in estrellas) / len(estrellas)
        z_promedio = sum(e.posicion.z for e in estrellas) / len(estrellas)
        
        return Vector3D(x=x_promedio, y=y_promedio, z=z_promedio)
    
    def _crear_grafo_conocimiento(
        self,
        estrellas: List[Estrella],
        constelaciones: List[Constelacion],
        notas: List[NotaObsidian]
    ) -> GrafoConocimiento:
        """Crea el grafo de conocimiento completo"""
        
        # Contar enlaces totales
        total_enlaces = sum(e.num_enlaces for e in estrellas) // 2  # Dividir por 2 (cada enlace cuenta doble)
        
        # Balance por dimensión
        dimensiones_balance = {}
        for estrella in estrellas:
            dim = estrella.dimension
            dimensiones_balance[dim] = dimensiones_balance.get(dim, 0) + 1
        
        return GrafoConocimiento(
            estrellas=estrellas,
            constelaciones=constelaciones,
            total_enlaces=total_enlaces,
            dimensiones_balance=dimensiones_balance,
            fecha_generacion=datetime.now()
        )
    
    def generar_estadisticas(
        self,
        estrellas: List[Estrella],
        notas: List[NotaObsidian]
    ) -> Dict:
        """Genera estadísticas del universo"""
        
        if not estrellas:
            return {}
        
        # Hubs (>= 3 conexiones)
        hubs = [e for e in estrellas if e.num_enlaces >= 3]
        
        # Orphans (0 conexiones)
        orphans = [e for e in estrellas if e.num_enlaces == 0]
        
        # Promedio de enlaces
        promedio_enlaces = sum(e.num_enlaces for e in estrellas) / len(estrellas)
        
        # Densidad del grafo
        max_enlaces_posibles = len(estrellas) * (len(estrellas) - 1) / 2
        enlaces_reales = sum(e.num_enlaces for e in estrellas) / 2
        densidad = enlaces_reales / max_enlaces_posibles if max_enlaces_posibles > 0 else 0
        
        # Por dimensión
        por_dimension = {}
        for estrella in estrellas:
            dim = estrella.dimension
            por_dimension[dim] = por_dimension.get(dim, 0) + 1
        
        return {
            'total_estrellas': len(estrellas),
            'total_enlaces': int(enlaces_reales),
            'promedio_enlaces_por_estrella': round(promedio_enlaces, 2),
            'estrellas_por_dimension': por_dimension,
            'hubs_count': len(hubs),
            'orphans_count': len(orphans),
            'densidad_grafo': round(densidad, 3)
        }

