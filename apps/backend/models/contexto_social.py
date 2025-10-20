"""
🤝 Contexto Social - Capa 2 (Social/Relacional)

Modela el contexto social y relacional del usuario:
- No-negociables (compromisos ineludibles)
- Proyectos activos
- Tensiones sociales/relacionales
- Compromisos del día

Principio: El contexto social no es ruido, es textura.
La Capa 2 reconoce que somos seres en relación.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime, date
from enum import Enum
from pathlib import Path
import json


class TipoNoNegociable(str, Enum):
    """Tipos de no-negociables"""
    BIOLOGICO = "biologico"          # Sueño, comida, ejercicio
    ESPIRITUAL = "espiritual"        # Estados Cero, práctica
    FINANCIERO = "financiero"        # Trabajo, clientes
    SOCIAL = "social"                # Familia, comunidad
    CREATIVO = "creativo"            # Proyectos creativos
    APRENDIZAJE = "aprendizaje"      # Estudio, investigación


class EstadoProyecto(str, Enum):
    """Estado de un proyecto"""
    ACTIVO = "activo"
    PAUSADO = "pausado"
    COMPLETADO = "completado"
    ARCHIVADO = "archivado"


class NoNegociable(BaseModel):
    """
    Compromiso ineludible del usuario.

    Los no-negociables son anclas del día que NO se negocian.
    """

    nombre: str = Field(
        ...,
        description="Nombre del no-negociable"
    )

    tipo: TipoNoNegociable = Field(
        ...,
        description="Categoría del no-negociable"
    )

    dias_semana: List[str] = Field(
        ...,
        description="Días en que aplica (ej: ['lunes', 'miércoles', 'viernes'])"
    )

    hora_preferida: Optional[str] = Field(
        None,
        description="Hora preferida (ej: '07:00')"
    )

    duracion_minutos: int = Field(
        ...,
        ge=1,
        description="Duración estimada en minutos"
    )

    ventana_flexible: bool = Field(
        default=False,
        description="¿Puede moverse dentro del día?"
    )

    prioridad: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Prioridad 1 (baja) a 5 (crítica)"
    )

    razon: Optional[str] = Field(
        None,
        max_length=200,
        description="Por qué es no-negociable"
    )


class Proyecto(BaseModel):
    """
    Proyecto activo del usuario.
    """

    nombre: str = Field(
        ...,
        description="Nombre del proyecto"
    )

    tipo: str = Field(
        ...,
        description="Tipo (código, escritura, diseño, investigación, etc.)"
    )

    estado: EstadoProyecto = Field(
        default=EstadoProyecto.ACTIVO,
        description="Estado actual"
    )

    prioridad: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Prioridad 1 (baja) a 5 (crítica)"
    )

    horas_semanales_deseadas: Optional[int] = Field(
        None,
        description="Horas que se quieren dedicar por semana"
    )

    deadline: Optional[date] = Field(
        None,
        description="Fecha límite (si existe)"
    )

    hitos: List[str] = Field(
        default_factory=list,
        description="Hitos o tareas clave"
    )

    notas: Optional[str] = Field(
        None,
        max_length=500
    )


class TensionSocial(BaseModel):
    """
    Tensión o conflicto social/relacional.

    Las tensiones NO son malas, son información.
    """

    descripcion: str = Field(
        ...,
        max_length=200,
        description="Descripción breve de la tensión"
    )

    ambito: str = Field(
        ...,
        description="Ámbito (familia, trabajo, amistad, pareja, etc.)"
    )

    intensidad: int = Field(
        ...,
        ge=1,
        le=5,
        description="Intensidad de la tensión (1=leve, 5=crítica)"
    )

    requiere_atencion_hoy: bool = Field(
        default=False,
        description="¿Requiere atención hoy?"
    )

    accion_posible: Optional[str] = Field(
        None,
        max_length=200,
        description="Acción que podría resolver/aliviar"
    )

    timestamp: datetime = Field(
        default_factory=datetime.now
    )


class ContextoSocial(BaseModel):
    """
    Contexto social completo del usuario.

    Este es el snapshot de la Capa 2 para un momento dado.
    """

    # === NO-NEGOCIABLES DEL DÍA ===
    no_negociables_hoy: List[NoNegociable] = Field(
        default_factory=list,
        description="No-negociables que aplican hoy"
    )

    # === PROYECTOS ACTIVOS ===
    proyectos_activos: List[Proyecto] = Field(
        default_factory=list,
        description="Proyectos en estado activo"
    )

    # === TENSIONES ===
    tensiones_actuales: List[TensionSocial] = Field(
        default_factory=list,
        description="Tensiones sociales/relacionales actuales"
    )

    # === COMPROMISOS DEL DÍA ===
    compromisos_externos: List[str] = Field(
        default_factory=list,
        description="Compromisos externos del día (reuniones, citas, etc.)"
    )

    # === METADATA ===
    fecha: date = Field(
        default_factory=date.today,
        description="Fecha del contexto"
    )

    dia_semana: str = Field(
        default_factory=lambda: datetime.now().strftime("%A").lower()
    )

    # === MÉTODOS ===

    def esta_activa(self) -> bool:
        """
        Determina si la capa social está 'activa' (relevante para este momento).

        Returns:
            True si hay no-negociables, proyectos activos, o tensiones intensas
        """
        tiene_no_negociables = len(self.no_negociables_hoy) > 0
        tiene_proyectos = len(self.proyectos_activos) > 0
        tiene_tensiones_intensas = any(
            t.intensidad >= 4 for t in self.tensiones_actuales
        )

        return tiene_no_negociables or tiene_proyectos or tiene_tensiones_intensas

    def generar_sintesis(self) -> str:
        """
        Genera síntesis textual del contexto social.

        Returns:
            Descripción del contexto social
        """
        partes = []

        if self.no_negociables_hoy:
            nn_nombres = [nn.nombre for nn in self.no_negociables_hoy[:2]]
            partes.append(f"no-negociables: {', '.join(nn_nombres)}")

        if self.proyectos_activos:
            proy_nombres = [p.nombre for p in self.proyectos_activos[:2]]
            partes.append(f"proyectos: {', '.join(proy_nombres)}")

        if self.tensiones_actuales:
            tensiones_intensas = [
                t for t in self.tensiones_actuales
                if t.intensidad >= 4
            ]
            if tensiones_intensas:
                partes.append(f"{len(tensiones_intensas)} tensiones intensas")

        if self.compromisos_externos:
            partes.append(f"{len(self.compromisos_externos)} compromisos externos")

        return ", ".join(partes) if partes else "Sin compromisos sociales significativos"

    def obtener_proyectos_prioritarios(self, top_n: int = 3) -> List[Proyecto]:
        """
        Obtiene proyectos más prioritarios.

        Args:
            top_n: Número de proyectos a retornar

        Returns:
            Lista de proyectos ordenados por prioridad
        """
        proyectos_ordenados = sorted(
            self.proyectos_activos,
            key=lambda p: p.prioridad,
            reverse=True
        )
        return proyectos_ordenados[:top_n]


# === FUNCIONES PÚBLICAS ===

def cargar_contexto_social_desde_config(
    config_path: Path,
    fecha: Optional[date] = None
) -> ContextoSocial:
    """
    Carga contexto social desde archivo de configuración.

    Args:
        config_path: Ruta al archivo de configuración
        fecha: Fecha para la que se carga el contexto (default: hoy)

    Returns:
        ContextoSocial cargado desde config
    """
    if fecha is None:
        fecha = date.today()

    dia_semana = fecha.strftime("%A").lower()

    contexto = ContextoSocial(
        fecha=fecha,
        dia_semana=dia_semana
    )

    if not config_path.exists():
        return contexto

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Cargar no-negociables
        if "no_negociables" in config:
            for nn_data in config["no_negociables"]:
                nn = NoNegociable(**nn_data)
                # Filtrar por día de la semana
                if dia_semana in [d.lower() for d in nn.dias_semana]:
                    contexto.no_negociables_hoy.append(nn)

        # Cargar proyectos activos
        if "proyectos" in config:
            for proy_data in config["proyectos"]:
                proy = Proyecto(**proy_data)
                if proy.estado == EstadoProyecto.ACTIVO:
                    contexto.proyectos_activos.append(proy)

        # Cargar tensiones
        if "tensiones_sociales" in config:
            for tension_data in config["tensiones_sociales"]:
                tension = TensionSocial(**tension_data)
                contexto.tensiones_actuales.append(tension)

    except Exception as e:
        print(f"⚠️ Error cargando contexto social: {e}")

    return contexto


if __name__ == "__main__":
    # Test
    print("🤝 CONTEXTO SOCIAL - Test\n")
    print("=" * 70)

    # Test 1: Crear no-negociable
    nn1 = NoNegociable(
        nombre="Entrenamiento de fuerza",
        tipo=TipoNoNegociable.BIOLOGICO,
        dias_semana=["lunes", "miércoles", "viernes"],
        hora_preferida="07:00",
        duracion_minutos=60,
        prioridad=5,
        razon="Salud física y mental"
    )

    print(f"\n📋 NO-NEGOCIABLE:")
    print(f"   {nn1.nombre}")
    print(f"   Días: {', '.join(nn1.dias_semana)}")
    print(f"   Prioridad: {nn1.prioridad}/5")

    # Test 2: Crear proyecto
    proy1 = Proyecto(
        nombre="Campo Sagrado MVP",
        tipo="código",
        estado=EstadoProyecto.ACTIVO,
        prioridad=5,
        horas_semanales_deseadas=20,
        hitos=["Implementar 7 capas", "Integrar frontend", "Testing completo"]
    )

    print(f"\n\n💼 PROYECTO:")
    print(f"   {proy1.nombre}")
    print(f"   Estado: {proy1.estado.value}")
    print(f"   Prioridad: {proy1.prioridad}/5")
    print(f"   Hitos: {len(proy1.hitos)}")

    # Test 3: Crear tensión social
    tension1 = TensionSocial(
        descripcion="Conversación pendiente con familia",
        ambito="familia",
        intensidad=3,
        requiere_atencion_hoy=False
    )

    print(f"\n\n⚡ TENSIÓN SOCIAL:")
    print(f"   {tension1.descripcion}")
    print(f"   Ámbito: {tension1.ambito}")
    print(f"   Intensidad: {tension1.intensidad}/5")

    # Test 4: Contexto social completo
    contexto = ContextoSocial(
        no_negociables_hoy=[nn1],
        proyectos_activos=[proy1],
        tensiones_actuales=[tension1]
    )

    print(f"\n\n📊 CONTEXTO SOCIAL COMPLETO:")
    print(f"   {contexto.generar_sintesis()}")
    print(f"   ¿Activa?: {contexto.esta_activa()}")

    proyectos_prioritarios = contexto.obtener_proyectos_prioritarios(top_n=1)
    print(f"   Proyecto prioritario: {proyectos_prioritarios[0].nombre}")

    print("\n" + "=" * 70)
    print("✅ Capa 2 (Social) implementada correctamente")
