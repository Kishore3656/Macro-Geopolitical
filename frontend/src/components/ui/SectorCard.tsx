'use client';

import { TrendingUp, TrendingDown } from 'lucide-react';
import { Sector } from '@/types';

interface SectorCardProps {
  sector: Sector;
}

export default function SectorCard({ sector }: SectorCardProps) {
  const isPositive = sector.change_pct >= 0;
  const color = isPositive ? 'text-success' : 'text-danger';
  const bgColor = isPositive ? 'bg-success bg-opacity-20' : 'bg-danger bg-opacity-20';

  return (
    <div className="bg-[#13151d] border border-slate-800 rounded-lg p-4">
      <div className="flex items-start justify-between mb-3">
        <h4 className="text-sm font-semibold text-slate-200">{sector.name}</h4>
        <div className={`p-2 rounded-lg ${bgColor}`}>
          {isPositive ? (
            <TrendingUp size={16} className={color} />
          ) : (
            <TrendingDown size={16} className={color} />
          )}
        </div>
      </div>

      <div className="space-y-2">
        <div>
          <p className="text-xs text-slate-500">Performance</p>
          <p className="text-lg font-bold text-slate-200">{sector.performance.toFixed(2)}</p>
        </div>
        <div className="pt-2 border-t border-slate-800">
          <p className={`text-sm font-semibold ${color}`}>
            {isPositive ? '+' : ''}{sector.change_pct.toFixed(2)}%
          </p>
        </div>
      </div>
    </div>
  );
}
