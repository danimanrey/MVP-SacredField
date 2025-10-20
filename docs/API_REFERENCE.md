# 📘 API Reference - Campo Sagrado MVP

## Índice

1. [Estado Cero](#estado-cero)
2. [Orquestador](#orquestador)
3. [Guardian](#guardian)
4. [Tiempos Litúrgicos](#tiempos-liturgicos)
5. [Calendario Hijri](#calendario-hijri)
6. [Manifestaciones (7 Dimensiones)](#manifestaciones)
7. [Ley de la Octava](#ley-de-la-octava)
8. [Vistas Temporales](#vistas-temporales)
9. [Health Check](#health-check)

---

## Base URL

```
http://localhost:8000
```

Todos los endpoints están bajo esta URL base.

---

## Estado Cero

### `GET /api/estado-cero/verificar-momento`

Verifica si es momento adecuado para realizar un Estado Cero.

**Parámetros de query:**
- `permitir_recuperacion` (bool, opcional): Si es `true`, permite iniciar Estado Cero aunque la ventana litúrgica haya pasado (para recuperación).

**Respuesta:**
```json
{
  "es_momento": true,
  "momento_liturgico": "dhuhr",
  "tiempo_disponible_minutos": 205,
  "proximo_tiempo_rezo": "asr",
  "mensaje": "Es momento de Estado Cero (Dhuhr). Tienes 205 minutos.",
  "fuera_de_ventana": false
}
```

**Estados:**
- `200 OK`: Verificación exitosa
- `400 Bad Request`: Error en parámetros

---

### `POST /api/estado-cero/iniciar`

Inicia un nuevo Estado Cero (consulta sacral con Claude).

**Body:**
```json
{
  "momento_liturgico": "dhuhr",
  "contexto_adicional": "Necesito revisar mis objetivos del mes"
}
```

**Respuesta:**
```json
{
  "id": "estado_cero_abc123",
  "momento_liturgico": "dhuhr",
  "timestamp": "2025-10-08T14:30:00",
  "preguntas_generadas": 7,
  "tiempo_estimado_minutos": 15,
  "estado": "en_progreso",
  "mensaje": "Estado Cero iniciado. Responde las preguntas con autoridad sacral."
}
```

**Estados:**
- `201 Created`: Estado Cero creado exitosamente
- `400 Bad Request`: No es momento litúrgico
- `500 Internal Server Error`: Error en generación de preguntas

---

### `POST /api/estado-cero/responder`

Envía respuestas a preguntas del Estado Cero.

**Body:**
```json
{
  "estado_cero_id": "estado_cero_abc123",
  "pregunta_id": "p1",
  "respuesta": "Sí",
  "respuesta_binaria": true,
  "confianza": 0.9
}
```

**Respuesta:**
```json
{
  "pregunta_id": "p1",
  "procesada": true,
  "siguiente_pregunta": {
    "id": "p2",
    "texto": "¿Sientes que tu energía está siendo bien dirigida hoy?",
    "tipo": "binaria"
  },
  "progreso_porcentaje": 14.3
}
```

**Estados:**
- `200 OK`: Respuesta procesada
- `404 Not Found`: Estado Cero no encontrado

---

### `GET /api/estado-cero/{estado_cero_id}`

Obtiene el detalle de un Estado Cero específico.

**Respuesta:**
```json
{
  "id": "estado_cero_abc123",
  "momento_liturgico": "dhuhr",
  "timestamp": "2025-10-08T14:30:00",
  "preguntas": [...],
  "respuestas": [...],
  "insight_generado": "Tu energía está alineada con...",
  "estado": "completado",
  "duracion_minutos": 12
}
```

---

### `GET /api/estado-cero/ventanas-perdidas`

Lista las ventanas de Estado Cero que fueron perdidas y pueden ser recuperadas.

**Respuesta:**
```json
{
  "ventanas_perdidas": [
    {
      "momento_liturgico": "fajr",
      "fecha": "2025-10-08",
      "hora_inicio": "06:46",
      "hora_fin": "08:19",
      "puede_recuperarse": true,
      "tiempo_desde_ventana": "6 horas"
    }
  ],
  "total_perdidas": 1,
  "mensaje": "Tienes 1 Estado Cero pendiente de recuperación."
}
```

---

## Orquestador

### `POST /api/orquestador/planificar-dia`

Genera el plan del día (Espejo Diario) basado en Estados Cero, no-negociables y autoridad sacral.

**Body:**
```json
{
  "fecha": "2025-10-08",
  "estados_cero_ids": ["estado_cero_abc123"],
  "contexto_adicional": "Tengo reunión importante a las 16:00"
}
```

**Respuesta:**
```json
{
  "fecha": "2025-10-08",
  "bloques": [
    {
      "id": "bloque_1",
      "hora_inicio": "06:46",
      "hora_fin": "07:00",
      "tipo": "ancla_liturgica",
      "titulo": "Fajr",
      "descripcion": "Salat del alba",
      "es_flexible": false,
      "prioridad": "alta"
    },
    {
      "id": "bloque_2",
      "hora_inicio": "07:15",
      "hora_fin": "07:30",
      "tipo": "estado_cero",
      "titulo": "Estado Cero (Fajr)",
      "descripcion": "Consulta sacral matinal",
      "es_flexible": false,
      "prioridad": "alta"
    },
    {
      "id": "bloque_3",
      "hora_inicio": "08:00",
      "hora_fin": "09:30",
      "tipo": "no_negociable",
      "titulo": "Deep Work - Proyecto Principal",
      "descripcion": "Fase de máxima concentración",
      "es_flexible": false,
      "prioridad": "alta"
    },
    {
      "id": "bloque_4",
      "hora_inicio": "09:30",
      "hora_fin": "12:00",
      "tipo": "espacio_libre",
      "titulo": "Espacio Libre",
      "descripcion": "40% sagrado - Emergencia permitida",
      "es_flexible": true,
      "prioridad": "media"
    }
  ],
  "estadisticas": {
    "anclas_liturgicas": 5,
    "estados_cero": 5,
    "no_negociables": 3,
    "espacio_libre_porcentaje": 42.5,
    "horas_productivas": 6.5
  },
  "insight": "Tu día está equilibrado al borde del caos (42.5% libre).",
  "generado_en": "2025-10-08T06:00:00"
}
```

**Estados:**
- `201 Created`: Plan generado exitosamente
- `400 Bad Request`: Datos inválidos
- `500 Internal Server Error`: Error en generación

---

### `GET /api/orquestador/espejo-diario/{fecha}`

Obtiene el Espejo Diario de una fecha específica.

**Respuesta:**
```json
{
  "fecha": "2025-10-08",
  "bloques": [...],
  "estadisticas": {...},
  "ultima_actualizacion": "2025-10-08T14:30:00"
}
```

---

## Guardian

### `GET /api/guardian/estado-sistema`

Obtiene el estado actual del sistema.

**Respuesta:**
```json
{
  "estado_general": "saludable",
  "agentes": {
    "estado_cero": {
      "activo": true,
      "ultima_ejecucion": "2025-10-08T14:30:00",
      "estados_hoy": 3,
      "estados_objetivo": 5
    },
    "orquestador": {
      "activo": true,
      "ultima_planificacion": "2025-10-08T06:00:00",
      "precision_estimaciones": 0.87
    },
    "documentador": {
      "activo": true,
      "documentos_creados_hoy": 3,
      "vault_conectado": true
    }
  },
  "metricas": {
    "coherencia_sistema": 0.92,
    "adherencia_plan": 0.85,
    "espacio_libre_respetado": 0.95
  },
  "alertas": []
}
```

---

### `GET /api/guardian/reportes/diario`

Genera un reporte diario del sistema.

**Respuesta:**
```json
{
  "fecha": "2025-10-08",
  "resumen": "Día productivo con 5/5 Estados Cero completados",
  "estados_cero_completados": 5,
  "adherencia_plan": 0.85,
  "espacio_libre_utilizado": 0.40,
  "logros_del_dia": [
    "Completaste todos los Estados Cero",
    "Respetaste el 95% de las anclas litúrgicas",
    "Mantuviste 42% de espacio libre"
  ],
  "areas_mejora": [
    "Considera reducir reuniones no-esenciales"
  ],
  "recomendaciones": [
    "Mañana prioriza la dimensión Biológica (Lunes/RE)"
  ]
}
```

---

## Tiempos Litúrgicos

### `GET /api/tiempos-liturgicos/hoy`

Obtiene los tiempos de rezo precisos para el día actual.

**Respuesta:**
```json
{
  "fecha": "2025-10-08",
  "ubicacion": {
    "latitud": 40.5472,
    "longitud": -3.6228,
    "ciudad": "San Sebastián de los Reyes"
  },
  "tiempos_rezo": {
    "fajr": "06:46",
    "sunrise": "08:19",
    "dhuhr": "14:31",
    "asr": "17:56",
    "maghrib": "20:37",
    "isha": "22:10"
  },
  "momento_actual": "dhuhr",
  "proximo_rezo": "asr",
  "tiempo_hasta_proximo": "3 horas 25 minutos"
}
```

---

### `GET /api/tiempos-liturgicos/semana`

Obtiene los tiempos de rezo para la semana completa.

**Respuesta:**
```json
{
  "semana_inicio": "2025-10-06",
  "semana_fin": "2025-10-12",
  "dias": [
    {
      "fecha": "2025-10-06",
      "dia_semana": "domingo",
      "nota": "do",
      "dimension": "espiritual",
      "tiempos_rezo": {...}
    },
    ...
  ]
}
```

---

## Calendario Hijri

### `GET /api/calendario-hijri/hoy`

Obtiene el contexto del día actual en el calendario Hijri.

**Respuesta:**
```json
{
  "fecha_gregoriana": "2025-10-08",
  "fecha_hijri": {
    "dia": 15,
    "mes": 4,
    "año": 1447,
    "nombre_mes": "Rabi' al-Thani",
    "mes_completo": {
      "numero": 4,
      "nombre": "Rabi' al-Thani",
      "significado": "Segunda Primavera",
      "cualidad": "Gratitud y Servicio",
      "es_sagrado": false,
      "ensenanza_mistica": "El segundo florecimiento del alma tras la purificación",
      "ayat_clave": "Sura 55:13 - ¿Cuál de las mercedes de vuestro Señor negaréis?"
    }
  },
  "fase_lunar": "creciente",
  "porcentaje_mes": 0.5
}
```

---

### `GET /api/calendario-hijri/año/{año_hijri}`

Obtiene todos los meses de un año Hijri específico.

**Respuesta:**
```json
{
  "año_hijri": 1447,
  "meses": [
    {
      "numero": 1,
      "nombre": "Muharram",
      "significado": "Sagrado",
      "cualidad": "Renovación y Retorno",
      "es_sagrado": true,
      "ensenanza_mistica": "El comienzo del viaje interior...",
      "ayat_clave": "Sura 9:36"
    },
    ...
  ],
  "total_meses": 12
}
```

---

## Manifestaciones

### `GET /api/manifestaciones/dimensiones`

Obtiene las 7 dimensiones del ser con sus manifestaciones (objetivos).

**Respuesta:**
```json
{
  "dimensiones": [
    {
      "id": "espiritual",
      "nombre": "Espiritual",
      "icono": "🕌",
      "color": "#DC2626",
      "descripcion": "Conexión con lo trascendente...",
      "pregunta_clave": "¿Estoy viviendo desde mi centro sagrado?",
      "manifestaciones": [
        {
          "id": "obj_1",
          "nombre": "Establecer práctica de dhikr diario",
          "progreso_general": 65.0,
          "dimension_primaria": "espiritual",
          "fecha_objetivo": "2025-12-31"
        }
      ],
      "total_manifestaciones": 1,
      "progreso_general": 65.0,
      "ultima_revision": "2025-10-08T14:30:00"
    },
    ...
  ]
}
```

---

### `GET /api/manifestaciones/dimension/{dimension_id}`

Obtiene detalle de una dimensión específica.

**Parámetros:**
- `dimension_id`: Uno de `espiritual`, `biologico`, `financiero`, `conocimiento`, `relacional`, `desarrollo`, `creativo`

**Respuesta:**
```json
{
  "id": "espiritual",
  "nombre": "Espiritual",
  "icono": "🕌",
  "color": "#DC2626",
  "descripcion": "Conexión con lo trascendente...",
  "pregunta_clave": "¿Estoy viviendo desde mi centro sagrado?",
  "manifestaciones": [...],
  "total_manifestaciones": 1,
  "progreso_general": 65.0,
  "ultima_revision": "2025-10-08T14:30:00"
}
```

---

### `POST /api/manifestaciones/manifestacion`

Crea una nueva manifestación (objetivo).

**Body:**
```json
{
  "nombre": "Dominar React Three Fiber",
  "descripcion": "Crear experiencias 3D inmersivas para Campo Sagrado",
  "dimension_primaria": "conocimiento",
  "fecha_objetivo": "2025-12-31",
  "practica_diaria": "Coding + tutorial",
  "pesos_armonicos": {
    "conocimiento": 0.4,
    "creativo": 0.3,
    "desarrollo": 0.2,
    "financiero": 0.1
  }
}
```

**Respuesta:**
```json
{
  "id": "obj_abc123",
  "nombre": "Dominar React Three Fiber",
  "descripcion": "Crear experiencias 3D inmersivas para Campo Sagrado",
  "dimension_primaria": "conocimiento",
  "nota_fundamental": "fa",
  "fecha_inicio": "2025-10-08",
  "fecha_objetivo": "2025-12-31",
  "progreso_general": 0.0,
  "estado": "activa",
  "armonicos": {...},
  "shocks_conscientes": [...],
  "plan_octava_semanal": [...]
}
```

**Estados:**
- `201 Created`: Manifestación creada
- `400 Bad Request`: Datos inválidos

---

### `PUT /api/manifestaciones/manifestacion/{objetivo_id}/progreso`

Actualiza el progreso de una manifestación.

**Body:**
```json
{
  "progreso": 75.0
}
```

**Respuesta:**
```json
{
  "id": "obj_abc123",
  "progreso_general": 75.0,
  "ultima_actualizacion": "2025-10-08T14:30:00"
}
```

---

### `GET /api/manifestaciones/auditoria-dimensiones`

Realiza una auditoría de equilibrio entre dimensiones.

**Respuesta:**
```json
{
  "desequilibrios": [],
  "dimensiones_sin_manifestaciones": ["financiero"],
  "dimensiones_bajo_progreso": ["biologico"],
  "recomendaciones": [
    "Considera añadir manifestaciones a la dimensión financiero.",
    "La dimensión biologico tiene bajo progreso (25%). Revisa tus objetivos."
  ]
}
```

---

## Ley de la Octava

### `GET /api/octavas/correspondencias`

Obtiene las 7 correspondencias completas de la Ley de la Octava.

**Respuesta:**
```json
[
  {
    "nota": "do",
    "dia": "domingo",
    "dimension": "espiritual",
    "arquetipo": "Sol ☀️",
    "color": "#DC2626",
    "fase": "NIYYAH - Intención pura",
    "es_intervalo_critico": false,
    "frecuencia_relativa": 1.0
  },
  {
    "nota": "mi",
    "dia": "martes",
    "dimension": "financiero",
    "arquetipo": "Marte ⚔️",
    "color": "#F59E0B",
    "fase": "ACCIÓN - Materialización",
    "es_intervalo_critico": true,
    "frecuencia_relativa": 1.25
  },
  ...
]
```

---

### `GET /api/octavas/dimension-hoy`

Obtiene la dimensión prioritaria del día actual.

**Respuesta:**
```json
{
  "fecha": "2025-10-08",
  "dimension_prioritaria": "relacional",
  "nota": "sol",
  "dia": "jueves",
  "arquetipo": "♃ Júpiter",
  "energia": "Expansión, generosidad, conexión",
  "fase": "EXPANSIÓN - Compartir",
  "pregunta_clave": "¿Nutro las conexiones que importan?",
  "color": "#3B82F6",
  "mensaje": "HOY es día de ♃ Júpiter. Prioriza la dimensión relacional."
}
```

---

### `POST /api/octavas/crear-objetivo`

Crea un nuevo objetivo basado en la Ley de la Octava.

**Body:**
```json
{
  "nombre": "Alcanzar libertad financiera",
  "descripcion": "Generar ingresos pasivos suficientes",
  "dimension_primaria": "financiero",
  "fecha_objetivo": "2026-10-08",
  "practica_diaria": "Trabajo en proyecto + inversión",
  "pesos_armonicos": {
    "financiero": 0.4,
    "conocimiento": 0.2,
    "desarrollo": 0.2,
    "creativo": 0.1,
    "biologico": 0.05,
    "espiritual": 0.025,
    "relacional": 0.025
  }
}
```

**Respuesta:**
```json
{
  "id": "octava_xyz789",
  "nombre": "Alcanzar libertad financiera",
  "dimension_primaria": "financiero",
  "nota_fundamental": "mi",
  "fecha_inicio": "2025-10-08",
  "fecha_objetivo": "2026-10-08",
  "progreso_general": 0.0,
  "octava_actual": 1,
  "nivel_frecuencia": 1.0,
  "armonicos": {...},
  "shocks_conscientes": [
    {
      "intervalo": "MI-FA",
      "dia_semana": "martes",
      "tipo": "revision_profunda",
      "pregunta_activacion": "Revisa tu intención profunda. ¿Sigue resonando?",
      "completado": false
    },
    {
      "intervalo": "SI-DO",
      "dia_semana": "sabado",
      "tipo": "celebracion_integracion",
      "pregunta_activacion": "Celebra lo logrado. ¿Qué emerge para la siguiente octava?",
      "completado": false
    }
  ],
  "plan_octava_semanal": [...]
}
```

---

### `GET /api/octavas/objetivo/{objetivo_id}`

Obtiene detalle de un objetivo específico.

**Respuesta:**
```json
{
  "id": "octava_xyz789",
  "nombre": "Alcanzar libertad financiera",
  "progreso_general": 35.0,
  "octava_actual": 2,
  "armonicos": {...},
  "shocks_conscientes": [...]
}
```

---

### `POST /api/octavas/objetivo/{objetivo_id}/shock`

Aplica un shock consciente a un objetivo.

**Body:**
```json
{
  "tipo_shock": "revision_profunda"
}
```

**Respuesta:**
```json
{
  "message": "Shock revision_profunda aplicado",
  "objetivo": {...}
}
```

---

### `GET /api/octavas/shocks-hoy`

Obtiene los shocks que deben aplicarse hoy.

**Respuesta:**
```json
{
  "fecha": "2025-10-08",
  "shocks_pendientes": [
    {
      "objetivo_id": "octava_xyz789",
      "objetivo_nombre": "Alcanzar libertad financiera",
      "shock": {
        "intervalo": "MI-FA",
        "tipo": "revision_profunda",
        "pregunta_activacion": "Revisa tu intención profunda. ¿Sigue resonando?"
      }
    }
  ],
  "total": 1
}
```

---

### `GET /api/octavas/objetivo/{objetivo_id}/espiral`

Genera datos para visualizar la espiral de octavas.

**Respuesta:**
```json
{
  "objetivo_id": "octava_xyz789",
  "nombre": "Alcanzar libertad financiera",
  "octava_actual": 2,
  "puntos_espiral": [
    {
      "nota": "do",
      "dimension": "espiritual",
      "progreso": 10.0
    },
    {
      "nota": "re",
      "dimension": "biologico",
      "progreso": 20.0
    },
    ...
  ]
}
```

---

## Vistas Temporales

### `GET /api/vistas/semanal`

Obtiene la vista semanal completa.

**Parámetros de query:**
- `fecha` (opcional): Fecha en formato `YYYY-MM-DD`. Por defecto, semana actual.

**Respuesta:**
```json
{
  "semana_inicio": "2025-10-06",
  "semana_fin": "2025-10-12",
  "dias": [
    {
      "fecha": "2025-10-06",
      "dia_semana": "domingo",
      "nota": "do",
      "dimension_prioritaria": "espiritual",
      "arquetipo": "☀️ Sol",
      "color": "#DC2626",
      "energia": "Intención, purificación, retorno al centro",
      "pregunta_clave": "¿Estoy viviendo desde mi centro sagrado?",
      "tiempos_rezo": {...},
      "espejo_diario": {...}
    },
    ...
  ],
  "insight_semanal": "Esta semana enfoca en equilibrio entre acción (MI) y reflexión (SI)."
}
```

---

### `GET /api/vistas/anual`

Obtiene la vista anual del calendario Hijri.

**Parámetros de query:**
- `año_hijri` (opcional): Año Hijri. Por defecto, año actual.

**Respuesta:**
```json
{
  "año_hijri": 1447,
  "año_gregoriano": 2025,
  "meses": [
    {
      "numero": 1,
      "nombre": "Muharram",
      "significado": "Sagrado",
      "cualidad": "Renovación y Retorno",
      "es_sagrado": true,
      "ensenanza_mistica": "El comienzo del viaje interior...",
      "fecha_inicio_aproximada": "2025-06-27",
      "total_dias": 29
    },
    ...
  ],
  "meses_sagrados": ["Muharram", "Rajab", "Dhu al-Qi'dah", "Dhu al-Hijjah"],
  "eventos_importantes": [
    {
      "nombre": "Ashura",
      "mes": "Muharram",
      "dia": 10,
      "significado": "Día de expiación y ayuno"
    },
    {
      "nombre": "Inicio de Ramadán",
      "mes": "Ramadan",
      "dia": 1,
      "significado": "Mes de ayuno y purificación"
    }
  ]
}
```

---

## Health Check

### `GET /health`

Verifica el estado de salud del backend.

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-08T14:30:00",
  "version": "1.0.0",
  "contexto_temporal": {
    "fecha_gregoriana": "2025-10-08",
    "fecha_hijri": "15 Rabi' al-Thani 1447",
    "momento_liturgico": "dhuhr",
    "proximo_rezo": "asr"
  },
  "agentes": {
    "estado_cero": "activo",
    "orquestador": "activo",
    "guardian": "activo",
    "documentador": "activo"
  }
}
```

**Estados:**
- `200 OK`: Sistema saludable
- `503 Service Unavailable`: Sistema con problemas

---

## Códigos de Estado HTTP

- **200 OK**: Solicitud exitosa
- **201 Created**: Recurso creado exitosamente
- **400 Bad Request**: Datos inválidos o faltantes
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error interno del servidor
- **503 Service Unavailable**: Servicio temporalmente no disponible

---

## Autenticación

En el MVP, no hay autenticación. En versiones futuras, se implementará:
- OAuth 2.0 con Google/Obsidian
- JWT tokens para sesiones
- API keys para integraciones

---

## Rate Limiting

Actualmente no hay límites. En producción:
- 100 requests/minuto por IP
- 1000 requests/hora por usuario autenticado
- Respuesta `429 Too Many Requests` si se excede

---

## CORS

El backend permite CORS desde:
- `http://localhost:5173` (SvelteKit dev)
- `http://localhost:3000` (Next.js dev)
- En producción: dominio específico

---

## WebSockets (Futuro)

Endpoints en tiempo real:
- `/ws/espejo-diario` - Actualizaciones en vivo del plan
- `/ws/guardian` - Alertas del sistema
- `/ws/contexto` - Contexto temporal actualizado

---

## Changelog

### v1.0.0 (2025-10-08)
- ✅ API completa de Estado Cero
- ✅ API de Orquestador
- ✅ API de Guardian
- ✅ Tiempos Litúrgicos precisos
- ✅ Calendario Hijri (12 meses)
- ✅ 7 Dimensiones del Ser
- ✅ Ley de la Octava completa
- ✅ Vistas temporales (semanal, anual)

---

## Soporte

Para problemas, sugerencias o documentación adicional:
- Email: mansodani375@gmail.com
- Repositorio: (privado)

---

**مَا شَاءَ ٱللَّٰهُ** - Lo que Dios ha querido

إن شاء الله - Si Dios quiere
