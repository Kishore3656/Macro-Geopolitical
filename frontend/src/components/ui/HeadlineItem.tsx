'use client';

import { ExternalLink, TrendingUp, TrendingDown } from 'lucide-react';
import { Headline } from '@/types';

interface HeadlineItemProps {
  headline: Headline;
}

export default function HeadlineItem({ headline }: HeadlineItemProps) {
  const isPositive = headline.sentiment_label === 'positive';
  const isNegative = headline.sentiment_label === 'negative';

  return (
    <a
      href={headline.url}
      target="_blank"
      rel="noopener noreferrer"
      className={`group hover:shadow-lg transition-all rounded-xl border backdrop-blur-sm p-5 block ${
        isPositive
          ? 'border-green-500/30 bg-gradient-to-r from-green-500/10 to-transparent hover:border-green-500/50'
          : isNegative
          ? 'border-red-500/30 bg-gradient-to-r from-red-500/10 to-transparent hover:border-red-500/50'
          : 'border-slate-700/50 bg-gradient-to-r from-slate-700/10 to-transparent hover:border-slate-600/50'
      }`}
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 mt-1">
          {isPositive ? (
            <TrendingUp className="w-4 h-4 text-green-400" />
          ) : isNegative ? (
            <TrendingDown className="w-4 h-4 text-red-400" />
          ) : (
            <div className="w-4 h-4 rounded-full bg-slate-600"></div>
          )}
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-semibold text-slate-200 group-hover:text-slate-100 transition-colors line-clamp-2 mb-2">
            {headline.title}
          </h4>
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs text-slate-400 font-medium">{headline.source}</span>
            <span className={`text-xs px-2 py-1 rounded-lg font-bold ${
              isPositive ? 'bg-green-500/20 text-green-300' :
              isNegative ? 'bg-red-500/20 text-red-300' :
              'bg-slate-700/20 text-slate-300'
            }`}>
              {headline.sentiment > 0 ? '+' : ''}{headline.sentiment.toFixed(2)}
            </span>
          </div>
        </div>
        <ExternalLink size={16} className="text-slate-500 group-hover:text-slate-300 transition-colors flex-shrink-0" />
      </div>
    </a>
  );
}
