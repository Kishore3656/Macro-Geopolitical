# Phase 5 Brief: Advanced Features & Real-Time Optimization

**Date**: 2026-05-07  
**Phase**: 5 of 6+  
**Scope**: Enhanced LLM capabilities, real-time streaming, multi-language support, confidence scoring  
**Estimated Duration**: 4-5 hours  
**Cost**: $0 (builds on existing free tier)

---

## Executive Summary

Phase 5 adds three advanced capabilities to the LLM sentiment analysis layer:

1. **Named Entity Recognition (NER)** — Extract financial entities (stocks, commodities, companies) from headlines
2. **Real-Time Streaming** — Display live sentiment updates as headlines arrive (WebSocket)
3. **Confidence Scoring** — Add statistical confidence intervals to regime predictions
4. **Multi-Language Headlines** — Extend analysis to non-English GDELT events

These features enrich the signal narrative and provide users with deeper market intelligence without additional API costs.

---

## Architecture

### 1. Named Entity Recognition (NER)

**Current State**: LLMAnalysis.entities is empty for HuggingFace (populated only by Ollama).  
**Goal**: Reliably extract financial entities (stocks, commodities, countries) from all providers.

**Implementation**:
- Use spaCy pre-trained NER model (`en_core_web_sm`, 40MB)
- Extract persons, organizations, geopolitical entities from headlines
- Enrich with custom regex patterns for stock tickers (AAPL, TSLA), commodities (Gold, Oil)
- Return top 3-5 most frequent entities in LLMAnalysis.entities

**File**: `nlp/ner.py` (NEW)  
**Class**: `EntityExtractor` with methods:
- `extract_entities(text: str) -> list[str]` — returns entity names
- `extract_financial_entities(text: str) -> dict[str, list]` — categorized entities {stocks, commodities, countries}

**Integration**: Modified `get_llm_analysis()` to also call EntityExtractor, populate LLMAnalysis.entities.

---

### 2. Real-Time Streaming via WebSocket

**Current State**: Frontend polls `/api/signals` every 60 seconds (reactive).  
**Goal**: Push sentiment updates in real-time as new headlines are analyzed.

**Implementation**:
- Add WebSocket endpoint `/ws/signals` (already exists in API, needs enhancement)
- Scheduler publishes sentiment updates via broadcast function
- Frontend subscribes to `/ws/signals`, receives updates immediately
- Example: New bullish headline arrives → Ollama analyzes → regime updated → frontend notified in <1 sec

**File**: Enhance `api/main.py` WebSocket `/ws/signals`  
**Changes**:
- Emit sentiment updates with entity extraction results
- Include confidence scores in broadcast
- Log event count (e.g., "3 bullish headlines in last 5 min")

**Frontend**: Enhance NexusAISignals to optionally subscribe to WebSocket for live updates (opt-in via settings).

---

### 3. Confidence Scoring for Regime Predictions

**Current State**: LLMAnalysis returns regime string but no confidence metric.  
**Goal**: Quantify confidence (0.0-1.0) that regime prediction is correct.

**Implementation**:
- Track regime prediction frequency over sliding window (last 10 headlines)
- If 8/10 headlines agree on regime → confidence = 0.8
- If 5/10 headlines agree → confidence = 0.5
- Add `confidence: float` field to LLMAnalysis

**File**: `nlp/llm_sentiment.py` (enhancement)  
**Logic**:
```python
# In get_llm_analysis():
recent_regimes = [fetch last 10 headline analyses]
regime_counts = Counter(r.regime for r in recent_regimes)
consensus_regime = regime_counts.most_common(1)[0][0]
confidence = regime_counts[consensus_regime] / 10.0
```

**API Response**: Include `confidence` field:
```json
{
  "regime": "risk-off",
  "confidence": 0.8,
  "narrative": "..."
}
```

**Frontend**: Display confidence as % next to regime badge (e.g., "risk-off (80%)").

---

### 4. Multi-Language Headline Analysis

**Current State**: LLM prompts and sentiment analysis are English-only.  
**Goal**: Support non-English headlines from GDELT (covers ~65% of global events).

**Implementation**:
- Use language detection library (textblob, langdetect)
- Detect language of headline before passing to LLM
- If non-English, use translate API (Google Translate free tier, ~5k req/month)
- Send translated headline to Ollama/HF for sentiment analysis
- Store both original + translated in sentiment record

**File**: `nlp/language.py` (NEW)  
**Functions**:
- `detect_language(text: str) -> str` — returns language code (en, fr, zh, etc.)
- `translate_to_english(text: str, source_lang: str) -> str` — translate to English
- `should_translate(lang: str) -> bool` — return True for non-English

**Integration**: Enhance `get_llm_analysis()` to detect language and auto-translate before sentiment analysis.

**Note**: Google Translate free tier is <5k requests/month; we get ~140 GTI cycles/day × 10 headlines = 1,400/day. Fits comfortably.

---

## Implementation Steps

### Step 1: Named Entity Recognition (60 min)
File: `nlp/ner.py` (NEW)
- Install spaCy: `pip install spacy`
- Download model: `python -m spacy download en_core_web_sm`
- Implement `EntityExtractor` class with `extract_entities()` method
- Modify `nlp/llm_sentiment.py` to call EntityExtractor in `get_llm_analysis()`
- Populate LLMAnalysis.entities with top 5 entities from headline batch

### Step 2: Real-Time WebSocket Enhancement (45 min)
File: `api/main.py` (enhance existing WebSocket)
- Update `/ws/signals` broadcast to include:
  - regime + confidence
  - entities from latest headlines
  - headline count in window
  - timestamp of latest analysis
- Test with WebSocket client (e.g., `websocat`)

### Step 3: Confidence Scoring (40 min)
File: `nlp/llm_sentiment.py` (enhancement)
- Add sliding window cache for last 10 analyses
- Compute regime consensus + confidence in `get_llm_analysis()`
- Update `LLMAnalysis` dataclass with `confidence: float`
- Update API response to include confidence

### Step 4: Multi-Language Support (50 min)
File: `nlp/language.py` (NEW)
- Implement language detection (textblob)
- Implement translation to English (Google Translate API)
- Modify `get_llm_analysis()` to auto-translate non-English headlines
- Log language + translation in debug output

### Step 5: Frontend Enhancement (30 min)
File: `frontend/src/components/dashboards/NexusAISignals.tsx`
- Add optional WebSocket subscription for live updates (opt-in via settings)
- Display confidence % next to regime badge
- Display extracted entities (financial + countries) in new card
- Update narrative to mention key entities

### Step 6: Testing & Validation (30 min)
- Test NER extraction on sample headlines
- Test WebSocket push with GTI job trigger
- Test confidence scoring with synthetic regime sequences
- Test multi-language headlines (fetch non-English from GDELT)
- Verify TypeScript + no console errors

---

## Success Criteria

✅ `EntityExtractor` class implemented, extracts 3-5 entities per headline  
✅ LLMAnalysis.entities populated in all provider chains  
✅ `/ws/signals` broadcasts regime + confidence + entities in real-time  
✅ Frontend optionally subscribes to WebSocket for live updates  
✅ Confidence score (0-1) added to regime predictions  
✅ Confidence % displayed next to regime badge  
✅ Language detection works for English, Spanish, Chinese, French, German  
✅ Non-English headlines auto-translated to English before analysis  
✅ Extracted entities displayed in UI (entities card)  
✅ No breaking changes to Phase 4 UI  
✅ All tests pass, no console errors

---

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| spaCy model download fails | Download explicitly in init script, log error clearly |
| WebSocket broadcast overwhelms frontend | Throttle broadcasts to max 1/sec, buffer on client |
| Google Translate API goes over quota | Monitor usage daily, fallback to English-only if exceeded |
| Language detection misidentifies English | Use textblob (handles ambiguous cases well) |
| Confidence scoring too low if regime volatile | Acceptable; reflects actual sentiment uncertainty |
| NER extracts irrelevant entities | Filter by confidence score from spaCy, manual blacklist |

---

## Dependencies

**New packages** (to add to `requirements.txt`):
```
spacy>=3.5.0              # NER via pre-trained model
textblob>=0.17.0          # Language detection + sentiment
google-cloud-translate>=3.11.0  # Multi-language translation (optional, fallback to textblob)
```

**Or lightweight alternative** (if avoiding Google Cloud):
```
langdetect>=1.0.9         # Language detection (smaller)
googletrans>=4.0.0        # Free Google Translate API wrapper
```

---

## Rollback Plan

If advanced features cause issues:
1. Revert `nlp/ner.py` and `nlp/language.py` additions
2. Remove confidence field from LLMAnalysis (fallback to single float sentiment_score)
3. Disable WebSocket streaming (use polling fallback)
4. NexusAISignals reverts to Phase 4 behavior (no entities card, no confidence %)

---

## Next Phase

Phase 6: Production Hardening & Deployment

---

## Sign-Off

This brief outlines Phase 5 enhancements that significantly deepen market intelligence without introducing API costs. NER + confidence scoring + real-time streaming provide traders with richer context. Multi-language support opens analysis to 65% of global GDELT events.

**Ready to implement.**

