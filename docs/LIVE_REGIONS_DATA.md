# Live Regions Data Integration

## Overview

The Command Hub dashboard now displays **live geopolitical region data** instead of hardcoded values. Region tension scores, trade flow status, and hazard levels are computed in real-time from GDELT conflict data and displayed on the interactive map.

---

## New API Endpoint: `/api/regions`

**Route**: `GET /api/regions`  
**Interval**: Called every 60 seconds by the frontend hook  
**Response Shape**:

```json
{
  "regions": [
    {
      "id": "eastern-europe",
      "tension": 8.5,
      "tradeFlow": "UNSTABLE",
      "statusLabel": "HAZARD",
      "statusValue": "HIGH",
      "tone": "magenta",
      "timestamp": "2026-05-07T15:30:00.000Z"
    },
    ...6 regions total
  ],
  "timestamp": "2026-05-07T15:30:00.000Z"
}
```

### Region Definitions

| Region ID | Countries | Geographic Box |
|---|---|---|
| `us-east` | US | −90°W to −60°W, 25°N to 50°N |
| `eu` | DE, FR, GB, ES, IT, NL, BE | −12°W to 32°E, 35°N to 63°N |
| `eastern-europe` | RU, UA, PL, BY, RS, BA | 20°E to 48°E, 45°N to 68°N |
| `middle-east` | IR, IQ, SY, IL, YE, SA, LB | 33°E to 62°E, 10°N to 42°N |
| `kashmir` | PK, IN | 70°E to 86°E, 26°N to 40°N |
| `apac` | CN, JP, KR, TW | 98°E to 148°E, 18°N to 56°N |

---

## Computation Logic

### 1. Conflict Data Aggregation

For each region:
1. Query the `conflict_summary` table for all rows whose `country_code` matches one of the region's countries.
2. If no matching countries have conflict data, the region defaults to `tension: 0.0, tone: "green", tradeFlow: "STABLE"`.

### 2. Tension Score Formula

**Goldstein scale** (source: GDELT events):
- Range: −10 (maximally negative/conflict) to +10 (maximally positive/cooperation)
- Average is computed as a **weighted mean** across matched countries, weighted by `conflict_count` to avoid skewing from low-volume countries.

**Tension calculation**:
```
tension = (-(weighted_goldstein) + 10.0) / 2.0, clamped to [0.0, 10.0]
```

- Goldstein −10 → tension 10.0 (maximum conflict)
- Goldstein 0 → tension 5.0 (neutral)
- Goldstein +10 → tension 0.0 (maximum cooperation)

### 3. Trade Flow Status

- `"UNSTABLE"` if **any** matched country has `avg_goldstein < -5.0` (critical severity threshold)
- `"STABLE"` otherwise

### 4. Hazard Classification

- `statusValue: "HIGH"` if `tension >= 7.0`; else `"STABLE"`
- `statusLabel: "HAZARD"` if `statusValue == "HIGH"`; else `"STATUS"`

### 5. Color Tone

- `"magenta"` if `tension >= 7.0` (high conflict)
- `"yellow"` if `tension >= 4.5` (moderate)
- `"green"` if `tension < 4.5` (stable)

---

## Frontend Integration

### Hook: `useRegions()`

**Location**: `frontend/src/hooks/useRegions.ts`

```typescript
const { regions, loading, error } = useRegions();
```

**Behavior**:
- Fetches from `/api/regions` on component mount
- Polls every **60 seconds** for updates
- Returns `regions` array, `loading` boolean, `error` string or null
- Graceful fallback: returns `[]` if backend is unavailable; component falls back to static data

### Component: `CommandCenterMap`

**Location**: `frontend/src/components/dashboards/CommandCenterMap.tsx`

**Data Flow**:
1. Hook calls `useRegions()` internally
2. Static region geometry (coordinates, popupPosition, label) is loaded from `regionCards` array
3. Live data (tension, tradeFlow, statusLabel, statusValue, tone) from API is merged into each region card
4. Fallback: if live data not yet loaded, static data is retained — map never shows blank values

**Merge Example**:
```typescript
const merged: RegionCard = live
  ? {
      ...staticRegion,
      tension: live.tension,       // ← from API
      tradeFlow: live.tradeFlow,   // ← from API
      statusLabel: live.statusLabel,
      statusValue: live.statusValue,
      tone: live.tone,
    }
  : staticRegion; // fallback while loading
```

### Component: `NexusCommand`

**Location**: `frontend/src/components/dashboards/NexusCommand.tsx`

**Global Zone Readout** (three summary boxes) are now computed from live GTI data:

| Box | Derived From | Formula |
|---|---|---|
| **Tension Index** | `gti.score` | `gti.score * 10` (0–1 scale → 0–10 display) |
| **Trade Flow** | `gti.risk_level` | HIGH_CONFLICT → UNSTABLE, MODERATE_TENSION → DISRUPTED, else STABLE |
| **Hazard** | `gti.risk_level` | HIGH_CONFLICT → HIGH, MODERATE_TENSION → ELEVATED, else LOW |

Colors update dynamically:
- **High conflict** (magenta): Tension Index magenta, Trade Flow magenta, Hazard orange (#ff7557)
- **Moderate** (yellow): All three yellow
- **Low conflict** (green): All three green

No new API calls — reuses existing `useGTI()` hook which is already called on line 28.

---

## End-to-End Verification

### 1. Backend API Test

```bash
curl http://localhost:8000/api/regions
```

**Expected output**: JSON with 6 region objects. If `conflict_summary` table is empty, all regions return `tension: 0.0, tone: "green"`.

### 2. GTI Score Scale Test

```bash
curl http://localhost:8000/api/gti
```

**Expected**: `score` field is a float between 0 and 1. If `score: 0.85`, the frontend displays `Tension Index: 8.5`.

### 3. TypeScript Compilation

```bash
cd frontend
npx tsc --noEmit
```

**Expected**: Zero errors. All type imports resolve correctly.

### 4. Hook Polling Verification

1. Open browser DevTools → Network tab
2. Filter by `/api/regions`
3. **Expected**: First request fires on component mount; subsequent requests fire every 60 seconds
4. Check Response tab to verify `regions` array contains live tension values

### 5. Map Live Update Verification

1. Start backend scheduler: `python scheduler.py`
2. Start frontend: `cd frontend && npm run dev`
3. Navigate to Command Hub (home page)
4. **Expected**: Region cards show live tension scores (not hardcoded 6.5, 8.5, etc.)
5. Hover over regions on the map; popups reflect live values

### 6. Backend Unavailability Test

1. Stop the backend server
2. **Expected**: Map still renders with static fallback values (no crash, no blank panel)
3. Console shows error message in `useRegions` hook, but component gracefully degrades

### 7. Summary Boxes Live Update

1. Monitor GTI score via WebSocket or direct API poll
2. **Expected**: Tension Index, Trade Flow, and Hazard boxes update within 60 seconds of GTI change
3. Colors change to reflect new risk level

### 8. Color Validation

**Test scenario**: Simulate HIGH_CONFLICT via test data or GDELT injection

**Expected colors**:
- **Tension Index**: Magenta (`#f43de2`)
- **Trade Flow**: Magenta (`#f43de2`)
- **Hazard**: Orange (`#ff7557`)

---

## Data Freshness & Latency

| Layer | Update Interval | Latency |
|---|---|---|
| GDELT ingestion | 15 minutes | ±15 min from live events |
| GTI computation | 15 minutes (scheduler) | ±15 min from ingestion |
| `/api/regions` aggregation | Real-time (on-demand) | <100 ms |
| Frontend polling | 60 seconds | 0–60 sec from API update |
| **Total end-to-end** | 60 seconds | ~15–75 minutes from event occurrence |

---

## Troubleshooting

### Map shows old hardcoded values

1. Clear browser cache: `Ctrl+Shift+Del` → Clear browsing data → All time
2. Hard refresh frontend: `Ctrl+Shift+R`
3. Check DevTools Network tab for `/api/regions` requests — if missing, the hook is not mounted

### `Tension Index` shows `—` (dash)

- Backend not ready or `/api/gti` endpoint unreachable
- Check backend logs: `python scheduler.py` should be running
- Verify `GTI_DB` (`data/gti.db`) has data: `sqlite3 data/gti.db "SELECT COUNT(*) FROM gti_scores"`

### Region colors not changing

1. Check if `conflict_summary` has data: `sqlite3 data/gti.db "SELECT COUNT(*) FROM conflict_summary"`
2. If zero rows, scheduler has not run yet — wait 15 minutes or manually trigger: `python -c "from scheduler import run_full_cycle; run_full_cycle()"`
3. Verify GDELT files are being downloaded: check `data/gdelt_*` files modification times

### TypeScript errors after update

- Delete `node_modules` and reinstall: `cd frontend && rm -rf node_modules && npm install`
- Run type check: `npx tsc --noEmit`
