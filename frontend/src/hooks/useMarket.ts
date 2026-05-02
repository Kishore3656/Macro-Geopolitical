import { useEffect } from 'react';
import { useMarketStore } from '@/store';
import { useWebSocket } from './useWebSocket';
import { SPYData } from '@/types';

export function useMarket() {
  const { spy, sectors, loading, error, fetchSPY, fetchSectors, applyWSUpdate } = useMarketStore();

  useEffect(() => {
    fetchSPY(100);
    fetchSectors();
  }, [fetchSPY, fetchSectors]);

  useWebSocket({
    url: 'ws://localhost:8000/ws/market',
    onMessage: (data: SPYData) => {
      applyWSUpdate(data);
    },
  });

  return { spy, sectors, loading, error };
}
