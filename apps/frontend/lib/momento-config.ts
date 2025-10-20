/**
 * Configuración personalizada por momento litúrgico
 */

export interface MomentoConfig {
  nombre: string
  emoji: string
  hora_aproximada: string
  color_primario: string
  color_secundario: string
  fase_universo: 'entrada' | 'expansion' | 'preguntas' | 'sintesis'
  texto_entrada: string
  texto_expansion: string
  cualidad: string
  enfoque: string
}

export const MOMENTOS_CONFIG: Record<string, MomentoConfig> = {
  fajr: {
    nombre: 'Fajr',
    emoji: '🌅',
    hora_aproximada: '~06:00',
    color_primario: '#A855F7',  // Violeta (espiritual)
    color_secundario: '#F59E0B', // Ambar (amanecer)
    fase_universo: 'entrada',
    texto_entrada: 'El día nace contigo',
    texto_expansion: 'Abre tu consciencia al nuevo día',
    cualidad: 'Pureza y nuevos comienzos',
    enfoque: 'Dirección del día'
  },
  
  dhuhr: {
    nombre: 'Dhuhr',
    emoji: '☀️',
    hora_aproximada: '~13:00',
    color_primario: '#EAB308',  // Amarillo (luz plena)
    color_secundario: '#22C55E', // Verde (vida)
    fase_universo: 'expansion',
    texto_entrada: 'El sol en su cenit',
    texto_expansion: 'Recentra tu energía',
    cualidad: 'Claridad y poder',
    enfoque: 'Ajuste de rumbo'
  },
  
  maghrib: {
    nombre: 'Maghrib',
    emoji: '🌆',
    hora_aproximada: '~19:00',
    color_primario: '#DC2626',  // Rojo (atardecer)
    color_secundario: '#8B5CF6', // Púrpura (transición)
    fase_universo: 'sintesis',
    texto_entrada: 'El día se cierra',
    texto_expansion: 'Integra lo vivido',
    cualidad: 'Gratitud y cierre',
    enfoque: 'Revisión del día'
  }
}

export function obtenerConfigMomento(momento: string): MomentoConfig {
  return MOMENTOS_CONFIG[momento] || MOMENTOS_CONFIG.fajr
}

export function obtenerTextosMomento(momento: string) {
  const config = obtenerConfigMomento(momento)
  
  return {
    pre_inicio: {
      titulo: config.texto_entrada,
      subtitulo: config.cualidad,
      emoji: config.emoji
    },
    entrada: {
      titulo: 'Respira profundo',
      subtitulo: config.texto_entrada
    },
    expansion: {
      titulo: config.texto_expansion,
      subtitulo: 'Conecta con tu autoridad interior'
    },
    preguntas: {
      titulo: 'Las preguntas emergen',
      subtitulo: `Enfoque: ${config.enfoque}`
    },
    sintesis: {
      titulo: 'La claridad emerge',
      subtitulo: 'Tu dirección se revela'
    },
    completado: {
      titulo: `${config.nombre} Completado`,
      subtitulo: config.cualidad
    }
  }
}

