'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { useEstadoCeroStore } from '@/lib/stores/estado-cero-store'
import { Clock, Plus, Save } from '@/app/components/icons'

interface BloqueIntensivo {
  id: string
  hora_inicio: string
  hora_fin: string
  titulo: string
  tipo: 'creacion' | 'desarrollo' | 'aprendizaje' | 'relaciones'
  energia_fase: 'alta' | 'moderada' | 'baja'
  dimension: string
  color: string
}

const RITMOS_CIRCADIANOS = {
  manana_alta: { inicio: '06:00', fin: '12:00', energia: 'alta', label: 'Mañana (energía alta)', color: '#22C55E' },
  tarde_moderada: { inicio: '14:00', fin: '18:00', energia: 'moderada', label: 'Tarde (energía moderada)', color: '#3B82F6' },
  noche_reflexion: { inicio: '20:00', fin: '22:00', energia: 'baja', label: 'Noche (reflexión)', color: '#8B5CF6' }
}

const TIPOS_BLOQUE = [
  { value: 'creacion', label: 'Creación/Build', emoji: '🎨', dimension: 'creatividad', color: '#8B5CF6' },
  { value: 'desarrollo', label: 'Desarrollo/Código', emoji: '💻', dimension: 'desarrollo', color: '#22C55E' },
  { value: 'aprendizaje', label: 'Aprendizaje', emoji: '📚', dimension: 'conocimiento', color: '#EAB308' },
  { value: 'relaciones', label: 'Relaciones/Reuniones', emoji: '👥', dimension: 'relaciones', color: '#3B82F6' }
]

export default function ValidacionSimplificada() {
  const router = useRouter()
  const { estadoActual, direccion } = useEstadoCeroStore()
  
  const [bloquesIntensivos, setBloquesIntensivos] = useState<BloqueIntensivo[]>([])
  const [guardando, setGuardando] = useState(false)

  useEffect(() => {
    // Generar sugerencia inicial basada en dirección emergente
    generarSugerenciaInicial()
  }, [direccion])

  function generarSugerenciaInicial() {
    // Sugerencia simple: 2 bloques de 90min en fases de alta energía
    const bloquesSugeridos: BloqueIntensivo[] = [
      {
        id: 'b1',
        hora_inicio: '09:00',
        hora_fin: '10:30',
        titulo: 'Bloque de trabajo profundo 1',
        tipo: 'desarrollo',
        energia_fase: 'alta',
        dimension: 'desarrollo',
        color: '#22C55E'
      },
      {
        id: 'b2',
        hora_inicio: '15:00',
        hora_fin: '16:30',
        titulo: 'Bloque de trabajo profundo 2',
        tipo: 'desarrollo',
        energia_fase: 'moderada',
        dimension: 'desarrollo',
        color: '#22C55E'
      }
    ]

    setBloquesIntensivos(bloquesSugeridos)
  }

  function agregarBloque() {
    const nuevoBloque: BloqueIntensivo = {
      id: `b${Date.now()}`,
      hora_inicio: '10:00',
      hora_fin: '11:30',
      titulo: 'Nuevo bloque de trabajo',
      tipo: 'desarrollo',
      energia_fase: 'alta',
      dimension: 'desarrollo',
      color: '#22C55E'
    }

    setBloquesIntensivos([...bloquesIntensivos, nuevoBloque])
  }

  function actualizarBloque(id: string, campo: keyof BloqueIntensivo, valor: any) {
    setBloquesIntensivos(bloques =>
      bloques.map(b => b.id === id ? { ...b, [campo]: valor } : b)
    )
  }

  function cambiarTipo(id: string, tipo: string) {
    const tipoInfo = TIPOS_BLOQUE.find(t => t.value === tipo)
    if (tipoInfo) {
      actualizarBloque(id, 'tipo', tipo as any)
      actualizarBloque(id, 'dimension', tipoInfo.dimension)
      actualizarBloque(id, 'color', tipoInfo.color)
    }
  }

  function eliminarBloque(id: string) {
    setBloquesIntensivos(bloques => bloques.filter(b => b.id !== id))
  }

  async function guardarYFinalizar() {
    setGuardando(true)

    try {
      // Por ahora, solo guardar en localStorage como demo
      // En producción, esto iría a Google Calendar o Anytype
      const configuracionDia = {
        fecha: new Date().toISOString().split('T')[0],
        estado_cero_id: estadoActual?.id,
        direccion_emergente: direccion,
        bloques_intensivos: bloquesIntensivos,
        estructura_no_negociable: {
          fajr: '06:00-06:30',
          dhuhr: '13:00-13:30',
          maghrib: '19:00-19:30'
        }
      }

      localStorage.setItem('configuracion_dia', JSON.stringify(configuracionDia))
      
      console.log('✅ Configuración del día guardada:', configuracionDia)

      // Pequeña pausa para feedback
      await new Promise(resolve => setTimeout(resolve, 500))

      // Ir al inicio o al espejo diario
      alert(`✅ Día organizado con éxito\n\n${bloquesIntensivos.length} bloques de trabajo intenso programados\n\nAhora ve al Espejo Diario (puerto 5173) para ejecutar`)
      
      router.push('/')
    } catch (err: any) {
      console.error('Error:', err)
      alert(`Error guardando: ${  err.message}`)
    } finally {
      setGuardando(false)
    }
  }

  // Calcular tiempo total asignado
  const minutosAsignados = bloquesIntensivos.reduce((acc, b) => {
    const inicio = b.hora_inicio.split(':').map(Number)
    const fin = b.hora_fin.split(':').map(Number)
    const duracion = (fin[0] * 60 + fin[1]) - (inicio[0] * 60 + inicio[1])
    return acc + duracion
  }, 0)

  const horasAsignadas = (minutosAsignados / 60).toFixed(1)
  const porcentajeAsignado = (minutosAsignados / (16 * 60)) * 100
  const porcentajeCaos = 100 - porcentajeAsignado

  return (
    <div className="min-h-screen bg-universo p-6">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <motion.header
          className="text-center mb-12"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-4xl md:text-5xl font-light mb-4">
            🎯 Organiza tu Día
          </h1>
          <p className="text-xl text-gray-300 mb-6">
            Al borde del caos con ritmos circadianos
          </p>
          
          {direccion && (
            <div className="max-w-2xl mx-auto p-6 bg-purpura-mistico/10 backdrop-blur-sm rounded-2xl border border-purpura-mistico/30">
              <p className="text-sm text-purpura-mistico mb-2 uppercase tracking-wider">Tu Dirección Emergente</p>
              <blockquote className="text-lg italic text-gray-200">
                "{direccion}"
              </blockquote>
            </div>
          )}
        </motion.header>

        {/* Métrica al borde del caos */}
        <motion.div
          className="mb-8 p-6 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-lg font-medium">Al Borde del Caos</h3>
              <p className="text-sm text-gray-400">{horasAsignadas}h de trabajo intenso</p>
            </div>
            <div className="text-right">
              <div className={`text-3xl font-bold ${porcentajeCaos >= 30 && porcentajeCaos <= 50 ? 'text-verde-vida' : 'text-yellow-500'}`}>
                {porcentajeCaos.toFixed(0)}%
              </div>
              <div className="text-xs text-gray-400">sin asignar</div>
            </div>
          </div>
          <div className="h-3 bg-white/10 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-500 ${porcentajeCaos >= 30 && porcentajeCaos <= 50 ? 'bg-verde-vida' : 'bg-yellow-500'}`}
              style={{ width: `${porcentajeAsignado}%` }}
            />
          </div>
          <p className="text-xs text-gray-500 mt-2">
            {porcentajeCaos >= 30 && porcentajeCaos <= 50 ? '✓ Equilibrio perfecto' : '⚠️ Ideal: 30-50% sin asignar'}
          </p>
        </motion.div>

        {/* Ritmos Circadianos (Info) */}
        <motion.div
          className="mb-6 p-4 bg-azul-estelar/10 backdrop-blur-sm rounded-xl border border-azul-estelar/30"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <p className="text-sm text-gray-300">
            <strong className="text-azul-estelar">💡 Ritmos Circadianos:</strong> Mañana (6-12h) energía alta para creación · Tarde (14-18h) energía moderada para ejecución · Noche (20-22h) energía baja para reflexión
          </p>
        </motion.div>

        {/* Bloques de Trabajo Intensivo */}
        <div className="space-y-4 mb-8">
          <h3 className="text-xl font-medium mb-4">Bloques de Trabajo Intensivo</h3>
          
          {bloquesIntensivos.map((bloque, index) => (
            <motion.div
              key={bloque.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-6 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10"
            >
              <div className="grid md:grid-cols-4 gap-4">
                {/* Horario */}
                <div>
                  <label className="block text-xs text-gray-400 mb-2">Horario</label>
                  <div className="flex items-center gap-2">
                    <input
                      type="time"
                      value={bloque.hora_inicio}
                      onChange={(e) => actualizarBloque(bloque.id, 'hora_inicio', e.target.value)}
                      className="w-full bg-white/5 border border-white/20 rounded-lg px-3 py-2 focus:outline-none focus:border-purpura-mistico"
                    />
                    <span className="text-gray-500">-</span>
                    <input
                      type="time"
                      value={bloque.hora_fin}
                      onChange={(e) => actualizarBloque(bloque.id, 'hora_fin', e.target.value)}
                      className="w-full bg-white/5 border border-white/20 rounded-lg px-3 py-2 focus:outline-none focus:border-purpura-mistico"
                    />
                  </div>
                </div>

                {/* Tipo */}
                <div>
                  <label className="block text-xs text-gray-400 mb-2">Tipo de Actividad</label>
                  <select
                    value={bloque.tipo}
                    onChange={(e) => cambiarTipo(bloque.id, e.target.value)}
                    className="w-full bg-white/5 border border-white/20 rounded-lg px-3 py-2 focus:outline-none focus:border-purpura-mistico"
                  >
                    {TIPOS_BLOQUE.map(tipo => (
                      <option key={tipo.value} value={tipo.value}>
                        {tipo.emoji} {tipo.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Título */}
                <div className="md:col-span-2">
                  <label className="block text-xs text-gray-400 mb-2">¿Qué vas a hacer?</label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={bloque.titulo}
                      onChange={(e) => actualizarBloque(bloque.id, 'titulo', e.target.value)}
                      className="flex-1 bg-white/5 border border-white/20 rounded-lg px-4 py-2 focus:outline-none focus:border-purpura-mistico"
                      placeholder="Ej: Desarrollar feature X, Escribir artículo..."
                    />
                    <button
                      onClick={() => eliminarBloque(bloque.id)}
                      className="px-4 py-2 bg-red-500/20 text-red-400 rounded-lg hover:bg-red-500/30 transition-colors"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              </div>

              {/* Info del bloque */}
              <div className="mt-3 flex items-center gap-4 text-sm text-gray-400">
                <span className="flex items-center gap-1">
                  <Clock size={14} />
                  {calcularDuracion(bloque.hora_inicio, bloque.hora_fin)}
                </span>
                <span 
                  className="px-2 py-1 rounded text-xs font-medium"
                  style={{ backgroundColor: `${bloque.color}20`, color: bloque.color }}
                >
                  {bloque.dimension}
                </span>
              </div>
            </motion.div>
          ))}

          {/* Botón añadir */}
          {bloquesIntensivos.length < 4 && (
            <button
              onClick={agregarBloque}
              className="w-full p-4 border-2 border-dashed border-white/20 rounded-xl hover:border-purpura-mistico hover:bg-purpura-mistico/10 transition-all flex items-center justify-center gap-2"
            >
              <Plus size={20} />
              <span>Añadir Bloque de Trabajo (máx 4)</span>
            </button>
          )}
        </div>

        {/* Estructura No-Negociable (Info) */}
        <motion.div
          className="mb-8 p-6 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <h3 className="text-lg font-medium mb-4">🔴 Estructura No-Negociable (Anclada)</h3>
          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div className="flex items-center gap-3">
              <span className="text-2xl">🌅</span>
              <div>
                <p className="font-medium">Fajr - 06:00</p>
                <p className="text-gray-400">Estado Cero</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-2xl">☀️</span>
              <div>
                <p className="font-medium">Dhuhr - 13:00</p>
                <p className="text-gray-400">Estado Cero</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-2xl">🌅</span>
              <div>
                <p className="font-medium">Maghrib - 19:00</p>
                <p className="text-gray-400">Validación</p>
              </div>
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-4">
            Estos momentos están anclados según tu configuración. El resto del día es flexible.
          </p>
        </motion.div>

        {/* Acciones */}
        <div className="flex justify-between items-center">
          <button
            onClick={() => router.push('/')}
            className="px-8 py-4 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 transition-all"
          >
            ← Volver
          </button>

          <button
            onClick={guardarYFinalizar}
            disabled={guardando || bloquesIntensivos.length === 0}
            className="px-12 py-6 text-xl font-medium rounded-full bg-gradient-to-r from-purpura-mistico to-azul-estelar hover:shadow-2xl hover:shadow-purpura-mistico/50 disabled:opacity-30 disabled:cursor-not-allowed transition-all flex items-center gap-3"
          >
            {guardando ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Guardando...
              </>
            ) : (
              <>
                <Save size={20} />
                Guardar y Finalizar
              </>
            )}
          </button>
        </div>

        {/* Ayuda */}
        <motion.div
          className="mt-8 p-4 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <p className="text-sm text-gray-400">
            <strong className="text-white">💡 Consejo:</strong> 2-3 bloques de 90 minutos son ideales. Respeta tus ritmos circadianos: mañana para creación, tarde para ejecución, noche para reflexión.
          </p>
        </motion.div>
      </div>
    </div>
  )
}

function calcularDuracion(inicio: string, fin: string): string {
  const [hi, mi] = inicio.split(':').map(Number)
  const [hf, mf] = fin.split(':').map(Number)
  
  const minutosInicio = hi * 60 + mi
  const minutosFin = hf * 60 + mf
  const duracion = minutosFin - minutosInicio
  
  const horas = Math.floor(duracion / 60)
  const mins = duracion % 60
  
  if (horas > 0 && mins > 0) return `${horas}h ${mins}min`
  if (horas > 0) return `${horas}h`
  return `${mins}min`
}
