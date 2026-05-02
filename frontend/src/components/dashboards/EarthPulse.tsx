'use client';

import { useGTI } from '@/hooks';
import { api } from '@/lib/api';
import { useEffect, useState } from 'react';
import { HeadlineData, ConflictData } from '@/types';
import LineChart from '@/components/charts/LineChart';
import SignalCard from '@/components/ui/SignalCard';
import HeadlineItem from '@/components/ui/HeadlineItem';
import StatusBadge from '@/components/ui/StatusBadge';

export default function EarthPulse() {
  const { current: gti, history: gtiHistory, loading: gtiLoading } = useGTI();
  const [headlines, setHeadlines] = useState<HeadlineData | null>(null);
  const [conflicts, setConflicts] = useState<ConflictData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      const [headlineRes, conflictRes] = await Promise.all([
        api.headlines(20),
        api.conflicts(15),
      ]);

      if (!('error' in headlineRes)) setHeadlines(headlineRes);
      if (!('error' in conflictRes)) setConflicts(conflictRes);
      setLoading(false);
    };

    loadData();
  }, []);

  return (
    <div className="p-8 space-y-8">
      <div className="grid grid-cols-4 gap-4">
        <StatusBadge
          label="GTI Score"
          status={gti && gti.score > 0.6 ? 'danger' : gti && gti.score > 0.4 ? 'warning' : 'success'}
          value={gti ? (gti.score * 100).toFixed(1) : '-'}
        />
        <StatusBadge
          label="Sentiment"
          status={gti && gti.sentiment < -10 ? 'danger' : 'neutral'}
          value={gti ? gti.sentiment.toFixed(1) : '-'}
        />
        <StatusBadge
          label="Volatility"
          status={gti && gti.volatility > 50 ? 'warning' : 'success'}
          value={gti ? gti.volatility.toFixed(1) : '-'}
        />
        <StatusBadge
          label="Active Conflicts"
          status={conflicts ? (conflicts.total_events > 100 ? 'danger' : 'warning') : 'neutral'}
          value={conflicts?.total_events || '-'}
        />
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2">
          <LineChart
            data={gtiHistory}
            dataKey="score"
            stroke="#00ffff"
            title="Geopolitical Tension Index (48h)"
            height={400}
          />
        </div>
        <SignalCard signal={null} loading={gtiLoading} />
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-semibold text-slate-200 mb-4">Top Headlines</h3>
          <div className="space-y-3">
            {headlines?.headlines.slice(0, 5).map((headline, i) => (
              <HeadlineItem key={i} headline={headline} />
            ))}
          </div>
        </div>

        <div>
          <h3 className="text-lg font-semibold text-slate-200 mb-4">Active Conflicts</h3>
          <div className="space-y-3">
            {conflicts?.conflicts.slice(0, 5).map((conflict, i) => (
              <div key={i} className="bg-[#13151d] border border-slate-800 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <p className="font-semibold text-slate-200">{conflict.country}</p>
                  <span className={`text-xs px-2 py-1 rounded ${
                    conflict.severity === 'high' ? 'bg-danger bg-opacity-20 text-danger' :
                    conflict.severity === 'medium' ? 'bg-amber bg-opacity-20 text-amber' :
                    'bg-success bg-opacity-20 text-success'
                  }`}>
                    {conflict.severity}
                  </span>
                </div>
                <p className="text-sm text-slate-400">{conflict.count} events</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
