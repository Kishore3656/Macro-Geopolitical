'use client';

import { Globe, Map, TrendingUp, Zap, Menu } from 'lucide-react';
import { useState } from 'react';

type TabType = 'earth-pulse' | 'geo-map' | 'market' | 'ai-signals';

interface SidebarProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
}

export default function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  const [isOpen, setIsOpen] = useState(true);

  const tabs = [
    { id: 'earth-pulse' as const, label: 'Earth Pulse', icon: Globe },
    { id: 'geo-map' as const, label: 'Geo Map', icon: Map },
    { id: 'market' as const, label: 'Market', icon: TrendingUp },
    { id: 'ai-signals' as const, label: 'AI Signals', icon: Zap },
  ];

  return (
    <>
      {/* Mobile Toggle */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-slate-900 rounded-lg border border-slate-800"
      >
        <Menu size={24} />
      </button>

      {/* Sidebar */}
      <div
        className={`fixed lg:relative top-0 left-0 h-screen w-64 bg-slate-900 border-r border-slate-800 p-4 z-40 transition-transform ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0`}
      >
        <div className="mb-8 pt-12 lg:pt-0">
          <h2 className="text-lg font-bold text-white">Sovereign</h2>
          <p className="text-xs text-slate-400">Intelligence Framework</p>
        </div>

        <nav className="space-y-2">
          {tabs.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => {
                onTabChange(id);
                setIsOpen(false);
              }}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                activeTab === id
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                  : 'text-slate-300 hover:bg-slate-800'
              }`}
            >
              <Icon size={20} />
              <span className="font-medium">{label}</span>
            </button>
          ))}
        </nav>

        {/* Footer */}
        <div className="absolute bottom-4 left-4 right-4 pt-4 border-t border-slate-800">
          <p className="text-xs text-slate-500">v1.0.0</p>
        </div>
      </div>

      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 lg:hidden z-30"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
}
