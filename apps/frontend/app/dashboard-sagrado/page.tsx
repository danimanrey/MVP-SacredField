"use client";

/**
 * 🕌 DASHBOARD SAGRADO - El Continente
 * 
 * Refleja la salud del Reino Humano bajo gobierno divino.
 * 
 * Estructura:
 * 1. Unidad del Ser (salud global)
 * 2. Ciclo del Día (Timeline Fajr → Maghrib)
 * 3. Decreto Sacral (PODER LEGISLATIVO)
 * 4. Gabinete Ministerial (PODER EJECUTIVO - 7 Ministerios)
 * 5. Pilares Fundamentales (8 Pilares)
 * 6. Espejo Nocturno (PODER JUDICIAL)
 */

import { useEffect, useState } from "react";
import { motion } from "framer-motion";

// Tipos
interface DashboardData {
  arquitectura_sagrada: {
    version: string;
    estado: string;
    fecha: string;
    hora_actual: string;
  };
  unidad_del_ser: {
    salud_organismo: number;
    estado: string;
    wahdat_al_wujud: string;
  };
  ciclo_dia: {
    fajr: { hora: string; poder: string; accion: string; completado: boolean };
    dhuhr: { hora: string; poder: string; accion: string; completado: boolean };
    maghrib: { hora: string; poder: string; accion: string; completado: boolean };
  };
  pilares: {
    score_global: number;
    pilares_cumplidos: number;
    total_pilares: number;
    cumple_arquitectura: boolean;
    pilares: Array<{ nombre: string; score: number; cumple: boolean }>;
  };
  poderes: {
    separacion: string;
    legislativo: any;
    ejecutivo: any;
    judicial: any;
  };
  ministerios: {
    salud_global: number;
    ministerios_activos: number;
    ministerios?: Array<{ nombre: string; nombre_divino: string; salud: number }>;
  };
  espejo_nocturno: any;
  invocacion: string;
}

export default function DashboardSagrado() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboard();
    
    // Actualizar cada 30 segundos
    const interval = setInterval(fetchDashboard, 30000);
    return () => clearInterval(interval);
  }, []);

  async function fetchDashboard() {
    try {
      const response = await fetch("http://localhost:8000/api/arquitectura-sagrada/dashboard");
      if (!response.ok) throw new Error("Error al cargar dashboard");
      const dashboardData = await response.json();
      setData(dashboardData);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="text-6xl"
        >
          🕌
        </motion.div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-8">
        <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-8 max-w-md">
          <h2 className="text-2xl font-bold text-red-400 mb-4">Error al cargar Dashboard</h2>
          <p className="text-red-300">{error || "No se pudo conectar con el backend"}</p>
          <button
            onClick={fetchDashboard}
            className="mt-4 px-6 py-2 bg-red-500/20 hover:bg-red-500/30 rounded-lg text-red-300"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center space-y-2"
        >
          <h1 className="text-5xl font-bold bg-gradient-to-r from-amber-200 via-amber-400 to-amber-200 bg-clip-text text-transparent">
            🕌 Dashboard Sagrado
          </h1>
          <p className="text-amber-300/80">
            {data.arquitectura_sagrada.estado}
          </p>
          <p className="text-sm text-amber-300/60">
            {data.arquitectura_sagrada.fecha} · {data.arquitectura_sagrada.hora_actual}
          </p>
        </motion.div>

        {/* Unidad del Ser - Salud Global */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-gradient-to-br from-purple-900/40 to-indigo-900/40 backdrop-blur-sm border border-purple-500/30 rounded-2xl p-8"
        >
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-3xl font-bold text-purple-200 mb-2">
                {data.unidad_del_ser.estado}
              </h2>
              <p className="text-purple-300/80 text-sm italic">
                {data.unidad_del_ser.wahdat_al_wujud}
              </p>
            </div>
            <div className="text-right">
              <div className="text-6xl font-bold text-amber-400">
                {data.unidad_del_ser.salud_organismo.toFixed(1)}
              </div>
              <div className="text-sm text-purple-300/60">Salud del Organismo</div>
            </div>
          </div>
        </motion.div>

        {/* Grid de 2 columnas */}
        <div className="grid md:grid-cols-2 gap-8">
          
          {/* Izquierda: Decreto + Ciclo */}
          <div className="space-y-8">
            
            {/* Decreto Sacral */}
            <DecretoCard decreto={data.poderes.legislativo} />
            
            {/* Ciclo del Día */}
            <CicloDiaCard ciclo={data.ciclo_dia} />
            
          </div>

          {/* Derecha: Pilares + Ministerios */}
          <div className="space-y-8">
            
            {/* 8 Pilares */}
            <PilaresCard pilares={data.pilares} />
            
            {/* 7 Ministerios */}
            <MinisteriosCard ministerios={data.ministerios} />
            
          </div>
        </div>

        {/* Espejo Nocturno (full width) */}
        {data.espejo_nocturno && (
          <EspejoNocturnoCard espejo={data.espejo_nocturno} />
        )}

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="text-center text-amber-300/60 text-sm pt-8"
        >
          {data.invocacion}
        </motion.div>

      </div>
    </div>
  );
}

// =====================================================================
// COMPONENTE: Decreto Sacral
// =====================================================================

function DecretoCard({ decreto }: { decreto: any }) {
  if (!decreto.decreto_emitido) {
    return (
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-gradient-to-br from-amber-900/20 to-yellow-900/20 backdrop-blur-sm border border-amber-500/30 rounded-xl p-6"
      >
        <h3 className="text-xl font-bold text-amber-300 mb-2 flex items-center gap-2">
          📜 Poder Legislativo
        </h3>
        <p className="text-amber-400/80 text-sm mb-4">{decreto.nombre}</p>
        <div className="bg-amber-900/20 rounded-lg p-4 text-center">
          <p className="text-amber-300">⚠️ Pendiente Estado Cero</p>
          <p className="text-amber-400/60 text-sm mt-2">
            El Sultán aún no ha emitido decreto para hoy
          </p>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.2 }}
      className="bg-gradient-to-br from-amber-900/40 to-yellow-900/40 backdrop-blur-sm border border-amber-500/50 rounded-xl p-6 shadow-2xl"
    >
      <h3 className="text-xl font-bold text-amber-200 mb-2 flex items-center gap-2">
        📜 Decreto Sacral
        {decreto.validado_pilares && <span className="text-green-400 text-sm">✓ 8 Pilares</span>}
      </h3>
      <p className="text-amber-400/80 text-sm mb-4">{decreto.nombre}</p>
      
      <div className="bg-amber-900/30 rounded-lg p-4 mb-3">
        <p className="text-amber-100 font-medium">{decreto.decreto}</p>
      </div>
      
      <div className="flex justify-between text-sm">
        <span className="text-amber-300/70">Momento: {decreto.momento}</span>
        <span className="text-green-400">{decreto.estado}</span>
      </div>
    </motion.div>
  );
}

// =====================================================================
// COMPONENTE: Ciclo del Día
// =====================================================================

function CicloDiaCard({ ciclo }: { ciclo: any }) {
  const momentos = [
    { key: "fajr", emoji: "🌅", color: "from-blue-500 to-purple-500" },
    { key: "dhuhr", emoji: "☀️", color: "from-yellow-500 to-orange-500" },
    { key: "maghrib", emoji: "🌆", color: "from-orange-500 to-red-500" },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.3 }}
      className="bg-gradient-to-br from-indigo-900/40 to-blue-900/40 backdrop-blur-sm border border-indigo-500/30 rounded-xl p-6"
    >
      <h3 className="text-xl font-bold text-indigo-200 mb-4">⏰ Ciclo del Día</h3>
      
      <div className="space-y-3">
        {momentos.map((momento) => {
          const data = ciclo[momento.key];
          return (
            <div
              key={momento.key}
              className={`
                bg-gradient-to-r ${momento.color} bg-opacity-20 rounded-lg p-3
                ${data.completado ? 'opacity-100' : 'opacity-50'}
              `}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{momento.emoji}</span>
                  <div>
                    <p className="font-bold text-white">{data.hora}</p>
                    <p className="text-xs text-white/80">{data.poder}</p>
                  </div>
                </div>
                <div className="text-right">
                  {data.completado ? (
                    <span className="text-green-400 text-2xl">✓</span>
                  ) : (
                    <span className="text-white/40 text-2xl">○</span>
                  )}
                </div>
              </div>
              <p className="text-white/70 text-sm mt-2 ml-11">{data.accion}</p>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}

// =====================================================================
// COMPONENTE: 8 Pilares
// =====================================================================

function PilaresCard({ pilares }: { pilares: any }) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.2 }}
      className="bg-gradient-to-br from-emerald-900/40 to-teal-900/40 backdrop-blur-sm border border-emerald-500/30 rounded-xl p-6"
    >
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold text-emerald-200">🏛️ 8 Pilares</h3>
        <div className="text-right">
          <div className="text-2xl font-bold text-emerald-400">
            {pilares.pilares_cumplidos}/{pilares.total_pilares}
          </div>
          <div className="text-xs text-emerald-300/60">
            {pilares.score_global.toFixed(0)}% cumplimiento
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-2">
        {pilares.pilares.map((pilar: any, idx: number) => (
          <div
            key={idx}
            className={`
              rounded-lg p-2 text-sm
              ${pilar.cumple 
                ? 'bg-emerald-900/30 text-emerald-200' 
                : 'bg-red-900/20 text-red-300'}
            `}
          >
            <div className="flex justify-between items-center">
              <span className="truncate">{pilar.nombre}</span>
              <span>{pilar.cumple ? '✓' : '○'}</span>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

// =====================================================================
// COMPONENTE: 7 Ministerios
// =====================================================================

function MinisteriosCard({ ministerios }: { ministerios: any }) {
  const ministeriosData = ministerios.ministerios || [];
  
  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.3 }}
      className="bg-gradient-to-br from-violet-900/40 to-fuchsia-900/40 backdrop-blur-sm border border-violet-500/30 rounded-xl p-6"
    >
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold text-violet-200">👥 7 Ministerios</h3>
        <div className="text-right">
          <div className="text-2xl font-bold text-violet-400">
            {ministerios.salud_global.toFixed(1)}
          </div>
          <div className="text-xs text-violet-300/60">Salud Global</div>
        </div>
      </div>
      
      {ministeriosData.length === 0 ? (
        <div className="bg-violet-900/20 rounded-lg p-4 text-center">
          <p className="text-violet-300/80 text-sm">
            {ministerios.mensaje || "Esperando decreto del Sultán"}
          </p>
        </div>
      ) : (
        <div className="space-y-2">
          {ministeriosData.map((ministerio: any, idx: number) => (
            <div
              key={idx}
              className="bg-violet-900/20 rounded-lg p-3 flex justify-between items-center"
            >
              <div>
                <p className="font-medium text-violet-200 capitalize">{ministerio.nombre}</p>
                <p className="text-xs text-violet-300/60">{ministerio.nombre_divino}</p>
              </div>
              <div className="text-right">
                <div className={`
                  text-lg font-bold
                  ${ministerio.salud >= 80 ? 'text-green-400' 
                    : ministerio.salud >= 60 ? 'text-yellow-400'
                    : 'text-red-400'}
                `}>
                  {ministerio.salud.toFixed(0)}
                </div>
                <div className="text-xs text-violet-300/60">salud</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </motion.div>
  );
}

// =====================================================================
// COMPONENTE: Espejo Nocturno
// =====================================================================

function EspejoNocturnoCard({ espejo }: { espejo: any }) {
  if (!espejo) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      className="bg-gradient-to-br from-slate-800/40 to-zinc-900/40 backdrop-blur-sm border border-slate-500/30 rounded-xl p-6"
    >
      <h3 className="text-2xl font-bold text-slate-200 mb-4">🌙 Espejo Nocturno</h3>
      
      <div className="grid md:grid-cols-2 gap-6">
        {/* Resonancias */}
        <div>
          <h4 className="text-green-400 font-bold mb-3 flex items-center gap-2">
            ✨ Resonancias
          </h4>
          <ul className="space-y-2">
            {espejo.resonancias?.map((r: string, idx: number) => (
              <li key={idx} className="text-green-300/80 text-sm flex items-start gap-2">
                <span className="text-green-400 mt-1">•</span>
                <span>{r}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Obstrucciones */}
        <div>
          <h4 className="text-orange-400 font-bold mb-3 flex items-center gap-2">
            ⚠️ Obstrucciones
          </h4>
          <ul className="space-y-2">
            {espejo.obstrucciones?.map((o: string, idx: number) => (
              <li key={idx} className="text-orange-300/80 text-sm flex items-start gap-2">
                <span className="text-orange-400 mt-1">•</span>
                <span>{o}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Semilla para mañana */}
      {espejo.semilla_mañana && (
        <div className="mt-6 bg-amber-900/20 rounded-lg p-4 border border-amber-500/30">
          <p className="text-amber-400 font-bold mb-2">🌱 Semilla para mañana:</p>
          <p className="text-amber-200/90">{espejo.semilla_mañana}</p>
        </div>
      )}

      {/* Nivel de cumplimiento */}
      <div className="mt-4 text-center">
        <span className={`
          inline-block px-4 py-2 rounded-full font-bold
          ${espejo.nivel_cumplimiento === 'ALTO' ? 'bg-green-900/40 text-green-300'
            : espejo.nivel_cumplimiento === 'MEDIO' ? 'bg-yellow-900/40 text-yellow-300'
            : 'bg-red-900/40 text-red-300'}
        `}>
          {espejo.nivel_cumplimiento}: {espejo.mensaje}
        </span>
      </div>
    </motion.div>
  );
}

