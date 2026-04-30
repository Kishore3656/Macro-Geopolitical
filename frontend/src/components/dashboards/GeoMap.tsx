'use client';

export default function GeoMap() {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">Geo Map</h2>
        <p className="text-sm text-slate-400 mt-1">Country-level heatmaps, currency flows & commodity tracking</p>
      </div>

      <div className="bg-slate-800/30 rounded-lg border border-slate-700/50 p-8">
        <div className="h-96 bg-slate-900/50 rounded-lg flex items-center justify-center border border-slate-700/50">
          <div className="text-center">
            <p className="text-slate-400">Geopolitical heatmap visualization</p>
            <p className="text-xs text-slate-500 mt-2">Interactive world map with real-time geopolitical data</p>
          </div>
        </div>
      </div>
    </div>
  );
}
