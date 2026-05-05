'use client';

import { useSignals } from '@/hooks';
import { useEffect, useState } from 'react';
import { SignalHistoryPoint } from '@/types';
import LineChart from '@/components/charts/LineChart';
import { TrendingUp, TrendingDown, Brain, Zap, Award } from 'lucide-react';

export default function AISignals() {
  const { current, history, loading } = useSignals();
  const [winRate, setWinRate] = useState<number>(0);

  useEffect(() => {
    if (history && history.length > 0) {
      const correctPredictions = history.filter((h) => h.direction === 'UP').length;
      setWinRate((correctPredictions / history.length) * 100);
    } else {
      setWinRate(0);
    }
  }, [history]);

  const safeHistory = history ?? [];
  const highVolatilityRate = safeHistory.length > 0
    ? (safeHistory.filter((h) => h.volatility === 'HIGH').length / safeHistory.length) * 100
    : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-900 p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2.5 rounded-lg bg-gradient-to-br from-fuchsia-500/20 to-pink-500/10 border border-fuchsia-500/30 backdrop-blur-sm">
            <Brain className="w-6 h-6 text-fuchsia-300" />
          </div>
          <h1 className="text-3xl lg:text-4xl font-bold bg-gradient-to-r from-fuchsia-300 via-pink-300 to-fuchsia-300 bg-clip-text text-transparent">
            AI Trading Signals
          </h1>
        </div>
        <p className="text-slate-400 text-sm lg:text-base ml-11">LightGBM Predictions • Confidence Analysis • Signal Performance</p>
      </div>

      {/* Current Signal - Large Featured Card */}
      {current && (
        <div className={`mb-8 relative overflow-hidden rounded-xl border backdrop-blur-md transition-all p-6 lg:p-8 ${
          current.direction === 'UP'
            ? 'border-green-500/40 bg-gradient-to-br from-green-500/25 via-green-500/15 to-transparent'
            : 'border-red-500/40 bg-gradient-to-br from-red-500/25 via-red-500/15 to-transparent'
        }`}>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-5 lg:gap-8">
            {/* Direction */}
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-3">Direction</p>
              <div className="flex items-center gap-3">
                {current.direction === 'UP' ? (
                  <div className="p-2 rounded-lg bg-green-500/20 border border-green-500/30">
                    <TrendingUp className="w-6 h-6 text-green-400" />
                  </div>
                ) : (
                  <div className="p-2 rounded-lg bg-red-500/20 border border-red-500/30">
                    <TrendingDown className="w-6 h-6 text-red-400" />
                  </div>
                )}
                <p className={`text-4xl font-black ${current.direction === 'UP' ? 'text-green-400' : 'text-red-400'}`}>
                  {current.direction}
                </p>
              </div>
            </div>

            {/* Direction Confidence */}
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-3">Direction Prob</p>
              <p className="text-4xl font-black text-cyan-400">{(current.direction_prob * 100).toFixed(1)}%</p>
              <p className="text-xs text-cyan-300 mt-2 font-semibold">{current.direction_prob > 0.7 ? '✓ STRONG' : '⚠ WEAK'}</p>
            </div>

            {/* Volatility */}
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-3">Vol. Expected</p>
              <p className={`text-4xl font-black ${
                current.volatility === 'HIGH' ? 'text-red-400' :
                current.volatility === 'MEDIUM' ? 'text-amber-400' :
                'text-emerald-400'
              }`}>
                {current.volatility}
              </p>
            </div>

            {/* Overall Confidence */}
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-3">Overall Score</p>
              <p className={`text-4xl font-black ${current.confidence > 0.75 ? 'text-green-400' : 'text-amber-400'}`}>
                {(current.confidence * 100).toFixed(0)}%
              </p>
              <p className="text-xs font-semibold mt-2">
                <span className={`${current.confidence > 0.75 ? 'text-green-300' : 'text-amber-300'}`}>{current.confidence > 0.75 ? '✓ HIGH' : '⚠ MEDIUM'}</span>
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Key Metrics - Data Heavy */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        {/* Total Predictions */}
        <div className="group relative overflow-hidden rounded-xl border border-blue-500/30 bg-gradient-to-br from-blue-500/20 to-blue-600/10 backdrop-blur-md transition-all duration-300 hover:shadow-lg hover:scale-105 hover:backdrop-blur-lg p-5">
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Total Signals</p>
                <p className="text-4xl font-black text-blue-400 mt-2">{history.length}</p>
              </div>
              <div className="p-2 rounded-lg bg-blue-500/20 border border-blue-500/30">
                <Award className="w-5 h-5 text-blue-400" />
              </div>
            </div>
            <p className="text-xs text-slate-400">Last 100 analyzed</p>
          </div>
        </div>

        {/* Win Rate */}
        <div className="group relative overflow-hidden rounded-xl border border-green-500/30 bg-gradient-to-br from-green-500/20 to-green-600/10 backdrop-blur-md transition-all duration-300 hover:shadow-lg hover:scale-105 hover:backdrop-blur-lg p-5">
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Win Rate</p>
                <p className="text-4xl font-black text-green-400 mt-2">{winRate.toFixed(1)}%</p>
              </div>
              <div className="p-2 rounded-lg bg-green-500/20 border border-green-500/30">
                <TrendingUp className="w-5 h-5 text-green-400" />
              </div>
            </div>
            <p className="text-xs text-slate-400">Bullish accuracy</p>
          </div>
        </div>

        {/* High Volatility */}
        <div className="group relative overflow-hidden rounded-xl border border-orange-500/30 bg-gradient-to-br from-orange-500/20 to-orange-600/10 backdrop-blur-md transition-all duration-300 hover:shadow-lg hover:scale-105 hover:backdrop-blur-lg p-5">
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">High Volatility</p>
                <p className="text-4xl font-black text-orange-400 mt-2">{highVolatilityRate.toFixed(1)}%</p>
              </div>
              <div className="p-2 rounded-lg bg-orange-500/20 border border-orange-500/30">
                <Zap className="w-5 h-5 text-orange-400" />
              </div>
            </div>
            <p className="text-xs text-slate-400">Of total signals</p>
          </div>
        </div>
      </div>

      {/* Confidence Chart */}
      <div className="mb-8">
        <div className="bg-gradient-to-br from-slate-900/60 via-slate-800/60 to-slate-900/60 rounded-xl border border-slate-600/30 backdrop-blur-xl p-6 shadow-xl">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-3">
              <div className="w-2.5 h-2.5 rounded-full bg-fuchsia-400 animate-pulse"></div>
              Confidence Timeline
            </h2>
            <div className="text-xs text-slate-400 bg-slate-800/50 px-3 py-1.5 rounded-lg border border-slate-700/50">
              Last {history.length} signals
            </div>
          </div>
          <LineChart
            data={history}
            dataKey="confidence"
            stroke="#d946ef"
            title=""
            height={320}
          />
        </div>
      </div>

      {/* Recent Signals - Data Heavy */}
      <div>
        <h2 className="text-lg font-bold text-slate-100 mb-5 flex items-center gap-3">
          <div className="w-2.5 h-2.5 rounded-full bg-pink-400 animate-pulse"></div>
          Signal History
        </h2>
        <div className="grid grid-cols-1 gap-3 max-h-96 overflow-y-auto pr-2">
          {history.slice(0, 10).map((signal, i) => (
            <div
              key={i}
              className={`group hover:shadow-lg hover:scale-102 transition-all rounded-lg border backdrop-blur-sm p-4 ${
                signal.direction === 'UP'
                  ? 'border-green-500/30 bg-gradient-to-r from-green-500/15 to-transparent hover:border-green-500/50 hover:bg-gradient-to-r hover:from-green-500/20'
                  : 'border-red-500/30 bg-gradient-to-r from-red-500/15 to-transparent hover:border-red-500/50 hover:bg-gradient-to-r hover:from-red-500/20'
              }`}
            >
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <div className={`p-1.5 rounded-lg flex-shrink-0 ${signal.direction === 'UP' ? 'bg-green-500/20 border border-green-500/30' : 'bg-red-500/20 border border-red-500/30'}`}>
                    {signal.direction === 'UP' ? (
                      <TrendingUp className="w-4 h-4 text-green-400" />
                    ) : (
                      <TrendingDown className="w-4 h-4 text-red-400" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                      <span className={`px-2.5 py-0.5 rounded-lg text-xs font-bold flex-shrink-0 ${
                        signal.direction === 'UP'
                          ? 'bg-green-500/20 text-green-300'
                          : 'bg-red-500/20 text-red-300'
                      }`}>
                        {signal.direction}
                      </span>
                      <span className={`text-xs font-semibold px-2 py-0.5 rounded-lg flex-shrink-0 ${
                        signal.volatility === 'HIGH' ? 'bg-red-500/20 text-red-300 border border-red-500/30' :
                        signal.volatility === 'MEDIUM' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' :
                        'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                      }`}>
                        {signal.volatility}
                      </span>
                    </div>
                    <p className="text-xs text-slate-400">
                      Dir: <span className="font-semibold text-slate-300">{(signal.direction_prob * 100).toFixed(0)}%</span> | Score: <span className="font-semibold text-slate-300">{(signal.confidence * 100).toFixed(0)}%</span>
                    </p>
                  </div>
                </div>
                <p className="text-xs text-slate-500 whitespace-nowrap flex-shrink-0">{new Date(signal.timestamp).toLocaleTimeString()}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
