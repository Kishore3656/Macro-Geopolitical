import { create } from 'zustand';
import { api } from '@/lib/api';
import { GTIData, GTIHistoryPoint } from '@/types';

interface GTIState {
  current: GTIData | null;
  history: GTIHistoryPoint[];
  loading: boolean;
  error: string | null;
  lastUpdate: Date | null;

  fetchCurrent: () => Promise<void>;
  fetchHistory: (hours: number) => Promise<void>;
  applyWSUpdate: (data: GTIData) => void;
}

export const useGTIStore = create<GTIState>((set) => ({
  current: null,
  history: [],
  loading: false,
  error: null,
  lastUpdate: null,

  fetchCurrent: async () => {
    set({ loading: true, error: null });
    const response = await api.gti();
    if ('error' in response) {
      set({ error: response.error, loading: false });
    } else {
      set({ current: response, lastUpdate: new Date(), loading: false });
    }
  },

  fetchHistory: async (hours: number) => {
    set({ loading: true, error: null });
    const response = await api.gtiHistory(hours);
    if ('error' in response) {
      set({ error: response.error, loading: false });
    } else {
      set({ history: response.history, loading: false });
    }
  },

  applyWSUpdate: (data: GTIData) => {
    set({ current: data, lastUpdate: new Date() });
  },
}));
