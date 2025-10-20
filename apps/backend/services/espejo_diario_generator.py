"""
Generador comprehensivo de Espejo Diario
Sintetiza 5 Estados Cero en una narrativa coherente
"""

from pathlib import Path
from datetime import date, datetime
from typing import List, Dict, Optional
import json
import os

# Asumiendo que estos agentes ya existen
try:
    from agentes.analizador_patrones import AnalizadorPatrones
    from agentes.entrelazador_dominios import EntrelazadorDominios
except ImportError:
    # Si no existen, crear stubs
    class AnalizadorPatrones:
        def __init__(self, vault_path):
            self.vault_path = vault_path
        def analizar_ultimos_estados(self, dias):
            return {}
    
    class EntrelazadorDominios:
        def __init__(self, vault_path):
            self.vault_path = vault_path
        def analizar_estado_dominios(self, dias):
            return {}
        def detectar_entrelazamientos(self, dominios):
            return []


class EspejoDiarioGenerator:
    """
    Genera Espejo Diario comprehensivo:
      - Resumen 5 Estados Cero
      - Análisis por dominio
      - Entrelazamientos detectados
      - Visualización temporal (ASCII art)
      - Insights narrativos
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.analizador = AnalizadorPatrones(vault_path)
        self.entrelazador = EntrelazadorDominios(vault_path)
        self.storage_path = Path("storage/estados_cero")
    
    def generar_espejo_completo(self, fecha: date) -> str:
        """Genera Espejo Diario completo para una fecha"""
        # 1. Cargar 5 Estados Cero del día
        estados = self._cargar_estados_dia(fecha)
        
        if not estados:
            return self._generar_espejo_vacio(fecha)
        
        # 2. Analizar por dominio
        dominios = self.entrelazador.analizar_estado_dominios(dias=1)
        
        # 3. Detectar entrelazamientos
        entrelazamientos = self.entrelazador.detectar_entrelazamientos(dominios) if dominios else []
        
        # 4. Generar visualización temporal
        viz_temporal = self._generar_visualizacion_temporal(estados)
        
        # 5. Generar narrativa
        narrativa = self._generar_narrativa_dia(estados, dominios, entrelazamientos)
        
        # 6. Compilar markdown
        return self._compilar_markdown(
            fecha, estados, dominios, 
            entrelazamientos, viz_temporal, narrativa
        )
    
    def _cargar_estados_dia(self, fecha: date) -> List[Dict]:
        """Carga todos los Estados Cero de un día"""
        estados = []
        fecha_str = fecha.strftime("%Y-%m-%d")
        
        # Buscar en storage local
        if self.storage_path.exists():
            for file in self.storage_path.glob("*.json"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get('fecha') == fecha_str:
                            estados.append(data)
                except:
                    continue
        
        # Ordenar por momento
        orden_momentos = {"fajr": 0, "dhuhr": 1, "asr": 2, "maghrib": 3, "isha": 4}
        estados.sort(key=lambda x: orden_momentos.get(x.get('momento', ''), 99))
        
        return estados
    
    def _generar_visualizacion_temporal(self, estados: List[Dict]) -> str:
        """
        Genera gráfica ASCII de tendencias a lo largo del día
        
        Ejemplo:
        ```
        Fajr    Dhuhr   Asr     Maghrib Isha
         ▲       ▲       ▼       ▼       ▲
        70%     85%     40%     35%     60%
        ```
        """
        viz = "## Flujo del Día\n\n```\n"
        momentos = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
        
        # Linea de momentos
        viz += "  ".join(f"{m:8s}" for m in momentos) + "\n"
        
        # Linea de flechas
        flechas = []
        for _ in momentos:
            # Buscar estado correspondiente
            momento_lower = _.lower()
            ec = next((e for e in estados if e.get('momento') == momento_lower), None)
            
            if ec:
                intensidad = ec.get('sintesis', {}).get('intensidad', 0.5)
                if intensidad > 0.6:
                    flechas.append("   ▲    ")
                elif intensidad < 0.4:
                    flechas.append("   ▼    ")
                else:
                    flechas.append("   ●    ")
            else:
                flechas.append("   -    ")
        
        viz += "".join(flechas) + "\n"
        
        # Linea de porcentajes
        porcentajes = []
        for _ in momentos:
            momento_lower = _.lower()
            ec = next((e for e in estados if e.get('momento') == momento_lower), None)
            if ec:
                intensidad = ec.get('sintesis', {}).get('intensidad', 0.0)
                porcentajes.append(f"{intensidad:6.0%}  ")
            else:
                porcentajes.append("   -    ")
        
        viz += "  ".join(porcentajes) + "\n"
        
        viz += "```\n\n"
        return viz
    
    def _generar_narrativa_dia(
        self, 
        estados: List[Dict],
        dominios: Dict,
        entrelazamientos: List
    ) -> str:
        """
        Genera narrativa comprehensiva del día
        Identifica:
          - Momento de mayor energía
          - Momento de mayor claridad
          - Transiciones significativas
          - Dominios en desequilibrio
        """
        narrativa = "## Narrativa del Día\n\n"
        
        if not estados:
            return narrativa + "*No hay Estados Cero para analizar.*\n\n"
        
        # Identificar picos y valles
        estados_con_intensidad = [e for e in estados if e.get('sintesis', {}).get('intensidad') is not None]
        
        if estados_con_intensidad:
            max_energia = max(estados_con_intensidad, key=lambda x: x.get('sintesis', {}).get('intensidad', 0))
            min_energia = min(estados_con_intensidad, key=lambda x: x.get('sintesis', {}).get('intensidad', 1))
            
            narrativa += f"**Punto Alto:** {max_energia.get('momento', '').upper()} "
            narrativa += f"({max_energia.get('sintesis', {}).get('intensidad', 0):.0%}) - "
            narrativa += f"{max_energia.get('reflexion') or 'Sin reflexión'}\n\n"
            
            narrativa += f"**Punto Bajo:** {min_energia.get('momento', '').upper()} "
            narrativa += f"({min_energia.get('sintesis', {}).get('intensidad', 0):.0%}) - "
            narrativa += f"{min_energia.get('reflexion') or 'Sin reflexión'}\n\n"
        
        # Analizar transiciones
        if len(estados_con_intensidad) > 1:
            narrativa += "### Transiciones Significativas\n\n"
            for i in range(len(estados_con_intensidad) - 1):
                actual = estados_con_intensidad[i]
                siguiente = estados_con_intensidad[i + 1]
                delta = siguiente.get('sintesis', {}).get('intensidad', 0) - actual.get('sintesis', {}).get('intensidad', 0)
                
                if abs(delta) > 0.3:  # Cambio significativo
                    direccion = "ascendió" if delta > 0 else "descendió"
                    narrativa += f"- De {actual.get('momento', '')} a {siguiente.get('momento', '')}: "
                    narrativa += f"La energía {direccion} {abs(delta):.0%}\n"
            narrativa += "\n"
        
        # Estado de Dominios
        if dominios:
            narrativa += "### Estado de Dominios\n\n"
            for nombre, dominio in dominios.items():
                estado_emoji = {
                    "expansion": "📈",
                    "contraccion": "📉",
                    "equilibrio": "⚖️"
                }.get(dominio.estado, "❓")
                
                narrativa += f"- **{nombre.title()}** {estado_emoji}: "
                narrativa += f"{dominio.estado} (Energía: {dominio.energia:.0%}, "
                narrativa += f"Urgencia: {dominio.urgencia:.0%})\n"
            narrativa += "\n"
        
        # Entrelazamientos clave
        if entrelazamientos:
            narrativa += "### Entrelazamientos Detectados\n\n"
            for e in entrelazamientos[:3]:  # Top 3
                narrativa += f"- **{' ↔ '.join(e.dominios)}** "
                narrativa += f"({e.tipo}, {e.intensidad:.0%}): "
                narrativa += f"{e.descripcion}\n"
            narrativa += "\n"
        
        return narrativa
    
    def _compilar_markdown(self, fecha, estados, dominios, entrelazamientos, viz, narrativa):
        """Compila todo en markdown comprehensivo"""
        
        md = f"""---
tipo: espejo-diario
fecha: {fecha.isoformat()}
estados_cero_completados: {len(estados)}
timestamp_generacion: {datetime.now().isoformat()}
---

# 🪞 Espejo Diario - {fecha.strftime('%d de %B, %Y')}

{viz}

{narrativa}

## Estados Cero del Día

"""
        for ec in estados:
            momento = ec.get('momento', '').upper()
            fecha_fmt = fecha.strftime('%Y/%m/%d')
            md += f"### {momento}\n\n"
            
            sintesis = ec.get('sintesis', {})
            md += f"- **Tendencia:** {sintesis.get('tendencia', 'N/A')} ({sintesis.get('intensidad', 0):.0%})\n"
            md += f"- **Intención:** {ec.get('intencion') or 'No especificada'}\n"
            md += f"- **Reflexión:** {ec.get('reflexion') or 'No especificada'}\n\n"
        
        md += """
## Metadatos del Organismo

- **Coherencia del día:** (Calculado desde variabilidad de intensidades)
- **Dominio predominante:** (Desde análisis de entrelazamientos)
- **Siguiente foco sugerido:** (Desde patrones emergentes)

---

*Generado automáticamente por Campo Sagrado del Entrelazador*
"""
        return md
    
    def _generar_espejo_vacio(self, fecha: date) -> str:
        """Genera espejo vacío cuando no hay Estados Cero"""
        return f"""---
tipo: espejo-diario
fecha: {fecha.isoformat()}
estados_cero_completados: 0
timestamp_generacion: {datetime.now().isoformat()}
---

# 🪞 Espejo Diario - {fecha.strftime('%d de %B, %Y')}

## Estados Cero del Día

*No se completaron Estados Cero en este día.*

---

*Generado automáticamente por Campo Sagrado del Entrelazador*
"""

