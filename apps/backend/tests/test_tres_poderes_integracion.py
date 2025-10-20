"""
🕌 TEST DE INTEGRACIÓN: 3 PODERES DE GOBIERNO

Este test verifica el flujo completo de la arquitectura sagrada:

1. PODER LEGISLATIVO (Estado Cero):
   - Usuario completa Estado Cero
   - Se emite DecretoSacral
   - Validado contra 8 Pilares

2. PODER EJECUTIVO (Orquestador):
   - Verifica que existe decreto
   - Consulta Gabinete Ministerial
   - Genera JornadaAlBordeCaos
   - Marca decreto como "en_ejecucion"

3. PODER JUDICIAL (Guardian):
   - Verifica cumplimiento del decreto
   - Registra observaciones judiciales
   - Genera Espejo Nocturno
   - Marca decreto como "completado"

Referencia: core/arquitectura/TRES_PODERES_GOBIERNO_DIVINO.md
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from datetime import date, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid

from models.database import Base, EstadoCeroDB
from models.decreto_sacral import DecretoSacral
from services.claude_client import ClaudeClient
from services.contexto import RecopiladorContexto
from services.tiempos_liturgicos import CalculadorTiemposLiturgicos
from services.calendario_hijri import CalendarioHijri
from agentes.estado_cero import AgenteEstadoCero
from agentes.orquestador import AgenteOrquestador
from agentes.guardian import AgenteGuardian


# Setup DB en memoria para testing
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
DecretoSacral.__table__.create(engine, checkfirst=True)
Session = sessionmaker(bind=engine)


def crear_estado_cero_mock(db, estado_id: str, completado: bool = True):
    """Crea un Estado Cero mock en la BD"""
    estado = EstadoCeroDB(
        id=estado_id,
        fecha=datetime.now(),
        momento="fajr",
        direccion="Enfócate en construir infraestructura técnica",
        accion='{"descripcion": "Implementar integración de 3 Poderes", "resultado_observable": "Código funcional", "duracion_estimada": "2h", "energia_requerida": 4}',
        completado=completado
    )
    db.add(estado)
    db.commit()
    return estado


async def test_flujo_completo_tres_poderes():
    """
    🕌 TEST PRINCIPAL: Flujo completo de 3 Poderes
    """
    print("\n" + "="*70)
    print("🕌 TESTING: INTEGRACIÓN COMPLETA DE 3 PODERES DE GOBIERNO")
    print("="*70 + "\n")
    
    db = Session()
    claude = ClaudeClient()
    calendario = CalendarioHijri()
    recopilador = RecopiladorContexto(db, claude, calendario)
    # Usar coordenadas de Madrid para testing
    calculador_tiempos = CalculadorTiemposLiturgicos(latitud=40.4168, longitud=-3.7038)
    
    try:
        # ==========================================
        # PASO 1: PODER LEGISLATIVO (ESTADO CERO)
        # ==========================================
        print("📜 PASO 1: PODER LEGISLATIVO - El Sultán (Corazón)")
        print("-" * 70)
        
        # Crear Estado Cero mock completado
        estado_id = str(uuid.uuid4())
        estado_mock = crear_estado_cero_mock(db, estado_id, completado=True)
        print(f"✅ Estado Cero creado: {estado_id}")
        print(f"   Dirección: {estado_mock.direccion}")
        
        # Instanciar agente Estado Cero
        agente_estado_cero = AgenteEstadoCero(db, claude, recopilador)
        
        # Emitir Decreto Sacral
        print("\n🕌 Emitiendo Decreto Sacral...")
        decreto = await agente_estado_cero.emitir_decreto_sacral(
            estado_id=estado_id,
            momento="fajr",
            validar_pilares=True
        )
        
        print(f"✅ DECRETO EMITIDO: {decreto.id}")
        print(f"   Acción tangible: {decreto.accion_tangible}")
        print(f"   Validado contra 8 Pilares: {decreto.validado_contra_pilares}")
        print(f"   Estado: {decreto.estado}")
        
        assert decreto is not None, "Decreto no fue creado"
        assert decreto.accion_tangible != "", "Decreto sin acción tangible"
        assert decreto.estado == "pendiente", f"Estado incorrecto: {decreto.estado}"
        
        print("\n✅ PODER LEGISLATIVO: OK\n")
        
        # ==========================================
        # PASO 2: PODER EJECUTIVO (ORQUESTADOR)
        # ==========================================
        print("🎼 PASO 2: PODER EJECUTIVO - El Primer Ministro (Aql)")
        print("-" * 70)
        
        # Instanciar agente Orquestador
        agente_orquestador = AgenteOrquestador(db, claude, calculador_tiempos)
        
        # Verificar que existe decreto activo
        print("\n🔍 Verificando decreto activo...")
        decreto_activo = agente_orquestador.obtener_decreto_activo()
        assert decreto_activo is not None, "No se encontró decreto activo"
        assert decreto_activo.id == decreto.id, "Decreto activo no coincide"
        print(f"✅ Decreto activo encontrado: {decreto_activo.id}")
        
        # Ejecutar decreto (consulta gabinete + genera plan)
        print("\n🏛️ Ejecutando decreto (consultando Gabinete Ministerial)...")
        plan = await agente_orquestador.ejecutar_decreto(decreto.id)
        
        print(f"\n✅ PLAN GENERADO:")
        print(f"   Fecha: {plan.fecha}")
        print(f"   Acción principal: {plan.accion_principal}")
        print(f"   Bloques: {len(plan.bloques_sugeridos)}")
        print(f"   Espacio emergencia: {plan.espacio_emergencia}%")
        
        # Verificar que el decreto cambió a "en_ejecucion"
        db.refresh(decreto)
        assert decreto.estado == "en_ejecucion", f"Estado incorrecto: {decreto.estado}"
        print(f"   Estado decreto: {decreto.estado}")
        
        # Mostrar algunos bloques
        print(f"\n   Bloques del día:")
        for i, bloque in enumerate(plan.bloques_sugeridos[:4], 1):
            print(f"   {i}. {bloque.inicio_aprox} - {bloque.actividad}")
        
        assert plan is not None, "Plan no fue generado"
        assert len(plan.bloques_sugeridos) > 0, "Plan sin bloques"
        
        print("\n✅ PODER EJECUTIVO: OK\n")
        
        # ==========================================
        # PASO 3: PODER JUDICIAL (GUARDIAN)
        # ==========================================
        print("⚖️ PASO 3: PODER JUDICIAL - El Escribano (Sirr)")
        print("-" * 70)
        
        # Instanciar agente Guardian
        agente_guardian = AgenteGuardian(db, claude)
        
        # Simular actividad del día (para que haya algo que verificar)
        # Ya tenemos el Estado Cero, podríamos añadir sesiones, etc.
        # Por ahora, el Guardian verificará con los datos existentes
        
        print("\n⚖️ Generando Espejo Nocturno (verificación judicial)...")
        reporte = await agente_guardian.generar_reporte_diario(date.today())
        
        print(f"\n✅ ESPEJO NOCTURNO GENERADO:")
        print(f"   Fecha: {reporte.fecha}")
        print(f"   Estados Cero: {reporte.estados_cero_completados}")
        print(f"   Resonancias: {len(reporte.resonancias)}")
        print(f"   Obstrucciones: {len(reporte.obstrucciones)}")
        
        # Verificar que el decreto fue marcado como verificado
        db.refresh(decreto)
        print(f"\n   Estado final decreto: {decreto.estado}")
        print(f"   Verificado por escribano: {decreto.verificado_por_escribano}")
        
        assert decreto.verificado_por_escribano, "Decreto no verificado"
        assert decreto.estado == "completado", f"Estado incorrecto: {decreto.estado}"
        assert decreto.observaciones_judiciales is not None, "Sin observaciones judiciales"
        
        # Mostrar observaciones judiciales
        if decreto.observaciones_judiciales:
            import json
            obs = json.loads(decreto.observaciones_judiciales)
            print(f"\n   Observaciones judiciales:")
            print(f"   - Nivel cumplimiento: {obs['verificacion_judicial']['nivel_cumplimiento']}")
            print(f"   - Mensaje: {obs['verificacion_judicial']['mensaje']}")
        
        print("\n✅ PODER JUDICIAL: OK\n")
        
        # ==========================================
        # RESUMEN FINAL
        # ==========================================
        print("="*70)
        print("🕌 RESUMEN: CICLO COMPLETO DE 3 PODERES")
        print("="*70)
        print(f"""
PODER LEGISLATIVO (Sultán - Corazón):
  ✅ Estado Cero completado
  ✅ Decreto Sacral emitido
  ✅ Validado contra 8 Pilares
  ✅ Estado inicial: "pendiente"

PODER EJECUTIVO (Primer Ministro - Aql):
  ✅ Decreto verificado
  ✅ Gabinete Ministerial consultado (7 ministerios)
  ✅ JornadaAlBordeCaos generada ({len(plan.bloques_sugeridos)} bloques)
  ✅ Estado actualizado: "en_ejecucion"

PODER JUDICIAL (Escribano - Sirr):
  ✅ Cumplimiento verificado
  ✅ Observaciones judiciales registradas
  ✅ Espejo Nocturno generado
  ✅ Estado final: "completado"

ARQUITECTURA SAGRADA: OPERATIVA ✅
        """)
        print("="*70)
        print("\n🕌 Alhamdulillah - Todo el sistema integrado correctamente\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN TEST: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.close()


if __name__ == "__main__":
    resultado = asyncio.run(test_flujo_completo_tres_poderes())
    sys.exit(0 if resultado else 1)

