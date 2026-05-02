import { create } from 'zustand';
import { api } from '@/lib/api';
import { SPYData, SectorData } from '@/types';

interface MarketState {
  spy: SPYData | null;
  sectors: SectorData | null;
  loading: boolean;
  error: string | null;
  lastUpdate: Date | null;

  fetchSPY: (bars: number) => Promise<void>;
  fetchSectors: () => Promise<void>;
  applyWSUpdate: (data: SPYData) => void;
}

export const useMarketStore = create<MarketState>((set) => ({
  spy: null,
  sectors: null,
  loading: false,
  error: null,
  lastUpdate: null,

  fetchSPY: async (bars: number) => {
    set({ loading: true, error: null });
    const response = await api.spy(bars);
    if ('error' in response) {
      set({ error: response.error, loading: false });
    } else {
      set({ spy: response, lastUpdate: new Date(), loading: false });
    }
  },

  fetchSectors: async () => {
    set({ loading: true, error: null });
    const response = await api.sectors();
    if ('error' in response) {
      set({ error: response.error, loading: false });
    } else {
      set({ sectors: response, loading: false });
    }
  },

  applyWSUpdate: (data: SPYData) => {
    set({ spy: data, lastUpdate: new Date() });
  },
}));
