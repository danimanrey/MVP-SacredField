"""
🕌 Estado Cero Simple - MVP Mínimo
=================================

Estado Cero sin IA sintética, solo con:
- Precisión matemática astronómica
- Archivo automático en Obsidian
- Metadatos para metabolismo del organismo
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
from pathlib import Path
import json
import os

from models.database import get_db
from services.tiempos_liturgicos import CalculadorTiemposLiturgicos
from services.calendario_hijri import CalendarioHijri

router = APIRouter()

# Configuración
LAT = float(os.getenv("LATITUD", "40.4168"))
LON = float(os.getenv("LONGITUD", "-3.7038"))
TZ = os.getenv("TIMEZONE", "Europe/Madrid")

# Servicios
calculador = CalculadorTiemposLiturgicos(LAT, LON, TZ)
calendario = CalendarioHijri()


@router.post("/iniciar-simple")
async def iniciar_estado_cero_simple(
    momento: str = None,
    db: Session = Depends(get_db)
):
    """
    Inicia Estado Cero simple sin IA sintética
    
    Solo genera:
    - Contexto temporal preciso
    - Preguntas binarias contextuales
    - Archivo automático en Obsidian
    """
    
    # Determinar momento actual si no se especifica
    if not momento:
        verificacion = calculador.verificar_momento_estado_cero()
        if verificacion["es_momento"]:
            momento = verificacion["momento"]
        else:
            proximo = calculador.proximo_estado_cero()
            momento = proximo["momento"]
    
    # Contexto temporal completo
    contexto_temporal = calendario.obtener_contexto_temporal_completo(date.today())
    tiempos_hoy = calculador.calcular_tiempos_hoy()
    
    # Generar preguntas contextuales según momento
    preguntas = generar_preguntas_contextuales(momento, contexto_temporal)
    
    # Crear Estado Cero
    estado_cero_id = f"ec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    estado_cero = {
        "id": estado_cero_id,
        "momento": momento,
        "fecha": date.today().isoformat(),
        "timestamp": datetime.now().isoformat(),
        "contexto_temporal": contexto_temporal,
        "tiempos_liturgicos": tiempos_hoy,
        "preguntas": preguntas,
        "respuestas": [],
        "completado": False,
        "archivado_en_obsidian": False
    }
    
    # Guardar en base de datos local
    guardar_estado_cero_local(estado_cero)
    
    return {
        "estado_cero_id": estado_cero_id,
        "momento": momento,
        "contexto_temporal": contexto_temporal,
        "preguntas": preguntas,
        "tiempos_liturgicos": tiempos_hoy,
        "mensaje": f"Estado Cero {momento.upper()} iniciado. Responde las preguntas binarias."
    }


@router.post("/{estado_cero_id}/responder")
async def responder_pregunta(
    estado_cero_id: str,
    pregunta_id: int,
    respuesta: bool,
    nota: str = None,
    db: Session = Depends(get_db)
):
    """
    Registra respuesta binaria a pregunta del Estado Cero
    """
    
    # Cargar Estado Cero
    estado_cero = cargar_estado_cero_local(estado_cero_id)
    if not estado_cero:
        raise HTTPException(status_code=404, detail="Estado Cero no encontrado")
    
    # Registrar respuesta
    respuesta_data = {
        "pregunta_id": pregunta_id,
        "respuesta": respuesta,
        "nota": nota,
        "timestamp": datetime.now().isoformat()
    }
    
    estado_cero["respuestas"].append(respuesta_data)
    
    # Guardar actualización
    guardar_estado_cero_local(estado_cero)
    
    return {
        "status": "success",
        "respuesta_registrada": respuesta_data,
        "progreso": f"{len(estado_cero['respuestas'])}/{len(estado_cero['preguntas'])}"
    }


@router.post("/{estado_cero_id}/finalizar")
async def finalizar_estado_cero(
    estado_cero_id: str,
    db: Session = Depends(get_db)
):
    """
    Finaliza Estado Cero y archiva en Obsidian
    """
    
    # Cargar Estado Cero
    estado_cero = cargar_estado_cero_local(estado_cero_id)
    if not estado_cero:
        raise HTTPException(status_code=404, detail="Estado Cero no encontrado")
    
    # Marcar como completado
    estado_cero["completado"] = True
    estado_cero["fecha_finalizacion"] = datetime.now().isoformat()
    
    # Generar síntesis simple
    sintesis = generar_sintesis_simple(estado_cero)
    estado_cero["sintesis"] = sintesis
    
    # Archivar en Obsidian
    archivo_path = archivar_en_obsidian(estado_cero)
    estado_cero["archivado_en_obsidian"] = True
    estado_cero["archivo_path"] = str(archivo_path)
    
    # Guardar estado final
    guardar_estado_cero_local(estado_cero)
    
    return {
        "status": "completado",
        "estado_cero_id": estado_cero_id,
        "sintesis": sintesis,
        "archivo_obsidian": str(archivo_path),
        "mensaje": "Estado Cero completado y archivado en Obsidian"
    }


def generar_preguntas_contextuales(momento: str, contexto_temporal: dict) -> list:
    """
    Genera preguntas binarias contextuales según momento y contexto
    """
    
    base_preguntas = {
        "fajr": [
            "¿Siento expansión o contracción al despertar?",
            "¿Mi energía fluye hacia la creación o hacia la protección?",
            "¿Mi cuerpo pide movimiento o quietud?",
            "¿Mi mente busca claridad o acepta la niebla?",
            "¿Mi corazón está abierto o cerrado al día?",
            "¿Mi espíritu anhela conexión o soledad?"
        ],
        "dhuhr": [
            "¿Mi energía está en su cenit o declinando?",
            "¿Necesito acelerar o desacelerar el ritmo?",
            "¿Mi enfoque está disperso o concentrado?",
            "¿Mi cuerpo pide alimento o puede esperar?",
            "¿Mi mente busca nuevos desafíos o consolidación?",
            "¿Mi corazón está satisfecho o inquieto?"
        ],
        "maghrib": [
            "¿Siento gratitud o resistencia al cierre del día?",
            "¿Mi energía se integra o se dispersa?",
            "¿Mi cuerpo pide descanso o actividad?",
            "¿Mi mente busca reflexión o distracción?",
            "¿Mi corazón está en paz o agitado?",
            "¿Mi espíritu se conecta o se desconecta?"
        ]
    }
    
    preguntas = base_preguntas.get(momento, base_preguntas["dhuhr"])
    
    # Personalizar según contexto del mes Hijri
    mes_hijri = contexto_temporal["mes_hijri"]
    if mes_hijri["cualidad"] == "expansión":
        preguntas[0] = f"¿Siento {mes_hijri['cualidad']} o contracción en este momento?"
    
    return [
        {"id": i, "texto": pregunta, "respondida": False}
        for i, pregunta in enumerate(preguntas)
    ]


def generar_sintesis_simple(estado_cero: dict) -> dict:
    """
    Genera síntesis simple basada en respuestas binarias
    """
    
    respuestas = estado_cero["respuestas"]
    momento = estado_cero["momento"]
    
    # Contar expansión vs contracción
    expansion_count = sum(1 for r in respuestas if r["respuesta"])
    contraccion_count = len(respuestas) - expansion_count
    
    # Determinar tendencia
    if expansion_count > contraccion_count:
        tendencia = "expansión"
        intensidad = expansion_count / len(respuestas)
    else:
        tendencia = "contracción"
        intensidad = contraccion_count / len(respuestas)
    
    # Generar dirección emergente simple
    contexto_temporal = estado_cero["contexto_temporal"]
    mes_hijri = contexto_temporal["mes_hijri"]
    
    direccion = f"""
En este momento {momento.upper()} de {mes_hijri['nombre']} ({mes_hijri['cualidad']}):
- Tu energía tiende hacia la {tendencia} ({intensidad:.1%})
- El mes invita a: {mes_hijri['practica']}
- Tu dimensión prioritaria: {mes_hijri['dimension']}
- Próximo momento: {calculador.proximo_estado_cero()['momento']}
"""
    
    return {
        "tendencia": tendencia,
        "intensidad": intensidad,
        "direccion_emergente": direccion.strip(),
        "momento": momento,
        "mes_hijri": mes_hijri["nombre"],
        "dimension_activa": mes_hijri["dimension"]
    }


def archivar_en_obsidian(estado_cero: dict) -> Path:
    """
    Archiva Estado Cero en Obsidian con estructura temporal
    """
    
    vault_path = Path(os.getenv("OBSIDIAN_VAULT_PATH", "obsidian_vault"))
    
    # Estructura: Estados-Cero/YYYY/MM/DD-momento.md
    fecha = datetime.fromisoformat(estado_cero["timestamp"])
    año = fecha.year
    mes = fecha.month
    dia = fecha.day
    momento = estado_cero["momento"]
    
    archivo_dir = vault_path / "Estados-Cero" / str(año) / f"{mes:02d}"
    archivo_dir.mkdir(parents=True, exist_ok=True)
    
    archivo_path = archivo_dir / f"{dia:02d}-{momento}.md"
    
    # Generar contenido markdown
    contenido = generar_markdown_estado_cero(estado_cero)
    
    with open(archivo_path, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    return archivo_path


def generar_markdown_estado_cero(estado_cero: dict) -> str:
    """
    Genera markdown estructurado para Obsidian
    """
    
    contexto = estado_cero["contexto_temporal"]
    sintesis = estado_cero["sintesis"]
    
    markdown = f"""---
tipo: estado-cero
momento: {estado_cero['momento']}
fecha: {estado_cero['fecha']}
timestamp: {estado_cero['timestamp']}
mes_hijri: {contexto['mes_hijri']['nombre']}
dimension_activa: {sintesis['dimension_activa']}
tendencia: {sintesis['tendencia']}
intensidad: {sintesis['intensidad']:.2f}
---

# 🕌 Estado Cero - {estado_cero['momento'].upper()}

**Fecha:** {estado_cero['fecha']}  
**Momento:** {estado_cero['momento'].upper()}  
**Mes Hijri:** {contexto['mes_hijri']['nombre']} ({contexto['mes_hijri']['cualidad']})

## Contexto Temporal

- **Mes Hijri:** {contexto['mes_hijri']['nombre']} - {contexto['mes_hijri']['significado']}
- **Día de la semana:** {contexto['dia_semana']['nombre']} - {contexto['dia_semana']['proposito']}
- **Dimensión activa:** {contexto['mes_hijri']['dimension']}
- **Práctica del mes:** {contexto['mes_hijri']['practica']}

## Preguntas y Respuestas

"""
    
    for i, pregunta in enumerate(estado_cero["preguntas"]):
        respuesta = next((r for r in estado_cero["respuestas"] if r["pregunta_id"] == i), None)
        if respuesta:
            simbolo = "✅" if respuesta["respuesta"] else "❌"
            nota = f" - {respuesta['nota']}" if respuesta["nota"] else ""
            markdown += f"- {simbolo} **{pregunta['texto']}**{nota}\n"
        else:
            markdown += f"- ⏳ **{pregunta['texto']}**\n"
    
    markdown += f"""

## Síntesis

**Tendencia:** {sintesis['tendencia']} ({sintesis['intensidad']:.1%})  
**Dirección emergente:** {sintesis['direccion_emergente']}

## Metadatos del Organismo

- **Momento litúrgico:** {estado_cero['momento']}
- **Cualidad del mes:** {contexto['mes_hijri']['cualidad']}
- **Dimensión prioritaria:** {sintesis['dimension_activa']}
- **Estado de completitud:** {'Completado' if estado_cero['completado'] else 'En progreso'}

---

*Archivado automáticamente por Campo Sagrado del Entrelazador*
"""
    
    return markdown


def guardar_estado_cero_local(estado_cero: dict):
    """
    Guarda Estado Cero en archivo local JSON
    """
    
    storage_dir = Path("storage/estados_cero")
    storage_dir.mkdir(parents=True, exist_ok=True)
    
    archivo_path = storage_dir / f"{estado_cero['id']}.json"
    
    with open(archivo_path, 'w', encoding='utf-8') as f:
        json.dump(estado_cero, f, indent=2, ensure_ascii=False)


def cargar_estado_cero_local(estado_cero_id: str) -> dict:
    """
    Carga Estado Cero desde archivo local JSON
    """
    
    archivo_path = Path(f"storage/estados_cero/{estado_cero_id}.json")
    
    if not archivo_path.exists():
        return None
    
    with open(archivo_path, 'r', encoding='utf-8') as f:
        return json.load(f)
