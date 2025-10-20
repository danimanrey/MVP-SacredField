"""
🕌 Campo Sagrado - Agente Entrelazador Personal
================================================

Este agente es el corazón del reconocimiento de configuración individual.
Entrelaza todos los aspectos de la vida: deportes, comidas, finanzas,
aprendizaje, desarrollo e inversiones.

Opera con conciencia de patrones, sinergias y conflictos.
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import json

from models.schemas import (
    PerfilPersonal,
    DashboardEntrelazamiento,
    EntrelazamientoDia,
    RutinaDeportiva,
    ComidaConfiguracion,
    PresupuestoCategoria,
    TemaAprendizaje,
    ProyectoDesarrollo,
    InversionAsunto,
    ContextoCompleto,
    EstructuraDia,
    AnclaDia,
    TiemposRezoDia
)
from services.claude_client import claude_client
from services.propositos import (
    obtener_proposito_dia_semana,
    generar_anclas_dia,
    calcular_espacio_libre
)


class AgenteEntrelazador:
    """
    Agente que entrelaza todos los aspectos de la vida del usuario
    """
    
    def __init__(self):
        self.perfil_usuario: Optional[PerfilPersonal] = None
    
    def cargar_perfil(self, perfil: PerfilPersonal):
        """Carga el perfil personal del usuario"""
        self.perfil_usuario = perfil
        print(f"✅ Perfil cargado: {perfil.nombre}")
    
    def generar_estructura_dia(
        self,
        fecha: date,
        tiempos_liturgicos: TiemposRezoDia
    ) -> EstructuraDia:
        """
        Genera estructura base de un día específico.
        
        ESTRUCTURA COMPLETA Y FLEXIBLE:
        1. Anclas (rezo + Estado Cero) - INTOCABLES
        2. No-negociables - Pueden ajustar hora
        3. Rutinas del día - Del perfil
        4. Espacio libre calculado (objetivo: 40%)
        """
        
        if not self.perfil_usuario:
            raise Exception("Perfil no cargado. Ejecuta cargar_perfil() primero")
        
        # Determinar día de la semana
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        dia_semana = dias_semana[fecha.weekday()]
        
        # Obtener propósito del día
        proposito = obtener_proposito_dia_semana(dia_semana)
        
        # 1. ANCLAS (rezo + Estado Cero) - INTOCABLES
        anclas = generar_anclas_dia(tiempos_liturgicos)
        
        # 2. NO-NEGOCIABLES del perfil (genéricos)
        no_negociables = [
            {"nombre": "Movimiento", "ventana": "7:00-9:00", "duracion": 30, "tipo": "biologico"},
            {"nombre": "Comida nutritiva", "ventana": "12:00-14:00", "duracion": 45, "tipo": "biologico"},
            {"nombre": "Lectura profunda", "ventana": "flexible", "duracion": 45, "tipo": "conocimiento"}
        ]
        
        # 3. RUTINAS del día (del perfil)
        rutinas_hoy = []
        for rutina in self.perfil_usuario.rutinas_deportivas:
            if dia_semana in rutina.dias_semana:
                rutinas_hoy.append({
                    "nombre": rutina.nombre,
                    "hora_preferida": rutina.hora_preferida,
                    "duracion_minutos": rutina.duracion_minutos,
                    "intensidad": rutina.intensidad
                })
        
        # 4. Calcular espacio libre
        espacio_libre_min, espacio_libre_pct = calcular_espacio_libre(
            tiempos_liturgicos,
            no_negociables,
            rutinas_hoy
        )
        
        return EstructuraDia(
            fecha=fecha,
            dia_semana=dia_semana,
            proposito_dia=proposito.proposito,
            energia_dia=proposito.energia,
            tiempos_liturgicos=tiempos_liturgicos,
            anclas=[AnclaDia(**a) for a in anclas],
            no_negociables_dia=[],  # Se llenarán después
            espacio_libre_minutos=espacio_libre_min,
            espacio_libre_porcentaje=espacio_libre_pct,
            rutinas_dia=rutinas_hoy,
            proyectos_sugeridos=[],
            aprendizaje_sugerido=[],
            conflictos=[],
            sinergias=[]
        )
    
    def generar_dashboard_semanal(self, fecha_inicio: date = None) -> DashboardEntrelazamiento:
        """
        Genera el dashboard completo de entrelazamiento semanal
        
        Analiza:
        - Rutinas deportivas y cuándo encajan mejor
        - Sistema de comidas y batch cooking
        - Presupuesto y cuándo hacer compras
        - Temas de aprendizaje y bloques de estudio
        - Proyectos de desarrollo y hitos
        - Asuntos de inversión y decisiones pendientes
        """
        if not self.perfil_usuario:
            raise ValueError("❌ Perfil no cargado. Usa cargar_perfil() primero.")
        
        if not fecha_inicio:
            fecha_inicio = date.today()
        
        fecha_fin = fecha_inicio + timedelta(days=6)
        
        # Generar entrelazamiento para cada día de la semana
        dias_semana = []
        for i in range(7):
            dia = fecha_inicio + timedelta(days=i)
            entrelazamiento_dia = self._generar_entrelazamiento_dia(dia)
            dias_semana.append(entrelazamiento_dia)
        
        # Calcular resúmenes semanales
        sesiones_deportivas = self._calcular_sesiones_deportivas_semana(dias_semana)
        batch_cooking = self._planificar_batch_cooking_semana(dias_semana)
        compra_necesaria = self._calcular_compra_semanal()
        
        # Analizar patrones y optimizaciones
        patron_energia = self._analizar_patron_energia_semanal(dias_semana)
        sugerencias = self._generar_sugerencias_optimizacion(dias_semana, patron_energia)
        espacios_emergencia = self._identificar_espacios_emergencia(dias_semana)
        
        dashboard = DashboardEntrelazamiento(
            semana_inicio=fecha_inicio,
            semana_fin=fecha_fin,
            dias_semana=dias_semana,
            sesiones_deportivas_semana=sesiones_deportivas,
            objetivo_cumplido_deporte=sesiones_deportivas >= 3,
            batch_cooking_planificado=batch_cooking,
            compra_necesaria=compra_necesaria,
            gasto_semana_proyectado=self._calcular_gasto_proyectado(),
            presupuesto_disponible=self._calcular_presupuesto_disponible(),
            alertas_financieras=self._detectar_alertas_financieras(),
            horas_aprendizaje_semana=self._calcular_horas_aprendizaje(),
            temas_prioridad=self._obtener_temas_prioridad(),
            horas_desarrollo_semana=self._calcular_horas_desarrollo(),
            proyectos_avance=self._calcular_avance_proyectos(),
            decisiones_pendientes=self._obtener_decisiones_pendientes(),
            patron_energia_semanal=patron_energia,
            sugerencias_optimizacion=sugerencias,
            espacios_emergencia=espacios_emergencia
        )
        
        return dashboard
    
    def _generar_entrelazamiento_dia(self, dia: date) -> EntrelazamientoDia:
        """Genera el entrelazamiento para un día específico"""
        dia_semana = self._nombre_dia(dia)
        
        # Deportes del día
        deportes_hoy = self._obtener_deportes_dia(dia_semana)
        
        # Comidas del día
        comidas_hoy = self._planificar_comidas_dia(dia_semana)
        
        # Finanzas del día
        necesita_compra = dia_semana == self.perfil_usuario.dia_compra_semanal
        presupuesto_disp = self._calcular_presupuesto_disponible()
        categorias_alerta = self._detectar_alertas_financieras()
        
        # Aprendizaje del día
        temas_sugeridos = self._sugerir_temas_aprendizaje_dia(dia_semana)
        
        # Desarrollo del día
        proyectos_sugeridos = self._sugerir_proyectos_dia(dia_semana)
        
        # Inversiones del día
        asuntos_revisar = self._obtener_asuntos_dia(dia)
        
        # Detectar conflictos y sinergias
        conflictos = self._detectar_conflictos_dia(deportes_hoy, comidas_hoy, temas_sugeridos, proyectos_sugeridos)
        sinergias = self._detectar_sinergias_dia(deportes_hoy, comidas_hoy, temas_sugeridos, proyectos_sugeridos)
        
        # Calcular energía requerida total
        energia_total = self._calcular_energia_requerida(deportes_hoy, proyectos_sugeridos, temas_sugeridos)
        
        # Generar recomendación principal del día
        recomendacion = self._generar_recomendacion_dia(dia, deportes_hoy, comidas_hoy, temas_sugeridos, proyectos_sugeridos)
        
        return EntrelazamientoDia(
            fecha=dia,
            deportes_hoy=deportes_hoy,
            comidas_hoy=comidas_hoy,
            necesita_compra=necesita_compra,
            presupuesto_disponible=presupuesto_disp,
            categorias_alerta=categorias_alerta,
            temas_sugeridos=temas_sugeridos,
            proyectos_sugeridos=proyectos_sugeridos,
            asuntos_revisar=asuntos_revisar,
            conflictos_detectados=conflictos,
            sinergias_detectadas=sinergias,
            recomendacion_principal=recomendacion,
            energia_requerida_total=energia_total
        )
    
    def _obtener_deportes_dia(self, dia_semana: str) -> List[dict]:
        """Obtiene las rutinas deportivas programadas para este día"""
        deportes = []
        for rutina in self.perfil_usuario.rutinas_deportivas:
            if dia_semana.lower() in [d.lower() for d in rutina.dias_semana]:
                deportes.append({
                    "nombre": rutina.nombre,
                    "tipo": rutina.tipo,
                    "hora_sugerida": rutina.hora_preferida,
                    "duracion": rutina.duracion_minutos,
                    "intensidad": rutina.intensidad,
                    "completado": False
                })
        return deportes
    
    def _planificar_comidas_dia(self, dia_semana: str) -> List[dict]:
        """Planifica las comidas del día"""
        comidas = []
        for comida_config in self.perfil_usuario.sistema_comidas:
            # Decidir si es día de batch cooking
            es_batch = (
                comida_config.batch_cooking and 
                comida_config.dias_batch and 
                dia_semana.lower() in [d.lower() for d in comida_config.dias_batch]
            )
            
            # Seleccionar receta (simplificado - se puede mejorar con IA)
            receta = comida_config.recetas_preferidas[0] if comida_config.recetas_preferidas else "Por definir"
            
            comidas.append({
                "tipo": comida_config.tipo,
                "hora": comida_config.hora_aproximada,
                "tiempo_cocinar": comida_config.duracion_preparacion,
                "receta_sugerida": receta,
                "es_batch_cooking": es_batch,
                "restricciones": comida_config.restricciones
            })
        return comidas
    
    def _sugerir_temas_aprendizaje_dia(self, dia_semana: str) -> List[dict]:
        """Sugiere qué temas estudiar hoy según prioridad y tiempo disponible"""
        temas_sugeridos = []
        
        # Ordenar temas por prioridad
        temas_ordenados = sorted(
            self.perfil_usuario.temas_aprendizaje,
            key=lambda t: t.prioridad,
            reverse=True
        )
        
        # Sugerir los 2-3 temas más prioritarios
        for tema in temas_ordenados[:3]:
            tiempo_sugerido = tema.tiempo_semanal_deseado // 7  # Distribuir en la semana
            
            temas_sugeridos.append({
                "tema": tema.nombre,
                "dominio": tema.dominio,
                "tiempo_sugerido": tiempo_sugerido,
                "prioridad": tema.prioridad,
                "recursos": tema.recursos[:2] if tema.recursos else [],
                "razon": f"Alta prioridad ({tema.prioridad}/5) en {tema.dominio}"
            })
        
        return temas_sugeridos
    
    def _sugerir_proyectos_dia(self, dia_semana: str) -> List[dict]:
        """Sugiere en qué proyectos trabajar hoy"""
        proyectos_sugeridos = []
        
        # Filtrar proyectos activos y ordenar por prioridad
        proyectos_activos = [
            p for p in self.perfil_usuario.proyectos_desarrollo 
            if p.estado == "activo"
        ]
        proyectos_ordenados = sorted(
            proyectos_activos,
            key=lambda p: (p.deadline or date.max, -p.prioridad)
        )
        
        # Sugerir los 2 proyectos más urgentes
        for proyecto in proyectos_ordenados[:2]:
            horas_dia = proyecto.horas_semanales_deseadas / 7
            tiempo_sugerido = int(horas_dia * 60)  # Convertir a minutos
            
            # Identificar próximos hitos
            proximos_hitos = proyecto.hitos[:2] if proyecto.hitos else ["Avanzar en el proyecto"]
            
            proyectos_sugeridos.append({
                "proyecto": proyecto.nombre,
                "tipo": proyecto.tipo,
                "tiempo_sugerido": tiempo_sugerido,
                "prioridad": proyecto.prioridad,
                "hitos_hoy": proximos_hitos,
                "deadline": proyecto.deadline.isoformat() if proyecto.deadline else None
            })
        
        return proyectos_sugeridos
    
    def _obtener_asuntos_dia(self, dia: date) -> List[dict]:
        """Obtiene asuntos de inversión que requieren atención hoy"""
        asuntos = []
        
        for asunto in self.perfil_usuario.inversiones_asuntos:
            # Asuntos con fecha de decisión cercana (próximos 7 días)
            if asunto.fecha_decision:
                dias_hasta_decision = (asunto.fecha_decision - dia).days
                if 0 <= dias_hasta_decision <= 7:
                    accion = "DECIDIR HOY" if dias_hasta_decision == 0 else f"Decidir en {dias_hasta_decision} días"
                    asuntos.append({
                        "asunto": asunto.nombre,
                        "tipo": asunto.tipo,
                        "accion_sugerida": accion,
                        "monto": asunto.monto_involucrado,
                        "prioridad": asunto.prioridad,
                        "urgencia": "alta" if dias_hasta_decision <= 2 else "media"
                    })
        
        return asuntos
    
    def _detectar_conflictos_dia(self, deportes, comidas, temas, proyectos) -> List[str]:
        """Detecta conflictos de tiempo o energía en el día"""
        conflictos = []
        
        # Conflicto: Demasiadas actividades de alta energía
        actividades_alta_energia = [d for d in deportes if d.get("intensidad", 0) >= 4]
        proyectos_demandantes = [p for p in proyectos if p.get("tiempo_sugerido", 0) > 120]
        
        if len(actividades_alta_energia) >= 2 and proyectos_demandantes:
            conflictos.append("⚠️ Muchas actividades de alta energía - considerar distribuir mejor")
        
        # Conflicto: Batch cooking + proyecto largo
        batch_cooking = any(c.get("es_batch_cooking") for c in comidas)
        if batch_cooking and proyectos_demandantes:
            conflictos.append("⚠️ Batch cooking + proyecto demandante - puede ser mucho para un día")
        
        # Conflicto: Tiempo total excesivo
        tiempo_total = (
            sum(d.get("duracion", 0) for d in deportes) +
            sum(c.get("tiempo_cocinar", 0) for c in comidas) +
            sum(t.get("tiempo_sugerido", 0) for t in temas) +
            sum(p.get("tiempo_sugerido", 0) for p in proyectos)
        )
        
        if tiempo_total > 480:  # Más de 8 horas
            conflictos.append(f"⚠️ Tiempo total muy alto: {tiempo_total//60}h {tiempo_total%60}min")
        
        return conflictos
    
    def _detectar_sinergias_dia(self, deportes, comidas, temas, proyectos) -> List[str]:
        """Detecta sinergias positivas entre actividades"""
        sinergias = []
        
        # Sinergia: Ejercicio matutino + proyectos creativos
        ejercicio_manana = any(
            d.get("hora_sugerida", "").startswith(("06", "07", "08"))
            for d in deportes
        )
        proyectos_creativos = any(
            p.get("tipo") in ["diseño", "escritura"]
            for p in proyectos
        )
        
        if ejercicio_manana and proyectos_creativos:
            sinergias.append("✨ Ejercicio matutino potencia creatividad para proyectos")
        
        # Sinergia: Batch cooking crea tiempo para estudio
        batch_cooking = any(c.get("es_batch_cooking") for c in comidas)
        if batch_cooking and temas:
            sinergias.append("✨ Batch cooking libera tiempo futuro para aprendizaje")
        
        # Sinergia: Balance energía
        tiene_ejercicio = len(deportes) > 0
        tiene_estudio = len(temas) > 0
        tiene_desarrollo = len(proyectos) > 0
        
        if tiene_ejercicio and tiene_estudio and tiene_desarrollo:
            sinergias.append("✨ Día balanceado: cuerpo, mente y creación")
        
        return sinergias
    
    def _calcular_energia_requerida(self, deportes, proyectos, temas) -> int:
        """Calcula la energía total requerida para el día (1-10)"""
        energia = 0
        
        # Deportes según intensidad
        for deporte in deportes:
            energia += deporte.get("intensidad", 3)
        
        # Proyectos según tiempo
        for proyecto in proyectos:
            tiempo = proyecto.get("tiempo_sugerido", 0)
            if tiempo > 180:  # Más de 3 horas
                energia += 4
            elif tiempo > 90:  # 1.5-3 horas
                energia += 3
            else:
                energia += 2
        
        # Aprendizaje según tiempo
        for tema in temas:
            tiempo = tema.get("tiempo_sugerido", 0)
            if tiempo > 60:
                energia += 2
            else:
                energia += 1
        
        return min(energia, 10)  # Máximo 10
    
    def _generar_recomendacion_dia(self, dia, deportes, comidas, temas, proyectos) -> str:
        """Genera la recomendación principal del día usando IA"""
        dia_nombre = self._nombre_dia(dia)
        
        # Si no hay Claude configurado, usar recomendación simple
        if not hasattr(claude_client, 'client') or not claude_client.client:
            if deportes:
                return f"Día de {deportes[0]['tipo']} - mantén alta energía"
            elif proyectos:
                return f"Enfócate en {proyectos[0]['proyecto']}"
            else:
                return "Día de baja demanda - perfecto para emergencia"
        
        # Construir contexto para Claude
        contexto = f"""Día: {dia_nombre}

Actividades planificadas:
- Deportes: {len(deportes)} sesión(es)
- Proyectos: {len(proyectos)} proyecto(s)
- Aprendizaje: {len(temas)} tema(s)
- Comidas especiales: {len([c for c in comidas if c.get('es_batch_cooking')])} batch cooking

Genera UNA recomendación principal para este día (máximo 2 frases, directo y específico):"""
        
        try:
            recomendacion = claude_client._generar_recomendacion_simple(contexto)
            return recomendacion
        except Exception as e:
            # Fallback a recomendación simple
            return f"Día {dia_nombre}: balance entre {len(deportes + proyectos + temas)} actividades"
    
    # Métodos auxiliares
    
    def _nombre_dia(self, dia: date) -> str:
        """Convierte date a nombre de día en español"""
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return dias[dia.weekday()]
    
    def _calcular_sesiones_deportivas_semana(self, dias_semana: List[EntrelazamientoDia]) -> int:
        """Cuenta sesiones deportivas totales de la semana"""
        total = sum(len(dia.deportes_hoy) for dia in dias_semana)
        return total
    
    def _planificar_batch_cooking_semana(self, dias_semana: List[EntrelazamientoDia]) -> List[dict]:
        """Identifica días de batch cooking"""
        batch_dias = []
        for dia in dias_semana:
            batch_comidas = [c for c in dia.comidas_hoy if c.get("es_batch_cooking")]
            if batch_comidas:
                batch_dias.append({
                    "dia": self._nombre_dia(dia.fecha),
                    "recetas": [c["receta_sugerida"] for c in batch_comidas],
                    "tiempo_total": sum(c["tiempo_cocinar"] for c in batch_comidas)
                })
        return batch_dias
    
    def _calcular_compra_semanal(self) -> List[dict]:
        """Calcula lista de compra semanal (simplificado)"""
        # Esto se puede mejorar con IA para analizar recetas
        return [
            {"ingrediente": "Proteínas", "cantidad": "7 porciones", "presupuesto": 50.0},
            {"ingrediente": "Verduras", "cantidad": "variadas", "presupuesto": 30.0},
            {"ingrediente": "Carbohidratos", "cantidad": "según recetas", "presupuesto": 20.0}
        ]
    
    def _calcular_gasto_proyectado(self) -> float:
        """Calcula gasto proyectado de la semana"""
        total = 0.0
        for categoria in self.perfil_usuario.presupuesto_mensual:
            # Estimar gasto semanal como 1/4 del mensual
            total += categoria.asignado_mensual / 4
        return total
    
    def _calcular_presupuesto_disponible(self) -> float:
        """Calcula presupuesto disponible total"""
        total = 0.0
        for categoria in self.perfil_usuario.presupuesto_mensual:
            disponible = categoria.asignado_mensual - categoria.gastado_mes_actual
            total += max(0, disponible)
        return total
    
    def _detectar_alertas_financieras(self) -> List[str]:
        """Detecta categorías con presupuesto bajo"""
        alertas = []
        for categoria in self.perfil_usuario.presupuesto_mensual:
            porcentaje_usado = (categoria.gastado_mes_actual / categoria.asignado_mensual) * 100
            if porcentaje_usado > 90:
                alertas.append(f"{categoria.nombre}: {porcentaje_usado:.0f}% usado")
        return alertas
    
    def _calcular_horas_aprendizaje(self) -> float:
        """Calcula horas semanales de aprendizaje planificadas"""
        total_minutos = sum(t.tiempo_semanal_deseado for t in self.perfil_usuario.temas_aprendizaje)
        return total_minutos / 60
    
    def _obtener_temas_prioridad(self) -> List[str]:
        """Obtiene temas de máxima prioridad"""
        temas_ordenados = sorted(
            self.perfil_usuario.temas_aprendizaje,
            key=lambda t: t.prioridad,
            reverse=True
        )
        return [t.nombre for t in temas_ordenados[:3]]
    
    def _calcular_horas_desarrollo(self) -> float:
        """Calcula horas semanales de desarrollo planificadas"""
        proyectos_activos = [p for p in self.perfil_usuario.proyectos_desarrollo if p.estado == "activo"]
        total_horas = sum(p.horas_semanales_deseadas for p in proyectos_activos)
        return total_horas
    
    def _calcular_avance_proyectos(self) -> List[dict]:
        """Calcula avance de proyectos activos"""
        avances = []
        for proyecto in self.perfil_usuario.proyectos_desarrollo:
            if proyecto.estado == "activo":
                avances.append({
                    "nombre": proyecto.nombre,
                    "hitos_completados": 0,  # Se puede mejorar con tracking real
                    "hitos_totales": len(proyecto.hitos),
                    "deadline": proyecto.deadline.isoformat() if proyecto.deadline else None
                })
        return avances
    
    def _obtener_decisiones_pendientes(self) -> List[dict]:
        """Obtiene decisiones de inversión pendientes"""
        decisiones = []
        hoy = date.today()
        for asunto in self.perfil_usuario.inversiones_asuntos:
            if asunto.tipo == "decisión_pendiente" or (
                asunto.fecha_decision and asunto.fecha_decision <= hoy + timedelta(days=7)
            ):
                decisiones.append({
                    "asunto": asunto.nombre,
                    "fecha_limite": asunto.fecha_decision.isoformat() if asunto.fecha_decision else None,
                    "monto": asunto.monto_involucrado,
                    "prioridad": asunto.prioridad
                })
        return decisiones
    
    def _analizar_patron_energia_semanal(self, dias: List[EntrelazamientoDia]) -> dict:
        """Analiza el patrón de energía a lo largo de la semana"""
        patron = {
            "lunes": 0, "martes": 0, "miércoles": 0, "jueves": 0,
            "viernes": 0, "sábado": 0, "domingo": 0
        }
        
        for dia in dias:
            nombre_dia = self._nombre_dia(dia.fecha)
            patron[nombre_dia] = dia.energia_requerida_total
        
        # Calcular promedio
        patron["promedio"] = sum(patron.values()) / 7
        
        # Identificar día más demandante
        dia_max = max(patron.items(), key=lambda x: x[1] if isinstance(x[1], (int, float)) else 0)
        patron["dia_pico"] = dia_max[0]
        
        return patron
    
    def _generar_sugerencias_optimizacion(self, dias: List[EntrelazamientoDia], patron_energia: dict) -> List[str]:
        """Genera sugerencias para optimizar la semana"""
        sugerencias = []
        
        # Sugerencia: Distribución de energía
        if patron_energia.get("promedio", 0) > 7:
            sugerencias.append("🔄 Semana muy demandante - considera mover actividades no urgentes")
        
        # Sugerencia: Días sobrecargados
        dias_sobrecargados = [d for d in dias if d.energia_requerida_total > 8]
        if len(dias_sobrecargados) >= 3:
            sugerencias.append(f"⚡ {len(dias_sobrecargados)} días sobrecargados - redistribuye carga")
        
        # Sugerencia: Balance
        dias_con_deportes = [d for d in dias if len(d.deportes_hoy) > 0]
        if len(dias_con_deportes) < 3:
            sugerencias.append("💪 Considera agregar más días de ejercicio para balance")
        
        # Sugerencia: Conflictos
        total_conflictos = sum(len(d.conflictos_detectados) for d in dias)
        if total_conflictos > 5:
            sugerencias.append(f"⚠️ {total_conflictos} conflictos detectados - revisa planificación")
        
        return sugerencias
    
    def _identificar_espacios_emergencia(self, dias: List[EntrelazamientoDia]) -> List[dict]:
        """Identifica espacios libres para emergencia (40% regla)"""
        espacios = []
        
        for dia in dias:
            # Si el día tiene baja demanda de energía, es buen espacio para emergencia
            if dia.energia_requerida_total < 5:
                espacios.append({
                    "dia": self._nombre_dia(dia.fecha),
                    "fecha": dia.fecha.isoformat(),
                    "energia_disponible": 10 - dia.energia_requerida_total,
                    "razon": "Día de baja demanda - ideal para emergencia"
                })
        
        return espacios


# Instancia global del agente
agente_entrelazador = AgenteEntrelazador()



