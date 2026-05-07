# Phase 4 Brief: Frontend Integration of Regime Display & LLM Settings

**Date**: 2026-05-07  
**Phase**: 4 of 6+  
**Scope**: Frontend UI enhancements + API endpoint for LLM configuration  
**Estimated Duration**: 3-4 hours  
**Cost**: $0 (no new dependencies)

---

## Executive Summary

Phase 4 integrates the backend LLM sentiment analysis (Phase 3) into the frontend dashboard. Users will see:
1. **Regime Indicator** — Visual badge showing market regime (risk-on/off/crisis/neutral)
2. **Signal Narrative** — Live text from LLM describing current market sentiment
3. **Model Status** — Version, accuracy, drift detection, last trained time
4. **Settings Panel** — Toggle LLM on/off, select provider (Ollama/HuggingFace)

---

## Architecture

### Frontend State Management
- **New Zustand store**: `frontend/src/store/settingsStore.ts`
  - Tracks: `llm_enabled` (boolean), `llm_provider` ("ollama" | "huggingface"), `last_updated` (timestamp)
  - Persists to localStorage for browser session continuity
  - Provides actions: `toggleLLM()`, `setProvider(provider)`, `fetchSettings()`

### Type Extensions
- **`frontend/src/types/index.ts`** — Extend `SignalsData` interface:
  ```typescript
  regime?: "risk-on" | "risk-off" | "crisis" | "neutral";
  narrative?: string;
  model_version?: string;
  ```

### Component Updates
- **`NexusAISignals.tsx`** — Replace "Operator Notes" section with three cards:
  1. **Model Status Card**: Displays model_version, vol_accuracy_recent, drift_detected, last_trained_at
  2. **Regime Indicator**: Color-coded badge (green=risk-on, red=risk-off, black=crisis, gray=neutral)
  3. **Signal Narrative**: Live text from API showing sentiment context

### New Components
- **`TopBar.tsx`** — New component with:
  - Settings gear icon (top-right corner)
  - Click opens drawer with LLM toggle + provider dropdown
  - Sends settings to `POST /api/settings/llm`

### API Changes
- **New endpoint**: `POST /api/settings/llm`
  - Request: `{ llm_enabled: boolean, llm_provider: string }`
  - Response: `{ status: "success", llm_enabled: boolean, llm_provider: string }`
  - Stores settings in-memory (persists via frontend localStorage)

---

## Implementation Steps

### Step 1: Type Extensions (5 min)
File: `frontend/src/types/index.ts`
- Extend `SignalsData` interface with `regime?`, `narrative?`, `model_version?` fields
- No breaking changes to existing code

### Step 2: Settings Store (15 min)
File: `frontend/src/store/settingsStore.ts` (NEW)
- Zustand store with state: `llm_enabled`, `llm_provider`
- Actions: `toggleLLM()`, `setProvider(provider)`, `initSettings()`
- Persist to localStorage

### Step 3: Update NexusAISignals Component (40 min)
File: `frontend/src/components/dashboards/NexusAISignals.tsx`
- Replace "Operator Notes" hardcoded text with three new cards:
  - Model Status (showing version, accuracy %, drift indicator, last trained)
  - Regime Indicator (color badge)
  - Signal Narrative (text from API)
- Add useSettings hook to read LLM state
- Fetch model status from new API endpoint if available

### Step 4: Create TopBar Component (30 min)
File: `frontend/src/components/TopBar.tsx` (NEW)
- Display in main layout (header)
- Settings gear icon opens drawer
- Drawer contains: LLM toggle + provider dropdown
- On change, dispatch to settingsStore + POST to /api/settings/llm

### Step 5: API Endpoint (20 min)
File: `api/main.py`
- Add `POST /api/settings/llm` endpoint
- Accepts: `{ llm_enabled, llm_provider }`
- Stores in-memory config dict (updated via env vars at startup)
- Returns: `{ status, llm_enabled, llm_provider }`

### Step 6: Test UI (15 min)
- Start frontend dev server: `npm run dev`
- Verify regime badge displays correctly
- Verify signal narrative appears
- Test settings gear opens drawer
- Test LLM toggle + provider selector work
- Test TopBar integrates into layout

---

## Success Criteria

✅ `SignalsData` interface extended with regime, narrative, model_version  
✅ `settingsStore.ts` created with Zustand state + localStorage persistence  
✅ `NexusAISignals.tsx` displays regime badge + narrative + model status  
✅ `TopBar.tsx` created with settings gear + drawer  
✅ Settings drawer toggles LLM on/off and selects provider  
✅ `POST /api/settings/llm` endpoint functional  
✅ Frontend fetches and displays current regime from `/api/signals`  
✅ No console errors or TypeScript warnings  
✅ Settings persist across browser refresh (localStorage)

---

## Testing Strategy

### Manual Testing
1. Start API server: `python api/main.py`
2. Start frontend: `npm run dev` (in frontend/)
3. Verify NexusAISignals shows regime badge with color
4. Verify signal narrative displays text from API
5. Click settings gear → toggle LLM → verify API call succeeds
6. Change provider dropdown → verify settings persist

### API Testing
```bash
# Get current signals (includes regime + narrative)
curl http://localhost:8000/api/signals | jq '.regime, .narrative'

# Update LLM settings
curl -X POST http://localhost:8000/api/settings/llm \
  -H "Content-Type: application/json" \
  -d '{"llm_enabled": true, "llm_provider": "ollama"}'
```

---

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Type mismatch on extended SignalsData | Verify API response matches new type definition |
| Settings not persisting | Test localStorage after browser refresh |
| Settings drawer layout breaks responsive design | Test on mobile breakpoints |
| API endpoint 404 | Verify POST route registered in FastAPI |
| NexusAISignals re-renders excessively | Use React.memo or useMemo on child components |

---

## Dependencies

No new npm packages required.  
Existing: React, TypeScript, Zustand, Tailwind CSS  

---

## Rollback Plan

If settings endpoint fails:
- Frontend defaults to LLM disabled
- NexusAISignals displays narrative as informational (no feature loss)
- Revert TopBar component addition

---

## Next Phase

Phase 5: Advanced Features (streaming, multi-language NER, confidence scoring)

---

## Sign-Off

This brief outlines a complete, low-risk Phase 4 implementation. All UI changes are additive (no breaking changes). API endpoint is optional—system works without it via environment variable fallback.

**Ready to implement.**
