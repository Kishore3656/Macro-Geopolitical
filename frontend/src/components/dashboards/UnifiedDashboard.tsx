'use client';

import { useSignals, useMarket, useGTI } from '@/hooks';
import { api } from '@/lib/api';
import { useEffect, useState } from 'react';
import { SignalHistoryPoint, BilateralData, GeoEventData } from '@/types';
import { TrendingUp, TrendingDown, Brain, BarChart3, Globe, AlertTriangle, Zap, Activity, MapPin, Clock } from 'lucide-react';

export default function UnifiedDashboard() {
  const { current: signal, history: signalHistory } = useSignals();
  const { spy, sectors } = useMarket();
  const { current: gti } = useGTI();
  const [bilateral, setBilateral] = useState<BilateralData | null>(null);
  const [events, setEvents] = useState<GeoEventData | null>(null);
  const [topSignals, setTopSignals] = useState<SignalHistoryPoint[]>([]);

  useEffect(() => {
    const loadGeoData = async () => {
      const [bilateralRes, eventsRes] = await Promise.all([
        api.bilateral(20),
        api.events(30),
      ]);
      if (!('error' in bilateralRes)) setBilateral(bilateralRes);
      if (!('error' in eventsRes)) setEvents(eventsRes);
    };
    loadGeoData();
  }, []);

  useEffect(() => {
    if (signalHistory && signalHistory.length > 0) {
      setTopSignals(signalHistory.slice(0, 5));
    }
  }, [signalHistory]);

  const dailyChange = spy?.daily_change_pct ?? 0;
  const gtiScore = gti?.score ?? 0;
  const criticalRelations = bilateral?.relations.filter(r => r.stress_category === 'critical').length || 0;
  const recentEvents = events?.events.length || 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-900 p-6 lg:p-8">
      {/* Header with Real-Time Status */}
      <div className="mb-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
          <div>
            <h1 className="text-4xl lg:text-5xl font-black bg-gradient-to-r from-cyan-300 via-blue-300 to-purple-300 bg-clip-text text-transparent mb-2">
              Trading Command Center
            </h1>
            <p className="text-slate-400 flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
              Real-time market analysis • Geopolitical intelligence • ML predictions
            </p>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800/40 border border-slate-700/50 w-fit">
            <Clock className="w-4 h-4 text-slate-400" />
            <span className="text-sm text-slate-300">{new Date().toLocaleTimeString()}</span>
          </div>
        </div>
      </div>

      {/* Primary Alert Band - Current Signal + GTI + Market */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* AI Signal - Largest */}
        {signal && (
          <div className={`lg:col-span-1 relative overflow-hidden rounded-2xl border backdrop-blur-md p-8 transition-all ${
            signal.direction === 'UP'
              ? 'border-green-500/40 bg-gradient-to-br from-green-500/25 via-green-500/15 to-transparent'
              : 'border-red-500/40 bg-gradient-to-br from-red-500/25 via-red-500/15 to-transparent'
          }`}>
            <div className="flex items-center gap-3 mb-6">
              <div className={`p-3 rounded-lg ${signal.direction === 'UP' ? 'bg-green-500/20 border border-green-500/30' : 'bg-red-500/20 border border-red-500/30'}`}>
                <Brain className={`w-6 h-6 ${signal.direction === 'UP' ? 'text-green-400' : 'text-red-400'}`} />
              </div>
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase">ML Signal</p>
                <p className={`text-3xl font-black ${signal.direction === 'UP' ? 'text-green-400' : 'text-red-400'}`}>
                  {signal.direction}
                </p>
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <p className="text-xs text-slate-400 mb-1">Confidence</p>
                <div className="flex items-end gap-3">
                  <p className="text-2xl font-black text-cyan-400">{(signal.confidence * 100).toFixed(0)}%</p>
                  <span className={`text-xs font-semibold px-2 py-1 rounded ${signal.confidence > 0.75 ? 'bg-green-500/20 text-green-300' : 'bg-amber-500/20 text-amber-300'}`}>
                    {signal.confidence > 0.75 ? '✓ HIGH' : '⚠ MEDIUM'}
                  </span>
                </div>
              </div>
              <div>
                <p className="text-xs text-slate-400 mb-1">Volatility</p>
                <p className={`text-lg font-bold ${
                  signal.volatility === 'HIGH' ? 'text-red-400' :
                  signal.volatility === 'MEDIUM' ? 'text-amber-400' :
                  'text-emerald-400'
                }`}>
                  {signal.volatility}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Market Status */}
        <div className={`relative overflow-hidden rounded-2xl border backdrop-blur-md p-8 transition-all ${
          dailyChange > 0
            ? 'border-green-500/40 bg-gradient-to-br from-green-500/20 to-green-600/10'
            : 'border-red-500/40 bg-gradient-to-br from-red-500/20 to-red-600/10'
        }`}>
          <div className="flex items-center gap-3 mb-6">
            <div className={`p-3 rounded-lg ${dailyChange > 0 ? 'bg-green-500/20 border border-green-500/30' : 'bg-red-500/20 border border-red-500/30'}`}>
              <BarChart3 className={`w-6 h-6 ${dailyChange > 0 ? 'text-green-400' : 'text-red-400'}`} />
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase">SPY</p>
              <p className="text-2xl font-black text-slate-100">${spy?.current_price?.toFixed(2) || '-'}</p>
            </div>
          </div>
          <div className="space-y-4">
            <div>
              <p className="text-xs text-slate-400 mb-1">Daily Change</p>
              <p className={`text-3xl font-black ${dailyChange > 0 ? 'text-green-400' : 'text-red-400'}`}>
                {dailyChange > 0 ? '+' : ''}{dailyChange.toFixed(2)}%
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-400 mb-1">Status</p>
              <p className={`text-lg font-bold ${dailyChange > 0 ? 'text-green-400' : 'text-red-400'}`}>
                {dailyChange > 0 ? '↑ BULLISH' : '↓ BEARISH'}
              </p>
            </div>
          </div>
        </div>

        {/* Geopolitical Threat Level */}
        <div className={`relative overflow-hidden rounded-2xl border backdrop-blur-md p-8 transition-all ${
          gtiScore * 100 >= 60
            ? 'border-red-500/40 bg-gradient-to-br from-red-500/20 to-red-600/10'
            : gtiScore * 100 >= 40
            ? 'border-amber-500/40 bg-gradient-to-br from-amber-500/20 to-amber-600/10'
            : 'border-emerald-500/40 bg-gradient-to-br from-emerald-500/20 to-emerald-600/10'
        }`}>
          <div className="flex items-center gap-3 mb-6">
            <div className={`p-3 rounded-lg ${
              gtiScore * 100 >= 60 ? 'bg-red-500/20 border border-red-500/30' :
              gtiScore * 100 >= 40 ? 'bg-amber-500/20 border border-amber-500/30' :
              'bg-emerald-500/20 border border-emerald-500/30'
            }`}>
              <Globe className={`w-6 h-6 ${
                gtiScore * 100 >= 60 ? 'text-red-400' :
                gtiScore * 100 >= 40 ? 'text-amber-400' :
                'text-emerald-400'
              }`} />
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase">GTI Score</p>
              <p className={`text-3xl font-black ${
                gtiScore * 100 >= 60 ? 'text-red-400' :
                gtiScore * 100 >= 40 ? 'text-amber-400' :
                'text-emerald-400'
              }`}>
                {(gtiScore * 100).toFixed(0)}
              </p>
            </div>
          </div>
          <div className="space-y-4">
            <div>
              <p className="text-xs text-slate-400 mb-1">Risk Level</p>
              <p className={`text-lg font-bold ${
                gtiScore * 100 >= 60 ? 'text-red-400' :
                gtiScore * 100 >= 40 ? 'text-amber-400' :
                'text-emerald-400'
              }`}>
                {gtiScore * 100 >= 60 ? '🔴 CRITICAL' : gtiScore * 100 >= 40 ? '🟡 ELEVATED' : '🟢 NORMAL'}
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-400 mb-1">Geopolitical Events</p>
              <p className="text-lg font-bold text-slate-100">{recentEvents}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Data Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Signal Performance Table */}
        <div className="lg:col-span-2 bg-gradient-to-br from-slate-900/60 via-slate-800/60 to-slate-900/60 rounded-2xl border border-slate-600/30 backdrop-blur-xl p-6 shadow-xl">
          <h2 className="text-lg font-bold text-slate-100 mb-6 flex items-center gap-3">
            <div className="w-2.5 h-2.5 rounded-full bg-fuchsia-400 animate-pulse"></div>
            Recent Predictions (Top 5)
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-700/50">
                  <th className="text-left py-3 px-4 text-xs font-semibold text-slate-400 uppercase">Time</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-slate-400 uppercase">Direction</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-slate-400 uppercase">Dir Prob</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-slate-400 uppercase">Volatility</th>
                </tr>
              </thead>
              <tbody>
                {topSignals.map((sig, i) => (
                  <tr key={i} className="border-b border-slate-700/30 hover:bg-slate-700/20 transition-colors">
                    <td className="py-3 px-4 text-slate-300">{new Date(sig.timestamp).toLocaleTimeString()}</td>
                    <td className="py-3 px-4">
                      <span className={`px-3 py-1 rounded-lg text-xs font-bold ${
                        sig.direction === 'UP'
                          ? 'bg-green-500/20 text-green-300'
                          : 'bg-red-500/20 text-red-300'
                      }`}>
                        {sig.direction === 'UP' ? '↑' : '↓'} {sig.direction}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-cyan-400 font-semibold">{(sig.direction_prob * 100).toFixed(0)}%</span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`text-xs font-semibold ${
                        sig.volatility === 'HIGH' ? 'text-red-400' :
                        sig.volatility === 'MEDIUM' ? 'text-amber-400' :
                        'text-emerald-400'
                      }`}>
                        {sig.volatility}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="space-y-6">
          {/* Sector Leaders */}
          <div className="bg-gradient-to-br from-slate-900/60 via-slate-800/60 to-slate-900/60 rounded-2xl border border-slate-600/30 backdrop-blur-xl p-6 shadow-xl">
            <h3 className="text-lg font-bold text-slate-100 mb-4 flex items-center gap-3">
              <div className="w-2.5 h-2.5 rounded-full bg-purple-400 animate-pulse"></div>
              Top Sectors
            </h3>
            <div className="space-y-3">
              {sectors?.sectors.slice(0, 4).map((sector, i) => (
                <div key={i} className="flex items-center justify-between p-3 rounded-lg hover:bg-slate-700/30 transition-colors border border-slate-700/20">
                  <p className="text-sm font-medium text-slate-200">{sector.name}</p>
                  <p className={`text-sm font-bold ${sector.change_pct >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {sector.change_pct >= 0 ? '+' : ''}{sector.change_pct.toFixed(2)}%
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Critical Zones */}
          <div className="bg-gradient-to-br from-slate-900/60 via-slate-800/60 to-slate-900/60 rounded-2xl border border-slate-600/30 backdrop-blur-xl p-6 shadow-xl">
            <h3 className="text-lg font-bold text-slate-100 mb-4 flex items-center gap-3">
              <div className="w-2.5 h-2.5 rounded-full bg-red-400 animate-pulse"></div>
              Critical Zones
            </h3>
            <div className="space-y-3">
              {bilateral?.relations.filter(r => r.stress_category === 'critical').slice(0, 3).map((rel, i) => (
                <div key={i} className="p-3 rounded-lg hover:bg-slate-700/30 transition-colors border border-red-500/20 bg-red-500/5">
                  <p className="text-sm font-semibold text-slate-100">{rel.country1} ↔ {rel.country2}</p>
                  <p className="text-xs text-slate-400 mt-1">Stress: {rel.stress_level.toFixed(1)}/10</p>
                </div>
              ))}
              {criticalRelations === 0 && (
                <p className="text-xs text-slate-400 text-center py-4">No critical zones detected</p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Grid - Bilateral Relations & Recent Events */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Bilateral Relations Map */}
        <div className="bg-gradient-to-br from-slate-900/60 via-slate-800/60 to-slate-900/60 rounded-2xl border border-slate-600/30 backdrop-blur-xl p-6 shadow-xl">
          <h2 className="text-lg font-bold text-slate-100 mb-6 flex items-center gap-3">
            <MapPin className="w-5 h-5 text-violet-400" />
            Bilateral Relations (All Tensions)
          </h2>
          <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
            {bilateral?.relations.map((rel, i) => (
              <div
                key={i}
                className={`group hover:shadow-lg transition-all rounded-lg border backdrop-blur-sm p-4 ${
                  rel.stress_category === 'critical'
                    ? 'border-red-500/30 bg-red-500/5 hover:border-red-500/50'
                    : rel.stress_category === 'tense'
                    ? 'border-amber-500/30 bg-amber-500/5 hover:border-amber-500/50'
                    : 'border-slate-600/30 bg-slate-700/10 hover:border-slate-600/50'
                }`}
              >
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div>
                    <p className="font-semibold text-slate-100 text-sm">{rel.country1} ↔ {rel.country2}</p>
                    <p className="text-xs text-slate-400 mt-1">{rel.recent_events} recent events</p>
                  </div>
                  <span className={`text-xs font-bold px-3 py-1 rounded-lg whitespace-nowrap ${
                    rel.stress_category === 'critical' ? 'bg-red-500/30 text-red-300' :
                    rel.stress_category === 'tense' ? 'bg-amber-500/30 text-amber-300' :
                    'bg-slate-500/30 text-slate-300'
                  }`}>
                    {rel.stress_level.toFixed(1)}/10
                  </span>
                </div>
                <div className="w-full h-1 bg-slate-600/30 rounded-full overflow-hidden">
                  <div
                    className={`h-full transition-all ${
                      rel.stress_category === 'critical' ? 'bg-red-500' :
                      rel.stress_category === 'tense' ? 'bg-amber-500' :
                      'bg-slate-500'
                    }`}
                    style={{ width: `${(rel.stress_level / 10) * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Geopolitical Events */}
        <div className="bg-gradient-to-br from-slate-900/60 via-slate-800/60 to-slate-900/60 rounded-2xl border border-slate-600/30 backdrop-blur-xl p-6 shadow-xl">
          <h2 className="text-lg font-bold text-slate-100 mb-6 flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-orange-400" />
            Recent Geopolitical Events
          </h2>
          <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
            {events?.events.slice(0, 10).map((event, i) => {
              const intensity = event.goldstein_scale ?? 5;
              const isHighIntensity = intensity > 7;
              const isMediumIntensity = intensity > 4;

              return (
                <div
                  key={i}
                  className={`group hover:shadow-lg transition-all rounded-lg border backdrop-blur-sm p-4 ${
                    isHighIntensity
                      ? 'border-red-500/30 bg-red-500/5 hover:border-red-500/50'
                      : isMediumIntensity
                      ? 'border-amber-500/30 bg-amber-500/5 hover:border-amber-500/50'
                      : 'border-emerald-500/30 bg-emerald-500/5 hover:border-emerald-500/50'
                  }`}
                >
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div>
                      <p className="font-semibold text-slate-100 text-sm">{event.country}</p>
                      <p className="text-xs text-slate-400 mt-1">{event.location} • {event.event_type}</p>
                    </div>
                    <span className={`text-xs font-bold px-3 py-1 rounded-lg whitespace-nowrap ${
                      isHighIntensity ? 'bg-red-500/30 text-red-300' :
                      isMediumIntensity ? 'bg-amber-500/30 text-amber-300' :
                      'bg-emerald-500/30 text-emerald-300'
                    }`}>
                      {intensity.toFixed(1)}
                    </span>
                  </div>
                  <p className="text-xs text-slate-500">{new Date(event.timestamp).toLocaleDateString()}</p>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
