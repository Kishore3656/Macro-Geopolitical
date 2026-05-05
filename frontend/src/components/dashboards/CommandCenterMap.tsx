'use client';

import { useMemo, useState } from 'react';

type RegionTone = 'yellow' | 'green' | 'magenta' | 'hatched';

interface RegionCard {
  id: string;
  label: string;
  tension: number;
  tradeFlow: string;
  hazard: string;
  tone: RegionTone;
  position: { left: string; top: string };
}

interface CommandCenterMapProps {
  accentTitle?: string;
  contextLabel?: string;
}

const toneClass: Record<RegionTone, string> = {
  yellow: 'border-[#f6e327] text-[#f6e327]',
  green: 'border-[#9eff4f] text-[#9eff4f]',
  magenta: 'border-[#f43de2] text-[#ff8df4]',
  hatched: 'border-white/40 text-[#d7d7cf]',
};

const regionCards: RegionCard[] = [
  {
    id: 'us-east',
    label: 'US East Coast',
    tension: 6.5,
    tradeFlow: 'STABLE',
    hazard: 'STABLE',
    tone: 'yellow',
    position: { left: '26%', top: '45%' },
  },
  {
    id: 'eu',
    label: 'EU',
    tension: 5.0,
    tradeFlow: 'STABLE',
    hazard: 'STABLE',
    tone: 'green',
    position: { left: '47%', top: '57%' },
  },
  {
    id: 'eastern-europe',
    label: 'Eastern Europe',
    tension: 8.5,
    tradeFlow: 'UNSTABLE',
    hazard: 'HIGH',
    tone: 'magenta',
    position: { left: '63%', top: '30%' },
  },
  {
    id: 'middle-east',
    label: 'Middle East',
    tension: 8.5,
    tradeFlow: 'UNSTABLE',
    hazard: 'HIGH',
    tone: 'magenta',
    position: { left: '57%', top: '63%' },
  },
  {
    id: 'kashmir',
    label: 'Kashmir Region',
    tension: 8.3,
    tradeFlow: 'UNSTABLE',
    hazard: 'MED',
    tone: 'magenta',
    position: { left: '72%', top: '37%' },
  },
  {
    id: 'apac',
    label: 'APAC',
    tension: 4.5,
    tradeFlow: 'STABLE',
    hazard: 'STABLE',
    tone: 'green',
    position: { left: '83%', top: '58%' },
  },
];

function RegionPopup({ region }: { region: RegionCard }) {
  return (
    <div className={`min-w-[180px] border bg-black/90 px-3 py-2 text-[10px] shadow-[0_0_25px_rgba(0,0,0,0.55)] ${toneClass[region.tone]}`}>
      <div className="font-bold uppercase tracking-[0.08em]">{region.label}</div>
      <div className="mt-1 text-[#f3f3eb]">TENSION_INDEX: {region.tension.toFixed(1)}</div>
      <div className="text-[#f3f3eb]">TRADE_FLOW: {region.tradeFlow}</div>
      <div className="text-[#f3f3eb]">HAZARD: {region.hazard}</div>
    </div>
  );
}

export default function CommandCenterMap({
  accentTitle = 'The Command Hub',
  contextLabel = 'Global geospatial conflict lattice',
}: CommandCenterMapProps) {
  const [activeRegion, setActiveRegion] = useState<string>('eastern-europe');

  const selectedRegion = useMemo(
    () => regionCards.find((region) => region.id === activeRegion) ?? regionCards[0],
    [activeRegion]
  );

  return (
    <section className="nexus-panel overflow-hidden">
      <div className="flex items-center gap-3 border-b border-white/10 px-4 py-3 text-[0.95rem] font-bold text-[#f4f1e8]">
        <span className="nexus-dot" />
        <span>{accentTitle}</span>
      </div>

      <div className="relative bg-black">
        <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_240px]">
          <div className="relative min-h-[620px] overflow-hidden border-r border-white/10 bg-black">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.045),transparent_34%)]" />
            <div className="absolute inset-0 bg-[linear-gradient(180deg,transparent_0%,rgba(255,255,255,0.015)_100%)]" />
            <svg viewBox="0 0 1100 700" className="absolute inset-0 h-full w-full">
              <defs>
                <pattern id="mapHatch" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
                  <rect width="12" height="12" fill="#7f7f7f" fillOpacity="0.08" />
                  <line x1="0" y1="0" x2="0" y2="12" stroke="#b6b6b6" strokeWidth="5" strokeOpacity="0.75" />
                </pattern>
                <pattern id="greyHatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                  <rect width="10" height="10" fill="#8b8b8b" fillOpacity="0.06" />
                  <line x1="0" y1="0" x2="0" y2="10" stroke="#b7b7b7" strokeWidth="4" strokeOpacity="0.8" />
                </pattern>
                <pattern id="greenHatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
                  <rect width="10" height="10" fill="#9eff4f" fillOpacity="0.12" />
                  <line x1="0" y1="0" x2="0" y2="10" stroke="#b7ff7d" strokeWidth="4" strokeOpacity="0.85" />
                </pattern>
                <pattern id="magentaHatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
                  <rect width="10" height="10" fill="#f43de2" fillOpacity="0.14" />
                  <line x1="0" y1="0" x2="0" y2="10" stroke="#f772ea" strokeWidth="4" strokeOpacity="0.85" />
                </pattern>
              </defs>

              <g opacity="0.98">
                <path d="M66 165 108 132 152 118 191 95 272 104 330 96 392 108 457 100 534 114 573 135 558 157 510 171 485 195 433 208 388 236 347 254 307 287 256 302 192 291 151 260 111 224 81 195Z" fill="url(#greyHatch)" stroke="#111" strokeWidth="2" />
                <path d="M150 255 221 260 280 287 314 322 297 356 253 385 209 395 162 404 118 389 104 354 92 310Z" fill="#f6e327" stroke="#111" strokeWidth="2" />
                <path d="M274 343 318 377 354 426 390 481 407 541 391 618 359 586 334 523 312 486 286 426 259 389Z" fill="url(#greyHatch)" stroke="#111" strokeWidth="2" />
                <path d="M447 220 475 209 503 218 517 235 516 257 496 270 470 267 447 247Z" fill="#f6e327" stroke="#111" strokeWidth="2" />
                <path d="M514 195 548 193 577 214 592 245 586 278 556 296 523 280 506 242Z" fill="#9eff4f" stroke="#111" strokeWidth="2" />
                <path d="M586 170 652 160 728 163 787 174 856 193 858 237 817 256 760 271 723 291 660 296 614 275 590 240Z" fill="url(#magentaHatch)" stroke="#111" strokeWidth="2" />
                <path d="M675 306 724 297 751 317 739 349 712 370 683 355 664 328Z" fill="#f43de2" stroke="#111" strokeWidth="2" />
                <path d="M560 294 606 312 648 370 636 430 600 533 557 519 531 447 520 382 526 335Z" fill="#6d6d6d" fillOpacity="0.72" stroke="#111" strokeWidth="2" />
                <path d="M646 278 733 277 817 281 883 311 910 348 888 381 857 394 822 430 783 451 728 420 706 378 681 344 649 325Z" fill="#9eff4f" stroke="#111" strokeWidth="2" />
                <path d="M861 458 894 476 924 519 908 561 869 585 820 575 804 541 812 491Z" fill="url(#greenHatch)" stroke="#111" strokeWidth="2" />
                <path d="M914 108 927 95 948 102 952 116 936 122Z" fill="#8b8b8b" stroke="#111" strokeWidth="1.5" />
                <path d="M686 124 698 118 704 126 696 133Z" fill="#f43de2" stroke="#111" strokeWidth="1.5" />
                <path d="M699 116 710 108 717 116 709 124Z" fill="#f43de2" stroke="#111" strokeWidth="1.5" />
                <path d="M719 110 731 104 737 110 728 118Z" fill="#f43de2" stroke="#111" strokeWidth="1.5" />
              </g>

              <g fill="none" strokeWidth="2">
                <rect x="0" y="158" width="430" height="152" stroke="#cdb75b" />
                <rect x="430" y="82" width="193" height="360" stroke="#d0bc59" />
                <rect x="623" y="80" width="266" height="268" stroke="#d039be" />
                <rect x="830" y="288" width="186" height="334" stroke="#8fce63" />
                <rect x="518" y="330" width="212" height="290" stroke="#d039be" />
                <rect x="250" y="280" width="190" height="340" stroke="#95cf72" />
              </g>
            </svg>

            {regionCards.map((region) => (
              <button
                key={region.id}
                type="button"
                className="group absolute z-20 h-4 w-4 -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/40 bg-black/70"
                style={{ left: region.position.left, top: region.position.top }}
                onMouseEnter={() => setActiveRegion(region.id)}
                onFocus={() => setActiveRegion(region.id)}
              >
                <span className={`absolute inset-0 rounded-full ${
                  region.tone === 'yellow'
                    ? 'bg-[#f6e327]'
                    : region.tone === 'green'
                    ? 'bg-[#9eff4f]'
                    : 'bg-[#f43de2]'
                } opacity-90`} />
                <span className="absolute -inset-1 animate-ping rounded-full border border-white/30 opacity-40" />
              </button>
            ))}

            <div
              className="absolute z-30"
              style={{
                left: selectedRegion.position.left,
                top: selectedRegion.position.top,
                transform: 'translate(18px, -110%)',
              }}
            >
              <RegionPopup region={selectedRegion} />
            </div>
          </div>

          <div className="flex flex-col bg-black">
            <div className="border-b border-white/10 px-4 py-4 text-xs uppercase tracking-[0.18em] text-[#8d8f86]">
              {contextLabel}
            </div>
            <div className="flex-1 space-y-3 px-4 py-4 text-xs">
              {regionCards.map((region) => (
                <button
                  key={region.id}
                  type="button"
                  onMouseEnter={() => setActiveRegion(region.id)}
                  onFocus={() => setActiveRegion(region.id)}
                  className={`w-full border px-3 py-3 text-left transition-colors ${
                    activeRegion === region.id
                      ? `${toneClass[region.tone]} bg-white/[0.03]`
                      : 'border-white/10 text-[#c2c2b8] hover:bg-white/[0.02]'
                  }`}
                >
                  <div className="font-bold uppercase">{region.label}</div>
                  <div className="mt-1 text-[#d9d9d0]">Tension Index: {region.tension.toFixed(1)}</div>
                  <div className="text-[#9ca096]">Trade Flow: {region.tradeFlow}</div>
                  <div className="text-[#9ca096]">Hazard: {region.hazard}</div>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
