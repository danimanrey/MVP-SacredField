'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import * as THREE from 'three';
import PuertaDeEntrada7Capas from '../components/PuertaDeEntrada7Capas';

interface Pregunta {
  id: number;
  texto: string;
  respondida: boolean;
}

interface EstadoCero {
  estado_cero_id: string;
  momento: string;
  intencion: string;
  reflexion: string;
  preguntas: Pregunta[];
}

interface InputsCapas {
  energia: number;
  calidad_sueno: number;
  resonancia_corporal: string;
  estado_emocional: string;
  intensidad_emocional: number;
}

export default function EstadoCeroInmersivo() {
  const [estadoCero, setEstadoCero] = useState<EstadoCero | null>(null);
  const [fase, setFase] = useState<'inicio' | 'puerta_entrada' | 'intencion' | 'preguntas' | 'reflexion' | 'completado'>('inicio');
  const [preguntaActual, setPreguntaActual] = useState(0);
  const [respuestas, setRespuestas] = useState<{[key: number]: boolean}>({});
  const [intencion, setIntencion] = useState('');
  const [reflexion, setReflexion] = useState('');
  const [cargando, setCargando] = useState(false);
  const [sintesis, setSintesis] = useState<any>(null);
  const [integrando, setIntegrando] = useState(false);
  const [botonesActivos, setBotonesActivos] = useState(false);
  const [inputsCapas, setInputsCapas] = useState<InputsCapas | null>(null);
  const [momentoActual, setMomentoActual] = useState('dhuhr');
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Geometría sagrada - Esfera de luz
  useEffect(() => {
    if (!canvasRef.current) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas: canvasRef.current, alpha: true });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    
    // Crear esfera de luz
    const geometry = new THREE.SphereGeometry(2, 32, 32);
    const material = new THREE.MeshBasicMaterial({ 
      color: 0x8B5CF6, 
      transparent: true, 
      opacity: 0.3,
      wireframe: true 
    });
    const sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);

    // Partículas de constelación
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 1000;
    const posArray = new Float32Array(particlesCount * 3);
    
    for (let i = 0; i < particlesCount * 3; i++) {
      posArray[i] = (Math.random() - 0.5) * 10;
    }
    
    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    
    const particlesMaterial = new THREE.PointsMaterial({
      size: 0.005,
      color: 0xffffff,
      transparent: true,
      opacity: 0.8
    });
    
    const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);

    camera.position.z = 5;

    const animate = () => {
      requestAnimationFrame(animate);

      // Respiración lumínica - pulso en lugar de rotación
      const pulseSpeed = 0.0008;
      const pulseAmplitude = 0.12;
      const time = Date.now();
      const pulse = 1 + Math.sin(time * pulseSpeed) * pulseAmplitude;

      sphere.scale.setScalar(pulse);
      (sphere.material as THREE.MeshBasicMaterial).opacity = 0.2 + Math.sin(time * pulseSpeed * 0.5) * 0.15;

      // Partículas con movimiento sutil (no rotación constante)
      particlesMesh.rotation.y = Math.sin(time * 0.0003) * 0.1;

      renderer.render(scene, camera);
    };
    
    animate();

    return () => {
      renderer.dispose();
    };
  }, []);

  const irAPuertaEntrada = () => {
    setFase('puerta_entrada');
  };

  const iniciarEstadoCeroConCapas = async (inputs: InputsCapas) => {
    setInputsCapas(inputs);
    setCargando(true);

    try {
      // 🔥 INTEGRACIÓN TOTAL: Usando endpoint /iniciar con sistema de 7 capas
      const response = await fetch('http://localhost:8000/api/estado-cero/iniciar?modo_testing=true', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          momento: momentoActual,
          energia: inputs.energia,
          calidad_sueno: inputs.calidad_sueno,
          resonancia_corporal: inputs.resonancia_corporal,
          estado_emocional: inputs.estado_emocional,
          intensidad_emocional: inputs.intensidad_emocional
        })
      });

      if (response.ok) {
        const data = await response.json();
        setEstadoCero(data);
        // 🔥 FLUJO SIMPLIFICADO: Saltar intención, ir directo a pregunta emergente
        setFase('preguntas');
        setPreguntaActual(0);
        setRespuestas({});
        setIntencion('');
        setReflexion('');
      }
    } catch (error) {
      console.error('Error iniciando Estado Cero:', error);
    } finally {
      setCargando(false);
    }
  };

  const guardarIntencion = async () => {
    if (!estadoCero) return;
    
    try {
      await fetch(`http://localhost:8000/api/estado-cero/${estadoCero.estado_cero_id}/guardar-texto`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tipo: 'intencion', texto: intencion }),
      });
    } catch (error) {
      console.error('Error guardando intención:', error);
    }
    
    setFase('preguntas');
  };

  // Activar botones después de pausa inicial (forzar respiración)
  useEffect(() => {
    if (fase === 'preguntas') {
      setBotonesActivos(false);
      const timer = setTimeout(() => setBotonesActivos(true), 1800);
      return () => clearTimeout(timer);
    }
  }, [preguntaActual, fase]);

  const responderPregunta = async (respuesta: boolean) => {
    if (!estadoCero || !botonesActivos) return;

    const nuevaRespuesta = { ...respuestas, [preguntaActual]: respuesta };
    setRespuestas(nuevaRespuesta);

    // Mostrar feedback de integración
    setIntegrando(true);

    try {
      await fetch(`http://localhost:8000/api/estado-cero/${estadoCero.estado_cero_id}/responder`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pregunta_id: preguntaActual,
          respuesta: respuesta,
          nota: null
        }),
      });
    } catch (error) {
      console.error('Error enviando respuesta:', error);
    }

    // Pausa de integración sacral (2.5 segundos para asentar)
    await new Promise(resolve => setTimeout(resolve, 2500));

    setIntegrando(false);

    if (preguntaActual < estadoCero.preguntas.length - 1) {
      setPreguntaActual(preguntaActual + 1);
    } else {
      setFase('reflexion');
    }
  };

  const guardarReflexion = async () => {
    if (!estadoCero) return;
    
    try {
      await fetch(`http://localhost:8000/api/estado-cero/${estadoCero.estado_cero_id}/guardar-texto`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tipo: 'reflexion', texto: reflexion }),
      });
    } catch (error) {
      console.error('Error guardando reflexión:', error);
    }
    
    finalizarEstadoCero();
  };

  const finalizarEstadoCero = async () => {
    if (!estadoCero) return;

    try {
      const response = await fetch(`http://localhost:8000/api/estado-cero/${estadoCero.estado_cero_id}/finalizar`, {
        method: 'POST',
      });
      
      if (response.ok) {
        const data = await response.json();
        setSintesis(data.sintesis);
        setFase('completado');
      }
    } catch (error) {
      console.error('Error finalizando Estado Cero:', error);
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

  if (fase === 'completado' && sintesis) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center p-4 relative overflow-hidden">
        <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1 }}
          className="max-w-4xl w-full bg-white/10 backdrop-blur-lg rounded-3xl p-12 text-white relative z-10"
        >
          <div className="text-center mb-12">
            <motion.div
              animate={{
                scale: [1, 1.08, 1],
                rotate: [0, 5, -5, 0]
              }}
              transition={{
                duration: 4,
                repeat: Infinity,
                ease: "easeInOut"
              }}
              className="text-6xl mb-6"
            >
              🕌
            </motion.div>
            <h1 className="text-3xl font-light mb-3">Completado</h1>
            <p className="text-sm opacity-50 font-light tracking-wider">{estadoCero?.momento.toUpperCase()}</p>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white/5 rounded-2xl p-8 mb-8"
          >
            <div className="space-y-6">
              <div className="text-center">
                <p className="text-sm opacity-60 mb-3 font-light">Tendencia detectada</p>
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.5, type: "spring" }}
                  className={`inline-block px-6 py-3 rounded-full ${
                    sintesis.tendencia === 'expansión'
                      ? 'bg-green-500/15 border border-green-400/30 text-green-300'
                      : 'bg-red-500/15 border border-red-400/30 text-red-300'
                  }`}
                >
                  <span className="text-xl">{sintesis.tendencia === 'expansión' ? '⊕' : '⊖'}</span>
                  <span className="ml-2 font-light">{sintesis.tendencia}</span>
                  <span className="ml-2 opacity-60 text-sm">({Math.round(sintesis.intensidad * 100)}%)</span>
                </motion.div>
              </div>

              <div className="bg-white/5 rounded-xl p-6">
                <h3 className="text-sm opacity-60 mb-3 font-light text-center">Dirección emergente</h3>
                <p className="text-center font-light leading-relaxed">{sintesis.direccion_emergente}</p>
              </div>
            </div>
          </motion.div>

          <div className="text-center space-y-4">
            <p className="text-sm text-green-300/70 font-light">Archivado en tu bóveda personal</p>
            <motion.button
              onClick={() => {
                setEstadoCero(null);
                setFase('inicio');
                setSintesis(null);
              }}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="bg-white/10 border border-white/20 hover:bg-white/15 text-white font-light py-3 px-12 rounded-full transition-all duration-500"
            >
              Cerrar
            </motion.button>
          </div>
        </motion.div>
      </div>
    );
  }

  if (fase === 'puerta_entrada') {
    return (
      <PuertaDeEntrada7Capas
        onComplete={iniciarEstadoCeroConCapas}
        momento={momentoActual}
      />
    );
  }

  if (fase === 'inicio') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center p-4 relative overflow-hidden">
        <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="max-w-2xl w-full text-center text-white relative z-10"
        >
          <motion.div
            animate={{
              scale: [1, 1.05, 1],
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            className="text-8xl mb-8"
          >
            🕌
          </motion.div>
          <h1 className="text-4xl font-light mb-4 tracking-wide">Estado Cero</h1>
          <p className="text-lg mb-4 opacity-60 font-light">
            Consulta Sacral • Sistema de 7 Capas
          </p>
          <p className="text-sm mb-12 opacity-40 font-light max-w-md mx-auto">
            El organismo digital te escucha. Física • Social • Biológica • Energética • Emocional • Mental • Cósmica
          </p>

          <motion.button
            onClick={irAPuertaEntrada}
            disabled={cargando}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="bg-white/10 backdrop-blur-sm border border-white/20 hover:bg-white/15 disabled:opacity-50 text-white font-light py-4 px-12 rounded-full text-lg transition-all duration-500"
          >
            {cargando ? 'Preparando espacio...' : 'Entrar al Organismo →'}
          </motion.button>
        </motion.div>
      </div>
    );
  }

  if (fase === 'intencion') {
    return (
      <div className={`min-h-screen bg-gradient-to-br ${obtenerColorMomento(estadoCero?.momento || 'dhuhr')} flex items-center justify-center p-4 relative overflow-hidden`}>
        <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl w-full bg-white/10 backdrop-blur-lg rounded-3xl p-12 text-white relative z-10"
        >
          <div className="text-center mb-12">
            <motion.div
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
              className="text-4xl mb-4"
            >
              🕌
            </motion.div>
            <h1 className="text-2xl font-light mb-2">Intención</h1>
            <p className="text-sm opacity-50 font-light tracking-wider">{estadoCero?.momento.toUpperCase()}</p>
          </div>

          <div className="bg-white/5 rounded-2xl p-8 mb-8 relative">
            <textarea
              value={intencion}
              onChange={(e) => setIntencion(e.target.value)}
              placeholder="¿Qué buscas en este momento?"
              className="w-full bg-transparent border-none text-white placeholder-gray-400/60 focus:outline-none text-lg min-h-[200px] resize-none font-light"
              autoFocus
            />
          </div>

          <div className="text-center">
            <motion.button
              onClick={guardarIntencion}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="bg-white/10 border border-white/20 hover:bg-white/15 text-white font-light py-3 px-12 rounded-full transition-all duration-500"
            >
              Continuar
            </motion.button>
          </div>
        </motion.div>
      </div>
    );
  }

  if (fase === 'preguntas') {
    const pregunta = estadoCero?.preguntas[preguntaActual];

    return (
      <div className={`min-h-screen bg-gradient-to-br ${obtenerColorMomento(estadoCero?.momento || 'dhuhr')} flex items-center justify-center p-4 relative overflow-hidden`}>
        <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />
        <AnimatePresence mode="wait">
          <motion.div
            key={preguntaActual}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{
              duration: 0.8,
              ease: [0.4, 0, 0.2, 1]
            }}
            className="max-w-4xl w-full bg-white/10 backdrop-blur-lg rounded-3xl p-8 text-white relative z-10"
          >
            <div className="text-center mb-12">
              <motion.div
                className="text-4xl mb-4"
                animate={{
                  scale: [1, 1.05, 1],
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              >
                🕌
              </motion.div>
              <h1 className="text-2xl font-light opacity-70 mb-2">{estadoCero?.momento.toUpperCase()}</h1>
            </div>

          <div className="relative">
            {/* Pregunta central */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.6 }}
              className="bg-white/5 rounded-2xl p-12 mb-12 relative overflow-hidden"
            >
              {/* Latido sacral de fondo */}
              <motion.div
                className="absolute inset-0 bg-white/5 rounded-2xl"
                animate={{
                  opacity: [0, 0.1, 0],
                  scale: [1, 1.02, 1]
                }}
                transition={{
                  duration: 5,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />

              <h2 className="text-3xl font-light text-center relative z-10">{pregunta?.texto}</h2>
            </motion.div>

            {integrando ? (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-center py-16"
              >
                {/* Ondas de integración */}
                <div className="relative w-32 h-32 mx-auto mb-6">
                  {[0, 1, 2].map((i) => (
                    <motion.div
                      key={i}
                      className="absolute inset-0 border-2 border-white/30 rounded-full"
                      animate={{
                        scale: [1, 2.5],
                        opacity: [0.6, 0]
                      }}
                      transition={{
                        duration: 2.5,
                        repeat: Infinity,
                        delay: i * 0.8,
                        ease: "easeOut"
                      }}
                    />
                  ))}
                  <motion.div
                    className="absolute inset-0 flex items-center justify-center text-5xl"
                    animate={{
                      scale: [1, 1.1, 1],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: "easeInOut"
                    }}
                  >
                    🕌
                  </motion.div>
                </div>
                <p className="text-lg opacity-60 font-light">Integrando respuesta...</p>
              </motion.div>
            ) : (
              <>
                {/* Ancla de respiración */}
                {!botonesActivos && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-center mb-12"
                  >
                    <div className="relative w-20 h-20 mx-auto mb-4">
                      <motion.div
                        animate={{
                          scale: [1, 1.3, 1],
                          opacity: [0.2, 0.5, 0.2]
                        }}
                        transition={{
                          duration: 4,
                          repeat: Infinity,
                          ease: "easeInOut"
                        }}
                        className="absolute inset-0 rounded-full border-2 border-white/30"
                      />
                      <motion.div
                        animate={{
                          rotate: 360
                        }}
                        transition={{
                          duration: 8,
                          repeat: Infinity,
                          ease: "linear"
                        }}
                        className="absolute inset-0 rounded-full border-t-2 border-white/50"
                      />
                    </div>
                    <p className="text-sm opacity-50 font-light tracking-wider">RESPIRA • SIENTE • RESPONDE</p>
                  </motion.div>
                )}

                {/* Botones de respuesta */}
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: botonesActivos ? 1 : 0.3 }}
                  transition={{ duration: 0.5 }}
                  className="flex gap-6 justify-center items-center"
                >
                  <motion.button
                    onClick={() => responderPregunta(false)}
                    disabled={!botonesActivos}
                    whileHover={botonesActivos ? { scale: 1.02 } : {}}
                    whileTap={botonesActivos ? { scale: 0.98 } : {}}
                    className={`relative bg-red-500/10 border border-red-400/40 text-red-200 font-light py-8 px-16 rounded-2xl text-lg transition-all duration-700 ${
                      botonesActivos
                        ? 'hover:shadow-[0_0_40px_rgba(239,68,68,0.3)] cursor-pointer'
                        : 'cursor-not-allowed'
                    }`}
                  >
                    <span className="text-2xl mr-2">⊖</span>
                    <span>Contracción</span>
                  </motion.button>

                  {/* Separador central con geometría */}
                  <div className="w-px h-20 bg-gradient-to-b from-transparent via-white/20 to-transparent" />

                  <motion.button
                    onClick={() => responderPregunta(true)}
                    disabled={!botonesActivos}
                    whileHover={botonesActivos ? { scale: 1.02 } : {}}
                    whileTap={botonesActivos ? { scale: 0.98 } : {}}
                    className={`relative bg-green-500/10 border border-green-400/40 text-green-200 font-light py-8 px-16 rounded-2xl text-lg transition-all duration-700 ${
                      botonesActivos
                        ? 'hover:shadow-[0_0_40px_rgba(34,197,94,0.3)] cursor-pointer'
                        : 'cursor-not-allowed'
                    }`}
                  >
                    <span className="text-2xl mr-2">⊕</span>
                    <span>Expansión</span>
                  </motion.button>
                </motion.div>
              </>
            )}
          </div>

            {/* Progreso silencioso - puntos sutiles */}
            <div className="flex gap-2 justify-center mt-8">
              {estadoCero?.preguntas.map((_, idx) => (
                <motion.div
                  key={idx}
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: idx * 0.1 }}
                  className={`rounded-full transition-all duration-700 ${
                    idx < preguntaActual
                      ? 'w-2 h-2 bg-white/60'
                      : idx === preguntaActual
                      ? 'w-3 h-3 bg-white'
                      : 'w-2 h-2 bg-white/20'
                  }`}
                />
              ))}
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    );
  }

  if (fase === 'reflexion') {
    return (
      <div className={`min-h-screen bg-gradient-to-br ${obtenerColorMomento(estadoCero?.momento || 'dhuhr')} flex items-center justify-center p-4 relative overflow-hidden`}>
        <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl w-full bg-white/10 backdrop-blur-lg rounded-3xl p-12 text-white relative z-10"
        >
          <div className="text-center mb-12">
            <motion.div
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
              className="text-4xl mb-4"
            >
              🕌
            </motion.div>
            <h1 className="text-2xl font-light mb-2">Reflexión</h1>
            <p className="text-sm opacity-50 font-light tracking-wider">¿Qué emerge?</p>
          </div>

          <div className="bg-white/5 rounded-2xl p-8 mb-8">
            <textarea
              value={reflexion}
              onChange={(e) => setReflexion(e.target.value)}
              placeholder="Permite que las palabras lleguen..."
              className="w-full bg-transparent border-none text-white placeholder-gray-400/60 focus:outline-none text-lg min-h-[200px] resize-none font-light"
              autoFocus
            />
          </div>

          <div className="text-center">
            <motion.button
              onClick={guardarReflexion}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="bg-white/10 border border-white/20 hover:bg-white/15 text-white font-light py-3 px-12 rounded-full transition-all duration-500"
            >
              Completar
            </motion.button>
          </div>
        </motion.div>
      </div>
    );
  }

  return null;
}
