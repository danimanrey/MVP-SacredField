"""
🕌 Campo Sagrado - Script para crear perfil de ejemplo
======================================================

Este script crea un perfil personal completo de ejemplo
para probar el Dashboard de Entrelazamiento
"""

import sys
sys.path.append('..')

from datetime import datetime, date, timedelta
from models.schemas import (
    PerfilPersonal,
    RutinaDeportiva,
    ComidaConfiguracion,
    PresupuestoCategoria,
    TemaAprendizaje,
    ProyectoDesarrollo,
    InversionAsunto
)
import json


def crear_perfil_ejemplo() -> PerfilPersonal:
    """
    Crea un perfil de ejemplo realista
    """
    
    # Rutinas deportivas
    rutinas = [
        RutinaDeportiva(
            nombre="Entrenamiento de Fuerza",
            dias_semana=["lunes", "miércoles", "viernes"],
            hora_preferida="07:00",
            duracion_minutos=60,
            tipo="fuerza",
            intensidad=4,
            notas="Gimnasio - enfoque en compuestos"
        ),
        RutinaDeportiva(
            nombre="Yoga/Movilidad",
            dias_semana=["martes", "jueves"],
            hora_preferida="07:30",
            duracion_minutos=45,
            tipo="movilidad",
            intensidad=2,
            notas="Sesión suave para recuperación"
        ),
        RutinaDeportiva(
            nombre="Caminata Larga",
            dias_semana=["domingo"],
            hora_preferida="10:00",
            duracion_minutos=90,
            tipo="cardio",
            intensidad=2,
            notas="Naturaleza - desconexión digital"
        )
    ]
    
    # Sistema de comidas
    comidas = [
        ComidaConfiguracion(
            tipo="desayuno",
            hora_aproximada="08:30",
            duracion_preparacion=15,
            recetas_preferidas=["Avena con frutos secos", "Huevos revueltos con aguacate"],
            restricciones=[],
            batch_cooking=False
        ),
        ComidaConfiguracion(
            tipo="almuerzo",
            hora_aproximada="14:00",
            duracion_preparacion=30,
            recetas_preferidas=[
                "Bowl de pollo con verduras asadas",
                "Salmón con quinoa y brócoli",
                "Curry de lentejas con arroz"
            ],
            restricciones=[],
            batch_cooking=True,
            dias_batch=["domingo", "miércoles"]
        ),
        ComidaConfiguracion(
            tipo="cena",
            hora_aproximada="20:30",
            duracion_preparacion=25,
            recetas_preferidas=[
                "Ensalada completa con proteína",
                "Sopa de verduras con pan integral",
                "Tortilla francesa con ensalada"
            ],
            restricciones=["evitar carbohidratos pesados"],
            batch_cooking=False
        )
    ]
    
    # Presupuesto mensual
    presupuesto = [
        PresupuestoCategoria(
            nombre="Alimentación",
            asignado_mensual=400.0,
            gastado_mes_actual=280.0,
            prioridad=5,
            notas="Incluye compra semanal y ocasionales"
        ),
        PresupuestoCategoria(
            nombre="Gimnasio",
            asignado_mensual=50.0,
            gastado_mes_actual=50.0,
            prioridad=4,
            notas="Cuota mensual fija"
        ),
        PresupuestoCategoria(
            nombre="Desarrollo Profesional",
            asignado_mensual=200.0,
            gastado_mes_actual=85.0,
            prioridad=5,
            notas="Cursos, libros, herramientas"
        ),
        PresupuestoCategoria(
            nombre="Ocio y Cultura",
            asignado_mensual=150.0,
            gastado_mes_actual=120.0,
            prioridad=3,
            notas="Cine, música, eventos"
        ),
        PresupuestoCategoria(
            nombre="Transporte",
            asignado_mensual=100.0,
            gastado_mes_actual=75.0,
            prioridad=4,
            notas="Transporte público y ocasional"
        ),
        PresupuestoCategoria(
            nombre="Emergencias",
            asignado_mensual=300.0,
            gastado_mes_actual=0.0,
            prioridad=5,
            notas="Fondo de emergencia mensual"
        )
    ]
    
    # Temas de aprendizaje
    temas = [
        TemaAprendizaje(
            nombre="Machine Learning Avanzado",
            dominio="tecnología",
            prioridad=5,
            tiempo_semanal_deseado=420,  # 7 horas
            recursos=[
                "Fast.ai Course",
                "Papers on arXiv",
                "Implementaciones propias"
            ],
            progreso_porcentaje=35.0,
            fecha_inicio=date(2025, 9, 1),
            fecha_objetivo=date(2026, 3, 1)
        ),
        TemaAprendizaje(
            nombre="Filosofía Estoica",
            dominio="filosofía",
            prioridad=4,
            tiempo_semanal_deseado=180,  # 3 horas
            recursos=[
                "Meditaciones de Marco Aurelio",
                "Cartas de Séneca",
                "The Daily Stoic"
            ],
            progreso_porcentaje=60.0,
            fecha_inicio=date(2025, 7, 1)
        ),
        TemaAprendizaje(
            nombre="Diseño de Sistemas Distribuidos",
            dominio="tecnología",
            prioridad=4,
            tiempo_semanal_deseado=300,  # 5 horas
            recursos=[
                "Designing Data-Intensive Applications",
                "System Design Interviews",
                "Blogs de ingeniería"
            ],
            progreso_porcentaje=20.0,
            fecha_inicio=date(2025, 10, 1),
            fecha_objetivo=date(2026, 4, 1)
        ),
        TemaAprendizaje(
            nombre="Árabe Moderno Estándar",
            dominio="idiomas",
            prioridad=3,
            tiempo_semanal_deseado=240,  # 4 horas
            recursos=[
                "Duolingo",
                "Al-Kitaab",
                "Conversación con nativos"
            ],
            progreso_porcentaje=15.0,
            fecha_inicio=date(2025, 9, 15)
        )
    ]
    
    # Proyectos de desarrollo
    proyectos = [
        ProyectoDesarrollo(
            nombre="Campo Sagrado MVP",
            tipo="código",
            estado="activo",
            prioridad=5,
            horas_semanales_deseadas=15,
            deadline=date(2025, 11, 1),
            hitos=[
                "Dashboard de entrelazamiento completo",
                "Integración Estado Cero con perfil personal",
                "Frontend con visualizaciones",
                "Sistema de recomendaciones personalizado"
            ],
            notas="Proyecto principal - organismo tecnológico-espiritual"
        ),
        ProyectoDesarrollo(
            nombre="Artículos Técnicos Blog",
            tipo="escritura",
            estado="activo",
            prioridad=3,
            horas_semanales_deseadas=5,
            hitos=[
                "Artículo sobre sistemas adaptativos",
                "Artículo sobre autoridad sacral en IA",
                "Artículo sobre diseño al borde del caos"
            ],
            notas="2 artículos por mes"
        ),
        ProyectoDesarrollo(
            nombre="Portfolio Personal",
            tipo="diseño",
            estado="pausado",
            prioridad=2,
            horas_semanales_deseadas=3,
            deadline=date(2026, 1, 1),
            hitos=[
                "Diseño visual",
                "Implementación SvelteKit",
                "Deploy"
            ],
            notas="En pausa hasta terminar Campo Sagrado"
        ),
        ProyectoDesarrollo(
            nombre="Investigación: LLMs y Autoridad Sacral",
            tipo="investigación",
            estado="activo",
            prioridad=4,
            horas_semanales_deseadas=8,
            deadline=date(2026, 2, 1),
            hitos=[
                "Literatura review",
                "Experimentos iniciales",
                "Paper draft",
                "Presentación"
            ],
            notas="Potencial publicación académica"
        )
    ]
    
    # Inversiones y asuntos financieros
    inversiones = [
        InversionAsunto(
            nombre="Renovar servidor cloud",
            tipo="decisión_pendiente",
            monto_involucrado=300.0,
            fecha_decision=date.today() + timedelta(days=5),
            prioridad=4,
            notas="Evaluar opciones: AWS vs DigitalOcean vs Hetzner"
        ),
        InversionAsunto(
            nombre="Inversión en formación ML",
            tipo="investigación",
            monto_involucrado=1200.0,
            fecha_decision=date.today() + timedelta(days=15),
            prioridad=3,
            notas="Evaluar: Fast.ai Pro vs Coursera ML Specialization"
        ),
        InversionAsunto(
            nombre="Upgrade equipo desarrollo",
            tipo="seguimiento",
            monto_involucrado=2500.0,
            fecha_decision=date.today() + timedelta(days=60),
            prioridad=3,
            notas="Monitorear ofertas en M3 MacBook"
        )
    ]
    
    # Crear perfil completo
    perfil = PerfilPersonal(
        nombre="Usuario Campo Sagrado",
        timezone="Europe/Madrid",
        rutinas_deportivas=rutinas,
        sistema_comidas=comidas,
        presupuesto_mensual=presupuesto,
        dia_compra_semanal="sábado",
        temas_aprendizaje=temas,
        proyectos_desarrollo=proyectos,
        inversiones_asuntos=inversiones,
        sistemas_documentacion=["obsidian", "anytype"],
        energia_pico_manana=True,
        prefiere_batch_cooking=True,
        creado=datetime.now(),
        actualizado=datetime.now()
    )
    
    return perfil


def guardar_perfil_json(perfil: PerfilPersonal, filename: str = "perfil_ejemplo.json"):
    """Guarda el perfil como JSON para referencia"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(perfil.model_dump(), f, indent=2, ensure_ascii=False, default=str)
    print(f"✅ Perfil guardado en {filename}")


if __name__ == "__main__":
    print("🕌 Creando perfil de ejemplo...")
    perfil = crear_perfil_ejemplo()
    
    print(f"\n📊 Perfil creado para: {perfil.nombre}")
    print(f"   Rutinas deportivas: {len(perfil.rutinas_deportivas)}")
    print(f"   Comidas configuradas: {len(perfil.sistema_comidas)}")
    print(f"   Categorías presupuesto: {len(perfil.presupuesto_mensual)}")
    print(f"   Temas aprendizaje: {len(perfil.temas_aprendizaje)}")
    print(f"   Proyectos desarrollo: {len(perfil.proyectos_desarrollo)}")
    print(f"   Asuntos inversión: {len(perfil.inversiones_asuntos)}")
    
    # Guardar como JSON
    guardar_perfil_json(perfil)
    
    print("\n🚀 Listo para probar con:")
    print("   POST /api/entrelazamiento/perfil")
    print("   GET  /api/entrelazamiento/dashboard-semanal")


