'use client'

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useRouter } from 'next/navigation'
import dynamic from 'next/dynamic'
import { useEstadoCeroStore } from '@/lib/stores/estado-cero-store'
import { estadoCeroAPI, RespuestaSacral } from '@/lib/api-client'
import { obtenerTextosMomento, obtenerConfigMomento } from '@/lib/momento-config'
import { useAudioSagrado } from '@/lib/audio-sagrado'
import PreguntasSacrales from './components/PreguntasSacrales'

// Importar UniversoEsferico dinámicamente (solo cliente)
const UniversoEsferico = dynamic(
  () => import('./components/UniversoEsferico'),
  { ssr: false }
)

type FaseVisual = 'entrada' | 'expansion' | 'preguntas' | 'sintesis'

export default function EstadoCeroPage() {
  const router = useRouter()
  const {
    fase,
    setFase,
    estadoActual,
    setEstadoActual,
    direccion,
    setDireccion,
    cargando,
    setCargando,
    error,
    setError
  } = useEstadoCeroStore()

  const [faseVisual, setFaseVisual] = useState<FaseVisual>('entrada')
  const [mostrarBotonIniciar, setMostrarBotonIniciar] = useState(false)
  const [momentoActual, setMomentoActual] = useState('')
  
  // Audio Sagrado
  const audio = useAudioSagrado()

  useEffect(() => {
    verificarYPrepararEstadoCero()
  }, [])

  useEffect(() => {
    // Mostrar botón después de la animación de entrada
    if (fase === 'pre-inicio') {
      const timer = setTimeout(() => setMostrarBotonIniciar(true), 3000)
      return () => clearTimeout(timer)
    }
  }, [fase])

  async function verificarYPrepararEstadoCero(): Promise<void> {
    try {
      const data = await estadoCeroAPI.verificarMomento()
      console.info('📅 Datos del momento:', data)

      const momento = data.momento_actual || data.momento || 'dhuhr'
      console.info('🕌 Momento detectado:', momento)

      setMomentoActual(momento)
    } catch (err: unknown) {
      console.error('Error verificando momento:', err)
      // Fallback: usar dhuhr como default
      setMomentoActual('dhuhr')
    }
  }

  async function iniciarMeditacion(): Promise<void> {
    setCargando(true)
    setError(null)

    try {
      // 🎵 Sonido inicial
      audio.playTransicion('inicio')
      
      // Fase de entrada (3 segundos)
      setFase('entrada')
      setFaseVisual('entrada')
      await delay(3000)

      // Fase de expansión (3 segundos)
      audio.playTransicion('avance')
      setFase('expansion')
      setFaseVisual('expansion')
      
      // 🎵 Comenzar ambiente del momento litúrgico
      audio.playAmbiente(momentoActual, 30)
      
      await delay(3000)

      // Iniciar Estado Cero en backend con el momento ACTUAL
      console.info('🔮 Iniciando Estado Cero para momento:', momentoActual)
      const estadoIniciado = await estadoCeroAPI.iniciar(momentoActual, true)
      console.info('✅ Estado Cero iniciado:', estadoIniciado)
      
      // Normalizar el objeto: backend retorna estado_cero_id, frontend espera id
      const estadoNormalizado = {
        ...estadoIniciado,
        id: estadoIniciado.estado_cero_id || estadoIniciado.id
      }
      
      setEstadoActual(estadoNormalizado)

      // Pasar a preguntas
      audio.playTransicion('avance')
      setFase('preguntas')
      setFaseVisual('preguntas')
    } catch (err: unknown) {
      console.error('❌ Error iniciando Estado Cero:', err)
      const errorMsg = err instanceof Error ? err.message : String(err)
      setError(errorMsg || 'Error desconocido al iniciar')
      setFase('pre-inicio')
      audio.stop()
    } finally {
      setCargando(false)
    }
  }

  async function onRespuestasCompletadas(respuestas: RespuestaSacral[]): Promise<void> {
    if (!estadoActual) {
      setError('No hay Estado Cero activo')
      return
    }

    setCargando(true)

    try {
      console.info('📝 Enviando respuestas:', respuestas)

      // Enviar todas las respuestas
      for (const respuesta of respuestas) {
        await estadoCeroAPI.responder(estadoActual.id, respuesta)
      }

      // 🎵 Sonido de transición a síntesis
      audio.playTransicion('completado')
      
      // Cambiar a fase de síntesis visual
      setFase('sintesis')
      setFaseVisual('sintesis')
      await delay(2000)

      console.info('🧠 Sintetizando dirección...')

      // Sintetizar dirección emergente
      const resultado = await estadoCeroAPI.sintetizar(estadoActual.id)
      console.info('✅ Dirección generada:', resultado)

      const direccionTexto = resultado.direccion || resultado.direccion_emergente || 'Dirección emergente procesándose...'
      setDireccion(direccionTexto)

      // 🎵 Pulsación profunda durante la reflexión
      audio.playPulsacion(5)

      // Mostrar dirección
      await delay(5000)

      // Completar
      setFase('completado')
      
      // 🎵 Detener audio al completar
      setTimeout(() => audio.stop(), 2000)
    } catch (err: unknown) {
      console.error('❌ Error procesando respuestas:', err)
      const errorMsg = err instanceof Error ? err.message : String(err)
      setError(errorMsg || 'Error procesando respuestas')
      audio.stop()
    } finally {
      setCargando(false)
    }
  }

  function irAValidacion(): void {
    router.push('/estado-cero/validacion')
  }

  function getMomentoIcono(momento: string): string {
    const config = obtenerConfigMomento(momento)
    return config.emoji
  }
  
  // Obtener textos personalizados por momento
  const textos = momentoActual ? obtenerTextosMomento(momentoActual) : obtenerTextosMomento('fajr')

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Universo 3D de fondo */}
      <UniversoEsferico fase={faseVisual} momento={momentoActual} />

      {/* Contenido sobre el universo */}
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-4">
        {/* Error overlay */}
        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50"
          >
            <div className="bg-red-500/20 border border-red-500 rounded-2xl p-8 max-w-md">
              <h3 className="text-xl font-medium mb-4">Error</h3>
              <p className="text-gray-300 mb-6">{typeof error === 'string' ? error : JSON.stringify(error)}</p>
              <button
                onClick={() => {
                  setError(null)
                  setFase('pre-inicio')
                }}
                className="w-full px-6 py-3 bg-red-500 hover:bg-red-600 rounded-full transition-colors"
              >
                Reintentar
              </button>
            </div>
          </motion.div>
        )}

        <AnimatePresence mode="wait">
          {/* Pre-inicio */}
          {fase === 'pre-inicio' && (
            <motion.div
              key="pre-inicio"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 1.05 }}
              transition={{ 
                duration: 0.8, 
                ease: [0.22, 1, 0.36, 1] // Cubic bezier suave
              }}
              className="text-center"
            >
              <motion.h1
                className="text-5xl md:text-7xl font-light mb-6"
                initial={{ y: 40, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ 
                  delay: 0.3, 
                  duration: 1,
                  ease: [0.22, 1, 0.36, 1]
                }}
              >
                {textos.pre_inicio.titulo}
              </motion.h1>
              
              <motion.p
                className="text-xl md:text-2xl text-gray-300 mb-12"
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.8 }}
              >
                {textos.pre_inicio.subtitulo}
              </motion.p>

              {momentoActual && (
                <motion.div
                  className="mb-8 flex items-center justify-center gap-3"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 1.2 }}
                >
                  <span className="text-4xl">{textos.pre_inicio.emoji}</span>
                  <span className="text-2xl capitalize">{momentoActual}</span>
                </motion.div>
              )}

              {mostrarBotonIniciar && (
                <motion.button
                  onClick={iniciarMeditacion}
                  disabled={cargando}
                  className="relative px-12 py-6 text-xl bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 rounded-full overflow-hidden disabled:opacity-50 disabled:cursor-not-allowed"
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  transition={{
                    type: "spring",
                    stiffness: 300,
                    damping: 20
                  }}
                >
                  {/* Efecto de brillo animado */}
                  <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
                    initial={{ x: '-100%' }}
                    animate={{ x: '200%' }}
                    transition={{
                      repeat: Infinity,
                      duration: 3,
                      ease: "linear"
                    }}
                  />
                  
                  {/* Resplandor pulsante */}
                  <motion.div
                    className="absolute inset-0 bg-purple-500/20 blur-xl"
                    animate={{
                      scale: [1, 1.2, 1],
                      opacity: [0.5, 0.8, 0.5]
                    }}
                    transition={{
                      repeat: Infinity,
                      duration: 2,
                      ease: "easeInOut"
                    }}
                  />
                  
                  <span className="relative z-10">
                    {cargando ? 'Preparando el espacio...' : 'Entrar al Estado Cero'}
                  </span>
                </motion.button>
              )}
            </motion.div>
          )}

          {/* Entrada */}
          {fase === 'entrada' && (
            <motion.div
              key="entrada"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 1.1 }}
              transition={{ 
                duration: 1.2, 
                ease: [0.22, 1, 0.36, 1] 
              }}
              className="text-center"
            >
              <motion.div
                className="text-7xl mb-6"
                animate={{ 
                  rotate: [0, 360],
                  scale: [1, 1.2, 1]
                }}
                transition={{ 
                  duration: 3, 
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              >
                {textos.entrada.emoji}
              </motion.div>
              
              <motion.h2
                className="text-4xl md:text-5xl font-light mb-4"
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3, duration: 0.8 }}
              >
                {textos.entrada.titulo}
              </motion.h2>
              
              <motion.p
                className="text-xl text-gray-300"
                initial={{ opacity: 0 }}
                animate={{ opacity: [0, 1, 0.7, 1] }}
                transition={{ 
                  delay: 0.8,
                  duration: 1.5
                }}
              >
                {textos.entrada.subtitulo}
              </motion.p>
            </motion.div>
          )}

          {/* Expansión */}
          {fase === 'expansion' && (
            <motion.div
              key="expansion"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 1.2 }}
              transition={{ 
                duration: 1.5, 
                ease: [0.22, 1, 0.36, 1] 
              }}
              className="text-center"
            >
              {/* Círculo expandiéndose */}
              <motion.div
                className="mx-auto mb-8 w-32 h-32 rounded-full border-2 border-purple-500/30 flex items-center justify-center"
                animate={{ 
                  scale: [1, 1.5, 1],
                  borderColor: [
                    'rgba(168, 85, 247, 0.3)',
                    'rgba(168, 85, 247, 0.8)',
                    'rgba(168, 85, 247, 0.3)'
                  ]
                }}
                transition={{ 
                  duration: 3, 
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              >
                <motion.div
                  className="text-5xl"
                  animate={{ 
                    scale: [1, 0.8, 1]
                  }}
                  transition={{ 
                    duration: 3, 
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                >
                  🌟
                </motion.div>
              </motion.div>
              
              <motion.h2
                className="text-4xl md:text-5xl font-light mb-4"
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.5, duration: 0.8 }}
              >
                {textos.expansion.titulo}
              </motion.h2>
              
              <motion.p
                className="text-xl text-gray-300"
                initial={{ opacity: 0 }}
                animate={{ opacity: [0, 1, 0.7, 1] }}
                transition={{ 
                  delay: 1,
                  duration: 1.5
                }}
              >
                {textos.expansion.subtitulo}
              </motion.p>
            </motion.div>
          )}

          {/* Preguntas */}
          {fase === 'preguntas' && estadoActual && (
            <motion.div
              key="preguntas"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="w-full"
            >
              <PreguntasSacrales
                preguntas={estadoActual.preguntas}
                momento={estadoActual.momento}
                onCompletado={onRespuestasCompletadas}
              />
            </motion.div>
          )}

          {/* Síntesis */}
          {fase === 'sintesis' && (
            <motion.div
              key="sintesis"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="text-center"
            >
              <motion.h2
                className="text-4xl md:text-5xl font-light mb-4"
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                La claridad emerge
              </motion.h2>
              <motion.p
                className="text-xl text-gray-300"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1 }}
              >
                Tu dirección se revela
              </motion.p>

              {direccion && (
                <motion.div
                  className="mt-12 p-8 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 max-w-2xl mx-auto"
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 2 }}
                >
                  <p className="text-sm text-purpura-mistico mb-3 uppercase tracking-wider">
                    Dirección Emergente
                  </p>
                  <blockquote className="text-2xl font-light italic leading-relaxed">
                    "{direccion}"
                  </blockquote>
                </motion.div>
              )}
            </motion.div>
          )}

          {/* Completado */}
          {fase === 'completado' && (
            <motion.div
              key="completado"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="text-center max-w-3xl"
            >
              <motion.div
                className="text-6xl mb-6"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', duration: 0.8 }}
              >
                ✓
              </motion.div>

              <h2 className="text-4xl md:text-5xl font-light mb-6">
                {textos.completado.titulo}
              </h2>
              
              <p className="text-gray-400 mb-6">{textos.completado.subtitulo}</p>

              {direccion && (
                <div className="mb-12 p-8 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10">
                  <p className="text-sm text-purpura-mistico mb-3 uppercase tracking-wider">
                    Tu dirección emergente
                  </p>
                  <blockquote className="text-xl font-light italic leading-relaxed text-gray-200">
                    "{direccion}"
                  </blockquote>
                </div>
              )}

              <motion.button
                onClick={irAValidacion}
                className="px-12 py-6 text-xl bg-gradient-to-r from-purpura-mistico to-azul-estelar rounded-full hover:shadow-2xl hover:shadow-purpura-mistico/50 transition-all"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Continuar → Organizar mi Día
              </motion.button>

              <p className="mt-6 text-sm text-gray-500">
                Valida tu calendario con armonía e inteligencia
              </p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Loading overlay */}
        {cargando && fase !== 'pre-inicio' && fase !== 'preguntas' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-40"
          >
            <div className="text-center">
              <motion.div
                className="w-16 h-16 border-4 border-purpura-mistico border-t-transparent rounded-full mx-auto mb-4"
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
              />
              <p className="text-gray-300">Procesando...</p>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}

// Utilidad para esperar
function delay(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

