'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Globe, TrendingUp, Zap, Map } from 'lucide-react';

const navItems = [
  { name: 'Earth Pulse', href: '/earth-pulse', icon: Globe },
  { name: 'Geo Map', href: '/geo-map', icon: Map },
  { name: 'Market', href: '/market', icon: TrendingUp },
  { name: 'AI Signals', href: '/ai-signals', icon: Zap },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-[#13151d] border-r border-slate-800 flex flex-col">
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-xl font-bold text-cyan">GeoMarket</h1>
        <p className="text-xs text-slate-400 mt-1">Intelligence Framework</p>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-cyan bg-opacity-20 text-cyan'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              <Icon size={20} />
              <span className="text-sm font-medium">{item.name}</span>
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-slate-800 text-xs text-slate-500">
        <p>API: localhost:8000</p>
        <p className="mt-1">Real-time streaming active</p>
      </div>
    </aside>
  );
}
