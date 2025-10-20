"""
🔧 API - Configuración Individual
================================

Endpoints para gestionar la configuración personalizada de cada usuario
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from models.database import get_db
from pydantic import BaseModel


router = APIRouter()


# ==================== SCHEMAS ====================

class NoNegociables(BaseModel):
    """No-negociables del usuario"""
    fajr_estado_cero: bool = True
    dhuhr_estado_cero: bool = True
    asr_estado_cero: bool = False
    maghrib_validacion: bool = True
    isha_estado_cero: bool = False


class ContextoFinanciero(BaseModel):
    """Contexto financiero del usuario"""
    runway_meses: int
    urgencia: bool


class ContextoBiologico(BaseModel):
    """Contexto biológico del usuario"""
    patron_sueno: str  # "regular", "irregular", "insomnio"
    nivel_energia: int  # 1-5
    ejercicio_regular: bool


class ConfiguracionIndividual(BaseModel):
    """Configuración completa del usuario"""
    user_id: str = "default"  # Por ahora un solo usuario
    no_negociables: NoNegociables
    dimensiones_prioritarias: list[str]  # ['finanzas', 'desarrollo', ...]
    energia_disponible: int  # 1-5
    contexto_financiero: ContextoFinanciero
    contexto_biologico: ContextoBiologico
    expresion_libre: Optional[str] = None


class ConfiguracionResponse(BaseModel):
    """Respuesta de configuración"""
    status: str
    message: str
    configuracion: Optional[ConfiguracionIndividual] = None


# ==================== ENDPOINTS ====================

@router.post("/individual", response_model=ConfiguracionResponse)
async def guardar_configuracion(
    config: ConfiguracionIndividual,
    db: Session = Depends(get_db)
):
    """
    Guarda la configuración individual del usuario
    
    Esta configuración se usa para:
    - Definir momentos litúrgicos activos
    - Personalizar preguntas de Estado Cero
    - Generar actividades relevantes
    - Ajustar la experiencia del usuario
    """
    try:
        # Guardar en dos lugares:
        # 1. JSON para acceso rápido
        # 2. Obsidian para edición y evolución
        import json
        from pathlib import Path
        import os
        
        # 1. Guardar en storage/configuracion_usuario.json
        storage_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent / "storage"
        storage_dir.mkdir(exist_ok=True)
        config_path = storage_dir / "configuracion_usuario.json"
        
        config_dict = config.dict()
        config_dict['fecha_creacion'] = datetime.now().isoformat()
        config_dict['fecha_actualizacion'] = datetime.now().isoformat()
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuración guardada en: {config_path}")
        
        # 2. Guardar en Obsidian (para edición futura)
        vault_path = Path(os.getenv("OBSIDIAN_VAULT_PATH", "obsidian_vault"))
        obsidian_config_path = vault_path / "00-Pilares" / "Configuracion-Individual.md"
        obsidian_config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generar markdown para Obsidian
        markdown = f"""---
tipo: configuracion-individual
user_id: {config.user_id}
fecha_creacion: {datetime.now().strftime('%Y-%m-%d')}
---

# 🕌 Configuración Individual - Campo Sagrado

**Última actualización:** {datetime.now().strftime('%d de %B, %Y - %H:%M')}

## No-Negociables

- Fajr (Estado Cero): {"✓" if config.no_negociables.fajr_estado_cero else "✗"}
- Dhuhr (Estado Cero): {"✓" if config.no_negociables.dhuhr_estado_cero else "✗"}
- Asr (Estado Cero): {"✓" if config.no_negociables.asr_estado_cero else "✗"}
- Maghrib (Validación): {"✓" if config.no_negociables.maghrib_validacion else "✗"}
- Isha (Estado Cero): {"✓" if config.no_negociables.isha_estado_cero else "✗"}

## Dimensiones Prioritarias

{chr(10).join([f"- {dim.capitalize()}" for dim in config.dimensiones_prioritarias]) if config.dimensiones_prioritarias else "- (Ninguna seleccionada)"}

## Contexto

### Financiero
- **Runway:** {config.contexto_financiero.runway_meses} meses
- **Urgencia financiera:** {"Sí ⚡" if config.contexto_financiero.urgencia else "No"}

### Biológico
- **Energía disponible:** {config.energia_disponible}/5
- **Patrón de sueño:** {config.contexto_biologico.patron_sueno.capitalize()}
- **Ejercicio regular:** {"Sí" if config.contexto_biologico.ejercicio_regular else "No"}

## Expresión Libre

{config.expresion_libre if config.expresion_libre else "_No proporcionada_"}

---

**Puedes editar esta nota para actualizar tu configuración**
"""
        
        with open(obsidian_config_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        print(f"✅ Configuración también guardada en Obsidian: {obsidian_config_path}")
        
        return ConfiguracionResponse(
            status="success",
            message="Configuración guardada exitosamente en JSON y Obsidian",
            configuracion=config
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error guardando configuración: {str(e)}"
        )


@router.get("/individual", response_model=ConfiguracionResponse)
async def obtener_configuracion(
    user_id: str = "default",
    db: Session = Depends(get_db)
):
    """
    Obtiene la configuración del usuario
    
    Si no existe configuración, retorna None para que el frontend
    redirija al wizard de onboarding
    """
    try:
        import json
        from pathlib import Path
        
        config_path = Path("storage/configuracion_usuario.json")
        
        if not config_path.exists():
            return ConfiguracionResponse(
                status="not_found",
                message="No existe configuración. Debe completar onboarding",
                configuracion=None
            )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        
        # Remover campos de fecha para el response
        config_dict.pop('fecha_creacion', None)
        config_dict.pop('fecha_actualizacion', None)
        
        config = ConfiguracionIndividual(**config_dict)
        
        return ConfiguracionResponse(
            status="success",
            message="Configuración encontrada",
            configuracion=config
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo configuración: {str(e)}"
        )


@router.put("/individual", response_model=ConfiguracionResponse)
async def actualizar_configuracion(
    config: ConfiguracionIndividual,
    db: Session = Depends(get_db)
):
    """
    Actualiza la configuración existente del usuario
    """
    try:
        import json
        from pathlib import Path
        
        config_path = Path("storage/configuracion_usuario.json")
        
        if not config_path.exists():
            raise HTTPException(
                status_code=404,
                detail="No existe configuración previa. Use POST para crear"
            )
        
        # Leer configuración existente
        with open(config_path, 'r', encoding='utf-8') as f:
            config_existente = json.load(f)
        
        # Actualizar
        config_dict = config.dict()
        config_dict['fecha_creacion'] = config_existente.get('fecha_creacion')
        config_dict['fecha_actualizacion'] = datetime.now().isoformat()
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
        
        return ConfiguracionResponse(
            status="success",
            message="Configuración actualizada exitosamente",
            configuracion=config
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error actualizando configuración: {str(e)}"
        )


@router.delete("/individual")
async def eliminar_configuracion(
    user_id: str = "default",
    db: Session = Depends(get_db)
):
    """
    Elimina la configuración del usuario
    (Útil para testing)
    """
    try:
        import os
        from pathlib import Path
        
        config_path = Path("storage/configuracion_usuario.json")
        
        if config_path.exists():
            os.remove(config_path)
            return {
                "status": "success",
                "message": "Configuración eliminada"
            }
        else:
            return {
                "status": "not_found",
                "message": "No había configuración que eliminar"
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error eliminando configuración: {str(e)}"
        )


@router.get("/dimensiones")
async def obtener_dimensiones_disponibles():
    """
    Retorna las 7 dimensiones del arcoíris disponibles
    """
    return {
        "dimensiones": [
            {
                "id": "finanzas",
                "nombre": "Finanzas",
                "descripcion": "Dinero, ingresos, inversiones, runway",
                "color": "#DC2626",
                "emoji": "🔴"
            },
            {
                "id": "biologia",
                "nombre": "Biología",
                "descripcion": "Salud, energía, ejercicio, alimentación",
                "color": "#F97316",
                "emoji": "🟠"
            },
            {
                "id": "conocimiento",
                "nombre": "Conocimiento",
                "descripcion": "Aprendizaje, libros, cursos, estudio",
                "color": "#EAB308",
                "emoji": "🟡"
            },
            {
                "id": "desarrollo",
                "nombre": "Desarrollo",
                "descripcion": "Proyectos, código, creación, build",
                "color": "#22C55E",
                "emoji": "🟢"
            },
            {
                "id": "relaciones",
                "nombre": "Relaciones",
                "descripcion": "Familia, amigos, comunidad, networking",
                "color": "#3B82F6",
                "emoji": "🔵"
            },
            {
                "id": "creatividad",
                "nombre": "Creatividad",
                "descripcion": "Arte, música, escritura, diseño",
                "color": "#8B5CF6",
                "emoji": "🟣"
            },
            {
                "id": "espiritualidad",
                "nombre": "Espiritualidad",
                "descripcion": "Meditación, filosofía, propósito",
                "color": "#A855F7",
                "emoji": "🟤"
            }
        ]
    }

