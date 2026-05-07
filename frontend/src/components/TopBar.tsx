'use client';

import { useState } from 'react';
import { useSettingsStore } from '@/store/settingsStore';

export default function TopBar() {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const settings = useSettingsStore();

  const handleToggleLLM = async () => {
    settings.toggleLLM();
    try {
      await fetch('/api/settings/llm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          llm_enabled: !settings.llm_enabled,
          llm_provider: settings.llm_provider,
        }),
      });
    } catch (error) {
      console.error('Failed to update LLM settings:', error);
    }
  };

  const handleSetProvider = async (provider: 'ollama' | 'huggingface') => {
    settings.setProvider(provider);
    try {
      await fetch('/api/settings/llm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          llm_enabled: settings.llm_enabled,
          llm_provider: provider,
        }),
      });
    } catch (error) {
      console.error('Failed to update LLM provider:', error);
    }
  };

  return (
    <>
      <div className="flex items-center justify-between border-b border-white/10 bg-black/50 px-6 py-4">
        <div className="text-sm uppercase tracking-[0.2em] text-[#8d8f86]">Trading Bot Dashboard</div>
        <button
          onClick={() => setDrawerOpen(!drawerOpen)}
          className="flex h-10 w-10 items-center justify-center rounded border border-white/10 text-[#8d8f86] hover:text-white/70 transition"
          title="Settings"
        >
          ⚙
        </button>
      </div>

      {drawerOpen && (
        <div className="fixed inset-0 z-50 flex">
          <div
            className="flex-1 bg-black/40"
            onClick={() => setDrawerOpen(false)}
          />
          <div className="w-80 border-l border-white/10 bg-black p-6 space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-sm uppercase tracking-[0.2em] text-[#8d8f86]">Settings</h2>
              <button
                onClick={() => setDrawerOpen(false)}
                className="text-[#8d8f86] hover:text-white/70 transition"
              >
                ×
              </button>
            </div>

            <div className="space-y-3">
              <label className="block text-xs uppercase tracking-[0.15em] text-[#8d8f86]">
                LLM Sentiment Analysis
              </label>
              <button
                onClick={handleToggleLLM}
                className={`w-full rounded px-4 py-2 font-bold uppercase text-sm tracking-[0.15em] transition ${
                  settings.llm_enabled
                    ? 'bg-[#9eff4f]/20 text-[#9eff4f] border border-[#9eff4f]'
                    : 'bg-white/10 text-[#8d8f86] border border-white/10'
                }`}
              >
                {settings.llm_enabled ? 'Enabled' : 'Disabled'}
              </button>
            </div>

            {settings.llm_enabled && (
              <div className="space-y-3">
                <label className="block text-xs uppercase tracking-[0.15em] text-[#8d8f86]">
                  LLM Provider
                </label>
                <div className="space-y-2">
                  {(['ollama', 'huggingface'] as const).map((provider) => (
                    <button
                      key={provider}
                      onClick={() => handleSetProvider(provider)}
                      className={`w-full rounded px-4 py-2 text-sm uppercase tracking-[0.15em] transition ${
                        settings.llm_provider === provider
                          ? 'bg-[#9eff4f]/20 text-[#9eff4f] border border-[#9eff4f]'
                          : 'bg-white/10 text-[#8d8f86] border border-white/10'
                      }`}
                    >
                      {provider}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="pt-4 border-t border-white/10 text-xs text-[#8d8f86]">
              <p>Last updated: {new Date(settings.last_updated).toLocaleString()}</p>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
