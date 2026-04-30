# GeoMarket Frontend - React/Next.js Dashboard

Modern React 19 + Next.js 15 frontend for the GeoMarket Intelligence platform. This is an **optional** environment that runs alongside the main Streamlit application.

## Features

- **Real-time Data**: Polling-based and WebSocket-ready data synchronization
- **Responsive Design**: Mobile-first dashboard using Tailwind CSS
- **Performance**: Built with Next.js 15 for optimal performance
- **Type-Safe**: Full TypeScript support
- **Dark Theme**: Professional UI with Lucide icons and Tailwind styling

## Tech Stack

- **Framework**: Next.js 15 (React 19)
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Charting**: Recharts
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Language**: TypeScript

## Getting Started

### Prerequisites

- Node.js 18+ (Node.js 24 LTS recommended)
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
npm start
```

## Project Structure

```
src/
├── app/              # Next.js app router (pages & layouts)
├── components/       # React components
│   ├── dashboards/   # Dashboard views (EarthPulse, GeoMap, Market, AISignals)
│   ├── charts/       # Chart components
│   ├── Dashboard.tsx # Main dashboard controller
│   ├── Sidebar.tsx   # Navigation sidebar
│   └── MetricCard.tsx # Metric display component
├── hooks/            # Custom React hooks
├── lib/              # Utilities
└── types/            # TypeScript interfaces
```

## Dashboards

- **Earth Pulse**: Global markets, capital flows, economic indicators, geopolitical tension
- **Geo Map**: Country-level heatmaps, currency movements, commodity flows
- **Market**: S&P 500 analysis, sector rankings, technical indicators
- **AI Signals**: ML-generated trade signals with confidence and volatility

## Environment Variables

Create a `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Integration

The frontend expects these backend endpoints:

```
GET /health                 → Connection status
GET /api/earth-pulse       → GTI, sentiment, volatility, capital flows
GET /api/signals           → Trade signals with confidence and volatility
GET /api/geo-map           → Geographic/market data
GET /api/market            → Market technicals and sector data
```

All data is fetched with 5-second polling intervals (configurable per component).

## Performance Optimization

- Code splitting and lazy loading
- Image optimization with Next.js Image component
- CSS-in-JS with Tailwind for minimal bundle size
- Incremental Static Regeneration (ISR) for frequently accessed pages

## Running with GeoMarket

Both environments can run simultaneously:

```bash
# Terminal 1: Main Streamlit app
python app.py

# Terminal 2: React frontend
cd frontend && npm run dev
```

- Streamlit UI: `http://localhost:8501`
- React Frontend: `http://localhost:3000`

## Design System

**Color Scheme**:
- Background: `#0f172a` (slate-950)
- Surface: `#1e293b` (slate-800)
- Accent: `#3b82f6` (blue-500)
- Success: `#10b981` (green-500)
- Warning: `#f59e0b` (amber-500)
- Danger: `#ef4444` (red-500)

**Layout**:
- Sidebar navigation (collapsible on mobile)
- Header with connection status
- Responsive grid layouts
- Dark theme throughout

## Deployment

### Vercel (Recommended)

```bash
vercel deploy
```

### Docker

```bash
docker build -t geomarket-frontend .
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://backend:8000 \
  geomarket-frontend
```

Environment variables:
- `NEXT_PUBLIC_API_URL`: Backend API URL (required)
- `NODE_ENV`: Set to `production` for production builds
