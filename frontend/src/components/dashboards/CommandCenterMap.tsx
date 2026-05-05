'use client';

import { useState } from 'react';
import { geoMercator, geoPath } from 'd3-geo';
import { feature, mesh } from 'topojson-client';
import landAtlas from 'world-atlas/land-110m.json';
import countriesAtlas from 'world-atlas/countries-110m.json';
import type { Feature, GeometryCollection, MultiLineString, MultiPolygon, Polygon } from 'geojson';

const VIEWBOX_WIDTH = 1100;
const VIEWBOX_HEIGHT = 650;

type RegionTone = 'yellow' | 'green' | 'magenta' | 'hatched';

interface AtlasTopology {
  type: 'Topology';
  arcs: number[][][];
  bbox?: [number, number, number, number];
  transform: {
    scale: [number, number];
    translate: [number, number];
  };
  objects: Record<string, GeometryCollection>;
}

interface RegionCard {
  id: string;
  label: string;
  tension: number;
  tradeFlow: string;
  statusLabel: 'STATUS' | 'HAZARD';
  statusValue: string;
  tone: RegionTone;
  coordinate: [number, number];
  popupPosition: { left: string; top: string };
}

interface RegionOverlay {
  id: string;
  fill: string;
  geometry: Polygon;
}

interface CommandCenterMapProps {
  accentTitle?: string;
  contextLabel?: string;
}

const landData = landAtlas as unknown as AtlasTopology;
const countriesData = countriesAtlas as unknown as AtlasTopology;

const landFeature = feature(
  landData as never,
  landData.objects.land as never
) as unknown as Feature<Polygon | MultiPolygon>;

const countryBorders = mesh(
  countriesData as never,
  countriesData.objects.countries as never,
  (a, b) => a !== b
) as unknown as MultiLineString;

const projection = geoMercator()
  .fitExtent(
    [
      [40, 50],
      [1040, 630],
    ],
    landFeature
  )
  .translate([520, 325]);

const pathBuilder = geoPath(projection);
const landPath = pathBuilder(landFeature) ?? '';
const countryBordersPath = pathBuilder(countryBorders) ?? '';

const toneClass: Record<RegionTone, string> = {
  yellow: 'border-[#f6e327] text-[#f6e327]',
  green: 'border-[#9eff4f] text-[#9eff4f]',
  magenta: 'border-[#f43de2] text-[#ff8df4]',
  hatched: 'border-white/40 text-[#d7d7cf]',
};

function geoBox(west: number, south: number, east: number, north: number): Polygon {
  return {
    type: 'Polygon',
    coordinates: [[
      [west, south],
      [east, south],
      [east, north],
      [west, north],
      [west, south],
    ]],
  };
}

const regionOverlays: RegionOverlay[] = [
  {
    id: 'us-east',
    fill: 'url(#zoneYellow)',
    geometry: geoBox(-90, 25, -60, 50),
  },
  {
    id: 'eu',
    fill: 'url(#zoneYellowHatch)',
    geometry: geoBox(-12, 35, 32, 63),
  },
  {
    id: 'eastern-europe',
    fill: 'url(#zoneMagentaHatch)',
    geometry: geoBox(20, 45, 48, 68),
  },
  {
    id: 'middle-east',
    fill: 'url(#zoneMagentaSolid)',
    geometry: geoBox(33, 10, 62, 42),
  },
  {
    id: 'kashmir',
    fill: 'url(#zoneMagentaSolid)',
    geometry: geoBox(70, 26, 86, 40),
  },
  {
    id: 'apac',
    fill: 'url(#zoneGreenHatch)',
    geometry: geoBox(98, 18, 148, 56),
  },
];

const regionCards: RegionCard[] = [
  {
    id: 'us-east',
    label: 'US East Coast',
    tension: 6.5,
    tradeFlow: 'STABLE',
    statusLabel: 'STATUS',
    statusValue: 'STABLE',
    tone: 'yellow',
    coordinate: [-74, 40.7],
    popupPosition: { left: '24.5%', top: '48.5%' },
  },
  {
    id: 'eu',
    label: 'EU',
    tension: 5.0,
    tradeFlow: 'STABLE',
    statusLabel: 'STATUS',
    statusValue: 'STABLE',
    tone: 'yellow',
    coordinate: [7, 47.5],
    popupPosition: { left: '43.5%', top: '59%' },
  },
  {
    id: 'eastern-europe',
    label: 'Eastern Europe',
    tension: 8.5,
    tradeFlow: 'UNSTABLE',
    statusLabel: 'HAZARD',
    statusValue: 'HIGH',
    tone: 'magenta',
    coordinate: [35, 53],
    popupPosition: { left: '61.5%', top: '31.5%' },
  },
  {
    id: 'middle-east',
    label: 'Middle East',
    tension: 8.5,
    tradeFlow: 'UNSTABLE',
    statusLabel: 'HAZARD',
    statusValue: 'HIGH',
    tone: 'magenta',
    coordinate: [45, 25],
    popupPosition: { left: '54.5%', top: '64.5%' },
  },
  {
    id: 'kashmir',
    label: 'Kashmir Region',
    tension: 8.3,
    tradeFlow: 'UNSTABLE',
    statusLabel: 'HAZARD',
    statusValue: 'HIGH',
    tone: 'magenta',
    coordinate: [75, 34],
    popupPosition: { left: '72.2%', top: '40.5%' },
  },
  {
    id: 'apac',
    label: 'APAC',
    tension: 4.5,
    tradeFlow: 'STABLE',
    statusLabel: 'STATUS',
    statusValue: 'STABLE',
    tone: 'green',
    coordinate: [120, 31],
    popupPosition: { left: '86.5%', top: '56.5%' },
  },
];

function RegionPopup({ region }: { region: RegionCard }) {
  return (
    <div
      className={`min-w-[180px] border bg-black/95 px-3 py-2 text-[10px] leading-[1.45] shadow-[0_0_25px_rgba(0,0,0,0.55)] ${toneClass[region.tone]}`}
    >
      <div className="flex items-start gap-2">
        <span
          className={`mt-[3px] inline-block h-2.5 w-2.5 shrink-0 ${
            region.tone === 'yellow'
              ? 'bg-[#f6e327]'
              : region.tone === 'green'
              ? 'bg-[#9eff4f]'
              : 'bg-[#f43de2]'
          }`}
        />
        <div>
          <div className="font-bold">{region.label}:</div>
          <div className="text-[#f3f3eb]">TENSION_INDEX: {region.tension.toFixed(1)}</div>
          <div className="text-[#f3f3eb]">TRADE_FLOW: {region.tradeFlow}</div>
          <div className="text-[#f3f3eb]">{region.statusLabel}: {region.statusValue}</div>
        </div>
      </div>
    </div>
  );
}

export default function CommandCenterMap({
  accentTitle = 'The Command Hub',
  contextLabel = 'Global geospatial conflict lattice',
}: CommandCenterMapProps) {
  const [hoveredRegionId, setHoveredRegionId] = useState<string | null>(null);

  const projectedCards = regionCards.map((region) => {
    const overlay = regionOverlays.find((o) => o.id === region.id);
    const point = projection(region.coordinate) ?? [0, 0];
    return {
      ...region,
      point,
      overlay,
    };
  });

  return (
    <section className="nexus-panel overflow-hidden">
      <div className="flex items-center gap-3 border-b border-white/10 px-4 py-3 text-[0.95rem] font-bold text-[#f4f1e8]">
        <span className="nexus-dot" />
        <span>{accentTitle}</span>
      </div>

      <div className="relative bg-black">
        <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_252px]">
          <div className="relative min-h-[600px] overflow-hidden border-r border-white/10 bg-black">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_14%,rgba(255,255,255,0.05),transparent_38%)]" />
            <div className="absolute inset-0 bg-[linear-gradient(180deg,transparent_0%,rgba(255,255,255,0.02)_100%)]" />

            <svg viewBox={`0 0 ${VIEWBOX_WIDTH} ${VIEWBOX_HEIGHT}`} className="absolute inset-0 h-full w-full">
              <defs>
                <pattern id="landHatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(38)">
                  <rect width="10" height="10" fill="#8f8f8f" fillOpacity="0.08" />
                  <line x1="0" y1="0" x2="0" y2="10" stroke="#bebebe" strokeWidth="4" strokeOpacity="0.75" />
                </pattern>
                <pattern id="zoneYellow" width="12" height="12" patternUnits="userSpaceOnUse">
                  <rect width="12" height="12" fill="#f6e327" />
                </pattern>
                <pattern id="zoneYellowHatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(38)">
                  <rect width="10" height="10" fill="#c4a024" fillOpacity="0.4" />
                  <line x1="0" y1="0" x2="0" y2="10" stroke="#f6e327" strokeWidth="4" strokeOpacity="0.8" />
                </pattern>
                <pattern id="zoneGreen" width="12" height="12" patternUnits="userSpaceOnUse">
                  <rect width="12" height="12" fill="#92ef3e" />
                </pattern>
                <pattern id="zoneGreenHatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(38)">
                  <rect width="10" height="10" fill="#7bc84a" fillOpacity="0.45" />
                  <line x1="0" y1="0" x2="0" y2="10" stroke="#b7f07f" strokeWidth="4" strokeOpacity="0.86" />
                </pattern>
                <pattern id="zoneMagentaHatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(38)">
                  <rect width="10" height="10" fill="#b833ab" fillOpacity="0.35" />
                  <line x1="0" y1="0" x2="0" y2="10" stroke="#ff83f3" strokeWidth="4" strokeOpacity="0.86" />
                </pattern>
                <pattern id="zoneMagentaSolid" width="12" height="12" patternUnits="userSpaceOnUse">
                  <rect width="12" height="12" fill="#d73bd0" />
                </pattern>
                <clipPath id="landClip">
                  <path d={landPath} />
                </clipPath>
              </defs>

              <path d={landPath} fill="url(#landHatch)" stroke="#151515" strokeWidth="2.5" />

              <g clipPath="url(#landClip)">
                {regionOverlays.map((overlay) => {
                  const overlayPath = pathBuilder(overlay.geometry) ?? '';
                  return <path key={overlay.id} d={overlayPath} fill={overlay.fill} opacity={0.98} />;
                })}
              </g>

              <path d={countryBordersPath} fill="none" stroke="#1a1a1a" strokeWidth="1.3" opacity={0.92} />

              <g clipPath="url(#landClip)" fill="none" pointerEvents="auto" style={{ cursor: 'pointer' }}>
                {regionOverlays.map((overlay) => {
                  const overlayPath = pathBuilder(overlay.geometry) ?? '';
                  return (
                    <path
                      key={`${overlay.id}-interactive`}
                      d={overlayPath}
                      opacity="0"
                      onMouseEnter={() => setHoveredRegionId(overlay.id)}
                      onMouseLeave={() => setHoveredRegionId(null)}
                    />
                  );
                })}
              </g>
            </svg>

            <div className="absolute inset-x-0 top-3 px-4 text-center text-[11px] uppercase tracking-[0.22em] text-[#80837b]">
              World conflict overview
            </div>


            {projectedCards.map((region) => (
              <div
                key={`${region.id}-popup`}
                className={`absolute z-30 transition-opacity duration-200 ${
                  hoveredRegionId === region.id ? 'opacity-100' : 'opacity-0 pointer-events-none'
                }`}
                style={{
                  left: `${region.point[0]}px`,
                  top: `${region.point[1]}px`,
                  transform: 'translate(-50%, -50%)',
                }}
                onMouseEnter={() => setHoveredRegionId(region.id)}
                onMouseLeave={() => setHoveredRegionId(null)}
              >
                <RegionPopup region={region} />
              </div>
            ))}
          </div>

          <div className="flex flex-col bg-black">
            <div className="border-b border-white/10 px-4 py-4 text-xs uppercase tracking-[0.18em] text-[#8d8f86]">
              {contextLabel}
            </div>
            <div className="flex-1 space-y-3 px-4 py-4 text-xs">
              {projectedCards.map((region) => (
                <div
                  key={region.id}
                  className={`w-full border px-3 py-3 text-left cursor-pointer transition-all duration-200 ${toneClass[region.tone]} ${
                    hoveredRegionId === region.id
                      ? 'bg-white/[0.1] shadow-[0_0_12px_rgba(255,255,255,0.1)]'
                      : 'bg-white/[0.03]'
                  }`}
                  onMouseEnter={() => setHoveredRegionId(region.id)}
                  onMouseLeave={() => setHoveredRegionId(null)}
                >
                  <div className="font-bold uppercase">{region.label}</div>
                  <div className="mt-1 text-[#d9d9d0]">Tension Index: {region.tension.toFixed(1)}</div>
                  <div className="text-[#9ca096]">Trade Flow: {region.tradeFlow}</div>
                  <div className="text-[#9ca096]">{region.statusLabel}: {region.statusValue}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
