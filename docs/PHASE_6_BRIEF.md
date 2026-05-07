# Phase 6 Brief: Production Hardening & Deployment

**Date**: 2026-05-07  
**Phase**: 6 of 6 (FINAL)  
**Scope**: Error handling, logging, monitoring, documentation, CI/CD, production readiness  
**Estimated Duration**: 3-4 hours  
**Cost**: $0 (local deployment option), or minimal cloud costs (optional)

---

## Executive Summary

Phase 6 hardens the trading bot for production deployment. This includes:

1. **Comprehensive Error Handling** — Graceful degradation chains for all components
2. **Structured Logging** — Production-grade logging with levels (DEBUG, INFO, WARN, ERROR)
3. **Health Checks & Monitoring** — Endpoints to verify system health, component status
4. **Configuration Management** — Unified .env handling, validation, documentation
5. **Database Backups** — Scheduled backups of SQLite databases to persistent storage
6. **API Rate Limiting** — Protect against abuse (already have token bucket, add HTTP middleware)
7. **Documentation** — README, deployment guide, architecture diagram, troubleshooting
8. **Testing Suite** — Unit tests for core modules (NER, LLM, drift detection)
9. **CI/CD Pipeline** — GitHub Actions to auto-test on push, run linting
10. **Docker** (Optional) — Containerize for easy deployment

---

## Implementation Steps

### Step 1: Enhanced Logging Setup (45 min)

**File**: `config.py` (extend) + new `logging_setup.py`

Create centralized logging with:
- Logger levels: DEBUG, INFO, WARN, ERROR
- Structured logging to file + console
- Log rotation (max 10MB, keep 7 days)
- Request/response logging for API
- Module-specific loggers

**Code**:
```python
# logging_setup.py
import logging
import logging.handlers

def setup_logging(level=logging.INFO):
    """Configure logging for production."""
    logger = logging.getLogger("trading_bot")
    logger.setLevel(level)
    
    # File handler (rotation)
    fh = logging.handlers.RotatingFileHandler(
        "logs/trading_bot.log",
        maxBytes=10485760,  # 10MB
        backupCount=7,
    )
    
    # Console handler
    ch = logging.StreamHandler()
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
```

**Integration**: Call `setup_logging()` in `api/main.py` and `scheduler.py` on startup.

---

### Step 2: Health Check & Status Endpoints (30 min)

**File**: `api/main.py` (add endpoints)

New endpoints:
- `GET /health` — Already exists, enhance it
- `GET /api/status` — System status (all components)
- `GET /api/status/models` — Model status (version, accuracy, last trained)
- `GET /api/status/llm` — LLM status (provider, enabled, last success)
- `GET /api/status/databases` — Database status (size, row counts)

**Example Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-07T15:30:00Z",
  "components": {
    "api": "up",
    "scheduler": "running",
    "llm": "ollama (enabled)",
    "models": {
      "direction": {
        "version": "20260507_120000",
        "accuracy": 0.612,
        "last_trained": "2026-05-07T12:00:00Z"
      }
    }
  },
  "databases": {
    "news": {"status": "ok", "size_mb": 45.2, "tables": {"rss_articles": 1200}},
    "market": {"status": "ok", "size_mb": 12.1, "tables": {"ohlcv": 8500}},
    "gti": {"status": "ok", "size_mb": 3.5, "tables": {"gti_scores": 140}},
    "predictions": {"status": "ok", "size_mb": 2.1, "tables": {"predictions": 95}}
  }
}
```

---

### Step 3: Configuration Validation (20 min)

**File**: `config.py` (add validation function)

Add startup validation:
```python
def validate_config():
    """Verify all required env vars are set and valid."""
    errors = []
    
    # Check LLM config
    if USE_LLM_SENTIMENT:
        if LLM_PROVIDER == "ollama":
            if not OLLAMA_API_URL:
                errors.append("USE_LLM_SENTIMENT=true but OLLAMA_API_URL not set")
        elif LLM_PROVIDER == "huggingface":
            if not HUGGINGFACE_API_KEY:
                errors.append("LLM_PROVIDER=huggingface but HUGGINGFACE_API_KEY not set")
    
    # Check database paths
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    
    # Check required Python packages
    required_packages = ["fastapi", "pandas", "lightgbm", "nltk"]
    missing = []
    for pkg in required_packages:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        errors.append(f"Missing packages: {', '.join(missing)}. Run: pip install -r requirements.txt")
    
    if errors:
        raise RuntimeError("Config validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
    
    print("[CONFIG] Validation passed ✓")
```

Call in `api/main.py` startup and `scheduler.py` startup.

---

### Step 4: Database Backups (30 min)

**File**: new `database/backup.py`

Implement backup strategy:
```python
def backup_databases(backup_dir="backups"):
    """Create timestamped copies of all databases."""
    import shutil
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{backup_dir}/{timestamp}"
    os.makedirs(backup_path, exist_ok=True)
    
    for db_name, db_path in [
        ("news", NEWS_DB),
        ("market", MARKET_DB),
        ("gti", GTI_DB),
        ("predictions", PREDICTIONS_DB),
    ]:
        if os.path.exists(db_path):
            backup_file = f"{backup_path}/{db_name}.db"
            shutil.copy2(db_path, backup_file)
            print(f"Backed up {db_name} → {backup_file}")
    
    # Keep only last 7 days of backups
    import glob
    for old_backup in sorted(glob.glob(f"{backup_dir}/*"))[::-1][7:]:
        shutil.rmtree(old_backup)
        print(f"Removed old backup: {old_backup}")
```

Schedule via scheduler: Run daily at 2 AM.

---

### Step 5: API Rate Limiting Middleware (20 min)

**File**: `api/main.py` (add middleware)

Add rate limiting middleware to FastAPI:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Apply rate limits to endpoints
@app.get("/api/signals")
@limiter.limit("60/minute")
def get_signals_current(request: Request):
    # ... existing code
```

Limits:
- `/api/*` endpoints: 60 requests/min per IP
- `/api/signals`: 120 requests/min (frequently accessed)
- `/api/headlines`: 30 requests/min

---

### Step 6: Testing Suite (60 min)

**File**: new `tests/` directory with:
- `test_ner.py` — Test entity extraction
- `test_language.py` — Test language detection
- `test_llm_sentiment.py` — Test sentiment analysis chains
- `test_drift_detector.py` — Test drift detection logic
- `test_api.py` — Test API endpoints

Example structure:
```python
# tests/test_ner.py
import pytest
from nlp.ner import EntityExtractor

@pytest.fixture
def extractor():
    return EntityExtractor()

def test_extract_entities(extractor):
    headline = "Apple CEO visits China amid trade tensions"
    entities = extractor.extract_entities(headline)
    assert "Apple" in entities
    assert "China" in entities

def test_extract_financial_entities(extractor):
    headline = "Oil prices spike as OPEC cuts production"
    fin_entities = extractor.extract_financial_entities(headline)
    assert "oil" in [x.lower() for x in fin_entities.get("commodities", [])]
```

Run tests: `pytest tests/ -v`

---

### Step 7: Documentation (60 min)

Create comprehensive docs:

**File**: `README.md` (main documentation)
- Project overview
- Feature list
- Quick start guide
- Architecture diagram
- API reference
- Troubleshooting

**File**: `DEPLOYMENT.md` (production guide)
- System requirements
- Installation steps
- Environment variables
- Database initialization
- Running scheduler
- Health checks
- Monitoring
- Backup/restore procedures

**File**: `ARCHITECTURE.md` (technical deep-dive)
- Data flow diagram
- Component interactions
- Database schema
- API endpoints
- LLM integration details

---

### Step 8: GitHub Actions CI/CD (30 min)

**File**: `.github/workflows/test.yml`

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
      - run: python -m pylint nlp/ prediction/ api/
```

---

### Step 9: Docker Setup (Optional, 30 min)

**Files**: `Dockerfile`, `docker-compose.yml`

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "api/main.py"]
```

Enables one-command deployment: `docker-compose up`

---

### Step 10: Final Integration & Hardening (30 min)

- Add graceful shutdown handlers (cleanup on SIGTERM)
- Add request validation middleware
- Add HTTPS/TLS support for production
- Add CORS restrictions for production
- Document all environment variables
- Create deployment checklist

---

## Success Criteria

✅ All components have structured logging  
✅ `/api/status` endpoint returns full system health  
✅ Config validation runs on startup  
✅ Database backups scheduled (daily)  
✅ API rate limiting active  
✅ Test suite passes (80%+ coverage)  
✅ README + DEPLOYMENT + ARCHITECTURE docs complete  
✅ GitHub Actions CI/CD pipeline working  
✅ Docker image builds successfully  
✅ No unhandled exceptions in logs  
✅ All endpoints have error handling + logging  

---

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Disk space full from logs | Log rotation (max 10MB, keep 7 days) + monitoring |
| Database corruption | Daily backups to separate storage |
| Rate limiting too strict | Adjustable via env vars, monitor 429 responses |
| Tests too slow | Run only essential tests in CI, full suite nightly |
| Docker image too large | Multi-stage build, alpine base (optional) |

---

## Deployment Checklist

Before going to production:
- [ ] All tests pass locally
- [ ] GitHub Actions CI/CD passes
- [ ] Environment variables documented in .env.example
- [ ] Database backups tested (restore from backup)
- [ ] Health checks respond correctly
- [ ] Logs rotate properly
- [ ] API rate limiting verified
- [ ] Docker image builds and runs
- [ ] Monitoring dashboard (optional) set up
- [ ] Incident playbook documented

---

## Monitoring & Alerting (Optional, Future)

Consider adding:
- Prometheus metrics (request counts, latencies, error rates)
- Grafana dashboards (visualize system health)
- Alerting rules (send Slack/email on errors)
- APM tool (e.g., New Relic, Datadog — optional, paid)

---

## Rollback Plan

If production issues arise:
1. Health checks detect failure
2. Switch to read-only mode (no new predictions)
3. Restore from latest database backup
4. Revert API code to last known-good commit
5. Investigate logs for root cause
6. Deploy fix and test in staging
7. Re-deploy to production

---

## Next Phase

After Phase 6: Operations & Monitoring (ongoing)

---

## Sign-Off

This brief outlines a production-grade deployment for the trading bot. Phase 6 ensures the system is robust, observable, and maintainable.

**Ready to implement.**

