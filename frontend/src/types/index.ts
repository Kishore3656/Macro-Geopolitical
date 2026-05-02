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
