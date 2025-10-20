'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronRight, ChevronLeft } from '@/app/components/icons'
import { PreguntaBinaria, RespuestaSacral } from '@/lib/api-client'

interface PreguntasSacralesProps {
  preguntas: PreguntaBinaria[]
  onCompletado: (respuestas: RespuestaSacral[]) => void
  momento?: string
}

export default function PreguntasSacrales({ preguntas, onCompletado, momento }: PreguntasSacralesProps) {
  const [preguntaActual, setPreguntaActual] = useState(0)
  const [respuestas, setRespuestas] = useState<RespuestaSacral[]>([])
  const [sensacionSeleccionada, setSensacionSeleccionada] = useState<'expansion' | 'contraccion' | null>(null)
  const [intensidad, setIntensidad] = useState(3)
  const [nota, setNota] = useState('')

  const pregunta = preguntas[preguntaActual]
  const progreso = ((preguntaActual + 1) / preguntas.length) * 100

  function seleccionarSensacion(sensacion: 'expansion' | 'contraccion') {
    setSensacionSeleccionada(sensacion)
  }

  function siguiente() {
    if (!sensacionSeleccionada) return

    // Guardar respuesta
    const respuesta: RespuestaSacral = {
      pregunta_id: pregunta.id,
      sensacion: sensacionSeleccionada,
      intensidad,
      nota: nota || undefined
    }

    const nuevasRespuestas = [...respuestas, respuesta]
    setRespuestas(nuevasRespuestas)

    // Si es la última pregunta
    if (preguntaActual === preguntas.length - 1) {
      onCompletado(nuevasRespuestas)
    } else {
      // Siguiente pregunta
      setPreguntaActual(preguntaActual + 1)
      setSensacionSeleccionada(null)
      setIntensidad(3)
      setNota('')
    }
  }

  function anterior() {
    if (preguntaActual > 0) {
      setPreguntaActual(preguntaActual - 1)
      // Recuperar respuesta anterior
      const respuestaAnterior = respuestas[preguntaActual - 1]
      setSensacionSeleccionada(respuestaAnterior?.sensacion || null)
      setIntensidad(respuestaAnterior?.intensidad || 3)
      setNota(respuestaAnterior?.nota || '')
      // Remover última respuesta
      setRespuestas(respuestas.slice(0, -1))
    }
  }

  return (
    <div className="relative z-10 w-full max-w-3xl mx-auto px-4">
      {/* Barra de progreso */}
      <motion.div
        className="mb-8"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <div className="h-1 bg-white/10 rounded-full overflow-hidden backdrop-blur-sm">
          <motion.div
            className="h-full bg-gradient-to-r from-purpura-mistico to-azul-estelar"
            initial={{ width: 0 }}
            animate={{ width: `${progreso}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
        <p className="text-sm text-gray-400 mt-2 text-center">
          Pregunta {preguntaActual + 1} de {preguntas.length}
        </p>
      </motion.div>

      {/* Pregunta actual */}
      <AnimatePresence mode="wait">
        <motion.div
          key={preguntaActual}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          {/* Contexto */}
          <motion.p
            className="text-sm text-purpura-mistico mb-4 uppercase tracking-wider"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            {pregunta.contexto}
          </motion.p>

          {/* Pregunta principal */}
          <motion.h2
            className="text-3xl md:text-4xl font-light mb-4 text-balance"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
          >
            {pregunta.pregunta}
          </motion.h2>

          {/* Categoría */}
          <motion.span
            className="inline-block px-4 py-1 bg-white/5 backdrop-blur-sm rounded-full text-sm text-gray-400 border border-white/10"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            {pregunta.categoria}
          </motion.span>
        </motion.div>
      </AnimatePresence>

      {/* Selector de sensación */}
      <motion.div
        className="grid grid-cols-2 gap-6 mb-8"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        {/* Expansión */}
        <motion.button
          onClick={() => seleccionarSensacion('expansion')}
          className={`p-8 rounded-2xl border-2 transition-all duration-300 ${
            sensacionSeleccionada === 'expansion'
              ? 'bg-verde-vida/20 border-verde-vida shadow-lg shadow-verde-vida/30'
              : 'bg-white/5 border-white/10 hover:border-verde-vida/50'
          }`}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <div className="text-5xl mb-3">✨</div>
          <h3 className="text-xl font-medium mb-2">Expansión</h3>
          <p className="text-sm text-gray-400">Mi cuerpo dice sí</p>
        </motion.button>

        {/* Contracción */}
        <motion.button
          onClick={() => seleccionarSensacion('contraccion')}
          className={`p-8 rounded-2xl border-2 transition-all duration-300 ${
            sensacionSeleccionada === 'contraccion'
              ? 'bg-gray-500/20 border-gray-400 shadow-lg shadow-gray-400/30'
              : 'bg-white/5 border-white/10 hover:border-gray-400/50'
          }`}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <div className="text-5xl mb-3">🌑</div>
          <h3 className="text-xl font-medium mb-2">Contracción</h3>
          <p className="text-sm text-gray-400">Mi cuerpo dice no</p>
        </motion.button>
      </motion.div>

      {/* Intensidad y nota (solo si hay sensación seleccionada) */}
      <AnimatePresence>
        {sensacionSeleccionada && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mb-8 space-y-6"
          >
            {/* Slider de intensidad */}
            <div className="p-6 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10">
              <label className="block text-sm text-gray-400 mb-3">
                Intensidad de la sensación
              </label>
              <input
                type="range"
                min="1"
                max="5"
                value={intensidad}
                onChange={(e) => setIntensidad(parseInt(e.target.value))}
                className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-purpura-mistico"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-2">
                <span>Sutil</span>
                <span className="text-lg font-medium text-white">{intensidad}</span>
                <span>Intensa</span>
              </div>
            </div>

            {/* Nota opcional */}
            <div className="p-6 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10">
              <label className="block text-sm text-gray-400 mb-3">
                Nota (opcional)
              </label>
              <textarea
                value={nota}
                onChange={(e) => setNota(e.target.value)}
                placeholder="¿Algo que quieras recordar sobre esta respuesta?"
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-purpura-mistico resize-none"
                rows={3}
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Navegación */}
      <motion.div
        className="flex justify-between items-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        <button
          onClick={anterior}
          disabled={preguntaActual === 0}
          className="flex items-center gap-2 px-6 py-3 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
        >
          <ChevronLeft size={20} />
          <span>Anterior</span>
        </button>

        <button
          onClick={siguiente}
          disabled={!sensacionSeleccionada}
          className="flex items-center gap-2 px-8 py-3 rounded-full bg-gradient-to-r from-purpura-mistico to-azul-estelar hover:shadow-lg hover:shadow-purpura-mistico/50 disabled:opacity-30 disabled:cursor-not-allowed transition-all disabled:hover:shadow-none"
        >
          <span>{preguntaActual === preguntas.length - 1 ? 'Completar' : 'Siguiente'}</span>
          <ChevronRight size={20} />
        </button>
      </motion.div>
    </div>
  )
}

