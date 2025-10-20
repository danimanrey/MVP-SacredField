'use client'

import { useEffect } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import dynamic from 'next/dynamic'
import { useOnboardingStore } from '@/lib/stores/onboarding-store'

// Importar componentes de pasos
import Paso1Bienvenida from './components/Paso1Bienvenida'
import Paso2NoNegociables from './components/Paso2NoNegociables'
import Paso3Contexto from './components/Paso3Contexto'
import Paso4ExpresionLibre from './components/Paso4ExpresionLibre'

// Universo de fondo (solo cliente)
const UniversoEsferico = dynamic(
  () => import('../estado-cero/components/UniversoEsferico'),
  { ssr: false }
)

export default function OnboardingPage() {
  const { pasoActual, setPaso, siguientePaso, anteriorPaso } = useOnboardingStore()

  // Scroll al top al cambiar de paso
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, [pasoActual])

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Universo 3D de fondo */}
      <div className="fixed inset-0 z-0">
        <UniversoEsferico fase="entrada" />
      </div>

      {/* Contenido */}
      <div className="relative z-10 min-h-screen flex flex-col">
        {/* Header con progreso */}
        <header className="p-6">
          <div className="max-w-4xl mx-auto">
            {/* Barra de progreso */}
            <div className="flex items-center gap-2 mb-4">
              {[1, 2, 3, 4].map((paso) => (
                <div
                  key={paso}
                  className="flex-1 relative"
                >
                  <div
                    className={`h-1 rounded-full transition-all duration-500 ${
                      paso <= pasoActual
                        ? 'bg-gradient-to-r from-purpura-mistico to-azul-estelar'
                        : 'bg-white/10'
                    }`}
                  />
                  {paso === pasoActual && (
                    <motion.div
                      className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-3 h-3 bg-purpura-mistico rounded-full"
                      layoutId="active-step"
                    />
                  )}
                </div>
              ))}
            </div>

            {/* Indicador de paso */}
            <div className="flex justify-between text-xs text-gray-400">
              <span className={pasoActual === 1 ? 'text-white font-medium' : ''}>Bienvenida</span>
              <span className={pasoActual === 2 ? 'text-white font-medium' : ''}>No-Negociables</span>
              <span className={pasoActual === 3 ? 'text-white font-medium' : ''}>Contexto</span>
              <span className={pasoActual === 4 ? 'text-white font-medium' : ''}>Expresión</span>
            </div>
          </div>
        </header>

        {/* Pasos del wizard */}
        <main className="flex-1 flex items-center justify-center p-6 py-12">
          <AnimatePresence mode="wait">
            {pasoActual === 1 && (
              <Paso1Bienvenida
                key="paso1"
                onSiguiente={siguientePaso}
              />
            )}

            {pasoActual === 2 && (
              <Paso2NoNegociables
                key="paso2"
                onSiguiente={siguientePaso}
                onAnterior={anteriorPaso}
              />
            )}

            {pasoActual === 3 && (
              <Paso3Contexto
                key="paso3"
                onSiguiente={siguientePaso}
                onAnterior={anteriorPaso}
              />
            )}

            {pasoActual === 4 && (
              <Paso4ExpresionLibre
                key="paso4"
                onAnterior={anteriorPaso}
              />
            )}
          </AnimatePresence>
        </main>

        {/* Footer */}
        <footer className="p-6 text-center text-sm text-gray-500">
          <p>إن شاء الله - Si Dios quiere</p>
        </footer>
      </div>
    </div>
  )
}

