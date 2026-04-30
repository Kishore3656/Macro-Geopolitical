import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'GeoMarket Intelligence',
  description: 'Sovereign Intelligence Framework - Geopolitical & Market Analysis Dashboard',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-100">{children}</body>
    </html>
  );
}
