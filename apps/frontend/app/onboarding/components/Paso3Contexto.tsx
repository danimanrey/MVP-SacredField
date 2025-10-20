'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useOnboardingStore } from '@/lib/stores/onboarding-store'
import { configuracionAPI, type Dimension } from '@/lib/api-client'

interface Paso3ContextoProps {
  onSiguiente: () => void
  onAnterior: () => void
}

export default function Paso3Contexto({ onSiguiente, onAnterior }: Paso3ContextoProps) {
  const {
    configuracion,
    setDimensiones,
    setEnergiaDisponible,
    setContextoFinanciero,
    setContextoBiologico
  } = useOnboardingStore()

  const [dimensionesDisponibles, setDimensionesDisponibles] = useState<Dimension[]>([])
  const [cargando, setCargando] = useState(true)

  useEffect(() => {
    cargarDimensiones()
  }, [])

  async function cargarDimensiones() {
    try {
      const dims = await configuracionAPI.obtenerDimensiones()
      setDimensionesDisponibles(dims)
    } catch (err) {
      console.error('Error cargando dimensiones:', err)
    } finally {
      setCargando(false)
    }
  }

  const toggleDimension = (dimensionId: string) => {
    const actual = configuracion.dimensiones_prioritarias || []
    if (actual.includes(dimensionId)) {
      setDimensiones(actual.filter(d => d !== dimensionId))
    } else {
      setDimensiones([...actual, dimensionId])
    }
  }

  const dimensionesSeleccionadas = configuracion.dimensiones_prioritarias || []
  const contextoFinanciero = configuracion.contexto_financiero || { runway_meses: 6, urgencia: false }
  const contextoBiologico = configuracion.contexto_biologico || { patron_sueno: 'regular', nivel_energia: 3, ejercicio_regular: false }
  const energiaDisponible = configuracion.energia_disponible || 3

  // Validar que al menos una dimensión esté seleccionada (pero ser flexible)
  const puedeAvanzar = true // Siempre permitir avanzar para no bloquear

  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      className="max-w-5xl mx-auto"
    >
      {/* Header */}
      <div className="text-center mb-12">
        <h2 className="text-4xl md:text-5xl font-light mb-4">
          Tu Contexto Individual
        </h2>
        <p className="text-xl text-gray-300">
          Ayúdanos a entender tu realidad actual
        </p>
      </div>

      <div className="space-y-12">
        {/* Sección Financiera */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="p-8 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10"
        >
          <h3 className="text-2xl font-medium mb-6 flex items-center gap-3">
            <span>💰</span>
            Contexto Financiero
          </h3>

          <div className="space-y-6">
            {/* Runway */}
            <div>
              <label className="block text-sm text-gray-400 mb-3">
                ¿Cuál es tu runway actual? (meses de ahorro)
              </label>
              <input
                type="number"
                min="0"
                max="60"
                value={contextoFinanciero.runway_meses}
                onChange={(e) => setContextoFinanciero({
                  ...contextoFinanciero,
                  runway_meses: parseInt(e.target.value) || 0
                })}
                className="w-full bg-white/5 border border-white/20 rounded-lg px-6 py-4 text-2xl font-medium focus:outline-none focus:border-purpura-mistico transition-colors"
              />
              <p className="text-xs text-gray-500 mt-2">
                Tu capacidad económica sin ingresos
              </p>
            </div>

            {/* Urgencia */}
            <div>
              <label className="block text-sm text-gray-400 mb-3">
                ¿Tienes urgencia financiera?
              </label>
              <div className="flex gap-4">
                <button
                  onClick={() => setContextoFinanciero({ ...contextoFinanciero, urgencia: false })}
                  className={`flex-1 p-4 rounded-xl border-2 transition-all ${
                    !contextoFinanciero.urgencia
                      ? 'bg-verde-vida/20 border-verde-vida'
                      : 'bg-white/5 border-white/10 hover:border-white/30'
                  }`}
                >
                  <div className="text-2xl mb-2">😌</div>
                  <div className="font-medium">No, estoy estable</div>
                </button>
                <button
                  onClick={() => setContextoFinanciero({ ...contextoFinanciero, urgencia: true })}
                  className={`flex-1 p-4 rounded-xl border-2 transition-all ${
                    contextoFinanciero.urgencia
                      ? 'bg-red-500/20 border-red-500'
                      : 'bg-white/5 border-white/10 hover:border-white/30'
                  }`}
                >
                  <div className="text-2xl mb-2">⚡</div>
                  <div className="font-medium">Sí, necesito ingresos</div>
                </button>
              </div>
            </div>
          </div>
        </motion.section>

        {/* Dimensiones Prioritarias */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="p-8 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10"
        >
          <h3 className="text-2xl font-medium mb-4 flex items-center gap-3">
            <span>🌈</span>
            Dimensiones Prioritarias
          </h3>
          <p className="text-sm text-gray-400 mb-6">
            Selecciona las áreas que son más importantes para ti ahora (puedes seleccionar varias o ninguna)
          </p>

          {cargando ? (
            <div className="text-center py-8">
              <div className="inline-block w-8 h-8 border-4 border-purpura-mistico border-t-transparent rounded-full animate-spin" />
              <p className="text-sm text-gray-400 mt-3">Cargando dimensiones...</p>
            </div>
          ) : dimensionesDisponibles.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-red-400 mb-4">No se pudieron cargar las dimensiones</p>
              <p className="text-xs text-gray-500">Puedes continuar y configurarlas después</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {dimensionesDisponibles.map((dim) => (
                <button
                  key={dim.id}
                  type="button"
                  onClick={() => toggleDimension(dim.id)}
                  className={`p-4 rounded-xl border-2 transition-all hover:scale-105 ${
                    dimensionesSeleccionadas.includes(dim.id)
                      ? 'border-2 shadow-lg'
                      : 'bg-white/5 border-white/10 hover:border-white/30'
                  }`}
                  style={{
                    backgroundColor: dimensionesSeleccionadas.includes(dim.id)
                      ? `${dim.color}20`
                      : undefined,
                    borderColor: dimensionesSeleccionadas.includes(dim.id)
                      ? dim.color
                      : undefined
                  }}
                >
                  <div className="text-3xl mb-2">{dim.emoji}</div>
                  <div className="font-medium text-sm">{dim.nombre}</div>
                  {dimensionesSeleccionadas.includes(dim.id) && (
                    <div className="mt-2">
                      <svg className="w-5 h-5 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    </div>
                  )}
                </button>
              ))}
            </div>
          )}
          
          {dimensionesSeleccionadas.length > 0 && (
            <div className="mt-4 text-sm text-gray-400 text-center">
              {dimensionesSeleccionadas.length} dimensión{dimensionesSeleccionadas.length > 1 ? 'es' : ''} seleccionada{dimensionesSeleccionadas.length > 1 ? 's' : ''}
            </div>
          )}
        </motion.section>

        {/* Sección Biológica */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="p-8 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10"
        >
          <h3 className="text-2xl font-medium mb-6 flex items-center gap-3">
            <span>🧘</span>
            Contexto Biológico
          </h3>

          <div className="space-y-6">
            {/* Energía */}
            <div>
              <label className="block text-sm text-gray-400 mb-3">
                ¿Cuánta energía disponible tienes diariamente?
              </label>
              <input
                type="range"
                min="1"
                max="5"
                value={energiaDisponible}
                onChange={(e) => setEnergiaDisponible(parseInt(e.target.value))}
                className="w-full h-3 bg-white/10 rounded-lg appearance-none cursor-pointer accent-purpura-mistico"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-2">
                <span>Muy baja</span>
                <span className="text-2xl text-white font-medium">{energiaDisponible}/5</span>
                <span>Muy alta</span>
              </div>
            </div>

            {/* Patrón de sueño */}
            <div>
              <label className="block text-sm text-gray-400 mb-3">
                ¿Cuál es tu patrón de sueño?
              </label>
              <div className="grid grid-cols-3 gap-4">
                {['regular', 'irregular', 'insomnio'].map((patron) => (
                  <button
                    key={patron}
                    onClick={() => setContextoBiologico({ ...contextoBiologico, patron_sueno: patron })}
                    className={`p-4 rounded-xl border-2 transition-all capitalize ${
                      contextoBiologico.patron_sueno === patron
                        ? 'bg-purpura-mistico/20 border-purpura-mistico'
                        : 'bg-white/5 border-white/10 hover:border-white/30'
                    }`}
                  >
                    {patron}
                  </button>
                ))}
              </div>
            </div>

            {/* Ejercicio */}
            <div>
              <label className="block text-sm text-gray-400 mb-3">
                ¿Haces ejercicio regularmente?
              </label>
              <div className="flex gap-4">
                <button
                  onClick={() => setContextoBiologico({ ...contextoBiologico, ejercicio_regular: true })}
                  className={`flex-1 p-4 rounded-xl border-2 transition-all ${
                    contextoBiologico.ejercicio_regular
                      ? 'bg-verde-vida/20 border-verde-vida'
                      : 'bg-white/5 border-white/10 hover:border-white/30'
                  }`}
                >
                  Sí
                </button>
                <button
                  onClick={() => setContextoBiologico({ ...contextoBiologico, ejercicio_regular: false })}
                  className={`flex-1 p-4 rounded-xl border-2 transition-all ${
                    !contextoBiologico.ejercicio_regular
                      ? 'bg-gray-500/20 border-gray-400'
                      : 'bg-white/5 border-white/10 hover:border-white/30'
                  }`}
                >
                  No
                </button>
              </div>
            </div>
          </div>
        </motion.section>
      </div>

      {/* Navegación */}
      <div className="flex justify-between items-center mt-12">
        <button
          onClick={onAnterior}
          className="px-8 py-4 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 transition-all"
        >
          ← Anterior
        </button>

        <button
          onClick={onSiguiente}
          className="px-12 py-4 rounded-full bg-gradient-to-r from-purpura-mistico to-azul-estelar hover:shadow-lg hover:shadow-purpura-mistico/50 transition-all"
        >
          Siguiente →
        </button>
      </div>
    </motion.div>
  )
}

