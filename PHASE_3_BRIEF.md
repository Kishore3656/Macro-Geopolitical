# Phase 3 Brief: Ollama-Based Sentiment & Regime Detection

**Date**: 2026-05-07  
**Status**: Pre-Implementation  
**Objective**: Add free, local LLM layer for sentiment analysis, regime detection, and signal narration

---

## Executive Summary

Phase 3 adds natural language understanding to the trading bot by integrating **Ollama** (free, local LLM) to:
1. Analyze headline sentiment and geopolitical regime (risk-on/off/crisis/neutral)
2. Generate narratives explaining model predictions (e.g., "Markets showing risk-off sentiment — GLD +2%, VIX +8%")
3. Keep all processing **100% free** and **locally hosted** (zero API costs)

---

## What We're Building

### 1. LLM Provider Abstraction (`nlp/llm_sentiment.py`)
- **OllamaProvider**: Calls local Ollama server on `http://localhost:11434`
- **HuggingFaceProvider**: Free-tier fallback (30k requests/month, no credit card)
- **NullProvider**: Falls back to VADER scores (zero LLM calls)
- Supports graceful degradation: if LLM unavailable → VADER always works

### 2. Sentiment + Regime Analysis
**Input**: Last 10 headlines (text)  
**Output** (JSON):
```json
{
  "sentiment_score": 0.65,
  "regime": "risk-on",
  "entities": ["Ukraine", "Oil", "Fed"],
  "narrative": "Geopolitical tensions easing; risk appetite returning",
  "provider_used": "ollama",
  "cached": false
}
```

**Regime Labels**:
- `risk-on`: Markets rallying, safe-haven flows out
- `risk-off`: Flight to safety (GLD/USD up), equity weakness
- `crisis`: Panic selling, circuit breakers active
- `neutral`: No clear directional bias

### 3. Integration Points
- **`gti/aggregator.py`**: After computing GTI score, call `get_llm_analysis()` on headline batch → store `regime` in `gti_scores` table
- **`/api/signals` endpoint**: Include `narrative` and `regime` in response
- **`scheduler.py`**: LLM analysis runs once per GTI cycle (every 15 min), no extra jobs needed
- **Config**: Toggle LLM on/off via `USE_LLM_SENTIMENT` environment variable

### 4. Caching & Rate Limiting
- **In-memory cache**: TTL 15 min, keyed by hash of headlines (prevents re-analyzing same news)
- **Rate limiter**: Token bucket, in-memory deque (resets on process restart)
- **Fallback**: If Ollama down or rate limited → VADER scores (never crashes pipeline)

---

## Architecture: Why Ollama?

| Feature | Ollama | OpenAI | Hugging Face Free |
|---------|--------|--------|-------------------|
| **Cost** | $0/month | $0.002-0.01/request | $0/month (30k req) |
| **Privacy** | Local, air-gapped | API, logged | API, logged |
| **Speed** | 100-200ms (GPU) | 500ms-2s (network) | 200-500ms (API) |
| **Offline** | Yes | No | No |
| **Setup** | `ollama run mistral` | API key required | API key required |
| **Model Quality** | Mistral/Llama2 (good) | GPT-4 (best) | DistilBERT (basic) |

**Decision**: Use **Ollama** as primary (free, fast, local), **HuggingFace free tier** as fallback.

---

## Implementation Plan

### Phase 3A: Config & Infrastructure
**File**: `config.py`  
Add:
```python
USE_LLM_SENTIMENT = os.getenv("USE_LLM_SENTIMENT", "false").lower() == "true"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "none")  # "ollama" | "huggingface" | "none"
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
LLM_CACHE_TTL_MINS = int(os.getenv("LLM_CACHE_TTL_MINS", "15"))
```

### Phase 3B: LLM Provider Abstraction
**File**: `nlp/llm_sentiment.py` (new)  
Implement:
- `LLMProvider` abstract base class
- `OllamaProvider` (primary)
- `HuggingFaceProvider` (free-tier fallback)
- `NullProvider` (VADER-only, zero LLM)
- `get_llm_analysis(headlines: list[str]) -> LLMAnalysis` function with caching + rate limiting

### Phase 3C: Database Schema Update
**File**: `ingestion/db.py`  
Extend `gti_scores` table:
```sql
ALTER TABLE gti_scores ADD COLUMN regime TEXT;  -- "risk-on", "risk-off", "crisis", "neutral"
```

### Phase 3D: GTI Aggregator Integration
**File**: `gti/aggregator.py`  
After computing `gti_score`, call:
```python
from nlp.llm_sentiment import get_llm_analysis
analysis = get_llm_analysis(last_10_headlines)
# Save regime to gti_scores table
```

### Phase 3E: API Integration
**File**: `api/main.py`  
Update `/api/signals` endpoint to include:
```json
{
  "model_version": "20260507_120000",
  "vol_prediction": "HIGH",
  "dir_prediction": "UP",
  "narrative": "Markets showing risk-off sentiment — GLD +2%, VIX +8%",
  "regime": "risk-off",
  "llm_enabled": true
}
```

---

## Success Criteria

| Criterion | Target | Verification |
|-----------|--------|--------------|
| **Zero API costs** | $0/month | Check API logs, no Anthropic/OpenAI charges |
| **Local deployment** | Ollama running | `curl http://localhost:11434/api/tags` returns models |
| **Sentiment in GTI** | `regime` column populated | Query `gti_scores` table, all rows have regime |
| **Narrative in signals** | `/api/signals` includes narrative | API response JSON has `narrative` field |
| **Graceful fallback** | VADER on LLM failure | Stop Ollama, verify VADER scores still returned |
| **Performance** | <500ms per prediction | Measure `/api/signals` response time |
| **Cache hit rate** | >50% in 15-min window | Log cache hits/misses |

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Ollama not running | LLM unavailable | Fallback to VADER (zero LLM calls) |
| OOM on local GPU | Model crashes | Use smaller model (neural-chat-7b vs mistral) |
| Headline batch too large | Timeout | Limit to 10 headlines max |
| Rate limiter too strict | Predictions skip LLM | Adjust token bucket size in config |
| LLM hallucinations | Bad narratives | Use structured JSON mode, validate output |

---

## Files to Create/Modify

**New Files**:
- `nlp/llm_sentiment.py` — Provider abstraction + analysis logic
- `nlp/__init__.py` — Package marker

**Modified Files**:
- `config.py` — Add LLM config keys
- `ingestion/db.py` — Add `regime` column to `gti_scores`
- `gti/aggregator.py` — Call `get_llm_analysis()`, save regime
- `api/main.py` — Include narrative + regime in `/api/signals`

**No changes to**:
- `prediction/` modules (drift, train, predict, features)
- `scheduler.py` (LLM runs in existing GTI job)
- Frontend (Phase 4)

---

## Testing Strategy

1. **Unit tests**: Mock Ollama responses, verify JSON parsing
2. **Integration tests**: Start local Ollama, run full GTI → LLM pipeline
3. **Fallback tests**: Stop Ollama, verify VADER fallback works
4. **API tests**: Call `/api/signals`, verify narrative field present
5. **Cost verification**: Run for 24 hours, confirm zero API charges

---

## Timeline

- **3A (Config)**: 15 min
- **3B (LLM abstraction)**: 1.5 hours
- **3C (Schema)**: 10 min
- **3D (GTI integration)**: 30 min
- **3E (API)**: 30 min
- **Testing**: 1 hour
- **Total**: ~4 hours

---

## Success = Phase 3 Complete When

✅ `config.py` has LLM keys  
✅ `nlp/llm_sentiment.py` exists with OllamaProvider + caching  
✅ `gti_scores` table has `regime` column  
✅ `gti/aggregator.py` calls `get_llm_analysis()` and saves regime  
✅ `/api/signals` includes `narrative` and `regime` fields  
✅ Test: Start Ollama locally, run GTI job, verify regime in database  
✅ Test: Stop Ollama, verify VADER fallback works  
✅ Cost check: Zero API charges (only local Ollama)

---

## Before You Proceed

**Prerequisites**:
1. Ollama installed: `brew install ollama` (macOS) or download from ollama.ai
2. Model pulled: `ollama pull mistral` or `ollama pull neural-chat` (one-time, ~4GB download)
3. Ollama running in background: `ollama serve`

**Optional**: HuggingFace free API key from https://huggingface.co/settings/tokens (if you want HF fallback)

---

## Sign-Off

This brief documents the **pre-implementation design** for Phase 3. All decisions are reversible; LLM is toggleable via config. If Ollama doesn't work locally, we fall back to HuggingFace free tier or VADER (zero cost either way).

**Approved for implementation**: Yes  
**Ready to push to GitHub**: Yes
