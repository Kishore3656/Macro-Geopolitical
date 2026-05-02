'use client';

import { useSignals } from '@/hooks';
import { useEffect, useState } from 'react';
import { SignalHistoryPoint } from '@/types';
import LineChart from '@/components/charts/LineChart';
import StatusBadge from '@/components/ui/StatusBadge';

export default function AISignals() {
  const { current, history, loading } = useSignals();
  const [winRate, setWinRate] = useState<number>(0);

  useEffect(() => {
    if (history && history.length > 0) {
      const correctPredictions = history.filter(h => h.direction === 'UP').length;
      setWinRate((correctPredictions / history.length) * 100);
    }
  }, [history]);

  return (
    <div className="p-8 space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">AI Trading Signals</h2>
        <p className="text-sm text-slate-400 mt-1">ML-generated trade signals with confidence metrics & prediction history</p>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <StatusBadge
          label="Direction"
          status={current?.direction === 'UP' ? 'success' : 'danger'}
          value={current?.direction || '-'}
        />
        <StatusBadge
          label="Direction Prob"
          status={current && current.direction_prob > 0.7 ? 'success' : 'warning'}
          value={current ? `${(current.direction_prob * 100).toFixed(1)}%` : '-'}
        />
        <StatusBadge
          label="Volatility"
          status={current?.volatility === 'HIGH' ? 'danger' : current?.volatility === 'MEDIUM' ? 'warning' : 'success'}
          value={current?.volatility || '-'}
        />
        <StatusBadge
          label="Confidence"
          status={current && current.confidence > 0.75 ? 'success' : 'warning'}
          value={current ? `${(current.confidence * 100).toFixed(1)}%` : '-'}
        />
      </div>

      <div>
        <h3 className="text-lg font-semibold text-slate-200 mb-4">Prediction History & Confidence</h3>
        <LineChart
          data={history}
          dataKey="confidence"
          stroke="#00ffff"
          title="Model Confidence Over Time"
          height={350}
        />
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="bg-[#13151d] border border-slate-800 rounded-lg p-6">
          <p className="text-sm text-slate-400 mb-2">Total Predictions</p>
          <p className="text-3xl font-bold text-cyan">{history.length}</p>
          <p className="text-xs text-slate-500 mt-2">Last 100 signals</p>
        </div>

        <div className="bg-[#13151d] border border-slate-800 rounded-lg p-6">
          <p className="text-sm text-slate-400 mb-2">Win Rate</p>
          <p className="text-3xl font-bold text-success">{winRate.toFixed(1)}%</p>
          <p className="text-xs text-slate-500 mt-2">Bullish accuracy</p>
        </div>

        <div className="bg-[#13151d] border border-slate-800 rounded-lg p-6">
          <p className="text-sm text-slate-400 mb-2">Avg Volatility</p>
          <p className="text-3xl font-bold text-amber">
            {history.length > 0
              ? (history.filter(h => h.volatility === 'HIGH').length / history.length * 100).toFixed(1)
              : 0
            }%
          </p>
          <p className="text-xs text-slate-500 mt-2">High volatility signals</p>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-slate-200 mb-4">Recent Signals</h3>
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {history.slice(0, 10).map((signal, i) => (
            <div key={i} className="bg-[#13151d] border border-slate-800 rounded-lg p-4">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className={`px-3 py-1 rounded text-xs font-semibold ${
                      signal.direction === 'UP'
                        ? 'bg-success bg-opacity-20 text-success'
                        : 'bg-danger bg-opacity-20 text-danger'
                    }`}>
                      {signal.direction}
                    </span>
                    <span className={`text-sm font-semibold ${
                      signal.volatility === 'HIGH' ? 'text-danger' :
                      signal.volatility === 'MEDIUM' ? 'text-amber' :
                      'text-success'
                    }`}>
                      {signal.volatility} Volatility
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">
                    Direction Confidence: {(signal.direction_prob * 100).toFixed(1)}% |
                    Overall Confidence: {(signal.confidence * 100).toFixed(1)}%
                  </p>
                </div>
                <p className="text-xs text-slate-500">{new Date(signal.timestamp).toLocaleTimeString()}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
