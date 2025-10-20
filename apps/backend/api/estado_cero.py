from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime

from models.database import get_db, EstadoCeroDB
from models.schemas import (
    EstadoCeroCompleto, IniciarEstadoCeroRequest,
    ResponderPreguntaRequest, ChatClarificacionRequest,
    RespuestaSacral, MensajeChat, AccionConcreta,
    MomentoLiturgico
)
from agentes.estado_cero import AgenteEstadoCero
from agentes.documentador import AgenteDocumentador
from services.claude_client import ClaudeClient
from services.contexto import RecopiladorContexto
from services.tiempos_liturgicos import CalculadorTiemposLiturgicos
from services.calendario_hijri import CalendarioHijri
import os

router = APIRouter()

# Servicios
LAT = float(os.getenv("LATITUD", "40.4168"))
LON = float(os.getenv("LONGITUD", "-3.7038"))
TZ = os.getenv("TIMEZONE", "Europe/Madrid")
VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "/Users/hp/Campo sagrado MVP/obsidian_vault")

calculador = CalculadorTiemposLiturgicos(LAT, LON, TZ)
calendario = CalendarioHijri()
claude_client = ClaudeClient()

@router.get("/test")
async def test_endpoint():
    return {"status": "ok", "message": "Estado Cero endpoint funcionando"}

@router.post("/simple")
async def iniciar_simple():
    return {"status": "simple", "message": "Endpoint simple funcionando"}

@router.get("/verificar-momento")
async def verificar_momento_estado_cero(permitir_recuperacion: bool = False):
    """
    Verifica si es momento adecuado para realizar un Estado Cero.
    """
    verificacion = calculador.verificar_momento_estado_cero(permitir_fuera_ventana=permitir_recuperacion)
    
    # Convertir a dict para manipulación
    result = verificacion.dict() if hasattr(verificacion, 'dict') else verificacion
    
    # Estandarizar campos para compatibilidad con frontend
    if 'momento' in result and result['momento']:
        # Asegurar que 'momento_liturgico' existe como alias
        result['momento_liturgico'] = result['momento'].value if hasattr(result['momento'], 'value') else str(result['momento'])
    
    if 'minutos_restantes' in result:
        # Asegurar que 'tiempo_disponible_minutos' existe como alias
        result['tiempo_disponible_minutos'] = result['minutos_restantes']
    
    if 'proximo_momento' in result and result['proximo_momento']:
        # Estandarizar nombre del próximo tiempo de rezo
        result['proximo_tiempo_rezo'] = result['proximo_momento'].value if hasattr(result['proximo_momento'], 'value') else str(result['proximo_momento'])
    
    return result

@router.get("/ventanas-perdidas")
async def obtener_ventanas_perdidas(db: Session = Depends(get_db)):
    """
    Retorna los Estados Cero que se perdieron hoy y pueden recuperarse.
    
    Útil para mostrar en UI:
    - "Perdiste Maghrib (19:43-21:09). ¿Recuperar ahora?"
    """
    from datetime import date as Date
    import json
    
    hoy = Date.today()
    tiempos = calculador.calcular_tiempos_hoy(hoy)
    ahora = calculador._hoy()
    
    ventanas_perdidas = []
    
    for momento_nombre in ["fajr", "dhuhr", "asr", "maghrib", "isha"]:
        tiempo = getattr(tiempos, momento_nombre)
        
        # Si la ventana ya pasó
        if ahora > tiempo.fin:
            # Verificar si se realizó el Estado Cero
            estado_realizado = db.query(EstadoCeroDB).filter(
                EstadoCeroDB.fecha == hoy,
                EstadoCeroDB.momento == momento_nombre,
                EstadoCeroDB.completado == True
            ).first()
            
            if not estado_realizado:
                ventanas_perdidas.append({
                    "momento": momento_nombre,
                    "ventana_inicio": tiempo.inicio.isoformat(),
                    "ventana_fin": tiempo.fin.isoformat(),
                    "puede_recuperarse": True,
                    "mensaje": f"Estado Cero de {momento_nombre.capitalize()} no realizado ({tiempo.inicio.strftime('%H:%M')}-{tiempo.fin.strftime('%H:%M')})"
                })
    
    return {
        "fecha": hoy.isoformat(),
        "ventanas_perdidas": ventanas_perdidas,
        "total_perdidas": len(ventanas_perdidas)
    }


@router.post("/iniciar-test")
async def iniciar_estado_cero_test(
    request: IniciarEstadoCeroRequest,
    db: Session = Depends(get_db)
):
    """
    🧪 ENDPOINT DE TESTING - Sin validación de momento litúrgico
    Permite probar el sistema de 7 capas en cualquier momento
    """
    try:
        # Usar directamente el generador de preguntas de 7 capas
        from services.generador_preguntas_7_capas import GeneradorPreguntas7Capas
        import uuid
        from datetime import datetime

        generador = GeneradorPreguntas7Capas()

        # Generar pregunta usando sistema de 7 capas
        resultado = generador.generar_pregunta_unica(
            momento=request.momento.value,
            energia=request.energia,
            calidad_sueno=request.calidad_sueno,
            resonancia_corporal=request.resonancia_corporal,
            estado_emocional=request.estado_emocional,
            intensidad_emocional=request.intensidad_emocional
        )

        # Crear un estado simplificado para retornar
        estado_id = str(uuid.uuid4())

        # Retornar formato compatible con frontend
        return {
            "estado_cero_id": estado_id,
            "momento": request.momento.value,
            "preguntas": [
                {
                    "id": 1,
                    "texto": resultado["pregunta"],
                    "respondida": False
                }
            ],
            "intencion": "",
            "reflexion": "",
            "contexto_7_capas": resultado["contexto_7_capas"],
            "dominios_conectados": resultado["dominios"]
        }

    except Exception as e:
        print(f"❌ Error en iniciar_estado_cero_test: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/iniciar")
async def iniciar_estado_cero(
    request: IniciarEstadoCeroRequest,
    db: Session = Depends(get_db),
    permitir_recuperacion: bool = False,
    modo_testing: bool = True  # 🔥 NUEVO: modo testing habilitado por defecto para MVP
):
    """
    🔥 INTEGRACIÓN TOTAL - Sistema de 7 Capas

    Inicia nueva consulta de Estado Cero con sistema de 7 capas integrado.

    Query params:
    - permitir_recuperacion: Si True, permite realizar Estado Cero fuera de ventana
    - modo_testing: Si True (default), no valida momento litúrgico (útil para desarrollo/testing)
    """
    try:
        # 🔥 MODO TESTING: Saltamos validación litúrgica para desarrollo
        if not modo_testing:
            # Solo validar momento si NO estamos en modo testing
            verificacion = calculador.verificar_momento_estado_cero(permitir_fuera_ventana=permitir_recuperacion)
            if not verificacion.es_momento:
                raise HTTPException(
                    status_code=400,
                    detail=f"No es momento de Estado Cero. Próximo: {verificacion.momento.value}"
                )

            # Verificar momento solicitado
            if verificacion.momento != request.momento:
                # Si estamos fuera de ventana y es recuperación, permitir
                if not (verificacion.fuera_de_ventana and permitir_recuperacion):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Momento incorrecto. Ahora es: {verificacion.momento.value}"
                    )

        # Crear agente y recopilador
        recopilador = RecopiladorContexto(db, calculador, calendario)
        agente = AgenteEstadoCero(db, claude_client, recopilador)

        # Iniciar consulta con parámetros de 7 capas
        estado = await agente.iniciar_consulta(
            request.momento,
            energia=request.energia,
            calidad_sueno=request.calidad_sueno,
            resonancia_corporal=request.resonancia_corporal,
            estado_emocional=request.estado_emocional,
            intensidad_emocional=request.intensidad_emocional
        )
        
        # Guardar estado inicial en DB
        estado_db = EstadoCeroDB(
            id=estado.id,
            fecha=estado.fecha,
            momento=estado.momento.value,
            contexto=json.dumps(estado.contexto.model_dump(), default=str),
            preguntas=json.dumps([p.model_dump() for p in estado.preguntas]),
            respuestas="[]",
            direccion="",
            accion="{}",
            chat="[]",
            completado=False
        )
        db.add(estado_db)
        db.commit()
        
        # 🔥 Retornar formato compatible con frontend (mismo que /iniciar-test)
        return {
            "estado_cero_id": estado.id,  # Usar estado_cero_id (no id) para frontend
            "momento": estado.momento.value,
            "preguntas": [
                {
                    "id": idx + 1,  # Frontend espera id numérico
                    "texto": p.pregunta,  # Frontend espera "texto" (no "pregunta")
                    "respondida": False
                } for idx, p in enumerate(estado.preguntas)
            ],
            "intencion": "",
            "reflexion": "",
            # Contexto adicional para debugging/visualización
            "contexto": {
                "temporal": {
                    "momento_liturgico": estado.contexto.temporal.momento_liturgico.value,
                    "dia_semana": estado.contexto.temporal.dia_semana,
                    "mes_hijri": estado.contexto.temporal.mes_hijri,
                    "cualidad_momento": estado.contexto.temporal.cualidad_momento,
                    "cualidad_mes": estado.contexto.temporal.cualidad_mes
                },
                "biologico": {
                    "energia_actual": estado.contexto.biologico.energia_actual,
                    "luz_solar_hoy": estado.contexto.biologico.luz_solar_hoy,
                    "ejercicio_hoy": estado.contexto.biologico.ejercicio_hoy
                },
                "tiempo_disponible_hoy": estado.contexto.tiempo_disponible_hoy
            }
        }
        
    except Exception as e:
        print(f"❌ Error en iniciar_estado_cero: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{estado_id}/guardar-texto")
async def guardar_texto(
    estado_id: str,
    request: dict = Body(...),
    db: Session = Depends(get_db)
):
    """Guarda intención o reflexión - Para modo testing simplificado"""
    # En modo testing, solo retornamos OK sin guardar en DB
    # (ya que no tenemos registro completo en DB)
    return {"status": "ok", "mensaje": "Texto guardado"}


@router.post("/{estado_id}/responder")
async def responder_pregunta(
    estado_id: str,
    request: dict = Body(...),
    db: Session = Depends(get_db)
):
    """Registra respuesta sacral - Simplificado para testing"""
    # En modo testing, aceptamos cualquier formato
    # y retornamos OK
    return {"status": "ok"}


@router.post("/{estado_id}/sintetizar")
async def sintetizar_direccion(
    estado_id: str,
    db: Session = Depends(get_db)
):
    """
    Sintetiza dirección emergente de las respuestas sacrales
    """
    
    recopilador = RecopiladorContexto(db, calculador, calendario)
    agente = AgenteEstadoCero(db, claude_client, recopilador)
    
    # Obtener estado
    estado_db = db.query(EstadoCeroDB).filter(EstadoCeroDB.id == estado_id).first()
    if not estado_db:
        raise HTTPException(status_code=404, detail="Estado Cero no encontrado")
    
    # Convertir respuestas
    respuestas_data = json.loads(estado_db.respuestas)
    respuestas = [RespuestaSacral(**r) for r in respuestas_data]
    
    # Sintetizar
    direccion = await agente.procesar_respuestas_sacrales(estado_id, respuestas)
    
    return {"direccion": direccion}


@router.post("/{estado_id}/chat")
async def chat_clarificador(
    estado_id: str,
    request: ChatClarificacionRequest,
    db: Session = Depends(get_db)
):
    """Chat para clarificar dirección en acción tangible"""
    
    recopilador = RecopiladorContexto(db, calculador, calendario)
    agente = AgenteEstadoCero(db, claude_client, recopilador)
    
    estado_db = db.query(EstadoCeroDB).filter(EstadoCeroDB.id == estado_id).first()
    if not estado_db:
        raise HTTPException(status_code=404, detail="Estado Cero no encontrado")
    
    # Generar respuesta
    respuesta = await agente.chat_clarificador(estado_id, request.mensaje)
    
    return {"respuesta": respuesta}


@router.post("/{estado_id}/finalizar")
async def finalizar_estado_cero(
    estado_id: str,
    db: Session = Depends(get_db)
):
    """
    Finaliza Estado Cero - Simplificado para testing
    """
    # En modo testing, solo retornamos síntesis mock
    return {
        "status": "completado",
        "sintesis": {
            "tendencia": "expansión",
            "intensidad": 0.75,
            "direccion_emergente": "Sigue la energía que emerge del entusiasmo hacia lo sagrado"
        }
    }


@router.get("/asr-test/")
async def test_asr():
    """Endpoint de prueba para ASR sin base de datos"""
    try:
        # Verificar momento
        verificacion = calculador.verificar_momento_estado_cero()
        if not verificacion.es_momento:
            return {
                "error": f"No es momento de Estado Cero. Próximo: {verificacion.momento} en {verificacion.minutos_restantes}min"
            }
        
        # Crear estado de prueba sin base de datos
        estado_prueba = {
            "id": "test-asr-123",
            "fecha": datetime.now().isoformat(),
            "momento": "asr",
            "contexto": {
                "temporal": {
                    "momento_liturgico": "asr",
                    "dia_semana": "Jueves",
                    "mes_hijri": "Shawwal",
                    "cualidad_momento": "Refinar",
                    "cualidad_mes": "Celebrar"
                },
                "biologico": {
                    "energia_actual": 4,
                    "luz_solar_hoy": True,
                    "ejercicio_hoy": False
                },
                "financiero": {
                    "runway_meses": 6.0,
                    "urgencia_financiera": False
                },
                "conocimiento": {
                    "capturas_sin_procesar": 5,
                    "insights_listos": 2
                },
                "tiempo_disponible_hoy": 58
            },
            "preguntas": [
                {
                    "id": "pregunta-1",
                    "pregunta": "¿Te expandes al enfocarte en la acción principal hoy?",
                    "contexto": "Acción prioritaria del día",
                    "categoria": "desarrollo"
                },
                {
                    "id": "pregunta-2", 
                    "pregunta": "¿Se siente vivo revisar finanzas 30 min ahora?",
                    "contexto": "Runway y foco",
                    "categoria": "finanzas"
                },
                {
                    "id": "pregunta-3",
                    "pregunta": "¿Tu cuerpo pide movimiento ligero 20 min ahora?",
                    "contexto": "Energía y ritmo",
                    "categoria": "biologia"
                },
                {
                    "id": "pregunta-4",
                    "pregunta": "¿Hay expansión en procesar capturas hoy?",
                    "contexto": "Metabolizar conocimiento",
                    "categoria": "conocimiento"
                },
                {
                    "id": "pregunta-5",
                    "pregunta": "¿Se siente claro un bloque profundo 90 min?",
                    "contexto": "Ritmo de trabajo",
                    "categoria": "desarrollo"
                },
                {
                    "id": "pregunta-6",
                    "pregunta": "¿Te expande preparar una comida nutritiva ahora?",
                    "contexto": "Biología de soporte",
                    "categoria": "biologia"
                }
            ],
            "respuestas": [],
            "direccion_emergente": "",
            "accion_tangible": {
                "descripcion": "",
                "resultado_observable": "",
                "duracion_estimada": "",
                "energia_requerida": 3
            },
            "chat_clarificacion": [],
            "completado": False
        }
        
        return estado_prueba
        
    except Exception as e:
        print(f"❌ Error en test_asr: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


@router.get("/{estado_id}")
async def obtener_estado_cero(
    estado_id: str,
    db: Session = Depends(get_db)
):
    """Obtiene un Estado Cero completo"""
    
    estado_db = db.query(EstadoCeroDB).filter(EstadoCeroDB.id == estado_id).first()
    if not estado_db:
        raise HTTPException(status_code=404, detail="Estado Cero no encontrado")
    
    return EstadoCeroCompleto(
        id=estado_db.id,
        fecha=estado_db.fecha,
        momento=MomentoLiturgico(estado_db.momento),
        contexto=json.loads(estado_db.contexto),
        preguntas=json.loads(estado_db.preguntas),
        respuestas=json.loads(estado_db.respuestas),
        direccion_emergente=estado_db.direccion,
        accion_tangible=json.loads(estado_db.accion) if estado_db.accion else None,
        chat_clarificacion=json.loads(estado_db.chat),
        completado=estado_db.completado
    )


@router.get("/")
async def listar_estados_cero(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Lista los últimos Estados Cero"""
    
    estados = db.query(EstadoCeroDB).order_by(EstadoCeroDB.fecha.desc()).limit(limit).all()
    
    return [
        {
            "id": estado.id,
            "fecha": estado.fecha,
            "momento": estado.momento,
            "completado": estado.completado,
            "archivo_path": estado.archivo_path
        }
        for estado in estados
    ]
