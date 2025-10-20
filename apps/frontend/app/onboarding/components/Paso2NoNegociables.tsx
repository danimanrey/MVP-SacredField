'use client'

import { motion } from 'framer-motion'
import { useOnboardingStore } from '@/lib/stores/onboarding-store'

interface Paso2NoNegociablesProps {
  onSiguiente: () => void
  onAnterior: () => void
}

interface MomentoToggle {
  key: keyof typeof initialState
  emoji: string
  nombre: string
  hora: string
  descripcion: string
  defaultValue: boolean
}

const momentos: MomentoToggle[] = [
  {
    key: 'fajr_estado_cero',
    emoji: '🌅',
    nombre: 'Estado Cero Fajr',
    hora: '~6:00 AM',
    descripcion: 'Comenzar el día con claridad y dirección',
    defaultValue: true
  },
  {
    key: 'dhuhr_estado_cero',
    emoji: '☀️',
    nombre: 'Estado Cero Dhuhr',
    hora: '~1:00 PM',
    descripcion: 'Recentrarse a mitad del día',
    defaultValue: true
  },
  {
    key: 'asr_estado_cero',
    emoji: '🌤️',
    nombre: 'Estado Cero Asr',
    hora: '~5:00 PM',
    descripcion: 'Momento opcional de reflexión',
    defaultValue: false
  },
  {
    key: 'maghrib_validacion',
    emoji: '🌅',
    nombre: 'Validación Maghrib',
    hora: '~7:00 PM',
    descripcion: 'Revisar la salud del día',
    defaultValue: true
  },
  {
    key: 'isha_estado_cero',
    emoji: '🌙',
    nombre: 'Estado Cero Isha',
    hora: '~9:00 PM',
    descripcion: 'Momento opcional antes de dormir',
    defaultValue: false
  }
]

const initialState = {
  fajr_estado_cero: true,
  dhuhr_estado_cero: true,
  asr_estado_cero: false,
  maghrib_validacion: true,
  isha_estado_cero: false
}

export default function Paso2NoNegociables({ onSiguiente, onAnterior }: Paso2NoNegociablesProps) {
  const { configuracion, setNoNegociables } = useOnboardingStore()
  const noNegociables = configuracion.no_negociables || initialState

  const toggle = (key: keyof typeof initialState) => {
    setNoNegociables({
      ...noNegociables,
      [key]: !noNegociables[key]
    })
  }

  const activos = Object.values(noNegociables).filter(Boolean).length

  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      className="max-w-4xl mx-auto"
    >
      {/* Header */}
      <div className="text-center mb-12">
        <h2 className="text-4xl md:text-5xl font-light mb-4">
          Tus No-Negociables
        </h2>
        <p className="text-xl text-gray-300">
          Define qué prácticas son innegociables para ti
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Mínimo 1 · Recomendado 3 · Activos: {activos}
        </p>
      </div>

      {/* Grid de momentos */}
      <div className="space-y-4 mb-12">
        {momentos.map((momento, index) => (
          <motion.button
            key={momento.key}
            onClick={() => toggle(momento.key)}
            className={`w-full p-6 rounded-2xl border-2 transition-all duration-300 text-left ${
              noNegociables[momento.key]
                ? 'bg-purpura-mistico/20 border-purpura-mistico shadow-lg shadow-purpura-mistico/20'
                : 'bg-white/5 border-white/10 hover:border-white/30'
            }`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <div className="flex items-start gap-4">
              {/* Checkbox */}
              <div className={`flex-shrink-0 w-6 h-6 rounded-md border-2 flex items-center justify-center transition-all ${
                noNegociables[momento.key]
                  ? 'bg-purpura-mistico border-purpura-mistico'
                  : 'border-white/30'
              }`}>
                {noNegociables[momento.key] && (
                  <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                  </svg>
                )}
              </div>

              {/* Contenido */}
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-3xl">{momento.emoji}</span>
                  <div>
                    <h3 className="text-lg font-medium">{momento.nombre}</h3>
                    <p className="text-sm text-gray-400">{momento.hora}</p>
                  </div>
                  {momento.defaultValue && (
                    <span className="ml-auto text-xs bg-verde-vida/20 text-verde-vida px-2 py-1 rounded-full">
                      Recomendado
                    </span>
                  )}
                </div>
                <p className="text-sm text-gray-400">{momento.descripcion}</p>
              </div>
            </div>
          </motion.button>
        ))}
      </div>

      {/* Info adicional */}
      <motion.div
        className="p-6 bg-azul-estelar/10 backdrop-blur-sm rounded-2xl border border-azul-estelar/30 mb-8"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        <p className="text-sm text-gray-300 leading-relaxed">
          <strong className="text-azul-estelar">💡 Consejo:</strong> Empieza con Fajr (amanecer), Dhuhr (mediodía) y Maghrib (atardecer). 
          Puedes añadir o quitar momentos más adelante en la configuración.
        </p>
      </motion.div>

      {/* Navegación */}
      <div className="flex justify-between items-center">
        <button
          onClick={onAnterior}
          className="px-8 py-4 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 transition-all"
        >
          ← Anterior
        </button>

        <button
          onClick={onSiguiente}
          disabled={activos === 0}
          className="px-12 py-4 rounded-full bg-gradient-to-r from-purpura-mistico to-azul-estelar hover:shadow-lg hover:shadow-purpura-mistico/50 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
        >
          Siguiente →
        </button>
      </div>
    </motion.div>
  )
}

