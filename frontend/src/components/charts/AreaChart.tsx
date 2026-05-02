'use client';

import {
  AreaChart as RechartAreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface AreaChartProps {
  data: any[];
  dataKey: string;
  fill?: string;
  stroke?: string;
  title?: string;
  height?: number;
}

export default function AreaChart({
  data,
  dataKey,
  fill = '#6ecf8a',
  stroke = '#6ecf8a',
  title,
  height = 300,
}: AreaChartProps) {
  return (
    <div className="bg-[#13151d] border border-slate-800 rounded-lg p-6">
      {title && <h3 className="text-sm font-medium text-slate-400 mb-4">{title}</h3>}
      <ResponsiveContainer width="100%" height={height}>
        <RechartAreaChart data={data}>
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
          <Area
            type="monotone"
            dataKey={dataKey}
            fill={fill}
            fillOpacity={0.3}
            stroke={stroke}
            strokeWidth={2}
            isAnimationActive={false}
          />
        </RechartAreaChart>
      </ResponsiveContainer>
    </div>
  );
}
