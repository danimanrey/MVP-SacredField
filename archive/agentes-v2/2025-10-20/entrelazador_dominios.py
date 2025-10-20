"""
🔗 Campo Sagrado - Entrelazador de Dominios
===========================================

Entrelaza los dominios de la vida (biológico, espiritual, financiero) 
basándose en los Estados Cero y genera acciones coordinadas.

Opera con pensamiento sistémico y reconocimiento de patrones.
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Any, Tuple
import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

@dataclass
class Dominio:
    """Representa un dominio de la vida"""
    nombre: str
    estado: str  # "expansión", "contracción", "equilibrio"
    energia: float  # 0.0 - 1.0
    urgencia: float  # 0.0 - 1.0
    recursos_disponibles: List[str]
    necesidades: List[str]

@dataclass
class Entrelazamiento:
    """Representa una conexión entre dominios"""
    dominios: List[str]
    tipo: str  # "apoyo", "conflicto", "secuencia", "sinergia"
    intensidad: float  # 0.0 - 1.0
    descripcion: str
    accion_sugerida: str

@dataclass
class AccionCoordinada:
    """Acción que coordina múltiples dominios"""
    nombre: str
    dominios_implicados: List[str]
    secuencia: List[str]  # Orden de ejecución
    tiempo_total: str
    recursos_totales: List[str]
    resultado_esperado: str
    indicadores_exito: List[str]
    urgencia: float
    impacto_sistémico: float

class EntrelazadorDominios:
    """
    Entrelaza dominios de la vida basándose en Estados Cero
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.estados_cero_dir = self.vault_path / "Estados-Cero"
        
        # Definir dominios principales
        self.dominios_principales = {
            "biologico": {
                "aspectos": ["salud", "ejercicio", "alimentación", "sueño", "energía física"],
                "indicadores": ["movimiento", "cuerpo", "ejercicio", "salud", "energía"],
                "recursos": ["tiempo", "espacio", "equipamiento", "motivación"],
                "necesidades": ["movimiento regular", "nutrición adecuada", "descanso", "cuidado"]
            },
            "espiritual": {
                "aspectos": ["propósito", "conexión", "significado", "fe", "meditación"],
                "indicadores": ["espíritu", "conexión", "propósito", "significado", "fe", "meditación"],
                "recursos": ["tiempo", "espacio sagrado", "atención", "compromiso"],
                "necesidades": ["quietud", "reflexión", "conexión", "propósito claro"]
            },
            "financiero": {
                "aspectos": ["ingresos", "gastos", "inversiones", "proyectos", "sostenibilidad"],
                "indicadores": ["dinero", "finanzas", "trabajo", "proyecto", "inversión", "ingresos"],
                "recursos": ["dinero", "tiempo", "habilidades", "red", "oportunidades"],
                "necesidades": ["flujo de ingresos", "gestión eficiente", "crecimiento", "seguridad"]
            },
            "conocimiento": {
                "aspectos": ["aprendizaje", "creatividad", "innovación", "sabiduría", "comprensión"],
                "indicadores": ["aprender", "crear", "estudiar", "leer", "escribir", "conocimiento"],
                "recursos": ["tiempo", "atención", "materiales", "mentores", "experiencia"],
                "necesidades": ["tiempo de estudio", "experimentación", "reflexión", "aplicación"]
            }
        }
    
    def analizar_estado_dominios(self, dias: int = 7) -> Dict[str, Dominio]:
        """
        Analiza el estado actual de cada dominio basándose en Estados Cero
        """
        estados = self._cargar_estados_ultimos_dias(dias)
        
        dominios_estado = {}
        
        for nombre_dominio, config in self.dominios_principales.items():
            estado_dominio = self._analizar_dominio_especifico(estados, nombre_dominio, config)
            dominios_estado[nombre_dominio] = estado_dominio
        
        return dominios_estado
    
    def detectar_entrelazamientos(self, dominios: Dict[str, Dominio]) -> List[Entrelazamiento]:
        """
        Detecta entrelazamientos entre dominios
        """
        entrelazamientos = []
        
        # Analizar todas las combinaciones de dominios
        nombres_dominios = list(dominios.keys())
        
        for i in range(len(nombres_dominios)):
            for j in range(i + 1, len(nombres_dominios)):
                dominio1 = nombres_dominios[i]
                dominio2 = nombres_dominios[j]
                
                entrelazamiento = self._analizar_entrelazamiento_par(
                    dominios[dominio1], 
                    dominios[dominio2], 
                    dominio1, 
                    dominio2
                )
                
                if entrelazamiento:
                    entrelazamientos.append(entrelazamiento)
        
        return entrelazamientos
    
    def generar_acciones_coordinadas(
        self, 
        dominios: Dict[str, Dominio], 
        entrelazamientos: List[Entrelazamiento]
    ) -> List[AccionCoordinada]:
        """
        Genera acciones que coordinan múltiples dominios
        """
        acciones = []
        
        # Acción basada en sinergias detectadas
        sinergias = [e for e in entrelazamientos if e.tipo == "sinergia"]
        for sinergia in sinergias:
            accion = self._crear_accion_sinergia(sinergia, dominios)
            if accion:
                acciones.append(accion)
        
        # Acción para resolver conflictos
        conflictos = [e for e in entrelazamientos if e.tipo == "conflicto"]
        for conflicto in conflictos:
            accion = self._crear_accion_resolucion_conflicto(conflicto, dominios)
            if accion:
                acciones.append(accion)
        
        # Acción de secuencia óptima
        secuencias = [e for e in entrelazamientos if e.tipo == "secuencia"]
        for secuencia in secuencias:
            accion = self._crear_accion_secuencia(secuencia, dominios)
            if accion:
                acciones.append(accion)
        
        return acciones
    
    def _cargar_estados_ultimos_dias(self, dias: int) -> List[Dict]:
        """Carga Estados Cero de los últimos N días"""
        estados = []
        fecha_inicio = date.today() - timedelta(days=dias)
        
        for i in range(dias):
            fecha_actual = fecha_inicio + timedelta(days=i)
            año = fecha_actual.year
            mes = f"{fecha_actual.month:02d}"
            
            dir_fecha = self.estados_cero_dir / str(año) / mes
            if dir_fecha.exists():
                for archivo in dir_fecha.glob(f"{fecha_actual.strftime('%d')}-*.md"):
                    estado = self._parsear_estado_cero(archivo)
                    if estado:
                        estados.append(estado)
        
        return estados
    
    def _parsear_estado_cero(self, archivo: Path) -> Optional[Dict]:
        """Parsea un archivo de Estado Cero"""
        try:
            contenido = archivo.read_text(encoding='utf-8')
            
            if contenido.startswith('---'):
                partes = contenido.split('---', 2)
                if len(partes) >= 3:
                    frontmatter = partes[1].strip()
                    cuerpo = partes[2].strip()
                    
                    metadata = {}
                    for linea in frontmatter.split('\n'):
                        if ':' in linea:
                            key, value = linea.split(':', 1)
                            metadata[key.strip()] = value.strip()
                    
                    return {
                        "archivo": str(archivo),
                        "fecha": metadata.get("fecha", ""),
                        "momento": metadata.get("momento", ""),
                        "tendencia": metadata.get("tendencia", ""),
                        "intensidad": float(metadata.get("intensidad", 0)),
                        "contenido": cuerpo.lower()
                    }
        except Exception as e:
            print(f"Error parseando {archivo}: {e}")
        
        return None
    
    def _analizar_dominio_especifico(self, estados: List[Dict], nombre_dominio: str, config: Dict) -> Dominio:
        """Analiza el estado de un dominio específico"""
        
        # Buscar menciones del dominio en los Estados Cero
        menciones = 0
        tendencias = []
        intensidades = []
        urgencias = []
        
        for estado in estados:
            contenido = estado.get("contenido", "")
            tendencia = estado.get("tendencia", "")
            intensidad = estado.get("intensidad", 0)
            
            # Verificar si el Estado Cero menciona este dominio
            for indicador in config["indicadores"]:
                if indicador in contenido:
                    menciones += 1
                    tendencias.append(tendencia)
                    intensidades.append(intensidad)
                    
                    # Calcular urgencia basada en intensidad y tipo de tendencia
                    if tendencia == "contracción":
                        urgencias.append(intensidad * 0.8)  # Contracción indica urgencia
                    elif tendencia == "expansión":
                        urgencias.append(intensidad * 0.3)  # Expansión es menos urgente
                    else:
                        urgencias.append(intensidad * 0.5)  # Equilibrio es moderado
                    break
        
        # Calcular métricas del dominio
        if menciones > 0:
            tendencia_predominante = max(set(tendencias), key=tendencias.count) if tendencias else "equilibrio"
            energia_promedio = sum(intensidades) / len(intensidades) if len(intensidades) > 0 else 0.0
            urgencia_promedio = sum(urgencias) / len(urgencias) if len(urgencias) > 0 else 0.0
        else:
            tendencia_predominante = "equilibrio"
            energia_promedio = 0.5  # Estado neutro
            urgencia_promedio = 0.3  # Urgencia baja por defecto
        
        return Dominio(
            nombre=nombre_dominio,
            estado=tendencia_predominante,
            energia=energia_promedio,
            urgencia=urgencia_promedio,
            recursos_disponibles=config["recursos"],
            necesidades=config["necesidades"]
        )
    
    def _analizar_entrelazamiento_par(self, dominio1: Dominio, dominio2: Dominio, nombre1: str, nombre2: str) -> Optional[Entrelazamiento]:
        """Analiza el entrelazamiento entre dos dominios específicos"""
        
        # Detectar tipo de entrelazamiento
        tipo_entrelazamiento = "neutral"
        intensidad = 0.0
        descripcion = ""
        accion_sugerida = ""
        
        # Lógica de detección de entrelazamientos
        
        # 1. Sinergia: Ambos en expansión
        if dominio1.estado == "expansión" and dominio2.estado == "expansión":
            tipo_entrelazamiento = "sinergia"
            intensidad = (dominio1.energia + dominio2.energia) / 2
            descripcion = f"Sinergia positiva entre {nombre1} y {nombre2} - ambos en expansión"
            accion_sugerida = f"Aprovechar el momento de expansión para acciones coordinadas entre {nombre1} y {nombre2}"
        
        # 2. Conflicto: Uno en expansión, otro en contracción
        elif (dominio1.estado == "expansión" and dominio2.estado == "contracción") or \
             (dominio1.estado == "contracción" and dominio2.estado == "expansión"):
            tipo_entrelazamiento = "conflicto"
            intensidad = abs(dominio1.energia - dominio2.energia)
            dominio_expansion = nombre1 if dominio1.estado == "expansión" else nombre2
            dominio_contraccion = nombre2 if dominio1.estado == "expansión" else nombre1
            descripcion = f"Conflicto energético: {dominio_expansion} en expansión vs {dominio_contraccion} en contracción"
            accion_sugerida = f"Buscar equilibrio entre {dominio_expansion} y {dominio_contraccion}"
        
        # 3. Secuencia: Uno necesita al otro para funcionar
        elif self._detectar_dependencia_secuencial(nombre1, nombre2):
            tipo_entrelazamiento = "secuencia"
            intensidad = max(dominio1.urgencia, dominio2.urgencia)
            descripcion = f"Secuencia óptima: {nombre1} → {nombre2}"
            accion_sugerida = f"Ejecutar {nombre1} antes que {nombre2} para máximo impacto"
        
        # 4. Apoyo: Uno puede ayudar al otro
        elif self._detectar_apoyo_mutuo(nombre1, nombre2):
            tipo_entrelazamiento = "apoyo"
            intensidad = (dominio1.energia + dominio2.energia) / 2
            descripcion = f"Apoyo mutuo entre {nombre1} y {nombre2}"
            accion_sugerida = f"Usar fortalezas de {nombre1} para apoyar {nombre2} y viceversa"
        
        # Solo retornar si hay un entrelazamiento significativo
        if tipo_entrelazamiento != "neutral" and intensidad > 0.3:
            return Entrelazamiento(
                dominios=[nombre1, nombre2],
                tipo=tipo_entrelazamiento,
                intensidad=intensidad,
                descripcion=descripcion,
                accion_sugerida=accion_sugerida
            )
        
        return None
    
    def _detectar_dependencia_secuencial(self, dominio1: str, dominio2: str) -> bool:
        """Detecta si un dominio depende secuencialmente del otro"""
        dependencias = {
            "biologico": ["espiritual"],  # El bienestar físico facilita la práctica espiritual
            "espiritual": ["conocimiento"],  # La claridad espiritual facilita el aprendizaje
            "conocimiento": ["financiero"],  # El conocimiento aplicado genera valor financiero
            "financiero": ["biologico"]  # La estabilidad financiera permite mejor cuidado físico
        }
        
        return dominio2 in dependencias.get(dominio1, [])
    
    def _detectar_apoyo_mutuo(self, dominio1: str, dominio2: str) -> bool:
        """Detecta si dos dominios se apoyan mutuamente"""
        apoyos = {
            "biologico": ["espiritual", "conocimiento"],
            "espiritual": ["biologico", "financiero"],
            "financiero": ["espiritual", "conocimiento"],
            "conocimiento": ["financiero", "biologico"]
        }
        
        return dominio2 in apoyos.get(dominio1, [])
    
    def _crear_accion_sinergia(self, sinergia: Entrelazamiento, dominios: Dict[str, Dominio]) -> Optional[AccionCoordinada]:
        """Crea una acción que aprovecha la sinergia entre dominios"""
        
        if sinergia.intensidad < 0.6:
            return None
        
        dominios_implicados = sinergia.dominios
        recursos_totales = []
        necesidades_totales = []
        
        for dominio_nombre in dominios_implicados:
            dominio = dominios[dominio_nombre]
            recursos_totales.extend(dominio.recursos_disponibles)
            necesidades_totales.extend(dominio.necesidades)
        
        # Eliminar duplicados
        recursos_totales = list(set(recursos_totales))
        necesidades_totales = list(set(necesidades_totales))
        
        return AccionCoordinada(
            nombre=f"Sinergia {sinergia.dominios[0].title()}-{sinergia.dominios[1].title()}",
            dominios_implicados=dominios_implicados,
            secuencia=dominios_implicados,  # Ejecutar en paralelo
            tiempo_total="2-4 horas",
            recursos_totales=recursos_totales,
            resultado_esperado=f"Amplificación mutua entre {' y '.join(dominios_implicados)}",
            indicadores_exito=[
                "energía sostenida en ambos dominios",
                "progreso visible en múltiples áreas",
                "sensación de flujo y coordinación",
                "impacto multiplicador observable"
            ],
            urgencia=sinergia.intensidad,
            impacto_sistémico=sinergia.intensidad * 1.2
        )
    
    def _crear_accion_resolucion_conflicto(self, conflicto: Entrelazamiento, dominios: Dict[str, Dominio]) -> Optional[AccionCoordinada]:
        """Crea una acción para resolver conflictos entre dominios"""
        
        if conflicto.intensidad < 0.4:
            return None
        
        dominios_implicados = conflicto.dominios
        
        return AccionCoordinada(
            nombre=f"Equilibrio {conflicto.dominios[0].title()}-{conflicto.dominios[1].title()}",
            dominios_implicados=dominios_implicados,
            secuencia=["espiritual", "biologico", "financiero", "conocimiento"],  # Secuencia de equilibrio
            tiempo_total="1-2 horas",
            recursos_totales=["tiempo", "atención", "espacio tranquilo"],
            resultado_esperado=f"Equilibrio energético entre {' y '.join(dominios_implicados)}",
            indicadores_exito=[
                "reducción de tensión entre dominios",
                "energía más equilibrada",
                "mayor claridad sobre prioridades",
                "sensación de armonía"
            ],
            urgencia=conflicto.intensidad,
            impacto_sistémico=conflicto.intensidad * 0.8
        )
    
    def _crear_accion_secuencia(self, secuencia: Entrelazamiento, dominios: Dict[str, Dominio]) -> Optional[AccionCoordinada]:
        """Crea una acción basada en secuencia óptima entre dominios"""
        
        return AccionCoordinada(
            nombre=f"Secuencia Óptima {secuencia.dominios[0].title()} → {secuencia.dominios[1].title()}",
            dominios_implicados=secuencia.dominios,
            secuencia=secuencia.dominios,  # Orden específico
            tiempo_total="1-3 horas",
            recursos_totales=["tiempo", "atención", "energía"],
            resultado_esperado=f"Progreso optimizado siguiendo secuencia {secuencia.dominios[0]} → {secuencia.dominios[1]}",
            indicadores_exito=[
                "mayor eficiencia en la ejecución",
                "menos resistencia",
                "progreso más rápido",
                "mejor calidad de resultados"
            ],
            urgencia=secuencia.intensidad * 0.7,
            impacto_sistémico=secuencia.intensidad
        )
    
    def generar_reporte_entrelazamiento(self, dominios: Dict[str, Dominio], entrelazamientos: List[Entrelazamiento], acciones: List[AccionCoordinada]) -> str:
        """Genera reporte de entrelazamiento en formato Markdown"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        reporte = f"""---
tipo: entrelazamiento-dominios
fecha: {date.today().isoformat()}
timestamp: {timestamp}
---

# 🔗 Entrelazamiento de Dominios - {date.today().strftime("%d/%m/%Y")}

## 🎯 Estado de los Dominios

"""
        
        for nombre, dominio in dominios.items():
            reporte += f"""### {nombre.title()}
- **Estado:** {dominio.estado.title()}
- **Energía:** {dominio.energia:.1%}
- **Urgencia:** {dominio.urgencia:.1%}
- **Recursos disponibles:** {', '.join(dominio.recursos_disponibles)}
- **Necesidades:** {', '.join(dominio.necesidades)}

"""
        
        if entrelazamientos:
            reporte += "## 🔗 Entrelazamientos Detectados\n\n"
            for entrelazamiento in entrelazamientos:
                reporte += f"""### {', '.join(entrelazamiento.dominios).title()}
- **Tipo:** {entrelazamiento.tipo.title()}
- **Intensidad:** {entrelazamiento.intensidad:.1%}
- **Descripción:** {entrelazamiento.descripcion}
- **Acción sugerida:** {entrelazamiento.accion_sugerida}

"""
        
        if acciones:
            reporte += "## 🎯 Acciones Coordinadas\n\n"
            for i, accion in enumerate(acciones, 1):
                reporte += f"""### {i}. {accion.nombre}
- **Dominios implicados:** {', '.join(accion.dominios_implicados)}
- **Secuencia:** {' → '.join(accion.secuencia)}
- **Tiempo total:** {accion.tiempo_total}
- **Urgencia:** {accion.urgencia:.1%}
- **Impacto sistémico:** {accion.impacto_sistémico:.1%}
- **Recursos totales:** {', '.join(accion.recursos_totales)}
- **Resultado esperado:** {accion.resultado_esperado}
- **Indicadores de éxito:**
"""
                for indicador in accion.indicadores_exito:
                    reporte += f"  - {indicador}\n"
                reporte += "\n"
        
        reporte += f"""---

*Entrelazamiento generado automáticamente por Campo Sagrado del Entrelazador - {timestamp}*
"""
        
        return reporte
    
    def guardar_reporte_entrelazamiento(self, dominios: Dict[str, Dominio], entrelazamientos: List[Entrelazamiento], acciones: List[AccionCoordinada]) -> str:
        """Guarda el reporte de entrelazamiento en Obsidian"""
        
        reporte = self.generar_reporte_entrelazamiento(dominios, entrelazamientos, acciones)
        
        # Crear directorio de entrelazamientos
        entrelazamiento_dir = self.vault_path / "Entrelazamiento-Dominios"
        entrelazamiento_dir.mkdir(exist_ok=True)
        
        # Guardar archivo
        fecha_str = date.today().strftime("%Y-%m-%d")
        archivo = entrelazamiento_dir / f"Entrelazamiento-Dominios-{fecha_str}.md"
        
        archivo.write_text(reporte, encoding='utf-8')
        
        return str(archivo)
