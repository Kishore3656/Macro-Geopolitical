'use client';

import { useMarket } from '@/hooks';

interface AssetCard {
  label: string;
  symbol: string;
  price: number;
  change: number;
  tone: 'text-[#9eff4f]' | 'text-[#ff7557]' | 'text-[#f6e327]';
}

export default function AssetImpact() {
  const { commodities } = useMarket();

  const buildAssetCards = (): AssetCard[] => {
    if (!commodities?.commodities) return [];

    return commodities.commodities.map((commodity) => {
      const change = commodity.daily_change_pct;
      const tone = change < -1.5 ? 'text-[#ff7557]' :
                   change < -0.5 ? 'text-[#f6e327]' : 'text-[#9eff4f]';

      return {
        label: commodity.name,
        symbol: commodity.symbol,
        price: commodity.current_price,
        change,
        tone,
      };
    });
  };

  const assetCards = buildAssetCards();

  return (
    <section className="nexus-panel p-4">
      <div className="text-xs uppercase tracking-[0.2em] text-[#8d8f86]">Asset Impact</div>
      <div className="mt-4 grid grid-cols-1 gap-3 md:grid-cols-3">
        {assetCards.map((asset) => (
          <div key={asset.symbol} className="border border-white/10 bg-white/[0.02] px-4 py-4">
            <div className="text-[0.72rem] uppercase tracking-[0.2em] text-[#8d8f86]">{asset.label}</div>
            <div className={`mt-3 text-[1.8rem] font-black tracking-[-0.08em] ${asset.tone}`}>
              ${asset.price.toFixed(2)}
            </div>
            <div className={`mt-2 text-sm font-semibold ${asset.tone}`}>
              {asset.change >= 0 ? '+' : ''}{asset.change.toFixed(2)}%
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
