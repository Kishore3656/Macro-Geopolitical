import { useState, useEffect, useCallback } from 'react';
import { api } from '@/lib/api';
import type { RegionLiveData } from '@/types';

export function useRegions() {
  const [regions, setRegions] = useState<RegionLiveData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRegions = useCallback(async () => {
    setLoading(true);
    const response = await api.regions();
    if ('error' in response) {
      setError(response.error ?? 'Unknown error');
    } else {
      setRegions(response.regions);
      setError(null);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchRegions();
    const interval = setInterval(fetchRegions, 60_000);
    return () => clearInterval(interval);
  }, [fetchRegions]);

  return { regions, loading, error };
}
