import { create } from 'zustand'
import { 
  ConfiguracionIndividual, 
  NoNegociables, 
  ContextoFinanciero, 
  ContextoBiologico 
} from '../api-client'

interface OnboardingStore {
  // Estado actual
  pasoActual: number
  configuracion: Partial<ConfiguracionIndividual>
  
  // Acciones
  setPaso: (paso: number) => void
  siguientePaso: () => void
  anteriorPaso: () => void
  
  setNoNegociables: (noNegociables: NoNegociables) => void
  setDimensiones: (dimensiones: string[]) => void
  setEnergiaDisponible: (energia: number) => void
  setContextoFinanciero: (contexto: ContextoFinanciero) => void
  setContextoBiologico: (contexto: ContextoBiologico) => void
  setExpresionLibre: (expresion: string) => void
  
  getConfiguracionCompleta: () => ConfiguracionIndividual
  reset: () => void
}

export const useOnboardingStore = create<OnboardingStore>((set, get) => ({
  // Estado inicial
  pasoActual: 1,
  configuracion: {
    no_negociables: {
      fajr_estado_cero: true,
      dhuhr_estado_cero: true,
      asr_estado_cero: false,
      maghrib_validacion: true,
      isha_estado_cero: false
    },
    dimensiones_prioritarias: [],
    energia_disponible: 3,
    contexto_financiero: {
      runway_meses: 6,
      urgencia: false
    },
    contexto_biologico: {
      patron_sueno: 'regular',
      nivel_energia: 3,
      ejercicio_regular: false
    },
    expresion_libre: ''
  },

  // Navegación
  setPaso: (paso) => set({ pasoActual: paso }),
  
  siguientePaso: () => set((state) => ({ 
    pasoActual: Math.min(state.pasoActual + 1, 4) 
  })),
  
  anteriorPaso: () => set((state) => ({ 
    pasoActual: Math.max(state.pasoActual - 1, 1) 
  })),

  // Setters
  setNoNegociables: (noNegociables) => set((state) => ({
    configuracion: {
      ...state.configuracion,
      no_negociables: noNegociables
    }
  })),

  setDimensiones: (dimensiones) => set((state) => ({
    configuracion: {
      ...state.configuracion,
      dimensiones_prioritarias: dimensiones
    }
  })),

  setEnergiaDisponible: (energia) => set((state) => ({
    configuracion: {
      ...state.configuracion,
      energia_disponible: energia
    }
  })),

  setContextoFinanciero: (contexto) => set((state) => ({
    configuracion: {
      ...state.configuracion,
      contexto_financiero: contexto
    }
  })),

  setContextoBiologico: (contexto) => set((state) => ({
    configuracion: {
      ...state.configuracion,
      contexto_biologico: contexto
    }
  })),

  setExpresionLibre: (expresion) => set((state) => ({
    configuracion: {
      ...state.configuracion,
      expresion_libre: expresion
    }
  })),

  // Obtener configuración completa
  getConfiguracionCompleta: () => {
    const state = get()
    return {
      user_id: 'default',
      no_negociables: state.configuracion.no_negociables!,
      dimensiones_prioritarias: state.configuracion.dimensiones_prioritarias!,
      energia_disponible: state.configuracion.energia_disponible!,
      contexto_financiero: state.configuracion.contexto_financiero!,
      contexto_biologico: state.configuracion.contexto_biologico!,
      expresion_libre: state.configuracion.expresion_libre
    }
  },

  // Reset
  reset: () => set({
    pasoActual: 1,
    configuracion: {
      no_negociables: {
        fajr_estado_cero: true,
        dhuhr_estado_cero: true,
        asr_estado_cero: false,
        maghrib_validacion: true,
        isha_estado_cero: false
      },
      dimensiones_prioritarias: [],
      energia_disponible: 3,
      contexto_financiero: {
        runway_meses: 6,
        urgencia: false
      },
      contexto_biologico: {
        patron_sueno: 'regular',
        nivel_energia: 3,
        ejercicio_regular: false
      },
      expresion_libre: ''
    }
  })
}))

