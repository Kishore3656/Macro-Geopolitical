'use client';

import {
  BarChart as RechartBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface BarDensityChartProps {
  data: any[];
  dataKey: string;
  fill?: string;
  title?: string;
  height?: number;
}

export default function BarDensityChart({
  data,
  dataKey,
  fill = '#ffb867',
  title,
  height = 300,
}: BarDensityChartProps) {
  return (
    <div className="bg-[#13151d] border border-slate-800 rounded-lg p-6">
      {title && <h3 className="text-sm font-medium text-slate-400 mb-4">{title}</h3>}
      <ResponsiveContainer width="100%" height={height}>
        <RechartBarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="timestamp" stroke="#94a3b8" style={{ fontSize: '12px' }} />
          <YAxis stroke="#94a3b8" style={{ fontSize: '12px' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#0a0b0f',
              border: '1px solid #334155',
              borderRadius: '8px',
            }}
            cursor={{ fill: '#334155', fillOpacity: 0.2 }}
          />
          <Bar dataKey={dataKey} fill={fill} isAnimationActive={false} />
        </RechartBarChart>
      </ResponsiveContainer>
    </div>
  );
}
