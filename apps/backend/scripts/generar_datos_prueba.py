#!/usr/bin/env python3
"""
Script para generar datos de prueba realistas para el MVP Campo Sagrado
"""

import sys
import os
from datetime import datetime, date, timedelta
import json
import random

# Agregar el path del backend
sys.path.append('/Users/hp/Campo sagrado MVP/backend')

from models.database import get_db, init_db
from models.schemas import MomentoLiturgico
from services.tiempos_liturgicos import CalculadorTiemposLiturgicos
from services.calendario_hijri import CalendarioHijri
from services.claude_client import ClaudeClient
from services.contexto import RecopiladorContexto
from integraciones.obsidian import ObsidianVault

# Configuración
LAT = 40.4168
LON = -3.7038
TZ = "Europe/Madrid"

def generar_estado_cero_realista(db, fecha: date, momento: MomentoLiturgico):
    """Genera un Estado Cero realista para una fecha y momento específico"""
    
    calculador = CalculadorTiemposLiturgicos(LAT, LON, TZ)
    calendario = CalendarioHijri()
    claude = ClaudeClient()
    recopilador = RecopiladorContexto(db, calculador, calendario)
    
    # Contexto realista
    contexto = {
        "temporal": {
            "momento_liturgico": momento.value,
            "dia_semana": fecha.strftime("%A"),
            "mes_hijri": "Shawwal",
            "cualidad_momento": "Reflexión",
            "cualidad_mes": "Celebrar"
        },
        "biologico": {
            "energia_actual": random.randint(2, 5),
            "hrv": None,
            "luz_solar_hoy": random.choice([True, False]),
            "ejercicio_hoy": random.choice([True, False])
        },
        "financiero": {
            "runway_meses": round(random.uniform(3.0, 12.0), 1),
            "urgencia_financiera": random.choice([True, False]),
            "proyectos_activos": ["MVP Campo Sagrado", "Consultoría", "Desarrollo Personal"]
        },
        "conocimiento": {
            "capturas_sin_procesar": random.randint(0, 15),
            "insights_listos": random.randint(0, 8)
        },
        "tiempo_disponible_hoy": random.randint(60, 240)
    }
    
    # Preguntas binarias realistas
    preguntas = [
        {
            "pregunta": "¿Te expandes al enfocarte en la acción principal hoy?",
            "contexto": "Acción prioritaria del día",
            "categoria": "desarrollo"
        },
        {
            "pregunta": "¿Se siente vivo revisar finanzas 30 min ahora?",
            "contexto": "Runway y foco",
            "categoria": "finanzas"
        },
        {
            "pregunta": "¿Tu cuerpo pide movimiento ligero 20 min ahora?",
            "contexto": "Energía y ritmo",
            "categoria": "biologia"
        },
        {
            "pregunta": "¿Hay expansión en procesar capturas hoy?",
            "contexto": "Metabolizar conocimiento",
            "categoria": "conocimiento"
        },
        {
            "pregunta": "¿Se siente claro un bloque profundo 90 min?",
            "contexto": "Ritmo de trabajo",
            "categoria": "desarrollo"
        },
        {
            "pregunta": "¿Te expande preparar una comida nutritiva ahora?",
            "contexto": "Biología de soporte",
            "categoria": "biologia"
        }
    ]
    
    # Respuestas realistas (algunas sí, algunas no)
    respuestas = [
        {"pregunta_id": i, "respuesta": random.choice([True, False]), "sensacion": random.choice(["expansión", "contracción", "neutral"])}
        for i in range(len(preguntas))
    ]
    
    # Dirección emergente
    direcciones = [
        "Enfoque en desarrollo técnico del MVP",
        "Priorizar bienestar biológico y descanso",
        "Acelerar aspectos financieros del proyecto",
        "Profundizar en metabolización de conocimiento",
        "Balance entre todos los dominios"
    ]
    
    direccion_emergente = random.choice(direcciones)
    
    # Acción tangible
    acciones = [
        {
            "titulo": "Implementar funcionalidad de Estado Cero",
            "descripcion": "Desarrollar 2 horas el flujo completo de Estado Cero en el frontend",
            "tiempo_estimado": "2h",
            "energia_requerida": 4,
            "deadline": (datetime.now() + timedelta(days=1)).isoformat()
        },
        {
            "titulo": "Revisión financiera semanal",
            "descripcion": "30 minutos revisando presupuesto y runway del proyecto",
            "tiempo_estimado": "30min",
            "energia_requerida": 2,
            "deadline": (datetime.now() + timedelta(hours=6)).isoformat()
        },
        {
            "titulo": "Paseo regenerativo",
            "descripcion": "20 minutos caminando al aire libre para reset biológico",
            "tiempo_estimado": "20min",
            "energia_requerida": 1,
            "deadline": (datetime.now() + timedelta(hours=2)).isoformat()
        }
    ]
    
    accion_tangible = random.choice(acciones)
    
    # Chat de clarificación
    chat_clarificacion = [
        {
            "usuario": "¿Qué significa exactamente 'acción principal'?",
            "asistente": "La acción principal es aquella que más te acerca a tu propósito del día. En este contexto, parece ser continuar con el desarrollo del MVP Campo Sagrado."
        },
        {
            "usuario": "¿Por qué es importante el movimiento ahora?",
            "asistente": "Tu cuerpo ha estado en modo sedentario durante las últimas horas. El movimiento ligero ayuda a resetear el sistema nervioso y mejora la concentración."
        }
    ]
    
    return {
        "fecha": fecha.isoformat(),
        "momento": momento.value,
        "contexto": contexto,
        "preguntas": preguntas,
        "respuestas": respuestas,
        "direccion_emergente": direccion_emergente,
        "accion_tangible": accion_tangible,
        "chat_clarificacion": chat_clarificacion,
        "completado": True
    }

def generar_sesiones_trabajo(db, fecha: date):
    """Genera sesiones de trabajo realistas para un día"""
    
    sesiones = []
    momentos = [MomentoLiturgico.FAJR, MomentoLiturgico.DHUHR, MomentoLiturgico.ASR, MomentoLiturgico.MAGHRIB]
    
    for momento in momentos:
        if random.random() > 0.3:  # 70% probabilidad de tener sesión
            sesion = {
                "fecha": fecha.isoformat(),
                "momento": momento.value,
                "actividad": random.choice([
                    "Desarrollo MVP",
                    "Revisión financiera",
                    "Ejercicio físico",
                    "Procesamiento capturas",
                    "Descanso regenerativo"
                ]),
                "duracion_minutos": random.randint(30, 180),
                "energia_inicial": random.randint(2, 5),
                "energia_final": random.randint(1, 5),
                "satisfaccion": random.randint(3, 5),
                "completada": random.choice([True, False])
            }
            sesiones.append(sesion)
    
    return sesiones

def generar_no_negociables_tracking(db, fecha: date):
    """Genera tracking de no-negociables para un día"""
    
    no_negociables = [
        {
            "fecha": fecha.isoformat(),
            "tipo": "biologico",
            "nombre": "Ejercicio físico",
            "completado": random.choice([True, False]),
            "hora": f"{random.randint(6, 20):02d}:{random.randint(0, 59):02d}",
            "notas": "Caminata de 30 minutos en el parque"
        },
        {
            "fecha": fecha.isoformat(),
            "tipo": "espiritual",
            "nombre": "Meditación",
            "completado": random.choice([True, False]),
            "hora": f"{random.randint(6, 8):02d}:{random.randint(0, 59):02d}",
            "notas": "10 minutos de respiración consciente"
        },
        {
            "fecha": fecha.isoformat(),
            "tipo": "financiero",
            "nombre": "Revisión presupuesto",
            "completado": random.choice([True, False]),
            "hora": f"{random.randint(9, 17):02d}:{random.randint(0, 59):02d}",
            "notas": "Verificación de gastos del día"
        }
    ]
    
    return no_negociables

def main():
    """Función principal para generar datos de prueba"""
    
    print("🔄 Generando datos de prueba para Campo Sagrado MVP...")
    
    # Inicializar base de datos
    init_db()
    
    # Conectar a la base de datos
    db = next(get_db())
    
    # Generar datos para los últimos 7 días
    hoy = date.today()
    fechas = [hoy - timedelta(days=i) for i in range(7)]
    
    estados_cero = []
    sesiones = []
    no_negociables = []
    
    for fecha in fechas:
        print(f"📅 Generando datos para {fecha}")
        
        # Estados Cero (1-2 por día)
        num_estados = random.randint(1, 2)
        momentos_usados = random.sample(list(MomentoLiturgico), num_estados)
        
        for momento in momentos_usados:
            estado = generar_estado_cero_realista(db, fecha, momento)
            estados_cero.append(estado)
        
        # Sesiones de trabajo
        sesiones_dia = generar_sesiones_trabajo(db, fecha)
        sesiones.extend(sesiones_dia)
        
        # No-negociables
        no_negociables_dia = generar_no_negociables_tracking(db, fecha)
        no_negociables.extend(no_negociables_dia)
    
    # Guardar en archivo JSON para revisión
    datos = {
        "estados_cero": estados_cero,
        "sesiones": sesiones,
        "no_negociables": no_negociables,
        "generado_en": datetime.now().isoformat()
    }
    
    with open('/Users/hp/Campo sagrado MVP/storage/datos_prueba.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Datos generados:")
    print(f"  - {len(estados_cero)} Estados Cero")
    print(f"  - {len(sesiones)} Sesiones de trabajo")
    print(f"  - {len(no_negociables)} No-negociables")
    print(f"📄 Guardado en: /Users/hp/Campo sagrado MVP/storage/datos_prueba.json")
    
    # Crear documento de prueba en Obsidian
    vault = ObsidianVault("~/Documents/CampoSagrado")
    
    contenido_obsidian = f"""# 📊 Datos de Prueba Generados

**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Resumen de Datos Generados

### Estados Cero: {len(estados_cero)}
- Generados para los últimos 7 días
- Cada uno con contexto completo, preguntas binarias, respuestas y acciones tangibles

### Sesiones de Trabajo: {len(sesiones)}
- Actividades variadas: desarrollo, finanzas, ejercicio, procesamiento
- Tracking de energía y satisfacción

### No-Negociables: {len(no_negociables)}
- Biológicos: ejercicio, descanso
- Espirituales: meditación, reflexión
- Financieros: presupuesto, tracking

## Próximos Pasos

1. ✅ Revisar datos generados en `storage/datos_prueba.json`
2. 🔄 Importar a la base de datos SQLite
3. 🎨 Probar visualizaciones en el frontend
4. 📈 Verificar métricas y reportes

---
*Generado automáticamente por el MVP Campo Sagrado*
"""
    
    filepath = vault.guardar_documento('40-Journal/datos-prueba-generados.md', contenido_obsidian)
    print(f"📝 Documento creado en Obsidian: {filepath}")

if __name__ == "__main__":
    main()
