import { create } from 'zustand';
import { api } from '@/lib/api';
import { SignalsData, SignalHistoryPoint } from '@/types';

interface SignalsState {
  current: SignalsData | null;
  history: SignalHistoryPoint[];
  loading: boolean;
  error: string | null;
  lastUpdate: Date | null;

  fetchCurrent: () => Promise<void>;
  fetchHistory: (limit: number) => Promise<void>;
  applyWSUpdate: (data: SignalsData) => void;
}

export const useSignalsStore = create<SignalsState>((set) => ({
  current: null,
  history: [],
  loading: false,
  error: null,
  lastUpdate: null,

  fetchCurrent: async () => {
    set({ loading: true, error: null });
    const response = await api.signals();
    if ('error' in response) {
      set({ error: response.error, loading: false });
    } else {
      set({ current: response, lastUpdate: new Date(), loading: false });
    }
  },

  fetchHistory: async (limit: number) => {
    set({ loading: true, error: null });
    const response = await api.signalsHistory(limit);
    if ('error' in response) {
      set({ error: response.error, loading: false });
    } else {
      set({ history: response.history, loading: false });
    }
  },

  applyWSUpdate: (data: SignalsData) => {
    set({ current: data, lastUpdate: new Date() });
  },
}));
