'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface InputsCapas {
  energia: number;
  calidad_sueno: number;
  resonancia_corporal: string;
  estado_emocional: string;
  intensidad_emocional: number;
}

interface Props {
  onComplete: (inputs: InputsCapas) => void;
  momento: string;
}

export default function PuertaDeEntrada7Capas({ onComplete, momento }: Props) {
  const [paso, setPaso] = useState(0);

  // Inputs de las capas
  const [energia, setEnergia] = useState(3);
  const [calidadSueno, setCalidadSueno] = useState(3);
  const [resonanciaCorporal, setResonanciaCorporal] = useState('neutral');
  const [estadoEmocional, setEstadoEmocional] = useState('neutro');
  const [intensidadEmocional, setIntensidadEmocional] = useState(3);

  const pasos = [
    {
      titulo: 'Energía Física',
      subtitulo: 'Capa 3: Biológica',
      pregunta: '¿Cómo está tu energía en este momento?',
      icono: '⚡',
      tipo: 'slider' as const,
      valor: energia,
      onChange: setEnergia,
      min: 1,
      max: 5,
      labels: ['Muy baja', 'Baja', 'Media', 'Alta', 'Muy alta']
    },
    {
      titulo: 'Calidad de Sueño',
      subtitulo: 'Capa 3: Biológica',
      pregunta: '¿Cómo fue tu sueño anoche?',
      icono: '🌙',
      tipo: 'slider' as const,
      valor: calidadSueno,
      onChange: setCalidadSueno,
      min: 1,
      max: 5,
      labels: ['Pésimo', 'Malo', 'Regular', 'Bueno', 'Excelente']
    },
    {
      titulo: 'Resonancia Corporal',
      subtitulo: 'Capa 3: Biológica',
      pregunta: '¿Qué siente tu cuerpo ahora?',
      icono: '🧘',
      tipo: 'opciones' as const,
      valor: resonanciaCorporal,
      onChange: setResonanciaCorporal,
      opciones: [
        { valor: 'tension', label: 'Tensión', emoji: '😰' },
        { valor: 'fatiga', label: 'Fatiga', emoji: '😮‍💨' },
        { valor: 'neutral', label: 'Neutral', emoji: '😐' },
        { valor: 'fluido', label: 'Fluido', emoji: '😌' },
        { valor: 'vibrante', label: 'Vibrante', emoji: '✨' }
      ]
    },
    {
      titulo: 'Estado Emocional',
      subtitulo: 'Capa 5: Emocional',
      pregunta: '¿Cómo te sientes emocionalmente?',
      icono: '💭',
      tipo: 'opciones' as const,
      valor: estadoEmocional,
      onChange: setEstadoEmocional,
      opciones: [
        { valor: 'calma', label: 'Calma', emoji: '🕊️' },
        { valor: 'ansioso', label: 'Ansioso', emoji: '😰' },
        { valor: 'entusiasmado', label: 'Entusiasmado', emoji: '🔥' },
        { valor: 'apagado', label: 'Apagado', emoji: '🌑' },
        { valor: 'neutro', label: 'Neutro', emoji: '⚪' }
      ]
    },
    {
      titulo: 'Intensidad Emocional',
      subtitulo: 'Capa 5: Emocional',
      pregunta: '¿Qué tan intensa es esa emoción?',
      icono: '🎚️',
      tipo: 'slider' as const,
      valor: intensidadEmocional,
      onChange: setIntensidadEmocional,
      min: 1,
      max: 5,
      labels: ['Muy leve', 'Leve', 'Media', 'Intensa', 'Muy intensa']
    }
  ];

  const pasoActual = pasos[paso];

  const siguientePaso = () => {
    if (paso < pasos.length - 1) {
      setPaso(paso + 1);
    } else {
      // Completar y pasar inputs al componente padre
      onComplete({
        energia,
        calidad_sueno: calidadSueno,
        resonancia_corporal: resonanciaCorporal,
        estado_emocional: estadoEmocional,
        intensidad_emocional: intensidadEmocional
      });
    }
  };

  const pasoAnterior = () => {
    if (paso > 0) {
      setPaso(paso - 1);
    }
  };

  const obtenerColorMomento = (momento: string) => {
    const colores = {
      fajr: 'from-purple-600 to-amber-500',
      dhuhr: 'from-yellow-500 to-green-500',
      maghrib: 'from-red-500 to-purple-600',
      asr: 'from-orange-500 to-red-500',
      isha: 'from-indigo-600 to-purple-800'
    };
    return colores[momento as keyof typeof colores] || 'from-gray-600 to-gray-800';
  };

  return (
    <div className={`min-h-screen bg-gradient-to-br ${obtenerColorMomento(momento)} flex items-center justify-center p-4`}>
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6 }}
        className="max-w-2xl w-full bg-white/10 backdrop-blur-lg rounded-3xl p-8 md:p-12 text-white"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <motion.div
            animate={{ scale: [1, 1.05, 1] }}
            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
            className="text-5xl mb-4"
          >
            {pasoActual.icono}
          </motion.div>
          <p className="text-xs opacity-50 font-light tracking-wider mb-2">{pasoActual.subtitulo}</p>
          <h2 className="text-2xl md:text-3xl font-light mb-2">{pasoActual.titulo}</h2>
          <p className="text-base opacity-70 font-light">{pasoActual.pregunta}</p>
        </div>

        {/* Contenido del paso */}
        <AnimatePresence mode="wait">
          <motion.div
            key={paso}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.4 }}
            className="mb-10"
          >
            {pasoActual.tipo === 'slider' && (
              <div className="space-y-6">
                {/* Slider */}
                <div className="relative">
                  <input
                    type="range"
                    min={pasoActual.min}
                    max={pasoActual.max}
                    value={pasoActual.valor}
                    onChange={(e) => pasoActual.onChange(parseInt(e.target.value))}
                    className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer slider-thumb"
                    style={{
                      background: `linear-gradient(to right, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0.4) ${((pasoActual.valor - pasoActual.min!) / (pasoActual.max! - pasoActual.min!)) * 100}%, rgba(255,255,255,0.1) ${((pasoActual.valor - pasoActual.min!) / (pasoActual.max! - pasoActual.min!)) * 100}%, rgba(255,255,255,0.1) 100%)`
                    }}
                  />
                </div>

                {/* Valor actual */}
                <div className="text-center">
                  <motion.div
                    key={pasoActual.valor}
                    initial={{ scale: 1.2, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="inline-block bg-white/20 backdrop-blur-sm px-6 py-3 rounded-full"
                  >
                    <span className="text-2xl font-light">{pasoActual.labels![pasoActual.valor - 1]}</span>
                  </motion.div>
                </div>

                {/* Labels de extremos */}
                <div className="flex justify-between text-xs opacity-50 font-light px-1">
                  <span>{pasoActual.labels![0]}</span>
                  <span>{pasoActual.labels![pasoActual.labels!.length - 1]}</span>
                </div>
              </div>
            )}

            {pasoActual.tipo === 'opciones' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {pasoActual.opciones!.map((opcion) => (
                  <motion.button
                    key={opcion.valor}
                    onClick={() => pasoActual.onChange(opcion.valor)}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className={`p-6 rounded-2xl border-2 transition-all duration-300 ${
                      pasoActual.valor === opcion.valor
                        ? 'bg-white/25 border-white/50 shadow-lg'
                        : 'bg-white/5 border-white/20 hover:bg-white/10'
                    }`}
                  >
                    <div className="text-3xl mb-2">{opcion.emoji}</div>
                    <div className="text-lg font-light">{opcion.label}</div>
                  </motion.button>
                ))}
              </div>
            )}
          </motion.div>
        </AnimatePresence>

        {/* Navegación */}
        <div className="flex items-center justify-between">
          <button
            onClick={pasoAnterior}
            disabled={paso === 0}
            className="px-6 py-3 rounded-full bg-white/10 border border-white/20 hover:bg-white/15 disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-300 font-light"
          >
            ← Atrás
          </button>

          {/* Progreso */}
          <div className="flex gap-2">
            {pasos.map((_, idx) => (
              <div
                key={idx}
                className={`w-2 h-2 rounded-full transition-all duration-300 ${
                  idx <= paso ? 'bg-white' : 'bg-white/20'
                }`}
              />
            ))}
          </div>

          <button
            onClick={siguientePaso}
            className="px-6 py-3 rounded-full bg-white/20 border border-white/30 hover:bg-white/25 transition-all duration-300 font-light"
          >
            {paso === pasos.length - 1 ? 'Comenzar →' : 'Siguiente →'}
          </button>
        </div>
      </motion.div>

      <style jsx>{`
        .slider-thumb::-webkit-slider-thumb {
          appearance: none;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: white;
          cursor: pointer;
          box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }

        .slider-thumb::-moz-range-thumb {
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: white;
          cursor: pointer;
          box-shadow: 0 2px 10px rgba(0,0,0,0.3);
          border: none;
        }
      `}</style>
    </div>
  );
}
