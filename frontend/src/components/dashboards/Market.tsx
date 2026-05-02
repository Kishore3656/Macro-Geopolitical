'use client';

import { useMarket } from '@/hooks';
import { useEffect, useState } from 'react';
import { SectorData } from '@/types';
import CandlestickChart from '@/components/charts/CandlestickChart';
import SectorCard from '@/components/ui/SectorCard';
import StatusBadge from '@/components/ui/StatusBadge';

export default function Market() {
  const { spy, sectors, loading } = useMarket();
  const [dailyChange, setDailyChange] = useState<number | null>(null);

  useEffect(() => {
    if (spy?.current_price && spy.bars.length > 0) {
      const firstBar = spy.bars[0];
      const change = ((spy.current_price - firstBar.open) / firstBar.open) * 100;
      setDailyChange(change);
    }
  }, [spy]);

  return (
    <div className="p-8 space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">Market Intelligence</h2>
        <p className="text-sm text-slate-400 mt-1">S&P 500 analysis, sector rankings & technical indicators</p>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <StatusBadge
          label="SPY Price"
          status={dailyChange && dailyChange > 1 ? 'success' : dailyChange && dailyChange < -1 ? 'danger' : 'neutral'}
          value={spy?.current_price ? `$${spy.current_price.toFixed(2)}` : '-'}
        />
        <StatusBadge
          label="Daily Change"
          status={dailyChange && dailyChange > 0 ? 'success' : 'danger'}
          value={dailyChange ? `${dailyChange.toFixed(2)}%` : '-'}
        />
        <StatusBadge
          label="Volume"
          status="neutral"
          value={spy?.bars[0]?.volume ? `${(spy.bars[0].volume / 1000000).toFixed(1)}M` : '-'}
        />
        <StatusBadge
          label="52W High"
          status="neutral"
          value={spy?.bars.length ? `$${Math.max(...spy.bars.map(b => b.high)).toFixed(2)}` : '-'}
        />
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2">
          <CandlestickChart
            data={spy?.bars || []}
            title="SPY 5-Day Candlestick (1H)"
            height={400}
          />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-slate-200 mb-4">Market State</h3>
          <div className="space-y-2 text-sm text-slate-300">
            <div className="bg-[#13151d] border border-slate-800 rounded-lg p-3">
              <p className="text-slate-400">Trend</p>
              <p className="font-semibold text-cyan">{dailyChange && dailyChange > 0 ? 'BULLISH ↑' : 'BEARISH ↓'}</p>
            </div>
            <div className="bg-[#13151d] border border-slate-800 rounded-lg p-3">
              <p className="text-slate-400">Volatility</p>
              <p className="font-semibold text-amber">{spy?.bars.length ? 'ELEVATED' : '-'}</p>
            </div>
            <div className="bg-[#13151d] border border-slate-800 rounded-lg p-3">
              <p className="text-slate-400">RSI Signal</p>
              <p className="font-semibold text-success">MOMENTUM</p>
            </div>
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-slate-200 mb-4">Sector Performance</h3>
        <div className="grid grid-cols-4 gap-4">
          {sectors?.sectors.slice(0, 8).map((sector, i) => (
            <SectorCard key={i} sector={sector} />
          ))}
        </div>
      </div>
    </div>
  );
}
