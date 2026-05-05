'use client';

import { useMarket } from '@/hooks';
import { useEffect, useState } from 'react';
import { SectorData } from '@/types';
import CandlestickChart from '@/components/charts/CandlestickChart';
import { TrendingUp, TrendingDown, BarChart3, Zap, Activity } from 'lucide-react';

export default function Market() {
  const { spy, sectors, loading } = useMarket();
  const [dailyChange, setDailyChange] = useState<number | null>(null);

  useEffect(() => {
    if (spy?.current_price && spy.bars.length > 0) {
      const firstBar = spy.bars[0];
      const change = ((spy.current_price - firstBar.open) / firstBar.open) * 100;
      setDailyChange(change);
    }
  }, [spy]);

  const highestHigh = spy?.bars && spy.bars.length > 0 ? Math.max(...spy.bars.map(b => b.high)) : null;
  const lowestLow = spy?.bars && spy.bars.length > 0 ? Math.min(...spy.bars.map(b => b.low)) : null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-900 p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2.5 rounded-lg bg-gradient-to-br from-emerald-500/20 to-green-500/10 border border-emerald-500/30 backdrop-blur-sm">
            <BarChart3 className="w-6 h-6 text-emerald-300" />
          </div>
          <h1 className="text-3xl lg:text-4xl font-bold bg-gradient-to-r from-emerald-300 via-green-300 to-teal-300 bg-clip-text text-transparent">
            Market Intelligence
          </h1>
        </div>
        <p className="text-slate-400 text-sm lg:text-base ml-11">S&P 500 Analysis • Sector Performance • Trading Indicators</p>
      </div>

      {/* Key Metrics - Data Heavy */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {/* SPY Price */}
        <div className="group relative overflow-hidden rounded-xl border border-emerald-500/30 bg-gradient-to-br from-emerald-500/20 to-emerald-600/10 backdrop-blur-md transition-all duration-300 hover:shadow-lg hover:scale-105 hover:backdrop-blur-lg p-5">
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">SPY Price</p>
                <p className="text-4xl font-black text-emerald-400 mt-2">${spy?.current_price?.toFixed(2) || '-'}</p>
              </div>
              <div className="p-2 rounded-lg bg-emerald-500/20 border border-emerald-500/30">
                <Activity className="w-5 h-5 text-emerald-400" />
              </div>
            </div>
            <div className="space-y-2">
              <p className="text-xs text-slate-400">S&P 500 ETF</p>
            </div>
          </div>
        </div>

        {/* Daily Change */}
        <div className={`group relative overflow-hidden rounded-xl border backdrop-blur-md transition-all duration-300 hover:shadow-lg hover:scale-105 hover:backdrop-blur-lg p-5 ${
          dailyChange && dailyChange > 0
            ? 'border-green-500/30 bg-gradient-to-br from-green-500/20 to-green-600/10'
            : 'border-red-500/30 bg-gradient-to-br from-red-500/20 to-red-600/10'
        }`}>
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Daily Change</p>
                <p className={`text-4xl font-black mt-2 ${dailyChange && dailyChange > 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {dailyChange ? `${dailyChange > 0 ? '+' : ''}${dailyChange.toFixed(2)}%` : '-'}
                </p>
              </div>
              <div className={`p-2 rounded-lg ${dailyChange && dailyChange > 0 ? 'bg-green-500/20 border border-green-500/30' : 'bg-red-500/20 border border-red-500/30'}`}>
                {dailyChange && dailyChange > 0 ? (
                  <TrendingUp className="w-5 h-5 text-green-400" />
                ) : (
                  <TrendingDown className="w-5 h-5 text-red-400" />
                )}
              </div>
            </div>
            <div className="text-xs font-semibold">
              <span className={`${dailyChange && dailyChange > 0 ? 'text-green-400' : 'text-red-400'}`}>{dailyChange && dailyChange > 0 ? 'BULLISH' : 'BEARISH'}</span>
            </div>
          </div>
        </div>

        {/* Volume */}
        <div className="group relative overflow-hidden rounded-xl border border-blue-500/30 bg-gradient-to-br from-blue-500/20 to-blue-600/10 backdrop-blur-md transition-all duration-300 hover:shadow-lg hover:scale-105 hover:backdrop-blur-lg p-5">
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Volume</p>
                <p className="text-4xl font-black text-blue-400 mt-2">{spy?.bars[0]?.volume ? `${(spy.bars[0].volume / 1000000).toFixed(1)}M` : '-'}</p>
              </div>
              <div className="p-2 rounded-lg bg-blue-500/20 border border-blue-500/30">
                <Zap className="w-5 h-5 text-blue-400" />
              </div>
            </div>
            <p className="text-xs text-slate-400">Daily volume</p>
          </div>
        </div>

        {/* 52W Range */}
        <div className="group relative overflow-hidden rounded-xl border border-purple-500/30 bg-gradient-to-br from-purple-500/20 to-purple-600/10 backdrop-blur-md transition-all duration-300 hover:shadow-lg hover:scale-105 hover:backdrop-blur-lg p-5">
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">52W Range</p>
                <p className="text-2xl font-black text-purple-400 mt-2">${highestHigh?.toFixed(0) || '-'}</p>
              </div>
              <div className="p-2 rounded-lg bg-purple-500/20 border border-purple-500/30">
                <Activity className="w-5 h-5 text-purple-400" />
              </div>
            </div>
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">High</span>
                <span className="text-purple-300 font-semibold">${highestHigh?.toFixed(2) || '-'}</span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">Low</span>
                <span className="text-purple-300 font-semibold">${lowestLow?.toFixed(2) || '-'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Chart Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2">
          <div className="bg-gradient-to-br from-slate-900/60 via-slate-800/60 to-slate-900/60 rounded-xl border border-slate-600/30 backdrop-blur-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-bold text-slate-100 flex items-center gap-3">
                <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></div>
                SPY Price Action (5D)
              </h2>
              <div className="text-xs text-slate-400 bg-slate-800/50 px-3 py-1.5 rounded-lg border border-slate-700/50">
                1H Bars
              </div>
            </div>
            <CandlestickChart
              data={spy?.bars || []}
              title=""
              height={300}
            />
          </div>
        </div>

        {/* Market State */}
        <div className="bg-gradient-to-br from-slate-900/60 via-slate-800/60 to-slate-900/60 rounded-xl border border-slate-600/30 backdrop-blur-xl p-6 shadow-xl">
          <h3 className="text-lg font-bold text-slate-100 mb-5 flex items-center gap-3">
            <div className="w-2.5 h-2.5 rounded-full bg-blue-400 animate-pulse"></div>
            Technical State
          </h3>
          <div className="space-y-3">
            {/* Trend */}
            <div className="group hover:bg-slate-700/40 rounded-lg p-4 border border-slate-700/30 hover:border-slate-600/50 transition-all cursor-pointer">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Trend Direction</p>
              <p className={`text-lg font-bold mt-2.5 ${dailyChange && dailyChange > 0 ? 'text-green-400' : 'text-red-400'}`}>
                {dailyChange && dailyChange > 0 ? '↑ BULLISH' : '↓ BEARISH'}
              </p>
            </div>

            {/* Volatility */}
            <div className="group hover:bg-slate-700/40 rounded-lg p-4 border border-slate-700/30 hover:border-slate-600/50 transition-all cursor-pointer">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Vol. Level</p>
              <p className="text-lg font-bold mt-2.5 text-amber-400">⚡ ELEVATED</p>
            </div>

            {/* RSI */}
            <div className="group hover:bg-slate-700/40 rounded-lg p-4 border border-slate-700/30 hover:border-slate-600/50 transition-all cursor-pointer">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Momentum</p>
              <p className="text-lg font-bold mt-2.5 text-cyan-400">💪 STRONG</p>
            </div>
          </div>
        </div>
      </div>

      {/* Sector Performance - Data Heavy */}
      <div>
        <h2 className="text-lg font-bold text-slate-100 mb-5 flex items-center gap-3">
          <div className="w-2.5 h-2.5 rounded-full bg-purple-400 animate-pulse"></div>
          Sector Performance
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {sectors?.sectors.slice(0, 8).map((sector, i) => {
            const isPositive = sector.change_pct >= 0;
            return (
              <div
                key={i}
                className={`group relative overflow-hidden rounded-xl border backdrop-blur-md transition-all duration-300 hover:scale-105 hover:shadow-lg p-5 ${
                  isPositive
                    ? 'border-green-500/30 bg-gradient-to-br from-green-500/20 to-green-600/10'
                    : 'border-red-500/30 bg-gradient-to-br from-red-500/20 to-red-600/10'
                }`}
              >
                <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
                  <div className={`absolute inset-0 bg-gradient-to-br ${isPositive ? 'from-green-500/10' : 'from-red-500/10'} to-transparent`}></div>
                </div>
                <div className="relative z-10">
                  <div className="flex items-start justify-between mb-3">
                    <h4 className="text-sm font-semibold text-slate-200 group-hover:text-slate-100 flex-1">{sector.name}</h4>
                    <div className={`p-1.5 rounded-lg ${isPositive ? 'bg-green-500/20 border border-green-500/30' : 'bg-red-500/20 border border-red-500/30'}`}>
                      {isPositive ? (
                        <TrendingUp className="w-4 h-4 text-green-400" />
                      ) : (
                        <TrendingDown className="w-4 h-4 text-red-400" />
                      )}
                    </div>
                  </div>
                  <p className={`text-3xl font-black ${isPositive ? 'text-green-400' : 'text-red-400'}`}>
                    {sector.performance !== undefined ? sector.performance.toFixed(1) : '-'}
                  </p>
                  <p className={`text-sm font-semibold mt-2 ${isPositive ? 'text-green-300' : 'text-red-300'}`}>
                    {isPositive ? '↑' : '↓'} {Math.abs(sector.change_pct).toFixed(2)}%
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
