"""
🕌 Estado Cero Ultra Simple - MVP Mínimo
=======================================

Solo lo esencial:
- Precisión matemática astronómica
- Archivo automático en Obsidian
- Sin IA sintética
"""

from fastapi import APIRouter, HTTPException, Request
from datetime import datetime, date
from pathlib import Path
import json
import os
import time
from services.event_queue import get_event_queue
from services.pregunta_liturgica import PreguntaLiturgica, MomentoLiturgico
from services.audit_trail import AuditTrail
from services.obsidian_structure import ObsidianStructureManager
from services.google_calendar import GoogleCalendarIntegration
from services.generador_preguntas import generar_pregunta_emergente

router = APIRouter()

# Configuración básica
LAT = float(os.getenv("LATITUD", "40.4168"))
LON = float(os.getenv("LONGITUD", "-3.7038"))
TZ = os.getenv("TIMEZONE", "Europe/Madrid")
VAULT_PATH = os.path.expanduser(os.getenv("OBSIDIAN_VAULT_PATH", "~/Documents/CampoSagrado"))

# Inicializar servicios
audit = AuditTrail(VAULT_PATH)
vault_manager = ObsidianStructureManager(VAULT_PATH)
calendar = GoogleCalendarIntegration(VAULT_PATH)


@router.get("/test")
async def test_endpoint():
    """Endpoint de prueba simple"""
    return {
        "status": "ok",
        "mensaje": "Estado Cero Simple funcionando",
        "timestamp": datetime.now().isoformat(),
        "ubicacion": f"{LAT}, {LON}",
        "timezone": TZ
    }


@router.post("/iniciar")
async def iniciar_estado_cero(modo: str = "emergente"):
    """
    Inicia Estado Cero con pregunta emergente única.

    Args:
        modo: "emergente" (default) = 1 pregunta del contexto | "liturgico" = 3 preguntas por momento

    El modo emergente genera UNA pregunta que:
    - Emerge del contexto multi-dimensional (momento, fase lunar, patrones)
    - Conecta múltiples dominios
    - Opera al borde del caos
    - REVELA en lugar de CONFIRMAR
    """
    start_time = time.time()

    try:
        # Generar ID único
        estado_cero_id = f"ec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Determinar momento actual (simplificado)
        hora_actual = datetime.now().hour
        if 5 <= hora_actual < 12:
            momento = "fajr"
        elif 12 <= hora_actual < 16:
            momento = "dhuhr"
        elif 16 <= hora_actual < 19:
            momento = "asr"
        elif 19 <= hora_actual < 21:
            momento = "maghrib"
        else:
            momento = "isha"

        # Generar pregunta según modo
        if modo == "emergente":
            # MODO NUEVO: Una pregunta emergente del contexto
            pregunta_data = generar_pregunta_emergente(momento, usuario_id="default")

            preguntas = [
                {
                    "id": 0,
                    "texto": pregunta_data["pregunta"],
                    "dimension": pregunta_data["dominios"][0] if pregunta_data["dominios"] else "existencial",
                    "polaridad": "revelacion",
                    "respondida": False,
                    "contexto_emergente": pregunta_data["contexto"],
                    "tipo": pregunta_data["tipo"],
                    "fase_lunar": pregunta_data["fase_lunar"]
                }
            ]

        else:
            # MODO LEGACY: Preguntas litúrgicas predefinidas
            momento_enum = MomentoLiturgico(momento)
            preguntas_liturgicas = PreguntaLiturgica.obtener_preguntas(momento_enum)

            preguntas = [
                {
                    "id": i,
                    "texto": p["texto"],
                    "dimension": p["dimension"],
                    "polaridad": p["polaridad"],
                    "respondida": False
                }
                for i, p in enumerate(preguntas_liturgicas)
            ]
        
        # Crear Estado Cero
        estado_cero = {
            "id": estado_cero_id,
            "momento": momento,
            "modo": modo,  # Nuevo: tracking del modo usado
            "fecha": date.today().isoformat(),
            "timestamp": datetime.now().isoformat(),
            "intencion": "",  # Hoja en blanco para intención
            "reflexion": "",  # Hoja en blanco para reflexión
            "preguntas": preguntas,
            "respuestas": [],
            "completado": False,
            "archivado_en_obsidian": False
        }
        
        # Guardar localmente
        guardar_estado_cero_local(estado_cero)
        
        # Audit trail
        duracion = int((time.time() - start_time) * 1000)
        audit.log_event(
            event_type="estado_cero_iniciado",
            origen="user_request",
            estado="success",
            metadata={
                "estado_cero_id": estado_cero_id,
                "momento": momento,
                "preguntas_count": len(preguntas)
            },
            duracion_ms=duracion
        )
        
        return {
            "estado_cero_id": estado_cero_id,
            "momento": momento,
            "modo": modo,
            "preguntas": preguntas,
            "mensaje": f"Estado Cero {momento.upper()} iniciado en modo {modo}"
        }
    
    except Exception as e:
        duracion = int((time.time() - start_time) * 1000)
        audit.log_event(
            event_type="estado_cero_iniciado",
            origen="user_request",
            estado="error",
            metadata={"error": str(e)},
            duracion_ms=duracion
        )
        raise


@router.post("/{estado_cero_id}/responder")
async def responder_pregunta(estado_cero_id: str, request: Request):
    """
    Registra respuesta binaria
    """
    
    body = await request.json()
    pregunta_id = body.get("pregunta_id")
    respuesta = body.get("respuesta")
    nota = body.get("nota")
    
    if pregunta_id is None or respuesta is None:
        raise HTTPException(status_code=400, detail="pregunta_id y respuesta son requeridos")
    
    # Cargar Estado Cero
    estado_cero = cargar_estado_cero_local(estado_cero_id)
    if not estado_cero:
        raise HTTPException(status_code=404, detail="Estado Cero no encontrado")
    
    # Obtener dimensión de la pregunta
    pregunta_data = next((p for p in estado_cero["preguntas"] if p["id"] == pregunta_id), None)
    if not pregunta_data:
        raise HTTPException(status_code=404, detail=f"Pregunta {pregunta_id} no encontrada")
    
    # Registrar respuesta con dimensión
    respuesta_data = {
        "pregunta_id": pregunta_id,
        "respuesta": respuesta,
        "dimension": pregunta_data.get("dimension", "desconocido"),
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


@router.post("/{estado_cero_id}/guardar-texto")
async def guardar_texto(estado_cero_id: str, request: Request):
    """
    Guarda intención o reflexión
    """
    
    body = await request.json()
    tipo = body.get("tipo")  # "intencion" o "reflexion"
    texto = body.get("texto")
    
    if not tipo or texto is None:
        raise HTTPException(status_code=400, detail="tipo y texto son requeridos")
    
    # Cargar Estado Cero
    estado_cero = cargar_estado_cero_local(estado_cero_id)
    if not estado_cero:
        raise HTTPException(status_code=404, detail="Estado Cero no encontrado")
    
    # Guardar texto
    estado_cero[tipo] = texto
    
    # Guardar actualización
    guardar_estado_cero_local(estado_cero)
    
    return {
        "status": "success",
        "tipo": tipo,
        "texto_guardado": texto
    }


@router.post("/{estado_cero_id}/finalizar")
async def finalizar_estado_cero(estado_cero_id: str):
    """
    Finaliza Estado Cero y archiva en Obsidian con estructura fractal
    """
    start_time = time.time()
    
    try:
        # Cargar Estado Cero
        estado_cero = cargar_estado_cero_local(estado_cero_id)
        if not estado_cero:
            raise HTTPException(status_code=404, detail="Estado Cero no encontrado")
        
        # Marcar como completado
        estado_cero["completado"] = True
        estado_cero["fecha_finalizacion"] = datetime.now().isoformat()
        
        # Generar síntesis simple
        respuestas = estado_cero["respuestas"]
        expansion_count = sum(1 for r in respuestas if r["respuesta"])
        contraccion_count = len(respuestas) - expansion_count
        
        if expansion_count > contraccion_count:
            tendencia = "expansión"
            intensidad = expansion_count / len(respuestas)
        else:
            tendencia = "contracción"
            intensidad = contraccion_count / len(respuestas)
        
        # Calcular dominios activos
        dominios_activos = PreguntaLiturgica.calcular_dominio_activo(respuestas)
        
        sintesis = {
            "tendencia": tendencia,
            "intensidad": intensidad,
            "direccion_emergente": f"En este momento {estado_cero['momento'].upper()}, tu energía tiende hacia la {tendencia} ({intensidad:.1%}).",
            "dominios_activos": dominios_activos
        }
        
        estado_cero["sintesis"] = sintesis
        
        # Archivar en Obsidian con estructura fractal
        archivo_path = archivar_en_obsidian_fractal(estado_cero)
        estado_cero["archivado_en_obsidian"] = True
        estado_cero["archivo_path"] = str(archivo_path)
        
        # Guardar estado final
        guardar_estado_cero_local(estado_cero)
        
        # Emitir evento para worker de ingesta
        event_queue = get_event_queue()
        event_id = event_queue.emit("estado_cero_completed", {
            "estado_cero_id": estado_cero_id,
            "momento": estado_cero["momento"],
            "fecha": estado_cero["fecha"],
            "archivo_path": str(archivo_path),
            "tendencia": sintesis["tendencia"],
            "intensidad": sintesis["intensidad"],
            "dominios_activos": dominios_activos
        })
        
        # Sincronizar con Google Calendar
        try:
            fecha_estado = date.fromisoformat(estado_cero["fecha"])
            await calendar.sincronizar_estado_cero_completado(
                estado_cero_id=estado_cero_id,
                momento=estado_cero["momento"],
                fecha=fecha_estado,
                tendencia=sintesis["tendencia"],
                intensidad=sintesis["intensidad"]
            )
            print(f"📅 Estado Cero sincronizado con Google Calendar")
        except Exception as e:
            print(f"⚠️ Error sincronizando con calendario: {e}")
            # No fallar el endpoint por error de calendario
        
        # Audit trail
        duracion = int((time.time() - start_time) * 1000)
        audit.log_event(
            event_type="estado_cero_finalizado",
            origen="user_request",
            estado="success",
            metadata={
                "estado_cero_id": estado_cero_id,
                "momento": estado_cero["momento"],
                "tendencia": sintesis["tendencia"],
                "intensidad": sintesis["intensidad"],
                "archivo_path": str(archivo_path)
            },
            duracion_ms=duracion
        )
        
        return {
            "status": "completado",
            "estado_cero_id": estado_cero_id,
            "sintesis": sintesis,
            "archivo_obsidian": str(archivo_path),
            "event_id": event_id,
            "mensaje": "Estado Cero completado y archivado en Obsidian (estructura fractal)"
        }
    
    except Exception as e:
        duracion = int((time.time() - start_time) * 1000)
        audit.log_event(
            event_type="estado_cero_finalizado",
            origen="user_request",
            estado="error",
            metadata={
                "estado_cero_id": estado_cero_id,
                "error": str(e)
            },
            duracion_ms=duracion
        )
        raise


def archivar_en_obsidian_fractal(estado_cero: dict) -> Path:
    """
    Archiva Estado Cero en estructura fractal de Obsidian
    Usa ObsidianStructureManager para determinar la ruta correcta
    """
    
    fecha = datetime.fromisoformat(estado_cero["timestamp"]).date()
    momento = estado_cero["momento"]
    
    # Obtener ruta según estructura fractal
    archivo_path = vault_manager.get_estado_cero_path(fecha, momento)
    archivo_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generar contenido markdown
    contenido = generar_markdown_estado_cero(estado_cero)
    
    with open(archivo_path, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    return archivo_path


def generar_markdown_estado_cero(estado_cero: dict) -> str:
    """
    Genera markdown para Obsidian con metadata ampliada.
    Soporta modo emergente (1 pregunta) y litúrgico (múltiples).
    """

    sintesis = estado_cero["sintesis"]
    dominios_activos = sintesis.get("dominios_activos", {})
    modo = estado_cero.get("modo", "liturgico")

    # Determinar dominio predominante
    try:
        dominio_predominante = max(dominios_activos.items(), key=lambda x: x[1])[0] if dominios_activos else "equilibrado"
    except (ValueError, KeyError):
        dominio_predominante = "equilibrado"

    # Metadata adicional para modo emergente
    pregunta_emergente = estado_cero["preguntas"][0] if modo == "emergente" else None
    fase_lunar = pregunta_emergente.get("fase_lunar", "N/A") if pregunta_emergente else "N/A"

    markdown = f"""---
tipo: estado-cero
modo: {modo}
momento: {estado_cero['momento']}
fecha: {estado_cero['fecha']}
timestamp: {estado_cero['timestamp']}
tendencia: {sintesis['tendencia']}
intensidad: {sintesis['intensidad']:.2f}
dominio_predominante: {dominio_predominante}
fase_lunar: {fase_lunar}
hrv_disponible: false
hrv_rmssd: null
hrv_coherence: null
---

# 🕌 Estado Cero - {estado_cero['momento'].upper()}

**Fecha:** {estado_cero['fecha']}
**Momento:** {estado_cero['momento'].upper()}
**Modo:** {modo.title()}
**Dominio Predominante:** {dominio_predominante.title()}
"""

    # Añadir contexto emergente si aplica
    if modo == "emergente" and pregunta_emergente:
        contexto_emergente = pregunta_emergente.get("contexto_emergente", "")
        if contexto_emergente:
            markdown += f"""
**Contexto emergente:** {contexto_emergente}
**Fase lunar:** {fase_lunar}
"""

    markdown += """

## Intención

{estado_cero.get('intencion', '_No escrita_')}

## Preguntas y Respuestas

"""
    
    for i, pregunta in enumerate(estado_cero["preguntas"]):
        respuesta = next((r for r in estado_cero["respuestas"] if r["pregunta_id"] == i), None)
        if respuesta:
            simbolo = "✅" if respuesta["respuesta"] else "❌"
            nota = f" - {respuesta.get('nota', '')}" if respuesta.get("nota") else ""
            dimension = pregunta.get('dimension', 'N/A')
            markdown += f"- {simbolo} **{pregunta['texto']}** _{dimension}_{nota}\n"
        else:
            markdown += f"- ⏳ **{pregunta['texto']}**\n"
    
    # Dominios activos
    if dominios_activos:
        markdown += "\n### Dominios Activos\n\n"
        for dominio, intensidad in sorted(dominios_activos.items(), key=lambda x: x[1], reverse=True):
            markdown += f"- **{dominio.title()}**: {intensidad:.0%}\n"
    
    markdown += f"""

## Reflexión

{estado_cero.get('reflexion', '_No escrita_')}

## Síntesis

**Tendencia:** {sintesis['tendencia']} ({sintesis['intensidad']:.1%})  
**Dirección emergente:** {sintesis['direccion_emergente']}

## Metadatos del Organismo

- **Momento litúrgico:** {estado_cero['momento']}
- **Estado de completitud:** {'Completado' if estado_cero['completado'] else 'En progreso'}
- **Archivado:** {estado_cero['archivado_en_obsidian']}
- **HRV disponible:** No (futuro: Polar H10)

---

*Archivado automáticamente por Campo Sagrado del Entrelazador*  
*Sistema operando al borde del caos - 40% capacidad sin asignar*
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
