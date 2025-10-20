'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { configuracionAPI } from '@/lib/api-client'

export default function Home() {
  const router = useRouter()
  const [mounted, setMounted] = useState(false)
  const [verificando, setVerificando] = useState(true)
  const [tieneConfiguracion, setTieneConfiguracion] = useState(false)
  const [momentoActual, setMomentoActual] = useState<string>('')
  const [siguienteEstadoCero, setSiguienteEstadoCero] = useState<string>('')

  useEffect(() => {
    setMounted(true)
    verificarConfiguracion()
  }, [])

  async function verificarConfiguracion() {
    try {
      // Verificar si existe configuración
      const response = await configuracionAPI.obtener()
      
      // TEMPORALMENTE: Permitir continuar sin configuración para testing
      // TODO: Activar redirección cuando el wizard esté 100% funcional
      if (response.status === 'not_found' || !response.configuracion) {
        console.log('⚠️ No hay configuración, pero permitiendo continuar para testing')
        // router.push('/onboarding') // Comentado temporalmente
      }

      // Siempre mostrar landing
      setTieneConfiguracion(true)
      await verificarMomento()
    } catch (err) {
      console.error('Error verificando configuración:', err)
      // En caso de error, permitir continuar
      setTieneConfiguracion(true)
      await verificarMomento()
    } finally {
      setVerificando(false)
    }
  }

  async function verificarMomento() {
    try {
      const res = await fetch('http://localhost:8000/api/estado-cero/verificar')
      const data = await res.json()
      setMomentoActual(data.momento_actual)
      setSiguienteEstadoCero(data.siguiente_estado_cero)
    } catch (err) {
      console.error('Error verificando momento:', err)
    }
  }

  if (!mounted || verificando) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-universo">
        <div className="text-center">
          <div className="text-6xl mb-4 animate-pulse">🕌</div>
          <p className="text-gray-400">Preparando tu espacio...</p>
        </div>
      </div>
    )
  }

  if (!tieneConfiguracion) {
    return null // Redirigiendo a onboarding
  }

  return (
    <main className="min-h-screen relative overflow-hidden">
      {/* Fondo de estrellas */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(100)].map((_, i) => (
          <div
            key={i}
            className="star"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              '--duration': `${2 + Math.random() * 4}s`,
            } as React.CSSProperties}
          />
        ))}
      </div>

      {/* Contenido principal */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="text-center max-w-4xl"
        >
          {/* Logo/Título */}
          <motion.h1
            className="text-6xl md:text-8xl font-light mb-6 text-balance"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1.2, delay: 0.2 }}
          >
            🕌
          </motion.h1>

          <motion.h2
            className="text-4xl md:text-6xl font-light mb-4 text-balance"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1, delay: 0.4 }}
          >
            Campo Sagrado
          </motion.h2>

          <motion.p
            className="text-xl md:text-2xl text-gray-300 mb-12 text-balance"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1, delay: 0.6 }}
          >
            Un organismo tecnológico-espiritual
            <br />
            que opera al borde del caos
          </motion.p>

          {/* Información del momento */}
          {momentoActual && (
            <motion.div
              className="mb-12 p-6 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.8 }}
            >
              <p className="text-sm text-gray-400 mb-2">Momento litúrgico</p>
              <p className="text-2xl font-medium capitalize mb-4">{momentoActual}</p>
              {siguienteEstadoCero && (
                <p className="text-sm text-gray-400">
                  Próximo Estado Cero: <span className="text-white">{siguienteEstadoCero}</span>
                </p>
              )}
            </motion.div>
          )}

          {/* Botón principal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 1 }}
          >
            <Link href="/estado-cero">
              <motion.button
                className="group relative px-12 py-6 text-xl font-medium text-white bg-gradient-to-r from-purpura-mistico to-azul-estelar rounded-full overflow-hidden shadow-2xl shadow-purpura-mistico/50"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <span className="relative z-10">Entrar al Estado Cero</span>
                <motion.div
                  className="absolute inset-0 bg-white"
                  initial={{ scale: 0, opacity: 0 }}
                  whileHover={{ scale: 1, opacity: 0.1 }}
                  transition={{ duration: 0.4 }}
                />
              </motion.button>
            </Link>
          </motion.div>

          {/* Información adicional */}
          <motion.div
            className="mt-16 text-sm text-gray-500"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1, delay: 1.2 }}
          >
            <p>5 momentos litúrgicos diarios · 40% al borde del caos · Autoridad sacral respetada</p>
          </motion.div>
        </motion.div>

        {/* Footer */}
        <motion.div
          className="absolute bottom-8 text-center text-sm text-gray-600"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 1.5 }}
        >
          <p>إن شاء الله - Si Dios quiere</p>
        </motion.div>
      </div>
    </main>
  )
}

