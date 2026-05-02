import { useEffect } from 'react';
import { useGTIStore } from '@/store';
import { useWebSocket } from './useWebSocket';
import { GTIData } from '@/types';

export function useGTI() {
  const { current, history, loading, error, fetchCurrent, fetchHistory, applyWSUpdate } = useGTIStore();

  useEffect(() => {
    fetchCurrent();
    fetchHistory(48);
  }, [fetchCurrent, fetchHistory]);

  useWebSocket({
    url: 'ws://localhost:8000/ws/gti',
    onMessage: (data: GTIData) => {
      applyWSUpdate(data);
    },
  });

  return { current, history, loading, error };
}
