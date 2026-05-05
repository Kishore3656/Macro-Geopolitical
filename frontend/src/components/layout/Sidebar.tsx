'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BarChart3, Square, Triangle, ChevronDown } from 'lucide-react';

const navItems = [
  { name: 'GEO-POLITICAL MARKET', href: '/', icon: Square },
  { name: 'Geospatial Map', href: '/geo-map', icon: Triangle },
  { name: 'Signal Analysis', href: '/ai-signals', icon: Square },
  { name: 'Analytics', href: '/market', icon: BarChart3 },
  { name: 'System Logs', href: '/earth-pulse', icon: ChevronDown },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex w-full flex-col border-b border-white/10 bg-black lg:sticky lg:top-0 lg:h-screen lg:w-[240px] lg:border-b-0 lg:border-r lg:border-white/10">
      <div className="border-b border-white/10 px-6 py-5">
        <div className="text-[1.6rem] font-black uppercase leading-none tracking-[-0.08em] text-[#f4f1e8]">
          GEOPOLITICAL
        </div>
        <div className="mt-1 text-[1.6rem] font-black uppercase leading-none tracking-[-0.08em] text-[#f4f1e8]">
          MARKET
        </div>
        <div className="mt-1 text-xs uppercase tracking-[0.18em] text-[#72766c]">
          WS_PORT:8000
        </div>
      </div>

      <nav className="flex-1 space-y-1 px-4 py-6">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 border border-transparent px-3 py-3 text-sm font-semibold transition-colors ${
                isActive
                  ? 'bg-white/[0.03] text-[#f4f1e8]'
                  : 'text-[#b8b8ad] hover:bg-white/[0.02] hover:text-[#f4f1e8]'
              }`}
            >
              <Icon size={14} strokeWidth={2.2} className={isActive ? 'text-[#f4f1e8]' : 'text-[#f4f1e8]'} />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
