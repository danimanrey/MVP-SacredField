"""
🧬 Metabolizador de Metadatos
==============================

El organismo extrae y metaboliza metadatos automáticamente
para generar insights valiosos y refinarse continuamente.

NO requiere intervención manual. Aprende observando.
"""

from datetime import date, datetime, timedelta
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from collections import Counter
import json

from models.database import EstadoCeroDB
from models.prisma_personal import PrismaPersonal, MetadatosOperativos
from services.sumario_contexto import GestorSumarioContexto


class MetabolizadorMetadatos:
    """
    Extrae y metaboliza metadatos del uso del sistema.
    
    Aprende:
    - Patrones biológicos reales
    - Patrones de decisión
    - Patrones de conocimiento
    - Patrones de manifestación
    """
    
    def __init__(self, db: Session, prisma: PrismaPersonal):
        self.db = db
        self.prisma = prisma
    
    async def metabolizar_semana(self) -> MetadatosOperativos:
        """
        Metaboliza datos de la última semana.
        Actualiza metadatos operativos del prisma.
        """
        
        hace_7_dias = date.today() - timedelta(days=7)
        
        # Obtener todos los Estados Cero de la semana
        estados = self.db.query(EstadoCeroDB).filter(
            EstadoCeroDB.fecha >= datetime.combine(hace_7_dias, datetime.min.time())
        ).all()
        
        if len(estados) < 7:  # Menos de 1 semana de datos
            print(f"⏳ Solo {len(estados)} Estados Cero. Necesito ≥7 para metabolizar.")
            return self.prisma.metadatos_operativos
        
        # Metabolizar cada tipo de patrón
        patrones_bio = self._extraer_patrones_biologicos(estados)
        patrones_decision = self._extraer_patrones_decision(estados)
        patrones_conocimiento = await self._extraer_patrones_conocimiento()
        patrones_manifestacion = self._extraer_patrones_manifestacion()
        
        # Actualizar metadatos
        metadatos = MetadatosOperativos(
            # Biológicos
            pico_energia_real=patrones_bio["pico_energia"],
            duracion_flujo_promedio=patrones_bio["duracion_flujo"],
            dias_alta_expansion=patrones_bio["dias_expansion"],
            
            # Decisión
            ratio_expansion_contraccion=patrones_decision["ratio"],
            categorias_maxima_expansion=patrones_decision["categorias_top"],
            decisiones_recurrentes=patrones_decision["recurrentes"],
            
            # Conocimiento
            temas_mas_explorados=patrones_conocimiento["temas_top"],
            frecuencia_captura_notas=patrones_conocimiento["frecuencia"],
            ratio_captura_vs_sintesis=patrones_conocimiento["ratio"],
            
            # Manifestación
            tasa_completitud_manifestaciones=patrones_manifestacion["tasa_completitud"],
            tiempo_promedio_materializacion=patrones_manifestacion["tiempo_promedio"],
            
            # Meta
            ultima_actualizacion=date.today(),
            dias_datos=len({e.fecha.date() for e in estados})
        )
        
        return metadatos
    
    def _extraer_patrones_biologicos(self, estados: List[EstadoCeroDB]) -> Dict:
        """
        Extrae patrones biológicos reales del usuario.
        
        ¿Cuándo tiene más energía REALMENTE?
        No lo que declaró, sino lo que demuestra.
        """
        
        # Agrupar por hora
        expansion_por_hora = {}
        
        for estado in estados:
            hora = estado.fecha.hour
            
            if estado.respuestas:
                respuestas = json.loads(estado.respuestas)
                
                # Calcular expansión promedio
                expansiones = [
                    r.get("intensidad", 3) for r in respuestas
                    if r.get("sensacion") == "expansion"
                ]
                
                if expansiones:
                    expansion_promedio = sum(expansiones) / len(expansiones)
                    
                    if hora not in expansion_por_hora:
                        expansion_por_hora[hora] = []
                    expansion_por_hora[hora].append(expansion_promedio)
        
        # Calcular promedios por hora
        promedios_hora = {
            hora: sum(expansiones) / len(expansiones)
            for hora, expansiones in expansion_por_hora.items()
        }
        
        # Identificar pico de energía (top 3 horas)
        if promedios_hora:
            top_horas = sorted(promedios_hora.items(), key=lambda x: x[1], reverse=True)[:3]
            hora_inicio = min(h for h, _ in top_horas)
            hora_fin = max(h for h, _ in top_horas) + 1
            pico_energia = f"{hora_inicio:02d}:00-{hora_fin:02d}:00"
        else:
            pico_energia = "Datos insuficientes"
        
        # Duración de flujo (estimado por tiempo entre Estados Cero con expansión alta)
        duracion_flujo = 90  # Default
        
        # Días de alta expansión
        expansion_por_dia = {}
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        for estado in estados:
            dia = dias_semana[estado.fecha.weekday()]
            
            if estado.respuestas:
                respuestas = json.loads(estado.respuestas)
                expansiones = [
                    r.get("intensidad", 3) for r in respuestas
                    if r.get("sensacion") == "expansion"
                ]
                
                if expansiones:
                    if dia not in expansion_por_dia:
                        expansion_por_dia[dia] = []
                    expansion_por_dia[dia].extend(expansiones)
        
        # Promedios por día
        promedios_dia = {
            dia: sum(expansiones) / len(expansiones)
            for dia, expansiones in expansion_por_dia.items()
        }
        
        # Top 3 días
        if promedios_dia:
            dias_expansion = sorted(promedios_dia.items(), key=lambda x: x[1], reverse=True)[:3]
            dias_alta = [dia for dia, _ in dias_expansion]
        else:
            dias_alta = []
        
        return {
            "pico_energia": pico_energia,
            "duracion_flujo": duracion_flujo,
            "dias_expansion": dias_alta
        }
    
    def _extraer_patrones_decision(self, estados: List[EstadoCeroDB]) -> Dict:
        """
        Extrae patrones de decisión del usuario.
        
        ¿Qué genera expansión?
        ¿Qué genera contracción?
        ¿Hay decisiones recurrentes?
        """
        
        total_expansiones = 0
        total_contracciones = 0
        categorias_expansion = []
        direcciones = []
        
        for estado in estados:
            if estado.respuestas:
                respuestas = json.loads(estado.respuestas)
                
                for r in respuestas:
                    if r.get("sensacion") == "expansion":
                        total_expansiones += 1
                        if "categoria" in r:
                            categorias_expansion.append(r["categoria"])
                    elif r.get("sensacion") == "contraccion":
                        total_contracciones += 1
            
            if estado.direccion:
                direcciones.append(estado.direccion.lower())
        
        # Ratio expansión/contracción
        total = total_expansiones + total_contracciones
        ratio = total_expansiones / total if total > 0 else 0.5
        
        # Categorías que más expansión generan
        if categorias_expansion:
            counter = Counter(categorias_expansion)
            categorias_top = [cat for cat, _ in counter.most_common(3)]
        else:
            categorias_top = []
        
        # Decisiones recurrentes (palabras clave en direcciones)
        decisiones_recurrentes = []
        if direcciones:
            # Extraer palabras clave comunes
            palabras = []
            for d in direcciones:
                palabras.extend(d.split())
            
            counter = Counter(palabras)
            # Filtrar palabras vacías
            stop_words = {'a', 'el', 'la', 'de', 'en', 'y', 'para', 'con', 'por', 'un', 'una'}
            palabras_clave = [
                palabra for palabra, count in counter.most_common(10)
                if palabra not in stop_words and len(palabra) > 4
            ][:3]
            
            decisiones_recurrentes = palabras_clave
        
        return {
            "ratio": ratio,
            "categorias_top": categorias_top,
            "recurrentes": decisiones_recurrentes
        }
    
    async def _extraer_patrones_conocimiento(self) -> Dict:
        """
        Extrae patrones de conocimiento.
        
        (Requiere integración con Obsidian/Anytype para datos reales)
        Por ahora retorna placeholders.
        """
        
        return {
            "temas_top": [],
            "frecuencia": "Datos insuficientes",
            "ratio": 0.0
        }
    
    def _extraer_patrones_manifestacion(self) -> Dict:
        """
        Extrae patrones de manifestación.
        
        ¿Cuántas manifestaciones se completan?
        ¿Cuánto tiempo tarda?
        """
        
        if not self.prisma.manifestaciones:
            return {
                "tasa_completitud": 0.0,
                "tiempo_promedio": "Sin datos"
            }
        
        # Calcular progreso promedio
        progreso_promedio = sum(m.progreso_estimado for m in self.prisma.manifestaciones) / len(self.prisma.manifestaciones)
        
        # Estimar tasa de completitud
        completadas = sum(1 for m in self.prisma.manifestaciones if m.progreso_estimado >= 100)
        tasa = completadas / len(self.prisma.manifestaciones) if self.prisma.manifestaciones else 0.0
        
        return {
            "tasa_completitud": tasa,
            "tiempo_promedio": "En análisis"
        }
    
    async def generar_insights_metabolizados(self, metadatos: MetadatosOperativos) -> List[str]:
        """
        Genera insights accionables basados en metadatos metabolizados.
        
        Estos insights:
        - Revelan patrones invisibles
        - Sugieren ajustes estructurales
        - Conectan con el prisma personal
        """
        
        insights = []
        
        # Insight biológico
        if metadatos.pico_energia_real != "Datos insuficientes":
            declarado = self.prisma.metodo_aprendizaje.mejor_momento_aprendizaje
            real = metadatos.pico_energia_real
            
            if declarado not in real:
                insights.append(
                    f"🔍 Tu pico de energía REAL ({real}) no coincide con lo declarado ({declarado}). "
                    f"¿Ajustar bloques profundos a este horario?"
                )
        
        # Insight de decisión
        if metadatos.ratio_expansion_contraccion < 0.5:
            insights.append(
                f"⚠️ Más contracciones que expansiones (ratio: {metadatos.ratio_expansion_contraccion:.2f}). "
                f"¿Estás forzando decisiones mentales? Tu {self.prisma.diseño_humano.autoridad.value} "
                f"puede estar siendo ignorada."
            )
        
        # Insight de días
        if metadatos.dias_alta_expansion:
            dias_declarados = []  # TODO: extraer de perfil
            dias_reales = metadatos.dias_alta_expansion
            
            insights.append(
                f"📊 Tus días de mayor expansión: {', '.join(dias_reales)}. "
                f"Reservar trabajo profundo para estos días."
            )
        
        # Insight de categorías
        if metadatos.categorias_maxima_expansion:
            top_cat = metadatos.categorias_maxima_expansion[0]
            insights.append(
                f"✨ La categoría '{top_cat}' genera tu mayor expansión. "
                f"¿Priorizar manifestaciones en esta dimensión?"
            )
        
        # Insight de manifestaciones
        if metadatos.tasa_completitud_manifestaciones < 0.3:
            insights.append(
                f"🎯 Tasa de completitud baja. Tipo {self.prisma.perfil_psicologico.eneagrama_base.value} "
                f"tiende a sobre-analizar. ¿Simplificar y priorizar 1 manifestación?"
            )
        
        return insights


async def metabolizar_y_guardar(db: Session, prisma: PrismaPersonal, ruta_prisma: str) -> List[str]:
    """
    Metaboliza metadatos y actualiza el prisma.
    
    Retorna insights generados.
    """
    
    metabolizador = MetabolizadorMetadatos(db, prisma)
    
    # Metabolizar
    print("🧬 Metabolizando datos de la última semana...")
    metadatos = await metabolizador.metabolizar_semana()
    
    # Generar insights
    print("💡 Generando insights...")
    insights = await metabolizador.generar_insights_metabolizados(metadatos)
    
    # Actualizar prisma
    prisma.metadatos_operativos = metadatos
    prisma.actualizado = date.today()
    
    # Guardar
    import json
    with open(ruta_prisma, 'w', encoding='utf-8') as f:
        f.write(prisma.model_dump_json(indent=2))
    
    print(f"✅ Prisma actualizado con {len(insights)} insights")
    
    return insights

