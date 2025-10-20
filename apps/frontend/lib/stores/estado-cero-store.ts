import { create } from 'zustand'
import { EstadoCeroCompleto, RespuestaSacral } from '../api-client'

type FaseMeditacion = 'pre-inicio' | 'entrada' | 'expansion' | 'preguntas' | 'sintesis' | 'validacion' | 'completado'

interface EstadoCeroStore {
  // Estado
  fase: FaseMeditacion
  estadoActual: EstadoCeroCompleto | null
  respuestas: RespuestaSacral[]
  direccion: string | null
  cargando: boolean
  error: string | null

  // Acciones
  setFase: (fase: FaseMeditacion) => void
  setEstadoActual: (estado: EstadoCeroCompleto | null) => void
  agregarRespuesta: (respuesta: RespuestaSacral) => void
  setDireccion: (direccion: string) => void
  setCargando: (cargando: boolean) => void
  setError: (error: string | null) => void
  reset: () => void
}

export const useEstadoCeroStore = create<EstadoCeroStore>((set) => ({
  // Estado inicial
  fase: 'pre-inicio',
  estadoActual: null,
  respuestas: [],
  direccion: null,
  cargando: false,
  error: null,

  // Acciones
  setFase: (fase) => set({ fase }),
  
  setEstadoActual: (estado) => set({ estadoActual: estado }),
  
  agregarRespuesta: (respuesta) => set((state) => ({
    respuestas: [...state.respuestas, respuesta]
  })),
  
  setDireccion: (direccion) => set({ direccion }),
  
  setCargando: (cargando) => set({ cargando }),
  
  setError: (error) => set({ error }),
  
  reset: () => set({
    fase: 'pre-inicio',
    estadoActual: null,
    respuestas: [],
    direccion: null,
    cargando: false,
    error: null
  })
}))

