'use client';

import { useGTI, useMarket, useSignals } from '@/hooks';
import CommandCenterMap from './CommandCenterMap';

const summaryBoxes = [
  {
    label: 'Tension Index',
    value: '8.5',
    tone: 'text-[#f43de2]',
    detail: 'Escalation concentrated across Eastern Europe and the Middle East.',
  },
  {
    label: 'Trade Flow',
    value: 'UNSTABLE',
    tone: 'text-[#f6e327]',
    detail: 'Maritime and energy corridors remain sensitive to conflict events.',
  },
  {
    label: 'Hazard',
    value: 'HIGH',
    tone: 'text-[#ff7557]',
    detail: 'Headline volatility and commodity shock risk remain elevated.',
  },
];

export default function NexusCommand() {
  const { current: gti } = useGTI();
  const { spy } = useMarket();
  const { current: signal } = useSignals();

  return (
    <div className="space-y-4">
      <CommandCenterMap accentTitle="The Command Hub" contextLabel="Primary geopolitical map stack" />

      <section className="grid grid-cols-1 gap-4 xl:grid-cols-[minmax(0,1.15fr)_minmax(0,0.85fr)]">
        <div className="nexus-panel p-4">
          <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Global Zone Readout</div>
          <div className="mt-4 grid grid-cols-1 gap-3 md:grid-cols-3">
            {summaryBoxes.map((box) => (
              <div key={box.label} className="border border-white/10 bg-white/[0.02] px-4 py-4">
                <div className="text-[0.72rem] uppercase tracking-[0.2em] text-[#8d8f86]">{box.label}</div>
                <div className={`mt-3 text-[1.8rem] font-black tracking-[-0.08em] ${box.tone}`}>{box.value}</div>
                <div className="mt-3 text-sm leading-6 text-[#c5c5bc]">{box.detail}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="nexus-panel grid grid-cols-1 gap-px bg-white/10 md:grid-cols-3 xl:grid-cols-1">
          <div className="bg-black px-4 py-4">
            <div className="text-[0.72rem] uppercase tracking-[0.2em] text-[#8d8f86]">GTI Score</div>
            <div className="mt-2 text-[2.25rem] font-black tracking-[-0.08em] text-[#f4f1e8]">
              {(gti?.score ?? 0).toFixed(1)}
            </div>
            <div className="mt-2 text-sm uppercase text-[#f6e327]">{gti?.risk_level ?? 'elevated'}</div>
          </div>

          <div className="bg-black px-4 py-4">
            <div className="text-[0.72rem] uppercase tracking-[0.2em] text-[#8d8f86]">Signal Bias</div>
            <div className={`mt-2 text-[2.25rem] font-black tracking-[-0.08em] ${signal?.direction === 'DOWN' ? 'text-[#ff7557]' : 'text-[#9eff4f]'}`}>
              {signal?.direction ?? 'UP'}
            </div>
            <div className="mt-2 text-sm uppercase text-[#c5c5bc]">
              Confidence {(signal?.confidence ?? 0).toFixed(2)}
            </div>
          </div>

          <div className="bg-black px-4 py-4">
            <div className="text-[0.72rem] uppercase tracking-[0.2em] text-[#8d8f86]">SPY Daily Drift</div>
            <div className={`mt-2 text-[2.25rem] font-black tracking-[-0.08em] ${(spy?.daily_change_pct ?? 0) < 0 ? 'text-[#ff7557]' : 'text-[#9eff4f]'}`}>
              {(spy?.daily_change_pct ?? 0) >= 0 ? '+' : ''}
              {(spy?.daily_change_pct ?? 0).toFixed(2)}%
            </div>
            <div className="mt-2 text-sm uppercase text-[#c5c5bc]">
              Current Price {(spy?.current_price ?? 0).toFixed(2)}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
