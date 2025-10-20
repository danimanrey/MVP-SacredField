#!/usr/bin/env python3
"""
🕌 Campo Sagrado - Asistente Interactivo de Personalización de Perfil
====================================================================

Este script te guía para crear tu perfil personal paso a paso
"""

import sys
import json
from datetime import datetime, date, timedelta

# Agregar path del backend
sys.path.insert(0, '..')

from models.schemas import (
    PerfilPersonal,
    RutinaDeportiva,
    ComidaConfiguracion,
    PresupuestoCategoria,
    TemaAprendizaje,
    ProyectoDesarrollo,
    InversionAsunto
)


def preguntar(pregunta, default=None):
    """Hace una pregunta al usuario"""
    if default:
        respuesta = input(f"{pregunta} [{default}]: ").strip()
        return respuesta if respuesta else default
    else:
        respuesta = input(f"{pregunta}: ").strip()
        return respuesta


def preguntar_si_no(pregunta, default="s"):
    """Pregunta sí/no"""
    respuesta = preguntar(pregunta, default).lower()
    return respuesta in ['s', 'si', 'sí', 'y', 'yes']


def preguntar_numero(pregunta, default=None, minimo=None, maximo=None):
    """Pregunta que espera un número"""
    while True:
        try:
            respuesta = preguntar(pregunta, str(default) if default else None)
            numero = int(respuesta) if respuesta else default
            
            if minimo is not None and numero < minimo:
                print(f"❌ El valor debe ser mayor o igual a {minimo}")
                continue
            if maximo is not None and numero > maximo:
                print(f"❌ El valor debe ser menor o igual a {maximo}")
                continue
                
            return numero
        except ValueError:
            print("❌ Por favor ingresa un número válido")


def preguntar_float(pregunta, default=None):
    """Pregunta que espera un número decimal"""
    while True:
        try:
            respuesta = preguntar(pregunta, str(default) if default else None)
            return float(respuesta) if respuesta else default
        except ValueError:
            print("❌ Por favor ingresa un número válido")


def preguntar_lista(pregunta, opciones, multiple=False):
    """Pregunta con opciones"""
    print(f"\n{pregunta}")
    for i, opcion in enumerate(opciones, 1):
        print(f"  {i}. {opcion}")
    
    if multiple:
        respuesta = preguntar("Selecciona opciones (separadas por coma)")
        indices = [int(x.strip()) - 1 for x in respuesta.split(',') if x.strip()]
        return [opciones[i] for i in indices if 0 <= i < len(opciones)]
    else:
        while True:
            try:
                respuesta = int(preguntar("Selecciona opción"))
                if 1 <= respuesta <= len(opciones):
                    return opciones[respuesta - 1]
                print(f"❌ Opción debe estar entre 1 y {len(opciones)}")
            except ValueError:
                print("❌ Por favor ingresa un número válido")


def crear_perfil_interactivo():
    """Crea el perfil de forma interactiva"""
    
    print("🕌 CAMPO SAGRADO - PERSONALIZACIÓN DE PERFIL")
    print("=" * 60)
    print("\nVamos a crear tu perfil personal paso a paso.")
    print("Puedes dejar campos en blanco para usar valores por defecto.\n")
    
    # Información básica
    print("\n📋 INFORMACIÓN BÁSICA")
    print("-" * 60)
    nombre = preguntar("¿Cómo te llamas?", "Usuario Campo Sagrado")
    timezone = preguntar("¿Tu zona horaria?", "Europe/Madrid")
    
    # Rutinas deportivas
    print("\n💪 RUTINAS DEPORTIVAS")
    print("-" * 60)
    rutinas = []
    agregar_deportes = preguntar_si_no("¿Quieres agregar rutinas deportivas?")
    
    while agregar_deportes:
        print("\n📝 Nueva rutina deportiva:")
        nombre_rutina = preguntar("Nombre de la rutina", "Entrenamiento")
        
        print("\nDías de la semana (separados por coma):")
        print("Ejemplo: lunes, miércoles, viernes")
        dias_input = preguntar("Días", "lunes,miércoles,viernes")
        dias_semana = [d.strip().lower() for d in dias_input.split(',')]
        
        hora = preguntar("Hora preferida (HH:MM)", "07:00")
        duracion = preguntar_numero("Duración en minutos", 60, minimo=15)
        
        tipo = preguntar_lista(
            "Tipo de rutina:",
            ["fuerza", "cardio", "movilidad", "yoga", "otro"]
        )
        
        intensidad = preguntar_numero("Intensidad (1-5)", 3, minimo=1, maximo=5)
        notas = preguntar("Notas adicionales (opcional)", "")
        
        rutinas.append(RutinaDeportiva(
            nombre=nombre_rutina,
            dias_semana=dias_semana,
            hora_preferida=hora,
            duracion_minutos=duracion,
            tipo=tipo,
            intensidad=intensidad,
            notas=notas
        ))
        
        agregar_deportes = preguntar_si_no("¿Agregar otra rutina?", "n")
    
    # Sistema de comidas
    print("\n🍽️  SISTEMA DE COMIDAS")
    print("-" * 60)
    comidas = []
    tipos_comida = ["desayuno", "almuerzo", "cena"]
    
    for tipo in tipos_comida:
        if preguntar_si_no(f"¿Quieres configurar {tipo}?"):
            print(f"\n📝 Configuración de {tipo}:")
            
            hora = preguntar(f"Hora aproximada", 
                           "08:30" if tipo == "desayuno" else "14:00" if tipo == "almuerzo" else "20:30")
            
            duracion = preguntar_numero("Tiempo de preparación (minutos)", 
                                      15 if tipo == "desayuno" else 30)
            
            print("\nRecetas preferidas (separadas por coma):")
            recetas_input = preguntar("Recetas", f"Receta {tipo} 1, Receta {tipo} 2")
            recetas = [r.strip() for r in recetas_input.split(',')]
            
            batch = preguntar_si_no(f"¿Haces batch cooking para {tipo}?", "n")
            dias_batch = None
            if batch:
                dias_input = preguntar("¿Qué días? (separados por coma)", "domingo")
                dias_batch = [d.strip().lower() for d in dias_input.split(',')]
            
            comidas.append(ComidaConfiguracion(
                tipo=tipo,
                hora_aproximada=hora,
                duracion_preparacion=duracion,
                recetas_preferidas=recetas,
                restricciones=[],
                batch_cooking=batch,
                dias_batch=dias_batch
            ))
    
    # Presupuesto
    print("\n💰 GESTIÓN FINANCIERA")
    print("-" * 60)
    presupuesto = []
    
    categorias_default = [
        ("Alimentación", 400.0),
        ("Transporte", 100.0),
        ("Desarrollo Profesional", 200.0),
        ("Ocio y Cultura", 150.0),
        ("Emergencias", 300.0)
    ]
    
    if preguntar_si_no("¿Quieres configurar tu presupuesto mensual?"):
        for nombre_cat, monto_default in categorias_default:
            if preguntar_si_no(f"  ¿Incluir categoría '{nombre_cat}'?"):
                monto = preguntar_float(f"    Monto mensual", monto_default)
                gastado = preguntar_float(f"    Gastado este mes", 0.0)
                prioridad = preguntar_numero(f"    Prioridad (1-5)", 3, minimo=1, maximo=5)
                
                presupuesto.append(PresupuestoCategoria(
                    nombre=nombre_cat,
                    asignado_mensual=monto,
                    gastado_mes_actual=gastado,
                    prioridad=prioridad
                ))
        
        # Categorías personalizadas
        if preguntar_si_no("¿Agregar categorías personalizadas?", "n"):
            while True:
                nombre_cat = preguntar("Nombre de categoría")
                monto = preguntar_float("Monto mensual")
                gastado = preguntar_float("Gastado este mes", 0.0)
                prioridad = preguntar_numero("Prioridad (1-5)", 3, minimo=1, maximo=5)
                
                presupuesto.append(PresupuestoCategoria(
                    nombre=nombre_cat,
                    asignado_mensual=monto,
                    gastado_mes_actual=gastado,
                    prioridad=prioridad
                ))
                
                if not preguntar_si_no("¿Agregar otra categoría?", "n"):
                    break
    
    dia_compra = None
    if preguntar_si_no("¿Tienes un día fijo para hacer compras?", "s"):
        dia_compra = preguntar_lista(
            "¿Qué día?",
            ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        )
    
    # Temas de aprendizaje
    print("\n📚 TEMAS DE APRENDIZAJE")
    print("-" * 60)
    temas = []
    
    if preguntar_si_no("¿Tienes temas de aprendizaje activos?"):
        while True:
            print("\n📝 Nuevo tema de aprendizaje:")
            nombre_tema = preguntar("Nombre del tema")
            dominio = preguntar_lista(
                "Dominio:",
                ["tecnología", "filosofía", "arte", "idiomas", "ciencia", "negocios", "otro"]
            )
            prioridad = preguntar_numero("Prioridad (1-5)", 3, minimo=1, maximo=5)
            tiempo_semanal = preguntar_numero("Tiempo semanal deseado (minutos)", 180)
            
            print("\nRecursos (separados por coma):")
            recursos_input = preguntar("Recursos", "Libro 1, Curso online")
            recursos = [r.strip() for r in recursos_input.split(',')]
            
            temas.append(TemaAprendizaje(
                nombre=nombre_tema,
                dominio=dominio,
                prioridad=prioridad,
                tiempo_semanal_deseado=tiempo_semanal,
                recursos=recursos,
                progreso_porcentaje=0.0,
                fecha_inicio=date.today()
            ))
            
            if not preguntar_si_no("¿Agregar otro tema?", "n"):
                break
    
    # Proyectos de desarrollo
    print("\n💻 PROYECTOS DE DESARROLLO")
    print("-" * 60)
    proyectos = []
    
    if preguntar_si_no("¿Tienes proyectos de desarrollo activos?"):
        while True:
            print("\n📝 Nuevo proyecto:")
            nombre_proyecto = preguntar("Nombre del proyecto")
            tipo = preguntar_lista(
                "Tipo:",
                ["código", "escritura", "diseño", "investigación", "otro"]
            )
            estado = preguntar_lista(
                "Estado:",
                ["activo", "pausado", "completado"]
            )
            prioridad = preguntar_numero("Prioridad (1-5)", 3, minimo=1, maximo=5)
            horas_semanales = preguntar_numero("Horas semanales deseadas", 10)
            
            tiene_deadline = preguntar_si_no("¿Tiene deadline?", "n")
            deadline = None
            if tiene_deadline:
                dias_hasta = preguntar_numero("¿En cuántos días?", 30)
                deadline = date.today() + timedelta(days=dias_hasta)
            
            print("\nHitos (separados por coma):")
            hitos_input = preguntar("Hitos", "Hito 1, Hito 2, Hito 3")
            hitos = [h.strip() for h in hitos_input.split(',')]
            
            proyectos.append(ProyectoDesarrollo(
                nombre=nombre_proyecto,
                tipo=tipo,
                estado=estado,
                prioridad=prioridad,
                horas_semanales_deseadas=horas_semanales,
                deadline=deadline,
                hitos=hitos
            ))
            
            if not preguntar_si_no("¿Agregar otro proyecto?", "n"):
                break
    
    # Inversiones y asuntos
    print("\n📈 INVERSIONES Y ASUNTOS FINANCIEROS")
    print("-" * 60)
    inversiones = []
    
    if preguntar_si_no("¿Tienes decisiones o asuntos financieros pendientes?", "n"):
        while True:
            print("\n📝 Nuevo asunto:")
            nombre_asunto = preguntar("Nombre del asunto")
            tipo = preguntar_lista(
                "Tipo:",
                ["decisión_pendiente", "investigación", "seguimiento"]
            )
            
            tiene_monto = preguntar_si_no("¿Involucra un monto específico?", "n")
            monto = preguntar_float("Monto", 0.0) if tiene_monto else None
            
            tiene_fecha = preguntar_si_no("¿Tiene fecha de decisión?", "n")
            fecha_decision = None
            if tiene_fecha:
                dias_hasta = preguntar_numero("¿En cuántos días?", 7)
                fecha_decision = date.today() + timedelta(days=dias_hasta)
            
            prioridad = preguntar_numero("Prioridad (1-5)", 3, minimo=1, maximo=5)
            
            inversiones.append(InversionAsunto(
                nombre=nombre_asunto,
                tipo=tipo,
                monto_involucrado=monto,
                fecha_decision=fecha_decision,
                prioridad=prioridad
            ))
            
            if not preguntar_si_no("¿Agregar otro asunto?", "n"):
                break
    
    # Preferencias
    print("\n⚙️  PREFERENCIAS")
    print("-" * 60)
    energia_pico_manana = preguntar_si_no("¿Tu pico de energía es por la mañana?")
    prefiere_batch = preguntar_si_no("¿Prefieres batch cooking?", "n")
    
    # Crear perfil
    perfil = PerfilPersonal(
        nombre=nombre,
        timezone=timezone,
        rutinas_deportivas=rutinas,
        sistema_comidas=comidas,
        presupuesto_mensual=presupuesto,
        dia_compra_semanal=dia_compra,
        temas_aprendizaje=temas,
        proyectos_desarrollo=proyectos,
        inversiones_asuntos=inversiones,
        sistemas_documentacion=["obsidian"],
        energia_pico_manana=energia_pico_manana,
        prefiere_batch_cooking=prefiere_batch,
        creado=datetime.now(),
        actualizado=datetime.now()
    )
    
    return perfil


def main():
    print("\n")
    print("=" * 60)
    
    perfil = crear_perfil_interactivo()
    
    # Resumen
    print("\n\n✅ PERFIL CREADO EXITOSAMENTE")
    print("=" * 60)
    print(f"👤 Usuario: {perfil.nombre}")
    print(f"💪 Rutinas deportivas: {len(perfil.rutinas_deportivas)}")
    print(f"🍽️  Comidas configuradas: {len(perfil.sistema_comidas)}")
    print(f"💰 Categorías presupuesto: {len(perfil.presupuesto_mensual)}")
    print(f"📚 Temas aprendizaje: {len(perfil.temas_aprendizaje)}")
    print(f"💻 Proyectos desarrollo: {len(perfil.proyectos_desarrollo)}")
    print(f"📈 Asuntos inversión: {len(perfil.inversiones_asuntos)}")
    
    # Guardar
    filename = "mi_perfil_personal.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(perfil.model_dump(), f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Perfil guardado en: {filename}")
    
    # Instrucciones
    print("\n📤 SIGUIENTE PASO: Carga tu perfil en el sistema")
    print("-" * 60)
    print("Ejecuta este comando:")
    print(f"\ncurl -X POST http://localhost:8000/api/entrelazamiento/perfil \\")
    print(f"  -H 'Content-Type: application/json' \\")
    print(f"  -d @{filename}")
    print()
    print("Luego consulta tu dashboard:")
    print("curl http://localhost:8000/api/entrelazamiento/resumen-semana | python -m json.tool")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

