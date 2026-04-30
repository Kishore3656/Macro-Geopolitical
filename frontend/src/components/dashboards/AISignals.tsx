'use client';

import { useEffect, useState } from 'react';

interface TradeSignal {
  id: string;
  symbol: string;
  direction: 'UP' | 'DOWN';
  confidence: number;
  volatility: number;
  timestamp: string;
}

export default function AISignals() {
  const [signals, setSignals] = useState<TradeSignal[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSignals = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/signals`);
        const result = await response.json();
        setSignals(Array.isArray(result) ? result : []);
      } catch (error) {
        console.error('Error fetching signals:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSignals();
    const interval = setInterval(fetchSignals, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">AI Trading Signals</h2>
        <p className="text-sm text-slate-400 mt-1">ML-generated trade signals with confidence metrics</p>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <p className="text-slate-400">Loading signals...</p>
        </div>
      ) : signals.length === 0 ? (
        <div className="text-center py-12 border border-slate-700/50 rounded-lg bg-slate-800/30">
          <p className="text-slate-400">No signals available</p>
        </div>
      ) : (
        <div className="overflow-x-auto border border-slate-700/50 rounded-lg bg-slate-800/30">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-700/50 bg-slate-800/50">
                <th className="text-left py-4 px-5 text-slate-300 font-semibold text-sm uppercase tracking-wider">Symbol</th>
                <th className="text-left py-4 px-5 text-slate-300 font-semibold text-sm uppercase tracking-wider">Direction</th>
                <th className="text-left py-4 px-5 text-slate-300 font-semibold text-sm uppercase tracking-wider">Confidence</th>
                <th className="text-left py-4 px-5 text-slate-300 font-semibold text-sm uppercase tracking-wider">Volatility</th>
                <th className="text-left py-4 px-5 text-slate-300 font-semibold text-sm uppercase tracking-wider">Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {signals.map((signal) => (
                <tr key={signal.id} className="border-b border-slate-700/30 hover:bg-slate-800/40 transition-colors">
                  <td className="py-4 px-5 text-white font-medium">{signal.symbol}</td>
                  <td className="py-4 px-5">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold inline-block ${
                        signal.direction === 'UP'
                          ? 'bg-green-500/20 text-green-400'
                          : 'bg-red-500/20 text-red-400'
                      }`}
                    >
                      {signal.direction}
                    </span>
                  </td>
                  <td className="py-4 px-5 text-slate-300 font-medium">{(signal.confidence * 100).toFixed(1)}%</td>
                  <td className="py-4 px-5 text-slate-300">{signal.volatility.toFixed(2)}</td>
                  <td className="py-4 px-5 text-slate-400 text-sm">{new Date(signal.timestamp).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
