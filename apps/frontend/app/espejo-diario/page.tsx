'use client';

import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

interface EspejoData {
  status: string;
  fecha: string;
  archivo: string;
  contenido: string;
}

export default function EspejoDiarioPage() {
  const [espejo, setEspejo] = useState<EspejoData | null>(null);
  const [fecha, setFecha] = useState(new Date().toISOString().split('T')[0]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadEspejo = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`http://localhost:8000/api/sistema/espejo-diario?fecha=${fecha}`);
      if (!res.ok) throw new Error('Error cargando Espejo Diario');
      const data = await res.json();
      setEspejo(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateEspejo = async () => {
    setLoading(true);
    setError(null);
    try {
      await fetch(`http://localhost:8000/api/sistema/generar-espejo-diario`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fecha })
      });
      await loadEspejo();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEspejo();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white">
      {/* Header con geometría sagrada */}
      <div className="relative overflow-hidden border-b border-white/10">
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] border border-purple-500/30 rounded-full"></div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] border border-blue-500/30 rounded-full"></div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] border border-cyan-500/30 rounded-full"></div>
        </div>
        
        <div className="relative z-10 max-w-6xl mx-auto p-8">
          <h1 className="text-5xl font-bold mb-2">🪞 Espejo Diario</h1>
          <p className="text-xl text-white/60">
            Síntesis comprehensiva de tus 5 Estados Cero
          </p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-8">
        {/* Controles */}
        <div className="mb-8 flex items-center gap-4 bg-white/5 rounded-2xl p-6 backdrop-blur-sm border border-white/10">
          <input 
            type="date" 
            value={fecha}
            onChange={(e) => setFecha(e.target.value)}
            className="bg-white/10 rounded-xl px-4 py-3 border border-white/20 focus:border-purple-500 focus:outline-none transition-colors"
          />
          <button 
            onClick={loadEspejo} 
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-6 py-3 rounded-xl font-medium transition-colors flex items-center gap-2"
          >
            {loading ? '⏳ Cargando...' : '📥 Cargar'}
          </button>
          <button 
            onClick={generateEspejo} 
            disabled={loading}
            className="bg-green-600 hover:bg-green-700 disabled:bg-gray-600 px-6 py-3 rounded-xl font-medium transition-colors flex items-center gap-2"
          >
            {loading ? '⏳ Generando...' : '✨ Generar Nuevo'}
          </button>
          <div className="flex-1"></div>
          <a 
            href="/"
            className="text-white/60 hover:text-white transition-colors"
          >
            ← Volver
          </a>
        </div>

        {/* Error */}
        {error && (
          <div className="mb-8 bg-red-500/20 border border-red-500/50 rounded-2xl p-6">
            <p className="text-red-200">⚠️ {error}</p>
          </div>
        )}

        {/* Contenido del Espejo */}
        {espejo && (
          <div className="bg-white/10 rounded-2xl p-8 backdrop-blur-sm border border-white/20">
            <div className="prose prose-invert prose-lg max-w-none">
              <ReactMarkdown
                components={{
                  h1: ({node, ...props}) => <h1 className="text-4xl font-bold mb-6 text-purple-300" {...props} />,
                  h2: ({node, ...props}) => <h2 className="text-3xl font-bold mb-4 mt-8 text-blue-300" {...props} />,
                  h3: ({node, ...props}) => <h3 className="text-2xl font-bold mb-3 mt-6 text-cyan-300" {...props} />,
                  p: ({node, ...props}) => <p className="mb-4 text-white/80 leading-relaxed" {...props} />,
                  ul: ({node, ...props}) => <ul className="list-disc list-inside mb-4 space-y-2" {...props} />,
                  li: ({node, ...props}) => <li className="text-white/80" {...props} />,
                  strong: ({node, ...props}) => <strong className="text-white font-semibold" {...props} />,
                  code: ({node, ...props}) => <code className="bg-black/50 px-2 py-1 rounded text-cyan-300 font-mono text-sm" {...props} />,
                  pre: ({node, ...props}) => <pre className="bg-black/50 p-4 rounded-lg overflow-x-auto mb-4" {...props} />,
                }}
              >
                {espejo.contenido}
              </ReactMarkdown>
            </div>

            {/* Metadata */}
            <div className="mt-8 pt-8 border-t border-white/10">
              <div className="flex items-center justify-between text-sm text-white/40">
                <span>📅 Fecha: {espejo.fecha}</span>
                <span>📁 Archivo: {espejo.archivo.split('/').pop()}</span>
              </div>
            </div>
          </div>
        )}

        {/* Estado sin Espejo */}
        {!espejo && !loading && !error && (
          <div className="bg-white/5 rounded-2xl p-12 text-center border border-white/10">
            <div className="text-6xl mb-4">🌙</div>
            <h3 className="text-2xl font-bold mb-2">No hay Espejo Diario para esta fecha</h3>
            <p className="text-white/60 mb-6">
              Genera uno nuevo para sintetizar tus Estados Cero del día
            </p>
            <button 
              onClick={generateEspejo}
              className="bg-purple-600 hover:bg-purple-700 px-8 py-3 rounded-xl font-medium transition-colors"
            >
              ✨ Generar Espejo Diario
            </button>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="max-w-6xl mx-auto p-8 text-center text-white/40 text-sm">
        <p>Sistema operando al borde del caos - 40% capacidad sin asignar</p>
        <p className="mt-2">Campo Sagrado del Entrelazador - Configuración 0.01%</p>
      </div>
    </div>
  );
}

