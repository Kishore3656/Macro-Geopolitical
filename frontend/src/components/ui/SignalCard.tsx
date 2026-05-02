'use client';

import { ArrowUp, ArrowDown } from 'lucide-react';
import { SignalsData } from '@/types';

interface SignalCardProps {
  signal: SignalsData | null;
  loading?: boolean;
}

export default function SignalCard({ signal, loading }: SignalCardProps) {
  if (loading) {
    return (
      <div className="bg-[#13151d] border border-slate-800 rounded-lg p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-slate-800 rounded w-1/2"></div>
          <div className="h-8 bg-slate-800 rounded w-full"></div>
        </div>
      </div>
    );
  }

  if (!signal) return null;

  const isUp = signal.direction === 'UP';
  const dirColor = isUp ? 'text-success' : 'text-danger';
  const dirBg = isUp ? 'bg-success bg-opacity-20' : 'bg-danger bg-opacity-20';

  return (
    <div className="bg-[#13151d] border border-slate-800 rounded-lg p-6">
      <h3 className="text-sm font-medium text-slate-400 mb-4">Market Direction</h3>

      <div className="flex items-end justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className={`p-3 rounded-lg ${dirBg}`}>
            {isUp ? <ArrowUp size={24} className={dirColor} /> : <ArrowDown size={24} className={dirColor} />}
          </div>
          <div>
            <p className={`text-3xl font-bold ${dirColor}`}>{signal.direction}</p>
            <p className="text-xs text-slate-500">{(signal.direction_prob * 100).toFixed(1)}% confidence</p>
          </div>
        </div>

        <div className="text-right">
          <p className="text-sm text-slate-400">Volatility</p>
          <p className="text-lg font-semibold text-amber">{signal.volatility}</p>
          <p className="text-xs text-slate-500">{(signal.volatility_prob * 100).toFixed(1)}% prob</p>
        </div>
      </div>

      <div className="pt-4 border-t border-slate-800">
        <div className="flex justify-between items-center">
          <span className="text-xs text-slate-500">Overall Confidence</span>
          <span className="text-sm font-semibold text-cyan">{(signal.confidence * 100).toFixed(1)}%</span>
        </div>
        <div className="w-full bg-slate-800 rounded-full h-2 mt-2">
          <div
            className="bg-cyan h-2 rounded-full transition-all"
            style={{ width: `${signal.confidence * 100}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
}
