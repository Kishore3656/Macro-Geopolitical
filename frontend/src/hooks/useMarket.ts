import { useEffect } from 'react';
import { useMarketStore } from '@/store';
import { useWebSocket } from './useWebSocket';
import { SPYData } from '@/types';

export function useMarket() {
  const { spy, sectors, commodities, loading, error, fetchSPY, fetchSectors, fetchCommodities, applyWSUpdate } = useMarketStore();

  useEffect(() => {
    fetchSPY(100);
    fetchSectors();
    fetchCommodities();
  }, [fetchSPY, fetchSectors, fetchCommodities]);

  useWebSocket({
    url: 'ws://localhost:8000/ws/market',
    onMessage: (data: SPYData) => {
      applyWSUpdate(data);
    },
  });

  return { spy, sectors, commodities, loading, error };
}
