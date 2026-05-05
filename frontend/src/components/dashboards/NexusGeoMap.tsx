'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { BilateralData } from '@/types';
import CommandCenterMap from './CommandCenterMap';

interface GeopoliticalEvent {
  country?: string;
  location?: string;
  event_type?: string;
  intensity?: number;
  timestamp?: string;
}

export default function NexusGeoMap() {
  const [bilateral, setBilateral] = useState<BilateralData | null>(null);
  const [events, setEvents] = useState<GeopoliticalEvent[]>([]);

  useEffect(() => {
    const loadData = async () => {
      const bilateralRes = await api.bilateral(20);
      if (!('error' in bilateralRes)) setBilateral(bilateralRes);
      
      const eventsRes = await api.events(10);
      if (!('error' in eventsRes)) setEvents(Array.isArray(eventsRes) ? eventsRes : eventsRes?.data || []);
    };

    loadData();
  }, []);

  const totalRelations = bilateral?.relations?.length || 0;
  const criticalZones = bilateral?.relations?.filter((r: any) => r.stress_category === 'critical').length || 0;
  const recentEvents = events?.length || 0;

  return (
    <div className="space-y-4">
      {/* Main Heading */}
      <div className="nexus-panel p-6 border-b border-white/10">
        <h1 className="text-3xl font-bold text-[#f4f1e8] uppercase tracking-wider">Geopolitical Intelligence</h1>
        <p className="mt-2 text-sm text-[#8d8f86]">Regional tension overlays and active hotspot monitoring</p>
      </div>

      {/* Metrics Cards */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="nexus-panel p-4 border-l-2 border-[#9eff4f]">
          <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Total Relations</div>
          <div className="mt-3 text-3xl font-bold text-[#9eff4f]">{totalRelations}</div>
          <div className="mt-2 text-xs text-[#c5c5bc]">Active bilateral relationships tracked</div>
        </div>
        
        <div className="nexus-panel p-4 border-l-2 border-[#f43de2]">
          <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Critical Zones</div>
          <div className="mt-3 text-3xl font-bold text-[#f43de2]">{criticalZones}</div>
          <div className="mt-2 text-xs text-[#c5c5bc]">High-tension regions requiring monitoring</div>
        </div>
        
        <div className="nexus-panel p-4 border-l-2 border-[#f6e327]">
          <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Recent Events</div>
          <div className="mt-3 text-3xl font-bold text-[#f6e327]">{recentEvents}</div>
          <div className="mt-2 text-xs text-[#c5c5bc]">Geopolitical incidents in last 24h</div>
        </div>
      </section>

      {/* Geospatial Map */}
      <div className="nexus-panel p-4">
        <CommandCenterMap accentTitle="Geospatial Map" contextLabel="Regional tension overlays and active hotspot popups" />
      </div>

      {/* Legend and Bilateral Stress */}
      <section className="grid grid-cols-1 gap-4 xl:grid-cols-[minmax(0,1fr)_320px]">
        <div className="nexus-panel p-4">
          <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Color Zone Legend</div>
          <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
            <div className="border border-white/10 px-3 py-3 text-sm text-[#d7d7cf]">
              <div className="h-3 w-10 bg-[#f6e327]" />
              <div className="mt-2 font-bold uppercase text-[#f6e327]">Yellow</div>
              <div className="mt-1 leading-6">Trade-sensitive zone with moderate instability.</div>
            </div>
            <div className="border border-white/10 px-3 py-3 text-sm text-[#d7d7cf]">
              <div className="h-3 w-10 bg-[#9eff4f]" />
              <div className="mt-2 font-bold uppercase text-[#9eff4f]">Green</div>
              <div className="mt-1 leading-6">Lower hazard corridor and stable bilateral routing.</div>
            </div>
            <div className="border border-white/10 px-3 py-3 text-sm text-[#d7d7cf]">
              <div className="h-3 w-10 bg-[#f43de2]" />
              <div className="mt-2 font-bold uppercase text-[#ff8df4]">Magenta</div>
              <div className="mt-1 leading-6">Escalation cluster with elevated commodity shock risk.</div>
            </div>
            <div className="border border-white/10 px-3 py-3 text-sm text-[#d7d7cf]">
              <div className="nexus-hatch h-3 w-10 border border-white/20" />
              <div className="mt-2 font-bold uppercase text-[#d7d7cf]">Grey-Hatched</div>
              <div className="mt-1 leading-6">Baseline map mass and low-priority monitoring space.</div>
            </div>
          </div>
        </div>

        <div className="nexus-panel p-4">
          <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Bilateral Stress</div>
          <div className="mt-4 space-y-3 text-sm">
            {bilateral?.relations?.slice(0, 6).map((relation: any) => (
              <div key={`${relation.country1}-${relation.country2}`} className="border border-white/10 bg-white/[0.02] px-3 py-3">
                <div className="font-bold uppercase text-[#f4f1e8]">
                  {relation.country1} / {relation.country2}
                </div>
                <div className="mt-2 flex items-center justify-between uppercase text-[#c5c5bc]">
                  <span>Stress</span>
                  <span className={relation.stress_level >= 7 ? 'text-[#ff7557]' : relation.stress_level >= 4 ? 'text-[#f6e327]' : 'text-[#9eff4f]'}>
                    {relation.stress_level.toFixed(1)}
                  </span>
                </div>
                <div className="mt-2 h-2 bg-white/10">
                  <div
                    className={relation.stress_level >= 7 ? 'h-full bg-[#f43de2]' : relation.stress_level >= 4 ? 'h-full bg-[#f6e327]' : 'h-full bg-[#9eff4f]'}
                    style={{ width: `${Math.min(relation.stress_level * 10, 100)}%` }}
                  />
                </div>
                <div className="mt-2 uppercase text-[#8d8f86]">{relation.stress_category}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Bilateral Relations and Recent Events */}
      <section className="grid grid-cols-1 xl:grid-cols-2 gap-4">
        {/* Bilateral Relations (Top Tensions) */}
        <div className="nexus-panel p-4">
          <h2 className="text-sm uppercase tracking-[0.15em] font-bold text-[#f4f1e8] mb-4">Bilateral Relations (Top Tensions)</h2>
          <div className="space-y-2 max-h-96 overflow-y-auto pr-2">
            {bilateral?.relations?.slice(0, 10).map((relation: any, idx: number) => (
              <div key={idx} className={`border border-white/10 bg-white/[0.02] px-3 py-2 text-xs ${
                relation.stress_category === 'critical' ? 'border-[#f43de2]/50' : 'border-white/10'
              }`}>
                <div className="flex justify-between items-start">
                  <div className="font-bold uppercase text-[#f4f1e8]">{relation.country1} ↔ {relation.country2}</div>
                  <span className={relation.stress_level >= 7 ? 'text-[#ff7557]' : relation.stress_level >= 4 ? 'text-[#f6e327]' : 'text-[#9eff4f]'}>
                    {relation.stress_level.toFixed(1)}/10
                  </span>
                </div>
                <div className="mt-1 text-[#8d8f86]">{relation.stress_category}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Geopolitical Events */}
        <div className="nexus-panel p-4">
          <h2 className="text-sm uppercase tracking-[0.15em] font-bold text-[#f4f1e8] mb-4">Recent Geopolitical Events</h2>
          <div className="space-y-2 max-h-96 overflow-y-auto pr-2">
            {events?.slice(0, 10).map((event: GeopoliticalEvent, idx: number) => (
              <div key={idx} className="border border-white/10 bg-white/[0.02] px-3 py-2 text-xs">
                <div className="flex justify-between items-start">
                  <div>
                    <div className="font-bold uppercase text-[#f4f1e8]">{event.country || 'Unknown'}</div>
                    <div className="text-[#c5c5bc] mt-0.5">{event.location || event.event_type || 'Event'}</div>
                  </div>
                  {event.intensity && (
                    <span className={event.intensity >= 7 ? 'text-[#ff7557]' : event.intensity >= 4 ? 'text-[#f6e327]' : 'text-[#9eff4f]'}>
                      [{event.intensity.toFixed(1)}]
                    </span>
                  )}
                </div>
                {event.timestamp && <div className="mt-1 text-[#8d8f86]">{new Date(event.timestamp).toLocaleDateString()}</div>}
              </div>
            ))}
            {events?.length === 0 && <div className="text-xs text-[#8d8f86] text-center py-4">No recent events</div>}
          </div>
        </div>
      </section>
    </div>
  );
}
