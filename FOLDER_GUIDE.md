# Folder Structure Guide - Phase 7

## Quick Navigation

```
trading-bot-geo-market-ml/
├── RUN.ps1                    ← START HERE: Main entry point
├── README.md                  ← Project overview
├── requirements.txt           ← Python dependencies
│
├── backend/                   ← Core Python application
│   ├── api/                   API endpoints (FastAPI)
│   ├── prediction/            ML models
│   │   ├── train.py           Training script
│   │   ├── predict.py         Inference script
│   │   ├── features.py        Feature engineering
│   │   └── models/            ✨ TRAINED MODELS SAVED HERE
│   │       ├── lgbm_direction.pkl       Direction model
│   │       ├── lgbm_volatility.pkl      Volatility model
│   │       ├── model_registry.json      Model versions & accuracy
│   │       └── archive/                  Versioned backups
│   ├── gti/                   Geopolitical Tension Index
│   ├── ingestion/             Data fetching
│   ├── nlp/                   NLP & sentiment analysis
│   ├── database/              DB utilities
│   └── config.py              Configuration
│
├── frontend/                  ← React/Next.js Dashboard
│   ├── src/
│   │   ├── app/               Route pages
│   │   ├── components/        React components
│   │   ├── store/             Zustand state
│   │   └── types/             TypeScript types
│   ├── package.json           NPM dependencies
│   └── .env.local             Local environment variables
│
├── scripts/                   ← Startup & utility scripts
│   ├── train-models.ps1       ← Train ML models (5-10 min)
│   ├── start-scheduler.ps1    ← Start background jobs
│   ├── start-api.ps1          ← Start REST API (port 8000)
│   ├── start-frontend.ps1     ← Start dashboard (port 3000)
│   └── run_tests.ps1          Run test suite
│
├── utils/                     ← Utility scripts
│   └── setup_and_train.py     ← Complete training pipeline
│
├── docs/                      ← Documentation
│   ├── PHASE_7_SUMMARY.md     Latest improvements
│   ├── TRAIN_INSTRUCTIONS.md  How to train models
│   ├── ML_IMPROVEMENTS.md     Technical details
│   ├── STARTUP_GUIDE.md       Getting started
│   ├── PHASE_*_BRIEF.md       Design documents
│   ├── PHASE_*_COMPLETION.md  Implementation reports
│   └── ... (19 more docs)
│
├── config/                    ← Configuration files
│   ├── .env                   Environment variables
│   └── .env.example           Template
│
├── data/                      ← Runtime databases (created automatically)
│   ├── gti.db                 Geopolitical data
│   ├── market.db              Market OHLCV data
│   ├── news.db                News & sentiment
│   └── predictions.db         Model predictions
│
├── logs/                      ← Application logs
│   └── trading_bot.log
│
└── venv/                      ← Python virtual environment
    └── Lib/site-packages/
```

## Key Takeaways

**Models:** `backend/prediction/models/lgbm_*.pkl`
**Startup:** `.\RUN.ps1 train` then `.\RUN.ps1 start`
**Docs:** See `docs/` folder for guides
**Scripts:** All in `scripts/` and `utils/`
