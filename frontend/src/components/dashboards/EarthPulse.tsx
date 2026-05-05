'use client';

import { useGTI } from '@/hooks';
import { api } from '@/lib/api';
import { useEffect, useState } from 'react';
import { HeadlineData, ConflictData } from '@/types';
import LineChart from '@/components/charts/LineChart';
import SignalCard from '@/components/ui/SignalCard';
import HeadlineItem from '@/components/ui/HeadlineItem';
import { AlertCircle, TrendingUp, Globe, Zap, Radio } from 'lucide-react';

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

  const getStatusColor = (value: number, thresholds: { danger: number; warning: number }) => {
    if (value >= thresholds.danger) return { bg: 'bg-gradient-to-br from-red-500/20 to-red-600/10', text: 'text-red-400', border: 'border-red-500/30' };
    if (value >= thresholds.warning) return { bg: 'bg-gradient-to-br from-amber-500/20 to-amber-600/10', text: 'text-amber-400', border: 'border-amber-500/30' };
    return { bg: 'bg-gradient-to-br from-emerald-500/20 to-emerald-600/10', text: 'text-emerald-400', border: 'border-emerald-500/30' };
  };

  const gtiScore = gti?.score ?? 0;
  const sentiment = gti?.sentiment ?? 0;
  const volatility = gti?.volatility ?? 0;

  const scoreStatus = getStatusColor(gtiScore * 100, { danger: 60, warning: 40 });
  const sentimentStatus = getStatusColor(Math.abs(sentiment), { danger: 20, warning: 10 });
  const volatilityStatus = getStatusColor(volatility, { danger: 50, warning: 30 });

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-900 p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2.5 rounded-lg bg-gradient-to-br from-cyan-500/20 to-blue-500/10 border border-cyan-500/30 backdrop-blur-sm">
            <Globe className="w-6 h-6 text-cyan-300" />
          </div>
          <h1 className="text-3xl lg:text-4xl font-bold bg-gradient-to-r from-cyan-300 via-blue-300 to-cyan-300 bg-clip-text text-transparent">
            Earth Pulse
          </h1>
        </div>
        <p className="text-slate-400 text-sm lg:text-base ml-11">Global Geopolitical Tension Index & Real-Time Intelligence</p>
      </div>

      {/* Key Metrics Grid - Data Heavy */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {/* GTI Score */}
        <div className={`group relative overflow-hidden rounded-xl border backdrop-blur-md transition-all duration-300 ${scoreStatus.border} ${scoreStatus.bg} hover:shadow-lg hover:scale-105 hover:backdrop-blur-lg p-5`}>
          <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
            <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 to-transparent"></div>
          </div>
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">GTI Score</p>
                <p className={`text-4xl font-black mt-2 ${scoreStatus.text}`}>{(gtiScore * 100).toFixed(0)}</p>
              </div>
              <div className={`p-2 rounded-lg ${scoreStatus.bg} border ${scoreStatus.border}`}>
                <Zap className={`w-5 h-5 ${scoreStatus.text}`} />
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">Status</span>
                <span className={`font-semibold ${scoreStatus.text}`}>{gtiScore * 100 >= 60 ? 'CRITICAL' : gtiScore * 100 >= 40 ? 'ELEVATED' : 'NORMAL'}</span>
              </div>
              <div className="w-full h-1.5 bg-slate-700/40 rounded-full overflow-hidden">
                <div className={`h-full ${scoreStatus.text} bg-gradient-to-r ${scoreStatus.bg} rounded-full`} style={{width: `${(gtiScore * 100)}%`}}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Sentiment */}
        <div className={`group relative overflow-hidden rounded-xl border backdrop-blur-md transition-all duration-300 ${sentimentStatus.border} ${sentimentStatus.bg} hover:shadow-lg hover:scale-105 hover:backdrop-blur-lg p-5`}>
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Sentiment</p>
                <p className={`text-4xl font-black mt-2 ${sentimentStatus.text}`}>{sentiment.toFixed(1)}</p>
              </div>
              <div className={`p-2 rounded-lg ${sentimentStatus.bg} border ${sentimentStatus.border}`}>
                <Radio className={`w-5 h-5 ${sentimentStatus.text}`} />
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">Outlook</span>
                <span className={`font-semibold ${sentimentStatus.text}`}>{sentiment < -10 ? 'NEGATIVE' : sentiment > 10 ? 'POSITIVE' : 'NEUTRAL'}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Volatility */}
        <div className={`group relative overflow-hidden rounded-xl border backdrop-blur-md transition-all duration-300 ${volatilityStatus.border} ${volatilityStatus.bg} hover:shadow-lg hover:scale-105 hover:backdrop-blur-lg p-5`}>
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Volatility</p>
                <p className={`text-4xl font-black mt-2 ${volatilityStatus.text}`}>{volatility.toFixed(0)}</p>
              </div>
              <div className={`p-2 rounded-lg ${volatilityStatus.bg} border ${volatilityStatus.border}`}>
                <TrendingUp className={`w-5 h-5 ${volatilityStatus.text}`} />
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">Level</span>
                <span className={`font-semibold ${volatilityStatus.text}`}>{volatility > 50 ? 'HIGH' : volatility > 30 ? 'MODERATE' : 'LOW'}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Active Events */}
        <div className="group relative overflow-hidden rounded-xl border backdrop-blur-md transition-all duration-300 border-emerald-500/30 bg-gradient-to-br from-emerald-500/20 to-emerald-600/10 hover:shadow-lg hover:scale-105 hover:backdrop-blur-lg p-5">
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Active Events</p>
                <p className="text-4xl font-black text-emerald-400 mt-2">{conflicts?.total_events || '0'}</p>
              </div>
              <div className="p-2 rounded-lg bg-emerald-500/20 border border-emerald-500/30">
                <AlertCircle className="w-5 h-5 text-emerald-400" />
              </div>
            </div>
            <div className="text-xs text-slate-400">Geopolitical incidents</div>
          </div>
        </div>
      </div>

      {/* Main Chart */}
      <div className="mb-8">
        <div className="bg-gradient-to-br from-slate-900/60 via-slate-800/60 to-slate-900/60 rounded-xl border border-slate-600/30 backdrop-blur-xl p-6 shadow-xl">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-3">
              <div className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></div>
              Tension Index Trend (48H)
            </h2>
            <div className="text-xs text-slate-400 bg-slate-800/50 px-3 py-1.5 rounded-lg border border-slate-700/50">
              Updated: Now
            </div>
          </div>
          <LineChart
            data={gtiHistory}
            dataKey="score"
            stroke="#06b6d4"
            title=""
            height={320}
          />
          <div className="grid grid-cols-3 gap-4 mt-6 pt-4 border-t border-slate-700/30">
            <div className="text-center">
              <p className="text-xs text-slate-400">Current</p>
              <p className="text-lg font-bold text-cyan-400">{(gtiScore * 100).toFixed(1)}</p>
            </div>
            <div className="text-center">
              <p className="text-xs text-slate-400">Max (48H)</p>
              <p className="text-lg font-bold text-red-400">{gtiHistory && gtiHistory.length > 0 ? Math.max(...gtiHistory.map((h: any) => h.score * 100)).toFixed(1) : '-'}</p>
            </div>
            <div className="text-center">
              <p className="text-xs text-slate-400">Min (48H)</p>
              <p className="text-lg font-bold text-green-400">{gtiHistory && gtiHistory.length > 0 ? Math.min(...gtiHistory.map((h: any) => h.score * 100)).toFixed(1) : '-'}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Grid - Data Heavy */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Headlines */}
        <div className="lg:col-span-2">
          <div className="bg-gradient-to-br from-slate-900/60 via-slate-800/60 to-slate-900/60 rounded-xl border border-slate-600/30 backdrop-blur-xl p-6 shadow-xl h-full">
            <div className="flex items-center justify-between mb-5">
              <h2 className="text-lg font-bold text-slate-100 flex items-center gap-3">
                <div className="w-2.5 h-2.5 rounded-full bg-blue-400 animate-pulse"></div>
                Top Headlines
              </h2>
              <span className="text-xs text-slate-400 bg-slate-800/50 px-2 py-1 rounded border border-slate-700/50">{headlines?.headlines.length || 0} items</span>
            </div>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {headlines?.headlines.slice(0, 6).map((headline, i) => (
                <HeadlineItem key={i} headline={headline} />
              ))}
            </div>
          </div>
        </div>

        {/* Signals & Conflicts */}
        <div className="space-y-6">
          <div className="bg-gradient-to-br from-slate-900/60 via-slate-800/60 to-slate-900/60 rounded-xl border border-slate-600/30 backdrop-blur-xl p-6 shadow-xl">
            <SignalCard signal={null} loading={gtiLoading} />
          </div>

          <div className="bg-gradient-to-br from-slate-900/60 via-slate-800/60 to-slate-900/60 rounded-xl border border-slate-600/30 backdrop-blur-xl p-6 shadow-xl">
            <h3 className="text-lg font-bold text-slate-100 mb-4 flex items-center gap-3">
              <div className="w-2.5 h-2.5 rounded-full bg-red-400 animate-pulse"></div>
              Critical Zones
            </h3>
            <div className="space-y-2.5">
              {conflicts?.conflicts.slice(0, 5).map((conflict, i) => (
                <div key={i} className="group hover:bg-slate-700/40 rounded-lg p-3.5 transition-all border border-slate-700/30 hover:border-slate-600/50 cursor-pointer">
                  <div className="flex justify-between items-start gap-2 mb-1.5">
                    <p className="font-semibold text-slate-200 group-hover:text-slate-100 text-sm">{conflict.country}</p>
                    <span className={`text-xs font-bold px-2.5 py-0.5 rounded-lg whitespace-nowrap ${
                      conflict.severity === 'high' ? 'bg-red-500/30 text-red-200 border border-red-500/40' :
                      conflict.severity === 'medium' ? 'bg-amber-500/30 text-amber-200 border border-amber-500/40' :
                      'bg-emerald-500/30 text-emerald-200 border border-emerald-500/40'
                    }`}>
                      {conflict.severity.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">{conflict.count} events</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
