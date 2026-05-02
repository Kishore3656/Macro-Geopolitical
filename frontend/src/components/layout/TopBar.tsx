'use client';

import { useState, useEffect } from 'react';
import { CheckCircle2, AlertCircle } from 'lucide-react';

export default function TopBar() {
  const [apiHealth, setApiHealth] = useState<'connected' | 'disconnected'>('disconnected');
  const [timestamp, setTimestamp] = useState<string>('');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch('http://localhost:8000/health', { timeout: 5000 });
        setApiHealth(response.ok ? 'connected' : 'disconnected');
      } catch {
        setApiHealth('disconnected');
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimestamp(now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="bg-[#13151d] border-b border-slate-800 px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          {apiHealth === 'connected' ? (
            <>
              <CheckCircle2 size={18} className="text-success" />
              <span className="text-sm text-success">API Connected</span>
            </>
          ) : (
            <>
              <AlertCircle size={18} className="text-danger" />
              <span className="text-sm text-danger">API Disconnected</span>
            </>
          )}
        </div>
      </div>

      <div className="text-sm text-slate-400">
        {timestamp}
      </div>
    </header>
  );
}
