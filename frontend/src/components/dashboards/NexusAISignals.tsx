'use client';

import { useMemo } from 'react';
import { useSignals } from '@/hooks';
import { useSettingsStore } from '@/store/settingsStore';

export default function NexusAISignals() {
  const { current: signal, history } = useSignals();
  const settings = useSettingsStore();

  const stats = useMemo(() => {
    const total = history?.length ?? 0;
    const upCount = history?.filter((item) => item.direction === 'UP').length ?? 0;
    const highVol = history?.filter((item) => item.volatility === 'HIGH').length ?? 0;

    return { total, upCount, highVol };
  }, [history]);

  return (
    <div className="grid grid-cols-1 gap-4 xl:grid-cols-[minmax(0,1.15fr)_minmax(0,0.85fr)]">
      <section className="nexus-panel p-4">
        <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Signal Analysis</div>
        <div className="mt-4 grid gap-3 md:grid-cols-3">
          <div className="border border-white/10 bg-white/[0.02] px-4 py-4">
            <div className="text-[0.72rem] uppercase tracking-[0.2em] text-[#8d8f86]">Current Direction</div>
            <div className={`mt-3 text-[2.1rem] font-black tracking-[-0.08em] ${signal?.direction === 'DOWN' ? 'text-[#ff7557]' : 'text-[#9eff4f]'}`}>
              {signal?.direction ?? 'UP'}
            </div>
          </div>
          <div className="border border-white/10 bg-white/[0.02] px-4 py-4">
            <div className="text-[0.72rem] uppercase tracking-[0.2em] text-[#8d8f86]">Confidence</div>
            <div className="mt-3 text-[2.1rem] font-black tracking-[-0.08em] text-[#f6e327]">
              {((signal?.confidence ?? 0) * 100).toFixed(0)}%
            </div>
          </div>
          <div className="border border-white/10 bg-white/[0.02] px-4 py-4">
            <div className="text-[0.72rem] uppercase tracking-[0.2em] text-[#8d8f86]">Volatility</div>
            <div className={`mt-3 text-[2.1rem] font-black tracking-[-0.08em] ${signal?.volatility === 'HIGH' ? 'text-[#f43de2]' : signal?.volatility === 'MEDIUM' ? 'text-[#f6e327]' : 'text-[#9eff4f]'}`}>
              {signal?.volatility ?? 'LOW'}
            </div>
          </div>
        </div>

        <div className="mt-4 space-y-3">
          {(history ?? []).slice(0, 14).map((item) => (
            <div key={item.timestamp} className="border border-white/10 bg-black px-4 py-3 text-sm">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className={`font-bold uppercase ${item.direction === 'DOWN' ? 'text-[#ff7557]' : 'text-[#9eff4f]'}`}>
                  {item.direction}
                </div>
                <div className="text-[#c5c5bc]">
                  {(item.direction_prob * 100).toFixed(0)}% direction confidence
                </div>
              </div>
              <div className="mt-2 text-xs uppercase tracking-[0.18em] text-[#8d8f86]">
                {new Date(item.timestamp).toLocaleString()} | volatility {item.volatility}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="space-y-4">
        <div className="nexus-panel p-4">
          <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Model Readout</div>
          <div className="mt-4 space-y-3 text-sm">
            <div className="border border-white/10 px-3 py-3">Signals processed: <span className="text-[#f4f1e8]">{stats.total}</span></div>
            <div className="border border-white/10 px-3 py-3">UP bias count: <span className="text-[#9eff4f]">{stats.upCount}</span></div>
            <div className="border border-white/10 px-3 py-3">High vol flags: <span className="text-[#f43de2]">{stats.highVol}</span></div>
          </div>
        </div>

        <div className="nexus-panel p-4">
          <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Model Status</div>
          <div className="mt-4 space-y-3 text-sm">
            <div className="border border-white/10 px-3 py-3">Version: <span className="text-[#f4f1e8]">{signal?.model_version ?? 'N/A'}</span></div>
            <div className="border border-white/10 px-3 py-3">LLM: <span className={settings.llm_enabled ? 'text-[#9eff4f]' : 'text-[#8d8f86]'}>{settings.llm_enabled ? `${settings.llm_provider} (ON)` : 'Disabled'}</span></div>
            <div className="border border-white/10 px-3 py-3">Timestamp: <span className="text-[#8d8f86] text-xs">{signal?.timestamp ? new Date(signal.timestamp).toLocaleString() : 'N/A'}</span></div>
          </div>
        </div>

        <div className="nexus-panel p-4">
          <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Regime Indicator</div>
          <div className="mt-4">
            {signal?.regime ? (
              <div className={`inline-block rounded px-4 py-2 font-bold uppercase text-sm tracking-[0.15em] ${
                signal.regime === 'risk-on' ? 'bg-[#9eff4f]/20 text-[#9eff4f] border border-[#9eff4f]' :
                signal.regime === 'risk-off' ? 'bg-[#ff7557]/20 text-[#ff7557] border border-[#ff7557]' :
                signal.regime === 'crisis' ? 'bg-black text-white border border-white/30' :
                'bg-[#8d8f86]/20 text-[#8d8f86] border border-[#8d8f86]'
              }`}>
                {signal.regime}
              </div>
            ) : (
              <div className="text-[#8d8f86] text-sm">Awaiting analysis...</div>
            )}
          </div>
        </div>

        <div className="nexus-panel p-4">
          <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Signal Narrative</div>
          <div className="mt-4 text-sm text-[#d7d7cf] border border-white/10 px-3 py-3 rounded">
            {signal?.narrative ? (
              <p>{signal.narrative}</p>
            ) : (
              <p className="text-[#8d8f86]">Generating market narrative...</p>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
