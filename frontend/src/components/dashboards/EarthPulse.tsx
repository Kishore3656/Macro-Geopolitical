'use client';

import { useEffect, useState } from 'react';
import MetricCard from '../MetricCard';
import LineChart from '../charts/LineChart';

interface EarthPulseData {
  gtiIndex: number;
  marketSentiment: number;
  volatility: number;
  capitalFlow: number;
  timestamp: string;
}

export default function EarthPulse() {
  const [data, setData] = useState<EarthPulseData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [gtiRes, marketRes] = await Promise.all([
          fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/gti`),
          fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/market/spy`)
        ]);
        const gtiData = await gtiRes.json();
        const marketData = await marketRes.json();

        setData({
          gtiIndex: gtiData.gti_score || 0,
          marketSentiment: gtiData.vader_sentiment || 0,
          volatility: marketData.volatility || 0,
          capitalFlow: marketData.volume || 0,
          timestamp: new Date().toISOString()
        });
      } catch (error) {
        console.error('Error fetching Earth Pulse data:', error);
        setData({
          gtiIndex: 0,
          marketSentiment: 0,
          volatility: 0,
          capitalFlow: 0,
          timestamp: new Date().toISOString()
        });
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="text-slate-400">Loading Earth Pulse...</div>;
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">Earth Pulse</h2>
        <p className="text-sm text-slate-400 mt-1">Global markets, capital flows & geopolitical indicators</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          label="Geopolitical Tension Index"
          value={data?.gtiIndex.toFixed(3) || '0.000'}
          unit="(0.0 - 1.0)"
          trend="neutral"
        />
        <MetricCard
          label="Market Sentiment"
          value={data?.marketSentiment.toFixed(2) || '0.00'}
          unit="%"
          trend={data && data.marketSentiment > 0 ? 'up' : 'down'}
        />
        <MetricCard
          label="Volatility"
          value={data?.volatility.toFixed(2) || '0.00'}
          unit="VIX"
          trend="neutral"
        />
        <MetricCard
          label="Capital Flow"
          value={data?.capitalFlow.toFixed(2) || '0.00'}
          unit="Billions"
          trend={data && data.capitalFlow > 0 ? 'up' : 'down'}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <LineChart title="GTI Trend (24h)" data={[]} />
        <LineChart title="Capital Flows (24h)" data={[]} />
      </div>
    </div>
  );
}
