#!/usr/bin/env python3
"""
🔮 Configuración del Prisma Personal
====================================

Script interactivo para configurar tu prisma único.
Usa preguntas SACRALES (no mentales) para extraer tu configuración.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.prisma_personal import (
    PrismaPersonal, DiseñoHumano, PerfilPsicologico,
    TipoHumanDesign, AutoridadInterna, EstrategiaVital,
    TipoMBTI, TipoEneagrama, Manifestacion,
    EstructuraConocimiento, MetodoAprendizaje, MetadatosOperativos,
    DimensionVida, NivelManifestacion, MetodoCaptura
)
from datetime import date, datetime
import json


def print_seccion(titulo: str):
    """Imprime sección con formato"""
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70 + "\n")


def pregunta_sacral(pregunta: str) -> bool:
    """Pregunta sacral binaria (sí/no)"""
    print(f"\n🔮 {pregunta}")
    print("   Siente la respuesta en tu cuerpo (no pienses).")
    while True:
        resp = input("   [S/N]: ").strip().upper()
        if resp in ['S', 'N']:
            return resp == 'S'
        print("   Por favor, responde S o N")


def input_con_default(prompt: str, default: str = "") -> str:
    """Input con valor por defecto"""
    if default:
        respuesta = input(f"{prompt} [{default}]: ").strip()
        return respuesta if respuesta else default
    return input(f"{prompt}: ").strip()


def configurar_diseño_humano() -> DiseñoHumano:
    """Configurar Diseño Humano"""
    print_seccion("🌟 Diseño Humano: Tu Blueprint Energético")
    
    print("Tipos:")
    print("  1. Manifestor (iniciar, impactar)")
    print("  2. Generador (responder, construir)")
    print("  3. Generador Manifestante (responder + iniciar)")
    print("  4. Proyector (guiar, esperar invitación)")
    print("  5. Reflector (reflejar, ciclo lunar)")
    
    tipo_map = {
        "1": TipoHumanDesign.MANIFESTOR,
        "2": TipoHumanDesign.GENERADOR,
        "3": TipoHumanDesign.GENERADOR_MANIFESTANTE,
        "4": TipoHumanDesign.PROYECTOR,
        "5": TipoHumanDesign.REFLECTOR
    }
    tipo = tipo_map[input_con_default("\nTu tipo", "2")]
    
    print("\nAutoridades:")
    print("  1. Sacral (respuesta visceral instantánea)")
    print("  2. Emocional (ola emocional completa)")
    print("  3. Esplénica (intuición en el momento)")
    print("  4. Ego (fuerza de voluntad)")
    print("  5. Self-Proyectado (expresión verbal)")
    print("  6. Mental (entorno - NO para decidir)")
    print("  7. Lunar (ciclo 28 días)")
    
    aut_map = {
        "1": AutoridadInterna.SACRAL,
        "2": AutoridadInterna.EMOCIONAL,
        "3": AutoridadInterna.ESPLENICA,
        "4": AutoridadInterna.EGO,
        "5": AutoridadInterna.SELF_PROYECTADO,
        "6": AutoridadInterna.MENTAL,
        "7": AutoridadInterna.LUNAR
    }
    autoridad = aut_map[input_con_default("Tu autoridad", "1")]
    
    estrategia_map = {
        TipoHumanDesign.MANIFESTOR: EstrategiaVital.INFORMAR,
        TipoHumanDesign.GENERADOR: EstrategiaVital.RESPONDER,
        TipoHumanDesign.GENERADOR_MANIFESTANTE: EstrategiaVital.RESPONDER,
        TipoHumanDesign.PROYECTOR: EstrategiaVital.ESPERAR_INVITACION,
        TipoHumanDesign.REFLECTOR: EstrategiaVital.ESPERAR_CICLO_LUNAR
    }
    estrategia = estrategia_map[tipo]
    
    perfil = input_con_default("\nTu perfil (ej: 5/1, 3/5)", "5/1")
    
    forma_decidir = input_con_default(
        "\n¿Cómo tomas decisiones correctas? (1 línea)",
        "Espero respuesta sacral (expansión/contracción) antes de decidir"
    )
    
    trampa = input_con_default(
        "\n¿Cuál es tu trampa mental principal?",
        "Iniciar mentalmente sin esperar respuesta del cuerpo"
    )
    
    return DiseñoHumano(
        tipo=tipo,
        autoridad=autoridad,
        estrategia=estrategia,
        perfil=perfil,
        centros_definidos=[],  # Se puede ampliar después
        canales_activos=[],
        patron_energia=f"Patrón de {tipo.value}",
        forma_correcta_decidir=forma_decidir,
        trampa_mental=trampa
    )


def configurar_perfil_psicologico() -> PerfilPsicologico:
    """Configurar MBTI + Eneagrama"""
    print_seccion("🧠 Perfil Psicológico: Tu Estructura Cognitiva")
    
    mbti_str = input_con_default("Tu MBTI (ej: ENTP, INTJ)", "ENTP").upper()
    mbti = TipoMBTI[mbti_str.replace("-", "_")]
    
    print("\nEneagrama:")
    print("  1-Perfeccionista  2-Ayudador  3-Triunfador")
    print("  4-Individualista  5-Investigador  6-Leal")
    print("  7-Entusiasta  8-Desafiador  9-Pacificador")
    
    enea_base = TipoEneagrama(input_con_default("\nTu tipo base", "5"))
    
    alas_input = input_con_default("Alas (separadas por coma, ej: 4,6)", "4,6")
    alas = [TipoEneagrama(a.strip()) for a in alas_input.split(",") if a.strip()]
    
    patron_aprendizaje = input_con_default(
        "\n¿Cómo aprendes mejor? (1-2 líneas)",
        "Exploración conceptual, conectando ideas, implementación práctica"
    )
    
    motivacion = input_con_default(
        "\n¿Qué te mueve profundamente?",
        "Comprensión de sistemas complejos, dominio técnico, autonomía"
    )
    
    punto_ciego = input_con_default(
        "\n¿Cuál es tu punto ciego?",
        "Desconexión de necesidades corporales, sobre-análisis"
    )
    
    return PerfilPsicologico(
        mbti=mbti,
        eneagrama_base=enea_base,
        alas=alas,
        patron_aprendizaje=patron_aprendizaje,
        motivacion_profunda=motivacion,
        punto_ciego=punto_ciego,
        trabajo_integracion=f"{enea_base.value}→8: Acción sin sobre-análisis"
    )


def configurar_manifestaciones() -> list[Manifestacion]:
    """Configurar manifestaciones principales"""
    print_seccion("✨ Manifestaciones: Qué Estás Materializando")
    
    manifestaciones = []
    
    print("Configuraremos tus 3 manifestaciones principales:")
    print("  1. Corto plazo (1-3 meses)")
    print("  2. Medio plazo (6-12 meses)")
    print("  3. Largo plazo (1-3 años)")
    
    dimensiones_map = {
        "1": DimensionVida.DESARROLLO,
        "2": DimensionVida.CONOCIMIENTO,
        "3": DimensionVida.FINANCIERO,
        "4": DimensionVida.BIOLOGICO,
        "5": DimensionVida.RELACIONES,
        "6": DimensionVida.ESPIRITUAL,
        "7": DimensionVida.CREATIVO
    }
    
    niveles = [
        (NivelManifestacion.TRIMESTRAL, "Trimestral (1-3 meses)"),
        (NivelManifestacion.ANUAL, "Anual (6-12 meses)"),
        (NivelManifestacion.QUINQUENAL, "Quinquenal (1-5 años)")
    ]
    
    for i, (nivel, nombre_nivel) in enumerate(niveles, 1):
        print(f"\n--- Manifestación {i}: {nombre_nivel} ---")
        
        print("\nDimensión:")
        print("  1-Desarrollo  2-Conocimiento  3-Financiero  4-Biológico")
        print("  5-Relaciones  6-Espiritual  7-Creativo")
        
        dim = dimensiones_map[input_con_default(f"Dimensión manifestación {i}", "1")]
        
        vision = input(f"\n¿Qué estás manifestando? (ej: 'Dominio de arquitecturas multi-agente'): ").strip()
        resultado = input("¿Cómo sabes que se materializó?: ").strip()
        practica = input("¿Qué práctica diaria lo materializa?: ").strip()
        
        manifestaciones.append(Manifestacion(
            id=f"m{i}",
            dimension=dim,
            nivel=nivel,
            vision=vision,
            resultado_observable=resultado,
            practica_diaria=practica,
            frecuencia_minima="diaria",
            tiempo_estimado_materializacion=nombre_nivel.split()[0].lower(),
            fecha_inicio=date.today(),
            progreso_estimado=0
        ))
    
    return manifestaciones


def configurar_conocimiento() -> tuple[EstructuraConocimiento, MetodoAprendizaje]:
    """Configurar sistema de conocimiento"""
    print_seccion("📚 Sistema Vivo de Conocimiento")
    
    print("¿Dónde capturas conocimiento primariamente?")
    print("  1. Obsidian")
    print("  2. Anytype")
    print("  3. Voz (transcripción)")
    
    captura_map = {
        "1": MetodoCaptura.OBSIDIAN,
        "2": MetodoCaptura.ANYTYPE,
        "3": MetodoCaptura.VOZ
    }
    captura = captura_map[input_con_default("Captura primaria", "1")]
    
    usa_zettel = pregunta_sacral("¿Usas método Zettelkasten / Segundo Cerebro?")
    
    estructura = EstructuraConocimiento(
        captura_primaria=captura,
        usa_zettelkasten=usa_zettel,
        sistema_vinculacion="backlinks",
        frecuencia_revision="semanal",
        umbral_nota_permanente="Cuando conecto con 3+ conceptos y puedo explicarlo en mis palabras",
        practica_sintesis_semanal=True,
        genera_mocs_automaticos=True,
        conecta_insights_automatico=True
    )
    
    print("\n¿Cuándo aprendes mejor?")
    mejor_momento = input_con_default("Momento óptimo", "07:00-12:00")
    
    print("\n¿Cuánto dura tu sesión de flujo profundo?")
    duracion = int(input_con_default("Minutos", "90"))
    
    metodo = MetodoAprendizaje(
        modalidad_preferida="lectura_escritura",
        profundidad_vs_amplitud=7,
        estrategias_efectivas=[
            "Exploración conceptual",
            "Construcción de frameworks",
            "Implementación práctica",
            "Enseñar/documentar"
        ],
        mejor_momento_aprendizaje=mejor_momento,
        duracion_optima_sesion=duracion,
        requiere_silencio=True,
        indicadores_dominio=[
            "Puedo explicarlo sin referencias",
            "Puedo implementarlo de memoria",
            "Puedo conectarlo con 5+ conceptos"
        ]
    )
    
    return estructura, metodo


def main():
    """Configuración interactiva completa"""
    print("\n" + "="*70)
    print("  🔮 CONFIGURACIÓN DEL PRISMA PERSONAL")
    print("  El organismo necesita conocer tu lente única")
    print("="*70)
    
    print("\nEste proceso toma ~15 minutos.")
    print("Usa respuestas SACRALES (siente, no pienses).")
    
    if not pregunta_sacral("\n¿Tu cuerpo se expande al configurar tu prisma ahora?"):
        print("\n⏸️  No problem. Vuelve cuando tu cuerpo diga sí.")
        print("   El organismo esperará.")
        return
    
    # Información básica
    print_seccion("👤 Información Básica")
    nombre = input("Tu nombre: ").strip()
    
    print("\nFecha de nacimiento (YYYY-MM-DD):")
    fecha_nac_str = input_con_default("", "1990-01-01")
    fecha_nac = datetime.strptime(fecha_nac_str, "%Y-%m-%d").date()
    
    # Configurar cada sección
    diseño = configurar_diseño_humano()
    perfil = configurar_perfil_psicologico()
    manifestaciones = configurar_manifestaciones()
    estructura_conocimiento, metodo_aprendizaje = configurar_conocimiento()
    
    # Crear prisma completo
    prisma = PrismaPersonal(
        nombre=nombre,
        fecha_nacimiento=fecha_nac,
        diseño_humano=diseño,
        perfil_psicologico=perfil,
        manifestaciones=manifestaciones,
        estructura_conocimiento=estructura_conocimiento,
        metodo_aprendizaje=metodo_aprendizaje,
        metadatos_operativos=MetadatosOperativos()
    )
    
    # Guardar
    print_seccion("💾 Guardando Prisma Personal")
    
    ruta = os.path.join(os.path.dirname(__file__), "..", "..", "config", "prisma_personal.json")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(prisma.model_dump_json(indent=2))
    
    print(f"✅ Prisma guardado en: {ruta}")
    
    # Resumen
    print_seccion("✨ Tu Prisma Personal")
    print(f"\n👤 {nombre}")
    print(f"🌟 {diseño.tipo.value.title()} | {diseño.autoridad.value.title()}")
    print(f"🧠 {perfil.mbti.value} | Eneagrama {perfil.eneagrama_base.value}")
    print(f"\n✨ Manifestaciones activas: {len(manifestaciones)}")
    for m in manifestaciones:
        print(f"   • {m.vision}")
    
    print(f"\n📚 Sistema: {estructura_conocimiento.captura_primaria.value.title()}")
    print(f"🎯 Aprendizaje óptimo: {metodo_aprendizaje.mejor_momento_aprendizaje}")
    
    print("\n" + "="*70)
    print("  🕌 El organismo ahora conoce tu prisma")
    print("  El espejo diario reflejará tu realidad única")
    print("="*70)
    
    print("\n💡 Próximo paso:")
    print("   El organismo comenzará a aprender tus patrones.")
    print("   Usa el sistema durante 7 días para que metabolice tu esencia.")


if __name__ == "__main__":
    main()

