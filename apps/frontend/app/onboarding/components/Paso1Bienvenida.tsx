'use client'

import { motion } from 'framer-motion'

interface Paso1BienvenidaProps {
  onSiguiente: () => void
}

export default function Paso1Bienvenida({ onSiguiente }: Paso1BienvenidaProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="max-w-3xl mx-auto text-center"
    >
      {/* Logo/Icono */}
      <motion.div
        className="text-8xl mb-8"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ type: 'spring', duration: 0.8, delay: 0.2 }}
      >
        🕌
      </motion.div>

      {/* Título */}
      <motion.h1
        className="text-5xl md:text-6xl font-light mb-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        Bienvenido al Campo Sagrado
      </motion.h1>

      {/* Subtítulo */}
      <motion.p
        className="text-xl md:text-2xl text-gray-300 mb-12 leading-relaxed"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        Un organismo tecnológico-espiritual que respeta tu{' '}
        <span className="text-purpura-mistico font-medium">autoridad sacral</span>
      </motion.p>

      {/* Características */}
      <motion.div
        className="grid md:grid-cols-3 gap-6 mb-12"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
      >
        <div className="p-6 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10">
          <div className="text-4xl mb-3">⚡</div>
          <h3 className="text-lg font-medium mb-2">Al Borde del Caos</h3>
          <p className="text-sm text-gray-400">
            40% de tu tiempo sin asignar para lo emergente
          </p>
        </div>

        <div className="p-6 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10">
          <div className="text-4xl mb-3">🌙</div>
          <h3 className="text-lg font-medium mb-2">5 Momentos Litúrgicos</h3>
          <p className="text-sm text-gray-400">
            Estados Cero alineados con tiempos sagrados
          </p>
        </div>

        <div className="p-6 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10">
          <div className="text-4xl mb-3">🎨</div>
          <h3 className="text-lg font-medium mb-2">7 Dimensiones</h3>
          <p className="text-sm text-gray-400">
            El arcoíris completo de tu vida
          </p>
        </div>
      </motion.div>

      {/* Filosofía */}
      <motion.div
        className="p-8 bg-purpura-mistico/10 backdrop-blur-sm rounded-2xl border border-purpura-mistico/30 mb-12"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 1 }}
      >
        <p className="text-lg leading-relaxed italic text-gray-200">
          "El sistema se adapta a ti, no tú al sistema. Tomemos unos minutos para 
          configurar tu experiencia personal según tu realidad única."
        </p>
      </motion.div>

      {/* Botón */}
      <motion.button
        onClick={onSiguiente}
        className="px-12 py-5 text-xl font-medium bg-gradient-to-r from-purpura-mistico to-azul-estelar rounded-full hover:shadow-2xl hover:shadow-purpura-mistico/50 transition-all"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 1.2 }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        Comenzar Configuración →
      </motion.button>

      {/* Footer */}
      <motion.p
        className="mt-8 text-sm text-gray-500"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.4 }}
      >
        4 pasos rápidos · 2-3 minutos · Se guarda automáticamente
      </motion.p>
    </motion.div>
  )
}

