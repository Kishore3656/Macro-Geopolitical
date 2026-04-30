'use client';

export default function Market() {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">Market</h2>
        <p className="text-sm text-slate-400 mt-1">S&P 500 analysis, sector rankings & technical indicators</p>
      </div>

      <div className="bg-slate-800/30 rounded-lg border border-slate-700/50 p-8">
        <div className="h-96 bg-slate-900/50 rounded-lg flex items-center justify-center border border-slate-700/50">
          <div className="text-center">
            <p className="text-slate-400">Market analysis and sector performance</p>
            <p className="text-xs text-slate-500 mt-2">Real-time price charts and technical analysis</p>
          </div>
        </div>
      </div>
    </div>
  );
}
