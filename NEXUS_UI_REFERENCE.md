# NEXUS UI Reference - Layout & Colors

---

## 📐 Four-Column Grid Layout

All NEXUS dashboards use this responsive grid:

```
┌─────────────┬──────────────────────┬──────────────┐
│  SIDEBAR    │     CENTER PANEL     │  RIGHT PANEL │
│  (1 col)    │     (2 cols)         │   (1 col)    │
│             │                      │              │
│ - Nav      │ - Maps              │ - News       │
│ - Stats    │ - Charts            │ - Alerts     │
│ - Metrics  │ - Tables            │ - Metrics    │
│             │                      │              │
└─────────────┴──────────────────────┴──────────────┘
```

**Responsive:** On mobile, stacks to single column

---

## 🎨 Color Palette

### Primary Colors
```
Green     #4ade80  (Stable, Safe, Primary)
Cyan      #22d3ee  (Info, Secondary)
Magenta   #ff00ff  (Warning, Highlight)
Yellow    #ffff00  (Caution, Trend)
Red       #ff0000  (Critical, Danger)
```

### Backgrounds
```
Black       #000000  (Primary background)
Black/80%   rgba(0,0,0,0.8)  (Panel background)
Black/60%   rgba(0,0,0,0.6)  (Card background)
Gray 900    #111111  (Hover state)
```

### Borders
```
Green 30%   border-green-400/30      (Primary borders)
Cyan 30%    border-cyan-400/30       (Info borders)
Red 50%     border-red-500/50        (Critical borders)
Yellow 50%  border-yellow-500/50     (Warning borders)
```

---

## 🖼️ Page Layouts

### 1. NEXUS Command (Home)
```
┌─────────────┬──────────────────────┬──────────────┐
│ INTEL CORE  │ NEXUS HEADER         │ LIVE NEWS    │
│ Navigation  │ "NEXUS Command v2"   │ TICKER       │
│             │                      │              │
│ Stats:      │ GEOSPATIAL MAP       │ ▢ Events     │
│ • Port      │ ┌──────────────────┐ │ ▢ Intensity  │
│ • Location  │ │ US: 🟡           │ │ ▢ Region     │
│ • Status    │ │ EU: 🟢           │ │              │
│             │ │ RU: 🔴 CRITICAL  │ │              │
│ LEGEND      │ │ ME: 🔴 HIGH      │ │ ASSET IMPACT │
│ 🔴 High     │ │ CN: 🟡           │ │ ▢ OIL: +3.5% │
│ 🟡 Medium   │ └──────────────────┘ │ ▢ EUR: -0.2% │
│ 🟢 Low      │                      │ ▢ GOLD: +1.8%│
│             │ REGION CARDS         │              │
│             │ ┌──────┐ ┌──────┐   │ STATUS SUM   │
│             │ │ USA  │ │ EU   │   │ Risk: HIGH   │
│             │ │ ✓OK  │ │ ✓OK  │   │ Stability: ⚠ │
│             │ └──────┘ └──────┘   │              │
└─────────────┴──────────────────────┴──────────────┘
```

### 2. Earth Pulse
```
┌─────────────┬──────────────────────┬──────────────┐
│ EARTH PULSE │ CRITICAL EVENTS      │ RISK METRICS │
│             │ ▢ Event 1 [INT: 9]   │ ▢ Instability│
│ GTI SCORE   │ ▢ Event 2 [INT: 8]   │ ▢ Trade Risk │
│ 7.2/10      │ ▢ Event 3 [INT: 7]   │ ▢ Sentiment  │
│ 🔴 CRITICAL │                      │              │
│             │ REGIONAL BREAKDOWN   │ HOTSPOTS     │
│ KEY METRICS │ ME: 15 events        │ 🔴 Middle E. │
│ • Vol: 340M │ EU: 12 events        │ 🔴 East. Eu. │
│ • Sentiment │ AS: 9 events         │ 🟡 S. China  │
│ • Threat    │ ...                  │              │
│             │                      │ SYSTEM ALERTS│
│             │                      │ ⚠ GTI spike  │
│             │                      │ ⚠ Trade risk │
│             │                      │ ✓ No cyber   │
└─────────────┴──────────────────────┴──────────────┘
```

### 3. Geo Map
```
┌─────────────┬──────────────────────┬──────────────┐
│ GEO MAPPER  │ WORLD MAP            │ BILATERAL    │
│             │ ┌──────────────────┐ │ RELATIONS    │
│ QUICK STATS │ │                  │ │              │
│ Crit: 8     │ │ 🟢 Americas      │ │ ▢ US-China   │
│ High: 12    │ │ 🟢 W.Europe      │ │   Stress: 7.2│
│ Medium: 4   │ │ 🔴 E.Europe 🎯   │ │              │
│             │ │ 🔴 Middle East   │ │ ▢ Russia-EU  │
│ FOCAL       │ │ 🟡 Asia          │ │   Stress: 8.3│
│ REGIONS     │ │ 🟡 S. China Sea  │ │              │
│ • M. East   │ │                  │ │ ▢ India-Pak  │
│ • E. Europe │ │                  │ │   Stress: 6.5│
│ • S. China  │ └──────────────────┘ │              │
│             │ CRITICAL ZONES       │ [20 more     │
│ LEGEND      │ • Russia-Ukraine     │  relations]  │
│ 🔴 Critical │ • Gaza-Israel        │              │
│ 🟡 High     │ • Iran-Saudi         │              │
│ 🟢 Stable   │                      │              │
└─────────────┴──────────────────────┴──────────────┘
```

### 4. Market
```
┌─────────────┬──────────────────────┬──────────────┐
│ MARKET      │ MAJOR INDICES        │ GLOBAL ASSETS│
│ MONITOR     │ ▢ S&P 500: $4,582    │ ▢ SPY  462.30│
│             │   ▲ +1.25%           │   ▲ +2.15%   │
│ SPY         │ ▢ NASDAQ: $14,285    │ ▢ QQQ  380.50│
│ $462.30     │   ▲ +2.15%           │   ▲ +1.80%   │
│ ▲ +2.15%    │ ▢ Russell: $1,950    │ ▢ IWM  195.20│
│             │   ▼ -0.85%           │   ▼ -0.85%   │
│ VIX: 18.5   │ ▢ Dow: $37,485       │ ▢ EWZ  42.10 │
│ Neutral     │   ▲ +0.45%           │   ▲ +1.50%   │
│             │                      │              │
│ BREADTH     │ SECTOR PERF          │ [More assets]│
│ Adv: 1,850  │ ▢ Tech   ▲ +3.2%     │              │
│ Dec: 1,225  │ ▢ Health ▼ -0.8%     │ SIGNALS      │
│ Unch: 245   │ ▢ Finance ▲ +1.5%    │ ✓ BUY Tech   │
│             │ [8 more sectors]     │ ◐ HOLD Bonds │
│             │                      │ ✗ SELL Hlth  │
└─────────────┴──────────────────────┴──────────────┘
```

### 5. AI Signals
```
┌─────────────┬──────────────────────┬──────────────┐
│ AI SIGNALS  │ SIGNAL HISTORY       │ CONFIDENCE   │
│             │ (Last 20)            │ BANDS        │
│ CURRENT     │ ▢ ▲ UP  16:45:23     │              │
│ ▲ UP        │   Conf: 87%          │ 🔴 90%+ Conf │
│             │   Vol: HIGH          │ 5 signals    │
│ Confidence  │   ✓ CORRECT          │              │
│ 87%         │ ▢ ▼ DOWN 16:42:15    │ 🟡 70-90% C.  │
│             │   Conf: 72%          │ 12 signals   │
│ Volatility  │   Vol: MEDIUM        │              │
│ HIGH        │   ✗ INCORRECT        │ 🟠 50-70% C.  │
│             │ [18 more signals]    │ 3 signals    │
│ MODEL STATS │                      │              │
│ Accuracy    │                      │ FEATURES     │
│ 78.5%       │                      │ ▢ GTI Score  │
│ Total: 145  │                      │   34% impor. │
│ Win Rate    │                      │ ▢ Volume Chg │
│ 84.3%       │                      │   28% impor. │
│             │                      │ [More...]    │
└─────────────┴──────────────────────┴──────────────┘
```

---

## 🎯 Component Styling

### Panel Header
```tsx
<div className="text-green-400 font-bold text-xs mb-3">SECTION TITLE</div>
```
- Color: Green (#4ade80)
- Font: Bold, Courier New
- Size: 0.75rem (12px)
- Margin: 12px bottom

### Panel Border
```tsx
<div className="border border-green-400/30 bg-black/80 p-4">
```
- Border: Green with 30% opacity
- Background: Black with 80% opacity
- Padding: 1rem (16px)
- Rounded: No rounded corners (hard edges)

### Data Row
```tsx
<div className="border-l-2 border-green-400/50 pl-3 py-2">
  <div className="flex justify-between mb-1">
    <span className="font-bold text-green-400">Label</span>
    <span className="text-gray-400">Value</span>
  </div>
</div>
```
- Left border: 2px solid green with 50% opacity
- Left padding: 12px
- Vertical padding: 8px
- Gap between label & value: Use flexbox with justify-between

### Alert/Status Badge
```tsx
<div className="bg-red-500/20 border border-red-500/50 p-2 rounded">
  <div className="text-red-400 font-bold">CRITICAL</div>
  <div className="text-gray-400 text-xs">Description</div>
</div>
```
- Background: Color with 20% opacity
- Border: Color with 50% opacity
- Text: Bright color (full opacity)
- Padding: 8px
- Border radius: 4px

---

## 📏 Spacing System

```
Padding:
- Panel padding: p-4 (16px)
- Section padding: p-3 (12px)
- Item padding: p-2 (8px)

Margins:
- Heading margin: mb-3 (12px)
- Card margin: mb-2 (8px)
- List item margin: py-2 (8px vertical)

Gaps:
- Grid gap: gap-4 (16px)
- Flex gap: gap-2 (8px)

Heights:
- Panel height: h-96 (384px) or flex-1 (take remaining space)
- Bar height: h-1.5 or h-2 for progress bars
```

---

## 🔤 Typography

### Heading
```tsx
<h1 className="text-2xl font-bold text-green-400 mb-2">Title</h1>
```
- Size: 1.5rem
- Weight: Bold (700)
- Color: Green

### Subheading
```tsx
<div className="text-xs text-gray-400">Subtitle</div>
```
- Size: 0.75rem
- Weight: Regular
- Color: Gray

### Data Value
```tsx
<div className="text-xl font-black text-yellow-400">782.35</div>
```
- Size: 1.25rem
- Weight: Black (900)
- Color: Yellow or green (status-based)

### Body Text
```tsx
<div className="text-xs text-gray-400">Normal paragraph text</div>
```
- Size: 0.75rem
- Weight: Regular
- Color: Gray (muted)

---

## 🎬 Animations

```css
/* Hover effect on cards */
hover:bg-green-400/10

/* Pulse animation for live indicator */
animate-pulse

/* Transition on color changes */
transition-colors

/* Smooth scrolling for overflow panels */
overflow-y-auto
```

---

## 📱 Responsive Breakpoints

```typescript
// Grid adapts based on screen size
grid-cols-4 gap-4      // Desktop (1 col + 2 col + 1 col)
@media (max-width: 1024px)
  grid-cols-1 gap-4    // Tablet/Mobile (full width)
```

---

## 🎨 Color Application Examples

### For Up/Bullish
```tsx
className="text-green-400 font-bold"  // Text green
className="border-green-400/50"       // Border green
className="bg-green-500/20"           // Background subtle green
```

### For Down/Bearish
```tsx
className="text-red-400 font-bold"    // Text red
className="border-red-500/50"         // Border red
className="bg-red-500/20"             // Background subtle red
```

### For Warning/Caution
```tsx
className="text-yellow-400 font-bold" // Text yellow
className="border-yellow-400/50"      // Border yellow
className="bg-yellow-500/20"          // Background subtle yellow
```

### For Info/Secondary
```tsx
className="text-cyan-400 font-bold"   // Text cyan
className="border-cyan-400/30"        // Border cyan
className="bg-cyan-500/20"            // Background subtle cyan
```

---

## 🔄 State Indicators

```
🟢 Green   = Safe, Stable, OK
🟡 Yellow  = Caution, Warning, Neutral
🔴 Red     = Critical, Danger, Stop
🔵 Blue    = Info, Secondary, Neutral
⚪ Gray    = Inactive, Disabled
```

---

## 📐 Grid Specifications

```typescript
// Main container
<div className="grid grid-cols-4 gap-4">

// Left sidebar (1 column)
<div className="col-span-1">

// Center (2 columns)
<div className="col-span-2">

// Right panel (1 column)
<div className="col-span-1">
</div>

// On mobile, everything becomes:
grid-cols-1 (single column, full width)
```

---

## ✅ Quick Copy-Paste Components

### Basic Panel
```tsx
<div className="border border-green-400/30 bg-black/80 p-4">
  <div className="text-green-400 font-bold text-xs mb-3">TITLE</div>
  {/* Content here */}
</div>
```

### Data Row
```tsx
<div className="border-l-2 border-green-400/50 pl-3 py-2 hover:bg-green-400/10">
  <div className="flex justify-between mb-1">
    <span className="font-bold text-green-400">Label</span>
    <span className="text-gray-400">Value</span>
  </div>
</div>
```

### Alert Badge
```tsx
<div className="bg-red-500/20 border border-red-500/50 p-2 rounded">
  <div className="text-red-400 font-bold">ALERT</div>
  <div className="text-gray-400 text-xs">Message</div>
</div>
```

---

**Use this reference when customizing or creating new NEXUS components.**
