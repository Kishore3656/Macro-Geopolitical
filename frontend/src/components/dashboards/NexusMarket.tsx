'use client';

import { useMarket } from '@/hooks';

export default function NexusMarket() {
  const { spy, sectors } = useMarket();
  const lastVolume = spy?.bars?.[spy.bars.length - 1]?.volume ?? 0;

  return (
    <div className="grid grid-cols-1 gap-4 xl:grid-cols-[minmax(0,1.2fr)_minmax(0,0.8fr)]">
      <section className="nexus-panel p-4">
        <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Trade Flow Matrix</div>
        <div className="mt-4 grid gap-3 md:grid-cols-3">
          <div className="border border-white/10 bg-white/[0.02] px-4 py-4">
            <div className="text-[0.72rem] uppercase tracking-[0.2em] text-[#8d8f86]">SPY</div>
            <div className="mt-3 text-[2rem] font-black tracking-[-0.08em] text-[#f4f1e8]">
              {(spy?.current_price ?? 0).toFixed(2)}
            </div>
            <div className={`mt-2 text-sm uppercase ${(spy?.daily_change_pct ?? 0) < 0 ? 'text-[#ff7557]' : 'text-[#9eff4f]'}`}>
              {(spy?.daily_change_pct ?? 0) >= 0 ? '+' : ''}
              {(spy?.daily_change_pct ?? 0).toFixed(2)}%
            </div>
          </div>
          <div className="border border-white/10 bg-white/[0.02] px-4 py-4">
            <div className="text-[0.72rem] uppercase tracking-[0.2em] text-[#8d8f86]">Volume</div>
            <div className="mt-3 text-[2rem] font-black tracking-[-0.08em] text-[#f6e327]">
              {(lastVolume / 1_000_000).toFixed(1)}M
            </div>
            <div className="mt-2 text-sm uppercase text-[#c5c5bc]">Last bar participation</div>
          </div>
          <div className="border border-white/10 bg-white/[0.02] px-4 py-4">
            <div className="text-[0.72rem] uppercase tracking-[0.2em] text-[#8d8f86]">Trade Bias</div>
            <div className="mt-3 text-[2rem] font-black tracking-[-0.08em] text-[#ff8df4]">
              {(sectors?.sectors?.filter((sector) => sector.change_pct > 0).length ?? 0)}/
              {sectors?.sectors?.length ?? 0}
            </div>
            <div className="mt-2 text-sm uppercase text-[#c5c5bc]">Advancing sectors</div>
          </div>
        </div>

        <div className="mt-4 grid gap-px bg-white/10 md:grid-cols-2">
          {(sectors?.sectors ?? []).map((sector) => (
            <div key={sector.name} className="bg-black px-4 py-4">
              <div className="flex items-center justify-between">
                <div className="font-bold uppercase text-[#f4f1e8]">{sector.name}</div>
                <div className={sector.change_pct >= 0 ? 'text-[#9eff4f]' : 'text-[#ff7557]'}>
                  {sector.change_pct >= 0 ? '+' : ''}
                  {sector.change_pct.toFixed(2)}%
                </div>
              </div>
              <div className="mt-3 h-2 bg-white/10">
                <div
                  className={sector.change_pct >= 0 ? 'h-full bg-[#9eff4f]' : 'h-full bg-[#f43de2]'}
                  style={{ width: `${Math.min(Math.abs(sector.change_pct) * 16, 100)}%` }}
                />
              </div>
              <div className="mt-2 text-xs uppercase tracking-[0.16em] text-[#8d8f86]">
                Performance {sector.performance.toFixed(2)}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="nexus-panel p-4">
        <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Market Notes</div>
        <div className="mt-4 space-y-3 text-sm">
          <div className="border border-[#f6e327]/40 px-3 py-3 text-[#d7d7cf]">
            Yellow corridors reflect rate-sensitive and import-dependent assets.
          </div>
          <div className="border border-[#9eff4f]/40 px-3 py-3 text-[#d7d7cf]">
            Green sectors are absorbing geopolitical noise with improving breadth.
          </div>
          <div className="border border-[#f43de2]/40 px-3 py-3 text-[#d7d7cf]">
            Magenta sectors remain exposed to conflict headlines and energy repricing.
          </div>
        </div>
      </section>
    </div>
  );
}
