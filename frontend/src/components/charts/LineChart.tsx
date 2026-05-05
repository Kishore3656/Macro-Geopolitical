'use client';

import {
  LineChart as RechartLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface LineChartProps {
  data: Array<Record<string, string | number>>;
  dataKey: string;
  stroke?: string;
  title?: string;
  height?: number;
}

export default function LineChart({
  data,
  dataKey,
  stroke = '#00ffff',
  title,
  height = 300,
}: LineChartProps) {
  return (
    <div className="bg-[#13151d] border border-slate-800 rounded-lg p-6">
      {title && <h3 className="text-sm font-medium text-slate-400 mb-4">{title}</h3>}
      <ResponsiveContainer width="100%" height={height}>
        <RechartLineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="timestamp" stroke="#94a3b8" style={{ fontSize: '12px' }} />
          <YAxis stroke="#94a3b8" style={{ fontSize: '12px' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#0a0b0f',
              border: '1px solid #334155',
              borderRadius: '8px',
            }}
            cursor={{ stroke: '#475569' }}
          />
          <Line
            type="monotone"
            dataKey={dataKey}
            stroke={stroke}
            dot={false}
            strokeWidth={2}
            isAnimationActive={false}
          />
        </RechartLineChart>
      </ResponsiveContainer>
    </div>
  );
}
