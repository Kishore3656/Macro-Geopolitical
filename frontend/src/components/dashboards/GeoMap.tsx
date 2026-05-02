'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { BilateralData, GeoEventData } from '@/types';
import BilateralCard from '@/components/ui/BilateralCard';

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

  return (
    <div className="p-8 space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">Geopolitical Intelligence</h2>
        <p className="text-sm text-slate-400 mt-1">Country-level heatmaps, bilateral tensions & geopolitical events</p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-[#13151d] border border-slate-800 rounded-lg p-4">
          <p className="text-sm text-slate-400">Total Relations</p>
          <p className="text-2xl font-bold text-cyan">{bilateral?.relations.length || 0}</p>
        </div>
        <div className="bg-[#13151d] border border-slate-800 rounded-lg p-4">
          <p className="text-sm text-slate-400">Critical Zones</p>
          <p className="text-2xl font-bold text-danger">
            {bilateral?.relations.filter(r => r.stress_category === 'critical').length || 0}
          </p>
        </div>
        <div className="bg-[#13151d] border border-slate-800 rounded-lg p-4">
          <p className="text-sm text-slate-400">Recent Events</p>
          <p className="text-2xl font-bold text-amber">{events?.events.length || 0}</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-semibold text-slate-200 mb-4">Bilateral Relations (Top Tensions)</h3>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {bilateral?.relations.slice(0, 10).map((relation, i) => (
              <BilateralCard key={i} relation={relation} />
            ))}
          </div>
        </div>

        <div>
          <h3 className="text-lg font-semibold text-slate-200 mb-4">Recent Geopolitical Events</h3>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {events?.events.slice(0, 10).map((event, i) => (
              <div key={i} className="bg-[#13151d] border border-slate-800 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <p className="font-semibold text-slate-200 text-sm">{event.country}</p>
                  <span className={`text-xs px-2 py-1 rounded ${
                    event.intensity > 7 ? 'bg-danger bg-opacity-20 text-danger' :
                    event.intensity > 4 ? 'bg-amber bg-opacity-20 text-amber' :
                    'bg-success bg-opacity-20 text-success'
                  }`}>
                    Intensity: {event.intensity}
                  </span>
                </div>
                <p className="text-xs text-slate-400 mb-2">{event.event_type}</p>
                <p className="text-xs text-slate-500">{new Date(event.timestamp).toLocaleDateString()}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
