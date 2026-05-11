import { BilateralData, GeoEventData, GTIData, RegionLiveData, SPYData } from '@/types';

type Tone = RegionLiveData['tone'];

type RegionDefinition = {
  id: string;
  label: string;
  tone: Tone;
  bounds: { west: number; south: number; east: number; north: number };
  countryCodes: string[];
  defaultTension: number;
  defaultTradeFlow: string;
  defaultStatusLabel: 'STATUS' | 'HAZARD';
  defaultStatusValue: string;
};

const REGION_DEFINITIONS: RegionDefinition[] = [
  {
    id: 'us-east',
    label: 'US East Coast',
    tone: 'yellow',
    bounds: { west: -90, south: 25, east: -60, north: 50 },
    countryCodes: ['USA', 'CAN'],
    defaultTension: 6.5,
    defaultTradeFlow: 'STABLE',
    defaultStatusLabel: 'STATUS',
    defaultStatusValue: 'STABLE',
  },
  {
    id: 'eu',
    label: 'EU',
    tone: 'yellow',
    bounds: { west: -12, south: 35, east: 32, north: 63 },
    countryCodes: ['FRA', 'DEU', 'GBR', 'ITA', 'ESP', 'NLD', 'BEL', 'POL', 'SWE', 'FIN', 'NOR', 'AUT'],
    defaultTension: 5,
    defaultTradeFlow: 'STABLE',
    defaultStatusLabel: 'STATUS',
    defaultStatusValue: 'STABLE',
  },
  {
    id: 'eastern-europe',
    label: 'Eastern Europe',
    tone: 'magenta',
    bounds: { west: 20, south: 45, east: 48, north: 68 },
    countryCodes: ['UKR', 'RUS', 'BLR', 'MDA', 'ROU', 'BGR', 'EST', 'LVA', 'LTU'],
    defaultTension: 8.5,
    defaultTradeFlow: 'UNSTABLE',
    defaultStatusLabel: 'HAZARD',
    defaultStatusValue: 'HIGH',
  },
  {
    id: 'middle-east',
    label: 'Middle East',
    tone: 'magenta',
    bounds: { west: 33, south: 10, east: 62, north: 42 },
    countryCodes: ['ISR', 'PSE', 'IRN', 'IRQ', 'SAU', 'ARE', 'QAT', 'KWT', 'SYR', 'JOR', 'LBN', 'YEM', 'OMN', 'TUR'],
    defaultTension: 8.5,
    defaultTradeFlow: 'UNSTABLE',
    defaultStatusLabel: 'HAZARD',
    defaultStatusValue: 'HIGH',
  },
  {
    id: 'kashmir',
    label: 'Kashmir Region',
    tone: 'magenta',
    bounds: { west: 70, south: 26, east: 86, north: 40 },
    countryCodes: ['IND', 'PAK', 'CHN'],
    defaultTension: 8.3,
    defaultTradeFlow: 'UNSTABLE',
    defaultStatusLabel: 'HAZARD',
    defaultStatusValue: 'HIGH',
  },
  {
    id: 'apac',
    label: 'APAC',
    tone: 'green',
    bounds: { west: 98, south: 18, east: 148, north: 56 },
    countryCodes: ['CHN', 'JPN', 'KOR', 'TWN', 'VNM', 'PHL', 'THA', 'MYS', 'SGP', 'IDN', 'AUS', 'NZL'],
    defaultTension: 4.5,
    defaultTradeFlow: 'STABLE',
    defaultStatusLabel: 'STATUS',
    defaultStatusValue: 'STABLE',
  },
];

function includesPoint(
  lat: number | null | undefined,
  lon: number | null | undefined,
  bounds: RegionDefinition['bounds']
): boolean {
  if (typeof lat !== 'number' || typeof lon !== 'number') return false;
  return lon >= bounds.west && lon <= bounds.east && lat >= bounds.south && lat <= bounds.north;
}

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function relationMatchesRegion(
  relation: BilateralData['relations'][number],
  region: RegionDefinition
): boolean {
  return region.countryCodes.includes(relation.country1) || region.countryCodes.includes(relation.country2);
}

function eventMatchesRegion(event: GeoEventData['events'][number], region: RegionDefinition): boolean {
  return includesPoint(event.latitude, event.longitude, region.bounds) || region.countryCodes.includes(event.country);
}

function toneFromTension(tension: number): Tone {
  if (tension >= 7.2) return 'magenta';
  if (tension >= 5.5) return 'yellow';
  return 'green';
}

export function buildRegionLiveData({
  bilateral,
  events,
  gti,
  spy,
}: {
  bilateral: BilateralData | null;
  events: GeoEventData | null;
  gti: GTIData | null;
  spy: SPYData | null;
}): RegionLiveData[] {
  return REGION_DEFINITIONS.map((region) => {
    const regionRelations = bilateral?.relations.filter((relation) => relationMatchesRegion(relation, region)) ?? [];
    const regionEvents = events?.events.filter((event) => eventMatchesRegion(event, region)) ?? [];

    const avgRelationStress =
      regionRelations.length > 0
        ? regionRelations.reduce((sum, relation) => sum + relation.stress_level, 0) / regionRelations.length
        : region.defaultTension;

    const eventIntensity =
      regionEvents.length > 0
        ? regionEvents.reduce((sum, event) => sum + Math.abs(event.goldstein_scale ?? 0), 0) / regionEvents.length
        : 0;

    const gtiLift = (gti?.score ?? 0) * 0.12;
    const marketLift = Math.abs(spy?.daily_change_pct ?? 0) * 0.08;
    const eventLift = Math.min(regionEvents.length * 0.18, 1.4);
    const intensityLift = Math.min(eventIntensity * 0.14, 1.5);

    const tension = clamp(
      Number(
        (
          avgRelationStress * 0.55 +
          region.defaultTension * 0.25 +
          gtiLift +
          marketLift +
          eventLift +
          intensityLift
        ).toFixed(1)
      ),
      0,
      9.9
    );

    const tradeFlow = tension >= 7 ? 'UNSTABLE' : tension >= 5.3 ? 'WATCHED' : 'STABLE';
    const statusLabel = tension >= 7 ? 'HAZARD' : 'STATUS';
    const statusValue = tension >= 8 ? 'HIGH' : tension >= 6 ? 'ELEVATED' : 'STABLE';

    return {
      id: region.id,
      tension,
      tradeFlow,
      statusLabel,
      statusValue,
      tone: toneFromTension(tension),
    };
  });
}

export const regionReference = REGION_DEFINITIONS.map((region) => ({
  id: region.id,
  label: region.label,
  bounds: region.bounds,
}));
