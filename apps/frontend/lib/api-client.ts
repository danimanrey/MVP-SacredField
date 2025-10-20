/**
 * Cliente API para comunicación con el backend FastAPI
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export interface PreguntaBinaria {
  id: string
  pregunta: string
  contexto: string
  categoria: string
}

export interface EstadoCeroCompleto {
  id: string
  momento: string
  fecha: string
  preguntas: PreguntaBinaria[]
  contexto: Record<string, unknown>
}

export interface RespuestaSacral {
  pregunta_id: string
  sensacion: 'expansion' | 'contraccion'
  intensidad: number
  nota?: string
}

export interface AccionConcreta {
  descripcion: string
  resultado_observable: string
  duracion_estimada: string
  energia_requerida: number
  rol?: string
}

// Tipos de respuesta del API
export interface MomentoResponse {
  momento_actual: string
  momento: string
  siguiente_estado_cero?: string
  configuracion?: Record<string, unknown>
}

export interface DireccionEmergente {
  sintesis: string
  direccion: string
  direccion_emergente: string
  tendencia?: string
  intensidad?: number
  urgencia?: string
}

export interface ChatResponse {
  respuesta: string
  contexto?: Record<string, unknown>
}

export interface FinalizarResponse {
  success: boolean
  message: string
  accion_id?: string
}

/**
 * API de Estado Cero
 */
export const estadoCeroAPI = {
  /**
   * Verificar momento litúrgico actual
   */
  async verificarMomento(): Promise<MomentoResponse> {
    const res = await fetch(`${API_BASE}/estado-cero/verificar`)
    if (!res.ok) throw new Error('Error verificando momento')
    return res.json()
  },

  /**
   * Iniciar nuevo Estado Cero
   */
  async iniciar(momento: string, permitirRecuperacion: boolean = false): Promise<EstadoCeroCompleto> {
    const res = await fetch(`${API_BASE}/estado-cero/iniciar?permitir_recuperacion=${permitirRecuperacion}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ momento })
    })
    if (!res.ok) {
      const error: { detail?: unknown } = await res.json()
      const errorDetail = error.detail
      const errorMsg = typeof errorDetail === 'string'
        ? errorDetail
        : Array.isArray(errorDetail)
        ? errorDetail.map((e: {msg: string}) => e.msg).join(', ')
        : 'Error iniciando Estado Cero'
      throw new Error(errorMsg)
    }
    return res.json()
  },

  /**
   * Enviar respuesta a pregunta sacral
   */
  async responder(estadoId: string, respuesta: RespuestaSacral): Promise<{ success: boolean }> {
    const res = await fetch(`${API_BASE}/estado-cero/${estadoId}/responder`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(respuesta)
    })
    if (!res.ok) throw new Error('Error enviando respuesta')
    return res.json()
  },

  /**
   * Sintetizar dirección emergente
   */
  async sintetizar(estadoId: string): Promise<DireccionEmergente> {
    const res = await fetch(`${API_BASE}/estado-cero/${estadoId}/sintetizar`, {
      method: 'POST'
    })
    if (!res.ok) throw new Error('Error sintetizando dirección')
    return res.json()
  },

  /**
   * Chat clarificador
   */
  async chat(estadoId: string, mensaje: string): Promise<ChatResponse> {
    const res = await fetch(`${API_BASE}/estado-cero/${estadoId}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mensaje })
    })
    if (!res.ok) throw new Error('Error en chat')
    return res.json()
  },

  /**
   * Finalizar Estado Cero
   */
  async finalizar(estadoId: string, accion: AccionConcreta): Promise<FinalizarResponse> {
    const res = await fetch(`${API_BASE}/estado-cero/${estadoId}/finalizar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(accion)
    })
    if (!res.ok) throw new Error('Error finalizando Estado Cero')
    return res.json()
  }
}

/**
 * API de Espejo Diario
 */
export const espejoDiarioAPI = {
  /**
   * Obtener espejo de hoy
   */
  async obtenerHoy(): Promise<Record<string, unknown>> {
    const res = await fetch(`${API_BASE}/espejo-diario/hoy`)
    if (!res.ok) throw new Error('Error obteniendo espejo')
    return res.json()
  },

  /**
   * Actualizar espejo con Estado Cero
   */
  async actualizar(estadoCeroId: string): Promise<{ success: boolean; timestamp: string }> {
    const res = await fetch(`${API_BASE}/espejo-diario/actualizar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ estado_cero_id: estadoCeroId })
    })
    if (!res.ok) throw new Error('Error actualizando espejo')
    return res.json()
  }
}

/**
 * API de Contexto Temporal
 */
export const contextoAPI = {
  /**
   * Obtener contexto temporal actual
   */
  async obtener(): Promise<Record<string, unknown>> {
    const res = await fetch(`${API_BASE}/contexto-temporal`)
    if (!res.ok) throw new Error('Error obteniendo contexto')
    return res.json()
  }
}

