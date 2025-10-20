'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

interface DashboardData {
  timestamp: string;
  periodo_analisis: string;
  resumen: {
    estados_cero_analizados: number;
    dominios_analizados: number;
    entrelazamientos_detectados: number;
    acciones_coordinadas: number;
    acciones_sistemicas: number;
  };
  patrones?: {
    tendencia_predominante: string;
    intensidad_promedio: number;
    consistencia: number;
    patrones_detectados: Array<{
      tipo: string;
      descripcion: string;
      frecuencia: number;
    }>;
  };
  dominios?: Record<string, {
    menciones: number;
    tendencia_predominante: string;
    energia_promedio: number;
    urgencia_promedio: number;
  }>;
  entrelazamientos?: Array<{
    dominios: string[];
    fuerza: number;
    tipo: string;
    descripcion: string;
  }>;
  acciones_prioritarias?: Array<{
    tipo: string;
    descripcion: string;
    urgencia: number;
    impacto_sistemico: number;
    dominios_implicados: string[];
  }>;
  archivos_generados: {
    patrones?: string;
    entrelazamiento?: string;
    acciones?: string;
  };
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/sistema/dashboard-data');
      
      if (!res.ok) {
        throw new Error(`Error ${res.status}: ${res.statusText}`);
      }
      
      const json = await res.json();
      
      if (json.error) {
        setError(json.error);
        setData(null);
      } else {
        setData(json);
        setLastUpdate(json.timestamp);
        setError(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
      setData(null);
    }
  };

  const handleRefresh = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Regenerar análisis
      console.log('🔄 Regenerando análisis...');
      const analysisRes = await fetch('http://localhost:8000/api/sistema/analisis-completo?dias=7');
      
      if (!analysisRes.ok) {
        throw new Error(`Error en análisis: ${analysisRes.status}`);
      }
      
      const analysisData = await analysisRes.json();
      console.log('✅ Análisis completado:', analysisData);
      
      // Recargar datos del dashboard
      await loadDashboard();
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error en actualización');
      console.error('❌ Error en actualización:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return timestamp;
    }
  };

  const getTendenciaColor = (tendencia: string) => {
    switch (tendencia.toLowerCase()) {
      case 'expansión':
        return 'text-green-400';
      case 'contracción':
        return 'text-red-400';
      default:
        return 'text-gray-400';
    }
  };

  const getUrgenciaColor = (urgencia: number) => {
    if (urgencia >= 0.8) return 'text-red-400';
    if (urgencia >= 0.6) return 'text-orange-400';
    if (urgencia >= 0.4) return 'text-yellow-400';
    return 'text-green-400';
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="max-w-2xl w-full bg-white/10 backdrop-blur-lg rounded-3xl p-8 text-white text-center"
        >
          <div className="text-6xl mb-6">⚠️</div>
          <h1 className="text-3xl font-bold mb-4">Error en Dashboard</h1>
          <p className="text-lg mb-6 text-red-300">{error}</p>
          <button
            onClick={handleRefresh}
            className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold py-3 px-6 rounded-full transition-all duration-300 transform hover:scale-105"
          >
            🔄 Reintentar
          </button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-5xl font-bold text-white mb-4">🕌 Dashboard Campo Sagrado</h1>
          <p className="text-xl text-gray-300 mb-6">Análisis Sistémico y Entrelazamiento</p>
          
          <div className="flex justify-center items-center gap-4">
            <button
              onClick={handleRefresh}
              disabled={loading}
              className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 text-white font-bold py-3 px-6 rounded-full transition-all duration-300 transform hover:scale-105"
            >
              {loading ? '🔄 Actualizando...' : '🔄 Actualizar Análisis'}
            </button>
            
            {lastUpdate && (
              <p className="text-sm text-gray-400">
                Última actualización: {formatTimestamp(lastUpdate)}
              </p>
            )}
          </div>
        </motion.div>

        {data ? (
          <div className="space-y-6">
            {/* Resumen General */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white/10 backdrop-blur-lg rounded-2xl p-6"
            >
              <h2 className="text-2xl font-bold text-white mb-4">📊 Resumen General</h2>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-400">{data.resumen.estados_cero_analizados}</div>
                  <div className="text-sm text-gray-300">Estados Cero</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-400">{data.resumen.dominios_analizados}</div>
                  <div className="text-sm text-gray-300">Dominios</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-400">{data.resumen.entrelazamientos_detectados}</div>
                  <div className="text-sm text-gray-300">Entrelazamientos</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-400">{data.resumen.acciones_coordinadas}</div>
                  <div className="text-sm text-gray-300">Acciones Coordinadas</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-400">{data.resumen.acciones_sistemicas}</div>
                  <div className="text-sm text-gray-300">Acciones Sistémicas</div>
                </div>
              </div>
            </motion.div>

            {/* Patrones */}
            {data.patrones && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="bg-white/10 backdrop-blur-lg rounded-2xl p-6"
              >
                <h2 className="text-2xl font-bold text-white mb-4">🔍 Patrones Detectados</h2>
                <div className="grid md:grid-cols-3 gap-4 mb-4">
                  <div>
                    <div className="text-sm text-gray-300">Tendencia Predominante</div>
                    <div className={`text-xl font-bold ${getTendenciaColor(data.patrones.tendencia_predominante)}`}>
                      {data.patrones.tendencia_predominante}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-300">Intensidad Promedio</div>
                    <div className="text-xl font-bold text-blue-400">
                      {(data.patrones.intensidad_promedio * 100).toFixed(1)}%
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-300">Consistencia</div>
                    <div className="text-xl font-bold text-purple-400">
                      {(data.patrones.consistencia * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>
                
                {data.patrones.patrones_detectados.length > 0 && (
                  <div>
                    <h3 className="text-lg font-bold text-white mb-2">Patrones Específicos</h3>
                    <div className="space-y-2">
                      {data.patrones.patrones_detectados.map((patron, index) => (
                        <div key={index} className="bg-white/5 rounded-lg p-3">
                          <div className="font-semibold text-white">{patron.tipo}</div>
                          <div className="text-sm text-gray-300">{patron.descripcion}</div>
                          <div className="text-xs text-blue-400">Frecuencia: {patron.frecuencia}%</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}

            {/* Dominios */}
            {data.dominios && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-white/10 backdrop-blur-lg rounded-2xl p-6"
              >
                <h2 className="text-2xl font-bold text-white mb-4">🌐 Análisis de Dominios</h2>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {Object.entries(data.dominios).map(([dominio, info]) => (
                    <div key={dominio} className="bg-white/5 rounded-lg p-4">
                      <h3 className="font-bold text-white capitalize mb-2">{dominio}</h3>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-300">Menciones:</span>
                          <span className="text-blue-400">{info.menciones}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-300">Tendencia:</span>
                          <span className={getTendenciaColor(info.tendencia_predominante)}>
                            {info.tendencia_predominante}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-300">Energía:</span>
                          <span className="text-green-400">{(info.energia_promedio * 100).toFixed(1)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-300">Urgencia:</span>
                          <span className={getUrgenciaColor(info.urgencia_promedio)}>
                            {(info.urgencia_promedio * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Entrelazamientos */}
            {data.entrelazamientos && data.entrelazamientos.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="bg-white/10 backdrop-blur-lg rounded-2xl p-6"
              >
                <h2 className="text-2xl font-bold text-white mb-4">🔗 Entrelazamientos Detectados</h2>
                <div className="space-y-3">
                  {data.entrelazamientos.map((entrelazamiento, index) => (
                    <div key={index} className="bg-white/5 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <div className="font-semibold text-white">
                          {entrelazamiento.dominios.join(' ↔ ')}
                        </div>
                        <div className="text-sm text-purple-400">
                          Fuerza: {(entrelazamiento.fuerza * 100).toFixed(1)}%
                        </div>
                      </div>
                      <div className="text-sm text-gray-300 mb-1">
                        Tipo: <span className="text-yellow-400">{entrelazamiento.tipo}</span>
                      </div>
                      <div className="text-sm text-gray-300">{entrelazamiento.descripcion}</div>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Acciones Prioritarias */}
            {data.acciones_prioritarias && data.acciones_prioritarias.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="bg-white/10 backdrop-blur-lg rounded-2xl p-6"
              >
                <h2 className="text-2xl font-bold text-white mb-4">⚡ Acciones Prioritarias</h2>
                <div className="space-y-3">
                  {data.acciones_prioritarias.map((accion, index) => (
                    <div key={index} className="bg-white/5 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <div className="font-semibold text-white">{accion.tipo}</div>
                        <div className="flex gap-2 text-sm">
                          <span className={`px-2 py-1 rounded ${getUrgenciaColor(accion.urgencia)} bg-opacity-20`}>
                            Urgencia: {(accion.urgencia * 100).toFixed(0)}%
                          </span>
                          <span className="px-2 py-1 rounded text-green-400 bg-green-400 bg-opacity-20">
                            Impacto: {(accion.impacto_sistemico * 100).toFixed(0)}%
                          </span>
                        </div>
                      </div>
                      <div className="text-sm text-gray-300 mb-2">{accion.descripcion}</div>
                      <div className="text-xs text-blue-400">
                        Dominios: {accion.dominios_implicados.join(', ')}
                      </div>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Archivos Generados */}
            {data.archivos_generados && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="bg-white/10 backdrop-blur-lg rounded-2xl p-6"
              >
                <h2 className="text-2xl font-bold text-white mb-4">📁 Archivos Generados</h2>
                <div className="grid md:grid-cols-3 gap-4">
                  {data.archivos_generados.patrones && (
                    <div className="bg-white/5 rounded-lg p-3">
                      <div className="font-semibold text-white mb-1">Patrones</div>
                      <div className="text-sm text-gray-300 break-all">{data.archivos_generados.patrones}</div>
                    </div>
                  )}
                  {data.archivos_generados.entrelazamiento && (
                    <div className="bg-white/5 rounded-lg p-3">
                      <div className="font-semibold text-white mb-1">Entrelazamiento</div>
                      <div className="text-sm text-gray-300 break-all">{data.archivos_generados.entrelazamiento}</div>
                    </div>
                  )}
                  {data.archivos_generados.acciones && (
                    <div className="bg-white/5 rounded-lg p-3">
                      <div className="font-semibold text-white mb-1">Acciones</div>
                      <div className="text-sm text-gray-300 break-all">{data.archivos_generados.acciones}</div>
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center py-12"
          >
            <div className="text-6xl mb-6">📊</div>
            <h2 className="text-2xl font-bold text-white mb-4">Cargando Dashboard...</h2>
            <p className="text-gray-300">Preparando análisis sistémico</p>
          </motion.div>
        )}
      </div>
    </div>
  );
}
