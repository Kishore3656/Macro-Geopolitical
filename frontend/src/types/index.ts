export interface GTIData {
  score: number;
  risk_level: string;
  sentiment: number;
  volatility: number;
  conflict_count: number;
  peaceful_count: number;
  conflict_ratio: number;
  timestamp: string;
}

export interface GTIHistoryPoint {
  timestamp: string;
  score: number;
  risk_level: string;
}

export interface SignalsData {
  direction: "UP" | "DOWN";
  direction_prob: number;
  volatility: "LOW" | "MEDIUM" | "HIGH";
  volatility_prob: number;
  confidence: number;
  timestamp: string;
  regime?: "risk-on" | "risk-off" | "crisis" | "neutral";
  regime_confidence?: number;
  entities?: string[];
  narrative?: string;
  model_version?: string;
}

export interface SignalHistoryPoint {
  timestamp: string;
  direction: "UP" | "DOWN";
  direction_prob: number;
  volatility: "LOW" | "MEDIUM" | "HIGH";
  volatility_prob: number;
}

export interface SPYBar {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface SPYData {
  bars: SPYBar[];
  current_price: number;
  daily_change_pct: number;
  timestamp: string;
}

export interface Sector {
  name: string;
  performance: number;
  change_pct: number;
}

export interface SectorData {
  sectors: Sector[];
  timestamp: string;
}

export interface Commodity {
  name: string;
  symbol: string;
  current_price: number;
  daily_change_pct: number;
}

export interface CommodityData {
  commodities: Commodity[];
  timestamp: string;
  status: string;
}

export interface ConflictEntry {
  country: string;
  count: number;
  severity: "low" | "medium" | "high";
}

export interface ConflictData {
  conflicts: ConflictEntry[];
  total_events: number;
  timestamp: string;
}

export interface BilateralRelation {
  country1: string;
  country2: string;
  stress_level: number;
  stress_category: "stable" | "tense" | "critical";
  recent_events: number;
}

export interface BilateralData {
  relations: BilateralRelation[];
  timestamp: string;
}

export interface Headline {
  title: string;
  source: string;
  url: string;
  sentiment: number;
  sentiment_label: "negative" | "neutral" | "positive";
  published: string;
}

export interface HeadlineData {
  headlines: Headline[];
  timestamp: string;
}

export interface GeoEvent {
  event_id: string;
  event_type: string;
  country: string;
  location: string;
  latitude: number;
  longitude: number;
  event_code: string;
  goldstein_scale: number;
  timestamp: string;
}

export interface GeoEventData {
  events: GeoEvent[];
  timestamp: string;
}

export interface APIError {
  error: string;
}

export type APIResponse<T> = T | APIError;

// ─── Regions ─────────────────────────────────────────────────────────────────

export type RegionTone = 'yellow' | 'green' | 'magenta';

export interface RegionLiveData {
  id: string;
  tension: number;
  tradeFlow: string;
  statusLabel: 'STATUS' | 'HAZARD';
  statusValue: string;
  tone: RegionTone;
}

export interface RegionsData {
  regions: RegionLiveData[];
  timestamp: string;
}
