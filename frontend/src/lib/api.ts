import {
  APIResponse,
  GTIData,
  GTIHistoryPoint,
  SignalsData,
  SignalHistoryPoint,
  SPYData,
  SectorData,
  ConflictData,
  BilateralData,
  HeadlineData,
  GeoEventData,
} from '@/types';

const API_BASE_URL = 'http://localhost:8000';

async function fetchAPI<T>(endpoint: string, params?: Record<string, string | number>): Promise<APIResponse<T>> {
  try {
    const url = new URL(`${API_BASE_URL}${endpoint}`);
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        url.searchParams.append(key, String(value));
      });
    }

    const response = await fetch(url.toString(), { timeout: 5000 });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'Unknown error' };
  }
}

export const api = {
  gti: async (): Promise<APIResponse<GTIData>> => {
    return fetchAPI<GTIData>('/api/gti');
  },

  gtiHistory: async (hours: number = 48): Promise<APIResponse<{ history: GTIHistoryPoint[] }>> => {
    return fetchAPI<{ history: GTIHistoryPoint[] }>('/api/gti/history', { hours });
  },

  signals: async (): Promise<APIResponse<SignalsData>> => {
    return fetchAPI<SignalsData>('/api/signals');
  },

  signalsHistory: async (limit: number = 100): Promise<APIResponse<{ history: SignalHistoryPoint[] }>> => {
    return fetchAPI<{ history: SignalHistoryPoint[] }>('/api/signals/history', { limit });
  },

  headlines: async (limit: number = 20): Promise<APIResponse<HeadlineData>> => {
    return fetchAPI<HeadlineData>('/api/headlines', { limit });
  },

  spy: async (bars: number = 100): Promise<APIResponse<SPYData>> => {
    return fetchAPI<SPYData>('/api/market/spy', { bars });
  },

  sectors: async (): Promise<APIResponse<SectorData>> => {
    return fetchAPI<SectorData>('/api/market/sectors');
  },

  conflicts: async (limit: number = 15): Promise<APIResponse<ConflictData>> => {
    return fetchAPI<ConflictData>('/api/conflicts', { limit });
  },

  bilateral: async (limit: number = 10): Promise<APIResponse<BilateralData>> => {
    return fetchAPI<BilateralData>('/api/bilateral', { limit });
  },

  events: async (limit: number = 50): Promise<APIResponse<GeoEventData>> => {
    return fetchAPI<GeoEventData>('/api/events', { limit });
  },

  health: async (): Promise<boolean> => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`, { timeout: 5000 });
      return response.ok;
    } catch {
      return false;
    }
  },
};
