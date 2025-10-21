from datetime import datetime, date
from typing import List, Dict, Optional
import uuid
import json
from sqlalchemy.orm import Session

from models.schemas import (
    MomentoLiturgico, ContextoCompleto, PreguntaBinaria,
    RespuestaSacral, AccionConcreta, MensajeChat,
    EstadoCeroCompleto, SensacionSacral
)
from models.database import EstadoCeroDB
from models.decreto_sacral import DecretoSacral  # 🏛️ Arquitectura Sagrada
from services.claude_client import ClaudeClient
from services.contexto import RecopiladorContexto
from services.verificador_pilares import obtener_verificador  # 🏛️ Arquitectura Sagrada
# from services.sumario_contexto import GestorSumarioContexto  # Archivado en Phase 3
# from services.motor_prisma import cargar_prisma_y_configurar  # Archivado en Phase 3

# Importar el entrelazador para recomendaciones personalizadas
try:
    # from agentes.entrelazador import agente_entrelazador  # Archivado en Phase 2
    ENTRELAZADOR_DISPONIBLE = True
except:
    ENTRELAZADOR_DISPONIBLE = False

# Cargar configuración del prisma (archivado en Phase 3, usar config estática)
# motor_prisma_global = cargar_prisma_y_configurar()
# CONFIG_PRISMA = motor_prisma_global.configurar_estado_cero() if motor_prisma_global else None
CONFIG_PRISMA = None  # MVP usa configuración estática


class AgenteEstadoCero:
    """
    🕌 AGENTE ESTADO CERO - El Sultán (Qalb/Corazón)
    
    PODER LEGISLATIVO del gobierno del reino humano.
    
    Responsabilidades:
    - Facilitar consulta sacral profunda
    - RECIBIR dirección emergente
    - EMITIR decreto claro (DecretoSacral)
    - Validar contra 8 Pilares
    
    Arquitectura Sagrada:
    - Parte de los 3 Poderes de Gobierno
    - Precede al Ejecutivo (Orquestador)
    - Sus decretos son ley para el reino
    
    Referencia: core/arquitectura/TRES_PODERES_GOBIERNO_DIVINO.md
    """
    
    def __init__(self, db: Session, claude: ClaudeClient, recopilador: RecopiladorContexto):
        self.db = db
        self.claude = claude
        self.recopilador = recopilador
        # self.gestor_sumario = GestorSumarioContexto(db, claude)  # Archivado
        self.verificador_pilares = obtener_verificador()  # 🏛️ Arquitectura Sagrada
        
    async def iniciar_consulta(
        self,
        momento: MomentoLiturgico,
        usuario_id: str = "default",
        energia: Optional[int] = None,
        calidad_sueno: Optional[int] = None,
        resonancia_corporal: Optional[str] = None,
        estado_emocional: Optional[str] = None,
        intensidad_emocional: Optional[int] = None
    ) -> EstadoCeroCompleto:
        """Proceso completo de consulta sacral con parámetros opcionales de 7 capas"""

        # 1. Recopilar contexto holístico (pasamos los parámetros de 7 capas)
        contexto = await self.recopilador.recopilar_contexto_completo(
            momento,
            energia=energia,
            calidad_sueno=calidad_sueno,
            resonancia_corporal=resonancia_corporal,
            estado_emocional=estado_emocional,
            intensidad_emocional=intensidad_emocional
        )
        
        # 2. Formular preguntas binarias
        preguntas = await self.formular_preguntas_sacrales(contexto)
        
        # Retorna estado inicial - el usuario responderá las preguntas
        estado_id = str(uuid.uuid4())
        
        return EstadoCeroCompleto(
            id=estado_id,
            fecha=datetime.now(),
            momento=momento,
            contexto=contexto,
            preguntas=preguntas,
            respuestas=[],
            direccion_emergente="",
            accion_tangible=AccionConcreta(
                descripcion="",
                resultado_observable="",
                duracion_estimada="",
                energia_requerida=3
            ),
            chat_clarificacion=[],
            completado=False
        )
    
    async def formular_preguntas_sacrales(
        self,
        contexto: ContextoCompleto
    ) -> List[PreguntaBinaria]:
        """
        🔺 LEY DEL TRES: Genera 3 preguntas alineadas con las 3 fuerzas fundamentales
        
        1. FUERZA ACTIVA (Afirmativa/Expansiva) - ¿Qué quiere emerger?
        2. FUERZA PASIVA (Receptiva/Restrictiva) - ¿Qué necesita ser honrado?
        3. FUERZA NEUTRALIZADORA (Reconciliadora) - ¿Cuál es el siguiente paso concreto?
        
        Esto honra los 3 Poderes de Gobierno, los 3 Centros, y la Ley del Tres de Gurdjieff.
        """
        momento = contexto.temporal.momento_liturgico.value
        energia = contexto.biologico.energia_actual
        
        try:
            # Usar Claude para generar 3 preguntas contextuales basadas en la Ley del Tres
            prompt = f"""Eres el Sultán del Campo Sagrado, formulando una consulta sacral en el momento litúrgico de {momento}.

CONTEXTO:
- Momento: {momento}
- Energía actual: {energia}/5
- Día: {contexto.temporal.dia_semana}
- Mes Hijri: {contexto.temporal.mes_hijri}

TAREA:
Genera EXACTAMENTE 3 preguntas binarias (respuesta SÍ/NO) siguiendo la LEY DEL TRES:

1. FUERZA ACTIVA (Expansión): Pregunta sobre lo que quiere EMERGER o manifestarse ahora
2. FUERZA PASIVA (Receptividad): Pregunta sobre lo que necesita ser HONRADO o respetado
3. FUERZA NEUTRALIZADORA (Acción): Pregunta sobre el PASO CONCRETO a tomar hoy

ESTILO:
- Profundas pero claras
- Conectadas al cuerpo (autoridad sacral)
- Específicas al momento actual
- Respetando el contexto energético

Retorna SOLO las 3 preguntas en formato JSON:
{{
  "preguntas": [
    {{"texto": "pregunta 1 (fuerza activa)", "fuerza": "activa"}},
    {{"texto": "pregunta 2 (fuerza pasiva)", "fuerza": "pasiva"}},
    {{"texto": "pregunta 3 (fuerza neutralizadora)", "fuerza": "neutralizadora"}}
  ]
}}"""

            # Llamar a Claude
            respuesta = await self.claude.generar_texto(
                prompt=prompt,
                max_tokens=800,
                temperature=0.8
            )
            
            # Parsear respuesta JSON
            import json
            try:
                data = json.loads(respuesta)
                preguntas_raw = data.get("preguntas", [])
            except:
                # Si falla JSON, extraer preguntas del texto
                preguntas_raw = [
                    {"texto": line.split(". ", 1)[1] if ". " in line else line, "fuerza": "activa"}
                    for line in respuesta.split("\n") 
                    if line.strip() and any(c in line for c in ["?", "¿"])
                ][:3]
            
            # Convertir a formato PreguntaBinaria
            preguntas = []
            fuerzas_labels = {
                "activa": "🔺 Fuerza Activa",
                "pasiva": "🔻 Fuerza Pasiva", 
                "neutralizadora": "⚖️ Fuerza Neutralizadora"
            }
            
            for i, p in enumerate(preguntas_raw[:3]):  # Asegurar máximo 3
                fuerza = p.get("fuerza", ["activa", "pasiva", "neutralizadora"][i])
                preguntas.append(PreguntaBinaria(
                    id=f"p{i+1}",
                    pregunta=p.get("texto", p.get("pregunta", "Pregunta no disponible")),
                    contexto=fuerzas_labels.get(fuerza, "Ley del Tres"),
                    categoria=momento
                ))
            
            # Si no se generaron 3, completar con fallback
            while len(preguntas) < 3:
                idx = len(preguntas)
                fallbacks = [
                    "¿Tu cuerpo se expande al seguir la dirección que emerge de este momento?",
                    "¿Hay algo que necesite ser honrado antes de actuar?",
                    "¿El siguiente paso es claro y tangible?"
                ]
                preguntas.append(PreguntaBinaria(
                    id=f"p{idx+1}",
                    pregunta=fallbacks[idx],
                    contexto=f"Ley del Tres - Pregunta {idx+1}",
                    categoria=momento
                ))
            
            return preguntas[:3]  # Exactamente 3 preguntas
            
        except Exception as e:
            print(f"⚠️ Error generando 3 preguntas: {e}")
            import traceback
            traceback.print_exc()

            # Fallback: 3 preguntas genéricas basadas en Ley del Tres
            return [
                PreguntaBinaria(
                    id="p1",
                    pregunta="¿Tu cuerpo se expande al seguir la dirección que emerge de este momento?",
                    contexto="🔺 Fuerza Activa - Emergencia",
                    categoria=momento
                ),
                PreguntaBinaria(
                    id="p2",
                    pregunta="¿Hay límites o compromisos que necesitan ser honrados primero?",
                    contexto="🔻 Fuerza Pasiva - Receptividad",
                    categoria=momento
                ),
                PreguntaBinaria(
                    id="p3",
                    pregunta="¿El siguiente paso concreto está claro y alineado?",
                    contexto="⚖️ Fuerza Neutralizadora - Acción",
                    categoria=momento
                )
            ]
    
    def _generar_preguntas_genericas(self, contexto) -> list:
        """Genera preguntas genéricas como fallback"""
        return [
            {
                "id": "p1",
                "pregunta": "¿Tu cuerpo se expande al pensar en trabajar en tu proyecto principal hoy?",
                "contexto": "Dirección y enfoque",
                "categoria": "desarrollo"
            },
            {
                "id": "p2",
                "pregunta": "¿Sientes expansión al priorizar ingresos en las próximas semanas?",
                "contexto": "Finanzas y urgencia",
                "categoria": "finanzas"
            },
            {
                "id": "p3",
                "pregunta": "¿Tu cuerpo dice sí a dedicar tiempo de aprendizaje hoy?",
                "contexto": "Conocimiento y crecimiento",
                "categoria": "conocimiento"
            },
            {
                "id": "p4",
                "pregunta": "¿Sientes expansión al conectar con alguien importante hoy?",
                "contexto": "Relaciones y comunidad",
                "categoria": "relaciones"
            },
            {
                "id": "p5",
                "pregunta": "¿Tu cuerpo se expande al pensar en cuidar tu salud hoy?",
                "contexto": "Biología y energía",
                "categoria": "biologia"
            },
            {
                "id": "p6",
                "pregunta": "¿Sientes contracción al seguir como hasta ahora?",
                "contexto": "Reflexión y cambio",
                "categoria": "espiritualidad"
            }
        ]
    
    async def procesar_respuestas_sacrales(
        self,
        estado_id: str,
        respuestas: List[RespuestaSacral]
    ) -> str:
        """
        Analiza las respuestas binarias y genera dirección emergente
        """
        
        # Guardar respuestas en BD
        estado_db = self.db.query(EstadoCeroDB).filter(EstadoCeroDB.id == estado_id).first()
        if estado_db:
            estado_db.respuestas = json.dumps([r.model_dump() for r in respuestas], default=str)
            self.db.commit()
        
        # Analizar patrones
        expansion = sum(1 for r in respuestas if r.sensacion == SensacionSacral.EXPANSION)
        contraccion = len(respuestas) - expansion
        
        # Generar dirección emergente - PROMPT OPTIMIZADO (compacto)
        # Convertir respuestas a formato simple
        resp_simple = "\n".join([
            f"{i+1}. {r.pregunta_id}: {'SÍ' if r.sensacion == SensacionSacral.EXPANSION else 'NO'} (intensidad {r.intensidad}/5)"
            for i, r in enumerate(respuestas)
        ])
        
        prompt = f"""Respuestas sacrales:
{resp_simple}
Expansión: {expansion}/3, Contracción: {contraccion}/3

Dirección emergente (1 línea, específica, accionable):"""

        messages = [{"role": "user", "content": prompt}]
        
        # Usar Sonnet para síntesis (es crítico, vale la pena)
        # Pero con max_tokens reducido
        direccion = await self.claude.generate("", messages, max_tokens=100)
        
        # Guardar dirección
        if estado_db:
            estado_db.direccion = direccion
            self.db.commit()
        
        return direccion
    
    async def chat_clarificador(
        self,
        estado_id: str,
        mensaje_usuario: str
    ) -> str:
        """
        Chat para clarificar dudas sobre la dirección emergente
        """
        
        # Obtener estado actual
        estado_db = self.db.query(EstadoCeroDB).filter(EstadoCeroDB.id == estado_id).first()
        if not estado_db:
            return "Estado no encontrado"
        
        # Construir contexto del chat
        contexto_chat = json.loads(estado_db.chat or "[]")
        contexto_chat.append({"role": "user", "content": mensaje_usuario})
        
        # Chat clarificador - PROMPT OPTIMIZADO
        prompt = f"""Dirección: {estado_db.direccion}
Duda: {mensaje_usuario}

Respuesta práctica y concreta (2-3 líneas):"""

        messages = [{"role": "user", "content": prompt}]
        
        # Usar Haiku para chat (respuesta simple)
        respuesta = await self.claude.generate_haiku("Chat clarificador sacral.", messages, max_tokens=150)
        
        # Guardar en chat
        contexto_chat.append({"role": "assistant", "content": respuesta})
        estado_db.chat = json.dumps(contexto_chat)
        self.db.commit()
        
        return respuesta
    
    async def definir_accion_tangible(
        self,
        estado_id: str,
        preferencias_usuario: Dict = None
    ) -> AccionConcreta:
        """
        Define acción concreta basada en dirección emergente + preferencias
        """
        
        estado_db = self.db.query(EstadoCeroDB).filter(EstadoCeroDB.id == estado_id).first()
        if not estado_db:
            return AccionConcreta(descripcion="Error", resultado_observable="", duracion_estimada="", energia_requerida=3)
        
        prompt = f"""Define una acción TANGIBLE basada en:

Dirección emergente: {estado_db.direccion}
Momento: {estado_db.momento}
Preferencias: {preferencias_usuario or {}}

La acción debe ser:
1. ESPECÍFICA y CONCRETA (no abstracta)
2. OBSERVABLE (se puede ver/medir el resultado)
3. REALIZABLE en el tiempo disponible
4. ALINEADA con la dirección sacral

FORMATO JSON:
{{
  "descripcion": "Acción específica a realizar",
  "resultado_observable": "Qué se verá cuando termine",
  "duracion_estimada": "Tiempo aproximado",
  "energia_requerida": 1-5
}}

Acción:"""

        messages = [{"role": "user", "content": prompt}]
        result = await self.claude.generate_json("", messages)
        
        accion = AccionConcreta(**result)
        
        # Guardar acción
        estado_db.accion = json.dumps(accion.model_dump())
        estado_db.completado = True
        self.db.commit()
        
        return accion
    
    async def emitir_decreto_sacral(
        self,
        estado_id: str,
        momento: str = "fajr",
        validar_pilares: bool = True
    ) -> DecretoSacral:
        """
        🕌 PODER LEGISLATIVO: Emite Decreto Sacral
        
        El Sultán (Corazón) EMITE decreto oficial que será
        ley para el Primer Ministro (Orquestador).
        
        Args:
            estado_id: ID del Estado Cero completado
            momento: Momento litúrgico (fajr, dhuhr, asr, maghrib, isha)
            validar_pilares: Si True, valida contra 8 Pilares
            
        Returns:
            DecretoSacral creado y guardado en DB
        """
        # 1. Obtener Estado Cero completado
        estado_db = self.db.query(EstadoCeroDB).filter(
            EstadoCeroDB.id == estado_id
        ).first()
        
        if not estado_db or not estado_db.completado:
            raise ValueError("Estado Cero no completado o no encontrado")
        
        # 2. Extraer dirección y acción
        direccion_emergente = estado_db.direccion or ""
        
        try:
            accion_data = json.loads(estado_db.accion or "{}")
            accion_tangible = accion_data.get("descripcion", "")
        except:
            accion_tangible = ""
        
        if not accion_tangible:
            raise ValueError("Acción tangible no definida")
        
        # 3. OPCIONAL: Validar contra 8 Pilares
        validado_pilares = False
        if validar_pilares:
            decision = {
                "accion_especifica": accion_tangible,
                "descripcion": direccion_emergente,
                "tipo": "creacion",  # Asumir que Estado Cero es generativo
                "comprende_implicaciones": True  # Usuario pasó por consulta sacral
            }
            
            verificacion = self.verificador_pilares.verificar_todos_pilares(decision)
            validado_pilares = verificacion["cumple_arquitectura"]
            
            # Log resultado de verificación
            print(f"🏛️ Verificación Pilares: Score {verificacion['score_global']:.1f}/100, "
                  f"Cumple: {validado_pilares}")
        
        # 4. Verificar que no existe decreto para hoy
        decreto_existente = self.db.query(DecretoSacral).filter(
            DecretoSacral.fecha == date.today(),
            DecretoSacral.estado.in_(["pendiente", "en_ejecucion"])
        ).first()
        
        if decreto_existente:
            # Ya hay decreto activo, retornarlo
            print(f"⚠️ Ya existe decreto activo para hoy: {decreto_existente.id}")
            return decreto_existente
        
        # 5. EMITIR DECRETO SACRAL
        decreto = DecretoSacral(
            fecha=date.today(),
            momento_liturgico=momento,
            direccion_emergente=direccion_emergente,
            accion_tangible=accion_tangible,
            validado_contra_pilares=validado_pilares,
            estado="pendiente"
        )
        
        self.db.add(decreto)
        self.db.commit()
        self.db.refresh(decreto)
        
        print(f"🕌 DECRETO SACRAL EMITIDO: {decreto.id}")
        print(f"   Acción: {accion_tangible}")
        print(f"   Validado contra 8 Pilares: {validado_pilares}")
        
        return decreto
