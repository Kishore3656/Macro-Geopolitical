'use client';

import { useEffect, useMemo, useState } from 'react';
import { api } from '@/lib/api';
import { GeoEvent } from '@/types';
import { useGTI } from '@/hooks';

export default function NexusEarthPulse() {
  const { current: gti } = useGTI();
  const [events, setEvents] = useState<GeoEvent[]>([]);

  useEffect(() => {
    const loadData = async () => {
      const eventsRes = await api.events(12);
      if (!('error' in eventsRes)) setEvents(eventsRes.events);
    };

    loadData();
  }, []);

  const regionCounts = useMemo(() => {
    return events.reduce<Record<string, number>>((acc, event) => {
      acc[event.country] = (acc[event.country] ?? 0) + 1;
      return acc;
    }, {});
  }, [events]);

  return (
    <div className="grid grid-cols-1 gap-4 xl:grid-cols-[minmax(0,1.15fr)_minmax(0,0.85fr)]">
      <section className="nexus-panel p-4">
        <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">System Logs</div>
        <div className="mt-4 space-y-3">
          {events.map((event) => (
            <div key={event.event_id} className="border border-white/10 bg-white/[0.02] px-4 py-4 text-sm">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="font-bold uppercase text-[#f4f1e8]">{event.event_type}</div>
                <div className={event.goldstein_scale <= -4 ? 'text-[#ff7557]' : event.goldstein_scale >= 4 ? 'text-[#9eff4f]' : 'text-[#f6e327]'}>
                  GS {event.goldstein_scale.toFixed(1)}
                </div>
              </div>
              <div className="mt-2 text-[#d7d7cf]">
                {event.country} | {event.location}
              </div>
              <div className="mt-2 text-xs uppercase tracking-[0.18em] text-[#8d8f86]">
                {new Date(event.timestamp).toLocaleString()}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="space-y-4">
        <div className="nexus-panel p-4">
          <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Global Risk</div>
          <div className="mt-3 text-[2.5rem] font-black tracking-[-0.08em] text-[#f4f1e8]">
            {(gti?.score ?? 0).toFixed(1)}
          </div>
          <div className="mt-2 uppercase text-[#f43de2]">{gti?.risk_level ?? 'elevated'}</div>
        </div>

        <div className="nexus-panel p-4">
          <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Regional Density</div>
          <div className="mt-4 space-y-3 text-sm">
            {Object.entries(regionCounts).map(([country, count]) => (
              <div key={country} className="border border-white/10 px-3 py-3">
                <div className="flex items-center justify-between">
                  <span className="font-bold uppercase text-[#f4f1e8]">{country}</span>
                  <span className={count >= 3 ? 'text-[#ff7557]' : count === 2 ? 'text-[#f6e327]' : 'text-[#9eff4f]'}>
                    {count}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
