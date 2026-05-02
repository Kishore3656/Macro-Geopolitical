'use client';

import { AlertTriangle } from 'lucide-react';
import { BilateralRelation } from '@/types';

interface BilateralCardProps {
  relation: BilateralRelation;
}

const stressColors = {
  stable: 'bg-success bg-opacity-20 text-success',
  tense: 'bg-amber bg-opacity-20 text-amber',
  critical: 'bg-danger bg-opacity-20 text-danger',
};

export default function BilateralCard({ relation }: BilateralCardProps) {
  return (
    <div className="bg-[#13151d] border border-slate-800 rounded-lg p-4">
      <div className="flex items-start justify-between mb-3">
        <div>
          <p className="text-sm font-semibold text-slate-200">
            {relation.country1} ↔ {relation.country2}
          </p>
          <p className="text-xs text-slate-500 mt-1">{relation.recent_events} recent events</p>
        </div>
        {relation.stress_category === 'critical' && (
          <AlertTriangle size={18} className="text-danger flex-shrink-0" />
        )}
      </div>

      <div className={`inline-block px-3 py-1 rounded text-xs font-medium ${stressColors[relation.stress_category]}`}>
        {relation.stress_category.charAt(0).toUpperCase() + relation.stress_category.slice(1)}
      </div>

      <div className="mt-3 pt-3 border-t border-slate-800">
        <div className="flex justify-between text-xs">
          <span className="text-slate-500">Stress Level</span>
          <span className="font-semibold text-slate-300">{relation.stress_level.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
}
