'use client';

import { ReactNode, useEffect, useMemo, useState } from 'react';
import { usePathname } from 'next/navigation';
import Sidebar from './Sidebar';
import { api } from '@/lib/api';
import { Headline, GeoEvent } from '@/types';
import { useGTI, useMarket, useSignals } from '@/hooks';

interface AppShellProps {
  children: ReactNode;
}

type TickerItem = {
  id: string;
  text: string;
  tone: 'yellow' | 'green' | 'magenta' | 'grey';
};

const pageTitles: Record<string, { title: string; label: string }> = {
  '/': {
    title: 'NEXUS Command - Variant 2',
    label: 'The Command Hub',
  },
  '/geo-map': {
    title: 'NEXUS Command - Variant 2',
    label: 'Geospatial Map',
  },
  '/market': {
    title: 'NEXUS Command - Variant 2',
    label: 'Trade Flow Matrix',
  },
  '/earth-pulse': {
    title: 'NEXUS Command - Variant 2',
    label: 'System Logs',
  },
  '/ai-signals': {
    title: 'NEXUS Command - Variant 2',
    label: 'Signal Analysis',
  },
};

function toneFromHeadline(headline: Headline): TickerItem['tone'] {
  if (headline.sentiment_label === 'negative') return 'magenta';
  if (headline.sentiment_label === 'positive') return 'green';
  return 'yellow';
}

function toneFromEvent(event: GeoEvent): TickerItem['tone'] {
  if (event.goldstein_scale <= -5) return 'magenta';
  if (event.goldstein_scale >= 4) return 'green';
  if (event.goldstein_scale >= 0) return 'yellow';
  return 'grey';
}

export default function AppShell({ children }: AppShellProps) {
  const pathname = usePathname();
  const { current: gti } = useGTI();
  const { spy, sectors } = useMarket();
  const { current: signal } = useSignals();
  const [headlines, setHeadlines] = useState<Headline[]>([]);
  const [events, setEvents] = useState<GeoEvent[]>([]);

  useEffect(() => {
    const loadShellData = async () => {
      const [headlineRes, eventRes] = await Promise.all([api.headlines(6), api.events(6)]);
      if (!('error' in headlineRes)) setHeadlines(headlineRes.headlines);
      if (!('error' in eventRes)) setEvents(eventRes.events);
    };

    loadShellData();
  }, []);

  const meta = pageTitles[pathname] ?? pageTitles['/'];

  const tickerItems = useMemo<TickerItem[]>(() => {
    const headlineItems = headlines.map((headline, index) => ({
      id: `headline-${index}`,
      text: headline.title.toUpperCase(),
      tone: toneFromHeadline(headline),
    }));

    const eventItems = events.map((event, index) => ({
      id: `event-${index}`,
      text: `${event.country.toUpperCase()} ${event.event_type.toUpperCase()}`,
      tone: toneFromEvent(event),
    }));

    return [...headlineItems, ...eventItems].slice(0, 12);
  }, [events, headlines]);

  const assetImpact = useMemo(() => {
    const sectorMoves = sectors?.sectors?.slice(0, 3) ?? [];
    const marketChange = spy?.daily_change_pct ?? 0;

    return [
      {
        asset: 'OIL_FUTURES',
        impact: gti && gti.score > 6 ? 'HIGH' : 'MEDIUM',
        change: `${gti && gti.score > 6 ? '+' : '-'}${((gti?.score ?? 5.4) / 2).toFixed(1)}%`,
      },
      {
        asset: 'EUR/USD',
        impact: marketChange < 0 ? 'MEDIUM' : 'LOW',
        change: `${marketChange >= 0 ? '+' : ''}${marketChange.toFixed(1)}%`,
      },
      {
        asset: 'GOLD',
        impact: signal?.volatility === 'HIGH' ? 'HIGH' : 'MEDIUM',
        change: `+${((signal?.confidence ?? 0.61) * 2.2).toFixed(1)}%`,
      },
      ...sectorMoves.map((sector) => ({
        asset: sector.name.toUpperCase().replace(/\s+/g, '_'),
        impact: Math.abs(sector.change_pct) > 1.5 ? 'MEDIUM' : 'LOW',
        change: `${sector.change_pct >= 0 ? '+' : ''}${sector.change_pct.toFixed(1)}%`,
      })),
    ].slice(0, 5);
  }, [gti, sectors, signal, spy]);

  const riskSummary = useMemo(() => {
    const score = gti?.score ?? 5.8;
    const risk = score >= 7 ? 'HIGH' : score >= 4.5 ? 'ELEVATED' : 'LOW';
    const market = Math.abs(spy?.daily_change_pct ?? 0) > 1.2 ? 'VOLATILE' : 'STABLE';
    const cyber = signal?.volatility === 'HIGH' ? 'CRITICAL' : signal?.volatility === 'MEDIUM' ? 'WATCH' : 'LOW';

    return { risk, market, cyber };
  }, [gti, signal, spy]);

  return (
    <div className="h-screen overflow-hidden bg-black text-[#f3f3eb]">
      <div className="flex h-full flex-col lg:flex-row">
        <Sidebar />

        <div className="flex min-h-0 min-w-0 flex-1 flex-col lg:flex-row">
          <div className="flex min-h-0 min-w-0 flex-1 flex-col">
            <header className="shrink-0 border-b border-white/10 bg-black px-4 py-4 sm:px-6">
              <div className="text-[2.2rem] font-black tracking-[-0.06em] text-[#f4f1e8] sm:text-[2.7rem]">
                {meta.title}
              </div>
              <div className="mt-3 flex flex-wrap items-center gap-6 border-t border-white/10 pt-3 text-[0.9rem] font-bold text-[#f4f1e8]">
                <span className="flex items-center gap-3">
                  <span className="nexus-dot" />
                  {meta.label}
                </span>
                <span className="hidden text-[#767a72] lg:inline">Global command-state overlay active</span>
              </div>
            </header>

            <main className="min-h-0 flex-1 overflow-y-auto overflow-x-hidden px-4 py-4 sm:px-6">
              {children}
            </main>
          </div>

          <aside className="flex w-full shrink-0 border-t border-white/10 bg-black lg:sticky lg:top-0 lg:h-screen lg:w-[84px] lg:flex-col lg:border-l lg:border-t-0 lg:border-white/10">
            <div className="flex items-center justify-center border-b border-white/10 px-2 py-4 text-center text-[0.9rem] font-bold text-[#f4f1e8] lg:min-h-[96px] lg:shrink-0 lg:[writing-mode:vertical-rl] lg:rotate-180">
              <span className="flex items-center gap-2 lg:flex-col">
                <span className="nexus-dot" />
                Live News Ticker
              </span>
            </div>
            <div className="flex min-h-[130px] flex-1 gap-4 overflow-x-auto px-2 py-3 lg:flex-col lg:overflow-y-auto lg:overflow-x-hidden">
              {tickerItems.map((item) => (
                <div
                  key={item.id}
                  className={`border border-white/10 px-2 py-2 text-[0.78rem] font-bold uppercase ${
                    item.tone === 'green'
                      ? 'text-[#9eff4f]'
                      : item.tone === 'magenta'
                      ? 'text-[#f43de2]'
                      : item.tone === 'yellow'
                      ? 'text-[#f6e327]'
                      : 'text-[#b5b7af]'
                  } lg:[writing-mode:vertical-rl] lg:rotate-180`}
                >
                  {item.text}
                </div>
              ))}
            </div>
          </aside>

          <aside className="w-full shrink-0 border-t border-white/10 bg-black lg:sticky lg:top-0 lg:flex lg:h-screen lg:w-[250px] lg:flex-col lg:border-l lg:border-t-0 lg:border-white/10">
            <div className="flex items-center gap-3 border-b border-white/10 px-4 py-4 text-[0.95rem] font-bold text-[#f4f1e8]">
              <span className="nexus-dot" />
              <span>Asset Impact</span>
            </div>
            <div className="space-y-3 px-4 py-4 text-sm lg:min-h-0 lg:flex-1 lg:overflow-y-auto">
              {assetImpact.map((item) => (
                <div key={item.asset} className="border border-white/10 bg-white/[0.02] px-3 py-3">
                  <div className="font-bold uppercase text-[#f4f1e8]">Asset: {item.asset}</div>
                  <div className="mt-1 uppercase text-[#d3d3ca]">
                    Impact:{' '}
                    <span
                      className={
                        item.impact === 'HIGH'
                          ? 'text-[#ff7557]'
                          : item.impact === 'MEDIUM'
                          ? 'text-[#f6e327]'
                          : 'text-[#9eff4f]'
                      }
                    >
                      [{item.impact}]
                    </span>
                  </div>
                  <div className="mt-1 uppercase text-[#d3d3ca]">
                    Change:{' '}
                    <span className={item.change.startsWith('-') ? 'text-[#ff7557]' : 'text-[#9eff4f]'}>
                      {item.change}
                    </span>
                  </div>
                </div>
              ))}
            </div>
            <div className="border-t border-white/10 px-4 py-4 text-sm uppercase text-[#b8b8ad]">
              <div>Global Risk: <span className={riskSummary.risk === 'HIGH' ? 'text-[#ff7557]' : 'text-[#f6e327]'}>{riskSummary.risk}</span></div>
              <div className="mt-1">Market Stability: <span className={riskSummary.market === 'VOLATILE' ? 'text-[#ff9f70]' : 'text-[#9eff4f]'}>{riskSummary.market}</span></div>
              <div className="mt-1">Cyber Threat: <span className={riskSummary.cyber === 'CRITICAL' ? 'text-[#ff7557]' : riskSummary.cyber === 'WATCH' ? 'text-[#f6e327]' : 'text-[#9eff4f]'}>{riskSummary.cyber}</span></div>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}
