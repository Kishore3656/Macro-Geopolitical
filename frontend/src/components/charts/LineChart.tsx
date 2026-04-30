'use client';

interface LineChartProps {
  title: string;
  data: any[];
}

export default function LineChart({ title, data }: LineChartProps) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
      <h3 className="text-lg font-semibold text-white mb-4">{title}</h3>
      <div className="h-64 bg-slate-900 rounded-lg flex items-center justify-center border border-slate-700">
        <p className="text-slate-500">Chart placeholder - Connect to real data</p>
      </div>
    </div>
  );
}
