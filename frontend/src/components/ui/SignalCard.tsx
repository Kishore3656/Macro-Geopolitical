'use client';

import { ArrowUp, ArrowDown, Gauge } from 'lucide-react';
import { SignalsData } from '@/types';

interface SignalCardProps {
  signal: SignalsData | null;
  loading?: boolean;
}

export default function SignalCard({ signal, loading }: SignalCardProps) {
  if (loading) {
    return (
      <div className="bg-gradient-to-br from-slate-900/80 via-slate-800/80 to-slate-900/80 rounded-2xl border border-slate-700/50 backdrop-blur-xl p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-slate-700 rounded-lg w-1/2"></div>
          <div className="h-10 bg-slate-700 rounded-lg w-full"></div>
          <div className="h-6 bg-slate-700 rounded-lg w-3/4"></div>
        </div>
      </div>
    );
  }

  if (!signal) return null;

  const isUp = signal.direction === 'UP';

  return (
    <div className={`bg-gradient-to-br backdrop-blur-xl rounded-2xl border transition-all p-6 ${
      isUp
        ? 'border-green-500/30 from-green-500/10 via-slate-900/80 to-slate-900/80 hover:shadow-lg hover:shadow-green-500/20'
        : 'border-red-500/30 from-red-500/10 via-slate-900/80 to-slate-900/80 hover:shadow-lg hover:shadow-red-500/20'
    }`}>
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-sm font-semibold text-slate-300 flex items-center gap-2">
          <Gauge className="w-4 h-4" />
          Market Direction
        </h3>
        <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></div>
      </div>

      <div className="mb-6">
        <div className="flex items-center gap-4">
          <div className={`flex-shrink-0 ${isUp ? 'text-green-400' : 'text-red-400'}`}>
            {isUp ? <ArrowUp className="w-8 h-8" /> : <ArrowDown className="w-8 h-8" />}
          </div>
          <div>
            <p className={`text-3xl font-bold ${isUp ? 'text-green-400' : 'text-red-400'}`}>
              {signal.direction}
            </p>
            <p className="text-xs text-slate-400 mt-1">{(signal.direction_prob * 100).toFixed(1)}% confidence</p>
          </div>
        </div>
      </div>

      <div className="space-y-4 pt-4 border-t border-slate-700/50">
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-400">Volatility</span>
            <span className={`text-sm font-bold ${
              signal.volatility === 'HIGH' ? 'text-red-400' :
              signal.volatility === 'MEDIUM' ? 'text-amber-400' :
              'text-emerald-400'
            }`}>
              {signal.volatility}
            </span>
          </div>
          <div className="w-full bg-slate-700/30 rounded-full h-1.5">
            <div
              className={`h-1.5 rounded-full transition-all ${
                signal.volatility === 'HIGH' ? 'bg-red-400' :
                signal.volatility === 'MEDIUM' ? 'bg-amber-400' :
                'bg-emerald-400'
              }`}
              style={{ width: `${(signal.volatility_prob * 100) || 50}%` }}
            ></div>
          </div>
          <p className="text-xs text-slate-500 mt-1">{(signal.volatility_prob * 100).toFixed(1)}% probability</p>
        </div>

        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-400">Overall Confidence</span>
            <span className="text-sm font-bold text-cyan-400">{(signal.confidence * 100).toFixed(1)}%</span>
          </div>
          <div className="w-full bg-slate-700/30 rounded-full h-2">
            <div
              className="bg-gradient-to-r from-cyan-400 to-blue-400 h-2 rounded-full transition-all"
              style={{ width: `${signal.confidence * 100}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
}
