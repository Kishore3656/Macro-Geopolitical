'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { BilateralData, GeoEventData } from '@/types';
import BilateralCard from '@/components/ui/BilateralCard';
import { AlertTriangle, Globe, Zap, MapPin, AlertCircle } from 'lucide-react';

export default function GeoMap() {
  const [bilateral, setBilateral] = useState<BilateralData | null>(null);
  const [events, setEvents] = useState<GeoEventData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      const [bilateralRes, eventsRes] = await Promise.all([
        api.bilateral(20),
        api.events(30),
      ]);

      if (!('error' in bilateralRes)) setBilateral(bilateralRes);
      if (!('error' in eventsRes)) setEvents(eventsRes);
      setLoading(false);
    };

    loadData();
  }, []);

  const criticalCount = bilateral?.relations.filter(r => r.stress_category === 'critical').length || 0;
  const tenseCount = bilateral?.relations.filter(r => r.stress_category === 'tense').length || 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-900 p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2.5 rounded-lg bg-gradient-to-br from-indigo-500/20 to-violet-500/10 border border-indigo-500/30 backdrop-blur-sm">
            <MapPin className="w-6 h-6 text-indigo-300" />
          </div>
          <h1 className="text-3xl lg:text-4xl font-bold bg-gradient-to-r from-indigo-300 via-violet-300 to-indigo-300 bg-clip-text text-transparent">
            Geopolitical Intelligence
          </h1>
        </div>
        <p className="text-slate-400 text-sm lg:text-base ml-11">Bilateral Relations • Stress Levels • Regional Events</p>
      </div>

      {/* Key Metrics - Data Heavy */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        {/* Total Relations */}
        <div className="group relative overflow-hidden rounded-xl border border-violet-500/30 bg-gradient-to-br from-violet-500/20 to-violet-600/10 backdrop-blur-md transition-all duration-300 hover:shadow-lg hover:scale-105 hover:backdrop-blur-lg p-5">
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Total Relations</p>
                <p className="text-4xl font-black text-violet-400 mt-2">{bilateral?.relations.length || 0}</p>
              </div>
              <div className="p-2 rounded-lg bg-violet-500/20 border border-violet-500/30">
                <Globe className="w-5 h-5 text-violet-400" />
              </div>
            </div>
            <p className="text-xs text-slate-400">Country pairs tracked</p>
          </div>
        </div>

        {/* Critical Zones */}
        <div className="group relative overflow-hidden rounded-xl border border-red-500/30 bg-gradient-to-br from-red-500/20 to-red-600/10 backdrop-blur-md transition-all duration-300 hover:shadow-lg hover:scale-105 hover:backdrop-blur-lg p-5">
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Critical Zones</p>
                <p className="text-4xl font-black text-red-400 mt-2">{criticalCount}</p>
              </div>
              <div className="p-2 rounded-lg bg-red-500/20 border border-red-500/30">
                <AlertTriangle className="w-5 h-5 text-red-400" />
              </div>
            </div>
            <p className="text-xs text-slate-400">{tenseCount} tense relations</p>
          </div>
        </div>

        {/* Recent Events */}
        <div className="group relative overflow-hidden rounded-xl border border-orange-500/30 bg-gradient-to-br from-orange-500/20 to-orange-600/10 backdrop-blur-md transition-all duration-300 hover:shadow-lg hover:scale-105 hover:backdrop-blur-lg p-5">
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Recent Events</p>
                <p className="text-4xl font-black text-orange-400 mt-2">{events?.events.length || 0}</p>
              </div>
              <div className="p-2 rounded-lg bg-orange-500/20 border border-orange-500/30">
                <AlertCircle className="w-5 h-5 text-orange-400" />
              </div>
            </div>
            <p className="text-xs text-slate-400">Last 30 events</p>
          </div>
        </div>
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Bilateral Relations */}
        <div className="bg-gradient-to-br from-slate-900/80 via-slate-800/80 to-slate-900/80 rounded-2xl border border-slate-700/50 backdrop-blur-xl p-6 shadow-xl">
          <h2 className="text-xl font-bold text-slate-100 mb-6 flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-violet-400 animate-pulse"></div>
            Bilateral Relations (Top Tensions)
          </h2>
          <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
            {bilateral?.relations.slice(0, 10).map((relation, i) => (
              <BilateralCard key={i} relation={relation} />
            ))}
          </div>
        </div>

        {/* Geopolitical Events */}
        <div className="bg-gradient-to-br from-slate-900/80 via-slate-800/80 to-slate-900/80 rounded-2xl border border-slate-700/50 backdrop-blur-xl p-6 shadow-xl">
          <h2 className="text-xl font-bold text-slate-100 mb-6 flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-orange-400 animate-pulse"></div>
            Recent Geopolitical Events
          </h2>
          <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
            {events?.events.slice(0, 10).map((event, i) => {
              const intensity = (event.goldstein_scale ?? 5);
              const isHighIntensity = intensity > 7;
              const isMediumIntensity = intensity > 4;

              return (
                <div
                  key={i}
                  className={`group hover:shadow-lg transition-all rounded-xl border backdrop-blur-sm p-5 ${
                    isHighIntensity
                      ? 'border-red-500/30 bg-gradient-to-r from-red-500/10 to-transparent hover:border-red-500/50'
                      : isMediumIntensity
                      ? 'border-amber-500/30 bg-gradient-to-r from-amber-500/10 to-transparent hover:border-amber-500/50'
                      : 'border-emerald-500/30 bg-gradient-to-r from-emerald-500/10 to-transparent hover:border-emerald-500/50'
                  }`}
                >
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div>
                      <p className="font-semibold text-slate-200 group-hover:text-slate-100">{event.country}</p>
                      <p className="text-xs text-slate-400 mt-1">{event.location}</p>
                    </div>
                    <span className={`text-xs font-bold px-3 py-1 rounded-lg whitespace-nowrap flex-shrink-0 ${
                      isHighIntensity ? 'bg-red-500/30 text-red-300' :
                      isMediumIntensity ? 'bg-amber-500/30 text-amber-300' :
                      'bg-emerald-500/30 text-emerald-300'
                    }`}>
                      {intensity.toFixed(1)}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mb-2 font-medium">{event.event_type}</p>
                  <p className="text-xs text-slate-500">{new Date(event.timestamp).toLocaleDateString()} • Code: {event.event_code}</p>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
