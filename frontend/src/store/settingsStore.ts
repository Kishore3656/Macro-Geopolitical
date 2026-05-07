import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface SettingsState {
  llm_enabled: boolean;
  llm_provider: 'ollama' | 'huggingface';
  last_updated: string;
  toggleLLM: () => void;
  setProvider: (provider: 'ollama' | 'huggingface') => void;
  initSettings: (enabled: boolean, provider: string) => void;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      llm_enabled: false,
      llm_provider: 'ollama',
      last_updated: new Date().toISOString(),

      toggleLLM: () =>
        set((state) => ({
          llm_enabled: !state.llm_enabled,
          last_updated: new Date().toISOString(),
        })),

      setProvider: (provider: 'ollama' | 'huggingface') =>
        set({
          llm_provider: provider,
          last_updated: new Date().toISOString(),
        }),

      initSettings: (enabled: boolean, provider: string) =>
        set({
          llm_enabled: enabled,
          llm_provider: provider as 'ollama' | 'huggingface',
          last_updated: new Date().toISOString(),
        }),
    }),
    {
      name: 'settings-store',
    }
  )
);
