'use client';

import { AlertTriangle, Zap, TrendingUp } from 'lucide-react';
import { BilateralRelation } from '@/types';

interface BilateralCardProps {
  relation: BilateralRelation;
}

export default function BilateralCard({ relation }: BilateralCardProps) {
  const isCritical = relation.stress_category === 'critical';
  const isTense = relation.stress_category === 'tense';

  return (
    <div className={`group hover:shadow-lg transition-all rounded-xl border backdrop-blur-sm p-5 ${
      isCritical
        ? 'border-red-500/30 bg-gradient-to-r from-red-500/10 to-transparent hover:border-red-500/50'
        : isTense
        ? 'border-amber-500/30 bg-gradient-to-r from-amber-500/10 to-transparent hover:border-amber-500/50'
        : 'border-emerald-500/30 bg-gradient-to-r from-emerald-500/10 to-transparent hover:border-emerald-500/50'
    }`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <p className="font-semibold text-slate-200 group-hover:text-slate-100">
              {relation.country1} ↔ {relation.country2}
            </p>
            {isCritical && <AlertTriangle size={16} className="text-red-400 flex-shrink-0" />}
          </div>
          <p className="text-xs text-slate-400 mt-1">{relation.recent_events} recent events</p>
        </div>
        <div className="text-right flex-shrink-0">
          <p className={`text-sm font-bold ${
            isCritical ? 'text-red-400' :
            isTense ? 'text-amber-400' :
            'text-emerald-400'
          }`}>
            {relation.stress_level.toFixed(1)}
          </p>
          <p className="text-xs text-slate-400">{relation.stress_category}</p>
        </div>
      </div>
    </div>
  );
}
