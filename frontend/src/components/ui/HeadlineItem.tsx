'use client';

import { ExternalLink } from 'lucide-react';
import { Headline } from '@/types';

interface HeadlineItemProps {
  headline: Headline;
}

const sentimentColors = {
  negative: 'bg-danger bg-opacity-20 text-danger',
  neutral: 'bg-slate-800 text-slate-300',
  positive: 'bg-success bg-opacity-20 text-success',
};

export default function HeadlineItem({ headline }: HeadlineItemProps) {
  return (
    <a
      href={headline.url}
      target="_blank"
      rel="noopener noreferrer"
      className="block bg-[#13151d] border border-slate-800 rounded-lg p-4 hover:border-slate-700 transition-colors group"
    >
      <div className="flex items-start gap-3">
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-semibold text-slate-200 group-hover:text-cyan transition-colors line-clamp-2 mb-2">
            {headline.title}
          </h4>
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500">{headline.source}</span>
            <span className={`text-xs px-2 py-1 rounded ${sentimentColors[headline.sentiment_label]}`}>
              {headline.sentiment > 0 ? '+' : ''}{headline.sentiment.toFixed(2)}
            </span>
          </div>
        </div>
        <ExternalLink size={16} className="text-slate-600 group-hover:text-cyan transition-colors flex-shrink-0 mt-1" />
      </div>
    </a>
  );
}
