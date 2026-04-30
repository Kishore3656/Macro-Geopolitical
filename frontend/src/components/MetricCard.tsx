'use client';

import { ArrowUp, ArrowDown, Minus } from 'lucide-react';

interface MetricCardProps {
  label: string;
  value: string | number;
  unit?: string;
  trend?: 'up' | 'down' | 'neutral';
  change?: number;
}

export default function MetricCard({ label, value, unit, trend = 'neutral', change }: MetricCardProps) {
  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <ArrowUp size={16} className="text-green-400" />;
      case 'down':
        return <ArrowDown size={16} className="text-red-400" />;
      default:
        return <Minus size={16} className="text-slate-400" />;
    }
  };

  const getTrendColor = () => {
    switch (trend) {
      case 'up':
        return 'text-green-400';
      case 'down':
        return 'text-red-400';
      default:
        return 'text-slate-400';
    }
  };

  return (
    <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-5 hover:border-slate-600 hover:bg-slate-800/70 transition-all duration-200">
      <p className="text-slate-400 text-xs font-medium uppercase tracking-wider mb-3">{label}</p>
      <div className="flex items-end justify-between">
        <div className="flex-1">
          <p className="text-3xl font-bold text-white leading-tight">{value}</p>
          {unit && <p className="text-xs text-slate-500 mt-2">{unit}</p>}
        </div>
        {change !== undefined && (
          <div className={`flex items-center gap-1 ml-4 ${getTrendColor()}`}>
            {getTrendIcon()}
            <span className="text-sm font-semibold">{Math.abs(change)}%</span>
          </div>
        )}
      </div>
    </div>
  );
}
