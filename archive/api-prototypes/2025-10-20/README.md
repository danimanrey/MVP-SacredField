# API Prototypes - Archived 2025-10-20

## Archivos

### estado_cero_simple.py
- **Propósito**: Prototipo sin IA sintética
- **Features**: Preguntas contextuales, archivo Obsidian
- **Estado**: Funcional pero no usado en producción
- **Razón archivo**: Duplicación con estado_cero.py (versión productiva)
- **Líneas**: ~377

### estado_cero_ultra_simple.py
- **Propósito**: Experimental - una pregunta emergente
- **Features**: Event queue, audit trail, Google Calendar
- **Estado**: Experimental
- **Razón archivo**: Usado solo por estado-cero-inmersivo (también archivado)
- **Líneas**: ~514

### main_simple.py
- **Propósito**: Entry point simplificado para desarrollo
- **Features**: 3 routers básicos, CORS sin seguridad
- **Estado**: Funcional para debug
- **Razón archivo**: Procfile usa main.py (versión completa)
- **Líneas**: ~124

## Recuperación

Si necesitas restaurar alguno:
```bash
cp archive/api-prototypes/2025-10-20/<file> apps/backend/api/
```

## Decisión Técnica

**Mantener**: `api/main.py` + `api/estado_cero.py` (confirmado por Procfile y uso en frontend)  
**Archivar**: 3 prototipos alternativos no usados en flujo productivo

## Verificación de Impacto

```bash
# Entry point real
$ cat apps/backend/Procfile
web: uvicorn api.main:app --host 0.0.0.0 --port $PORT

# Imports en main.py
$ grep "estado_cero" apps/backend/api/main.py
from api import estado_cero
app.include_router(estado_cero.router, prefix="/api/estado-cero", tags=["Estado Cero"])
```

**Conclusión**: Solo estado_cero.py se importa. Versiones simples/ultra-simples no están en uso.

## Notas

- Preservados para referencia futura
- Contienen ideas útiles para v2.0
- No eliminar, solo archivar
- Fecha: 2025-10-20
- Branch: consolidation/estado-cero-unificado
- Commit: TBD

إن شاء الله

