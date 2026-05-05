'use client';

import { ReactNode } from 'react';

interface NexusThemeProviderProps {
  children: ReactNode;
}

export function NexusThemeProvider({ children }: NexusThemeProviderProps) {
  return (
    <div className="min-h-screen bg-black text-white overflow-x-hidden" style={{ fontFamily: 'Courier New, monospace' }}>
      <style>{`
        :root {
          --color-bg-primary: #000000;
          --color-bg-secondary: rgba(0, 0, 0, 0.8);
          --color-border-primary: rgba(74, 222, 128, 0.3);
          --color-border-accent: rgba(34, 211, 238, 0.3);
          --color-text-primary: #ffffff;
          --color-text-secondary: #9ca3af;
          --color-accent-green: #4ade80;
          --color-accent-cyan: #22d3ee;
          --color-accent-magenta: #ff00ff;
          --color-accent-yellow: #ffff00;
          --color-status-high: #ff0000;
          --color-status-medium: #fbbf24;
          --color-status-low: #10b981;
        }

        .nexus-panel {
          border: 1px solid var(--color-border-primary);
          background-color: var(--color-bg-secondary);
          padding: 1rem;
        }

        .nexus-panel-accent {
          border: 1px solid var(--color-border-accent);
          background-color: var(--color-bg-secondary);
        }

        .nexus-text-accent {
          color: var(--color-accent-green);
          font-weight: bold;
        }

        .nexus-text-warning {
          color: var(--color-accent-yellow);
        }

        .nexus-text-critical {
          color: var(--color-status-high);
        }

        .nexus-status-bar {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.5rem 1rem;
          background-color: rgba(0, 0, 0, 0.6);
          border-bottom: 1px solid var(--color-border-primary);
          font-size: 0.75rem;
        }

        .nexus-header {
          text-align: center;
          padding: 1.5rem;
          border-bottom: 1px solid var(--color-border-primary);
          margin-bottom: 1rem;
        }

        .nexus-header h1 {
          font-size: 1.5rem;
          font-weight: bold;
          color: var(--color-accent-green);
          margin-bottom: 0.5rem;
        }

        .nexus-grid-4 {
          display: grid;
          grid-template-columns: 1fr 2fr 1fr;
          gap: 1rem;
          height: 100vh;
        }

        .nexus-scroll {
          overflow-y: auto;
          max-height: 100%;
        }

        @media (max-width: 1024px) {
          .nexus-grid-4 {
            grid-template-columns: 1fr;
            height: auto;
          }
        }
      `}</style>
      {children}
    </div>
  );
}

interface NexusPanelProps {
  children: ReactNode;
  title?: string;
  accent?: boolean;
  className?: string;
}

export function NexusPanel({ children, title, accent = false, className = '' }: NexusPanelProps) {
  return (
    <div className={`nexus-panel ${accent ? 'nexus-panel-accent' : ''} ${className}`}>
      {title && <div className="nexus-text-accent text-xs mb-3">{title}</div>}
      {children}
    </div>
  );
}

interface NexusBadgeProps {
  status: 'high' | 'medium' | 'low' | 'neutral';
  children: ReactNode;
}

export function NexusBadge({ status, children }: NexusBadgeProps) {
  const colors = {
    high: 'bg-red-500/20 text-red-400 border border-red-500/50',
    medium: 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/50',
    low: 'bg-green-500/20 text-green-400 border border-green-500/50',
    neutral: 'bg-gray-500/20 text-gray-400 border border-gray-500/50',
  };

  return (
    <span className={`px-2 py-1 rounded text-xs font-bold ${colors[status]}`}>
      {children}
    </span>
  );
}
