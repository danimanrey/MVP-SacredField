'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { useOnboardingStore } from '@/lib/stores/onboarding-store'
import { configuracionAPI } from '@/lib/api-client'

interface Paso4ExpresionLibreProps {
  onAnterior: () => void
}

export default function Paso4ExpresionLibre({ onAnterior }: Paso4ExpresionLibreProps) {
  const router = useRouter()
  const { configuracion, setExpresionLibre, getConfiguracionCompleta } = useOnboardingStore()
  const [guardando, setGuardando] = useState(false)
  const [error, setError] = useState('')

  const expresion = configuracion.expresion_libre || ''

  async function finalizar() {
    if (guardando) return // Evitar doble click
    
    setGuardando(true)
    setError('')

    try {
      // Obtener configuración completa
      const configCompleta = getConfiguracionCompleta()
      
      console.log('💾 Guardando configuración:', configCompleta)

      // Guardar en backend
      const response = await configuracionAPI.guardar(configCompleta)
      
      console.log('✅ Configuración guardada:', response)

      // Pequeña pausa para feedback visual
      await new Promise(resolve => setTimeout(resolve, 500))

      // Redirigir a Estado Cero
      router.push('/estado-cero')
    } catch (err: any) {
      console.error('❌ Error guardando configuración:', err)
      setError(err.message || 'Error guardando configuración')
      setGuardando(false)
    }
  }

  const caracteresRestantes = 1000 - expresion.length

  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      className="max-w-4xl mx-auto"
    >
      {/* Header */}
      <div className="text-center mb-12">
        <motion.div
          className="text-6xl mb-6"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', duration: 0.6 }}
        >
          ✍️
        </motion.div>
        <h2 className="text-4xl md:text-5xl font-light mb-4">
          Expresión Libre
        </h2>
        <p className="text-xl text-gray-300">
          Comparte lo que sientas relevante sobre tu situación actual
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Campo opcional · Útil para personalizar tu experiencia
        </p>
      </div>

      {/* Textarea */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="mb-8"
      >
        <textarea
          value={expresion}
          onChange={(e) => setExpresionLibre(e.target.value)}
          placeholder="Ejemplo: Estoy en transición profesional. Dejé mi trabajo hace 3 meses para dedicarme a mi proyecto, pero necesito generar ingresos en los próximos 6 meses. Me siento con energía pero también ansiedad por el dinero. Quiero usar este sistema para mantener claridad y no dispersarme..."
          className="w-full h-64 bg-white/5 border border-white/20 rounded-2xl px-6 py-4 text-gray-200 placeholder-gray-600 focus:outline-none focus:border-purpura-mistico resize-none transition-colors"
          maxLength={1000}
        />
        <div className="flex justify-between items-center mt-2 px-2">
          <p className="text-xs text-gray-500">
            Esto ayuda a Claude a entender mejor tu contexto
          </p>
          <p className={`text-xs ${caracteresRestantes < 100 ? 'text-red-400' : 'text-gray-500'}`}>
            {caracteresRestantes} caracteres restantes
          </p>
        </div>
      </motion.div>

      {/* Ejemplos */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="p-6 bg-azul-estelar/10 backdrop-blur-sm rounded-2xl border border-azul-estelar/30 mb-8"
      >
        <p className="text-sm font-medium text-azul-estelar mb-3">💡 Sugerencias de qué compartir:</p>
        <ul className="text-sm text-gray-300 space-y-2">
          <li>• Tu situación laboral o profesional actual</li>
          <li>• Proyectos en los que estás trabajando</li>
          <li>• Desafíos o preocupaciones principales</li>
          <li>• Lo que quieres lograr con este sistema</li>
          <li>• Cualquier contexto relevante de tu vida</li>
        </ul>
      </motion.div>

      {/* Error */}
      {error && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="p-4 bg-red-500/20 border border-red-500 rounded-xl mb-8"
        >
          <p className="text-red-300">{error}</p>
        </motion.div>
      )}

      {/* Resumen */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="p-8 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 mb-8"
      >
        <h3 className="text-lg font-medium mb-4">✨ Resumen de tu configuración:</h3>
        <div className="grid md:grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-400 mb-1">No-negociables activos:</p>
            <p className="font-medium">
              {Object.values(configuracion.no_negociables || {}).filter(Boolean).length} momentos
            </p>
          </div>
          <div>
            <p className="text-gray-400 mb-1">Dimensiones prioritarias:</p>
            <p className="font-medium">
              {(configuracion.dimensiones_prioritarias || []).length} seleccionadas
            </p>
          </div>
          <div>
            <p className="text-gray-400 mb-1">Runway financiero:</p>
            <p className="font-medium">
              {configuracion.contexto_financiero?.runway_meses || 0} meses
            </p>
          </div>
          <div>
            <p className="text-gray-400 mb-1">Energía disponible:</p>
            <p className="font-medium">
              {configuracion.energia_disponible || 3}/5
            </p>
          </div>
        </div>
      </motion.div>

      {/* Navegación */}
      <div className="flex justify-between items-center">
        <button
          onClick={onAnterior}
          disabled={guardando}
          className="px-8 py-4 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 transition-all disabled:opacity-30"
          type="button"
        >
          ← Anterior
        </button>

        <button
          onClick={finalizar}
          disabled={guardando}
          className="px-12 py-6 text-xl font-medium rounded-full bg-gradient-to-r from-purpura-mistico to-azul-estelar hover:shadow-2xl hover:shadow-purpura-mistico/50 disabled:opacity-50 transition-all flex items-center gap-3 cursor-pointer"
          type="button"
        >
          {guardando ? (
            <>
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Guardando...
            </>
          ) : (
            <>
              ✓ Guardar y Comenzar
            </>
          )}
        </button>
      </div>

      {/* Footer */}
      <motion.p
        className="text-center mt-8 text-sm text-gray-500"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
      >
        Tu configuración se guardará y podrás editarla más adelante
      </motion.p>
    </motion.div>
  )
}

