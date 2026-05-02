'use client';

import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface CandleData {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

interface CandlestickChartProps {
  data: CandleData[];
  title?: string;
  height?: number;
}

export default function CandlestickChart({
  data,
  title,
  height = 400,
}: CandlestickChartProps) {
  const processedData = data.map((d) => ({
    timestamp: d.timestamp,
    open: d.open,
    close: d.close,
    high: d.high,
    low: d.low,
    volume: d.volume,
    range: [d.low, d.high],
  }));

  return (
    <div className="bg-[#13151d] border border-slate-800 rounded-lg p-6">
      {title && <h3 className="text-sm font-medium text-slate-400 mb-4">{title}</h3>}
      <ResponsiveContainer width="100%" height={height}>
        <ComposedChart data={processedData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="timestamp" stroke="#94a3b8" style={{ fontSize: '12px' }} />
          <YAxis stroke="#94a3b8" style={{ fontSize: '12px' }} yAxisId="left" />
          <YAxis stroke="#94a3b8" style={{ fontSize: '12px' }} yAxisId="right" orientation="right" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#0a0b0f',
              border: '1px solid #334155',
              borderRadius: '8px',
            }}
            cursor={{ stroke: '#475569' }}
          />
          <Bar
            yAxisId="right"
            dataKey="volume"
            fill="#6ecf8a"
            fillOpacity={0.2}
            isAnimationActive={false}
          />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="close"
            stroke="#00ffff"
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
          />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="high"
            stroke="#ffb867"
            strokeWidth={1}
            strokeDasharray="5 5"
            dot={false}
            isAnimationActive={false}
          />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="low"
            stroke="#ff2d2d"
            strokeWidth={1}
            strokeDasharray="5 5"
            dot={false}
            isAnimationActive={false}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
