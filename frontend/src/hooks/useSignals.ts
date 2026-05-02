import { useEffect } from 'react';
import { useSignalsStore } from '@/store';
import { useWebSocket } from './useWebSocket';
import { SignalsData } from '@/types';

export function useSignals() {
  const { current, history, loading, error, fetchCurrent, fetchHistory, applyWSUpdate } = useSignalsStore();

  useEffect(() => {
    fetchCurrent();
    fetchHistory(100);
  }, [fetchCurrent, fetchHistory]);

  useWebSocket({
    url: 'ws://localhost:8000/ws/signals',
    onMessage: (data: SignalsData) => {
      applyWSUpdate(data);
    },
  });

  return { current, history, loading, error };
}
