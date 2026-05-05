'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { BilateralData } from '@/types';
import CommandCenterMap from './CommandCenterMap';

export default function NexusGeoMap() {
  const [bilateral, setBilateral] = useState<BilateralData | null>(null);

  useEffect(() => {
    const loadData = async () => {
      const bilateralRes = await api.bilateral(8);
      if (!('error' in bilateralRes)) setBilateral(bilateralRes);
    };

    loadData();
  }, []);

  return (
    <div className="space-y-4">
      <CommandCenterMap accentTitle="Geospatial Map" contextLabel="Regional tension overlays and active hotspot popups" />

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
            {bilateral?.relations?.slice(0, 6).map((relation) => (
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
    </div>
  );
}
