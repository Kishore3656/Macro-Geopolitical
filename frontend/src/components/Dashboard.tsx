'use client';

import { useState, useEffect } from 'react';
import Sidebar from './Sidebar';
import EarthPulse from './dashboards/EarthPulse';
import GeoMap from './dashboards/GeoMap';
import Market from './dashboards/Market';
import AISignals from './dashboards/AISignals';

type TabType = 'earth-pulse' | 'geo-map' | 'market' | 'ai-signals';

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState<TabType>('earth-pulse');
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`);
        setIsConnected(response.ok);
      } catch {
        setIsConnected(false);
      }
    };

    checkConnection();
    const interval = setInterval(checkConnection, 10000);
    return () => clearInterval(interval);
  }, []);

  const renderDashboard = () => {
    switch (activeTab) {
      case 'earth-pulse':
        return <EarthPulse />;
      case 'geo-map':
        return <GeoMap />;
      case 'market':
        return <Market />;
      case 'ai-signals':
        return <AISignals />;
      default:
        return <EarthPulse />;
    }
  };

  return (
    <div className="flex h-screen bg-slate-950">
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />

      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="border-b border-slate-700 bg-slate-900 px-6 py-4 flex justify-between items-center shadow-sm">
          <div>
            <h1 className="text-xl font-bold text-white">GeoMarket Intelligence</h1>
            <p className="text-xs text-slate-500">Sovereign Intelligence Framework</p>
          </div>
          <div className="flex items-center gap-3">
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-sm text-slate-400">{isConnected ? 'Connected' : 'Disconnected'}</span>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto bg-slate-950">
          <div className="p-6 max-w-7xl mx-auto w-full">
            {renderDashboard()}
          </div>
        </div>
      </div>
    </div>
  );
}
